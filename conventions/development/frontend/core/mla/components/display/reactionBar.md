# ReactionBar

*Last updated: 2026-09-10*

> The row of reaction chips, with an add button on the end.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must hang reactions off a message, a comment, or a post
- must handle `@react` with the chip's key and `@add` to open a picker

---

## Instead of

| Reach for | When |
|---|---|
| [Tag](tag.md) | the pills are labels the reader removes |
| [AvatarGroup](avatarGroup.md) | the strip counts people rather than reactions |
| `ToggleButtonGroup` | the row owns one selection rather than many counts |

---

## Values

- should leave `hasAddButton` on and `hasEmpty` off — a zero-count chip is noise
- should set `isCompact` in a dense row; it drops the counts and keeps the emoji
