# US AltGr Intl No Dead Keys

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

### Differences from other layouts

- **Debian `altgr-intl`:** the same characters in the same positions, but none of the 17 dead keys (marked †). Where Debian waits for the next key, this layout types the accent immediately.
- **Apple's "U.S. International - PC":** there, `'`, `"`, `` ` ``, `~` and `^` are dead keys on the base layer; here they type immediately. That layout mirrors Windows US-International, and xkb notes that `altgr-intl` diverges from the Microsoft layout on the `1`, `6`, `7`, `8`, `R`, `F`, `X`, `V` and `B` keys.

## Development

None of this is needed to install or use the layout.

The development tools need Python 3, which comes with the Xcode Command Line Tools (`xcode-select --install`). They use only the Python standard library and do not access the network.

### Validating the layout

The `.keylayout` is edited by hand. Run the validator before every commit that touches it:

```sh
python3 scripts/check-layout.py
```

It compares the layout with the pinned xkeyboard-config reference in `vendor/xkeyboard-config/` and checks the project rules:

- no dead keys under any modifier;
- ASCII-only Base and Shift layers;
- Caps Lock behaviour;
- ASCII-only Command and Control maps;
- consistent bundle naming;
- a valid, consistent Semantic Versioning version in `Info.plist` and `version.plist`.

It prints one line per finding (`key / layer / expected / actual`) and exits with status 1 if there are any.

Run the unit tests with:

```sh
python3 -m unittest discover -s scripts/tests
```

### Regenerating the menu-bar icon

The `.icns` in the bundle is committed, so installing never needs build tools. To regenerate it, for example after changing `scripts/make-icon.swift`, run:

```sh
swift scripts/make-icon.swift US "$TMPDIR/us.iconset"
iconutil -c icns "$TMPDIR/us.iconset" \
  -o "US AltGr Intl No Dead Keys.bundle/Contents/Resources/US AltGr Intl No Dead Keys.icns"
```

The badge is a template image: a rounded rectangle with "US" knocked out. macOS cannot draw its own text badge for third-party layouts. This badge copies the shape and letter height of the native badges instead (44:32, measured on macOS 27). Because icon canvases are square, it spans the canvas width and is slightly smaller than the native badges.

### Provenance of the `.keylayout`

`scripts/bootstrap-from-xkb.py` generated the initial `.keylayout` from `vendor/xkeyboard-config/symbols/us`. It is kept only as a record and is not part of the normal workflow.

## Provenance and prior art

Every character mapping comes from [xkeyboard-config](https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config)'s `symbols/us` (MIT/X11-style licenses). A pinned copy is in `vendor/xkeyboard-config/`, together with its license and the upstream commit it was taken from. `scripts/bootstrap-from-xkb.py` generated the initial `.keylayout` from that copy. No code or layout data from other projects is used.

These projects port `altgr-intl` or US-International to macOS. They were consulted as references only:

- [carjorvaz/macos-us-altgr-intl](https://github.com/carjorvaz/macos-us-altgr-intl)
- [philippwallrafen/macos-us-intl-no-dead-keys-iso](https://github.com/philippwallrafen/macos-us-intl-no-dead-keys-iso)
- [xv0x7c0/osx-us-altgr-intl](https://github.com/xv0x7c0/osx-us-altgr-intl)

## License

[MIT](LICENSE).
