# installation Specification

## Purpose
Defines how users install and uninstall the keyboard layout from a clone of the repository, either for the current user or system-wide, without modifying their input source settings.

## Requirements

### Requirement: Per-user installation by default
Running `scripts/install.sh` without options SHALL install the layout bundle into `~/Library/Keyboard Layouts/` without requiring administrator privileges. It SHALL work regardless of the current working directory.

#### Scenario: Default install
- **WHEN** the user runs `./scripts/install.sh` from any directory
- **THEN** the bundle is copied to `~/Library/Keyboard Layouts/US AltGr Intl No Dead Keys.bundle` and no sudo prompt appears

#### Scenario: Reinstall replaces the previous copy
- **WHEN** the layout is already installed in the target location and the user runs the installer again
- **THEN** the previous bundle is fully replaced by the current one, with no leftover files

### Requirement: System-wide installation on request
Running `scripts/install.sh --system` SHALL install the bundle into `/Library/Keyboard Layouts/`, requesting administrator privileges only for that operation.

#### Scenario: System install
- **WHEN** the user runs `./scripts/install.sh --system`
- **THEN** the user is prompted for sudo and the bundle is copied to `/Library/Keyboard Layouts/US AltGr Intl No Dead Keys.bundle`

#### Scenario: Unknown option
- **WHEN** the user runs the installer with an unrecognized option
- **THEN** it prints usage, changes nothing and exits with a non-zero status

### Requirement: Installation guidance
After installing, the installer SHALL:
- refresh cached input source icons where possible;
- tell the user to log out and back in, then add "US AltGr Intl No Dead Keys" from System Settings > Keyboard > Input Sources.

It SHALL NOT enable, disable or reorder input sources itself. It SHALL NOT open System Settings either: the layout only becomes available after the next login, so the settings pane would be of no use at that point.

#### Scenario: Post-install message
- **WHEN** installation succeeds
- **THEN** the next steps are printed, no application is opened, and the list of enabled input sources is unchanged

### Requirement: Uninstallation detects the install location
Running `scripts/uninstall.sh` SHALL remove the bundle from `~/Library/Keyboard Layouts/` and from `/Library/Keyboard Layouts/`, whichever contain it. It SHALL request administrator privileges only when a system-wide copy exists.

#### Scenario: Per-user copy only
- **WHEN** the bundle exists only in `~/Library/Keyboard Layouts/`
- **THEN** it is removed without any sudo prompt

#### Scenario: System copy present
- **WHEN** the bundle exists in `/Library/Keyboard Layouts/`
- **THEN** the user is prompted for sudo and the system copy is removed

#### Scenario: Nothing installed
- **WHEN** neither location contains the bundle
- **THEN** the script reports that there is nothing to remove and exits successfully

### Requirement: Uninstallation guidance
After uninstalling, the uninstaller SHALL tell the user to remove the input source in System Settings > Keyboard > Input Sources if it is still listed, and to log out and back in to clear the system cache. It SHALL NOT modify input source settings itself.

#### Scenario: Post-uninstall message
- **WHEN** uninstallation completes
- **THEN** the remaining manual steps are printed

### Requirement: Supported platform
The scripts SHALL run only on macOS. Before installing, the installer SHALL warn when the macOS version is older than 26, because the layout is designed for macOS 26 and later and tested on macOS 27. End users SHALL need only the tools shipped with macOS.

#### Scenario: Not macOS
- **WHEN** a script is run on a non-macOS system
- **THEN** it exits with an error and changes nothing

#### Scenario: Older macOS
- **WHEN** the installer runs on macOS 15
- **THEN** it prints a warning that the version is not supported and still installs the layout

### Requirement: Scripts produce English output
All messages printed by the installation scripts SHALL be in English.

#### Scenario: Messages
- **WHEN** any installation script prints output
- **THEN** the text is in English
