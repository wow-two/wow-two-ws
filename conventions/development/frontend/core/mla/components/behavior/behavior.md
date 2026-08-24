# Behavior components

*Last updated: 2026-08-23*

> Which seam or hook to reach for, and with what values.
> What each role **is** → [behavior constructs](../../constructs/behavior/behavior.md).
> One instance's full surface → its own source, beside the code.

## Return shape

- **Object return** for multiple values that cannot fail: `{ value, setValue, reset }`.
- **Tuple return** only for a simple state pair: `[value, setValue]`.
- a hook that can fail returns a [result](../data/data.md) instead, and the shape question does not arise.

---

## Effects

- must abort an in-flight fetch on unmount or dependency change with `AbortController`, ignoring `AbortError`.
- must keep one concern per effect — never fetch and subscribe in the same one.

---

## Neighbours

- [behavior constructs](../../constructs/behavior/behavior.md) — what each role is
- [components](../components.md) — the application register these sit in
