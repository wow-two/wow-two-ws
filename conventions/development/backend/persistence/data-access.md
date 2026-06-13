# Data access (Dapper)

*Last updated: 2026-06-13*

Dapper query and command classes for direct SQL access, shared across services via a common Persistence assembly. Generic CRUD is delegated to the SDK's `DapperRepository<TEntity, TId>`; hand-written SQL covers everything else. No `IQueryable` / Specification layer — see [§No query abstraction](#no-query-abstraction).

## Location

| Folder | Purpose | Examples |
|---|---|---|
| `{Repo}.Persistence/Queries/` | Read operations | `UnclassifiedListingsQuery`, `UnenrichedListingsQuery` |
| `{Repo}.Persistence/Commands/` | Write operations | `SupplySourceUrlCommands` |
| `{Repo}.Persistence/Repositories/` | Generic-CRUD subclasses | `OlxListingsRepository : DapperRepository<…>` |

One file per query/command type (per [code-organization.md](../code-style/code-organization.md)).

## Connections

> **Inject `IDbConnectionFactory` — never a raw `DbConnection` or connection string.** It is the single connection-factory abstraction across the repo, and it isolates the connection-string lookup to one place (`Data.Dapper.IDbConnectionFactory`).

- **Open one fresh connection per operation** via `await using var conn = await connectionFactory.CreateOpenAsync(ct);` at the start of each method. The factory hands back an already-opened `DbConnection`; do not cache, reuse, or share a connection across operations.
- `IDbConnectionFactory` also exposes `Create()` (returns a *closed* connection — caller opens + disposes); prefer `CreateOpenAsync(ct)` in app code.

### Registration

Register the factory **once** at startup (`Data.Dapper.DapperServiceCollectionExtensions`). Pick one:

| Helper | Backing | Use when |
|---|---|---|
| `AddDataSourceConnectionFactory()` | A registered `DbDataSource` (e.g. `NpgsqlDataSource`) → `DataSourceConnectionFactory` (singleton) | Default. Pooling, enum mapping, etc. configured on the data source. |
| `AddDbConnectionFactory<TFactory>()` | A custom `IDbConnectionFactory` you supply (singleton) | Provider without a `DbDataSource`, or bespoke connection construction. |

```csharp
services.AddNpgsqlDataSource(connectionString); // registers a DbDataSource
services.AddDataSourceConnectionFactory();       // → IDbConnectionFactory
services.AddDapperConventions();                 // global mappings + handlers (idempotent)
```

## Conventions (global, once)

`AddDapperConventions()` is **idempotent** (guarded by `Interlocked.Exchange`) and wires the process-wide Dapper conventions:

- snake_case column → PascalCase property mapping (`DefaultTypeMap.MatchNamesWithUnderscores = true`)
- `DateOnlyTypeHandler` — `DATE` ↔ `DateOnly`
- `ListTypeHandler<string>` — `TEXT[]` ↔ `List<string>`

Call it once at startup (or rely on `AddDapperRepository<…>` / `AddDataSourceConnectionFactory` paths that call it for you). Additional list handlers register at startup via `SqlMapper.AddTypeHandler`:

```csharp
SqlMapper.AddTypeHandler(new ListTypeHandler<int>());
SqlMapper.AddTypeHandler(new ListTypeHandler<Guid>());
```

> Enum-as-text columns: use `AddEnumTypeHandler<TEnum>(CaseStyle.Snake)` (registers `EnumTypeHandler<TEnum>`) — see [Enum-as-text columns](#enum-as-text-columns) and [enums.md](enums.md).

## Generic CRUD — `DapperRepository<TEntity, TId>`

For straightforward single-table read/CRUD, depend on the SDK's `IRepository<TEntity, TId>` (read+write) or `IReadRepository<TEntity, TId>` (read-only) and let `DapperRepository<TEntity, TId>` generate the SQL — don't hand-roll `SELECT */INSERT/UPDATE/DELETE`.

### Entity requirements

`TEntity` must declare **both** `IKeyedEntity<TId>` (exposes `Id`) **and** `IHasTableName` (static abstract `TableName`); `TId` must be `notnull, IEquatable<TId>`.

```csharp
public sealed class OlxListingEntity : IKeyedEntity<Guid>, IHasTableName
{
    public static string TableName => "olx_listings";   // storage casing (snake_case)
    public Guid Id { get; init; }
    public string Title { get; set; } = "";
    public DateTimeOffset? EnrichedAt { get; set; }
}
```

The column set is **every public instance property with a getter *and* setter**, mapped via `SqlNaming.ColumnCase`. The id column is `nameof(IKeyedEntity<TId>.Id)`.

### Store-generated columns

Override the protected `ExcludedOnInsert` / `ExcludedOnUpdate` to omit identity / computed / store-generated columns. Defaults: `ExcludedOnInsert` = none; `ExcludedOnUpdate` = `Id`.

```csharp
public sealed class OlxListingsRepository(IDbConnectionFactory connectionFactory)
    : DapperRepository<OlxListingEntity, Guid>(connectionFactory)
{
    // DB fills these via DEFAULT / trigger — never in the INSERT/UPDATE column list
    protected override IReadOnlyCollection<string> ExcludedOnInsert => [nameof(OlxListingEntity.CreatedAt)];
    protected override IReadOnlyCollection<string> ExcludedOnUpdate => [nameof(OlxListingEntity.Id), nameof(OlxListingEntity.CreatedAt)];
}
```

All members are `virtual` — override `GetByIdAsync`, `CreateAsync`, etc. for bespoke SQL while inheriting the rest.

### Registration

`AddDapperRepository` (in `Data.Dapper.Repositories`) registers the implementation under **both** `IRepository<,>` and `IReadRepository<,>` and calls `AddDapperConventions()` for you (Scoped by default):

```csharp
services.AddDapperRepository<OlxListingEntity, Guid>();                          // generic repo
services.AddDapperRepository<OlxListingsRepository, OlxListingEntity, Guid>();   // concrete subclass (custom queries / excluded cols)
```

## SQL conventions

For hand-written queries and commands.

- **Table references** — `SqlNaming.Table<TEntity>()` (or `SqlNaming.Table<TEntity>("o")` for an aliased reference). Requires `TEntity : IHasTableName`. Define a class-level constant: `private static readonly string Table = SqlNaming.Table<OlxListingEntity>();`.
- **Column names** — `SqlNaming.Col("EnrichedAt")` → `enriched_at` (default `CaseStyle.Snake`); aliased `SqlNaming.Col("EnrichedAt", "l")` → `l.enriched_at`; strongly-typed `SqlNaming.Col<OlxListingEntity>(x => x.EnrichedAt)`. Hard-coded snake_case is fine for simple single-table queries; use `SqlNaming.Col` when building dynamic WHERE clauses or aliased joins.
- **Parameters** — `SqlNaming.ParRef("Limit")` → `@limit` (placeholder, default `CaseStyle.Camel`); `SqlNaming.Par("Limit")` → bare `limit` (for `DynamicParameters.Add`). Strongly-typed `SqlNaming.ParRef<OlxListingEntity>(x => x.Id)`. Pass values via an anonymous object or `DynamicParameters`.
- **Casing is global** — defaults are columns `Snake`, params `Camel`. Override **once at startup** via `SqlNaming.ColumnCase` / `SqlNaming.ParameterCase` if a schema differs; never per-call.
- **Raw strings** — follow [code-organization.md](../code-style/code-organization.md) raw-string rules (opening `"""` on its own line).
- **Wrap every call** in `new CommandDefinition(sql, parameters, cancellationToken: ct)` — never `QueryAsync(sql, parameters)` without it (loses the CT).

```csharp
public sealed class UnenrichedListingsQuery(IDbConnectionFactory connectionFactory)
{
    private static readonly string Table = SqlNaming.Table<OlxListingEntity>();

    public async Task<int> GetCountAsync(CancellationToken ct = default)
    {
        await using var conn = await connectionFactory.CreateOpenAsync(ct);

        var sql =
            $"""
             SELECT COUNT(*)::INTEGER
             FROM {Table}
             WHERE enriched_at IS NULL
             """;

        return await conn.ExecuteScalarAsync<int>(
            new CommandDefinition(sql, cancellationToken: ct));
    }
}
```

> **Stale-helper fix:** earlier drafts referenced `Tab<T>()` / `Col()`. Those names do not exist — the helpers are static members on `SqlNaming`: `SqlNaming.Table<T>` / `SqlNaming.Col` / `SqlNaming.Col<T>` / `SqlNaming.Par` / `SqlNaming.ParRef`. `Table<T>` requires `IHasTableName`.

### DI registration (query/command classes)

Scoped lifetime (shares request-scoped connection state). Register in the persistence registration extension.

## Reusable SQL fragments

For queries with shared WHERE logic across count + batch methods, extract into a `static readonly string`:

```csharp
private static readonly string WhereClause =
    $"""
     FROM {Table} rl
     WHERE rl.enriched_at IS NOT NULL
       AND NOT EXISTS (...)
     """;

public Task<int> GetCountAsync(CancellationToken ct) =>
    conn.ExecuteScalarAsync<int>($"SELECT COUNT(*)::INTEGER {WhereClause}");

public Task<List<T>> GetBatchAsync(CancellationToken ct) =>
    conn.QueryAsync<T>($"""
     SELECT rl.id, rl.title, ...
     {WhereClause}
     ORDER BY rl.scraped_at ASC
     LIMIT @limit
     """);
```

> **Note:** `const string` cannot use string interpolation — use `static readonly string` when fragments reference `SqlNaming.Table<T>()` / `SqlNaming.Col(...)` helpers.

## Type handlers

`AddDapperConventions()` registers the default handlers (see [Conventions](#conventions-global-once)):
- `DateOnlyTypeHandler` — `DATE` ↔ `DateOnly`
- `ListTypeHandler<string>` — `TEXT[]` ↔ `List<string>`
- snake_case → PascalCase property mapping

Additional list handlers (`List<int>`, `List<Guid>`) → register at startup via `SqlMapper.AddTypeHandler(new ListTypeHandler<int>())`.

### Enum-as-text columns

When a column stores an enum as text (the portable default), register a string-backed handler once at startup:

```csharp
services.AddEnumTypeHandler<OrderStatus>();              // default CaseStyle.Snake → "in_progress"
services.AddEnumTypeHandler<OrderStatus>(CaseStyle.Camel);
```

`AddEnumTypeHandler<TEnum>` (constraint `TEnum : struct, Enum`) registers `EnumTypeHandler<TEnum>`: writes emit the chosen `CaseStyle`, reads are case-insensitive. For Postgres **native** enum types, use Npgsql's driver-level `MapEnum` instead — see [enums.md](enums.md).

## No query abstraction

No `IQueryable`, no Specification pattern, no expression-tree query builder. Reads are either generic-CRUD methods on `IReadRepository<,>` (`GetByIdAsync`, `GetAllAsync`, `ExistsAsync`, `CountAsync`) or hand-written SQL in a `Query`/`Queries` class. Compose filtering in SQL, not in C# query objects.

## Documentation

Per the starter table in [documentation.md](../code-style/documentation.md):

### Query / Commands class

- `/// <summary>` starts with **Fetches** (for `Query`/`Queries`) or **Persists** / **Writes** (for `Command`/`Commands`)
- One-liner — `<remarks>` only when multi-method commands need explanation

```csharp
/// <summary>Fetches OLX external listings that have not been enriched yet.</summary>
public sealed class UnenrichedListingsQuery { }

/// <summary>Persists status changes for supply source URLs.</summary>
public sealed class SupplySourceUrlCommands { }
```

### Method docs

- `/// <summary>` one-liner — describes what the method returns or what it persists

## Naming

| Suffix | Purpose | Examples |
|---|---|---|
| `Query` | Single read operation | `UnclassifiedListingsQuery` |
| `Queries` | Multiple related reads on one entity | `ChannelsQueries` |
| `Command` | Single write operation | `MarkListingPublishedCommand` |
| `Commands` | Multiple related writes on one entity | `SupplySourceUrlCommands` |
| `Repository` | `DapperRepository<,>` subclass for one entity | `OlxListingsRepository` |

## Class shape (queries / commands)

- **Sealed class** with primary constructor injecting `IDbConnectionFactory`
- **Connection pattern** — `await using var conn = await connectionFactory.CreateOpenAsync(ct);` per method
- **No DbContext** — Dapper uses raw connections; if you need EF, use an EF repository against the `DbContext` instead

## See also

- [database.md](database.md) — schema-first rule, type mappings, EF Core path
- [entities.md](entities.md) — entity shape, `IKeyedEntity<TId>` / `IHasTableName`, audit interfaces
- [enums.md](enums.md) — enum storage strategy, text vs Postgres-native, `AddEnumTypeHandler<TEnum>`
- [services.md](../architecture/services.md) — service / repository naming
- [documentation.md](../code-style/documentation.md) — XML doc + starter table
