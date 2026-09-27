# Design

## Context

- The repository only contains an OpenSpec skeleton and an `idea/` prototype, which stays out of version control. It is not a git repository yet. See proposal.md for why the prototype and existing ports cannot be reused.
- Findings from the exploration that shape the approach:
  - `idea/` resolves Caps+Shift and Caps+Option to its default (Control) map, so those combinations type nothing.
  - `carjorvaz/macos-us-altgr-intl` (GPL-3.0) has scrambled characters in its Caps+Option map.
  - `philippwallrafen/macos-us-intl-no-dead-keys-iso` (MIT) uses Windows US-Intl positions, emits U+02C6 on Shift+6, and keeps a dead `'` under Caps Lock.
  - Apple's own layouts ship no `.icns`: their badges are drawn by the system. Apple's input methods get system-drawn text badges via a `TISIconLabels` dictionary (`Primary`/`Secondary`) in their input mode entries. Examples: VietnameseIM, KoreanIM, JapaneseIM.
  - macOS registers a bundle's layout under an input source id derived from the bundle identifier and layout name (observed: `com.ajmasia.keyboardlayout.intl-altgr.keylayout.IntlAltGr`), not the literal `TISInputSourceID` value.
- The development machine runs macOS 27.0 and currently has two layouts in `~/Library/Keyboard Layouts/`: `Intl AltGr.bundle` (prototype) and `US Intl no dead keys ISO.bundle`.

## Goals / Non-Goals

**Goals:**
- A single hand-maintained `.keylayout` whose correctness is enforced by an offline validator.
- Provenance that is simple to explain: every character mapping derives from xkeyboard-config.
- A badge indistinguishable from native ones if macOS allows it, otherwise the agreed fallback (same height, template).
- Plain-bash install scripts with no dependencies beyond a stock macOS.

**Non-Goals:**
- A maintained layout generator. The bootstrap runs once; afterwards the `.keylayout` is the source.
- Supporting JIS-specific keys beyond inheriting the ANSI maps.
- Automated end-to-end keystroke tests. Real typing is verified manually against a checklist.

## Decisions

### D1. Bundle layout
```
US AltGr Intl No Dead Keys.bundle/Contents/
  Info.plist              CFBundleIdentifier, KLInfo_US AltGr Intl No Dead Keys {
                            TISInputSourceID, TISIntendedLanguage=en,
                            TISIconIsTemplate=true, TISIconLabels{Primary="US"} (if spike S1 succeeds) }
  version.plist
  Resources/US AltGr Intl No Dead Keys.keylayout
  Resources/US AltGr Intl No Dead Keys.icns
  Resources/en.lproj/InfoPlist.strings   localized display name
```
File names, the `name` attribute and the `KLInfo_` suffix must be identical, because macOS ties them together. The validator enforces this (layout-validation: bundle consistency). Alternative considered: a bare `.keylayout` + `.icns` in `Keyboard Layouts/`. Rejected because it has no stable identifier, no localization and no Info.plist keys for the icon.

### D2. Modifier maps cover every combination explicitly
The keylayout declares one `keyMapSelect` per meaningful combination, so that no real keystroke falls through to `defaultIndex`. That fall-through is the root cause of the `idea/` Caps bugs.

| Map | Modifiers | Content |
|---|---|---|
| 0 | none | xkb level 1 |
| 1 | anyShift | xkb level 2 |
| 2 | caps | level 1, or level 2 for alphabetic keys |
| 3 | anyShift caps | level 2, or level 1 for alphabetic keys |
| 4 | anyOption | xkb level 3 (with dead-key replacements) |
| 5 | anyShift anyOption | xkb level 4 (with dead-key replacements) |
| 6 | caps anyOption | level 3, or level 4 where levels 3/4 are a case pair |
| 7 | anyShift caps anyOption | level 4, or level 3 where levels 3/4 are a case pair |
| 8 | command (+ optional caps/option) | ASCII base characters for shortcut matching |
| 9 | control (+ any) | standard ASCII control characters |
| 10 | anyShift command (+ optional caps/option) | ASCII shift characters for shortcut matching |

Map 10 mirrors Apple's U.S. layout, where Command+Shift resolves to the shifted character (for example Command+? for Help). It is listed before map 9 in the `modifierMap`, so Control combinations still reach map 9.

`defaultIndex` points to map 0. Which keys count as "alphabetic" follows xkb's automatic key-type rules:
- `FOUR_LEVEL_ALPHABETIC` when both level pairs are case pairs;
- `FOUR_LEVEL_SEMIALPHABETIC` when only levels 1/2 are.

The command map deliberately emits plain ASCII, mirroring how Apple's U.S. layout resolves Command shortcuts, so that `Cmd+Opt+I` and similar shortcuts match by their base letter. Alternative: copy Apple's own modifier structure (as the Ukelele-derived ports do). Not possible without Apple's source, and it offers no benefit over explicit maps.

### D3. Key map sets
One `ANSI` keyMapSet contains all keys, including key code 10 (ISO extra key: `\ |` on all four character layers) and key code 50 (`` ` ~ ``). A `JIS` keyMapSet inherits from it via `baseMapSet`. ISO keyboards use the ANSI set. Because the Voyager and the K3 Pro are programmable, the ISO 10/50 swap question is left to the keyboard firmware rather than solved in the layout. Alternative: a separate ISO set with swapped codes (the philippwallrafen approach). Rejected because it bakes one vendor's firmware quirk into the layout.

### D4. Non-character keys
Return, Tab, Delete, Escape, Enter, arrows, Home/End/Page keys, forward delete, function keys and keypad keys use the conventional control outputs that every macOS keylayout uses (for example `U+000D` for Return, `U+001C`–`U+001F` for arrows, `U+0010` for function keys). Space emits U+0020 in every map, including Option, so no NBSP is typed by accident.

### D5. Bootstrap once from xkb, then maintain by hand
`scripts/bootstrap-from-xkb.py` works as follows:
1. Parse the pinned `vendor/xkeyboard-config/symbols/us`.
2. Resolve `altgr-intl`, including its `include "us(intl)"`.
3. Apply the dead-key replacement table from the keyboard-layout spec.
4. Map xkb key names to macOS key codes.
5. Write the initial `.keylayout` using the modifier maps from D2.

After the first commit, edits go to the `.keylayout` directly. `scripts/check-layout.py` reuses the same parsing module (`scripts/xkb.py`), so the bootstrap and the validator cannot disagree on how xkb is read. Only the Python 3 standard library is used. Alternative: a permanent generator (rejected during exploration as more code than the layout warrants), or hand-writing the XML from scratch (error-prone). Copying carjorvaz's or xv0x7c0's XML is ruled out for licensing reasons.

### D6. Validator scope
`check-layout.py` loads the `.keylayout` with the standard XML parser, after mapping XML-1.0-illegal control-character entities to placeholders. It resolves each key through the modifier-map selection the way macOS would, for every combination of {shift, caps, option}. It then checks the rules in the layout-validation spec. Its report is a list of `key / layer / expected / actual` lines, with exit status 1 on any finding. Command and Control maps are only checked for being ASCII and non-dead. Shortcut behaviour itself is covered by the manual checklist.

### D7. Icon: spike first, then fallback
The first implementation task is a spike on the development Mac. Each variant is installed, the user logs out and back in, and the badge is compared against "Spanish - ISO" in the menu bar and in the input menu:

| Variant | Info.plist | .icns |
|---|---|---|
| S1 | `TISIconLabels {Primary: "US"}` | none |
| S2 | `TISIconLabels` + `TISIconIsTemplate` | yes |
| S3 | neither | none |
| S4 | `TISIconIsTemplate` | square badge (current approach) |

- If S1 or S2 yields a native badge, ship S2: the labels key plus the template `.icns` as a safety net.
- Otherwise ship S4. The badge fills the square canvas vertically so its height matches native badges; this is fallback F1.

`scripts/make-icon.swift` renders the template iconset (black rounded rect, glyph knocked out, heavy compressed system font) and `iconutil` packs it. The resulting `.icns` is committed. The installer never generates it.

### D8. Install scripts
- `install.sh`:
  1. Resolve the repo root from the script's own path.
  2. Check `uname` = Darwin and warn if `sw_vers -productVersion` < 26.
  3. Copy the bundle to a temporary name in the target directory, then swap it into place. This way a failed copy never leaves a half-installed bundle.
  4. `touch` the bundle so the cached icon is dropped, then `killall TextInputMenuAgent` (ignoring errors).
  5. Print the next steps and `open "x-apple.systempreferences:com.apple.Keyboard-Settings.extension"`.
  
  `--system` targets `/Library/Keyboard Layouts` and prefixes the file operations with `sudo`.
- `uninstall.sh` checks both directories and removes whatever copies it finds. It uses sudo only for the `/Library` copy.
- Neither script touches `com.apple.HIToolbox` or calls TIS APIs, because a freshly copied layout is not visible to TIS until the next login.

### D9. Repository conventions
- `openspec/config.yaml` gains a `context` stating the project conventions: Conventional Commits, atomic commits, no AI attribution in commits or PRs, all project text in English.
- `.gitignore` excludes `idea/`, `.claude/` and `.DS_Store`.
- `vendor/xkeyboard-config/` holds `symbols/us`, xkeyboard-config's `COPYING`, and a `SOURCE` file with the upstream URL and commit hash.
- The README credits xkeyboard-config and lists the reference projects as prior art without deriving from them.

## Risks / Trade-offs

- [`TISIconLabels` may be ignored for keylayout bundles] → The spike runs first. Fallback F1 is already agreed and specified.
- [Command map choice could break a shortcut in some app] → Manual checklist covering Cmd, Cmd+Shift and Cmd+Opt shortcuts in Safari, Terminal and an editor. Adjust map 8 if needed.
- [Icon and layout caches make results look stale] → The installer touches the bundle and restarts TextInputMenuAgent. The docs say to log out and back in. Use a fresh keylayout `id` if macOS keeps a stale registration.
- [Keyboard-layout id collision with other installed layouts] → Pick a random negative `id` in the Unicode group (126) and check it against the installed layouts during bootstrap.
- [Combining marks (horn, dot below, hook, stroke) attach to the previous character] → Accepted in the spec and documented in the README.
- [Hand edits drift from xkb] → The validator is the gate. Run it before every commit that touches the `.keylayout`.

## Migration Plan

1. On the development Mac, remove the prototype with `idea/uninstall.sh`. Remove `US Intl no dead keys ISO.bundle` from `~/Library/Keyboard Layouts/` and disable both in Input Sources, so their badges and caches do not mix with the new layout during testing.
2. Install the new bundle with `scripts/install.sh`, log out and back in, and enable it.
3. Rollback: `scripts/uninstall.sh`, log out and back in, and optionally reinstall the prototype from `idea/`.

## Open Questions

- Exact wording and screenshot for the README menu-bar image. This can be decided after the spike without affecting specs or tasks.
