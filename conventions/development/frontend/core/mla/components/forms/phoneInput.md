# PhoneInput

*Last updated: 2026-09-10*

> A phone number with its country — a dial-code select beside the national number, emitting E.164.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must collect a number that will be dialled or texted, not merely stored
- must accept the value is E.164-shaped — `+<country><number>`, one string

---

## Instead of

| Reach for | When |
|---|---|
| [TelInput](telInput.md) | the number is local and no country code is needed |
| [MaskedInput](maskedInput.md) | the format is fixed to one country and never varies |
| [TextInput](textInput.md) | the field is an extension or a short internal code |

---

## Values

- must validate phone numbers using the applicable numbering rules; formatting is not validation.
- must choose country and placeholder from an explicit user choice or product locale policy.
