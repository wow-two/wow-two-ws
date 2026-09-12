# Surface

*Last updated: 2026-09-10*

> The bare recipe wrapper — fill, border, radius and shadow, with no structure of its own.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must apply the shipped surface recipe to content that brings its own structure
- must reach for `asChild` to merge the recipe onto a child instead of wrapping it
- should reach for it when the recipe varies at the call site

---

## Instead of

| Reach for | When |
|---|---|
| [Frame](frame.md) | the shell is a card or a muted well, and the look is fixed |
| `Card` | the content splits into header, body and footer |
| [Box](box.md) | no fill, border or shadow is wanted |
| [Section](section.md) | the recipe is a full-bleed band behind a centred column |
