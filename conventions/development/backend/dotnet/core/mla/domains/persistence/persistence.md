# Persistence

*Last updated: 2026-09-10*

> How a service stores and reads its own state, cut into the four things that swap independently.
> Purpose — an entity is not tied to an engine, an engine not to a mapper, neither to a migrator.
> Use case — adding a table, choosing how code reaches it, or changing the schema.

## Contract

- must take schema authority from the selected [migration strategy](migrations/migrations.md#strategy):
  applied scripts for SQL-owned schemas, model and generated migrations for EF-owned schemas.
- must keep the [entity](../../constructs/data/entity.md) free of any provider type.
- must express a schema change as a migration, never as a hand-edit against a live database.

---

## The four axes

| Axis | Answers | Lead |
|---|---|---|
| [entities](entities/entity-contracts.md) | what a persisted type implements | identity, audit, soft-delete, tenancy |
| [database](database/database.md) | which engine, and what it fixes | types, enum forms, column conventions |
| [access](access/access.md) | how code reaches a row | EF tracked, Dapper untracked |
| [migrations](migrations/migrations.md) | how the schema changes | `sql` · `dbup` · `ef` |

- must place a rule at the axis that owns it — a type mapping is the engine's, a configuration API is access's.
- must not assume one axis implies another; a Dapper service still needs an engine and a migrator.

---

## The contract leads, the provider follows

A key, an audit stamp and a soft-delete flag are properties of the **row**, not of Postgres, EF or Dapper.
The entity axis declares them once; every axis below reads that declaration and adds only its own mechanics.

- must declare an entity-shaping rule in [entity contracts](entities/entity-contracts.md), never in a
  database, access or migration doc.
- must keep a provider doc to its own mechanics — `HasNoKey()`, `HasKey(x => new { … })`, a column type,
  an index — each reading a contract already declared upstream.
- must not let an EF-first habit become the contract: another provider keys, stamps and soft-deletes the
  same rows, and the entity cannot tell which one is mapping it.
- must move a rule up when two providers restate it — a shared rule was never the provider's.

---

## Testing

- [test databases](testing/test-databases.md) — the tiers a test picks from, and what each resets.
