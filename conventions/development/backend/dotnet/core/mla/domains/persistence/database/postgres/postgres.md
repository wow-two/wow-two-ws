# Postgres

*Last updated: 2026-10-28*

> PostgreSQL names, column types and stored values; access APIs belong to their provider.
> Point ids cite the [migrations analysis](../../../../../../../../../../ideas/migrations-analysis-2026-10/migrations-analysis-2026-10.md).

## Version

- must run the newest stable PostgreSQL major everywhere — 18 today: hosts, compose files, CI services, test
  containers (owner 2026-10-28).
- must take a new major once it is generally available, never a beta or release candidate.
- must name the image by its major (`postgres:18-alpine`), never `latest`: a major jump cannot open the old data
  directory, so a major upgrade is a planned dump and restore.

---

## Schema

- must verify names and types against the [schema owner](../../persistence.md#contract) before editing models or queries.
- must read the data dictionary and mapping reference when the repository maintains them.
- must make a column `NOT NULL` unless the domain value is genuinely optional.
- must supply values explicitly rather than adding defaults that hide missing inputs.
- key shape → [entity identity](../../entities/entity-contracts.md#identity).

---

## Naming

- must name tables, columns, constraints and stored values in unquoted snake_case (M64).
- must name an instant `*_at`, a date `*_on`, a time of day `*_time` (M67, M68, M69).
- must name a measured elapsed time `*_ms` (M70).
- must keep a package-owned date column's name as the package ships it (M68).

---

## Types

| Value | Column | .NET | Point |
|---|---|---|---|
| key | `uuid` v7 | `Guid` | M65 |
| instant | `timestamptz`, UTC | `DateTimeOffset` at offset zero | M67 |
| calendar date | `date` | `DateOnly` | M68 |
| time of day | `time` | `TimeOnly` | M69 |
| span SQL computes with | `interval` | `TimeSpan` | M70 |
| measured elapsed time | `bigint` milliseconds | `long` | M70 |
| money | `bigint` minor or micro units | `long` | M72 |
| exact ratio, such as an exchange rate | `numeric(p,s)` | `decimal` | M72 |
| measurement | `double precision` | `double` | M72 |
| string with a sensible domain limit | `varchar(n)` | `string` | M73 |
| free-form body | `text` | `string` | M73 |
| document | `jsonb` | the mapped type | M66 |
| flag · binary | `boolean` · `bytea` | `bool` · `byte[]` | — |

- must store each value in the column its row names.
- must make keys in the application (`Guid.CreateVersion7()`), with no database default (M65).
- must take v7 from PostgreSQL's built-in `uuidv7()` for rows SQL inserts itself; no extension or own function (M65).
- must keep a public token (a share link, a short code) a separate random value; v7 reveals its time (M65).
- may key only claim rows and append-only logs by `bigint GENERATED … AS IDENTITY` (M65).
- must key a singleton row `integer CHECK (id = 1)` (M65).
- must give a time of day that belongs to a place an IANA zone column; never `timetz` (M69).
- may store a zoneless `timestamp` only for a declared local wall-clock value beside its zone (M69).
- must name money's currency in a column or in the column's name (M72).
- must use `json` only for a document whose exact text is the value (M66).
- must write stored JSON from SQL with camelCase keys and ISO-8601 durations (M66) → [stored JSON](../../stored-json.md).
- must use a native enum array for a list of native enum values.
- must use `text[]` for a list of unconstrained strings.
- must verify the provider supports the chosen element type before using another array shape.
- which type changes are expands → [compatibility](../../migrations/migrations.md#compatibility).

---

## Text matching

- must enforce case-insensitive uniqueness by a unique index on `lower(…)` (M73).
- may add a normalized column only where a library reads one (M73).
- must not use `citext` (M73).

---

## Numeric units

- must store bounded quantities as integers in a documented unit under the current integer-storage policy.
- must select integer width from the full allowed range, not from sample values.
- must state currency and scale for monetary amounts; whole currency is valid only when fractional units are excluded.
- must use checked conversion and an explicit rounding rule when converting into the stored unit.
- must not assume a fixed-width integer covers an arbitrary precision or unbounded range.

---

## Audit and soft delete

- must leave `created_at` and `updated_at` to the interceptor; the database adds only `DEFAULT now()` on
  `created_at`, for rows SQL inserts (M74).
- must not add an `updated_at` trigger (M74).
- must store soft delete as `deleted_at timestamptz NULL` alone (M75).
- must scope a unique index on a soft-deleted table `WHERE deleted_at IS NULL` (M75).
- traits → [entity contracts](../../entities/entity-contracts.md#traits).

---

## Enums

- must use a native PostgreSQL enum for every new enum column (M71).
- must convert an existing text enum to a native one when its product next changes that enum (M71).
- must use snake_case labels for PascalCase CLR members.
- must use styled text for providers without native enum types, except a documented existing-schema compatibility mapping.
- must keep type names and label translation identical in every access path.
- must register driver mappings before building the data source.
- must also register mappings on the EF provider when EF consumes an external data source.
- must not infer EF mapping from driver registration alone.
- may use `MapEnums` for driver-level discovery; its `assemblies` argument follows `pgTypeName`.

```csharp
services.AddNpgsqlDataSource(dataSource => dataSource.MapEnums(
    CaseStyle.Snake,
    ns => ns.StartsWith("Wheelhouse.Domain", StringComparison.Ordinal),
    assemblies: typeof(ChannelType).Assembly));
```

- must configure EF with the corresponding `MapEnum` call and the same translator:

```csharp
builder.UseNpgsqlConventional(dataSource, npgsql => npgsql.MapEnum<ChannelType>(
    "channel_type",
    nameTranslator: new CaseStyleNameTranslator(CaseStyle.Snake)));
```

- EF/driver requirements → [Npgsql enum mapping](https://www.npgsql.org/efcore/mapping/enum.html).
- current driver helper → [enum mapping source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src/Data/EntityFrameworkCore/Postgres/NpgsqlEnumMappingExtensions.cs).
- string-backed mapping APIs → [Dapper enums](../../access/dapper/dapper.md#enums).
- SQL enum evolution → [migration dialects](../../migrations/sql/migration-dialects.md#native-enum-changes).
