# UrlInput

*Last updated: 2026-09-10*

> A link typed in — `type="url"`, the URL keyboard on mobile, autofill wired, spellcheck off.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must collect one address the app will link to or fetch
- should reach for it over [TextInput](textInput.md) purely for the mobile keyboard

---

## Instead of

| Reach for | When |
|---|---|
| [TextInput](textInput.md) | the value is a slug, a handle, or a path fragment |
| [EmailInput](emailInput.md) | the identifier is an address |
| [TagsInput](tagsInput.md) | several links go into one field |
| `Link` | the URL is rendered as a destination rather than collected |

---

## Values

- should leave `size` at `md`, `border` at `sm`, `ring` at `md` — the input house set
