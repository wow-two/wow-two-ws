# DataTable

*Last updated: 2026-09-10*

> The column-driven table — hand it rows and a `columns` descriptor, it sorts on the client.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must render a list of records the reader reads, scans and sorts
- must reach for it before [Table](table.md) whenever a descriptor can express the columns
- should sort on the client only while the whole set is already loaded

---

## Instead of

| Reach for | When |
|---|---|
| [Table](table.md) | the cells are too irregular for a column descriptor |
| [DataGrid](dataGrid.md) | the reader edits cells rather than reading them |
| `Pagination` | the set is paged — the table sorts, it does not page |
| [Sortable](sortable.md) | rows are dragged into a new order rather than sorted by a column |

---

## Values

- should leave the [Table](table.md) dials unset — each defers to the root's own default
- should leave `emptyContent` at `No results.`, or raise an [EmptyState](emptyState.md)
