# BadgeOverlay

*Last updated: 2026-09-10*

> The corner mount — it pins any badge onto any child.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must hang a [CountBadge](countBadge.md) or [Badge](badge.md) off an avatar or an icon button
- must keep the wrapped child unchanged; the wrapper owns only the corner
- should hide the badge through `isHidden` rather than unmounting it in the caller

---

## Instead of

| Reach for | When |
|---|---|
| [NotificationDot](notificationDot.md) | the dot's own `position` already pins it to the parent |
| [AvatarGroup](avatarGroup.md) | the thing stacked on the avatar is another avatar |

---

## Values

- should leave `position` at `top-right`, the house corner
