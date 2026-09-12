# BackToTopButton

*Last updated: 2026-09-10*

> The scroll-to-top affordance for a long page or a scoped scroll region.
> Kind → [action](../../constructs/visual/action.md).

## Reach for it when

- must reach for it when a page is long enough that its top scrolls out of reach
- must pass `scrollContainer` when the scroll lives on a panel, not the window
- should reach for it icon-only — a visible label is the exception

---

## Instead of

| Reach for | When |
|---|---|
| [Fab](fab.md) | the floating button runs a real command rather than scrolling |
| [SpeedDial](speedDial.md) | more than one command needs the same floating anchor |

---

## Values

- should keep the `bottom-right` anchor; move it only when it collides with a [Fab](fab.md)
