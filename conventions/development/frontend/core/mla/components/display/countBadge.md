# CountBadge

*Last updated: 2026-09-10*

> The numeric pill — inbox and notification counts, capped at a maximum.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must show how many unread, pending, or queued items there are
- must let it hide itself at zero rather than branching in the caller
- should mount it through [BadgeOverlay](badgeOverlay.md) to pin it to an icon

---

## Instead of

| Reach for | When |
|---|---|
| [NotificationDot](notificationDot.md) | only the fact that something is new matters, not how many |
| [Badge](badge.md) | the pill's content is a word rather than a count |
| [Stat](stat.md) | the number is a headline metric rather than a marker |

---

## Values

- should leave `max` at `99` — past it the pill reads `99+`
- should leave `canHideZero` on; turn it off only when a `0` must stay visible
