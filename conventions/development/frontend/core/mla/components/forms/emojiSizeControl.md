# EmojiSizeControl

*Last updated: 2026-09-10*

> The three size presets for a chosen emoji, each tile previewing the real glyph rather than naming a number.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must scale a glyph the reader already picked — [EmojiPicker](emojiPicker.md) chose it, this sizes it
- must show the choice as the glyph itself, since a ratio means nothing on its own
- should reach for it wherever an emoji is placed on a surface at a chosen scale

---

## Instead of

| Reach for | When |
|---|---|
| [EmojiPicker](emojiPicker.md) | the choice is which emoji, not how big |
| [Slider](slider.md) | the scale is continuous rather than three presets |
| [ChoiceCard](choiceCard.md) | the options need a title and description each |
| `ToggleButtonGroup` | the options are words with nothing to preview |

---

## Values

- should leave `maxPreviewGlyph` at `24` px, the cap that stops a glyph clipping its tile
