# SpeedDial

*Last updated: 2026-09-10*

> A Fab that fans out into a small stack of secondary commands.
> What an action is → [action](../../constructs/visual/action.md).

## Reach for it when

- must reach for it when one floating anchor has to offer several commands
- should let it replace the screen's [Fab](fab.md) rather than sit beside one

---

## Instead of

| Reach for | When |
|---|---|
| [Fab](fab.md) | the anchor runs exactly one command |
| [Toolbar](toolbar.md) | the commands belong in the content flow, as a strip |
| `ActionSheet` | the choices take the full width of a mobile sheet → [overlay](../../constructs/visual/overlay.md) |

---

## Values

- should keep `gap` at `12` px, and let `direction` derive from `position`
