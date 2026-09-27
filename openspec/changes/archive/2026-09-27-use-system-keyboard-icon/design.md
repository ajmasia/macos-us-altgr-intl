# Design

## Context

Version 0.1.0 ships a template `.icns` "US" badge (design D7 of the archived change `add-us-altgr-intl-no-dead-keys-layout`). On macOS 27, the input source indicator next to the text cursor was tested with seven bundles:

| Variant | Icon | Indicator |
|---|---|---|
| 0.1.0, C1 | filled badge, template (C1 also with `TISIconLabels`) | empty |
| C2 | filled badge, not template | empty |
| D1 | "US" glyphs only, template | empty |
| D2 | outlined badge, template | empty |
| C3 | no `.icns` (only `TISIconLabels`) | generic keyboard icon |

The layout from philippwallrafen/macos-us-intl-no-dead-keys-iso ships an `.icns`, but macOS shows the generic keyboard icon for it: its red accent is absent from a menu screenshot. That is why its indicator is not empty either. According to the Ukelele users list, `TISIconLabels` is only honoured for Apple's built-in layouts.

## Goals / Non-Goals

**Goals:**
- A visible indicator next to the cursor when switching to the layout.
- Nothing in the bundle that silently degrades the indicator again.

**Non-Goals:**
- A "US" label in the indicator. No mechanism for third-party keyboard layouts is known; an input method would be required, which is out of scope.

## Decisions

### D1. Ship no icon
Delete the `.icns` and the `TISIconIsTemplate` key. macOS then uses its generic keyboard icon everywhere: menu bar, input menu and cursor indicator. The system adapts it to light and dark appearance.

Alternatives considered:
- Keep the badge and accept an empty indicator. Rejected by the user.
- Ship a keyboard-shaped `.icns`. Rejected: every custom icon tested left the indicator empty.

### D2. Validator rejects `.icns`
`check-layout.py` fails if `Contents/Resources` contains any `.icns`, and no longer expects one.

### D3. Remove the icon tooling
Delete `scripts/make-icon.swift`, the README section on regenerating the icon and the Swift badge. They would only document an approach that does not work. The history remains in git and in the archived change.

### D4. Version 0.2.0
The menu-bar icon change is visible to every user, so this is a minor release under the versioning spec. While the version is 0.x, visible changes go in minor releases.

## Risks / Trade-offs

- [The menu bar no longer says "US", and several third-party layouts may share the same keyboard icon] → The name is still shown in the input menu. Accepted by the user.
- [Cached icons keep showing the old badge after upgrading] → The installer touches the bundle and restarts TextInputMenuAgent. Users log out and back in, and restart if the indicator misbehaves, as observed during testing.
