# ThreadView

*Last updated: 2026-09-10*

> The thread side-panel chrome — parent message, reply count, replies, composer.
> Kind → [view](../../constructs/visual/view.md).

## Reach for it when

- must open one conversation beside the main list, with its own composer
- must fill the parent, replies and composer slots — the panel owns only the chrome

---

## Instead of

| Reach for | When |
|---|---|
| [MessageList](messageList.md) | the surface is the main conversation, not one thread off it |
| [CommentThread](commentThread.md) | the replies nest more than one level |
| `Drawer` | the panel should float over the page rather than sit beside it |

---

## Values

- should leave `hasCloseButton` on — a side panel the reader cannot close is a trap
