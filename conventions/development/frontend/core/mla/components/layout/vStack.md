# VStack

*Last updated: 2026-09-10*

> The column preset — [Stack](stack.md)'s own default, named for symmetry with [HStack](hStack.md).
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must pair a column with an [HStack](hStack.md) so both axes read the same way
- must not reach for it with no [HStack](hStack.md) nearby — [Stack](stack.md) is already the column

---

## Instead of

| Reach for | When |
|---|---|
| [Stack](stack.md) | no [HStack](hStack.md) is in sight — the column is its default already |
| [HStack](hStack.md) | the axis is the row |
