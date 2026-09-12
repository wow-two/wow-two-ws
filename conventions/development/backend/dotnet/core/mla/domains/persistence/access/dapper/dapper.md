# Dapper

*Last updated: 2026-09-10*

> SQL access through a connection factory, with explicit naming and cancellation.

## Entities

- must declare [entity identity](../../entities/entity-contracts.md#identity) independently of the access provider.
- must implement `IHasTableName` when SQL uses the entity's table-name contract.
- must return the actual storage name from `TableName`.
- must verify that name against the [schema owner](../../persistence.md#contract).

---

## Connections

- must inject `IDbConnectionFactory`, not a raw connection or connection string.
- must open and dispose a fresh connection for each independent operation.
- must not cache or share an open connection between independent operations.
- must register `AddDataSourceConnectionFactory()` over a shared `DbDataSource`, or a custom factory for another provider.
- must keep transaction-sharing policy at the [unit-of-work boundary](../../../../constructs/patterns/unit-of-work.md).

```csharp
await using var connection = await connectionFactory.CreateOpenAsync(ct);
```

---

## Mapping

- must call `AddDapperConventions()` at startup for the process-wide underscore mapping and default type handlers.
- must register additional type handlers at startup, before queries run.
- must not change a global Dapper mapping per request.
- must configure `SqlNamingOptions` for the consuming repository and pass casing to `SqlNamingMapper` calls.
- must not treat mapper casing as mutable process-global state.

```csharp
var column = SqlNamingMapper.Col("EnrichedAt", naming.ColumnCase);
var aliased = SqlNamingMapper.Col("EnrichedAt", "l", naming.ColumnCase);
var parameter = SqlNamingMapper.ParRef("Limit", naming.ParameterCase);
```

- source and defaults → [Dapper registration](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/Dapper/DapperServiceCollectionExtensions.cs)
  and [SQL naming](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/Dapper/SqlNamingMapper.cs).

---

## Generic CRUD

- must use `IReadRepository<TEntity, TId>` or `IRepository<TEntity, TId>` for supported single-table operations.
- must satisfy the generic repository's `IKeyedEntity<TId>` and `IHasTableName` constraints.
- must use bespoke SQL when the operation exceeds the generic repository's contract.
- must exclude generated or immutable properties from insert/update lists through `ExcludedOnInsert` and `ExcludedOnUpdate`.
- must include the id among update exclusions when overriding that set.
- must register through `AddDapperRepository` in the owning persistence registration.
- current constraints, virtual methods and registration overloads → [repository source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/Dapper/Repositories/DapperRepository.cs).

---

## SQL

- must parameterize data values with an anonymous object or `DynamicParameters`.
- must pass `CommandDefinition(sql, parameters, cancellationToken: ct)` to each cancellable Dapper call.
- must use `SqlNamingMapper.Table<TEntity>()` for an entity-owned table name.
- may write fixed storage column names directly in a simple query.
- must use the naming mapper for generated identifiers, with the repository's explicit casing.
- must follow [raw-string style](../../../../../lla/notation/style/style.md).
- may extract shared SQL fragments when multiple queries must preserve the same predicate.
- must keep all values parameterized when composing those fragments.

```csharp
await using var connection = await connectionFactory.CreateOpenAsync(ct);
var rows = await connection.QueryAsync<TEntity>(
    new CommandDefinition(sql, parameters, cancellationToken: ct));
return rows.AsList();
```

---

## Enums

- must use driver mapping for native PostgreSQL enum columns → [Postgres mapping](../../database/postgres/postgres.md#enums).
- must register `AddEnumTypeHandler<TEnum>(style)` for string-backed enum columns.
- must keep stored labels reversible through `EnumNameMapper<TEnum>`.
- must not substitute `nameof(...).ToSnakeCase()` plus `Enum.Parse` for that reverse mapping.

---

## Queries

- must keep bespoke reads and writes in repositories.
- may split repository code into `Queries/` and `Commands/` when it grows.
- must not expose `IQueryable`, a specification framework or expression-tree query builder over Dapper.
- must compose database filtering in SQL.
