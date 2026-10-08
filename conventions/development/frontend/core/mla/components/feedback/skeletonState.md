# SkeletonState

*Last updated: 2026-10-01*

> The placeholder block — the shape of content that has not arrived yet.
> What a state is → [state](../../constructs/visual/state.md).

## Reach for it when

- must stand in for loading route and section content; use a generic structural shape when the exact layout is unknown
- must be reached for where a spinner would let the layout shift on arrival
- should be repeated to sketch a list or a card, one node per line of real content
- must stand in for a region's values during a user-requested refresh — the [loading pattern](../../domains/data/state-and-data.md#loading)

---

## Instead of

| Reach for | When |
|---|---|
| `Button` `isLoading` | an action is pending; keep its label and focus |
| [InlineSpinner](inlineSpinner.md) | the row keeps its content and only an action is busy |
| [LoadingOverlay](loadingOverlay.md) | content is already on screen and only needs blocking |

---

## Parts

| Part | Reach for it when |
|---|---|
| `SkeletonState` | a known shape has no content yet |
| `SkeletonStateText` | a paragraph is pending; the last line runs shorter |
| `SkeletonStateSlot` | a value sits inside a layout that stays — its placeholder takes the value's exact size |
| `SkeletonStateGroup` | a region loads as one — it sets `aria-busy`, announces once and switches every slot together |

---

## Values

- must route the loading announcement through the owning region; repeated skeleton shapes remain decorative.
