# LiveCursor

*Last updated: 2026-08-23*

> A remote collaborator's pointer, drawn on a shared surface.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).
> Its full surface → `LiveCursor.vue`.

## Reach for it when

- must show where another person is pointing on a canvas, a board, or an editor
- must be mounted once per remote peer, keyed by that peer's id
- must be wrapped by a `position: relative` parent — it places itself absolutely

---

## Instead of

| Reach for | When |
|---|---|
| [PresenceIndicator](presenceIndicator.md) | only the person's connection state matters, not their position |
| [TypingIndicator](typingIndicator.md) | the person is composing rather than pointing |

---

## Values

- must pass `x` and `y` in pixels relative to the parent's top-left corner
- must give each peer its own `color` — the default suits a single peer
- should set `isPointerOnly` where names would crowd the surface
- should leave `isSmooth` on — it disables itself under reduced motion
- should leave `labelOffset` at `{ x: 12, y: 16 }` — the label clears the pointer
