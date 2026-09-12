# DataGrid

*Last updated: 2026-09-10*

> The editable grid — cell-by-cell keyboard navigation and in-place edit.
> Kind → [control](../../constructs/visual/control.md).

## Reach for it when

- must let the reader change cell values without leaving the table
- should keep the row array on the caller; the grid reports an edit, it never mutates

---

## Instead of

| Reach for | When |
|---|---|
| [DataTable](dataTable.md) | the rows are read and sorted, never edited |
| [Table](table.md) | the cells are irregular and nothing is edited |
| `Form` | the record is edited as fields rather than as a grid |
