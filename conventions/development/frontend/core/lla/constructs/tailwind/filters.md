# Filters

*Last updated: 2026-09-10*

> Every filter and backdrop-filter utility, what each costs to paint, and the ones that stand in for a token.
> Purpose — a filter repaints on every composited frame, and it silently changes what `fixed` measures against.
> Use case — reach here before blurring, dimming or desaturating anything.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `backdrop-blur-sm` · `backdrop-blur-md` | the frosted wash behind an overlay or a sticky bar | `use` |
| `backdrop-brightness-*` · `backdrop-saturate-*` | a backdrop dimmed or enriched | `use with care` |
| `blur-sm` … `blur-3xl` | a decorative glow, or an out-of-focus surface | `use with care` |
| `brightness-*` | a hover or pressed state on an image | `use with care` |
| `contrast-*` · `saturate-*` · `sepia-*` | colour grading | `use with care` |
| `grayscale` | a desaturated preview or an inactive thumbnail | `use with care` |
| `invert` | an asset flipped for the opposite theme | `use with care` |
| `hue-rotate-*` | a hue shifted away from its token | `banned` |
| `drop-shadow-*` | a shadow following an alpha shape, such as an icon | `use with care` |
| `filter-none` · `backdrop-filter-none` | filters removed | `use` |
| an arbitrary blur — `backdrop-blur-[1px]` | a radius the scale has no step for | `use with care` |
| `blur-*` on text | text made unreadable and still selectable | `banned` |
| `brightness-*` / `grayscale` standing in for a disabled look | a state expressed as a colour shift | `banned` |
| a filter on an ancestor of a `fixed` child | a containing block created by a paint property | `banned` |
| `backdrop-blur-*` on a full-page overlay on mobile | a whole-viewport repaint per scroll frame | `use with care` |

- must reach for a token before a filter — a colour change is a token change, not a hue rotation.
- must keep `backdrop-blur-*` to a bounded surface: an overlay backdrop, a sticky bar, a card.
- must check for a `fixed` descendant before adding any filter to an ancestor ([position](position.md)).
- must gate a filter that animates on `motion-safe:` ([transitions](transitions.md)).
- must reach for a second asset over `invert` when a logo has to work in both themes.

---

## Banned

- **`hue-rotate-*`** — reach for the token that already names the colour ([color](color.md)); a rotation is computed
  from whatever the source colour happens to be, so re-pointing the token under `.dark` shifts it somewhere unplanned.
- **`blur-*` on text** — reach for a redaction on the data itself; the text stays in the DOM, so it is selectable,
  copyable, readable by a screen reader, and visible in the page source.
- **`brightness-*` or `grayscale` as the disabled look** — reach for the `disabled` attribute with `opacity-50`
  ([effects](effects.md)); a colour shift tells the pointer nothing, so the control still takes focus and still fires.
- **a filter on an ancestor of a `fixed` child** — reach for a portal
  ([visual kinds](../../../mla/constructs/visual/visual.md)); `filter` and `backdrop-filter` both make the ancestor the
  containing block, so the fixed child pins to it and scrolls away.

```vue
<!-- ✅ a bounded frosted backdrop, and a disabled state the pointer can read -->
<div class="fixed inset-0 z-overlay bg-black/45 backdrop-blur-sm" />
<button type="button" disabled class="opacity-50 disabled:cursor-not-allowed">Save</button>

<!-- ❌ blurred text is still selectable and still read aloud; grayscale disables nothing -->
<p class="blur-sm">{{ secret }}</p>
<button type="button" class="grayscale">Save</button>
```

---

## Neighbours

- [effects](effects.md) — opacity and shadow, the cheaper layering tools
- [color](color.md) — the tokens a filter is usually standing in for
- [position](position.md) · [z-index](z-index.md) — what a filter does to a stacking context
- [transitions](transitions.md) — gating an animated filter on the motion preference
