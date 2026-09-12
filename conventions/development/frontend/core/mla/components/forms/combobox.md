# Combobox

*Last updated: 2026-09-10*

> Type to narrow, then pick one — the picker for an option set too large to enumerate.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must let the reader filter a long or remote list by typing
- must compose the parts — `ComboboxInput`, `ComboboxContent`, `ComboboxItem`
- should reach for it when each keystroke refetches the options

---

## Instead of

| Reach for | When |
|---|---|
| [Select](select.md) | the set is small, enumerable, and needs no typing |
| [MultiSelect](multiSelect.md) | the reader picks more than one value |
| [TagsInput](tagsInput.md) | the reader supplies values the list does not hold |
| [SearchInput](searchInput.md) | the typing searches the page rather than setting a value |
| `CommandPalette` | the entries run commands rather than set a value |

---

## Values

- should leave `fillInputOnSelect` on — the input then reads back the chosen option
- should leave `ComboboxContent` at `placement` `bottom` and `offset` `6`
