# PasswordInput

*Last updated: 2026-09-10*

> A masked secret with a reveal toggle — the only control that hides what it holds.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must collect a secret the reader types — a password, a token, an API key
- should pair it with [PasswordStrength](passwordStrength.md) on a create or reset flow

---

## Instead of

| Reach for | When |
|---|---|
| [TextInput](textInput.md) | the value is not secret and needs no masking |
| [PinInput](pinInput.md) | the secret is a short code entered one character per box |
| `Snippet` | the secret is shown to be copied, not typed |

---

## Values

- must set autocomplete for the actual flow, distinguishing sign-in from creating a new secret.
