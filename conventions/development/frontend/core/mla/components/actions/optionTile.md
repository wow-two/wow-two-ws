# OptionTile

*Last updated: 2026-09-10*

> An icon-only square tile for a preset grid — fill types, module shapes, gradient presets.
> Kind → [control](../../constructs/visual/control.md).

## Reach for it when

- must reach for it when the option reads as a glyph or swatch, not a word
- must mount it inside an [OptionTileGroup](optionTileGroup.md) — it carries name and disabled state
- should keep the active value on the parent; the tile takes `selected`

---

## Instead of

| Reach for | When |
|---|---|
| [ToggleButton](toggleButton.md) | the option carries a visible word label |
| [ToggleButtonGroup](toggleButtonGroup.md) | the strip itself should own the selected value |
| [Button](button.md) | picking the option runs a command instead of leaving a selection |
