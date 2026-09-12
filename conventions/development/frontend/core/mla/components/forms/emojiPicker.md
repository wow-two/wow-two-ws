# EmojiPicker

*Last updated: 2026-09-10*

> The whole emoji catalogue — search, recents, and a category nav over every bundled glyph.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must let the reader reach any emoji, not a curated handful
- must remember what they used last — recents are the point of the storage seam
- should reach for `EmojiPickerPopover` where it hangs off a trigger

---

## Instead of

| Reach for | When |
|---|---|
| [ReactionPicker](reactionPicker.md) | the row is a handful of quick reactions on a message |
| [IconPicker](iconPicker.md) | the glyphs are UI icons rather than emoji |
| [EmojiSizeControl](emojiSizeControl.md) | the glyph is already chosen and only its scale moves |
| `ReactionBar` | the strip counts existing reactions rather than picking one |

---

## Values

- should leave `size` at `md`, `tileShape` at `rounded`, `rowsCount` at `6`
- should leave `categoryNavVariant` at `strip`; the labelled pills need more width
- should leave the popover variant's `placement` at `bottom` — the house anchor
