#!/usr/bin/env python3
"""Validate the keyboard layout bundle against xkb us(altgr-intl).

Usage: check-layout.py [BUNDLE]

BUNDLE defaults to the bundle in the repository root. Prints one line per
finding and exits 1 if there are any; exits 0 otherwise. Works offline: the
reference is the vendored xkeyboard-config copy.
"""

import itertools
import os
import plistlib
import re
import sys
import xml.etree.ElementTree as ET

import xkb

NAME = "US AltGr Intl No Dead Keys"
BUNDLE_ID = "com.ajmasia.keyboardlayout.us-altgr-intl-no-dead-keys"
DEFAULT_BUNDLE = os.path.join(xkb.REPO_ROOT, NAME + ".bundle")

MODIFIERS = ["shift", "caps", "option", "command", "control"]
TOKEN_GROUPS = {
    "shift": "shift", "rightShift": "shift", "anyShift": "shift",
    "option": "option", "rightOption": "option", "anyOption": "option",
    "control": "control", "rightControl": "control", "anyControl": "control",
    "command": "command", "caps": "caps",
}
# Modifier states of the eight character layers, in xkb.all_layers() order.
LAYER_STATES = [
    ((), "Base"), (("shift",), "Shift"), (("option",), "Option"),
    (("shift", "option"), "Shift+Option"), (("caps",), "Caps"),
    (("shift", "caps"), "Shift+Caps"), (("caps", "option"), "Caps+Option"),
    (("shift", "caps", "option"), "Shift+Caps+Option"),
]

# XML 1.0 parsers reject control-character references that keylayouts use
# (for example &#x0010; for function keys). They are parsed as private-use
# placeholders and mapped back when reading outputs.
PLACEHOLDER_BASE = 0xE000


def _placeholder(match):
    code = int(match.group(1), 16)
    if code < 0x20 and code not in (0x09, 0x0A, 0x0D):
        return "&#x%X;" % (PLACEHOLDER_BASE + code)
    return match.group(0)


def _restore(text):
    if text is None:
        return None
    return "".join(chr(ord(c) - PLACEHOLDER_BASE)
                   if PLACEHOLDER_BASE <= ord(c) < PLACEHOLDER_BASE + 0x20 else c
                   for c in text)


def state_name(mods):
    names = [m.capitalize() for m in MODIFIERS if m in mods]
    return "+".join(names) or "Base"


def describe(value):
    if value is None:
        return "nothing"
    kind, text = value
    if kind == "dead":
        return "dead key (state %s)" % text
    return " ".join("%s (U+%04X)" % (c if c.isprintable() else "", ord(c))
                    for c in text).strip() or "empty"


class Keylayout:
    def __init__(self, path):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        self.raw = text
        text = re.sub(r"&#x([0-9A-Fa-f]+);", _placeholder, text)
        text = re.sub(r'^<\?xml version="1\.1"', '<?xml version="1.0"', text)
        self.root = ET.fromstring(text.encode("utf-8"))
        self.name = self.root.get("name")

        mod_map = self.root.find("modifierMap")
        self.default_index = int(mod_map.get("defaultIndex", "0"))
        self.selects = [(int(s.get("mapIndex")),
                         [m.get("keys", "") for m in s.findall("modifier")])
                        for s in mod_map.findall("keyMapSelect")]

        ansi = [lay for lay in self.root.find("layouts").findall("layout")
                if int(lay.get("first")) == 0]
        self.map_set_id = ansi[0].get("mapSet") if ansi else None
        self.map_sets = {}
        for ms in self.root.findall("keyMapSet"):
            maps = {}
            for km in ms.findall("keyMap"):
                base = km.get("baseMapSet")
                maps[int(km.get("index"))] = (
                    (base, int(km.get("baseIndex", km.get("index")))) if base else None,
                    {int(k.get("code")): k for k in km.findall("key")})
            self.map_sets[ms.get("id")] = maps
        self.actions = {a.get("id"): a for a in self.root.iter("action")
                        if a.get("id") is not None}

    def map_index(self, mods):
        for index, exprs in self.selects:
            if any(_matches(expr, mods) for expr in exprs):
                return index
        return self.default_index

    def key_codes(self):
        codes = set()
        for base, keys in self.map_sets.get(self.map_set_id, {}).values():
            codes.update(keys)
        return sorted(codes)

    def _key(self, map_set, index, code, depth=0):
        maps = self.map_sets.get(map_set, {})
        if index not in maps or depth > 4:
            return None
        base, keys = maps[index]
        if code in keys:
            return keys[code]
        if base:
            return self._key(base[0], base[1], code, depth + 1)
        return None

    def resolve(self, code, mods):
        """Return ("out", text), ("dead", state) or None for a keystroke."""
        key = self._key(self.map_set_id, self.map_index(mods), code)
        if key is None:
            return None
        if key.get("output") is not None:
            return ("out", _restore(key.get("output")))
        action = key.find("action")
        if action is None:
            action = self.actions.get(key.get("action"))
        if action is None:
            return None
        for when in action.findall("when"):
            if when.get("state") == "none":
                if when.get("next"):
                    return ("dead", when.get("next"))
                return ("out", _restore(when.get("output")))
        return None


def _matches(expr, mods):
    required, optional = set(), set()
    for token in expr.split():
        opt = token.endswith("?")
        group = TOKEN_GROUPS.get(token.rstrip("?"))
        if group is None:
            continue
        (optional if opt else required).add(group)
    return required <= set(mods) and set(mods) <= required | optional


def check_mapping(layout, findings):
    chars = xkb.layers()
    for name, code in sorted(xkb.MAC_KEYCODES.items(), key=lambda kv: kv[1]):
        expected_layers = xkb.all_layers(chars[name])
        for (mods, layer), expected in zip(LAYER_STATES, expected_layers):
            actual = layout.resolve(code, mods)
            if actual != ("out", expected):
                findings.append("key %s / %s / expected %s / actual %s" % (
                    xkb.key_label(name, chars[name]), layer,
                    describe(("out", expected)), describe(actual)))


def check_structure(layout, findings):
    # macOS silently drops the whole layout if any keyMap has no keys.
    for ms in layout.root.findall("keyMapSet"):
        for km in ms.findall("keyMap"):
            if not km.findall("key"):
                findings.append("structure: keyMap %s in keyMapSet %s is empty"
                                % (km.get("index"), ms.get("id")))


def check_dead_keys(layout, findings):
    if layout.root.find("terminators") is not None:
        findings.append("dead keys: <terminators> element present")
    for action_id, action in layout.actions.items():
        for when in action.findall("when"):
            if when.get("next"):
                findings.append("dead keys: action %s enters state %s"
                                % (action_id, when.get("next")))
    for code in layout.key_codes():
        for n in range(len(MODIFIERS) + 1):
            for mods in itertools.combinations(MODIFIERS, n):
                result = layout.resolve(code, mods)
                if result and result[0] == "dead":
                    findings.append("dead keys: key code %d / %s / %s"
                                    % (code, state_name(mods), describe(result)))


def _non_ascii(result):
    return result and result[0] == "out" and any(ord(c) > 0x7F for c in result[1])


def check_ascii_layers(layout, findings):
    for code in layout.key_codes():
        for mods in ((), ("shift",)):
            result = layout.resolve(code, mods)
            if _non_ascii(result):
                findings.append("non-ASCII in %s layer: key code %d / %s"
                                % (state_name(mods), code, describe(result)))


def check_shortcut_maps(layout, findings):
    for code in layout.key_codes():
        for n in range(len(MODIFIERS) + 1):
            for mods in itertools.combinations(MODIFIERS, n):
                if "command" not in mods and "control" not in mods:
                    continue
                result = layout.resolve(code, mods)
                if result and (result[0] == "dead" or any(ord(c) > 0x7F for c in result[1])):
                    findings.append("shortcut map not ASCII: key code %d / %s / %s"
                                    % (code, state_name(mods), describe(result)))


def check_bundle(bundle, layout, findings):
    name = os.path.basename(os.path.normpath(bundle))
    if not name.endswith(".bundle"):
        findings.append("bundle: directory %r does not end in .bundle" % name)
    name = name[:-len(".bundle")] if name.endswith(".bundle") else name
    if name != NAME:
        findings.append("bundle: directory name %r, expected %r" % (name, NAME))
    resources = os.path.join(bundle, "Contents", "Resources")
    for ext in ("keylayout", "icns"):
        if not os.path.isfile(os.path.join(resources, "%s.%s" % (name, ext))):
            findings.append("bundle: missing Resources/%s.%s" % (name, ext))
    if layout is not None and layout.name != name:
        findings.append("bundle: keylayout name attribute %r does not match bundle %r"
                        % (layout.name, name))
    info_path = os.path.join(bundle, "Contents", "Info.plist")
    try:
        with open(info_path, "rb") as f:
            info = plistlib.load(f)
    except (OSError, plistlib.InvalidFileException) as e:
        findings.append("bundle: cannot read Info.plist (%s)" % e)
        return
    if info.get("CFBundleIdentifier") != BUNDLE_ID:
        findings.append("bundle: CFBundleIdentifier %r, expected %r"
                        % (info.get("CFBundleIdentifier"), BUNDLE_ID))
    kl_keys = [k for k in info if k.startswith("KLInfo_")]
    if kl_keys != ["KLInfo_" + name]:
        findings.append("bundle: Info.plist has %s, expected KLInfo_%s"
                        % (", ".join(kl_keys) or "no KLInfo_ key", name))


def validate(bundle):
    findings = []
    name = os.path.basename(os.path.normpath(bundle))[:-len(".bundle")]
    path = os.path.join(bundle, "Contents", "Resources", name + ".keylayout")
    layout = None
    try:
        layout = Keylayout(path)
    except (OSError, ET.ParseError) as e:
        findings.append("keylayout: cannot load %s (%s)" % (path, e))
    if layout is not None:
        check_structure(layout, findings)
        check_mapping(layout, findings)
        check_dead_keys(layout, findings)
        check_ascii_layers(layout, findings)
        check_shortcut_maps(layout, findings)
    check_bundle(bundle, layout, findings)
    return findings


def main(argv):
    if len(argv) > 2 or (len(argv) == 2 and argv[1].startswith("-")):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    bundle = argv[1] if len(argv) == 2 else DEFAULT_BUNDLE
    findings = validate(bundle)
    for line in findings:
        print(line)
    if findings:
        print("%d finding(s)" % len(findings), file=sys.stderr)
        return 1
    print("OK: %s matches xkb us(%s)" % (os.path.basename(bundle), xkb.VARIANT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
