# MediaCard

*Last updated: 2026-11-20*

> The image-first card — the media fills it, and its text sits on a blurred fade at the foot.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must reach for it when a record leads with a picture — a post, an event, a listing — and its text fits a short
  panel: a pill row, a two-line title, one or two meta lines
- must lay several out in the auto-fill grid `repeat(auto-fill, minmax(min(100%, 17rem), 1fr))`, which gives 4, 3, 2
  and 1 columns from desktop to phone
- should give a record with no picture the `fallback` tile — its glyph, or its date for an event — never a stock image

---

## Instead of

| Reach for | When |
|---|---|
| [Card](card.md) | the record has no picture to lead with, or its content outgrows a short panel (tags, a summary, an extraction block) |
| [ImagePreview](imagePreview.md) | the picture itself is the content, not a cover for a record |

---

## Values

### Content blur

The blur exists so the content can be read, so the content decides where it sits (developer, 2026-11-20: "the blur's
edge matches the content edge").

- must anchor the blur to the content block it carries, never to a fraction of the card or the media — a fixed
  `h-3/5` drifts off the content when a title wraps, the ratio changes or a pill row is added
- must reach full strength, the blur and the dark wash together, at the content's top edge — the top border of its
  first row, pills included — and hold it down to the card's foot
- must keep the whole fade above that edge: a `2rem` feather, transparent at its top, and nothing of the blur higher
- must size the layer from the content's own box: the blur is a child of the content container,
  `absolute inset-x-0 bottom-0 -top-8`, masked `linear-gradient(to top, black calc(100% - 2rem), transparent)`, so a
  taller content box carries the blur up with it
- must keep the wash and the blur at `bg-gradient-to-t from-black/80 via-black/45` with `backdrop-blur-xl`, white
  text over it, and glass pills (`Badge` `glass`)
- must leave the top-corner controls on the sharp image, each on its own glass — the blur never stretches up to
  reach them
- must apply the same rule to any content laid over imagery outside `MediaCard` — an image header with a title, a
  hero, a captioned tile
