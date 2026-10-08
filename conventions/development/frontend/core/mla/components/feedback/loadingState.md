# LoadingState

*Last updated: 2026-10-01*

> The centred busy report for a whole section — spinner, title and description, stacked.
> What a state is → [state](../../constructs/visual/state.md).

## Reach for it when

- must use [SkeletonState](skeletonState.md) for route and section content while data loads, including a generic structural skeleton when the exact shape is unknown
- must not introduce a visible `Loading…` paragraph or centred spinner as the content placeholder
- may retain this component for compatibility; new app content follows the [loading pattern](../../domains/data/state-and-data.md#loading)
- must keep action loading on the initiating button, with its label retained

---

## Instead of

| Reach for | When |
|---|---|
| [InlineSpinner](inlineSpinner.md) | the busy mark sits in a row and the layout holds |
| [SkeletonState](skeletonState.md) | the incoming shape is known and worth drawing |
| [LoadingOverlay](loadingOverlay.md) | content is already on screen and only needs blocking |
| `EmptyState` | the fetch finished and returned nothing |
