# Checkbox

*Last updated: 2026-09-10*

> One independent boolean the form submits — the default box for opt-ins, flags, and row selection.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- should use it for a submitted choice; row selection may take effect immediately
- must set `isIndeterminate` on a parent whose children are partly checked
- should reach for [CheckboxField](checkboxField.md) when the box needs a label

---

## Instead of

| Reach for | When |
|---|---|
| [Switch](switch.md) | the toggle applies at once and nothing is submitted |
| [CheckboxGroup](checkboxGroup.md) | several boxes share one value array under a legend |
| [Radio](radio.md) | exactly one of a set may be chosen |
| `ToggleButton` | the state is a toolbar mode, not a form value |

---

## Values

- should leave `size` at `md`, `variant` at `solid`, `tone` at `primary`
