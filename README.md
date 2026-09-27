# US AltGr Intl No Dead Keys

[![Version](https://img.shields.io/github/v/tag/ajmasia/macos-us-altgr-intl?label=version&sort=semver)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Platform: macOS 26+](https://img.shields.io/badge/macOS-26%2B-black?logo=apple)](#requirements)
[![Based on xkeyboard-config](https://img.shields.io/badge/based%20on-xkeyboard--config-orange)](https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config)
[![Planned with OpenSpec](https://img.shields.io/badge/planned%20with-OpenSpec-6f42c1)](#planning-with-openspec)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-FE5196?logo=conventionalcommits&logoColor=white)](https://www.conventionalcommits.org)

A macOS keyboard layout that behaves like Debian's "English (intl., with AltGr dead keys)" (`xkb us(altgr-intl)`), but with no dead keys at all. The base and Shift layers are plain US ASCII, so `'`, `"`, `` ` ``, `~` and `^` are typed immediately, which suits programming. Accented letters and symbols sit on Option (acting as AltGr), and each of them is typed with a single keystroke.

## Requirements

macOS 26 Tahoe or later. Tested on macOS 27. Installing needs only the tools that ship with macOS.

## Installation

Clone the repository and run the installer:

```sh
git clone https://github.com/ajmasia/macos-us-altgr-intl.git
cd macos-us-altgr-intl
./scripts/install.sh
```

This installs the layout for your user in `~/Library/Keyboard Layouts/`. To install it for all users in `/Library/Keyboard Layouts/` instead, run `./scripts/install.sh --system`. You will be asked for your password.

Then:

1. Log out and log back in. macOS only registers new keyboard layouts at login.
2. Open System Settings > Keyboard > Input Sources > Edit, click "+", choose English and add **US AltGr Intl No Dead Keys**.

The installer does not open System Settings or change your input sources; it only copies the layout.

## Uninstallation

```sh
./scripts/uninstall.sh
```

The script removes the layout from `~/Library/Keyboard Layouts/` and `/Library/Keyboard Layouts/`, whichever contain it. It asks for your password only when a system-wide copy exists. Afterwards, remove the input source in System Settings > Keyboard > Input Sources if it is still listed, then log out and log back in.

## Layout

Without modifiers and with Shift, every key types the same ASCII character as the standard US layout. Option plays the role of AltGr:

| Key | Option | Shift+Option |
|---|---|---|
| `` ` `` `~` | `` ` `` † | `~` † |
| `1` `!` | `¹` | `¡` |
| `2` `@` | `²` | `˝` † |
| `3` `#` | `³` | `¯` † |
| `4` `$` | `¤` | `£` |
| `5` `%` | `€` | `¸` † |
| `6` `^` | `ˆ` † | `¼` |
| `7` `&` | U+031B † | `½` |
| `8` `*` | `˛` † | `¾` |
| `9` `(` | `‘` | `˘` † |
| `0` `)` | `’` | `˚` † |
| `-` `_` | `¥` | U+0323 † |
| `=` `+` | `×` | `÷` |
| `Q` | `ä` | `Ä` |
| `W` | `å` | `Å` |
| `E` | `é` | `É` |
| `R` | `ë` | `Ë` |
| `T` | `þ` | `Þ` |
| `Y` | `ü` | `Ü` |
| `U` | `ú` | `Ú` |
| `I` | `í` | `Í` |
| `O` | `ó` | `Ó` |
| `P` | `ö` | `Ö` |
| `[` `{` | `«` | `“` |
| `]` `}` | `»` | `”` |
| `A` | `á` | `Á` |
| `S` | `ß` | `§` |
| `D` | `ð` | `Ð` |
| `F` | `f` | `F` |
| `G` | `g` | `G` |
| `H` | `h` | `H` |
| `J` | `ï` | `Ï` |
| `K` | `œ` | `Œ` |
| `L` | `ø` | `Ø` |
| `;` `:` | `¶` | `°` |
| `'` `"` | `´` † | `¨` † |
| `\` `\|` | `¬` | `¦` |
| `Z` | `æ` | `Æ` |
| `X` | `œ` | `Œ` |
| `C` | `©` | `¢` |
| `V` | `®` | `™` |
| `B` | `·` | U+0338 † |
| `N` | `ñ` | `Ñ` |
| `M` | `µ` | `±` |
| `,` `<` | `ç` | `Ç` |
| `.` `>` | `˙` † | `ˇ` † |
| `/` `?` | `¿` | U+0309 † |
| ISO key (`\` `\|`) | `\` | `\|` |

† A dead key in `xkb us(altgr-intl)`. Here it types the diacritic on its own, straight away, and does not change the next key.

Four of those positions have no standalone (spacing) form in Unicode, so they type a combining mark that attaches to the character **before** it:

- U+031B combining horn (Option+7);
- U+0323 combining dot below (Shift+Option+-);
- U+0309 combining hook above (Shift+Option+/);
- U+0338 combining long solidus overlay (Shift+Option+B).

For example, typing `o` and then Option+7 gives `ơ`.

Option+Space types a regular space, never a non-breaking space.

### Caps Lock

Caps Lock works as on Linux: it changes the case of letters only, and Shift reverses it. For example, Caps Lock with `a`, Option+`a` and Shift+Option+`a` gives `A`, `Á` and `á`. Digits, punctuation and symbols such as `1`, `'` and Option+`c` (`©`) are not affected.

### Shortcuts

Command and Control shortcuts behave as with Apple's "U.S." layout. Command+Option shortcuts such as Command+Option+I match their base letter.

### Menu bar icon

The layout uses macOS's generic keyboard icon, in the menu bar, in the input menu and in the indicator that appears next to the text cursor when you switch input sources. It has no "US" badge of its own. On macOS 27, that indicator stays empty for every custom icon of a third-party keyboard layout, and macOS offers no way for such layouts to show a text label like the built-in ones ("A", "US"). The generic icon is the only one that appears everywhere.

### Differences from other layouts

- **Debian `altgr-intl`:** the same characters in the same positions, but none of the 17 dead keys (marked †). Where Debian waits for the next key, this layout types the accent immediately.
- **Apple's "U.S. International - PC":** there, `'`, `"`, `` ` ``, `~` and `^` are dead keys on the base layer; here they type immediately. That layout mirrors Windows US-International, and xkb notes that `altgr-intl` diverges from the Microsoft layout on the `1`, `6`, `7`, `8`, `R`, `F`, `X`, `V` and `B` keys.

## Development

None of this is needed to install or use the layout.

The development tools need Python 3, which comes with the Xcode Command Line Tools (`xcode-select --install`). They use only the Python standard library and do not access the network.

### Scripts

| Script | Purpose |
|---|---|
| `scripts/check-layout.py` | Validates the layout bundle. Run it before every commit that touches the bundle. |
| `scripts/xkb.py` | Module used by the other two scripts: reads `vendor/xkeyboard-config/symbols/us`, resolves `us(altgr-intl)`, maps xkb keys to macOS key codes and holds the table of the 17 dead-key replacements. Not run directly. |
| `scripts/bootstrap-from-xkb.py` | Generated the initial `.keylayout` from xkb. Kept as a record; not part of the normal workflow. |
| `scripts/tests/` | Unit tests for `xkb.py` and `check-layout.py`. |

### Validating the layout

```sh
python3 scripts/check-layout.py [BUNDLE]
```

`BUNDLE` defaults to `US AltGr Intl No Dead Keys.bundle` in the repository root. The script compares the layout with the pinned xkeyboard-config reference and checks the project rules:

- the Base, Shift, Option and Shift+Option layers, and their Caps Lock variants, match xkb `us(altgr-intl)` plus the documented dead-key replacements;
- no dead keys under any modifier;
- ASCII-only Base and Shift layers, and ASCII-only Command and Control maps;
- no empty `keyMap` (macOS silently rejects the whole layout if one is empty);
- consistent bundle naming, and no custom `.icns` icon;
- a valid, consistent Semantic Versioning version in `Info.plist` and `version.plist`.

It prints one line per finding (`key / layer / expected / actual`) and exits with status 1 if there are any, or prints `OK` and exits with status 0.

Run the unit tests with:

```sh
python3 -m unittest discover -s scripts/tests
```

### Changing a key

1. Edit `US AltGr Intl No Dead Keys.bundle/Contents/Resources/US AltGr Intl No Dead Keys.keylayout`. Each `<keyMap index="N">` is one modifier combination (see the `<modifierMap>` at the top of the file), and each `<key code="…" output="…"/>` is one key, identified by its macOS key code.
2. The validator expects exactly xkb `us(altgr-intl)`. The only exceptions it allows are the 17 dead-key replacements in `DEAD_KEY_REPLACEMENTS` (`scripts/xkb.py`). A change to one of those characters goes in that table. Any other deliberate departure from xkb needs a new exception in `scripts/xkb.py`, with a test.
3. Run `python3 scripts/check-layout.py` and the unit tests.
4. Run `./scripts/install.sh`, then log out and back in to try it. macOS only reloads layouts at login.

### Regenerating from xkb

`scripts/bootstrap-from-xkb.py` rebuilds the `.keylayout` from `vendor/xkeyboard-config/symbols/us`:

```sh
python3 scripts/bootstrap-from-xkb.py --id -24458 --output "$TMPDIR/new.keylayout"
diff "US AltGr Intl No Dead Keys.bundle/Contents/Resources/US AltGr Intl No Dead Keys.keylayout" "$TMPDIR/new.keylayout"
```

- `--id` sets the keyboard layout id. Keep `-24458`, the id of the shipped layout; without it the script picks a random unused id.
- `--output` sets where to write. Without it, the script **overwrites** the shipped `.keylayout`, discarding any hand edits, so write elsewhere and compare first.

This is only useful after updating the vendored xkeyboard-config: replace `vendor/xkeyboard-config/symbols/us` and `COPYING` with the files from a newer upstream commit, update `vendor/xkeyboard-config/SOURCE`, and run the validator to see what changed.

## Planning with OpenSpec

Changes to this project are planned with [OpenSpec](https://github.com/Fission-AI/OpenSpec) before they are implemented. A plan is a set of Markdown files:

- `openspec/specs/<capability>/spec.md`: how the project currently behaves, as requirements with scenarios. There is one capability per area (`keyboard-layout`, `menu-bar-icon`, `installation`, `layout-validation`, `versioning`).
- `openspec/changes/<change>/`: a proposed change, made of:
  - `proposal.md`: why and what;
  - `design.md`: how, and the decisions taken;
  - `specs/`: the requirements it adds, modifies or removes;
  - `tasks.md`: the implementation checklist.
- `openspec/changes/archive/`: completed changes. Archiving a change merges its spec changes into `openspec/specs/`.

Install the CLI with `npm install -g @fission-ai/openspec`. The commands you will use most:

```sh
openspec list                       # active changes
openspec list --specs               # capabilities
openspec show <change-or-spec>      # read a change or a spec
openspec new change <name>          # start a change (kebab-case, e.g. fix-caps-option-comma)
openspec status --change <name>     # which planning files are done
openspec validate <name> --strict   # check a change before implementing and before archiving
openspec archive <name>             # merge the change into openspec/specs and archive it
```

### How to proceed

**New feature or behaviour change** (a new key, a different character, a new installer option):

1. Run `openspec new change add-<something>` and write `proposal.md`, the spec changes under `specs/`, `design.md` if there are decisions to record, and `tasks.md`.
2. Run `openspec validate add-<something> --strict`.
3. Implement the tasks in order and tick each one off in `tasks.md` as it is done. Use one Conventional Commit per logical step.
4. Run `python3 scripts/check-layout.py` and the unit tests, and add an entry under `Unreleased` in `CHANGELOG.md`.
5. Once it is merged, run `openspec archive add-<something>`.

**Bug fix:**

- If the layout or scripts do not do what a spec says, the spec is right and the code is wrong. Fix the code with a `fix:` commit, add a check or test that would have caught it, and add a `Fixed` entry to `CHANGELOG.md`. No OpenSpec change is needed.
- If the spec itself is wrong or incomplete, open a change (for example `fix-<something>`) that modifies the requirement, then implement it as for a new feature.

**Maintenance with no change in behaviour** (typos, refactors, updating the README): commit directly with the matching Conventional Commit type (`docs:`, `refactor:`, `chore:`). No OpenSpec change is needed.

### Releasing

1. Choose the next version:
   - **patch** for fixes;
   - **minor** for new behaviour;
   - **major** for changes that break existing typing habits (while the version is `0.x`, use minor).
2. Set `CFBundleShortVersionString` and `CFBundleVersion` in `Info.plist` and `version.plist`. `check-layout.py` fails if the four values differ.
3. Move the `Unreleased` entries in `CHANGELOG.md` to a new dated section, and update the comparison links at the bottom.
4. Commit, create a signed tag and push both:
   ```sh
   git tag -s vX.Y.Z -m "vX.Y.Z"
   git push --follow-tags
   ```
5. Publish a GitHub release for the tag, using that version's `CHANGELOG.md` section as the notes:
   ```sh
   gh release create vX.Y.Z --verify-tag --title "vX.Y.Z" --notes-file notes.md
   ```

## Provenance and prior art

Every character mapping comes from [xkeyboard-config](https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config)'s `symbols/us` (MIT/X11-style licenses). A pinned copy is in `vendor/xkeyboard-config/`, together with its license and the upstream commit it was taken from. `scripts/bootstrap-from-xkb.py` generated the initial `.keylayout` from that copy. No code or layout data from other projects is used.

These projects port `altgr-intl` or US-International to macOS. They were consulted as references only:

- [carjorvaz/macos-us-altgr-intl](https://github.com/carjorvaz/macos-us-altgr-intl)
- [philippwallrafen/macos-us-intl-no-dead-keys-iso](https://github.com/philippwallrafen/macos-us-intl-no-dead-keys-iso)
- [xv0x7c0/osx-us-altgr-intl](https://github.com/xv0x7c0/osx-us-altgr-intl)

## Versioning

Releases follow [Semantic Versioning](https://semver.org/). Each one is tagged `vMAJOR.MINOR.PATCH`, and the same version is recorded in the bundle's `Info.plist`. See [CHANGELOG.md](CHANGELOG.md) for what changed in each release.

## License

[MIT](LICENSE).
