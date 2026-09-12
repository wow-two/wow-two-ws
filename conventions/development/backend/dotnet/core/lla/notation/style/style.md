# Style

*Last updated: 2026-09-10*

> What the text inside a file looks like — its order, its wrapping, its width.
> Purpose — remove every per-file judgment call about layout so a diff shows meaning, not formatting.
> Use case — reach here while writing or reviewing the body of any file.

## The file's frame

What a file declares before any type appears.

### Namespaces
- namespace form → [constructs](../../constructs/constructs.md) § *The constructs*.

```csharp
// ✅ Correct
namespace WoW.Two.Sdk.Backend.Beta.Data.Abstractions;

public interface IEntity { Guid Id { get; } }
```

### Imports
- `System.*` → `Microsoft.*` → third-party → project namespaces — IDE auto-sort handles it; never hand-order
- No unused `using` statements (analyzer enforces)
- static imports → [naming](../naming/naming.md) § *`using static` is banned*.

Neither a construct nor a statement — a directive declares no type and runs nothing; it changes what a file can see.

| Directive | Verdict | Rule |
|---|---|---|
| `using {namespace}` | use | ordered per § *The file's frame* |
| `global using` | use with care | one file per project owns them; scattered, it is invisible at the call site |
| `using {alias} = {type}` | use with care | only to disambiguate two types with the same name in one file |
| `using static` | → [naming](../naming/naming.md) | static-import policy |
| `extern alias` | banned | two assemblies exporting one type is a packaging fault, fixed upstream |

- `#nullable`
  - verdict: use
  - rule: only to enable; a per-file disable hides a real warning
- `#if` · `#elif` · `#else` · `#endif`
  - verdict: use with care
  - rule: a build-configuration branch, never a feature switch
- `#region` · `#endregion`
  - verdict: use
  - rule: grouping members past 60 lines → [constructs](../../constructs/constructs.md) § *Behavior components*
- `#pragma warning`
  - verdict: use with care
  - rule: must name the warning and carry a `//` saying why
- `#line` · `#error` · `#warning`
  - verdict: use with care
  - rule: generator output and build-time assertions only
- `#!`, `#:sdk`, `#:property`, `#:package`, `#:project`
  - verdict: use with care
  - rule: file-based apps only

---

## The signature
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

---

## The body

### Shape

Whether a member's body may be `=>` is decided by its **component**, never by the member. The gates below run in order,
and the first `no` blocks the expression body — a component that grants `=>` still has to pass them.

1. must be a single expression with no statement body.
2. must fit one line inside the 120-character budget.
3. must hold no intermediate worth naming — an intermediate you would want to breakpoint fails here.
4. must not branch — a conditional is a step, and a step wants a name; a fluent chain is one expression.
5. must not be a construction — `new Foo(a, b)` is a body, however short, because a constructed shape gains members.
6. must belong to a component whose doc grants `=>` — the grant is per component, and the default is a block body.

- must use a block body `{ }` when any gate answers no.
- must apply the rule from the start, not on the first growth — a one-liner written today gets its block today.

### Declaring a value
- must use `var` when the initializer names the type — `var codes = new List<CodeEntity>();` repeats nothing.
- must write the type when the initializer does **not** show it — a call, a ternary, a chained LINQ result.
- the rule is not a ban: `var` is the default, and spelling the type is the exception it earns.

### Literals
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

---

## Chains

- must not cap a chain's length — a chain is one expression, however many calls it carries.
- must keep a chain on one line while it fits the 120-character budget.
- must break an overflowing chain onto one call per line, each line opening with the dot.
- must not split a chain that already fits — a break earns its place only by overflow.

```csharp
// ✅ fits, so it stays on one line
RuleFor(x => x.Ssid).NotEmpty().MaximumLength(32);
// ✅ overflows, so every call takes a line
RuleFor(x => x.Password)
    .NotEmpty()
    .MinimumLength(8)
    .WithMessage("A network password is at least 8 characters.");
```

---

## Width
**120 characters, hard.** Rider and ReSharper draw the margin there by default, so the guide is already on
screen; the limit keeps two files legible side by side on a 1920 display.

- Applies to every line — code, XML doc comments, string literals in source.
- **Doc comments break the limit most often, and this limit is the *last* gate they pass.**
  - run its field's own test first ([documentation](../documentation/documentation.md)).
    - a block wrapped without that pass hides the defect.
- Only a block that survives both earlier gates and still exceeds 120 goes multi-line, tags on their own lines:

```csharp
// ✅ Correct — the block wraps, each line under 120
/// <summary>
/// Shared payload-encoding primitives for the static <see cref="CodeContent"/> types — escaping and formatting
/// helpers ported byte-for-byte from the frontend's <c>contentTypes.ts</c>, so a code encoded here decodes
/// identically to one the builder previewed.
/// </summary>

// ❌ Wrong — one 240-char line, unreadable in a split pane and in a diff
/// <summary>Shared payload-encoding primitives for the static <see cref="CodeContent"/> types — escaping and formatting helpers ported byte-for-byte from the frontend's <c>contentTypes.ts</c>, so a code encoded here decodes identically to one the builder previewed.</summary>
```

- **Code over 120** wraps at the natural boundary — one argument, one LINQ operator, one initializer member per line.
- **Exempt:** a string literal or URL that cannot be split without changing its value, and generated code.
- No second, looser tier — two 150-char panes no longer fit a 1920 display.

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

---

## Neighbours

- [constructs](../../constructs/constructs.md) — the constructs and statements these rules lay out
- [components](../../../mla/components/components.md) — the components that grant an expression body
