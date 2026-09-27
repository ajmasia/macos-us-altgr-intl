# menu-bar-icon Specification

## Purpose
Defines how the layout is represented in the macOS menu bar and input menu, so that it is recognizable and visually consistent with the system's native input source badges.

## Requirements

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
