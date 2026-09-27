# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.2] - 2026-09-27

### Changed

- README: table of contents, upgrading instructions, troubleshooting (layout not listed, stale icons, Option in Terminal and iTerm2, Caps Lock switching input sources), ANSI/ISO/JIS compatibility, a repository map, and full documentation of the development scripts, how to change a key, how to regenerate from xkb and how to publish a release.

## [0.2.1] - 2026-09-27

### Changed

- README: removed the Python and Bash badges, which do not concern users of the layout.
- The menu-bar-icon spec's purpose now describes the generic keyboard icon and the text-cursor indicator.

## [0.2.0] - 2026-09-27

### Changed

- **Breaking (visual):** the layout uses macOS's generic keyboard icon instead of the "US" badge. On macOS 27, the input source indicator next to the text cursor stays empty for any custom icon of a third-party layout; with the generic icon it shows the keyboard.
- The installer no longer opens System Settings: a new layout only appears there after logging back in.
- `scripts/check-layout.py` now fails if the bundle ships an `.icns` file.

### Removed

- The "US" badge icon and `scripts/make-icon.swift`.

## [0.1.0] - 2026-09-27

### Added

- "US AltGr Intl No Dead Keys" keyboard layout for macOS 26 and later:
  - Debian `xkb us(altgr-intl)` positions, with Option as AltGr;
  - literal ASCII Base and Shift layers;
  - no dead keys: the 17 former dead-key positions type standalone diacritics or combining marks;
  - Linux-style Caps Lock;
  - ISO extra key typing `\` and `|`;
  - Command and Control shortcuts as in Apple's "U.S." layout.
- Template menu-bar badge "US" with the shape of the native badges.
- `scripts/install.sh` (per user, or system-wide with `--system`) and `scripts/uninstall.sh`.
- `scripts/check-layout.py`: offline validator against a pinned copy of xkeyboard-config `symbols/us`, with unit tests.
- `scripts/make-icon.swift` to regenerate the badge, and `scripts/bootstrap-from-xkb.py` as a record of how the layout was generated.

[Unreleased]: https://github.com/ajmasia/macos-us-altgr-intl/compare/v0.2.2...HEAD
[0.2.2]: https://github.com/ajmasia/macos-us-altgr-intl/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/ajmasia/macos-us-altgr-intl/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/ajmasia/macos-us-altgr-intl/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/ajmasia/macos-us-altgr-intl/releases/tag/v0.1.0
