# DropdownMenu

*Last updated: 2026-09-10*

> The button-triggered menu — the shape to reach for by default.
> What a nav component is → [nav](../../constructs/visual/nav.md).

## Reach for it when

- must hang a short list of destinations or commands off a visible trigger
- must let a keyboard reader open the list from the trigger and land on an item
- should be the first menu tried — the other three exist for gestures it cannot serve

---

## Instead of

| Reach for | When |
|---|---|
| [Menu](menu.md) | the anchor or the open state is owned elsewhere |
| [ContextMenu](contextMenu.md) | the gesture is a right-click over a region, not a button |
| [Menubar](menubar.md) | several triggers share one strip and one open slot |
| [NavigationMenu](navigationMenu.md) | the trigger drops a rich panel, not a list of rows |
| [CommandPalette](commandPalette.md) | the list is long and the reader would rather search it |

---

## Values

- should keep the default `bottom-start` placement and `6` px offset
