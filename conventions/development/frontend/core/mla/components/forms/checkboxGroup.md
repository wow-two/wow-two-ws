# CheckboxGroup

*Last updated: 2026-09-10*

> Zero-to-many from a short fixed set, every option visible at once under one legend.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must collect several values from a set short enough to show whole
- must give every item a `value` — the group keys selection by it
- must give the selection group an accessible name

---

## Instead of

| Reach for | When |
|---|---|
| [MultiSelect](multiSelect.md) | the set is long enough to need a dropdown |
| [Listbox](listbox.md) | the options scroll in place with arrow-key movement |
| [Checkbox](checkbox.md) | the box is one independent boolean |
| `ToggleButtonGroup` | the choices set a mode rather than a submitted value |

---

## Values

- should leave `orientation` at `vertical` — the readable default for labels
