# keyboard-layout Specification

## Purpose
Defines what the "US AltGr Intl No Dead Keys" macOS keyboard layout types for every key and modifier combination: Debian's `us(altgr-intl)` positions with a literal ASCII base layer and no dead keys at all.

## Requirements

### Requirement: Layout identity
The layout SHALL be named "US AltGr Intl No Dead Keys" in the input menu and in System Settings, SHALL be listed under English, and SHALL use the bundle identifier `com.ajmasia.keyboardlayout.us-altgr-intl-no-dead-keys`.

#### Scenario: Layout appears under English
- **WHEN** the user opens System Settings > Keyboard > Input Sources > "+" after installing and logging back in
- **THEN** "US AltGr Intl No Dead Keys" is listed under English

#### Scenario: Name shown in the input menu
- **WHEN** the layout is enabled and the user opens the input menu in the menu bar
- **THEN** the entry reads "US AltGr Intl No Dead Keys"

### Requirement: Key positions follow xkb us(altgr-intl)
For the Base, Shift, Option and Shift+Option layers, every key that `xkb us(altgr-intl)` defines SHALL produce the character xkb assigns to it at level 1, 2, 3 and 4 respectively. The Option key plays the role of AltGr. The only exceptions are the dead-key replacements and the ISO key defined in this spec.

#### Scenario: Direct Spanish characters
- **WHEN** the user types Option+a, Option+e, Option+i, Option+o, Option+u, Option+n, Option+y, Option+/ and Option+Shift+1
- **THEN** the output is `á`, `é`, `í`, `ó`, `ú`, `ñ`, `ü`, `¿` and `¡`

#### Scenario: Uppercase accented characters
- **WHEN** the user types Shift+Option+a, Shift+Option+e, Shift+Option+n
- **THEN** the output is `Á`, `É`, `Ñ`

#### Scenario: altgr-intl specific positions
- **WHEN** the user types Option+b, Option+f, Shift+Option+v, Shift+Option+m, Option+6 with Shift
- **THEN** the output is `·`, `f`, `™`, `±`, `¼`

### Requirement: Base and Shift layers are literal ASCII
With no modifier or only Shift, every printable key SHALL produce the same ASCII character as the US QWERTY layout. In particular, `'`, `"`, `` ` ``, `~` and `^` SHALL be emitted immediately as ASCII (U+0027, U+0022, U+0060, U+007E, U+005E).

#### Scenario: Quotes and tilde are literal
- **WHEN** the user types `'`, Shift+`'`, `` ` ``, Shift+`` ` `` followed by `a`
- **THEN** the output is `'"`` `~a` with no composition and no wait for a following key

#### Scenario: Circumflex is ASCII
- **WHEN** the user types Shift+6
- **THEN** the output is `^` (U+005E), not `ˆ` (U+02C6)

### Requirement: No dead keys
The layout SHALL NOT contain any dead-key state. Every keystroke, under any modifier combination including Caps Lock, SHALL either emit its output immediately or emit nothing. No keystroke SHALL change how the next keystroke is interpreted.

#### Scenario: Former dead key does not compose
- **WHEN** the user types Option+`'` followed by `e`
- **THEN** the output is `´e` (two characters), not `é`

#### Scenario: No dead key under Caps Lock
- **WHEN** Caps Lock is on and the user types `'` followed by `a`
- **THEN** the output is `'A`

### Requirement: Dead-key positions emit standalone diacritics
The 17 positions that are dead keys in `xkb us(altgr-intl)` SHALL emit the corresponding spacing diacritic. Where Unicode has no spacing form, they SHALL emit the combining mark:

| Key | Layer | xkb dead key | Output |
|---|---|---|---|
| `` ` `` | Option | dead_grave | `` ` `` U+0060 |
| `` ` `` | Shift+Option | dead_tilde | `~` U+007E |
| `'` | Option | dead_acute | `´` U+00B4 |
| `'` | Shift+Option | dead_diaeresis | `¨` U+00A8 |
| `2` | Shift+Option | dead_doubleacute | `˝` U+02DD |
| `3` | Shift+Option | dead_macron | `¯` U+00AF |
| `5` | Shift+Option | dead_cedilla | `¸` U+00B8 |
| `6` | Option | dead_circumflex | `ˆ` U+02C6 |
| `7` | Option | dead_horn | U+031B (combining horn) |
| `8` | Option | dead_ogonek | `˛` U+02DB |
| `9` | Shift+Option | dead_breve | `˘` U+02D8 |
| `0` | Shift+Option | dead_abovering | `˚` U+02DA |
| `-` | Shift+Option | dead_belowdot | U+0323 (combining dot below) |
| `.` | Option | dead_abovedot | `˙` U+02D9 |
| `.` | Shift+Option | dead_caron | `ˇ` U+02C7 |
| `/` | Shift+Option | dead_hook | U+0309 (combining hook above) |
| `b` | Shift+Option | dead_stroke | U+0338 (combining long solidus overlay) |

#### Scenario: Acute accent standalone
- **WHEN** the user types Option+`'`
- **THEN** `´` (U+00B4) is emitted immediately

#### Scenario: Caron standalone
- **WHEN** the user types Shift+Option+`.`
- **THEN** `ˇ` (U+02C7) is emitted immediately

### Requirement: ISO extra key
The key between left Shift and Z on ISO keyboards (macOS key code 10) SHALL produce `\` in the Base and Option layers and `|` in the Shift and Shift+Option layers, matching xkb `<LSGT>`. The layout SHALL work on ANSI and ISO keyboards alike.

#### Scenario: ISO key on an ISO keyboard
- **WHEN** a keyboard sends key code 10 with no modifier, then with Shift
- **THEN** the output is `\` then `|`

#### Scenario: ANSI keyboard unaffected
- **WHEN** the layout is used with an ANSI keyboard that has no key code 10
- **THEN** every other key behaves as specified

### Requirement: Caps Lock behaves as on Linux
Caps Lock SHALL invert case only for keys whose characters in the active layer form an uppercase/lowercase pair, following xkb's alphabetic key types. It SHALL NOT affect digits, punctuation or symbols. Shift SHALL cancel Caps Lock on those keys.

#### Scenario: Letters
- **WHEN** Caps Lock is on and the user types `a`, then Shift+`a`
- **THEN** the output is `A` then `a`

#### Scenario: Accented letters
- **WHEN** Caps Lock is on and the user types Option+`a`, then Option+`n`, then Shift+Option+`a`
- **THEN** the output is `Á`, `Ñ`, `á`

#### Scenario: Symbols unaffected
- **WHEN** Caps Lock is on and the user types `1`, `'`, Option+`c`
- **THEN** the output is `1`, `'`, `©`

### Requirement: Keyboard shortcuts match Apple's U.S. layout
Command- and Control-based shortcuts SHALL behave the same as with Apple's "U.S." layout. This includes combinations that add Shift and/or Option. Control+letter SHALL produce the standard ASCII control characters.

#### Scenario: Common shortcuts
- **WHEN** the user presses Command+C, Command+V, Command+Z, Command+/ and Command+Shift+Z in a text editor
- **THEN** they trigger Copy, Paste, Undo, Toggle Comment and Redo as with the U.S. layout

#### Scenario: Command+Option shortcut
- **WHEN** the user presses Command+Option+I in Safari with the developer menu enabled
- **THEN** the Web Inspector opens, as with the U.S. layout

#### Scenario: Control characters
- **WHEN** the user presses Control+C in Terminal while a process runs
- **THEN** the process receives an interrupt (ETX, U+0003)

### Requirement: Non-character keys behave as the U.S. layout
Return, Tab, Delete, Escape, arrows, function keys and keypad keys SHALL behave as in Apple's U.S. layout under all modifiers. Space SHALL produce U+0020 under every modifier combination handled by the layout, including Option, so that no non-breaking space is inserted by accident.

#### Scenario: Option+Space
- **WHEN** the user types Option+Space
- **THEN** a regular space (U+0020) is emitted
