# TelInput

*Last updated: 2026-09-10*

> A phone number as plain text — `type="tel"`, the dial keypad on mobile, autofill wired.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must collect a number whose country is already known or irrelevant
- should reach for it over [TextInput](textInput.md) purely for the mobile keypad

---

## Instead of

| Reach for | When |
|---|---|
| [PhoneInput](phoneInput.md) | the reader must choose a country and the value is E.164 |
| [MaskedInput](maskedInput.md) | the number must be typed into a fixed national shape |
| [TextInput](textInput.md) | the field is an extension or an internal code |

---

## Values

- should leave `size` at `md`, `border` at `sm`, `ring` at `md` — the input house set
