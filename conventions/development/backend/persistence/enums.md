# Enums

*Last updated: 2026-06-16*

> Domain enums — where they live, how they're documented, named, modeled, and mapped to a database column.
> Purpose — keep enums co-located with their entities and round-trip them losslessly across providers via shared SDK converters.
> Use case — reach for it when adding or persisting a domain enum (a closed set of states / categories / kinds).

---

## Location

- `{Repo}.Domain/{Subdomain}/Enums/{Name}.cs` — **one file per enum** (per [code-organization.md](../code-style/code-organization.md)).
- Lives alongside its entities in the Domain assembly, under the owning subdomain folder.

---

## Documentation

- The `/// <summary>` is the top line of the file — write it first, then the declaration below.

### Enum-level

- `/// <summary>` starts with **Defines** — per [documentation.md](../code-style/documentation.md) starter table
- `/// <example>` describes when/where the enum is used (not the value list)

```csharp
/// <summary>Defines the category of a channel.</summary>
/// <example>Classifies channels as supply (scraping listings) or demand (capturing inquiries)</example>
public enum ChannelType { Supply, Demand }
```

### Value-level

- `/// <summary>` on each value describes what the value means
- `/// <example>` on each value gives a concrete usage example

```csharp
/// <summary>Defines the execution status of a pipeline run.</summary>
/// <example>running, completed, failed, cancelled</example>
public enum PipelineRunStatus
{
    /// <summary>Pipeline is currently executing.</summary>
    /// <example>ScrapeListings pipeline processing a batch of 50 URLs</example>
    Running,

    /// <summary>Pipeline finished successfully.</summary>
    /// <example>All 50 URLs scraped and persisted without errors</example>
    Completed,

    /// <summary>Pipeline terminated due to an error.</summary>
    /// <example>Database connection timeout during persist node</example>
    Failed,

    /// <summary>Manually stopped by user before completion.</summary>
    /// <example>User clicked Stop in pipeline dashboard mid-execution</example>
    Cancelled
}
```

---

## Naming

- **Singular** — no plural (`ChannelType` not `ChannelTypes`)
- **No `Enum` suffix** — `PipelineRunStatus` not `PipelineRunStatusEnum`
- **PascalCase values** — `Supply`, `Demand`, `ApartmentRent`

---

## Modeling

- **Backing type** — default `int`, no explicit values unless mapping to DB ordinals (rare; prefer PG enums)
- **No `[Flags]`** unless genuinely bitwise — most domain enums are not

---

## Database mapping

> **Standard:** native PostgreSQL enum types. Text columns are the fallback for non-PG providers (SqlServer / Sqlite) only — see *Text-column
> fallback*.

### Postgres (native enum types) — default

- **Storage** — PostgreSQL custom enum types (`CREATE TYPE listing_type AS ENUM (...)`).
- **C# ↔ PG case mapping** — PascalCase C# values map to snake_case PG labels (`ApartmentRent` ↔ `'apartment_rent'`).
- **Registration** — **one bulk call**, not per-enum, not per-property `.HasConversion()`. Call `MapEnums(CaseStyle.Snake, namespaceFilter,
  assemblies)` (`NpgsqlEnumMappingExtensions`) inside the `configure` delegate of `AddNpgsqlDataSource` (`PostgresServiceCollectionExtensions`).
- Npgsql requires enum mappings at the data-source (driver) level — `MapEnums` runs on the builder before `Build()`, scans the given assemblies, and
  registers every public non-nested enum that passes `namespaceFilter`.

```csharp
// Registration — once at startup
services.AddNpgsqlDataSource(builder =>
    builder.MapEnums(
        CaseStyle.Snake,
        ns => ns.StartsWith("Drydock.Domain"),
        typeof(ChannelType).Assembly));
```

**Why bulk, why a translator:**

- `MapEnums` derives the PG type name from the enum type name via `CaseConverter.ToCase(name, style)`.
- It routes both type and member names through a single `CaseStyleNameTranslator(style)` (an `INpgsqlNameTranslator`).
- Driver-level label mapping and any string-based mapping therefore agree *by construction* — they can't drift.
- No more listing each enum twice (`MapEnum<T>` on both `NpgsqlDataSourceBuilder` and `UseNpgsql`).
- **Per-enum PG type override** — pass the optional `pgTypeName` delegate to `MapEnums` (`Func<Type, string?>`; return `null` to keep the styled
  default).

---

### Text-column fallback (SqlServer / Sqlite)

- When the provider has no native enum types, store the enum as a **case-styled string** — reversibly, via the SDK converters.
- Never hand-roll `nameof(...).ToSnakeCase()` + `Enum.Parse`: that underscore-stripping pair is lossy on multi-word members. The SDK builds its
  reverse map from the enum's own members.
- **EF Core** — `EnumPropertyBuilderExtensions.HasEnumStringConversion<TEnum>()` (defaults `CaseStyle.Snake`):

```csharp
builder.Property(e => e.Status).HasEnumStringConversion();        // snake_case text column
```

- Applies `EnumCaseConverter<TEnum>` (a `ValueConverter<TEnum, string>`); reads are case-insensitive on the label, writes emit the configured style.
- **Dapper** — `DapperServiceCollectionExtensions.AddEnumTypeHandler<TEnum>()` (defaults `CaseStyle.Snake`):

```csharp
services.AddEnumTypeHandler<OrderStatus>();                       // registers EnumTypeHandler<OrderStatus>
```

- Both paths round-trip through `EnumNameConverter<TEnum>` (`ToLabel` / `Parse` / `TryParse`) — the single source of truth for label ↔ member,
  cached per `(enum, style)`.

> **Forward note:** a future text-enum-default mode (text as the standard, native PG opt-in) lands with the SQLite track. Until then, native PG
> enums are the standard and text columns are the non-PG fallback only.
