# NotificationCenter

*Last updated: 2026-09-10*

> The panel of notices already delivered — a header, a scrolling list, an optional footer.
> Kind → [display](../../constructs/visual/display.md).

## Reach for it when

- must let the reader browse past notices rather than catch them as they pass
- must show past notices with a meaningful empty state when none exist
- should sit inside a `Popover` or a `Drawer` hung off the shell's bell

---

## Instead of

| Reach for | When |
|---|---|
| [ToastHost](toastHost.md) | the notice is transient and has to be caught as it happens |
| `ActivityFeed` | the list is a domain record rather than a report to the reader |
| `NotificationDot` | only the unread count belongs on the trigger |

---

## Values

- should override the `emptyState` slot only where its default copy is wrong
- should mark a row `isUnread` rather than sort it — the row carries its own emphasis
