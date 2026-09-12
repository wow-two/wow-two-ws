# Avatar

*Last updated: 2026-09-10*

> A person or entity as an image, falling back to initials.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must stand for a person, a team, or an account in a row or a header
- must pass `name` even with a `src` — it seeds the initials and the auto-colour
- should hang presence or counts off it with [BadgeOverlay](badgeOverlay.md)

---

## Instead of

| Reach for | When |
|---|---|
| [AvatarGroup](avatarGroup.md) | several avatars stack with a `+N` overflow |
| [Image](image.md) | the picture is content rather than an identity |
| [Badge](badge.md) | the identity is better carried by a word than a face |

---

## Values

- should leave `size` at `md`, `shape` at `circle`, `bgStyle` at `solid`, `ring` at `none`
