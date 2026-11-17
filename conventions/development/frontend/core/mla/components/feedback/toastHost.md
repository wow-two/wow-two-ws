# ToastHost

*Last updated: 2026-11-15*

> The one toast viewport — a store, a portal, a stack, and a timer per card.
> What a host is → [host](../../constructs/visual/host.md).

## Reach for it when

- must mount one renderer per bus scope; application-wide notices use the application root.
- must publish through the matching scope's documented publisher so notices cannot leak between applications or SSR requests.
- should reach for [FeedbackToastHost](feedbackToastHost.md) for bus-published notices

---

## Instead of

| Reach for | When |
|---|---|
| [FeedbackToastHost](feedbackToastHost.md) | notices are published headlessly through `notify()` |
| [UndoBar](undoBar.md) | the report is one reversible act with a countdown |
| [Banner](banner.md) | the condition persists and must not scroll away |
| [NotificationCenterGroup](notificationCenterGroup.md) | the notices are browsed later rather than caught live |

---

## Values

- must follow the [host scope](../../constructs/visual/host.md#gate) and the bus's delivery contract.

- must default the toast viewport to `top-right` and respect the safe area at the selected edge
- must offset the viewport below a fixed app bar and fit the cards within the available width
- must show the SDK severity icon beside each notice
- must keep close as an icon-only control with an accessible label
- must remove the selected toast's countdown while pinned and restart it at full duration on unpin
- must offer pin on standard timed toasts by default
- must keep actual deadlines independent of the stack order and interaction holds
- must not remove retained history when a toast closes or expires
- retention and deletion → [NotificationCenterGroup](notificationCenterGroup.md#values).
