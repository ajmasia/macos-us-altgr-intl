## ADDED Requirements

### Requirement: System keyboard icon
The layout SHALL NOT ship an icon of its own. macOS SHALL represent it with its generic keyboard icon in the menu bar and the input menu, and that icon SHALL adapt to light and dark appearance the way system icons do.

#### Scenario: Menu bar and input menu
- **WHEN** the layout is installed and enabled, and the user opens the input menu
- **THEN** the menu bar and the input menu show the generic macOS keyboard icon next to "US AltGr Intl No Dead Keys"

#### Scenario: Dark menu bar
- **WHEN** the menu bar is dark
- **THEN** the keyboard icon is legible, like other system icons

### Requirement: Visible in the input source indicator
When the user switches to the layout while a text cursor is active, the input source indicator next to the cursor SHALL show an icon rather than an empty bubble.

#### Scenario: Switching layouts in a text field
- **WHEN** the text cursor is in Notes and the user switches from "Spanish - ISO" to "US AltGr Intl No Dead Keys"
- **THEN** the indicator next to the cursor shows the generic keyboard icon

## REMOVED Requirements

### Requirement: Badge text
**Reason**: The text-cursor input indicator in macOS 27 draws nothing for any custom icon of a third-party keyboard layout, so a "US" badge left the indicator empty.
**Migration**: None needed. After upgrading and logging back in, the layout is shown with the generic keyboard icon.

### Requirement: Badge matches native badges
**Reason**: There is no custom badge any more. The system keyboard icon is used instead.
**Migration**: None needed.

### Requirement: Adapts to light and dark appearance
**Reason**: Replaced by "System keyboard icon". The system icon adapts to the appearance by itself.
**Migration**: None needed.

### Requirement: Icon available without build tools
**Reason**: The bundle no longer contains an icon, so there is nothing to generate or ship.
**Migration**: None needed.
