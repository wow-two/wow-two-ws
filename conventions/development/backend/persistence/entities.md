# Entities

*Last updated: 2026-06-22*

> Domain entities — plain `sealed record` types mapping 1:1 to database tables, living in the Domain assembly with zero ORM dependency.
> Purpose — keep the domain model EF-Core-free and consistent, so contracts (`IKeyedEntity<TId>`, traits) drive both EF interceptors and hand-written SQL.
> Use case — reach for these rules when adding or shaping any persisted type: its location, doc-comments, record shape, contract, and trait composition.

## Location

- `{Repo}.Domain/{Subdomain}/Entities/{Name}Entity.cs`
- Subdomain examples:
  - `Channels` → `ChannelEntity`, `ChannelSourceEntity`, `PipelineRun`, `NodeRun`
  - `Listings` → `ListingEntity`, `ListingImageEntity`, `LandmarkEntity`

---

## Documentation

The `/// <summary>` is the top line of the file — write it first, then the record declaration and members below. Follows the starter table in
[documentation.md](../code-style/documentation.md), with entity-specific conventions below.

### Entity-level

- `/// <summary>` starts with **Represents** + a human-readable description of what the entity holds

```csharp
/// <summary>Represents an external listing channel.</summary>
public sealed record ChannelEntity : IKeyedEntity<Guid> { }
```

### Member-level (regular properties)

- `/// <summary>` starts with **"Gets or sets the {property} of the {entity}"** — always state which entity the member belongs to, even if obvious

```csharp
/// <summary>Gets or sets the kebab-case slug of the channel, used as unique code reference.</summary>
public required string Slug { get; set; }
```

### Relations

- `/// <summary>` starts with **"Gets or sets"** + describes the relation, using the "collection of {entity}" convention

```csharp
/// <summary>Gets or sets the collection of search URLs that belong to this channel.</summary>
public List<ChannelSourceEntity> Sources { get; set; } = null!;
```

### Primary keys & foreign keys

- PK/FK properties (`Id`, `ListingId`, etc.) carry a `<summary>` like every other member.

```csharp
/// <summary>Gets or sets the unique identifier of the listing.</summary>
public required Guid Id { get; set; }

/// <summary>Gets or sets the ID of the parent channel.</summary>
public required Guid ChannelId { get; set; }
```

### Trait members

- Audit / soft-delete / tenant / concurrency members follow the same doc rules as the rest of the entity — `Gets or sets the …`.

---

## Modeling

### Record shape

- `sealed record` — see [models.md](../code-style/models.md)
- No positional constructors — body properties only
- Suffix with `Entity` when it maps to a DB table (`ChannelEntity` → `channels`); value objects (`PipelineRun`, `NodeRun`) skip the suffix
- Primary key: `Guid Id` — see [database.md](database.md) for the PK rules
- Implements `IKeyedEntity<Guid>` (from the SDK's `Data.Abstractions` package — adds `Id`)

### Members

- **Non-nullable by default** — no nullable types unless the column is genuinely optional
- **Always returned by persistence** — `required` with `{ get; set; }`
- **Not always returned** — no `required`, initialize with `null!` (relations, joined fields, EF-managed navigations)
- **Collections** — always `List<T>` (see [models.md](../code-style/models.md) for the three patterns)

#### Enum arrays

- A `List<TEnum>` mapped to a Postgres array uses a **PG enum array type** (e.g. `tenant_type[]`), not `TEXT[]` — preserves DB-layer type safety.

```csharp
// ✅ Correct — enum array, PG type is tenant_type[]
public required List<TenantType> AcceptedTenants { get; set; }

// ✅ Correct — free-form text array, PG type is TEXT[]
public required List<string> ApartmentAmenities { get; set; }
```

### Database mapping

- See [database.md](database.md) for type mappings, numeric units, and EF Core configuration rules
- See [enums.md](enums.md) for enum mapping

---

## Entity contract — `IKeyedEntity<TId>` vs `IEntity`

Contracts live in the zero-ORM-dependency `Data.Abstractions` package, so **Domain never references EF Core** — the EF Core interceptors (Audit,
SoftDelete) consume these same interfaces from the persistence layer.

- **`IKeyedEntity<out TId> : IEntity`** — the real contract; constrained `where TId : notnull, IEquatable<TId>`, exposes `TId Id { get; }` (get-only on the
  contract; entity records still declare `{ get; set; }`). Every persisted type implements it; `Guid` is the standard `TId`.
- **`IEntity`** — a bare marker (`public interface IEntity;`), the common base every trait extends. Reserve for keyless read-side shapes (projections,
  view-backed reads) with **no** primary key. A type that needs an `Id` uses `IKeyedEntity<TId>`, never bare `IEntity`.

### Dapper-targeted entities — `IHasTableName`

Entities read through hand-written SQL (Dapper `FROM`/`JOIN`) declare their table name on the type itself via **`IHasTableName.TableName`** — a
`static abstract string TableName { get; }`. It is the single source of truth for SQL and table-name resolution; give the name in **storage casing**
(snake_case for Postgres).

```csharp
public sealed record OrderLineItemEntity : IKeyedEntity<Guid>, IHasTableName
{
    public static string TableName => "order_line_items";
    public required Guid Id { get; set; }
    // …
}
```

---

## Trait stack

Behaviors are **single-purpose interfaces, never base classes** — an entity composes exactly the traits it needs, and each contract extends the bare
`IEntity` marker. The EF Core `AuditInterceptor` / `SoftDeleteInterceptor` stamp these fields automatically; see [database.md](database.md) for
interceptor wiring.

### Audit — split by lifecycle

Audit is **two independent halves** — pick the one(s) the entity actually has. Append-only / event-log types take **creation-only** (no phantom
`UpdatedAt`); only mutable rows get the modification half.

- Creation timestamp (write-once) → `ICreationAuditable` → `CreatedAt`
- Update timestamp → `IModificationAuditable` → `UpdatedAt`
- Both timestamps → `IAuditable` → composite of the two above
- Creation actor → `ICreationAuditableBy<TUserId>` → `CreatedBy`
- Update actor → `IModificationAuditableBy<TUserId>` → `UpdatedBy`
- Both actors → `IAuditableBy<TUserId>` → composite

Rules:

- **Write-once creation:** `AuditInterceptor` stamps `CreatedAt` / `CreatedBy` only on `Added`, then pins them on update
  (`entry.Property(nameof(ICreationAuditable.CreatedAt)).IsModified = false`) — they never change after insert. `UpdatedAt` / `UpdatedBy` re-stamp on every
  `Modified` save.
- **Actor type is a struct:** the `*By<TUserId>` interfaces constrain `where TUserId : struct`. The wired `IAuditCurrentUserAccessor.GetCurrentUserId()`
  returns `Guid?`, so `Guid` is the standard `TUserId`.
- **Composites are just unions** — `IAuditable : ICreationAuditable, IModificationAuditable` and
  `IAuditableBy<TUserId> : ICreationAuditableBy<TUserId>, IModificationAuditableBy<TUserId>`. Implement a composite only when both halves apply.

### Soft-delete

- Soft-delete → `ISoftDeletable` → `IsDeleted`, `DeletedAt`
- Soft-delete actor → `ISoftDeletableBy<TUserId>` → `DeletedBy` (`TUserId : struct`)

### Multi-tenancy

- Tenant scope → `IHasTenant<TTenantId>` → `TenantId`

### Concurrency — pick exactly ONE

Optimistic-concurrency tokens are **mutually exclusive** — an entity implements at most one, matching its provider. Don't stack them.

- Portable (provider-agnostic) → `IVersioned` → `Version` (`uint`)
- Postgres → `IHasXmin` → `Xmin` (`uint`)
- SqlServer → `IRowVersioned` → `RowVersion` (`byte[]`)

The SDK doc-comments cross-reference each other (`IHasXmin` ↔ `IRowVersioned`) precisely to flag the either/or — choose by the entity's backing store.
