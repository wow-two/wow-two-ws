# OptionTileGroup

*Last updated: 2026-09-10*

> The labelled fieldset wrapping a row or grid of [OptionTile](optionTile.md)s.
> Kind → [field](../../constructs/visual/field.md).

## Reach for it when

- must wrap every [OptionTile](optionTile.md) set — it carries the group's accessible name
- must reach for it to disable a whole grid — one flag blocks every tile
- should reach for `wrap` when the tiles outrun a single row

---

## Instead of

| Reach for | When |
|---|---|
| [ToggleButtonGroup](toggleButtonGroup.md) | the group should own the selected value rather than the caller |
| [ButtonGroup](buttonGroup.md) | the row is commands, with no selection to track |
| [Toolbar](toolbar.md) | the row needs one tab stop and arrow-key movement |

---

## Values

- should keep `align` at `start` and `wrap` off, the defaults for a single tile row
