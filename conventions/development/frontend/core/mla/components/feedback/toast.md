# Toast

*Last updated: 2026-09-10*

> One transient card, mounted by hand — visual only, with no queue, portal, or timer of its own.
> What a feedback component is → [feedback](../../constructs/visual/feedback.md).

## Reach for it when

- must place a single card outside the app's queue — a story, a bespoke viewport
- must delegate queue, timer and portal ownership to one viewport, whether custom or shared
- should reach for [ToastHost](toastHost.md) in product code — it renders this already

---

## Instead of

| Reach for | When |
|---|---|
| [ToastHost](toastHost.md) | the app fires toasts imperatively and wants one queue |
| [FeedbackToastHost](feedbackToastHost.md) | the notices are published on the headless bus |
| [ToastSimple](toastSimple.md) | the card's body is free-form |
| [Alert](alert.md) | the note stays until the state it reports changes |
