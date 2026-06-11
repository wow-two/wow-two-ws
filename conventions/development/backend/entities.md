# Entities

*Last updated: 2026-02-23*

Domain entities are plain C# records that map 1:1 to database tables. They live in the Domain assembly under a subdomain folder.

## Location

`{Repo}.Domain/{Subdomain}/Entities/{Name}Entity.cs`

Example structure:

| Subdomain | Examples |
|---|---|
| `Channels` | `ChannelEntity`, `ChannelSourceEntity`, `PipelineRun`, `NodeRun` |
| `Listings` | `ListingEntity`, `ListingImageEntity`, `LandmarkEntity` |

## Modeling

### Record shape

- `sealed record` — see [models.md](models.md)
- No positional constructors — body properties only
- Naming: suffix with `Entity` when it maps to a DB table (`ChannelEntity` → `channels` table); value objects (`PipelineRun`, `NodeRun`) skip the suffix
- Primary key: `Guid Id` — see [database.md](database.md) for the PK rules
- Implements `IKeyedEntity<Guid>` (from the SDK's `Data.Abstractions` package — adds `Id`)

### Members

- **Non-nullable by default** — no nullable types unless the column is genuinely optional
- **Always returned by persistence** — `required` with `{ get; set; }`
- **Not always returned** — no `required`, initialize with `null!` (e.g. relations, joined fields, EF-managed navigations)
- **Collections** — always `List<T>` (see [models.md](models.md) for the three patterns)

#### Enum arrays

When a `List<TEnum>` maps to a Postgres array, use a **PG enum array type** (e.g., `tenant_type[]`), not `TEXT[]`. Preserves type safety at the DB layer.

```csharp
// ✅ Correct — enum array, PG type is tenant_type[]
public required List<TenantType> AcceptedTenants { get; set; }

// ✅ Correct — free-form text array, PG type is TEXT[]
public required List<string> ApartmentAmenities { get; set; }
```

### Database mapping

- See [database.md](database.md) for type mappings, numeric units, and EF Core configuration rules
- See [enums.md](enums.md) for enum mapping

## Documentation

Follows the starter table in [documentation.md](documentation.md), with entity-specific conventions:

### Entity-level

- `/// <summary>` starts with **Represents**
- `/// <example>` contains a human-readable description of what the entity holds

```csharp
/// <summary>Represents an external listing channel.</summary>
/// <example>OLX Uzbekistan supply channel with scraping sources and pipeline config</example>
public sealed record ChannelEntity : IKeyedEntity<Guid> { }
```

### Member-level (regular properties)

- `/// <summary>` starts with **"Gets or sets the {property} of the {entity}"** — always state what entity the member belongs to, even if obvious from context

```csharp
/// <summary>Gets or sets the kebab-case slug of the channel, used as unique code reference.</summary>
/// <example>olx-uz</example>
public required string Slug { get; set; }
```

### Relations

- `/// <summary>` starts with **"Gets or sets"** + describes the relation
- `<example>` uses the "Collection of {entity}" convention

```csharp
/// <summary>Gets or sets the search URLs that belong to this channel.</summary>
/// <example>Collection of channel sources</example>
public List<ChannelSourceEntity> Sources { get; set; } = null!;
```

### Primary keys & foreign keys

- **No `<example>` on PK/FK properties** — `Id`, `ListingId`, `OlxRawListingId`, etc. are self-explanatory UUIDs. Fake UUID examples (`a1b2c3d4-...`) add noise, not value. Use `<summary>` only.

```csharp
/// <summary>Gets or sets the unique identifier of the listing.</summary>
public required Guid Id { get; set; }

/// <summary>Gets or sets the ID of the parent channel.</summary>
public required Guid ChannelId { get; set; }
```

## Audit / soft-delete / tenant traits

When an entity opts into SDK behaviors (audit timestamps, soft-delete, multi-tenancy, concurrency), it implements the corresponding interface from `Data.Abstractions` — see the SDK's docs for the full list. Each opt-in adds the documented members:

| Trait | Interface | Members |
|---|---|---|
| Creation timestamp | `ICreationAuditable` | `CreatedAt` |
| Update timestamp | `IModificationAuditable` | `UpdatedAt` |
| Both timestamps | `IAuditable` | (composite) |
| Creation user | `ICreationAuditableBy<TUserId>` | `CreatedBy` |
| Update user | `IModificationAuditableBy<TUserId>` | `UpdatedBy` |
| Both users | `IAuditableBy<TUserId>` | (composite) |
| Soft-delete | `ISoftDeletable` | `IsDeleted`, `DeletedAt` |
| Soft-delete user | `ISoftDeletableBy<TUserId>` | `DeletedBy` |
| Multi-tenancy | `IHasTenant<TTenantId>` | `TenantId` |
| Concurrency (SqlServer) | `IRowVersioned` | `RowVersion` |
| Concurrency (Postgres) | `IHasXmin` | `Xmin` |
| Concurrency (portable) | `IVersioned` | `Version` |

These members follow the same doc rules as the rest of the entity — `Gets or sets the …`.

## See also

- [database.md](database.md) — DB mapping, EF Core configurations
- [enums.md](enums.md) — enum modeling
- [models.md](models.md) — general record / member rules
- [documentation.md](documentation.md) — XML doc + starter table
