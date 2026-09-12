# Transforms

*Last updated: 2026-09-10*

> Every transform utility, the containing block each one creates, and the moves that should have been layout.
> Purpose — a transform moves paint without moving layout, which is what makes it cheap and what makes it surprising.
> Use case — reach here before nudging, centring, flipping or scaling a box.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `translate-x-*` · `translate-y-*` | a move along one axis, layout unchanged | `use` |
| `-translate-x-1/2` · `-translate-y-1/2` | the centring pair, with `top-1/2 left-1/2` | `use` |
| `translate-x-0` · `translate-y-0` | the resting half of a slide | `use` |
| `scale-*` · `scale-x-*` · `scale-y-*` | a size change that does not reflow | `use` |
| `scale-95` · `scale-100` | the pop-in pair | `use` |
| `rotate-90` · `rotate-180` | a chevron or an icon turned | `use` |
| `-rotate-*` | rotation the other way | `use` |
| `skew-x-*` · `skew-y-*` | a slanted box | `use with care` |
| `origin-center` · `origin-top-left` | the point a transform pivots around | `use` |
| `transform-gpu` · `transform-none` | layer promotion, and a transform removed | `use with care` |
| `perspective-*` · `transform-3d` · `backface-hidden` | three-dimensional transforms | `use with care` |
| `translate-*` on a positioned overlay's own root | a containing block for every `fixed` descendant | `banned` |
| `scale-*` on text | text rendered at a size the type scale does not define | `banned` |
| `translate-*` used to lay a box out | layout expressed where nothing else can see it | `banned` |
| `rotate-*` on a control's hit area | a target the pointer no longer matches | `use with care` |

- must reach for `translate-*` and `scale-*` for motion, and layout utilities for layout.
- must apply [motion rules](transitions.md) when a transform changes over time.
- may use static transforms for centering, mirroring or a fixed orientation without adding motion.
- must keep a transform off any ancestor of a `fixed` child.
- must set `origin-*` whenever a rotation or scale should pivot anywhere but the centre.
- must size text with the type scale, never with `scale-*` ([typography](typography.md)).

---

## Banned

- **a transform on an ancestor of a `fixed` descendant** — reach for a portal
  ([visual kinds](../../../mla/constructs/visual/visual.md)); a transformed element becomes the containing block, so
  every `fixed` child inside pins to it and scrolls away with the page.
- **`scale-*` on text** — reach for a `text-*` step ([typography](typography.md)); scaling resamples the rasterised
  glyphs, so the text blurs and its size stops matching any other text on the screen.
- **translation replacing flow spacing** — use `gap-*`, `p-*` or a grid track; static positioned centering is allowed.

```vue
<!-- ✅ the centring pair, and a slide that is actually animated -->
<div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">…</div>
<div class="translate-y-0 transition-transform data-[state=closed]:translate-y-2">…</div>

<!-- ❌ layout by translation: the box keeps its old space and overlaps its neighbour -->
<div class="translate-x-4">…</div>
```

---

## Neighbours

- [position](position.md) — the offsets the centring pair completes
- [transitions](transitions.md) — what makes a transform motion rather than layout
- [spacing](spacing.md) — where a nudge usually belongs instead
- [effects](effects.md) — opacity, the transform's partner in every enter/exit pair
