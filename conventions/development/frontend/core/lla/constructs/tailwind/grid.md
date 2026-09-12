# Grid

*Last updated: 2026-09-10*

> Every grid container and placement utility, and the grids that should have been a flex row.
> Purpose — grid is for two-dimensional layout; reaching for it one-dimensionally costs a track definition per change.
> Use case — reach here when rows and columns both matter, and whenever a column count must follow the viewport.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `grid` · `inline-grid` | a grid container | `use` |
| `grid-cols-1` … `grid-cols-12` | equal columns from the track scale | `use` |
| `grid-rows-*` | explicit rows | `use with care` |
| `grid-cols-[max-content_1fr]` | tracks the numeric scale cannot express | `use with care` |
| `grid-rows-[0fr]` and its `1fr` pair | the animatable height-collapse trick | `use with care` |
| `col-span-*` · `row-span-*` | an item spanning several tracks | `use` |
| `col-span-full` | an item across every column | `use` |
| `col-start-*` · `col-end-*` · `row-start-*` · `row-end-*` | explicit placement | `use with care` |
| `auto-cols-*` · `auto-rows-*` | the size of tracks the browser creates | `use with care` |
| `grid-flow-row` · `grid-flow-col` · `grid-flow-dense` | how items fill the tracks | `use with care` |
| `place-items-center` · `place-content-*` · `place-self-*` | both axes aligned in one utility | `use` |
| `gap-*` on a grid | the space between tracks ([spacing](spacing.md)) | `use` |
| `grid-cols-subgrid` · `grid-rows-subgrid` | tracks inherited from the parent | `use with care` |
| `grid` with one column | responsive or track-aligned layout | `use with care` |
| `grid-flow-dense` on interactive items | a visual order the tab order does not follow | `banned` |
| a fixed `grid-cols-*` that cannot fit its supported viewport | overflowing layout | `banned` |
| a margin between grid children | spacing that a re-flow relocates | `banned` |

- must default to `flex` for a simple one-axis stack ([flexbox](flexbox.md)).
- may use a one-column grid for responsive collapse, shared tracks or deliberate cell overlap.
- must collapse a card layout when its tracks no longer fit ([variants](variants.md)).
- must preserve semantic columns, such as seven calendar weekdays; provide a fitting or scrollable presentation.
- must space tracks with `gap-*`, never margins on the items.
- must reach for `place-items-center` to centre in both axes, over a `flex` plus two alignment utilities.
- must keep `grid-flow-dense` and explicit placement off interactive items — neither moves the tab order.
- must add `min-w-0` to a grid item whose content must truncate ([sizing](sizing.md)).

---

## Banned

- **`grid-flow-dense` on interactive items** — reach for the natural order; dense packing reorders items visually
  while the tab order follows the DOM, so keyboard focus jumps around the screen.
- **an overflowing fixed card grid** — use a responsive column count; semantic grids follow the exception above.
- **a margin between grid children** — reach for `gap-*`; margins do not collapse across grid tracks, so the space
  doubles where two items meet and stays single at the edges.

```vue
<!-- ✅ two axes, responsive down to one column, gap from the scale -->
<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
  <Card v-for="c in codes" :key="c.id" class="min-w-0">…</Card>
</div>

<!-- ❌ a fixed count that overflows a phone, and margins instead of a gap -->
<div class="grid grid-cols-3">
  <Card v-for="c in codes" :key="c.id" class="m-2">…</Card>
</div>
```

---

## Neighbours

- [flexbox](flexbox.md) — the tool for one-dimensional layout
- [spacing](spacing.md) — `gap-*` between tracks
- [sizing](sizing.md) — `min-w-0` on an item that must shrink
- [variants](variants.md) — the breakpoint variants a column count needs
