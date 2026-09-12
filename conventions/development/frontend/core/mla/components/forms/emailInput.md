# EmailInput

*Last updated: 2026-09-10*

> One email address — `type="email"`, the `@` keyboard on mobile, autofill wired, spellcheck off.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must collect exactly one address — sign-in, sign-up, invite, contact
- should reach for it over [TextInput](textInput.md) purely for the mobile keyboard

---

## Instead of

| Reach for | When |
|---|---|
| [TextInput](textInput.md) | the value is free text with no address semantics |
| [TagsInput](tagsInput.md) | several addresses go into one field |
| [UrlInput](urlInput.md) | the identifier is a link |
| [TelInput](telInput.md) | the identifier is a phone number |

---

## Values

- should leave `size` at `md`, `border` at `sm`, `ring` at `md` — the input house set
