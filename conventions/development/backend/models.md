# Models

*Last updated: 2026-02-23*

General rules for all C# models (entities, result types, DTOs, settings, value objects).

## Record style

Records use **body properties with `{ get; init; }`** — not positional constructors (primary ctors). Applies to entities, DTOs, results, and all data-carrying records.

**Why:** Positional constructor parameters don't support standard XML doc comments (`/// <summary>`, `/// <example>`). Body properties do.

**Exception:** Primary constructors are fine for **DI injection** (services, controllers, handlers) where XML docs on parameters aren't needed.

```csharp
// ✅ Correct — body properties with XML docs
public sealed record PipelineDto
{
    /// <summary>Gets the kebab-case pipeline id.</summary>
    /// <example>sup-scrape-olx-urls</example>
    public required string Id { get; init; }

    /// <summary>Gets the display name.</summary>
    /// <example>Scrape URLs</example>
    public required string Name { get; init; }
}

// ❌ Wrong — positional ctor, XML docs don't attach to parameters
public sealed record PipelineDto(string Id, string Name);

// ✅ OK — primary ctor for DI injection (no XML docs needed)
public class ChannelsController(
    PipelineRegistry registry,
    PipelineExecutionTracker tracker) : ControllerBase
```

## `sealed record` everywhere

Default to `sealed record` for every data carrier. Open `record` (non-sealed) only when intentionally designed for inheritance — which is rare and usually a code smell.

## Member rules

### Required vs init defaults

- **`required`** on every non-nullable property whose value must come from outside the constructor (caller, EF, binder)
- **No default values** unless the property is genuinely optional
- **Init-only** (`{ get; init; }`) for immutable models — settings, DTOs, value objects
- **Get-set** (`{ get; set; }`) for entities — EF Core requires set accessors

### Nullability

- Non-nullable by default — use NRT (`string`, not `string?`)
- `?` on the type when the value is genuinely optional
- Never `string.Empty` or `[]` as a default for a non-nullable — leave it required

### Collections

- Always `List<T>` for collection-typed properties (EF Core compat, Npgsql array mapping, mutability for `Add`)
- Never `T[]`, `ICollection<T>`, `IEnumerable<T>`, `IReadOnlyList<T>` on entities
- Three patterns (see [entities.md](entities.md) for entity-specific guidance):
  - `public required List<T> Prop { get; set; }` — always-populated value collections
  - `public List<T> Prop { get; set; } = null!;` — EF navigation properties
  - `public List<T>? Prop { get; set; }` — genuinely optional collections

## Documentation

Every public model gets `/// <summary>` (required) + `/// <example>` (required, see per-kind tables in linked files). Properties: `/// <summary>` + `/// <example>` (except PK/FK which skip `<example>`).

Per the starter table in [documentation.md](documentation.md):

| Kind | Summary starter |
|---|---|
| Entity | **Represents** |
| DTO | **Represents** (or projection-shape description) |
| Settings | **Configuration for** |
| Result base | **Represents the outcome of** |
| Value object | **Represents** |

## Naming

- **Entities** — suffix with `Entity` when the type maps 1:1 to a DB table (`ChannelEntity` → `channels` table)
- **Value objects within entities** — no suffix (`PipelineRun`, `NodeRun`)
- **DTOs** — suffix with `Dto` (`ChannelDto`, `ChannelWithPipelinesDto`)
- **Settings** — suffix with `Settings` (`ClassificationSettings`)
- **Results** — suffix with `Result` (`ChannelGetAllResult`)
- **Query/Command** — suffix with `Query` / `Command` (`ChannelGetAllQuery`, `PipelineExecuteCommand`)

## See also

- [entities.md](entities.md) — entity-specific modeling rules
- [enums.md](enums.md) — enums
- [settings.md](settings.md) — settings records
- [result-pattern.md](result-pattern.md) — Result type structure
- [code-organization.md](code-organization.md) — file-per-type
- [documentation.md](documentation.md) — XML doc + starter table
