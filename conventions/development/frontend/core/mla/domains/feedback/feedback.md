# Feedback

*Last updated: 2026-08-22*

> The notice bus app code publishes on, and the surface that renders a notice.
> Purpose — a publisher is rarely inside a component, so the hub is module state rather than an injected value.
> Use case — reporting an outcome from anywhere, or turning every failed request into a notice.

## The contract

- must carry a notice as data — tone, title, optional description and action, an id, a duration.
- must give a notice an intent; the tone vocabulary drops the neutral case a notice never has.
- must assign an id when the publisher omits one, and return it from the publish call.
- must stay fire-and-forget with no replay — a notice published before a subscriber mounts is dropped.
- must never let a throwing subscriber reach the publisher; a listener failure routes to the error handler.
- must publish safely with nothing subscribed, so a publisher never guards the call.
- must subscribe nothing automatically ([conventions](../../../../../../conventions.md) § *Product principles*).
- must return an unsubscribe from a subscription, and drop it when the owning scope disposes.
- must render no UI from the bus — the surface is a separate adapter, and the boundary runs one way.
- must keep a bridge to a request seam on this side, so that seam never depends on the bus.
- must mount exactly one rendering adapter per app; two subscribers render every notice twice.

---

## Providers

| Provider | Implements | Reach for it when |
|---|---|---|
| toasts | a subscriber forwarding each notice into the toast API | the default surface, mounted once at the app root |
| the query-error seam | a callback coercing a request failure to a notice | a global request error hook should notify |
| any subscriber | a listener over published notices | a notification centre, a banner region, a test spy |

---

```txt
✅ notify({ tone: NoticeTone.Success, title: 'Saved' })
✅ createQueryClient({ onError: feedbackQueryErrors() })
❌ <ToastHost/> mounted alongside <FeedbackToastHost/>          every notice renders twice
```

---

## Neighbours

- [domains](../domains.md) — the shape every domain follows
- [data](../data/state-and-data.md) — the error the query bridge coerces into a notice
- [feedback components](../../constructs/visual/feedback.md) — the kind that renders a notice
- [observability](../observability/observability.md) — the local record of the same failure
