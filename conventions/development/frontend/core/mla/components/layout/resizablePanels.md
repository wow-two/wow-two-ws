# ResizablePanels

*Last updated: 2026-09-10*

> The draggable split — two or more panes the reader resizes by dragging between them.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must let the reader set the split, rather than the layout fixing it
- must compose panels and separators as children, alternating
- should reach for it for an editor beside its preview, or a tree beside a document

---

## Instead of

| Reach for | When |
|---|---|
| [TwoColumn](twoColumn.md) | the aside width is fixed and the reader never moves it |
| [Grid](grid.md) | the tracks are equal and the layout owns them |
| `Drawer` | the second pane opens and closes over the first |
| [ScrollArea](scrollArea.md) | the panes never resize and only one of them scrolls |
