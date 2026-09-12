# Position

*Last updated: 2026-09-10*

> Every positioning utility, the containing block each depends on, and the ones that escape the layout entirely.
> Purpose — a positioned box leaves the flow, so it stops reserving space and stops being clipped predictably.
> Use case — reach here before pulling a box out of the flow, and whenever an overlay lands in the wrong place.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `static` | the default — in the flow, offsets ignored | `use` |
| `relative` | in the flow, and the containing block for absolute children | `use` |
| `absolute` | out of the flow, placed against the nearest positioned ancestor | `use` |
| `fixed` | out of the flow, placed against the viewport | `use with care` |
| `sticky` | in the flow until a scroll threshold, then pinned | `use` |
| `top-*` · `right-*` · `bottom-*` · `left-*` | one edge offset, from the spacing scale | `use` |
| `start-*` · `end-*` | edge offsets that follow the writing direction | `use` |
| `inset-0` · `inset-x-0` · `inset-y-0` | all edges, or one axis, at once | `use` |
| `-top-*` · `-right-*` | a negative offset, for a badge overhanging its parent | `use` |
| `top-1/2` · `left-1/2` with `-translate-*` | the centring pair | `use` |
| `top-full` · `bottom-full` | placement flush against a sibling's edge | `use` |
| `top-auto` · `left-auto` | an edge released so another can drive | `use` |
| an arbitrary offset — `right-[35px]` | a position with no scale step behind it | `use with care` |
| `absolute` with no positioned ancestor | a box placed against whatever ancestor happens to qualify | `banned` |
| `fixed` inside a transformed ancestor | a box pinned to the ancestor rather than the viewport | `banned` |
| `sticky` inside an `overflow-hidden` ancestor | a box that never sticks | `banned` |
| a raw `z-*` number beside a positioned box | stacking outside the tier scale ([z-index](z-index.md)) | `banned` |
| `absolute` used to overlap two boxes | overlap that a grid cell expresses in the flow | `use with care` |

- must add `relative` to the intended containing block whenever a child is `absolute`.
- must centre with `top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2`, or with `grid place-items-center`.

---

## Banned

- **`absolute` with no positioned ancestor** — reach for `relative` on the parent; the box falls back to the nearest
  positioned ancestor anywhere up the tree, so it lands correctly until a parent elsewhere gains `relative`.
- **`fixed` inside a transformed ancestor** — reach for a portalled overlay
  ([visual kinds](../../../mla/constructs/visual/visual.md)); a `transform`, `filter` or `backdrop-filter` makes that
  ancestor the containing block, so the box pins to it and scrolls away with the content.
- **`sticky` inside an `overflow-hidden` ancestor** — reach for moving the overflow rule; sticky positions against the
  nearest scroll container, and a clipped ancestor becomes one that never scrolls.
- **a raw `z-*` number** — reach for a tier ([z-index](z-index.md)); a hand-picked number is compared against tiers it
  cannot see, so it wins or loses by accident.

```vue
<!-- ✅ containing block declared, centring pair, tier from the scale -->
<div class="relative">
  <span class="absolute -right-0.5 -top-0.5 z-raised">{{ count }}</span>
  <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">…</div>
</div>

<!-- ❌ no relative parent: the badge lands against whichever ancestor happens to be positioned -->
<div>
  <span class="absolute -right-0.5 -top-0.5">{{ count }}</span>
</div>
```

---

## Neighbours

- [z-index](z-index.md) — the tier a positioned box stacks in
- [transforms](transforms.md) — the centring pair, and what breaks `fixed`
- [overflow](overflow.md) — the clipping that decides whether `sticky` works
- [display](display.md) — what leaving the flow does to the box
