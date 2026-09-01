# Value objects

*Last updated: 2026-08-24*

> The type an entity stores whole, identified by its values rather than by a key.
> Purpose — a concept with rules of its own stops being loose columns on the entity that holds it.
> Use case — an amount, an address, a routing rule; anything meaningless apart from its values.

> Defined at [value objects — the construct](../constructs/data/value-object.md); this doc carries every condition for using one.

## Reaching for one

- must reach here when two instances carrying equal values are the same thing — no key distinguishes them.
- must reach for an [entity](../constructs/data/entity.md) instead when the thing has a lifetime: it is
  created, changed and referred to by identity across time.
- must reach for a [DTO](../constructs/data/dto.md) instead when the shape exists to cross a boundary and
  carries no rule of its own.
- must not introduce one for a single primitive with no rule — a `string Name` stays a `string`.

---

## What it owns

- must own every rule that makes its values valid together, so an invalid instance cannot be constructed.
- must validate in the factory or the constructor, never in the entity that stores it.
- must expose behaviour over its own values — a money type adds and compares, it is not read apart and
  recombined by callers.
- must not reach a store, a clock or any injected collaborator; its whole contract is its values.

---

## Members

- must be immutable — `init` accessors, no setter, no mutating method.
- must return a new instance from any operation that changes a value, never mutate in place.
- must carry a `<summary>` on each member stating what the value means, plus its unit where one exists.
- must state the allowed range or set when a value is bounded, so the constructor's guard has a stated reason.
- must not carry a member the entity owns instead — a timestamp of when the row changed belongs to the row.

---

## Equality

- must let the `record` compiler-generated equality stand, which compares every member.
- must exclude a member from equality only when it genuinely does not identify the value, and say why in
  one line on the member.
- must not implement `Equals` or `GetHashCode` by hand on a `record`.

---

## Persistence

- must be stored inside the owning entity's row, as owned columns or a serialized column, never as its own
  table → [ef-mapping](../domains/persistence/access/ef/ef-mapping.md).
- must not carry a key, a row version, or an audit stamp — those belong to the entity that owns it.
- must be replaced wholesale when it changes, so the owning entity assigns a new instance.

---

## Neighbours

- [value objects — the construct](../constructs/data/value-object.md) — what it is and how it is declared
- [entity](../constructs/data/entity.md) — the type that owns a row and stores this one inside it
- [ef-mapping](../domains/persistence/access/ef/ef-mapping.md) — how an owned type reaches columns
