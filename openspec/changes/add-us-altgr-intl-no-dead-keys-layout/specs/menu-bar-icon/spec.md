# Spec Delta

## Purpose

Defines how the layout is represented in the macOS menu bar and input menu, so that it is recognizable and visually consistent with the system's native input source badges.

## ADDED Requirements

### Requirement: Badge text
The layout's icon SHALL be a badge showing the text "US".

#### Scenario: Badge in the menu bar
- **WHEN** the layout is the active input source
- **THEN** the menu bar shows a badge reading "US"

### Requirement: Badge matches native badges
The badge SHALL be rendered with the same size, shape and typography as the system-generated badges of built-in layouts such as "Spanish - ISO", both in the menu bar and in the input menu. If macOS provides no mechanism for a third-party keyboard layout to obtain a system-rendered badge, the badge SHALL instead be a template image with the same width-to-height ratio as the native badges, spanning the full width of the square icon canvas. Because macOS scales icon canvases to the height of native badges, the fallback badge will then be slightly smaller than the native badges, with the same shape.

#### Scenario: Side by side in the input menu
- **WHEN** the user opens the input menu with both "Spanish - ISO" and "US AltGr Intl No Dead Keys" enabled
- **THEN** both badges have the same shape, and the same size if the system-rendered badge is available

#### Scenario: Fallback badge proportions
- **WHEN** the system-rendered badge is not available and the fallback badge is shown next to a native badge in the menu bar
- **THEN** both badges have the same width-to-height ratio, and the fallback badge is as wide as its icon canvas

### Requirement: Adapts to light and dark appearance
The badge SHALL adapt to the menu bar and menu appearance like native badges. It SHALL remain legible on light and dark menu bars and in the highlighted state of the input menu.

#### Scenario: Dark menu bar
- **WHEN** the menu bar is dark
- **THEN** the badge is drawn light with the text knocked out, like native badges

#### Scenario: Light menu bar
- **WHEN** the menu bar is light
- **THEN** the badge is drawn dark with the text knocked out, like native badges

### Requirement: Icon available without build tools
The icon SHALL ship inside the bundle. Installing the layout SHALL NOT require generating the icon or having developer tools on the target Mac.

#### Scenario: Install on a clean Mac
- **WHEN** the layout is installed on a Mac without Xcode Command Line Tools
- **THEN** the badge is displayed correctly after logging back in
