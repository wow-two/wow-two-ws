# Box

*Last updated: 2026-09-10*

> The box-model utilities — sizing mode, ratio, media fit, float, isolation, column breaks — and the legacy ones.
> Purpose — these change how a box is measured and how content fits inside it, before any other utility applies.
> Use case — reach here when media has to fill a shape, or a box measures differently than expected.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `box-border` | width including padding and border — the reset's default | `use` |
| `box-content` | width excluding them — the legacy box model | `banned` |
| `aspect-square` · `aspect-video` | a box holding its ratio as it resizes | `use` |
| `aspect-auto` · `aspect-[4/3]` | the ratio released, or one the scale lacks | `use with care` |
| `object-cover` | media filling its box, cropping the overflow | `use` |
| `object-contain` | media fitted inside its box, letterboxed | `use` |
| `object-fill` | media stretched to the box, ignoring its ratio | `banned` |
| `object-none` · `object-scale-down` | media unscaled, or shrunk only if too large | `use with care` |
| `object-center` · `object-top` · `object-bottom` | the part kept when cropping | `use` |
| `isolate` · `isolation-auto` | a stacking context that contains its children ([z-index](z-index.md)) | `use` |
| `float-left` · `float-right` · `float-none` | a box taken out of the flow, text wrapping it | `use with care` |
| `clear-left` · `clear-right` · `clear-both` | flow resumed below a float | `use with care` |
| `columns-*` · `break-inside-avoid` | multi-column text, and an item kept whole | `use with care` |
| `break-after-*` · `break-before-*` | a forced break, for print | `use with care` |
| `float-*` used for layout | layout expressed through a text-wrapping mechanism | `banned` |
| `aspect-*` on a box whose content sets its height | a ratio fighting the content | `banned` |
| `object-*` on anything but replaced content | a utility that silently does nothing | `banned` |

- must reach for `aspect-square` plus `object-cover` for any thumbnail, avatar or preview.
- must let `box-border` stand — the reset sets it, and re-declaring it is noise.
- must reach for `float-*` only to wrap prose around a figure inside authored content ([css](../css/css.md)).
- must reach for `isolate` when a subtree's stacking must stay local ([z-index](z-index.md)).
- must set `object-position` whenever a crop would cut the subject — a face, a logo.
- must size media by ratio before pinning both axes ([sizing](sizing.md)).

---

## Banned

- **`box-content`** — reach for `box-border`; padding and border then add to the declared width, so every `w-*` in the
  subtree measures something other than the box on screen, and the layout drifts by exactly the padding.
- **`object-fill`** — reach for `object-cover` or `object-contain`; fill stretches the image to the box, so a portrait
  in a square slot renders visibly distorted rather than cropped.
- **`float-*` for layout** — reach for `flex` or `grid` ([flexbox](flexbox.md)); a float leaves the flow without
  giving the parent height, so the container collapses and a clearfix has to be added back.
- **`aspect-*` on a box whose content sets its height** — reach for `min-h-*`; the ratio and the content give two
  different heights, and the content wins by overflowing.
- **`object-*` on a non-replaced element** — reach for `bg-cover` on a background, or wrap real media; the utility
  applies only to `<img>`, `<video>` and their kin, so on a `<div>` it compiles and does nothing.

```vue
<!-- ✅ ratio first, crop chosen, subject kept in frame -->
<img :src="code.previewUrl" alt="" class="aspect-square w-full rounded-md object-cover object-center" />

<!-- ❌ a stretched portrait, on a box whose content also wants to set the height -->
<img :src="code.previewUrl" alt="" class="aspect-square h-auto object-fill" />
```

---

## Neighbours

- [sizing](sizing.md) — the width and height these utilities constrain
- [overflow](overflow.md) — what happens to what `object-cover` crops away
- [z-index](z-index.md) — `isolate` and the stacking context it makes
- [embedded](../html/embedded.md) — the elements `object-*` actually applies to
