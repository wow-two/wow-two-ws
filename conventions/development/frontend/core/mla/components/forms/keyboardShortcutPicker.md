# KeyboardShortcutPicker

*Last updated: 2026-09-10*

> Record a chord — the reader presses the combination and the control captures it as normalized keys.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must let a reader rebind a command in settings
- must accept the value is a key-name array — `['Meta', 'K']`, never a display string
- should reach for it over typing the chord; a typed shortcut is unverifiable

---

## Instead of

| Reach for | When |
|---|---|
| `KeyboardShortcut` | the chord is shown beside a command, not set |
| `Kbd` | one key is rendered inline in prose |
| [TextInput](textInput.md) | the value is a command name rather than a chord |

---

## Values

- must check reserved chords for supported platforms and allow canceling capture through the keyboard.
