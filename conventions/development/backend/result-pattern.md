# Result pattern

*Last updated: 2026-02-23*

Operations that can succeed or fail use **sealed class inheritance** — one abstract base with `Success` and `Failure` as sealed inner classes.

## Why this shape

- Pattern-matching exhaustiveness — `switch` over the base with `Success` and `Failure` cases is compiler-checked
- The base name reads as the outcome category (`SeedResult<T>`, `ChannelGetAllResult`)
- Different payloads on each variant — `Success` holds the data, `Failure` holds the error
- Sealed inner classes prevent external subclassing
- Static factory methods on each variant keep construction explicit

## File-per-type exception

`Success` and `Failure` are **nested inside** the abstract base — they exist only as variants of the parent. The whole hierarchy lives in **one file** (per [code-organization.md](code-organization.md) nested-types rule).

## Modeling

### Base class

- **Abstract class** with private constructor (prevents external subclassing)
- **Shared properties** — common to both outcomes (e.g. `Id`, `OperationVersion`)
- **`{ get; private init; }`** — properties set only via the static factory methods

### Success / Failure inner classes

- **`public sealed class Success : {Base}`** and **`public sealed class Failure : {Base}`**
- **Static `Create()` factory** — each subclass exposes a static factory method
- **Outcome-specific properties**: Success holds the payload, Failure holds error details + optional failure enum

```csharp
/// <summary>Represents the outcome of reading seed data for an entity type.</summary>
/// <example>Success with deserialized entities, or failure with reason and message</example>
public abstract class SeedResult<T>
{
    private SeedResult() { }

    /// <summary>Seed data read successfully — entities ready for upsert.</summary>
    /// <example>3 channel records deserialized from seed file</example>
    public sealed class Success : SeedResult<T>
    {
        /// <summary>Gets the deserialized entities.</summary>
        /// <example>Collection of channels</example>
        public IReadOnlyList<T> Entities { get; private init; } = [];

        public static Success Create(IReadOnlyList<T> entities) => new() { Entities = entities };
    }

    /// <summary>Seed data read failed — error tracked for diagnostics.</summary>
    /// <example>Seed file missing from expected path</example>
    public sealed class Failure : SeedResult<T>
    {
        /// <summary>Gets the failure reason category.</summary>
        /// <example>Seed file missing from expected path</example>
        public SeedFailure FailureType { get; private init; }

        /// <summary>Gets the human-readable error message.</summary>
        /// <example>File not found: Data/Seed/channels.json</example>
        public string ErrorMessage { get; private init; } = "";

        public static Failure Create(SeedFailure failureType, string errorMessage) =>
            new() { FailureType = failureType, ErrorMessage = errorMessage };
    }
}
```

## Usage

```csharp
var result = seedReader.Read<ChannelEntity>();

switch (result)
{
    case SeedResult<ChannelEntity>.Success success:
        foreach (var channel in success.Entities) { /* upsert */ }
        break;
    case SeedResult<ChannelEntity>.Failure failure:
        logger.LogError("Seed failed: {Type} — {Message}", failure.FailureType, failure.ErrorMessage);
        break;
}
```

## CQRS variant — domain result containers

For CQRS query/command handlers, the domain result container is a **static class** with nested `Success : ISuccessResult` / `Failure : IFailureResult` records:

```csharp
/// <summary>Represents the outcome of fetching all channels.</summary>
/// <example>Success with channels, or failure with error message</example>
public static class ChannelGetAllResult
{
    public sealed record Success(IReadOnlyList<ChannelWithPipelinesDto> Channels) : ISuccessResult;
    public sealed record Failure(string ErrorMessage) : IFailureResult;
}
```

See [api-endpoints.md](api-endpoints.md) for full CQRS shape.

## Naming

| Type | Naming | Example |
|---|---|---|
| Domain operation result | `{Domain}{Operation}Result` | `SeedResult<T>`, `ChannelGetAllResult` |
| Failure reason enum | `{Domain}{Operation}Failure` or `{Domain}Failure` | `SeedFailure` |

## Documentation

Per [documentation.md](documentation.md):

- **Base class** — `<summary>` starts with **Represents the outcome of**
- **Success variant** — `<summary>` describes the success state (no fixed starter)
- **Failure variant** — `<summary>` describes the failure state (no fixed starter)
- **Members on each variant** — follow the standard property rules

## See also

- [api-endpoints.md](api-endpoints.md) — CQRS Result containers + ApiResponse mapping
- [code-organization.md](code-organization.md) — nested-types file rule
- [documentation.md](documentation.md) — XML doc + starter table
