# RadioField

*Last updated: 2026-09-10*

> A radio and its label in one clickable `<label>` — one option of a mutex set.
> What a field is → [field](../../constructs/visual/field.md).

## Reach for it when

- must reach for it whenever a bare [Radio](radio.md) needs a visible label
- must mount it inside a [RadioGroup](radioGroup.md) for a mutex set — the group supplies `name`
- must give every item a `value` inside a group; the group tracks selection by it
- must keep each option in its named mutually exclusive group

---

## Instead of

| Reach for | When |
|---|---|
| [Radio](radio.md) | a surrounding [Field](field.md) supplies the label |
| [RadioGroup](radioGroup.md) | the group itself should own the selected value |
| [ChoiceCard](choiceCard.md) | the option reads as a card with a title and a description |
| [CheckboxField](checkboxField.md) | the options are not mutually exclusive |
| `ToggleButtonGroup` | the choice switches a mode instead of posting a value |
