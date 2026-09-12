# Box

*Last updated: 2026-09-10*

> The lowest primitive — one element and one class, arranging nothing of its own.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must wrap something that needs a class and no arrangement at all
- must swap the rendered tag through `as`, without a wrapper around it
- should be the last layout tried — every sibling says more about the arrangement

---

## Instead of

| Reach for | When |
|---|---|
| [Flex](flex.md) | the children have to sit on a flex line |
| [Stack](stack.md) | the axis and the gap between children are the point |
| [Frame](frame.md) | the shell carries a border, a padding and a radius |
| [Surface](surface.md) | the shell carries the fill, border and shadow recipe |
