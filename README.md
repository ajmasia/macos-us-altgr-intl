# US AltGr Intl No Dead Keys

A macOS keyboard layout that behaves like Debian's "English (intl., with AltGr dead keys)" (`xkb us(altgr-intl)`), but with no dead keys at all. The base and Shift layers are plain US ASCII, so `'`, `"`, `` ` ``, `~` and `^` are typed immediately, which suits programming. Accented letters and symbols sit on Option (acting as AltGr), and each of them is typed with a single keystroke.

## Requirements

macOS 26 Tahoe or later. Tested on macOS 27. Installing needs only the tools that ship with macOS.

## Installation

From a clone of this repository, run:

```sh
./scripts/install.sh
```

This installs the layout for your user in `~/Library/Keyboard Layouts/`. To install it for all users in `/Library/Keyboard Layouts/` instead, run `./scripts/install.sh --system`. You will be asked for your password.

Then:

1. Log out and log back in. macOS only registers new keyboard layouts at login.
2. Open System Settings > Keyboard > Input Sources > Edit, click "+", choose English and add **US AltGr Intl No Dead Keys**.

The installer opens the Keyboard settings pane for you. It never enables, disables or reorders input sources itself.

## Uninstallation

```sh
./scripts/uninstall.sh
```

The script removes the layout from `~/Library/Keyboard Layouts/` and `/Library/Keyboard Layouts/`, whichever contain it. It asks for your password only when a system-wide copy exists. Afterwards, remove the input source in System Settings > Keyboard > Input Sources if it is still listed, then log out and log back in.

## Layout

_To be written._

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
- consistent bundle naming.

It prints one line per finding (`key / layer / expected / actual`) and exits with status 1 if there are any.

Run the unit tests with:

```sh
python3 -m unittest discover -s scripts/tests
```

### Provenance of the `.keylayout`

`scripts/bootstrap-from-xkb.py` generated the initial `.keylayout` from `vendor/xkeyboard-config/symbols/us`. It is kept only as a record and is not part of the normal workflow.

## Provenance and prior art

_To be written._

## License

[MIT](LICENSE).
