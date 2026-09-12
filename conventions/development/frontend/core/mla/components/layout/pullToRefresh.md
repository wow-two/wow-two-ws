# PullToRefresh

*Last updated: 2026-09-10*

> The drag-to-refresh wrapper — a phone gesture over a region that scrolls.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must refresh a list on a downward drag from the top, on touch
- must let it own the scrolling — its own root is the scroll container
- should pair it with a visible refresh command for pointer users

---

## Instead of

| Reach for | When |
|---|---|
| [ScrollArea](scrollArea.md) | the region scrolls and nothing refreshes |
| `Button` | the refresh is a command a pointer user clicks |
| `LoadingState` | the wait is a load, not a reader-initiated refresh |
