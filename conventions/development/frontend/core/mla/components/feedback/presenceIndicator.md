# PresenceIndicator

*Last updated: 2026-08-23*

> The presence dot — one person's connection state, usually pinned to an avatar.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).
> Its full surface → `PresenceIndicator.vue`.

## Reach for it when

- must encode a person's availability — online, idle, busy, offline, invisible
- must sit on or beside the person it describes, never alone
- should reach for it over a [StatusIndicator](statusIndicator.md) for a person

---

## Instead of

| Reach for | When |
|---|---|
| [StatusIndicator](statusIndicator.md) | the subject is a service and the report carries copy |
| `NotificationDot` | the dot marks unread content rather than a person |
| [TypingIndicator](typingIndicator.md) | the person is composing right now |

---

## Values

- must set `position` only inside a positioned parent — it places itself absolutely
- must set `label` where the status name is not the word the product uses
- should set `hasPulse` for a live socket; it is ignored on every status but `online`
- should leave `status` at `online` only for the reader — peers pass their own
- should leave `size` at `sm`; only `xs` through `lg` carry a diameter
