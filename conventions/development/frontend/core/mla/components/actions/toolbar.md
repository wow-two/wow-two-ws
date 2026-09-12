# Toolbar

*Last updated: 2026-09-10*

> A strip of commands sharing one tab stop, arrow keys moving between them.
> What an action is → [action](../../constructs/visual/action.md).

## Reach for it when

- must reach for it for an editor toolbar, action bar, or formatting strip
- must reach for it when tabbing past the strip costs one stop, not one per button
- must not nest a [ToggleButtonGroup](toggleButtonGroup.md) in it — items are flat, roving is not shared
- should compose an existing [Button](button.md) or [ToggleButton](toggleButton.md) through the item's `asChild`

---

## Instead of

| Reach for | When |
|---|---|
| [ButtonGroup](buttonGroup.md) | the buttons only need to look connected, each keeping its tab stop |
| [ToggleButtonGroup](toggleButtonGroup.md) | the strip owns a selected value |
| `Menubar` | the items open menus rather than run commands → [nav](../../constructs/visual/nav.md) |
| [SpeedDial](speedDial.md) | the commands float over the content |

---

## Values

- should split item groups with the separator, which flips axis with the toolbar
