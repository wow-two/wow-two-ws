# SwipeActions

*Last updated: 2026-09-10*

> Drag a row aside to reveal its actions — the phone row gesture.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must hide per-row commands behind a gesture on a narrow screen
- must offer the same commands somewhere reachable — the gesture is not discoverable
- should keep the revealed set to one or two buttons per side

---

## Instead of

| Reach for | When |
|---|---|
| [Sortable](sortable.md) | the drag reorders the row instead of revealing actions |
| `ContextMenu` | a long-press or right-click should open the commands |
| `ActionSheet` | the phone should get a list of actions as a sheet |
