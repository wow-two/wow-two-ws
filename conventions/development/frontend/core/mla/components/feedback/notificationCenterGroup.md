# NotificationCenterGroup

*Last updated: 2026-10-02*

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
| `ActivityTimeline` | the list is a domain record rather than a report to the reader |
| `NotificationIndicator` | only the unread count belongs on the trigger |

---

## Values

- must retain notices only through an explicit retained category in the owning bus scope
- must keep retained notices available until their delete action or scope reset
- must render close and delete as accessible icon-only controls
- must offer delete only for retained notices; close dismisses the current surface
- may add notice-specific actions through the shared notice contract
- must keep retention separate from automatic toast duration
- must clear scoped notices on logout or identity change
- must wire durable storage explicitly; must not persist notices automatically
- should override the `emptyState` slot only where its default copy is wrong
- should mark a row `isUnread` rather than sort it — the row carries its own emphasis
