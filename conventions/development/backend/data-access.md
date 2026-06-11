# Data access (Dapper)

*Last updated: 2026-02-23*

Dapper query and command classes for direct SQL access, shared across services via a common Persistence assembly.

## Location

| Folder | Purpose | Examples |
|---|---|---|
| `{Repo}.Persistence/Queries/` | Read operations | `UnclassifiedListingsQuery`, `UnenrichedListingsQuery` |
| `{Repo}.Persistence/Commands/` | Write operations | `SupplySourceUrlCommands` |

One file per query/command type (per [code-organization.md](code-organization.md)).

## Modeling

### Class shape

- **Sealed class** with primary constructor
- **Constructor** — inject `IDbConnectionFactory` (SDK's `Data.Dapper` package) — single connection-factory abstraction across the repo
- **Connection pattern** — `await using var conn = await connectionFactory.CreateOpenAsync(ct);` at the start of each method
- **No DbContext** — Dapper uses raw connections; if you need EF, use a repository against the DbContext instead

### Naming

| Suffix | Purpose | Examples |
|---|---|---|
| `Query` | Single read operation | `UnclassifiedListingsQuery` |
| `Queries` | Multiple related reads on one entity | `ChannelsQueries` |
| `Command` | Single write operation | `MarkListingPublishedCommand` |
| `Commands` | Multiple related writes on one entity | `SupplySourceUrlCommands` |

### DI registration

Scoped lifetime (shares request-scoped connection state). Register in the persistence registration extension.

## SQL conventions

- **Table names** — use a `Tab<TEntity>()` helper that resolves the entity's table name; alternatively hard-code snake_case
- **Column names** — hard-coded snake_case is fine for simple single-table queries. Use `Col(nameof(Entity.Prop), alias)` when building dynamic WHERE clauses with aliases
- **Table constants** — define at class level: `private static readonly string Table = Tab<OlxExternalListingEntity>();`
- **Raw strings** — follow [code-organization.md](code-organization.md) raw-string rules (opening `"""` on its own line)
- **Parameters** — `@paramName` in SQL, pass via anonymous object or `DynamicParameters`
- **Wrap all calls** in `new CommandDefinition(sql, parameters, cancellationToken: ct)` — never call `QueryAsync(sql, parameters)` without it (loses CT)

```csharp
public sealed class UnenrichedListingsQuery(IDbConnectionFactory connectionFactory)
{
    private static readonly string Table = Tab<OlxExternalListingEntity>();

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

> **Note:** `const string` cannot use string interpolation — use `static readonly string` when fragments reference `Tab<T>()` or `Col()` helpers.

## Type handlers

The SDK's `Data.Dapper` package registers default type handlers:
- `DateOnlyTypeHandler` — `DATE` ↔ `DateOnly`
- `ListTypeHandler<string>` — `TEXT[]` ↔ `List<string>`
- Snake-case → PascalCase property mapping

If you need additional list handlers (`List<int>`, `List<Guid>`), register at startup:

```csharp
SqlMapper.AddTypeHandler(new ListTypeHandler<int>());
SqlMapper.AddTypeHandler(new ListTypeHandler<Guid>());
```

## Documentation

Per the starter table in [documentation.md](documentation.md):

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

## See also

- [database.md](database.md) — schema-first rule, type mappings, EF Core path
- [services.md](services.md) — service / repository naming
- [documentation.md](documentation.md) — XML doc + starter table
