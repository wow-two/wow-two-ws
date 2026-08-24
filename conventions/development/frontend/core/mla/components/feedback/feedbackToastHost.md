# FeedbackToastHost

*Last updated: 2026-08-22*

> The bus-to-viewport adapter — mounts the toast viewport and subscribes it to `notify()`.
> What a host is → [host](../../constructs/visual/host.md).
> Its full surface → `FeedbackToastHost.vue`.

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

- must not mount it beside a [ToastHost](toastHost.md) — every toast would render twice
- must mount it above anything that publishes; notices raised before mount are dropped
- should leave `bus` unset — it binds the `feedbackBus` that `notify()` publishes on
- should pass any [ToastHost](toastHost.md) value straight through — they all forward
