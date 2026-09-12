# Confetti

*Last updated: 2026-09-10*

> A one-shot celebration burst, fired by hand or on mount.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must mark a real completion — a signup finished, a goal hit, a plan bought
- must fire it through the exposed handle, or arm `canAutoFire` on a landing
- should keep it rare; a burst on every save stops meaning anything

---

## Instead of

| Reach for | When |
|---|---|
| `Toast` | the app is confirming an ordinary action |
| [EmptyState](emptyState.md) | the screen is celebrating having nothing left to do |

---

## Values

- should leave `particleCount` at `60`, `lifetime` at `3000` ms
- should leave `gravity` at `1200`, `spread` at `60`, `velocity` at `500`
