# Overflow

*Last updated: 2026-09-10*

> Every overflow and overscroll utility, and the clips that hide content with no way to reach it.
> Purpose — `overflow-hidden` is the fastest way to make a layout look right and to make content unreachable.
> Use case — reach here whenever content exceeds its box, and whenever a sticky or a popover stops working.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `overflow-auto` | scrollbars on either axis, only when needed | `use` |
| `overflow-y-auto` · `overflow-x-auto` | a scroll container on one axis | `use` |
| `overflow-hidden` | content clipped, with no way to scroll to it | `use with care` |
| `overflow-hidden` for a rounded corner | a child clipped to its parent's radius | `use` |
| `overflow-visible` | clipping released, so a child may escape | `use` |
| `overflow-scroll` | scrollbars whether or not they are needed | `use with care` |
| `overflow-clip` · `overflow-x-clip` | clipping with no scroll container created | `use with care` |
| `overscroll-contain` · `overscroll-none` | scroll chaining stopped at this container | `use` |
| `truncate` | one clipped line with an ellipsis ([typography](typography.md)) | `use` |
| `line-clamp-*` | several lines, then an ellipsis | `use` |
| `overflow-hidden` on an ancestor of a popover | a floating panel clipped to its parent | `banned` |
| `overflow-hidden` on an ancestor of a `sticky` child | an element that never sticks | `banned` |
| `overflow-hidden` on a text container | content clipped with no scroll and no ellipsis | `banned` |
| `overflow-x-hidden` on `body` to hide a leak | a horizontal overflow suppressed rather than fixed | `banned` |
| a scroll container with no accessible name | a scrollable region a keyboard user cannot find | `use with care` |

- must reach for `overflow-auto` when content may exceed the box, and `overflow-hidden` only to clip to a radius.
- must give a scroll container a bounded height — `max-h-*` or `h-full` — or it never scrolls ([sizing](sizing.md)).
- must add `overscroll-contain` to any scroll area inside an overlay, so the page behind does not scroll with it.
- must check every ancestor for `overflow-hidden` before debugging a clipped popover or a dead `sticky`
  ([position](position.md)).
- must reach for `truncate` or `line-clamp-*` for text, and give the full value another route — a `title`, a tooltip.
- must make a scroll container focusable and named where its content is the point.

---

## Banned

- **`overflow-hidden` on an ancestor of a floating panel** — reach for a portal
  ([visual kinds](../../../mla/constructs/visual/visual.md)); the panel is clipped at the ancestor's edge, so a
  dropdown near the bottom of a card renders as a sliver.
- **`overflow-hidden` on an ancestor of a `sticky` child** — reach for moving the clip; sticky positions against the
  nearest scroll container, and a clipped ancestor becomes one that cannot scroll, so the child simply never pins.
- **`overflow-hidden` on a text container** — reach for `truncate` or `line-clamp-*`; a plain clip cuts mid-word with
  no ellipsis, so the reader gets no signal that anything is missing.
- **`overflow-x-hidden` on `body`** — reach for the element that is too wide; hiding it leaves the page scrollable to
  a blank area on touch, and the real overflow keeps growing behind the clip.

```vue
<!-- ✅ bounded height, contained scroll, ellipsis where text is clipped -->
<div class="max-h-72 overflow-y-auto overscroll-contain">
  <p v-for="row in rows" :key="row.id" class="truncate" :title="row.label">{{ row.label }}</p>
</div>

<!-- ❌ a plain clip: text cut mid-word, and the dropdown inside is clipped to the card -->
<div class="h-72 overflow-hidden">
  <p>{{ row.label }}</p>
</div>
```

---

## Neighbours

- [sizing](sizing.md) — the bounded height a scroll container needs
- [position](position.md) — `sticky`, and what a clip does to it
- [typography](typography.md) — `truncate` and `line-clamp-*`
- [interactivity](interactivity.md) — `scroll-*`, `snap-*`, `overscroll-*`
