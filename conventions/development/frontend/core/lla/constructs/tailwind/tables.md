# Tables

*Last updated: 2026-09-10*

> The table-specific utilities — layout algorithm, border model, caption side — and the ones that dissolve the grid.
> Purpose — a table's layout algorithm decides whether columns follow content or stay put while the body scrolls.
> Use case — reach here when a table's columns jump on load, or a header has to stay put.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `border-collapse` | one shared edge between adjacent cells | `use` |
| `border-separate` | each cell drawing its own edge | `use with care` |
| `border-spacing-*` · `border-spacing-x-*` | the gap `border-separate` leaves | `use with care` |
| `table-auto` | column widths derived from content — the default | `use` |
| `table-fixed` | column widths from the first row, content ignored | `use` |
| `caption-top` · `caption-bottom` | which side the caption renders on | `use` |
| `w-full` on a `<table>` | a table filling its container ([sizing](sizing.md)) | `use` |
| `overflow-x-auto` on a wrapper | horizontal scroll without touching the table | `use` |
| `sticky top-0` on `<thead>` | a header row pinned while the body scrolls | `use` |
| `table-fixed` with no column widths | every column an equal share, whatever the content | `use with care` |
| `table` · `table-row` · `table-cell` | table boxes made from non-table elements | `use with care` |
| `flex` or `grid` on `<tr>` / `<td>` | a table's internal box tree dissolved | `banned` |
| `border-separate` with `sticky` headers | a header whose own border scrolls away from it | `banned` |
| `overflow-x-auto` on the `<table>` itself | a scroll container the header cannot stick inside | `banned` |
| a fixed `w-*` on every `<td>` | column widths that ignore the content entirely | `banned` |

- must reach for `border-collapse` by default, and `border-separate` only when cells need visible gaps.
- must reach for `table-fixed` when columns must not jump as rows load, and set each width on the header row.
- must put `overflow-x-auto` on a wrapper `<div>`, never on the table ([overflow](overflow.md)).
- must pair a `sticky top-0` header with `border-collapse` and a background token, or the rows show through.
- must keep the elements themselves semantic ([tables](../html/tables.md)).

---

## Banned

- **`flex` or `grid` on `<tr>` / `<td>`** — reach for a separate mobile component ([tables](../html/tables.md)); the
  table's internal boxes are what carry the row and column relationships, and re-boxing drops them along with the
  announcement of which column a cell belongs to.
- **`border-separate` under a sticky header** — reach for `border-collapse`; a separated cell's own border is not part
  of the sticky element, so the header's bottom edge scrolls away and leaves the rows running into it.
- **`overflow-x-auto` on the `<table>`** — reach for a wrapper; the table becomes its own scroll container, so a
  `sticky` header inside it has nothing above to stick to and scrolls with the body.
- **a fixed `w-*` on every cell** — reach for `table-fixed` plus widths on the header row; per-cell widths have to
  agree across every row, and the first row that disagrees decides the column for all of them.

```vue
<!-- ✅ wrapper scrolls, table collapses its borders, header sticks with its own surface -->
<div class="overflow-x-auto">
  <table class="w-full table-fixed border-collapse">
    <thead class="sticky top-0 bg-card"><tr><th scope="col" class="w-48">Name</th></tr></thead>
    <tbody><tr v-for="r in rows" :key="r.id"><td class="truncate">{{ r.name }}</td></tr></tbody>
  </table>
</div>

<!-- ❌ the table scrolls itself, so the sticky header has nothing to stick to -->
<table class="w-full overflow-x-auto border-separate">
  <thead class="sticky top-0"><tr><th scope="col">Name</th></tr></thead>
</table>
```

---

## Neighbours

- [tables](../html/tables.md) — the elements these utilities style
- [overflow](overflow.md) — where the scroll container belongs
- [border](border.md) — the edge widths and colours a collapsed border shares
- [visual kinds](../../../mla/constructs/visual/visual.md) — `Table`, `DataTable`, `DataGrid`
