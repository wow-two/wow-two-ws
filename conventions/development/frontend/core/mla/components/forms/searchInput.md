# SearchInput

*Last updated: 2026-09-10*

> A query box — `type="search"`, a leading magnifier, and a clear action.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must filter or query something the reader is already looking at
- must accept the value is the query, never a selected record
- should handle `clear` — the button emits it and clears nothing beyond the box

---

## Instead of

| Reach for | When |
|---|---|
| [Combobox](combobox.md) | the typing narrows options and one of them becomes the value |
| `CommandPalette` | the query runs commands rather than filters content |
| [TextInput](textInput.md) | the value is stored rather than searched with |

---

## Values

- should leave `isClearable` on — a query the reader cannot clear is a dead end
- should leave `size` at `md`, `border` at `sm`, `ring` at `md` — the input house set
