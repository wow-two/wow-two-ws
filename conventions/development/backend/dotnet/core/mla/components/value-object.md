# Value objects

*Last updated: 2026-09-12*

> Applying the [value-object construct](../constructs/data/value-object.md) to values with their own invariants.

## Location

- must use the construct's [location](../constructs/data/value-object.md#location).

---

## Declaration

- must use the construct's [declaration](../constructs/data/value-object.md#declaration).

---

## Content

- must choose a value object when equal identifying values mean the same thing.
- must choose an entity when identity persists while values change.
- must choose a DTO when the shape only carries data across a boundary.
- must not wrap one primitive with no additional rule.
- must keep validation of its values with its concept, normally in an external extension method or validator; the storing entity must not reimplement those rules.
- must expose operations over its own values without reaching a store, clock or injected collaborator.
- must leave existing instances unchanged when producing a changed value.
- must document each member's meaning, unit and permitted range.
- must keep row timestamps, keys, concurrency and audit stamps on the owning entity.

---

## Invariants

- must follow [validation placement](../domains/validation/validation.md#placement): construction, copying and deserialization produce candidates validated at the accepting boundary.
- must reserve constructor data checks for the documented exceptional contracts defined there.
- must not claim a constructor guard protects an independently assignable `init` member.
- must not claim `init` makes referenced collections deeply immutable.
- must retain the record/init declaration; external validation does not require get-only members or a constructor-only creation API.

---

## Equality

- must use compiler-generated equality where each identifying member already has the required equality semantics.
- must not assume an array or list compares by contents under record equality.
- must not claim a member is excluded from equality when its backing field still participates.
- may implement explicit typed equality and `GetHashCode` when generated equality does not express the value's meaning, including collection content comparison.
- must use the same participating values and element comparers for equality and hashing; equal values must produce equal hashes.
- must document whether collection order and duplicate items matter; use sequence semantics for ordered lists and set semantics only when the domain defines a set.
- must exclude a member only when it does not define the value, with that exclusion stated in the type's equality contract and applied consistently to hashing.
- must keep equality-participating data stable while used as a hash key or set element; `init` and deep copying do not make nested mutable collections immutable.
- must verify equal contents in separate instances, unequal contents, the declared order/duplicate behavior and matching hashes for equal values when supplying custom equality.

---

## Persistence

- must store the value inside its owning row as columns or a serialized column.
- must replace the stored value wholesale when it changes.
- EF mapping → [runtime mapping](../domains/persistence/access/ef/ef-mapping.md).
