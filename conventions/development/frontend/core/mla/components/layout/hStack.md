# HStack

*Last updated: 2026-09-10*

> The row preset — [Stack](stack.md) with `direction="row"` fixed at the import.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must lay out a row whose direction is never a call-site choice
- should reach for it over `Stack direction="row"` where the axis pair reads clearer

---

## Instead of

| Reach for | When |
|---|---|
| [Stack](stack.md) | the direction is decided at the call site |
| [Inline](inline.md) | the items wrap onto more lines as the row fills |
| [Cluster](cluster.md) | the wrapping row reads as centred |
| [VStack](vStack.md) | the axis is the column |

---

## Values

- should carry the inherited `gap` default of `4` unless the row is tighter
