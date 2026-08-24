# Toast

*Last updated: 2026-08-22*

> One transient card, mounted by hand — visual only, with no queue, portal, or timer of its own.
> What a feedback component is → [feedback](../../constructs/visual/feedback.md).
> Its full surface → `Toast.spec.md`.

## Reach for it when

- must place a single card outside the app's queue — a story, a bespoke viewport
- must be reached for only where the caller owns the mount, the timer, and the portal
- should reach for [ToastHost](toastHost.md) in product code — it renders this already

---

## Instead of

| Reach for | When |
|---|---|
| [ToastHost](toastHost.md) | the app fires toasts imperatively and wants one queue |
| [FeedbackToastHost](feedbackToastHost.md) | the notices are published on the headless bus |
| [ToastSimple](toastSimple.md) | the card's body is free-form |
| [Alert](alert.md) | the note stays until the state it reports changes |

---

## Values

- must bind `@close` to get a close button — an unbound handler renders none
- must set `severity`; unset falls through to `neutral` on the underlying card
- must not add a timer around it — auto-dismiss belongs to [ToastHost](toastHost.md)
- should leave `closeLabel` at `Dismiss`
