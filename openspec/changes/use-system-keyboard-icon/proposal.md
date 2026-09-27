# Proposal

## Why

In macOS 27, the input source indicator that appears next to the text cursor after switching layouts is empty for this layout: a blue bubble with nothing in it. Tests with seven icon variants showed the following:
- The indicator never draws a custom `.icns` from a third-party keyboard layout: filled, outline, glyph-only, template and non-template icons all left the bubble empty.
- `TISIconLabels` is ignored for keyboard layout bundles.
- Only a layout without an icon of its own gets something in the bubble: macOS then uses its generic keyboard icon, in the menu bar and in the bubble alike.

Other third-party layouts, for example philippwallrafen/macos-us-intl-no-dead-keys-iso, show the same generic icon, and it is visible in the bubble. A recognizable indicator in the bubble matters more than the "US" badge in the menu bar.

## What Changes

- **BREAKING (visual):** the bundle no longer ships an icon. macOS shows its generic keyboard icon in the menu bar, the input menu and the text-cursor indicator, instead of the "US" badge.
- Remove `TISIconIsTemplate` from `Info.plist`; without an icon it has no effect.
- The validator requires that the bundle ships no `.icns`, so the empty-indicator problem cannot come back unnoticed.
- Remove `scripts/make-icon.swift`, its README section and the Swift badge.
- Document in the README why the layout uses the generic icon.
- Release as 0.2.0.

## Capabilities

### New Capabilities
<!-- None. -->

### Modified Capabilities
- `menu-bar-icon`: the "US" badge requirements are replaced by the generic system keyboard icon, which must be visible in the menu bar, the input menu and the text-cursor indicator.
- `layout-validation`: bundle consistency no longer expects an `.icns` file and fails if one is present.

## Impact

- Bundle: delete `Resources/US AltGr Intl No Dead Keys.icns` and the `TISIconIsTemplate` key.
- `scripts/check-layout.py` and its tests; delete `scripts/make-icon.swift`.
- README and CHANGELOG. Bundle version 0.2.0 and tag `v0.2.0`.
- Users who upgrade see the menu-bar icon change from "US" to a keyboard after logging back in.
