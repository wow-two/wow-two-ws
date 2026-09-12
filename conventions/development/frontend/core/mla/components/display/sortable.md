# Sortable

*Last updated: 2026-09-10*

> Drag-to-reorder — headless, handle-initiated, and it never owns the array.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must let the reader set an order by hand — a playlist, a checklist, a column set
- must compose `SortableItem` per row and `SortableHandle` inside it
- should apply the move in the caller; `@reorder` reports raw `from` and `to` indices

---

## Instead of

| Reach for | When |
|---|---|
| [DataTable](dataTable.md) | the order comes from sorting a column, not from the reader |
| [List](list.md) | the order is fixed |
| [SwipeActions](swipeActions.md) | the drag reveals actions rather than moving the row |

---

## Values

- must provide keyboard and single-pointer move commands with the same result as dragging.
- must identify moved items stably and reject stale reorder requests rather than blindly applying indices.
