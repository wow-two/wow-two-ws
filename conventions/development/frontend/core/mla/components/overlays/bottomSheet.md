# BottomSheet

*Last updated: 2026-09-10*

> The draggable bottom surface — a handle and snap heights, for a body the reader resizes.
> What an overlay is → [overlay](../../constructs/visual/overlay.md).

## Reach for it when

- must let the reader resize the surface — a map peek, a list that grows to full height
- should sit on the bottom edge, where a thumb reaches it
- must offer an explicit dismissal control as well as a drag gesture

---

## Instead of

| Reach for | When |
|---|---|
| [Drawer](drawer.md) | the bottom panel rests at one height and needs no handle |
| [ActionSheet](actionSheet.md) | the body is a row per action rather than free content |
| [Modal](modal.md) | the same place on a wide viewport |

---

## Values

- should leave `snapPoints` at `['40vh', '90vh']` unless the body has a natural rest height
