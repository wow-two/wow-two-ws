# Data components

*Last updated: 2026-08-20*

> Which carrier or shape to reach for, and with what values.
> What each one **is** → [data constructs](../../constructs/data/data.md).

## Choosing a failure

`AppError` is a **returned value**, never a thrown one — it rides in a `Result`'s failure branch, and the caller
reads it off the type.

- must reach for `AppError` first; it carries a type, a message and metadata, which covers reporting and
  mapping to a status.
- must reach for `Result<T, TFailure>` only where the caller **switches** on which failure happened — a closed
  `{Noun}FailureCode` makes that switch checked.
- must not throw either one. A throw is reserved for a failed invariant, which is a bug rather than an outcome
  ([result](../../constructs/data/result.md)).

---

## Neighbours

- [data constructs](../../constructs/data/data.md) — what each carrier is
- [components](../components.md) — the application register these sit in
