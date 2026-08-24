# ToastHost

*Last updated: 2026-08-22*

> The one toast viewport — a store, a portal, a stack, and a timer per card.
> What a host is → [host](../../constructs/visual/host.md).
> Its full surface → `ToastHost.spec.md`.

## Reach for it when

- must be mounted once per app, at the root, for toasts fired anywhere
- must be the surface every `toastHost.toast()` and `useToastHost()` call lands on
- should reach for [FeedbackToastHost](feedbackToastHost.md) for bus-published notices

---

## Instead of

| Reach for | When |
|---|---|
| [FeedbackToastHost](feedbackToastHost.md) | notices are published headlessly through `notify()` |
| [UndoBar](undoBar.md) | the report is one reversible act with a countdown |
| [Banner](banner.md) | the condition persists and must not scroll away |
| [NotificationCenter](notificationCenter.md) | the notices are browsed later rather than caught live |

---

## Values

- must not mount a second one — every toast would render twice
- must pass `duration: Infinity` for a toast the reader has to dismiss
- must set `key` on a repeatable toast — a re-fire then updates in place
- should leave `defaultDuration` at `5000` ms and `max` at `5`
- should leave `position` at `bottom-right` and `gap` at `8` px
- should leave `canPauseOnHover` on — a paused timer resumes with its remainder
- should reach for `toastHost.promise` for a request — it settles its own loading toast
- should pass `onDismiss` when the toast owns cleanup — it skips on a dedup update
