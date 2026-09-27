## MODIFIED Requirements

### Requirement: Verifies bundle consistency
The validation SHALL check that the following are consistent: the bundle directory name, the `.keylayout` file name, the `name` attribute of the `.keylayout`, the `KLInfo_<name>` key in `Info.plist`, and the bundle identifier. It SHALL also fail if the bundle contains an `.icns` file, because a custom icon leaves the text-cursor input indicator empty.

#### Scenario: Mismatched KLInfo key
- **WHEN** `Info.plist` contains `KLInfo_Intl AltGr` but the `.keylayout` is named "US AltGr Intl No Dead Keys"
- **THEN** the validation reports the mismatch and fails

#### Scenario: Custom icon present
- **WHEN** the bundle's `Resources` directory contains an `.icns` file
- **THEN** the validation reports it and fails
