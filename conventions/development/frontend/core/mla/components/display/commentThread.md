# CommentThread

*Last updated: 2026-09-10*

> Nested comments — a `tree` of `Comment` rows, each collapsing its own replies.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must show replies that hang off replies — a review, a document, a discussion
- must nest through each `Comment`'s replies slot; the root owns only the `tree` role
- should carry avatar, badge and actions in their slots, and author and timestamp as props

---

## Instead of

| Reach for | When |
|---|---|
| [MessageList](messageList.md) | the messages are a flat stream in time order |
| [ThreadView](threadView.md) | the panel is one thread with a composer, replies flat |
| [Tree](tree.md) | the nodes are data rather than comments |
