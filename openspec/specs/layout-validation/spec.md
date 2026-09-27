# layout-validation Specification

## Purpose
Provides an automated development check that the shipped keyboard layout keeps matching the xkb `us(altgr-intl)` reference and the project's no-dead-keys, ASCII and Caps Lock rules, so hand edits cannot silently break it.

## Requirements

### Requirement: Pinned xkb reference
The repository SHALL contain a pinned copy of xkeyboard-config `symbols/us`. Alongside it, the repository SHALL record the upstream commit it was taken from and xkeyboard-config's license. The validation SHALL use only this copy and SHALL NOT access the network.

#### Scenario: Offline validation
- **WHEN** the validation runs without network access
- **THEN** it completes using the pinned reference

### Requirement: Mapping matches the reference
The validation SHALL compare every key defined by `us(altgr-intl)`, including the keys it inherits from `us(intl)`, across the Base, Shift, Option and Shift+Option layers against the shipped `.keylayout`. It SHALL allow only the documented dead-key replacements and the ISO key mapping. Each mismatch SHALL be reported with the key, the layer, the expected character and the actual character.

#### Scenario: Correct layout
- **WHEN** the shipped `.keylayout` matches the reference and the documented exceptions
- **THEN** the validation reports success and exits with status 0

#### Scenario: Wrong character
- **WHEN** Shift+Option+v produces `®` instead of `™`
- **THEN** the validation reports key `v`, layer Shift+Option, expected `™`, actual `®`, and exits with a non-zero status

### Requirement: Detects dead keys
The validation SHALL fail if the `.keylayout` defines any dead-key state reachable from any modifier combination, including Caps Lock combinations.

#### Scenario: Dead key under Caps Lock
- **WHEN** the `'` key starts a dead-key state while Caps Lock is on
- **THEN** the validation reports it and fails

### Requirement: Detects non-ASCII in Base and Shift layers
The validation SHALL fail if any printable key in the Base or Shift layer produces a character outside ASCII.

#### Scenario: Modifier letter circumflex
- **WHEN** Shift+6 produces `ˆ` (U+02C6)
- **THEN** the validation reports it and fails

### Requirement: Verifies Caps Lock behaviour
The validation SHALL verify the Caps Lock requirement of the `keyboard-layout` capability for the Base, Shift, Option and Shift+Option layers, using xkb's alphabetic key semantics to decide which keys change case.

#### Scenario: Caps Lock with Option
- **WHEN** Caps Lock+Option+`a` produces nothing or a character other than `Á`
- **THEN** the validation reports it and fails

### Requirement: Verifies bundle consistency
The validation SHALL check that the following are consistent: the bundle directory name, the `.keylayout` file name, the `name` attribute of the `.keylayout`, the `KLInfo_<name>` key in `Info.plist`, and the bundle identifier. It SHALL also fail if the bundle contains an `.icns` file, because a custom icon leaves the text-cursor input indicator empty.

#### Scenario: Mismatched KLInfo key
- **WHEN** `Info.plist` contains `KLInfo_Intl AltGr` but the `.keylayout` is named "US AltGr Intl No Dead Keys"
- **THEN** the validation reports the mismatch and fails

#### Scenario: Custom icon present
- **WHEN** the bundle's `Resources` directory contains an `.icns` file
- **THEN** the validation reports it and fails

### Requirement: Verifies the bundle version
The validation SHALL check that `CFBundleShortVersionString` and `CFBundleVersion` in `Info.plist` and `version.plist` are all equal and are a valid Semantic Versioning `MAJOR.MINOR.PATCH` version.

#### Scenario: Mismatched versions
- **WHEN** `Info.plist` says `0.1.0` but `version.plist` says `1.0`
- **THEN** the validation reports the mismatch and fails
