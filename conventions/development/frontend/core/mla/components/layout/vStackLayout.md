# VStackLayout

*Last updated: 2026-09-10*

> The column preset — [StackLayout](stackLayout.md)'s own default, named for symmetry with [HStackLayout](hStackLayout.md).
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must pair a column with an [HStackLayout](hStackLayout.md) so both axes read the same way
- must not reach for it with no [HStackLayout](hStackLayout.md) nearby — [StackLayout](stackLayout.md) is already the column

---

## Instead of

| Reach for | When |
|---|---|
| [StackLayout](stackLayout.md) | no [HStackLayout](hStackLayout.md) is in sight — the column is its default already |
| [HStackLayout](hStackLayout.md) | the axis is the row |
