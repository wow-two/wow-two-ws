# EmptyState

*Last updated: 2026-10-02*

> The stand-in for a successful empty collection — plain copy within its content region.
> It ships in the SDK's `display/` group but is a [state](../../constructs/visual/state.md), not a
> [display](../../constructs/visual/display.md).

## Reach for it when

- must fill a region whose successful response contains no results
- must be chosen by the owner of the empty region; a table may own its empty row
- must name the absent collection or unmatched filter; never use a bare `No data`
- must not infer an empty result from a failed request

---

## Instead of

| Reach for | When |
|---|---|
| [DataTable](dataTable.md) | the table's own `emptyContent` line is enough |
| `LoadingState` | the region is pending rather than empty |
| `AppErrorBoundary` | the region is empty because a subtree threw |

---

## Values

- must center empty collection copy within the region that would hold its grid or rows
- must render that copy without a card background, border, elevation or decorative illustration
- must leave page actions in the persistent toolbar; an empty result does not own them
- may inherit an existing table or section container; must not add a container for emptiness
