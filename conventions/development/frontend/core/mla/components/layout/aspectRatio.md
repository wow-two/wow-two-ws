# AspectRatio

*Last updated: 2026-09-10*

> The shape lock — a box that holds its ratio before its content has loaded.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must derive a media box's height from its width, ahead of the load
- must hold one child — an image, a video, an embed
- should reach for it wherever a late-loading media box would shift the page

---

## Instead of

| Reach for | When |
|---|---|
| [Frame](frame.md) | the box needs a border and padding, not a fixed shape |
| [Box](box.md) | the height is set outright rather than derived |
| [Center](center.md) | the child is positioned, and the box's shape is free |
