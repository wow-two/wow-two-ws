# PasswordStrength

*Last updated: 2026-09-10*

> The strength meter under a new-password box — it reads the value and sets nothing.
> A [feedback](../../constructs/visual/feedback.md) component, not a control, though the SDK ships it in `forms/`.

## Reach for it when

- must show how strong a secret is while it is being created or reset
- must sit under a [PasswordInput](passwordInput.md), never replace it

---

## Instead of

| Reach for | When |
|---|---|
| [CharacterCount](characterCount.md) | the constraint is a length cap rather than strength |
| `MeterBar` | the ratio is generic and carries no password rules |
| [FormErrorMessage](formErrorMessage.md) | the password failed a rule and must be rewritten |

---

## Values

- must show strength only where the user is choosing a secret, not on sign-in.

- should leave `isLabelHidden` off — the band name carries the meaning, not the colour
