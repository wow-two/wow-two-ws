# OnboardingChecklist

*Last updated: 2026-09-10*

> The first-run task card — progress derived from the tasks it holds, not passed to it.
> What a feedback component is → [feedback](../../constructs/visual/feedback.md).

## Reach for it when

- must track a small set of setup tasks a new account works through
- must hold `OnboardingChecklistTask` rows; each registers itself and drives the count
- should reach for it over a [Tour](../overlays/tour.md) when the reader sets the pace

---

## Instead of

| Reach for | When |
|---|---|
| [Tour](../overlays/tour.md) | the flow is walked step by step, right now, over the live UI |
| [ProgressSteps](progressSteps.md) | the stages are sequential and cannot be skipped |
| `Wizard` | the steps collect the input themselves rather than link out to it |

---

## Values

- should set `canDismissOnComplete` where the card has no reason to persist
- should leave `dismissDelay` at `2000` ms — the done state is seen first
