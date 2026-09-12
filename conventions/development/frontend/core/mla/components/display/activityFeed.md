# ActivityFeed

*Last updated: 2026-09-10*

> Who did what to which thing — sentences down a rail, with avatars.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must show a stream of actions — an audit log, a project feed, a record's history
- must compose `ActivityItem` rows; the feed owns the rail, not the sentence
- should carry the avatar, preview and actions in their slots

---

## Instead of

| Reach for | When |
|---|---|
| [Timeline](timeline.md) | the entries are events with titles rather than actor sentences |
| [MessageList](messageList.md) | the entries are messages people wrote to each other |
| [CommentThread](commentThread.md) | the entries nest as replies |
