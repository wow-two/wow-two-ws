# Tag

*Last updated: 2026-09-10*

> The removable pill — a badge the reader can take off.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must show a chosen filter, label, or recipient the reader can drop
- must bind `@close` — the close button renders only when a listener exists
- should leave the array to the caller; removal is reported, never applied

---

## Instead of

| Reach for | When |
|---|---|
| [Badge](badge.md) | the pill is inert and nothing removes it |
| `ToggleButton` | the pill toggles a selection instead of being removed |
| [ReactionBar](reactionBar.md) | the pills are emoji reactions with counts |

---

## Values

- should leave `variant` at `neutral` and pick a tone only when it means something
