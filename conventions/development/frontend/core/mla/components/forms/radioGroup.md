# RadioGroup

*Last updated: 2026-09-10*

> Exactly one from a short fixed set, every option visible at once under one legend.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must pick one value from a set short enough to show whole
- must own the items' `name` and selection — the children read it by injection
- must give the selection group an accessible name

---

## Instead of

| Reach for | When |
|---|---|
| [CheckboxGroup](checkboxGroup.md) | more than one option may hold at a time |
| [SelectPicker](selectPicker.md) | the set is long enough that showing it whole costs the screen |
| `ToggleGroup` | the choices are short and read better as one strip |
| [ListboxPicker](listboxPicker.md) | the options scroll in place with arrow-key movement |

---

## Values

- should leave `orientation` at `vertical` — the readable default for labels
- should hold [ChoiceCard](choiceCard.md) items when each option needs explaining
