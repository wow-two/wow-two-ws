# AlertSimple

*Last updated: 2026-09-10*

> The alert's tinted container and nothing else — for a body the structured slots cannot shape.
> What a feedback component is → [feedback](../../constructs/visual/feedback.md).

## Reach for it when

- must own the note's whole body — a list, a table, a form fragment
- must be the base a product-side note composes on, when it ships its own layout
- should not be picked to omit a title — [Alert](alert.md) empties its slots too

---

## Instead of

| Reach for | When |
|---|---|
| [Alert](alert.md) | icon, title, description and actions are the layout wanted |
| [Callout](callout.md) | the note is quieter — a left rule, no fill |
| [ToastSimple](toastSimple.md) | the same free-form body is transient and elevated |
