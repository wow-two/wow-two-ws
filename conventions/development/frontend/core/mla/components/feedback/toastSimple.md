# ToastSimple

*Last updated: 2026-08-22*

> The toast card's surface with free-form children — elevated, tone-driven, no structure.
> What a feedback component is → [feedback](../../constructs/visual/feedback.md).
> Its full surface → `ToastSimple.spec.md`.

## Reach for it when

- must own the card's whole body rather than fill icon, title, description and actions
- must be the base a product-side toast layout composes on

---

## Instead of

| Reach for | When |
|---|---|
| [Toast](toast.md) | the structured icon, title, description and actions are wanted |
| [ToastHost](toastHost.md) | a queue, a portal and auto-dismiss are wanted with it |
| `Card` | the panel holds content rather than a report — no live region, no elevation |

---

## Values

- must set `severity`; unset falls to `neutral`, unlike its siblings
- should pass `role="alert"` for an interrupting failure; `status` yields to it
