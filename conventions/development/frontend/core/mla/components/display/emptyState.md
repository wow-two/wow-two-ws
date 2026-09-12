# EmptyState

*Last updated: 2026-09-10*

> The stand-in for content that is absent — icon, title, line, and a way out.
> It ships in the SDK's `display/` group but is a [state](../../constructs/visual/state.md), not a
> [display](../../constructs/visual/display.md).

## Reach for it when

- must fill a region whose data came back empty, offering a next action
- must be chosen by the owner of the empty region; a table may own its empty row
- should name why it is empty and what to do — never a bare `No data`

---

## Instead of

| Reach for | When |
|---|---|
| [DataTable](dataTable.md) | the table's own `emptyContent` line is enough |
| `LoadingState` | the region is pending rather than empty |
| `AppErrorBoundary` | the region is empty because a subtree threw |

---

## Values

- should leave `size` at `md`; `sm` inside a card, larger for a whole page
