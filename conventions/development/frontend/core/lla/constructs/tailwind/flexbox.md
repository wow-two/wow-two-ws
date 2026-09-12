# Flexbox

*Last updated: 2026-09-10*

> Every flex container and item utility, and the spellings that make a row stop shrinking or stop wrapping.
> Purpose — flex is the default layout tool here; a one-dimensional row or column needs nothing else.
> Use case — reach here before laying anything out, and whenever a flex child overflows its parent.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `flex` · `inline-flex` | a flex container, block-level or inline | `use` |
| `flex-row` · `flex-col` | the main axis | `use` |
| `flex-row-reverse` · `flex-col-reverse` | a visual order that no longer matches the DOM | `use with care` |
| `flex-wrap` · `flex-nowrap` · `flex-wrap-reverse` | whether items may move to a second line | `use` |
| `items-center` · `items-start` · `items-end` · `items-stretch` | cross-axis alignment for every item | `use` |
| `items-baseline` | text baselines aligned across differently sized items | `use` |
| `justify-start` · `justify-center` · `justify-end` | main-axis packing | `use` |
| `justify-between` · `justify-around` · `justify-evenly` | main-axis distribution | `use` |
| `content-*` | cross-axis packing of wrapped lines | `use with care` |
| `place-items-*` · `place-content-*` | both axes in one utility | `use` |
| `self-start` · `self-center` · `self-end` · `self-stretch` | one item overriding `items-*` | `use` |
| `flex-1` · `flex-auto` · `flex-initial` · `flex-none` | the grow / shrink / basis shorthand | `use` |
| `grow` · `grow-0` · `shrink` · `shrink-0` | one axis of that shorthand | `use` |
| `basis-*` | the item's starting size before growing | `use with care` |
| `order-*` · `order-first` · `order-last` | a visual order the tab order does not follow | `use with care` |
| `min-w-0` on a flexible child | a child allowed to shrink below its content | `use` |
| `justify-*` used to space siblings | gaps produced by pushing rather than by a scale | `banned` |
| a margin used as the gap between flex children | spacing that a wrap or a reorder breaks | `banned` |
| `flex` with no direction on a wrapping row | an implicit `row` a reader has to infer | `use with care` |

- must space children with `gap-*`, never with margins on the children ([spacing](spacing.md)).
- must add `shrink-0` to anything fixed-size inside a flex row — an icon, an avatar, a badge.
- must add `min-w-0` to the flexible child whenever its content must truncate ([sizing](sizing.md)).
- must keep `order-*` and `-reverse` off anything interactive — neither moves the tab order.
- must reach for `ml-auto` to push one item, and `justify-between` only when the ends are the intent.

---

## Banned

- **`justify-*` standing in for spacing** — reach for `gap-*`; distribution divides whatever space is left, so the gap
  changes with the container's width and matches no step in the scale.
- **a margin between flex children** — reach for `gap-*`; a margin survives a `flex-wrap` line break as a leading edge
  gap, and `-reverse` puts it on the wrong side of the item.
- **a flex child with no `min-w-0` that must truncate** — reach for `min-w-0`; a flex item's default minimum is its
  content size, so `truncate` never engages and the row overflows its parent instead.

```vue
<!-- ✅ icon fixed, label shrinkable and truncating, gap from the scale -->
<div class="flex items-center gap-2">
  <IconFile aria-hidden="true" class="size-4 shrink-0" />
  <span class="min-w-0 flex-1 truncate">{{ file.name }}</span>
</div>

<!-- ❌ no min-w-0, so truncate never engages and the row overflows -->
<div class="flex items-center gap-2">
  <span class="flex-1 truncate">{{ file.name }}</span>
</div>
```

---

## Neighbours

- [grid](grid.md) — the tool for two-dimensional layout
- [spacing](spacing.md) — `gap-*`, and why it beats margins here
- [sizing](sizing.md) · [overflow](overflow.md) — `min-w-0`, `truncate` and what makes a row shrink
- [display](display.md) — what `flex` and `inline-flex` change about the box
