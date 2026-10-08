# ToastHost

*Last updated: 2026-10-02*

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

- must place the toast viewport at `top-right`, respecting the viewport safe area
- must show the SDK severity icon beside each notice
- must keep close as an icon-only control with an accessible label
- must not remove retained history when a toast closes or expires
- retention and deletion → [NotificationCenterGroup](notificationCenterGroup.md#values).
