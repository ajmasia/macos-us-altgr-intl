"""Read xkeyboard-config symbols and resolve the us(altgr-intl) layout.

Shared by bootstrap-from-xkb.py and check-layout.py so that both read xkb the
same way. Standard library only.
"""

import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENDORED_US = os.path.join(REPO_ROOT, "vendor", "xkeyboard-config", "symbols", "us")
VARIANT = "altgr-intl"

# Includes of other symbols files only define modifier keys (for example the
# AltGr level-3 switch), so they are skipped. Anything else is an error.
IGNORED_INCLUDE_FILES = {"level3"}

# xkb key name -> macOS virtual key code (ANSI positions).
MAC_KEYCODES = {
    "TLDE": 50, "AE01": 18, "AE02": 19, "AE03": 20, "AE04": 21, "AE05": 23,
    "AE06": 22, "AE07": 26, "AE08": 28, "AE09": 25, "AE10": 29, "AE11": 27,
    "AE12": 24,
    "AD01": 12, "AD02": 13, "AD03": 14, "AD04": 15, "AD05": 17, "AD06": 16,
    "AD07": 32, "AD08": 34, "AD09": 31, "AD10": 35, "AD11": 33, "AD12": 30,
    "AC01": 0, "AC02": 1, "AC03": 2, "AC04": 3, "AC05": 5, "AC06": 4,
    "AC07": 38, "AC08": 40, "AC09": 37, "AC10": 41, "AC11": 39, "BKSL": 42,
    "AB01": 6, "AB02": 7, "AB03": 8, "AB04": 9, "AB05": 11, "AB06": 45,
    "AB07": 46, "AB08": 43, "AB09": 47, "AB10": 44,
    "LSGT": 10,
}

# Keysym names used by us(basic), us(intl) and us(altgr-intl). Single letters
# and digits, and Uxxxx names, are handled in keysym_to_char().
KEYSYMS = {
    "space": " ", "exclam": "!", "quotedbl": '"', "numbersign": "#",
    "dollar": "$", "percent": "%", "ampersand": "&", "apostrophe": "'",
    "parenleft": "(", "parenright": ")", "asterisk": "*", "plus": "+",
    "comma": ",", "minus": "-", "period": ".", "slash": "/", "colon": ":",
    "semicolon": ";", "less": "<", "equal": "=", "greater": ">",
    "question": "?", "at": "@", "bracketleft": "[", "backslash": "\\",
    "bracketright": "]", "asciicircum": "^", "underscore": "_", "grave": "`",
    "braceleft": "{", "bar": "|", "braceright": "}", "asciitilde": "~",
    "exclamdown": "¡", "cent": "¢", "sterling": "£",
    "currency": "¤", "yen": "¥", "brokenbar": "¦",
    "section": "§", "copyright": "©", "guillemotleft": "«",
    "notsign": "¬", "registered": "®", "degree": "°",
    "plusminus": "±", "twosuperior": "²", "threesuperior": "³",
    "mu": "µ", "paragraph": "¶", "periodcentered": "·",
    "onesuperior": "¹", "guillemotright": "»",
    "onequarter": "¼", "onehalf": "½", "threequarters": "¾",
    "questiondown": "¿", "Aacute": "Á", "Adiaeresis": "Ä",
    "Aring": "Å", "AE": "Æ", "Ccedilla": "Ç",
    "Eacute": "É", "Ediaeresis": "Ë", "Iacute": "Í",
    "Idiaeresis": "Ï", "ETH": "Ð", "Ntilde": "Ñ",
    "Oacute": "Ó", "Odiaeresis": "Ö", "multiply": "×",
    "Oslash": "Ø", "Uacute": "Ú", "Udiaeresis": "Ü",
    "THORN": "Þ", "ssharp": "ß", "aacute": "á",
    "adiaeresis": "ä", "aring": "å", "ae": "æ",
    "ccedilla": "ç", "eacute": "é", "ediaeresis": "ë",
    "iacute": "í", "idiaeresis": "ï", "eth": "ð",
    "ntilde": "ñ", "oacute": "ó", "odiaeresis": "ö",
    "division": "÷", "oslash": "ø", "uacute": "ú",
    "udiaeresis": "ü", "thorn": "þ", "OE": "Œ", "oe": "œ",
    "leftsinglequotemark": "‘", "rightsinglequotemark": "’",
    "leftdoublequotemark": "“", "rightdoublequotemark": "”",
    "EuroSign": "€", "trademark": "™",
}

# The 17 dead keys of us(altgr-intl) and the character each position emits
# instead (keyboard-layout spec). Levels are 1-based as in xkb.
DEAD_KEY_REPLACEMENTS = [
    ("TLDE", 3, "dead_grave", "`"),
    ("TLDE", 4, "dead_tilde", "~"),
    ("AC11", 3, "dead_acute", "´"),
    ("AC11", 4, "dead_diaeresis", "¨"),
    ("AE02", 4, "dead_doubleacute", "˝"),
    ("AE03", 4, "dead_macron", "¯"),
    ("AE05", 4, "dead_cedilla", "¸"),
    ("AE06", 3, "dead_circumflex", "ˆ"),
    ("AE07", 3, "dead_horn", "\u031b"),
    ("AE08", 3, "dead_ogonek", "˛"),
    ("AE09", 4, "dead_breve", "˘"),
    ("AE10", 4, "dead_abovering", "˚"),
    ("AE11", 4, "dead_belowdot", "\u0323"),
    ("AB09", 3, "dead_abovedot", "˙"),
    ("AB09", 4, "dead_caron", "ˇ"),
    ("AB10", 4, "dead_hook", "\u0309"),
    ("AB05", 4, "dead_stroke", "\u0338"),
]

LAYER_NAMES = ["Base", "Shift", "Option", "Shift+Option"]
CAPS_LAYER_NAMES = ["Caps", "Shift+Caps", "Caps+Option", "Shift+Caps+Option"]


class XkbError(Exception):
    pass


def is_dead(keysym):
    return keysym.startswith("dead_")


def keysym_to_char(keysym):
    if is_dead(keysym):
        raise XkbError("dead keysym has no character: %s" % keysym)
    if len(keysym) == 1:
        return keysym
    if re.fullmatch(r"U[0-9A-Fa-f]{4,6}", keysym):
        return chr(int(keysym[1:], 16))
    if keysym in KEYSYMS:
        return KEYSYMS[keysym]
    raise XkbError("unknown keysym: %s" % keysym)


def _strip_comments(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"//[^\n]*", "", text)


def parse_symbols(path):
    """Return {variant: [statement, ...]} for an xkb symbols file.

    Statements are ("include", "file(variant)") or ("key", name, [keysyms])
    in file order.
    """
    with open(path, encoding="utf-8") as f:
        text = _strip_comments(f.read())
    variants = {}
    for m in re.finditer(r'xkb_symbols\s+"([^"]+)"\s*\{(.*?)\n\};', text, re.S):
        body = m.group(2)
        statements = []
        stmt_re = re.compile(
            r'include\s+"([^"]+)"|key\s+<(\w+)>\s*\{\s*\[([^\]]*)\]', re.S)
        for s in stmt_re.finditer(body):
            if s.group(1):
                statements.append(("include", s.group(1)))
            else:
                syms = [x.strip() for x in s.group(3).split(",")]
                statements.append(("key", s.group(2), syms))
        variants[m.group(1)] = statements
    return variants


def resolve(path=VENDORED_US, variant=VARIANT):
    """Resolve a variant of the given symbols file, following includes.

    Returns {xkb key name: [keysym level 1..4]}. Later definitions override
    earlier ones level by level, as xkb's default include merge mode does.
    """
    variants = parse_symbols(path)
    file_name = os.path.basename(path)

    def apply(name, keys, seen):
        if name in seen:
            raise XkbError("include loop at %s" % name)
        if name not in variants:
            raise XkbError("variant not found: %s(%s)" % (file_name, name))
        for stmt in variants[name]:
            if stmt[0] == "include":
                m = re.fullmatch(r"(\w[\w-]*)(?:\(([\w-]+)\))?", stmt[1])
                if not m:
                    raise XkbError("cannot parse include: %s" % stmt[1])
                inc_file, inc_variant = m.group(1), m.group(2) or "basic"
                if inc_file == file_name:
                    apply(inc_variant, keys, seen | {name})
                elif inc_file not in IGNORED_INCLUDE_FILES:
                    raise XkbError("unsupported include: %s" % stmt[1])
            else:
                _, key, syms = stmt
                levels = keys.setdefault(key, [None] * 4)
                for i, sym in enumerate(syms[:4]):
                    if sym:
                        levels[i] = sym
        return keys

    return apply(variant, {}, set())


def replacement_table():
    """Return {(key, level): (dead keysym, replacement character)}."""
    return {(k, lvl): (dead, ch) for k, lvl, dead, ch in DEAD_KEY_REPLACEMENTS}


def layers(path=VENDORED_US, variant=VARIANT):
    """Return {xkb key name: [char level 1..4]} with dead keys replaced.

    Raises XkbError if a dead key is not covered by the replacement table or a
    table entry does not match the reference.
    """
    table = replacement_table()
    result = {}
    for key, syms in resolve(path, variant).items():
        chars = []
        for i, sym in enumerate(syms, start=1):
            if sym is None:
                raise XkbError("%s has no level %d" % (key, i))
            entry = table.get((key, i))
            if entry is not None:
                if sym != entry[0]:
                    raise XkbError("%s level %d is %s, table expects %s"
                                   % (key, i, sym, entry[0]))
                chars.append(entry[1])
            elif is_dead(sym):
                raise XkbError("%s level %d: unhandled dead key %s" % (key, i, sym))
            else:
                chars.append(keysym_to_char(sym))
        result[key] = chars
    for key, lvl in table:
        if key not in result:
            raise XkbError("replacement for unknown key %s" % key)
    return result


def is_case_pair(lower, upper):
    """True if lower/upper are a lowercase/uppercase pair of one letter."""
    return (lower != upper and lower.islower() and upper.isupper()
            and lower.upper() == upper and upper.lower() == lower)


def key_type(chars):
    """Classify a four-level key the way xkb's automatic key types do."""
    if is_case_pair(chars[0], chars[1]):
        if is_case_pair(chars[2], chars[3]):
            return "FOUR_LEVEL_ALPHABETIC"
        return "FOUR_LEVEL_SEMIALPHABETIC"
    return "FOUR_LEVEL"


def caps_layers(chars):
    """Characters for Caps, Shift+Caps, Caps+Option and Shift+Caps+Option.

    Caps Lock swaps a level pair only when the pair is a case pair (design D2).
    """
    c1, c2, c3, c4 = chars
    pair12, pair34 = is_case_pair(c1, c2), is_case_pair(c3, c4)
    return [c2 if pair12 else c1, c1 if pair12 else c2,
            c4 if pair34 else c3, c3 if pair34 else c4]


def all_layers(chars):
    """The eight character layers of a key: LAYER_NAMES then CAPS_LAYER_NAMES."""
    return list(chars) + caps_layers(chars)


def key_label(key, chars):
    """Human-readable key name, e.g. "v (AB04)"."""
    return "%s (%s)" % (chars[0], key)
