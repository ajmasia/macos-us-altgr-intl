# Tasks

## 1. Bundle and validator

- [x] 1.1 Update `scripts/check-layout.py`: no longer require an `.icns`, and report any `.icns` in `Contents/Resources`. Update the tests: the fixture ships no `.icns`, and a new test adds one and expects the finding. Verify: `python3 -m unittest discover -s scripts/tests` passes.
- [x] 1.2 Delete `Resources/US AltGr Intl No Dead Keys.icns` and the `TISIconIsTemplate` key from `Info.plist`. Verify: `plutil -lint` passes and `python3 scripts/check-layout.py` exits 0.

## 2. Tooling and docs

- [x] 2.1 Delete `scripts/make-icon.swift`, the README section "Regenerating the menu-bar icon" and the Swift badge. Verify: `git grep -n make-icon` only matches the archive and the CHANGELOG.
- [x] 2.2 Explain in the README that the layout uses the generic macOS keyboard icon, and why (the cursor indicator is empty for custom icons). Verify: the section exists.

## 3. Release 0.2.0

- [x] 3.1 Set the bundle version to 0.2.0 in `Info.plist` and `version.plist`, and add a dated `0.2.0` section to `CHANGELOG.md`. Verify: `check-layout.py` exits 0 and the CHANGELOG links compare `v0.1.0...v0.2.0`.
- [x] 3.2 With the user: install, log out and back in (restart if the indicator does not appear), and switch to the layout in Notes. Verify: the generic keyboard icon appears in the menu bar, the input menu and the cursor indicator, in light and dark mode.
- [x] 3.3 Create the signed tag `v0.2.0`. Verify: `git tag -v v0.2.0` reports a good signature.
