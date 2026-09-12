# PresenceIndicator

*Last updated: 2026-09-10*

> The presence dot — one person's connection state, usually pinned to an avatar.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).

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
