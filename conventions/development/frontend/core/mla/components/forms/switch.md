# Switch

*Last updated: 2026-09-10*

> A setting flipped on — it takes effect where it stands, with no submit behind it.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must turn something on or off immediately — a preference, a feature, a notification
- must be reversible at no cost; a flip that needs confirming is not a switch
- should reach for [SwitchField](switchField.md) when the track needs a label

---

## Instead of

| Reach for | When |
|---|---|
| [Checkbox](checkbox.md) | the boolean is submitted with a form rather than applied at once |
| `ToggleButton` | the state is a toolbar mode shown as a pressed button |
| `ToggleButtonGroup` | the setting has three or more named states |

---

## Values

- should leave `size` at `md`; `lg` for a standalone row with a thumb target
