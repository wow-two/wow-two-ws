# Menu

*Last updated: 2026-09-10*

> The raw floating menu — the caller owns the anchor and the open state.
> What a nav component is → [nav](../../constructs/visual/nav.md).

## Reach for it when

- must open a list of rows from a gesture none of the wrappers cover
- must anchor the surface to an element the caller already holds
- should be the last resort; the wrappers cover a button, a right-click and a strip

---

## Instead of

| Reach for | When |
|---|---|
| [DropdownMenu](dropdownMenu.md) | a visible button opens it and takes focus back on close |
| [ContextMenu](contextMenu.md) | a right-click or long-press opens it at the pointer |
| [Menubar](menubar.md) | several menus share one strip and one open slot |
| [CommandPalette](commandPalette.md) | the list is long enough that the reader would search it |

---

## Values

- should keep the default `bottom-start` placement and `6` px offset
