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
