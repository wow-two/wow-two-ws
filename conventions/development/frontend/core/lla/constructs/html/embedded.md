# Embedded

*Last updated: 2026-09-10*

> Every element that pulls content in from outside the document, and the ones we never embed.
> Purpose — embedded content is the only markup that fails at runtime, shifts the layout, or runs foreign code.
> Use case — reach here before adding an image, an icon, a media player or a frame.

## The elements

| Element | Means | Verdict |
|---|---|---|
| `<img src alt>` | a raster image with a text alternative | `use` |
| `<img alt="">` | an image that adds nothing a caption does not already say | `use` |
| `<img>` with no `alt` | an image a reader announces by its file name | `banned` |
| `<svg>` inline | vector artwork the document can style and animate | `use` |
| `<svg aria-hidden="true">` | decorative artwork beside its own visible label | `use` |
| `<svg role="img">` + `<title>` | artwork that carries meaning on its own | `use` |
| `<picture>` · `<source>` · `srcset` · `sizes` | one image chosen per format or viewport | `use with care` |
| `<img loading="lazy" decoding="async">` | a below-the-fold image deferred | `use` |
| `width` / `height` on `<img>` | the intrinsic ratio that reserves the box | `use` |
| `<figure>` · `<figcaption>` | embedded content with its caption bound to it | `use with care` |
| `<video>` · `<audio>` | a media player with native controls | `use with care` |
| `<track kind="captions">` | timed text for a media element | `use` |
| `<canvas>` | a bitmap a script paints, with no accessible content | `use with care` |
| `<iframe title sandbox>` | a nested browsing context, named and confined | `use with care` |
| `<iframe>` with no `title` | a frame announced as "frame" and nothing else | `banned` |
| `<object>` · `<embed>` | the plugin-era embedding elements | `banned` |
| `<map>` · `<area>` | click regions positioned over an image | `banned` |
| `autoplay` on `<video>` / `<audio>` | media that starts without being asked | `banned` |
| a background image standing in for content | an image no reader can announce | `banned` |

- must give every `<img>` an `alt` — descriptive when it carries meaning, empty when it does not.
- must set `width` and `height`, so the box is reserved before the bytes arrive.
- must mark a decorative `<svg>` `aria-hidden="true"`, and name a meaningful one with `role="img"` and a `<title>`.
- must give every `<iframe>` a `title` and the narrowest `sandbox` that still works.
- must ship captions with any `<video>` that carries speech.
- must size media through utilities, never `width` / `height` attributes doing layout
  ([sizing](../tailwind/sizing.md)).

---

## Banned

- **`<img>` with no `alt`** — reach for `alt=""` when decorative and real text when not; with the attribute missing
  entirely a screen reader falls back to announcing the file name, one URL segment at a time.
- **`<iframe>` with no `title`** — reach for a `title` naming the embedded document; the frame appears in the landmark
  list as "frame", so a user cannot tell which of several to enter.
- **`<object>` · `<embed>`** — reach for `<img>`, inline `<svg>` or `<video>`; both are plugin-era elements with
  inconsistent fallback handling and no reliable accessible name.
- **`<map>` · `<area>`** — reach for positioned `<button>`s over the image; the coordinates are in image pixels, so
  every responsive resize moves the hit area away from the thing it targets.
- **`autoplay`** — reach for a play control; audio starting on load talks over a screen reader mid-announcement, and
  it ignores `prefers-reduced-motion`.
- **a CSS background image carrying content** — reach for `<img>`; a background has no `alt`, so the content is
  invisible to a reader and absent from the printed page.

```vue
<!-- ✅ box reserved before load, decorative icon silenced beside its own visible label -->
<img :src="code.previewUrl" :alt="`Preview of ${code.name}`" width="240" height="240" loading="lazy" />
<button type="button"><IconTrash aria-hidden="true" class="size-4" /> Delete</button>

<!-- ❌ no alt at all — the reader announces the URL's file name -->
<img :src="code.previewUrl" class="size-60" />
```

---

## Neighbours

- [flow](flow.md) — the boxes these sit inside
- [global attributes](global-attributes.md) — `aria-hidden`, `role`, `title`
- [sizing](../tailwind/sizing.md) · [box](../tailwind/box.md) — `size-*`, `aspect-*`, `object-*`
- [visual kinds](../../../mla/constructs/visual/visual.md) — the icon and media components already built
