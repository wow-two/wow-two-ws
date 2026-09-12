# PinInput

*Last updated: 2026-09-10*

> A short code, one character per box — paste-aware, and it fires once the last cell fills.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must collect a one-time code, a verification code, or a short PIN
- must act on `complete` rather than watching the value fill up

---

## Instead of

| Reach for | When |
|---|---|
| [PasswordInput](passwordInput.md) | the secret is long and the reader may want to reveal it |
| [MaskedInput](maskedInput.md) | the value carries literals and varies in length |
| [NumberInput](numberInput.md) | the digits are a quantity, not a code |

---

## Values

- should leave `type` at `numeric` so mobile opens the digit keypad
- should leave `size` at `md`; `lg` where the boxes must be thumb-sized
