# Postgres

*Last updated: 2026-09-10*

> PostgreSQL column and stored-value conventions; access APIs belong to their provider.

## Schema

- must verify names and types against the [schema owner](../../persistence.md#contract) before editing models or queries.
- must read the data dictionary and mapping reference when the repository maintains them.
- must make a column `NOT NULL` unless the domain value is genuinely optional.
- must supply values explicitly rather than adding defaults that hide missing inputs.
- may use defaults for timestamps or trigger-created rows when the database owns those values.
- must not add a redundant database UUID default when the application owns key generation.
- key shape → [entity identity](../../entities/entity-contracts.md#identity).

---

## Types

- must store `Guid` as `uuid`.
- must store instants as `timestamptz`, using UTC values supported by Npgsql.
- must store calendar dates as `date` and model them as `DateOnly`.
- must prefer `text`; use `varchar(n)` only for a meaningful storage limit.
- must store booleans as `boolean` and binary values as `bytea`.
- must use a native enum array for a list of native enum values.
- must use `text[]` for a list of unconstrained strings.
- must verify the provider supports the chosen element type before using another array shape.

---

## Numeric units

- must store bounded quantities as integers in a documented unit under the current integer-storage policy.
- must select integer width from the full allowed range, not from sample values.
- must state currency and scale for monetary amounts; whole currency is valid only when fractional units are excluded.
- must use checked conversion and an explicit rounding rule when converting into the stored unit.
- must not assume a fixed-width integer covers an arbitrary precision or unbounded range.
- must not introduce `NUMERIC` / `DECIMAL` under the current default without an explicit scoped convention decision.

---

## Enums

- must use native PostgreSQL enums under the current PostgreSQL default.
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
    ns => ns.StartsWith("Drydock.Domain", StringComparison.Ordinal),
    assemblies: typeof(ChannelType).Assembly));
```

- must configure EF with the corresponding `MapEnum` call and the same translator:

```csharp
builder.UseNpgsqlConventional(dataSource, npgsql => npgsql.MapEnum<ChannelType>(
    "channel_type",
    nameTranslator: new CaseStyleNameTranslator(CaseStyle.Snake)));
```

- EF/driver requirements → [Npgsql enum mapping](https://www.npgsql.org/efcore/mapping/enum.html).
- current driver helper → [enum mapping source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/EntityFrameworkCore/Postgres/NpgsqlEnumMappingExtensions.cs).
- string-backed mapping APIs → [Dapper enums](../../access/dapper/dapper.md#enums).
- SQL enum evolution → [migration dialects](../../migrations/sql/migration-dialects.md#native-enum-changes).
