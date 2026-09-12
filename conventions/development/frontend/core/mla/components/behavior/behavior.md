# Behavior components

*Last updated: 2026-09-10*

> Which seam or hook to reach for, and with what values.
> What each role **is** → [behavior constructs](../../constructs/behavior/behavior.md).
> One instance's full surface → its own source, beside the code.

## Return shape

- must choose an object for named lifecycle state and operations.
- may choose a tuple for a simple state/setter pair whose position is unambiguous.
- must apply [hook outcomes and lifecycle](../../constructs/behavior/hooks.md#return-shape) to fallible work.

---

## Effects

- must abort an in-flight fetch on unmount or dependency change with `AbortController`, ignoring `AbortError`.
- must keep one concern per effect — never fetch and subscribe in the same one.

---

## Neighbours

- [behavior constructs](../../constructs/behavior/behavior.md) — what each role is
- [components](../components.md) — the application register these sit in
