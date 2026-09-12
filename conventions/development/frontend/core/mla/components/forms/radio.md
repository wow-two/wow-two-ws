# Radio

*Last updated: 2026-09-10*

> One dot of a mutually exclusive set — it means nothing outside the group that names it.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must offer one option of a set where exactly one may hold
- must sit inside a [RadioGroup](radioGroup.md) — the group owns `name` and the selection
- should reach for [RadioField](radioField.md) when the dot needs a label beside it

---

## Instead of

| Reach for | When |
|---|---|
| [Checkbox](checkbox.md) | each option is independent and several may hold |
| [ChoiceCard](choiceCard.md) | the option needs a description or an icon to be picked |
| `ToggleButtonGroup` | the options are short and belong in one strip |
| [Select](select.md) | the set is long enough that laying it out costs the screen |

---

## Values

- should leave `size` at `md`; `lg` for a standalone dot with a thumb target
