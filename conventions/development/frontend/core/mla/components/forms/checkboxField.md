# CheckboxField

*Last updated: 2026-09-10*

> A checkbox and its label in one clickable `<label>` — the default for any labelled box.
> What a field is → [field](../../constructs/visual/field.md).

## Reach for it when

- must reach for it whenever a bare [Checkbox](checkbox.md) needs a visible label
- must not hand-roll the `<label>` around a checkbox — this one owns the association
- must give every item a `value` inside a [CheckboxGroup](checkboxGroup.md)
- must use the existing field context for help/error without adding a second label or state owner

---

## Instead of

| Reach for | When |
|---|---|
| [Checkbox](checkbox.md) | a surrounding [Field](field.md) supplies the label |
| [CheckboxGroup](checkboxGroup.md) | several boxes share one name and one selection |
| [SwitchField](switchField.md) | the toggle applies at once instead of on submit |
| [ChoiceCard](choiceCard.md) | the option reads as a card with a title and a description |
| [Field](field.md) | the control is anything but a checkbox |
