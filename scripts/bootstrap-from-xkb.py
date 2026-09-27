#!/usr/bin/env python3
"""One-off: write the initial .keylayout from the vendored xkb us(altgr-intl).

After the first commit the .keylayout is maintained by hand and checked with
check-layout.py; this script is kept only to document where it came from.

Usage: bootstrap-from-xkb.py [--id N] [--output PATH]
"""

import argparse
import glob
import os
import random
import re
import sys
import unicodedata

import xkb

NAME = "US AltGr Intl No Dead Keys"
DEFAULT_OUTPUT = os.path.join(xkb.REPO_ROOT, NAME + ".bundle", "Contents",
                              "Resources", NAME + ".keylayout")
LAYOUT_DIRS = [
    os.path.expanduser("~/Library/Keyboard Layouts"),
    "/Library/Keyboard Layouts",
    "/System/Library/Keyboard Layouts",
]

# Hardware keyboard types, as in Apple's own layouts: JIS types use the JIS
# key map set, everything else (ANSI and ISO) uses the ANSI set (design D3).
LAYOUTS = [
    (0, 17, "ANSI"), (18, 18, "JIS"), (21, 23, "JIS"), (30, 30, "JIS"),
    (33, 33, "JIS"), (36, 36, "JIS"), (194, 194, "JIS"), (197, 197, "JIS"),
    (200, 201, "JIS"), (206, 207, "JIS"),
]

# Modifier maps (design D2). Index -> modifier expression. Document order is
# the matching order. Unlisted modifiers must be released.
MODIFIER_MAPS = [
    (0, ""),
    (1, "anyShift"),
    (2, "caps"),
    (3, "anyShift caps"),
    (4, "anyOption"),
    (5, "anyShift anyOption"),
    (6, "caps anyOption"),
    (7, "anyShift caps anyOption"),
    (8, "command caps? anyOption?"),
    (10, "anyShift command caps? anyOption?"),
    (9, "anyControl anyShift? caps? anyOption? command?"),
]
MAP_COUNT = 11

# Non-character keys (design D4): the same output in every map.
FUNCTION_KEY = "\x10"
SPECIAL_KEYS = {
    36: "\r", 48: "\t", 49: " ", 51: "\x08", 52: "\x03", 53: "\x1b",
    71: "\x1b", 76: "\x03", 114: "\x05", 115: "\x01", 116: "\x0b",
    117: "\x7f", 119: "\x04", 121: "\x0c",
    123: "\x1c", 124: "\x1d", 125: "\x1f", 126: "\x1e",
    # Keypad.
    65: ".", 67: "*", 69: "+", 75: "/", 78: "-", 81: "=",
    82: "0", 83: "1", 84: "2", 85: "3", 86: "4", 87: "5", 88: "6", 89: "7",
    91: "8", 92: "9",
}
for code in (122, 120, 99, 118, 96, 97, 98, 100, 101, 109, 103, 111,
             105, 107, 113, 106, 64, 79, 80, 90):  # F1-F20
    SPECIAL_KEYS[code] = FUNCTION_KEY

JIS_KEYPAD_COMMA = 95

# Control+key characters that differ from the key's base character.
CONTROL_CHARS = {"[": "\x1b", "\\": "\x1c", "]": "\x1d"}


def control_char(base):
    if "a" <= base <= "z":
        return chr(ord(base) - ord("a") + 1)
    return CONTROL_CHARS.get(base, base)


def character_maps(chars):
    """Return the output of one key for maps 0..10."""
    c1, c2 = chars[0], chars[1]
    maps = xkb.all_layers(chars)  # 0-3 plain layers, then 4-7 caps layers
    plain, caps = maps[:4], maps[4:]
    return [
        plain[0], plain[1], caps[0], caps[1],      # 0 base, 1 shift, 2-3 caps
        plain[2], plain[3], caps[2], caps[3],      # 4-5 option, 6-7 caps
        c1, control_char(c1), c2,                  # 8 command, 9 control, 10
    ]


def encode(ch):
    if (ch in "&<>\"'" or ord(ch) < 0x20 or ord(ch) == 0x7F
            or unicodedata.category(ch).startswith("M")):
        return "&#x%04X;" % ord(ch)
    return ch


def installed_ids():
    ids = set()
    for d in LAYOUT_DIRS:
        for path in glob.glob(os.path.join(d, "**", "*.keylayout"), recursive=True):
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    m = re.search(r'<keyboard\b[^>]*\bid="(-?\d+)"', f.read(4096))
            except OSError:
                continue
            if m:
                ids.add(int(m.group(1)))
    return ids


def pick_id():
    taken = installed_ids()
    rng = random.SystemRandom()
    while True:
        candidate = -rng.randint(2, 32767)
        if candidate not in taken:
            return candidate


def render(layout_id):
    chars = xkb.layers()
    keys = {}  # key code -> outputs for maps 0..10
    for name, code in xkb.MAC_KEYCODES.items():
        keys[code] = character_maps(chars[name])
    for code, out in SPECIAL_KEYS.items():
        keys[code] = [out] * MAP_COUNT

    lines = [
        '<?xml version="1.1" encoding="UTF-8"?>',
        '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">',
        "<!-- Derived from xkeyboard-config symbols/us(altgr-intl); see vendor/xkeyboard-config. -->",
        '<keyboard group="126" id="%d" name="%s" maxout="1">' % (layout_id, NAME),
        "    <layouts>",
    ]
    for first, last, map_set in LAYOUTS:
        lines.append('        <layout first="%d" last="%d" mapSet="%s" modifiers="Modifiers"/>'
                     % (first, last, map_set))
    lines += ["    </layouts>", '    <modifierMap id="Modifiers" defaultIndex="0">']
    for index, expr in MODIFIER_MAPS:
        lines += ['        <keyMapSelect mapIndex="%d">' % index,
                  '            <modifier keys="%s"/>' % expr,
                  "        </keyMapSelect>"]
    lines += ["    </modifierMap>", '    <keyMapSet id="ANSI">']
    for index in range(MAP_COUNT):
        lines.append('        <keyMap index="%d">' % index)
        for code in sorted(keys):
            lines.append('            <key code="%d" output="%s"/>'
                         % (code, encode(keys[code][index])))
        lines.append("        </keyMap>")
    lines += ["    </keyMapSet>", '    <keyMapSet id="JIS">']
    # macOS rejects the whole layout if a keyMap is empty, so each JIS map
    # defines the JIS keypad comma and inherits everything else from ANSI.
    for index in range(MAP_COUNT):
        lines += ['        <keyMap index="%d" baseMapSet="ANSI" baseIndex="%d">' % (index, index),
                  '            <key code="%d" output=","/>' % JIS_KEYPAD_COMMA,
                  "        </keyMap>"]
    lines += ["    </keyMapSet>", "</keyboard>", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--id", type=int, help="keyboard id (default: random, unused)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    layout_id = args.id if args.id is not None else pick_id()
    if not -32768 <= layout_id <= -2:
        parser.error("--id must be between -32768 and -2")
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(render(layout_id))
    print("wrote %s (id %d)" % (args.output, layout_id))
    return 0


if __name__ == "__main__":
    sys.exit(main())
