# Code organization

*Last updated: 2026-06-14*

## One file per type (REQUIRED)

Every public type lives in its own `.cs` file. The file name matches the type name.

### Exception: generic + non-generic pair

When a non-generic type exists **only** as a convenience alias for a specific generic form, the pair lives in the same file:

```csharp
// ✅ IEntity.cs — non-generic + generic abstract pair
public interface IEntity : IEntity<Guid>;

public interface IEntity<TId>
{
    TId Id { get; }
}
```

Conditions for the same-file exception:
- The non-generic type is the **abstract** convenience form (`IEntity` is just `IEntity<Guid>` with no extra members)
- Both types are at the same abstraction level (both interfaces, or both abstract classes)
- Together they read as one concept with a default-type overload

### What does NOT qualify for the exception

| Case | Resolution |
|---|---|
| Concrete specialization (`public interface IFoo : IFoo<Guid> { string Name { get; } }`) — adds members | Separate file |
| Unrelated types in the same file (e.g. `IAuditable` + `IHasTenant` — independent traits) | Split |
| Sibling types around the same theme (`ISoftDeletable` + `ISoftDeletableBy`) | Split — they have different shapes |
| Result type with nested `Success`/`Failure` (nested classes inside one abstract base) | **Same file** — these are sealed inner classes of one type, not separate types |

### Nested types

Nested types (sealed inner classes, value-object records inside a parent) live in the parent's file when they exist **only** to model variants/states of the parent. Example: `Result<T>` with nested `Success` and `Failure` lives in `Result.cs`.

### File naming

- File name = primary type name + `.cs` (`Channel.cs`, `IEntity.cs`, `ChannelGetAllQuery.cs`)
- For the generic+non-generic exception, the non-generic name wins (`IEntity.cs`, not `IEntity{T}.cs`)
- Generic-only types use the simple base name (`Repository.cs` for `Repository<T>`)

## Source folders

- **Backend source folders are PascalCase**, matching their namespace segment 1:1 (`Mediator/Cqrs/`, `Application/Channels/Queries/`, `Data/Migrations/`). Distinct from the top-level **project** dir `{slug}.backend-services/`, which stays kebab — that's the IDE-collision-proof project folder, not a source folder ([repo/repo-structure.md](../../repo/repo-structure.md) §3).

## Acronyms

- **Acronyms are always PascalCase, never all-caps** — `Id` not `ID`, `Ai` not `AI`, `Api` not `API`, `Sql`, `Http`, `Json`, `Io`, `Ui`, `Mqtt`, `Grpc`.
- First letter capital, rest lowercase, **even when it distorts an established acronym** — consistency over original styling.
- Applies to type / namespace / folder / member names.
- This governs *all-caps runs* only — a mixed-case proper name with no all-caps run (`OAuth`, `SendGrid`, `MailKit`) is unaffected.
- Cross-ref: the SDK's `docs/conventions/naming.md` §Acronyms matches this rule
  ([wow-two-sdk-beta/wow-two-sdk.backend.beta](../../../../../wow-two-sdk-beta/wow-two-sdk.backend.beta/docs/conventions/naming.md)).

## Section dividers

- **Never** use ASCII art dividers — no `// ═══`, `// ---`, `// ***`, or similar C/C++ block separators
- **Never** use dotted/dashed inline comments — no `// ---- Section name ----` or `// -- Section name --`. Use plain comments: `// Section name`
- **Use `#region` / `#endregion`** when a file has distinct logical sections that benefit from collapsing (e.g. internal row types, dimension queries, WHERE builder)
- **Use nothing** when sections are small or obvious — not every group of methods needs a divider
- **Lightweight inline labels are fine** — `// ── Tables ──` or `// ── Meta ──` for small field groups within a class

```csharp
// ❌ Wrong — C++ style block divider
// ══════════════════════════════════════════════════════════════════════════
// Internal row types
// ══════════════════════════════════════════════════════════════════════════

// ✅ Correct — #region for collapsible sections
#region Internal row types
// ...
#endregion

// ✅ Correct — lightweight inline label for field groups
// ── Tables ──
private static readonly string ListingsTable = ListingEntity.TableName;
```

## Parameter formatting

- **More than 2 parameters** — multiline (one parameter per line)
- **2 or fewer parameters** — single line
- Applies to: method signatures, method calls, constructor calls, `new` expressions

```csharp
// ✅ Correct — 2 params, single line
var (where, parameters) = BuildWhere(filter, exclude: "district");

// ✅ Correct — >2 params, multiline
var propertyTypesTask = QueryDimensionAsync(
    nameof(ListingEntity.PropertyType),
    filter,
    exclude: "propertyType",
    ct: ct);

// ✅ Correct — >2 params in nested call
var rows = await conn.QueryAsync<DimensionRow>(
    new CommandDefinition(
        sql,
        parameters,
        cancellationToken: ct));

// ❌ Wrong — >2 params on single line
var rows = await conn.QueryAsync<DimensionRow>(new CommandDefinition(sql, parameters, cancellationToken: ct));
```

## Raw string literals

- **Opening `"""`** always on its own line (never inline with `var sql =`)
- **Closing `"""`** on its own line, at the indentation level that controls the content's left margin
- Applies to: SQL, JSON, XML, any multiline string content

```csharp
// ✅ Correct — """ on its own line
var sql =
    $"""
     SELECT ...
     FROM ...
     """;

// ✅ Correct — in switch expression
var sql = kind switch
{
    DimensionKind.Integer =>
        $"""
         SELECT ...
         FROM ...
         """,
};

// ❌ Wrong — """ inline with assignment
var sql = $"""
    SELECT ...
    FROM ...
    """;
```

## SQL line length

- **Long SQL clauses** — break into one column/condition per line when a line exceeds ~120 chars
- **SELECT** — one column per line when >2 columns
- **JOIN ON** — one condition per line when >1 condition
- **WHERE** — one condition per line
- Keep SQL keywords (`SELECT`, `FROM`, `JOIN`, `WHERE`, `GROUP BY`, `ORDER BY`) at the start of their line

```csharp
// ✅ Correct
var sql =
    $"""
     SELECT
         {Col("LandmarkId", Lls)} AS value,
         {Col("Name", Lm)} AS label,
         COUNT(DISTINCT {Col("Id", Sl)}) AS count
     FROM {ListingsTable} {Sl}
     JOIN {SignalsTable} {Lls}
         ON {Col("ListingId", Lls)} = {Col("Id", Sl)}
         AND {Col("SignalType", Lls)} = 'district'
         AND {Col("LandmarkId", Lls)} IS NOT NULL
     WHERE 1=1 {where}
     GROUP BY
         {Col("LandmarkId", Lls)},
         {Col("Name", Lm)}
     ORDER BY count DESC
     """;
```

## File-scoped namespaces

Required everywhere. Block namespaces are not used.

```csharp
// ✅ Correct
namespace WoW.Two.Sdk.Backend.Beta.Data.Abstractions;

public interface IEntity { Guid Id { get; } }
```

## `using` ordering

- `System.*` first, then `Microsoft.*`, then third-party, then project namespaces — IDE auto-sort handles this; do not hand-order
- No unused `using` statements (analyzer enforces)

## Banned symbols

Per `naming.md` in the SDK conventions:
- `var` for non-obvious types (let analyzers complain)
- Hungarian notation (`m_`, `s_`, `_`)
- Suffix `Helper`, `Util`, `Manager` for *public* types — internal helpers ok
- `dynamic` (use generics or polymorphism)
- `BinaryFormatter` (security)

## See also

- [documentation.md](documentation.md) — XML doc rules
- [models.md](models.md) — record style
