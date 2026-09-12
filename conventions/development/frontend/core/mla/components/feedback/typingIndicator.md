# TypingIndicator

*Last updated: 2026-09-10*

> Three bouncing dots — someone is composing, right now.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).

## Reach for it when

- must show live composition in a chat, a comment thread, or an assistant reply
- must be mounted only while the signal is live — it holds no timer of its own
- should sit where the message will land, so the list does not jump

---

## Instead of

| Reach for | When |
|---|---|
| [PresenceIndicator](presenceIndicator.md) | the report is the person's connection state |
| [InlineSpinner](inlineSpinner.md) | the wait is a request, not a person |
| [Skeleton](skeleton.md) | the incoming message's shape is already known |

---

## Values

- should set `isSubtle` in a dense thread, so the dots recede between bounces
