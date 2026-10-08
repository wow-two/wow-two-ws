# Table

*Last updated: 2026-09-10*

> The table primitives — the caller writes the rows and cells by hand.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must lay out a table whose cells no column descriptor can express
- must own the markup — the parts ship as siblings, `TableHead` through `TableCaption`
- should let the root carry density and striping; the sections read them by injection

---

## Instead of

| Reach for | When |
|---|---|
| [DataTable](dataTable.md) | the rows come from data and a `columns` descriptor covers them |
| [DataGridEditor](dataGridEditor.md) | the reader edits cells in place |
| [DescriptionGroup](descriptionGroup.md) | the table is one record's properties, not many records |
| [ListGroup](listGroup.md) | each row has a single field |

---

## Values

- should leave `density` at `cozy` and `radius` at `md`
- should leave `isStriped` and `isHoverable` off unless the rows are hard to track
