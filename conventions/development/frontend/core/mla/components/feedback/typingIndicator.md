# TypingIndicator

*Last updated: 2026-08-23*

> Three bouncing dots — someone is composing, right now.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).
> Its full surface → `TypingIndicator.vue`.

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

- must set `who` to name the typist — the label falls back to `Typing`
- should set `isSubtle` in a dense thread, so the dots recede between bounces
- should leave `size` at `md` and `tone` at `muted` — only `sm`–`lg` size a dot
