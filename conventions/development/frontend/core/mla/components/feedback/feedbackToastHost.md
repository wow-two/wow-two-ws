# FeedbackToastHost

*Last updated: 2026-09-10*

> The bus-to-viewport adapter — mounts the toast viewport and subscribes it to `notify()`.
> What a host is → [host](../../constructs/visual/host.md).

## Reach for it when

- must render notices published through `notify()` or an explicit `FeedbackBus`
- must be mounted once at the app root, in place of a bare [ToastHost](toastHost.md)
- should reach for it whenever a non-view layer raises notices — a query hook

---

## Instead of

| Reach for | When |
|---|---|
| [ToastHost](toastHost.md) | every toast is fired imperatively from view code |
| [UndoBar](undoBar.md) | the notice is a single reversible act, not a queue |

---

## Values

- must follow the [host scope](../../constructs/visual/host.md#gate) and the bus's delivery contract.
