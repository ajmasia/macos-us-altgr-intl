# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/ajmasia/macos-us-altgr-intl/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ajmasia/macos-us-altgr-intl/releases/tag/v0.1.0
