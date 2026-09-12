# Grid

*Last updated: 2026-09-10*

> The two-axis container — equal tracks and one gap, optionally per breakpoint.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must align items across rows as well as down columns
- must change the track count at a breakpoint, through the responsive map
- should keep the tracks equal — an uneven split is an explicit `gridTemplateColumns`

---

## Instead of

| Reach for | When |
|---|---|
| [Stack](stack.md) | the children run down one axis only |
| [TwoColumn](twoColumn.md) | one column is a fixed-width aside and the other flexes |
| [Inline](inline.md) | the items wrap freely and need no column alignment |
| [ResizablePanels](resizablePanels.md) | the reader drags the split between the tracks |

---

## Values

- should set an explicit `gridTemplateColumns` style for non-uniform tracks
