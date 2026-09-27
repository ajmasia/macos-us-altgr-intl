# versioning Specification

## Purpose
Defines how releases of the keyboard layout are numbered and recorded, so users and macOS can tell which version is installed and what changed between versions.

## Requirements

### Requirement: Semantic version
The project SHALL be versioned with Semantic Versioning 2.0.0 (`MAJOR.MINOR.PATCH`). The first release SHALL be 0.1.0.

#### Scenario: First release
- **WHEN** the first release is published
- **THEN** its version is 0.1.0

### Requirement: Version recorded in the bundle
The bundle SHALL carry the release version in `CFBundleShortVersionString` and `CFBundleVersion` of both `Info.plist` and `version.plist`, so the installed copy identifies its release.

#### Scenario: Installed bundle version
- **WHEN** the user inspects the installed bundle's `Info.plist`
- **THEN** `CFBundleShortVersionString` and `CFBundleVersion` both equal the release version, for example `0.1.0`

### Requirement: Release tags
Each release SHALL be marked by a signed git tag named `v` followed by the version (for example `v0.1.0`), pointing to a commit whose bundle carries that version.

#### Scenario: Tag matches bundle
- **WHEN** the tag `v0.1.0` is checked out
- **THEN** the bundle version is `0.1.0`

### Requirement: Changelog
The repository SHALL contain a `CHANGELOG.md` in the Keep a Changelog format, with one section per released version and an `Unreleased` section for pending changes.

#### Scenario: Release entry
- **WHEN** version 0.1.0 is released
- **THEN** `CHANGELOG.md` has a `0.1.0` section with its date and a summary of what the release contains
