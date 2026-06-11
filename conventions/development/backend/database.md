# Database

*Last updated: 2026-02-23*

Schema-first development rule + column constraints + EF Core entity type configurations.

## Schema-first rule

**Before writing any code that touches database tables (models, migrations, queries):**

1. Read the canonical schema file for the repo (`src/database/db-setup.md` for Haven; `migrations/*.sql` for SDK consumers) — actual `CREATE TABLE` statements, column names, types, constraints
2. Read the data dictionary if one exists — field reference, allowed values, who sets each column
3. Cross-check the DB ↔ C# mapping doc if one exists — column ↔ property mapping, known pitfalls

Never assume column names or types — always verify against the schema files first.

Applies to: C# models, SQL migrations, Dapper queries, EF Core configurations, filter logic.

## Column constraints

**NOT NULL without DEFAULT** for all new columns unless there's a valid reason for a default.

Valid reasons for `DEFAULT`:
- Primary keys (`DEFAULT gen_random_uuid()` — but see PK note below)
- Timestamps (`DEFAULT NOW()`) — unless the value must be provided by code (precision, exact calculated time)
- Trigger-created rows

Everything else — booleans, enums, arrays, strings — must be set explicitly from code. Defaults mask missing values and introduce silent bugs when pipelines evolve.

## Primary keys

- **`Guid` for `Id`** unless there's a valid reason (slug-based PK, composite PK)
- **EF Core generates client-side via `Guid.NewGuid()`** — do NOT add `DEFAULT gen_random_uuid()` on ID columns. DB defaults never fire since EF always provides the value
- All entities implement `IEntity` (`Guid Id` member) — see SDK's `Data.Abstractions` package

## Type mappings (Postgres / Npgsql)

| C# | Postgres | Notes |
|---|---|---|
| `Guid` | `uuid` | EF Core generates client-side |
| `DateTime` / `DateTimeOffset` | `timestamptz` | Always use `timestamptz`, never `timestamp` |
| `DateOnly` | `date` | Needs Dapper handler for raw queries — see [data-access.md](data-access.md) |
| `string` | `text` or `varchar(n)` | Prefer `text`; use `varchar(n)` only when a hard limit is meaningful |
| `bool` | `boolean` | |
| `List<TEnum>` (PG enum array) | `tenant_type[]` | Use PG enum array type, not `TEXT[]` |
| `List<string>` (free-form) | `TEXT[]` | For AI output, URLs, tags, unstructured text |
| `byte[]` | `bytea` | |
| `List<T>` (single-table cols) | array type | EF Core handles native Npgsql array mapping |

## Numeric type conventions

Avoid `NUMERIC`/`DECIMAL` — store values as integers in the smallest meaningful unit.

| Data kind | DB type | C# type | Unit | Example |
|---|---|---|---|---|
| Percentages / confidence | `SMALLINT` + `CHECK (col BETWEEN 0 AND 100)` | `short` | 0–100 whole percent | `85` = 85% |
| Money (large amounts) | `BIGINT` | `long` | Raw whole amount in original currency | `3840000000` = 3.84B UZS |
| Money (micro-amounts, API costs) | `INTEGER` | `int` | Micro-USD (×1,000,000) | `123` = $0.000123 |
| Area | `INTEGER` | `int` | Square centimeters (cm²) | `750000` = 75.00 m² |
| Height / length | `SMALLINT` | `short` | Centimeters | `280` = 2.80 m |
| Counts / ordinals | `SMALLINT` | `short` | Natural unit | `3` = 3 rooms |

No `NUMERIC`/`DECIMAL` anywhere — integer storage in the appropriate unit covers all cases. This means no `.HasPrecision()` needed in EF Core configs.

## EF Core entity type configurations

### Location

`{Repo}.Persistence/Configurations/{Name}Configuration.cs`

One `IEntityTypeConfiguration<T>` per entity. Multiple configurations can share a file when entities are tightly coupled (e.g. `ChannelEntityConfiguration` + `ChannelSourceEntityConfiguration`) — but the file-per-type rule in [code-organization.md](code-organization.md) still says **split by default**, only merge for very tight coupling.

### What to configure (runtime effect)

| Pattern | Why it's needed |
|---|---|
| `.ToTable()` | EF must know which table to query |
| `.HasKey()` | Change tracking, identity resolution, LINQ-to-SQL key comparisons |
| `.HasOne()` / `.HasMany()` | Navigation properties — `.Include()`, in-memory cascade |
| `.HasForeignKey()` | Tells EF which property is the FK for the relationship |
| `.OnDelete()` | EF in-memory cascade behavior |
| `.HasConversion()` | Value conversion at read/write time (rarely needed — PG enums handled globally) |
| `.HasColumnType("jsonb")` | Npgsql needs this to serialize JSONB columns correctly |
| `.Ignore()` | Excludes computed or non-persisted properties from mapping |

### What NOT to configure (migration-only = dead code in schema-first repos)

| Pattern | Why it's waste |
|---|---|
| `.IsRequired()` | NRT already tells EF nullability — `string` = required, `string?` = optional. Redundant |
| `.HasMaxLength()` | EF does not validate string length at runtime; DB enforces |
| `.HasColumnName()` | Redundant when `UseSnakeCaseNamingConvention()` is on |
| `.HasIndex()` | Migration-only; index lives in the schema file |
| `.HasFilter()` | Partial index predicate — migration-only |
| `.HasDatabaseName()` | Custom index name — migration-only |
| `.HasPrecision()` | Not needed when numeric columns use integer types |

> **Note:** if you're NOT schema-first and EF generates migrations, all of these are valid. The "waste" rule only applies when migrations are produced out-of-band.

### Enum mapping (Postgres)

Do NOT use `.HasConversion()` per property — register enums globally via `MapEnum<T>()` inside `UseNpgsql()` and `NpgsqlDataSourceBuilder` (handles C# ↔ PG enum type mapping at the Npgsql provider level).

### Section order inside a configuration

Organize in this order, separated by lightweight comment headers (see [code-organization.md](code-organization.md)):

1. **Table + Key** — `.ToTable()`, `.HasKey()`
2. **Column type overrides** — `.HasColumnType("jsonb")` etc.
3. **Conversions** — `.HasConversion()` for the rare cases
4. **Relationships** — `.HasOne()`, `.HasMany()`, `.HasForeignKey()`, `.OnDelete()`

### Chaining

Always chain on new lines, even for a single method call:

```csharp
builder
    .ToTable(ListingEntity.TableName);

builder
    .HasKey(e => e.Id);

// ── Relationships ──

builder
    .HasOne(e => e.OlxRawListing)
    .WithOne(e => e.Listing)
    .HasForeignKey<ListingEntity>(e => e.OlxRawListingId);

builder
    .HasMany(e => e.Images)
    .WithOne(e => e.Listing)
    .HasForeignKey(e => e.ListingId)
    .OnDelete(DeleteBehavior.Cascade);
```

### Documentation

Single `/// <summary>` one-liner starting with **"Configures"** — per [documentation.md](documentation.md) starter table. No `<remarks>` or `<example>`.

```csharp
/// <summary>Configures the listings table mapping and relationships.</summary>
public class ListingEntityConfiguration : IEntityTypeConfiguration<ListingEntity> { }
```

## See also

- [entities.md](entities.md) — entity modeling, members, navigation properties
- [enums.md](enums.md) — PG enum registration
- [data-access.md](data-access.md) — Dapper conventions for raw SQL paths
- [code-organization.md](code-organization.md) — file-per-type rule
