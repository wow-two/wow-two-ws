# Field

*Last updated: 2026-09-10*

> The generic wrapper — a label, a helper and an error around any one control, and the id that ties them together.
> What a field is → [field](../../constructs/visual/field.md).

## Reach for it when

- must wrap any control that needs a visible label, a hint, or an error
- must reuse the form adapter's context when present and support standalone field chrome without a form engine
- must not hand-wire `for`, `aria-describedby` or `aria-invalid` — the wrapper mints the id
- should leave `error` unset under the forms engine — every client and server message renders itself
- should pass `label`, `helper` and `error` as props; the same-named slots are for rich copy only

---

## Instead of

| Reach for | When |
|---|---|
| [CheckboxField](checkboxField.md) | the control is a checkbox and the label sits beside the box |
| [RadioField](radioField.md) | the control is a radio inside a [RadioGroup](radioGroup.md) |
| [SwitchField](switchField.md) | the toggle applies at once instead of on submit |
| [Fieldset](fieldset.md) + [Legend](legend.md) | several fields answer to one name |
| [Label](label.md) alone | a compact row wants the name and no helper or error slot |
