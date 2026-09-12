# Ef mapping

*Last updated: 2026-09-10*

> EF runtime mapping under an explicitly selected schema-ownership strategy.

## Schema ownership

- must choose the [migration strategy](../../migrations/migrations.md#strategy) before configuring the model.
- must treat applied scripts as canonical under a SQL-owned strategy.
- must not call `EnsureCreated`, `Migrate` or generate EF migrations against that SQL-owned schema.
- must use [EF migration rules](../../migrations/ef/ef-migrations.md) when the EF model owns schema evolution.
- must retain DDL configuration needed by EF-generated migrations under that strategy.

---

## Context

- must derive product contexts from `AppDbContextBase`.
- must call `base.OnModelCreating(modelBuilder)` before additional model conventions.
- must put pre-convention customization in `ConfigureConventionsCore`, not override `ConfigureConventions`.
- must keep per-entity mapping in [entity configurations](entity-configuration.md).
- base behavior → [context source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/EntityFrameworkCore/AppDbContextBase.cs).

---

## Registration

- must use `AddEntityFrameworkCore<TContext>` or a composed SDK persistence registration.
- must configure the provider in its callback.
- must bind database configuration through `AddDatabaseSettings`.
- must share one `NpgsqlDataSource` between EF and Dapper when both access the same database.
- must choose pooling only when context state and dependencies are compatible with pooled lifetimes.
- must register SDK interceptors through their registration seams and verify they attach to the context.
- registration API → [context registration](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/EntityFrameworkCore/EntityFrameworkCoreServiceCollectionExtensions.cs).

---

## Runtime mapping

- must configure table names, keys, relationships, foreign keys, delete behavior and conversions where runtime mapping needs them.
- must configure `HasColumnName` when the schema name differs from the selected naming convention.
- must not repeat a convention-generated column name when no override is needed.
- must treat nullable-reference annotations as the default nullability mapping, with explicit overrides only where required.
- must not add index DDL metadata to a SQL-owned model solely to mirror scripts.
- must not expect `HasMaxLength` or `HasPrecision` to validate application inputs.
- must verify column type, nullability and conversion compatibility against the actual schema.
- must apply `UseSnakeCaseNamingConvention()` for a schema following the Postgres naming convention.

---

## JSON

- must pair `HasJsonConversion<T>()` with the provider's JSON storage type.
- must retain the associated `JsonValueComparer<T>` for snapshot/change tracking.
- must pin any non-default stored serializer options through `HasJsonConversion(options)`.
- stored JSON policy → [serialization](../../../../../../shapes/service/platform/responses/serialization.md).

```csharp
builder
    .Property(e => e.Metadata)
    .HasColumnType("jsonb")
    .HasJsonConversion();
```

---

## Enums

- must configure native enums at both the Npgsql driver and EF provider levels when using an external data source.
- must keep both registrations on the same CLR type, PostgreSQL type name and label translator.
- must not substitute a per-property string conversion for a native PostgreSQL enum.
- registration and fallback policy → [Postgres enums](../../database/postgres/postgres.md#enums).

---

## Traits

- must inherit identity, audit, soft-delete and concurrency choices from [entity contracts](../../entities/entity-contracts.md).
- must register audit and soft-delete interceptors through SDK registration.
- must not resolve a scoped current-user service into a singleton interceptor.
- must call `ApplyNpgsqlConventions()` or `ApplySqlServerConventions()` for the corresponding native concurrency token.
- must let the base apply provider-independent `IVersioned` conventions.
- current interceptor registration → [interceptor source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/EntityFrameworkCore/Interceptors/EfInterceptorServiceCollectionExtensions.cs).
