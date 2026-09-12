# ToggleButton

*Last updated: 2026-09-10*

> A button that stays pressed — a mode, not a one-shot command.
> Kind → [control](../../constructs/visual/control.md).

## Reach for it when

- must reach for it when the pressed state persists and is read back — bold, pin
- must reach for it inside a [ToggleButtonGroup](toggleButtonGroup.md) when toggles share one selection
- should reach for it standalone only when nothing coordinates it

---

## Instead of

| Reach for | When |
|---|---|
| [Button](button.md) | the click runs once and leaves no state |
| [DisclosureButton](disclosureButton.md) | the state is an expanded region, not a mode |
| `Switch` | the on/off state is the widget's value → [control](../../constructs/visual/control.md) |
| [OptionTile](optionTile.md) | the option is an icon-only preset in a grid |

---

## Values

- should keep the `ghost` / `primary` defaults; `solid` fills on press
