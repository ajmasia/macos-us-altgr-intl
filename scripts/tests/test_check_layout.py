import os
import plistlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(SCRIPTS)
CHECK = os.path.join(SCRIPTS, "check-layout.py")
NAME = "US AltGr Intl No Dead Keys"
KEYLAYOUT = os.path.join(REPO_ROOT, NAME + ".bundle", "Contents", "Resources",
                         NAME + ".keylayout")

DEAD_ACTIONS = """    <actions>
        <action id="apostrophe">
            <when state="none" next="acute"/>
            <when state="acute" output="&#x00E1;"/>
        </action>
    </actions>
    <terminators>
        <when state="acute" output="&#x0027;"/>
    </terminators>
</keyboard>"""


class CheckLayoutTest(unittest.TestCase):
    """Runs check-layout.py on a fixture bundle built from the shipped
    .keylayout, with a valid Info.plist and a placeholder .icns."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.bundle = os.path.join(self.tmp, NAME + ".bundle")
        resources = os.path.join(self.bundle, "Contents", "Resources")
        os.makedirs(resources)
        with open(KEYLAYOUT, encoding="utf-8") as f:
            self.keylayout_text = f.read()
        self.keylayout = os.path.join(resources, NAME + ".keylayout")
        self.write_keylayout(self.keylayout_text)
        with open(os.path.join(resources, NAME + ".icns"), "wb") as f:
            f.write(b"icns\x00\x00\x00\x08")
        self.write_info({
            "CFBundleIdentifier": "com.ajmasia.keyboardlayout.us-altgr-intl-no-dead-keys",
            "KLInfo_" + NAME: {"TISIntendedLanguage": "en"},
        })

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write_keylayout(self, text):
        with open(self.keylayout, "w", encoding="utf-8") as f:
            f.write(text)

    def write_info(self, info):
        with open(os.path.join(self.bundle, "Contents", "Info.plist"), "wb") as f:
            plistlib.dump(info, f)

    def set_key(self, map_index, code, attrs):
        """Replace a key in keyMap map_index of the ANSI key map set."""
        text = self.keylayout_text
        start = text.index('<keyMap index="%d">' % map_index)
        end = text.index("</keyMap>", start)
        block, n = re.subn(r'<key code="%d" [^/]*/>' % code,
                           '<key code="%d" %s/>' % (code, attrs), text[start:end])
        self.assertEqual(n, 1)
        self.keylayout_text = text[:start] + block + text[end:]
        self.write_keylayout(self.keylayout_text)

    def run_check(self):
        proc = subprocess.run([sys.executable, CHECK, self.bundle],
                              capture_output=True, text=True)
        return proc.returncode, proc.stdout

    def test_fixture_passes(self):
        code, out = self.run_check()
        self.assertEqual(out.strip().splitlines()[-1][:3], "OK:", out)
        self.assertEqual(code, 0)

    def test_wrong_character(self):
        self.set_key(5, 9, 'output="&#x00AE;"')  # Shift+Option+v: ® instead of ™
        code, out = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("key v (AB04) / Shift+Option / expected ™ (U+2122) "
                      "/ actual ® (U+00AE)", out)

    def test_dead_key_under_caps(self):
        self.set_key(2, 39, 'action="apostrophe"')  # Caps + '
        self.keylayout_text = self.keylayout_text.replace("</keyboard>", DEAD_ACTIONS)
        self.write_keylayout(self.keylayout_text)
        code, out = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("dead keys: key code 39 / Caps / dead key (state acute)", out)
        self.assertIn("dead keys: <terminators> element present", out)
        self.assertIn("key ' (AC11) / Caps / expected ' (U+0027) "
                      "/ actual dead key (state acute)", out)

    def test_non_ascii_shift_layer(self):
        self.set_key(1, 22, 'output="&#x02C6;"')  # Shift+6: ˆ instead of ^
        code, out = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("non-ASCII in Shift layer: key code 22 / ˆ (U+02C6)", out)

    def test_caps_option(self):
        self.set_key(6, 0, 'output="&#x00E1;"')  # Caps+Option+a: á instead of Á
        code, out = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("key a (AC01) / Caps+Option / expected Á (U+00C1) "
                      "/ actual á (U+00E1)", out)

    def test_non_ascii_command_map(self):
        self.set_key(8, 0, 'output="&#x00E1;"')
        code, out = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("shortcut map not ASCII: key code 0 / Command / á (U+00E1)", out)

    def test_empty_keymap(self):
        self.keylayout_text = self.keylayout_text.replace(
            '<keyMap index="3" baseMapSet="ANSI" baseIndex="3">\n'
            '            <key code="95" output=","/>\n'
            '        </keyMap>',
            '<keyMap index="3" baseMapSet="ANSI" baseIndex="3"/>')
        self.write_keylayout(self.keylayout_text)
        code, out = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("structure: keyMap 3 in keyMapSet JIS is empty", out)

    def test_klinfo_mismatch(self):
        self.write_info({
            "CFBundleIdentifier": "com.ajmasia.keyboardlayout.us-altgr-intl-no-dead-keys",
            "KLInfo_Intl AltGr": {"TISIntendedLanguage": "en"},
        })
        code, out = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("bundle: Info.plist has KLInfo_Intl AltGr, "
                      "expected KLInfo_US AltGr Intl No Dead Keys", out)


if __name__ == "__main__":
    unittest.main()
