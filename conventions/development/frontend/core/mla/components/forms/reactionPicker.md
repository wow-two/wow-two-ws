# ReactionPicker

*Last updated: 2026-09-10*

> The quick-reaction row — a handful of emoji reached in one click, with a `+` out to the full catalogue.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must react to a message, a comment, or a post without opening anything
- must keep the common reactions one click away and the rest one click behind that
- should mount it inside a `Popover` on hover or long-press

---

## Instead of

| Reach for | When |
|---|---|
| [EmojiPicker](emojiPicker.md) | any emoji is fair game, and search matters |
| `ReactionBar` | the strip reports existing reactions and their counts |
| `ToggleButtonGroup` | the row owns one selection rather than many independent ones |
