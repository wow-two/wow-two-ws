# StackLayout

*Last updated: 2026-09-10*

> The default container — children on one axis, with a gap the parent owns.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must place children along one axis with a gap between them
- must reach for it first — it is the arrangement with no more specific sibling
- should reach for it over a hand-written `flex flex-col gap-*` shell

---

## Instead of

| Reach for | When |
|---|---|
| [HStackLayout](hStackLayout.md) | the row never varies, so the direction belongs to the import |
| [VStackLayout](vStackLayout.md) | the column never varies, and the pair reads clearer named |
| [Grid](grid.md) | the children line up on two axes, not one |
| [InlineLayout](inlineLayout.md) | small items wrap onto more lines as the row fills |
| [FlexLayout](flexLayout.md) | the arrangement needs classes this variant matrix has no prop for |

---

## Values

- should leave `align`, `justify` and `wrap` unset — the variant defaults none of them
