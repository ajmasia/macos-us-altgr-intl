# Proposal

## Why

On Linux/Debian, "English (intl., with AltGr dead keys)" (`xkb us(altgr-intl)`) gives a literal ASCII base layer for programming and direct accented letters on AltGr. macOS has no equivalent: native layouts either make `'` `"` `` ` `` `~` `^` dead keys or need two keystrokes for accents. The existing third-party ports are each broken in some way: the Windows-style layout has non-ASCII `ˆ` on Shift+6 and a dead `'` under Caps Lock, the faithful xkb port keeps 17 dead keys and ships no bundle or icon, and the local prototype mishandles Caps Lock combinations. The prototype and its upstream also have no license, so none of them can be used as a base. The goal is a macOS layout that behaves like Debian `altgr-intl` with no dead keys at all, installs cleanly, and shows a menu-bar badge that matches the native ones.

## What Changes

- New keyboard layout bundle **US AltGr Intl No Dead Keys** (`com.ajmasia.keyboardlayout.us-altgr-intl-no-dead-keys`) containing:
  - a `.keylayout` whose key positions follow `xkb us(altgr-intl)` exactly;
  - every one of the 17 xkb dead keys replaced by its standalone spacing diacritic (or combining mark where Unicode has no spacing form), so every keystroke emits a character immediately;
  - a literal ASCII base/Shift layer;
  - the ISO extra key producing `\ |`;
  - Linux-style Caps Lock behaviour;
  - Command/Control shortcuts identical to Apple's "U.S." layout.
- Menu-bar badge **"US"**:
  - Preferred: rendered by the system through `TISIconLabels`, to match native badges such as Español.
  - Fallback: a pre-generated template `.icns` badge with the same shape (aspect ratio) as native badges.
- `scripts/install.sh` (per-user by default, `--system` for `/Library` via sudo) and `scripts/uninstall.sh` (detects where the bundle is installed and only uses sudo when needed). Neither script modifies the enabled input sources; both print next steps.
- Development tooling, none of it needed by end users:
  - `scripts/check-layout.py` validates the `.keylayout` against a pinned copy of xkeyboard-config `symbols/us`;
  - `scripts/bootstrap-from-xkb.py` is a one-off script that produces the initial `.keylayout` with clean provenance;
  - `scripts/make-icon.swift` regenerates the fallback icon.
- Semantic versioning starting at 0.1.0: version in the bundle, signed `vX.Y.Z` tags and a `CHANGELOG.md`.
- Repository scaffolding:
  - MIT `LICENSE`;
  - English `README.md` with a text layout table;
  - `.gitignore` excluding `idea/`, `.claude/` and `.DS_Store`;
  - project conventions in `openspec/config.yaml`: Conventional Commits, atomic commits, no AI attribution, all text in English.

## Capabilities

### New Capabilities
- `keyboard-layout`: character output of every key and modifier combination (base, Shift, Option, Shift+Option, Caps Lock, Command, Control), the no-dead-keys guarantee, ISO key and ANSI/ISO compatibility, and layout identity (name, input source id, language).
- `menu-bar-icon`: how the input source is represented in the menu bar and input menu (badge text, native-matching size, light/dark adaptation).
- `installation`: installing and uninstalling the bundle per-user or system-wide, user guidance, and supported macOS versions.
- `layout-validation`: automated verification that the shipped `.keylayout` matches the xkb reference and the no-dead-keys, ASCII and Caps Lock rules.
- `versioning`: Semantic Versioning for releases, the version recorded in the bundle, signed release tags and a changelog. The first release is 0.1.0.

### Modified Capabilities
<!-- None: the project has no existing specs. -->

## Impact

- Greenfield repository: the directory is not yet a git repo, and nothing under `idea/` is reused or committed. `idea/` is derived from `xv0x7c0/osx-us-altgr-intl`, which has no license.
- New third-party material: a pinned copy of xkeyboard-config `symbols/us` (MIT/X11) under `vendor/`, with its license and source commit.
- Tooling dependencies are for development only: Python 3 for validation/bootstrap, and Swift plus `iconutil` for the icon. They come with the Xcode Command Line Tools. End users only need `bash`.
- Target platform: macOS 26 Tahoe and later, tested on macOS 27.
- Out of scope:
  - GitHub releases, `curl` installer and Homebrew;
  - automatic enabling/disabling of the input source;
  - automatic layout switching per physical keyboard;
  - a rendered layout image;
  - macOS versions before 26.
