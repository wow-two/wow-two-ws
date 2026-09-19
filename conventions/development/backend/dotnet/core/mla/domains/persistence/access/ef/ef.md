# Ef

*Last updated: 2026-09-10*

> Reaching the database through EF Core — the change tracker, the mapping, and code-first migrations.
> Schema authority follows the selected migration strategy.
> Use case — mapping an entity, or generating and applying a code-first migration.

## What lives here

- [entity configuration](entity-configuration.md) — `IEntityTypeConfiguration<T>` mapping and call order
- [ef migrations](../../migrations/ef/ef-migrations.md) — `AddEfMigrationsRunner<TContext>` and the code-first flow

---

## Boundary

- must keep EF types out of the Domain assembly — the entity stays provider-free.
- must not mix EF migrations with another strategy against one database.

---

## Tracked writes

- must use the single tracked entity instance for a load-modify-save operation; validate incoming changes, assign the accepted properties or invoke domain operations on that instance, and save the unit of work.
- must not pass a `with` copy, deep clone or manually copied class instance to `Update` or `Attach` as a replacement while the original with the same key is tracked.
- must not call `Update` merely to notify EF about ordinary detected changes on an already tracked entity; preserve its original values and property-level change tracking.
- must not silently merge a duplicate-key instance, detach the original or clear the tracker to make a replacement copy succeed.
- may use copies as detached candidates or snapshots under the [prototype contract](../../../../constructs/patterns/prototype.md); a candidate is not itself the tracked update target.
- must define any separate detached-update or explicit candidate-application operation in terms of allowed fields, relationships and original concurrency values; scalar `SetValues` is not a graph-merge contract.
- framework behavior → [EF identity resolution](https://learn.microsoft.com/en-us/ef/core/change-tracking/identity-resolution#query-then-apply-changes).
