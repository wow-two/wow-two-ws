# Enums

*Last updated: 2026-02-23*

Domain enums live alongside entities in the Domain assembly under a subdomain folder.

## Location

`{Repo}.Domain/{Subdomain}/Enums/{Name}.cs` — **one file per enum** (per [code-organization.md](code-organization.md)).

## Naming

- **Singular** — no plural (`ChannelType` not `ChannelTypes`)
- **No `Enum` suffix** — `PipelineRunStatus` not `PipelineRunStatusEnum`
- **PascalCase values** — `Supply`, `Demand`, `ApartmentRent`

## Modeling

- **Backing type** — default `int`, no explicit values unless mapping to DB ordinals (rare; prefer PG enums)
- **No `[Flags]`** unless genuinely bitwise — most domain enums are not

## Database mapping (Postgres)

- **Storage** — PostgreSQL custom enum types (`CREATE TYPE listing_type AS ENUM (...)`)
- **Registration** — map globally via `MapEnum<T>()` inside `UseNpgsql()` and `NpgsqlDataSourceBuilder` — NOT per-property `.HasConversion()`. Both calls are needed for Npgsql 9.x
- **C# ↔ PG case mapping** — PascalCase C# values auto-map to snake_case PG values (`ApartmentRent` ↔ `'apartment_rent'`)

```csharp
// Registration — once at startup
services.AddSingleton(sp =>
{
    var settings = sp.GetRequiredService<DbSettings>();
    var dataSourceBuilder = new NpgsqlDataSourceBuilder(settings.ConnectionString);
    dataSourceBuilder.MapEnum<ChannelType>(nameof(ChannelType).ToSnakeCase());
    return dataSourceBuilder.Build();
});

services.AddDbContext<AppDb>((sp, opt) =>
    opt.UseNpgsql(sp.GetRequiredService<NpgsqlDataSource>(), npgsql =>
    {
        npgsql.MapEnum<ChannelType>(nameof(ChannelType).ToSnakeCase());
    }));
```

> **SDK note:** the SDK plans a source generator to eliminate this MapEnum duplication. Until then, both calls are required.

## Documentation

### Enum-level

- `/// <summary>` starts with **Defines** — per [documentation.md](documentation.md) starter table
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

## See also

- [entities.md](entities.md) — how enums show up on entities (including enum arrays)
- [database.md](database.md) — PG type mapping
- [documentation.md](documentation.md) — XML doc + starter table
