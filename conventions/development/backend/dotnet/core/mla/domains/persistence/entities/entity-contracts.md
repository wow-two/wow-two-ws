# Entity contracts

*Last updated: 2026-09-10*

> The interfaces a persisted type implements — identity, audit, soft-delete, tenancy and concurrency.
> Purpose — contracts live in a zero-ORM package, so the Domain assembly never references EF Core.
> Use case — shaping a new [entity](../../../constructs/data/entity.md), or wiring an interceptor that stamps one.

## Identity

`IEntity` is the umbrella — it says the type is a table shape, and says nothing about keys. Every concrete
type declares **which shape of key it has**, so a missing key reads as a choice rather than an oversight.

| Contract | For | Key |
|---|---|---|
| `IKeyedEntity<TId>` | the ordinary row | one column, exposed as `Id` |
| `ICompositeKeyEntity` | a join or link row | two or more columns, no single `Id` |
| `IKeylessEntity` | a view- or query-backed read shape | none |

- must implement `IKeyedEntity<TId>` for a row with one key column — `where TId : notnull, IEquatable<TId>`.
- must use `Guid` as the standard `TId`.
- must declare exactly one of the three on a concrete type — bare `IEntity` cannot say whether the key was
  chosen or forgotten, so it is the one shape a reviewer cannot check.
- must not implement `IEntity` directly; the three derive from it, and generic code constrains on it.
- must not wrap a composite key in a value-object `TId` to reach `IKeyedEntity<TId>` — the provider keys on
  the real columns, so the wrapper maps to nothing.
- all four live in the SDK's `Data.Abstractions`, provider-free by construction.

- must declare an entity-shaping rule here, never in a database, access or migration doc —
  [persistence](../persistence.md) § *The contract leads, the provider follows*.

---

## Members

- must be non-nullable unless the column is genuinely optional.
- must be `required` with `{ get; set; }` when persistence always returns the value.
- must drop `required` and initialize with `null!` when the value is not always loaded — relations, joined fields.
- must use `List<T>` for a collection.
- storage mapping → [database conventions](../database/database.md).

---

## Traits

Single-purpose interfaces, never base classes — an entity composes exactly the traits it has.

| Concern | Interface | Adds |
|---|---|---|
| creation timestamp | `ICreationAuditable` | `CreatedAt` |
| update timestamp | `IModificationAuditable` | `UpdatedAt` |
| both timestamps | `IAuditable` | the union of the two |
| creation actor | `ICreationAuditableBy<TUserId>` | `CreatedBy` |
| update actor | `IModificationAuditableBy<TUserId>` | `UpdatedBy` |
| both actors | `IAuditableBy<TUserId>` | the union of the two |
| soft delete | `ISoftDeletable` | `IsDeleted`, `DeletedAt` |
| soft-delete actor | `ISoftDeletableBy<TUserId>` | `DeletedBy` |
| tenant scope | `IHasTenant<TTenantId>` | `TenantId` |

- must take creation-only audit on an append-only type — a phantom `UpdatedAt` claims a lifecycle it has not got.
- must let the interceptor stamp creation once and pin it on update; `CreatedAt` never changes after insert.
- must use a struct as `TUserId` — the `*By<TUserId>` interfaces constrain it, and `Guid` is the standard.
- must implement a composite only when both halves apply.

---

## Concurrency

Optimistic-concurrency tokens are mutually exclusive — an entity implements at most one, matching its store.

| Store | Interface | Token |
|---|---|---|
| provider-agnostic | `IVersioned` | `Version` (`uint`) |
| Postgres | `IHasXmin` | `Xmin` (`uint`) |
| SQL Server | `IRowVersioned` | `RowVersion` (`byte[]`) |

- must not stack two tokens on one entity.


---

## Tenancy

- must take tenant scope from server-authoritative caller context, not an untrusted body field.
- must enforce tenant scope on reads and writes when a stored row is tenant-owned.
- must not infer isolation from implementing `IHasTenant<TTenantId>` alone.
- must keep authorization at the owning boundary → [identity](../../identity/identity.md#authorization).
