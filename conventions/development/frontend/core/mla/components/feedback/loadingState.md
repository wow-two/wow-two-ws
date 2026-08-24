# LoadingState

*Last updated: 2026-08-23*

> The centred busy report for a whole section — spinner, title and description, stacked.
> What a state is → [state](../../constructs/visual/state.md).
> Its full surface → `LoadingState.spec.md`.

## Reach for it when

- must fill a section or a route that has nothing to show yet
- must be the report rendered while a first fetch is in flight
- should reach for it over a [Skeleton](skeleton.md) when the shape is unknown

---

## Instead of

| Reach for | When |
|---|---|
| [InlineSpinner](inlineSpinner.md) | the busy mark sits in a row and the layout holds |
| [Skeleton](skeleton.md) | the incoming shape is known and worth drawing |
| [LoadingOverlay](loadingOverlay.md) | content is already on screen and only needs blocking |
| `EmptyState` | the fetch finished and returned nothing |

---

## Values

- must set `description` where the wait is long enough to need explaining
- should leave `title` at `Loading…` and `size` at `lg`
