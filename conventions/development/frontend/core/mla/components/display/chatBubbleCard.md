# ChatBubbleCard

*Last updated: 2026-09-10*

> One message in a conversation — a side, a tone, and a delivery state.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must render a single message inside a [MessageGroup](messageGroup.md)
- must set `tone="system"` for a join, leave, or metadata row; it centres itself

---

## Instead of

| Reach for | When |
|---|---|
| [CommentThreadGroup](commentThreadGroup.md) | the message is a comment carrying nested replies |
| [ActivityTimeline](activityTimeline.md) | the row is an actor-verb-target sentence, not a message |
| [Card](card.md) | the message is a record rather than a turn in a conversation |
