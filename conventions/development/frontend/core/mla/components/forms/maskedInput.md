# MaskedInput

*Last updated: 2026-09-10*

> A fixed shape typed into — the mask inserts the literals and rejects the wrong character class.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must collect a value whose punctuation is part of its shape — a card, an SSN, a code
- must accept the value stays a string, mask literals included
- should reach for it when the format is rigid; a flexible one frustrates typing

---

## Instead of

| Reach for | When |
|---|---|
| [PhoneInput](phoneInput.md) | the value is a phone number and needs a country dial code |
| [PinInput](pinInput.md) | the value is a short code in one box per character |
| [NumberInput](numberInput.md) | the value is a number and the separators are cosmetic |
| [TextInput](textInput.md) | the shape varies and a mask would block valid entries |

---

## Values

- should keep masks short — `###-###-####`, `##/##/####`, `AAA-####`
