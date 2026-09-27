import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xkb  # noqa: E402


class ResolveTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.syms = xkb.resolve()
        cls.chars = xkb.layers()

    def test_altgr_intl_overrides_intl(self):
        # us(intl) makes AC11 dead on levels 1/2; altgr-intl moves them to 3/4.
        self.assertEqual(self.syms["AC11"],
                         ["apostrophe", "quotedbl", "dead_acute", "dead_diaeresis"])
        self.assertEqual(self.syms["AE06"],
                         ["6", "asciicircum", "dead_circumflex", "onequarter"])
        self.assertEqual(self.syms["AB05"],
                         ["b", "B", "periodcentered", "dead_stroke"])

    def test_keys_inherited_from_intl(self):
        self.assertEqual(self.chars["AC01"], ["a", "A", "á", "Á"])
        self.assertEqual(self.chars["AB06"], ["n", "N", "ñ", "Ñ"])
        self.assertEqual(self.chars["AB10"][2], "¿")

    def test_lsgt(self):
        self.assertEqual(self.chars["LSGT"], ["\\", "|", "\\", "|"])
        self.assertEqual(xkb.MAC_KEYCODES["LSGT"], 10)
        self.assertEqual(xkb.MAC_KEYCODES["TLDE"], 50)

    def test_every_key_has_a_keycode(self):
        self.assertEqual(set(self.chars), set(xkb.MAC_KEYCODES))
        self.assertEqual(len(set(xkb.MAC_KEYCODES.values())), len(xkb.MAC_KEYCODES))

    def test_classification(self):
        self.assertEqual(xkb.key_type(self.chars["AC01"]), "FOUR_LEVEL_ALPHABETIC")
        self.assertEqual(xkb.key_type(self.chars["AB03"]), "FOUR_LEVEL_SEMIALPHABETIC")
        self.assertEqual(xkb.key_type(self.chars["AC04"]), "FOUR_LEVEL_ALPHABETIC")
        self.assertEqual(xkb.key_type(self.chars["AE01"]), "FOUR_LEVEL")

    def test_caps_layers(self):
        self.assertEqual(xkb.caps_layers(self.chars["AC01"]), ["A", "a", "Á", "á"])
        self.assertEqual(xkb.caps_layers(self.chars["AB03"]), ["C", "c", "©", "¢"])
        self.assertEqual(xkb.caps_layers(self.chars["AC11"]), ["'", '"', "´", "¨"])


class DeadKeyReplacementTest(unittest.TestCase):
    def test_table_has_17_entries(self):
        self.assertEqual(len(xkb.DEAD_KEY_REPLACEMENTS), 17)
        self.assertEqual(len(xkb.replacement_table()), 17)

    def test_no_dead_keysym_remains(self):
        syms = xkb.resolve()
        dead = {(k, i + 1) for k, levels in syms.items()
                for i, s in enumerate(levels) if xkb.is_dead(s)}
        self.assertEqual(dead, set(xkb.replacement_table()))
        for chars in xkb.layers().values():
            self.assertEqual(len(chars), 4)
            for ch in chars:
                self.assertEqual(len(ch), 1)

    def test_spot_checks(self):
        chars = xkb.layers()
        self.assertEqual(chars["AC11"][2], "\u00b4")  # ´
        self.assertEqual(chars["AB09"][3], "\u02c7")  # ˇ
        self.assertEqual(chars["AB05"][3], "\u0338")  # combining long solidus


if __name__ == "__main__":
    unittest.main()
