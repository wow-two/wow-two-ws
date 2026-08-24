# NotificationCenter

*Last updated: 2026-08-23*

> The panel of notices already delivered — a header, a scrolling list, an optional footer.
> What a panel is → [panel](../../constructs/visual/panel.md).
> Its full surface → `NotificationCenter.vue`.

## Reach for it when

- must let the reader browse past notices rather than catch them as they pass
- must hold `NotificationItem` rows — the panel derives its empty state from them
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

- must leave `count` unset rather than pass `0` — a zero still renders the badge
- must bind a row's `@select` to make it interactive; an unbound row stays inert
- should override the `emptyState` slot only where its default copy is wrong
- should leave `title` at `Notifications`
- should mark a row `isUnread` rather than sort it — the row carries its own emphasis
