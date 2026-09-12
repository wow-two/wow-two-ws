# TextInput

*Last updated: 2026-09-10*

> The default single-line box — every string value no typed sibling in this folder claims.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must collect one line of free text — a name, a title, a reference
- must reach for it whenever no typed sibling matches; specificity, not habit, picks the others
- should let it read `id`, disabled, required, read-only and invalid off the field context

---

## Instead of

| Reach for | When |
|---|---|
| [EmailInput](emailInput.md) | the value is an address and autofill should recognise it |
| [SearchInput](searchInput.md) | the value is a query the reader clears rather than saves |
| [UrlInput](urlInput.md) | the value is a link |
| [TelInput](telInput.md) | the value is a phone number |
| [TextAreaInput](textAreaInput.md) | the value runs past one line |
| [MaskedInput](maskedInput.md) | the value has a rigid shape worth enforcing while typing |

---

## Values

- should leave `size` at `md`, `border` at `sm`, `ring` at `md` — the input house set
