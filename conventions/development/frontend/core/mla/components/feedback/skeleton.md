# Skeleton

*Last updated: 2026-08-23*

> The placeholder block — the shape of content that has not arrived yet.
> What a state is → [state](../../constructs/visual/state.md).
> Its full surface → `Skeleton.spec.md`.

## Reach for it when

- must stand in for content whose layout is already known
- must be reached for where a spinner would let the layout shift on arrival
- should be repeated to sketch a list or a card, one node per line of real content

---

## Instead of

| Reach for | When |
|---|---|
| [LoadingState](loadingState.md) | the incoming shape is unknown, or the whole route is waiting |
| [InlineSpinner](inlineSpinner.md) | the row keeps its content and only an action is busy |
| [LoadingOverlay](loadingOverlay.md) | content is already on screen and only needs blocking |

---

## Values

- must size it through `class` — `w-32 h-4` for a line, a box for a block
- must set `shape` to `text` for a line, `circle` for an avatar; `rect` is default
- must not rely on it to announce — it is `aria-hidden`, so pair a live region with it
