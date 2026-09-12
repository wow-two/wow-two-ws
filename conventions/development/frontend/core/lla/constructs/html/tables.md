# Tables

*Last updated: 2026-09-10*

> Every table element, the header wiring that makes a cell readable, and the shapes that lose the grid.
> Purpose — a table announces a cell's row and column headers; a grid of `div`s announces the cell's text alone.
> Use case — reach here when data has rows and shared columns, and whenever a table needs to scroll or sort.

## The elements

| Element | Means | Verdict |
|---|---|---|
| `<table>` | a grid of data with shared columns | `use` |
| `<caption>` | the table's accessible name, first child | `use` |
| `<thead>` · `<tbody>` · `<tfoot>` | the header, body and summary row groups | `use` |
| `<tr>` | one row | `use` |
| `<th scope="col">` · `<th scope="row">` | a header cell, and the axis it heads | `use` |
| `<td>` | a data cell | `use` |
| `<th>` with no `scope` | a header a reader cannot attach to its cells | `banned` |
| `colspan` · `rowspan` | a cell spanning several columns or rows | `use with care` |
| `<colgroup>` · `<col>` | column-wide styling hooks | `use with care` |
| `headers` on `<td>` | an explicit header link for an irregular table | `use with care` |
| `aria-sort` on a sortable `<th>` | the current sort direction | `use` |
| `aria-rowcount` · `aria-colindex` | the real extent behind a virtualised body | `use with care` |
| `role="grid"` + `role="gridcell"` | a table the arrow keys navigate as a widget | `use with care` |
| a scroll container wrapping `<table>` | horizontal overflow without breaking the grid | `use` |
| `display` utilities on `<tr>` / `<td>` | table rows re-boxed as flex or grid | `banned` |
| `<table>` used for layout | rows and columns that are not in the data | `banned` |
| a grid of `<div>`s carrying tabular data | cells with no row or column headers | `banned` |
| `<caption>` replaced by a heading above the table | a name the table itself does not carry | `use with care` |

- must give every data table a `<caption>` or an `aria-label`, so the reader can tell one table from another.
- must mark every header cell `<th>` with an explicit `scope`.
- must keep `<thead>` / `<tbody>` present — a sticky header row needs the group to stick to.
- must wrap a wide table in an `overflow-x-auto` container rather than shrinking the cells
  ([overflow](../tailwind/overflow.md)).
- must express a card-per-row mobile layout as a second component, never as re-boxed table elements.

---

## Banned

- **`<th>` with no `scope`** — reach for `scope="col"` or `scope="row"`; without it a reader guesses the axis from
  position, so a table with both a header row and a header column announces the wrong header for most cells.
- **`<table>` used for layout** — reach for `grid` or `flex` ([grid](../tailwind/grid.md)); the reader announces
  "table, N rows, M columns" and then reads coordinates for content that has none.
- **a grid of `<div>`s carrying tabular data** — reach for the real elements; each cell is announced as loose text,
  with no way to ask which column it belongs to, so a wide table becomes unreadable off-screen.
- **`display` utilities re-boxing `<tr>` / `<td>`** — reach for a separate mobile component; `flex` on a row destroys
  the table's internal box tree, and browsers drop the row/column relationships along with it.

```vue
<!-- ✅ named, scoped, and scrolled by a wrapper rather than by squeezing cells -->
<div class="overflow-x-auto">
  <table class="w-full border-collapse">
    <caption class="caption-bottom text-xs text-muted-foreground">Saved codes</caption>
    <thead><tr><th scope="col">Name</th><th scope="col">Created</th></tr></thead>
    <tbody><tr v-for="row in rows" :key="row.id"><td>{{ row.name }}</td><td>{{ row.created }}</td></tr></tbody>
  </table>
</div>

<!-- ❌ header cells with no scope — the wrong header is announced for most cells -->
<thead><tr><th>Name</th><th>Created</th></tr></thead>
```

---

## Neighbours

- [lists](lists.md) — the group to reach for when items share no columns
- [global attributes](global-attributes.md) — `aria-sort`, `aria-rowcount`, `role`
- [tables](../tailwind/tables.md) — `border-collapse`, `caption-bottom`, `table-fixed`
- [visual kinds](../../../mla/constructs/visual/visual.md) — `Table`, `DataTable`, `DataGrid`
