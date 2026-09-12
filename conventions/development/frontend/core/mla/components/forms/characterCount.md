# CharacterCount

*Last updated: 2026-09-10*

> The live `current / max` readout under a capped text control — it owns no value and edits nothing.
> A [feedback](../../constructs/visual/feedback.md) component, not a control, though the SDK ships it in `forms/`.

## Reach for it when

- must show how much of a hard cap a text control has spent
- must pass `value` as the current length, never the string itself
- should sit in the field's helper row, beside the error, not inside the control

---

## Instead of

| Reach for | When |
|---|---|
| [PasswordStrength](passwordStrength.md) | the measure is strength rather than length |
| `MeterBar` | the ratio reads better than the two numbers |
| [FormHelperText](formHelperText.md) | the copy is a hint and no cap is enforced |
