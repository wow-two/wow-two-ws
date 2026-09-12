# LiveCursor

*Last updated: 2026-09-10*

> A remote collaborator's pointer, drawn on a shared surface.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).

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

- should set `isPointerOnly` where names would crowd the surface
- should leave `labelOffset` at `{ x: 12, y: 16 }` — the label clears the pointer
