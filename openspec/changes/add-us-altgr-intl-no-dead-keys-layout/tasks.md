# Tasks

## 1. Repository setup

- [x] 1.1 Run `git init`. Add `.gitignore` excluding `idea/`, `.claude/` and `.DS_Store`. Verify: `git status` shows neither `idea/` nor `.claude/`.
- [x] 1.2 Add `context` to `openspec/config.yaml` with the project conventions: Conventional Commits, atomic commits, no AI attribution, all text in English. Verify: `openspec context --json` succeeds and `openspec instructions proposal --change add-us-altgr-intl-no-dead-keys-layout --json` shows the context.
- [x] 1.3 Add an MIT `LICENSE` and a skeleton English `README.md` (title, one-paragraph description, placeholder sections). Verify: both files exist and the README renders.
- [x] 1.4 Vendor xkeyboard-config into `vendor/xkeyboard-config/`: `symbols/us` from a specific upstream commit, `COPYING`, and a `SOURCE` file with the URL and commit hash. Verify: the `altgr-intl` and `intl` blocks exist in the vendored file and `SOURCE` names the commit.
- [x] 1.5 Make the first commits (one per task above, Conventional Commits, no AI attribution). Verify: `git log` shows atomic `chore:`/`docs:` commits.

## 2. Icon spike (menu-bar-icon)

- [x] 2.1 Build throwaway bundles for variants S1–S4 from design D7 outside the repo (`$TMPDIR`), each with a distinct bundle id and name. Verify: four bundles exist with the intended Info.plist keys (`plutil -p`).
- [x] 2.2 With the user: remove the prototype and other test layouts (design, Migration Plan step 1), install the variants, log out and back in, enable them, and compare against "Spanish - ISO" in the menu bar and input menu, in light and dark mode. Verify: screenshots and a written verdict on whether `TISIconLabels` produces a native badge.
- [x] 2.3 Record the outcome (S2 or S4) in design.md D7 and remove the spike bundles from `~/Library/Keyboard Layouts/`. Verify: design.md states the chosen variant and no spike bundle remains installed.

## 3. xkb parsing and layout bootstrap (keyboard-layout)

- [x] 3.1 Implement `scripts/xkb.py`:
  - parse the vendored `symbols/us` and resolve `altgr-intl` with its `include "us(intl)"`;
  - map xkb key names to macOS key codes, including `LSGT`→10 and `TLDE`→50;
  - classify keys as alphabetic or semi-alphabetic following the xkb type rules.

  Verify: `python3 -m unittest scripts/tests/test_xkb.py` passes, covering AC11, AE06, AB05, LSGT and the classification of `a`, `c` and `f`.
- [x] 3.2 Add the dead-key replacement table (the 17 entries from the keyboard-layout spec) to `scripts/xkb.py` as data. Verify: a unit test asserts that no dead keysym remains in the four resolved layers and spot-checks `´`, `ˇ` and U+0338.
- [x] 3.3 Implement `scripts/bootstrap-from-xkb.py` to write the `.keylayout`:
  - modifier maps as in design D2, with `defaultIndex` pointing to map 0;
  - ANSI and JIS key map sets as in D3;
  - non-character keys as in D4, with Space = U+0020 in every map;
  - a random negative id in group 126 that does not collide with the installed layouts.

  Verify: the output is well-formed XML (`plutil -lint` is not applicable; use `python3 -c "import xml.dom.minidom"` after entity mapping) and contains no `<terminators>` and no `next=` attribute.
- [x] 3.4 Generate `US AltGr Intl No Dead Keys.bundle/Contents/Resources/US AltGr Intl No Dead Keys.keylayout` and commit it together with the bootstrap script. Verify: the file exists and its `name` attribute is "US AltGr Intl No Dead Keys".

## 4. Layout validator (layout-validation)

- [x] 4.1 Implement `scripts/check-layout.py`:
  - load the `.keylayout`, including XML-illegal control entities;
  - resolve each key through the modifier-map selection for every {shift, caps, option} combination;
  - compare the result with `scripts/xkb.py` plus the documented exceptions, reporting `key / layer / expected / actual` and exiting 1 on any finding.

  Verify: running it on the generated layout exits 0.
- [x] 4.2 Add checks for dead-key states in any map (Caps included), non-ASCII characters in the Base/Shift layers, Caps Lock behaviour, ASCII-only Command/Control maps, and bundle naming consistency (design D1). Verify: `python3 -m unittest scripts/tests/test_check_layout.py` passes using mutated fixture copies (™→®, dead `'` under Caps, Shift+6=U+02C6, `KLInfo_` mismatch), and each mutation is reported with the expected message.
- [x] 4.3 Document validation in the README "Development" section: how to run the checks and the unit tests, and that Python 3 comes with the Xcode CLT. Verify: the documented commands run as written.

## 5. Bundle metadata and icon (keyboard-layout, menu-bar-icon)

- [x] 5.1 Write `Info.plist`:
  - `CFBundleIdentifier` `com.ajmasia.keyboardlayout.us-altgr-intl-no-dead-keys`;
  - `KLInfo_US AltGr Intl No Dead Keys` containing `TISInputSourceID`, `TISIntendedLanguage=en`, `TISIconIsTemplate=true`, plus `TISIconLabels {Primary: "US"}` if the spike chose S2.

  Also write `version.plist` and `en.lproj/InfoPlist.strings`. Verify: `plutil -lint` passes on all three and `check-layout.py` bundle-consistency passes.
- [x] 5.2 Implement `scripts/make-icon.swift`: a template badge with "US" knocked out of a black rounded rect with the native 44:32 aspect ratio spanning the canvas width (F2 geometry, design D7), bold system font with capitals at 17/32 of the badge height as on native badges. Verify: `swift scripts/make-icon.swift US "$TMPDIR/us.iconset"` writes all 10 iconset PNGs.
- [x] 5.3 Generate and commit `US AltGr Intl No Dead Keys.icns` with `iconutil`. Verify: `iconutil -c iconset` round-trips it, and the 32 px image shows a full-width badge with the native aspect ratio and transparent "US".
- [x] 5.4 Document icon regeneration in the README "Development" section. Verify: the documented commands reproduce a byte-identical or visually identical `.icns`.

## 6. Install and uninstall scripts (installation)

- [x] 6.1 Implement `scripts/install.sh` following design D8:
  - Darwin check and macOS < 26 warning;
  - repo root resolved from the script path;
  - `--system` option, usage and non-zero exit on unknown options;
  - copy to a temporary name and swap into place;
  - cache refresh and English next-steps message (no settings pane is opened; see design D8).

  Verify: run from another directory, the bundle lands in `~/Library/Keyboard Layouts/`; a second run leaves exactly one bundle; `--bogus` exits non-zero without changes; `shellcheck scripts/install.sh` is clean.
- [x] 6.2 Verify `scripts/install.sh --system` with the user: the sudo prompt appears and the bundle lands in `/Library/Keyboard Layouts/`.
- [x] 6.3 Implement `scripts/uninstall.sh`: remove the copies found in `~/Library` and `/Library` (sudo only for `/Library`), report "nothing to remove" when neither exists, and print English next steps. Verify: the per-user, system and nothing-installed cases behave as in the installation spec, and `shellcheck scripts/uninstall.sh` is clean.
- [x] 6.4 Document installation and uninstallation in the README (including `--system`, logging out and back in, adding the input source, and supported macOS 26+ / tested on 27). Verify: following the README steps on the development Mac installs and removes the layout.

## 7. README layout reference (keyboard-layout)

- [x] 7.1 Add the layout table to the README: Option and Shift+Option per key, with the 17 former dead-key positions marked, the combining-mark caveat, the Caps Lock behaviour, and the differences from Debian `altgr-intl` and from Apple's "U.S. International - PC". Verify: every entry matches `check-layout.py`'s resolved output (spot-check 10 keys).
- [x] 7.2 Add provenance and prior art to the README: derived from xkeyboard-config (MIT/X11), with carjorvaz, philippwallrafen and xv0x7c0 listed as references only. Verify: the section exists and the links resolve.

## 8. End-to-end verification on the development Mac

- [x] 8.1 Install the layout, log out and back in, and enable it. Walk through the keyboard-layout spec scenarios manually in TextEdit and Terminal: direct accents, literal quotes, no composition after Option+`'`, Caps Lock cases, ISO key via a programmable keyboard, Option+Space. Verify: every scenario produces the specified output; any failure is fixed in the `.keylayout` and `check-layout.py` still passes.
- [x] 8.2 Check shortcuts in Safari, Terminal and an editor: Cmd+C/V/Z, Cmd+Shift+Z, Cmd+/, Cmd+Opt+I, Ctrl+C. Verify: they behave as with Apple's "U.S." layout.
- [x] 8.3 Check the badge next to "Spanish - ISO" in the menu bar and input menu, in light and dark mode. Verify: the menu-bar-icon spec scenarios hold for the chosen variant.
- [x] 8.4 Run `openspec validate add-us-altgr-intl-no-dead-keys-layout --strict` and confirm that `git log` is atomic, uses Conventional Commits, and has no AI attribution. Verify: validation passes and the log meets the conventions.
