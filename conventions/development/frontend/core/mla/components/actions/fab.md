# Fab

*Last updated: 2026-09-10*

> The one floating command a screen pins over its own content.
> What an action is → [action](../../constructs/visual/action.md).

## Reach for it when

- must reach for it for the screen's most prominent action — one per screen
- must reach for it when the command stays reachable while the content scrolls
- should reach for it on touch layouts, where an in-flow button scrolls away

---

## Instead of

| Reach for | When |
|---|---|
| [SpeedDial](speedDial.md) | the same anchor has to offer several commands |
| [BackToTopButton](backToTopButton.md) | the floating command is scroll-to-top |
| [Button](button.md) | the command belongs in the content flow |

---

## Values

- should keep `size="md"` (3.5rem); `sm` (2.5rem) and `lg` (4rem) are the exceptions
