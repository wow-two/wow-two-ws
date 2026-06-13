# Result pattern

*Last updated: 2026-06-13*

Operations that can succeed or fail return a **result type** instead of throwing. The canonical carrier is the SDK's generic `Result` / `Result<T>`; named domain containers (sealed-class inheritance, CQRS static containers) are the per-operation alternative when a single railway value is too coarse.

## Canonical carrier — SDK `Result` / `Result<T>`

> **Default for new code.** `WoW.Two.Sdk.Backend.Beta.Results.Result` (no value) and `Result<T>` (value-carrying), in [`src/Foundation/Results/Result.cs`](../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/src/Foundation/Results/Result.cs) + [`ResultOfT.cs`](../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/src/Foundation/Results/ResultOfT.cs).

Both are **abstract records** with a private constructor and two nested sealed-record cases:

- `Result` → `Result.Success` · `Result.Failure(DomainError Error)`
- `Result<T>` → `Result<T>.Success(T Value)` · `Result<T>.Failure(DomainError Error)`

Construct via static factories — never `new` a case directly:

| Factory | Returns | Use |
|---|---|---|
| `Result.Ok()` | `Result.Success` | Void operation succeeded |
| `Result.Fail(error)` | `Result.Failure` | Void operation failed, carries `DomainError` |
| `Result<T>.Ok(value)` | `Result<T>.Success` | Operation produced `value` |
| `Result<T>.Fail(error)` | `Result<T>.Failure` | Operation failed, carries `DomainError` |

Failure **always** carries a `DomainError` (§ DomainError) — there is no bare-string failure case on the SDK carrier. `IsSuccess` is a convenience predicate (`this is Success`); prefer `Match` over reading it.

### Consume — `Match` / `Map`

`Match<TOut>(onSuccess, onFailure)` collapses both cases into one value; `onFailure` receives the `DomainError`. `Map<TOut>(selector)` transforms the success value and propagates the failure unchanged — `Result.Map` lifts a void result into `Result<TOut>`, `Result<T>.Map` re-maps the value.

```csharp
using WoW.Two.Sdk.Backend.Beta.Results;
using WoW.Two.Sdk.Backend.Beta.Errors;

Result<User> result = repo.Find(id) is { } user
    ? Result<User>.Ok(user)
    : Result<User>.Fail(DomainError.NotFound("user.not_found", "User not found"));

string label = result.Match(
    onSuccess: u => u.DisplayName,
    onFailure: err => $"[{err.Code}] {err.Message}");

Result<UserDto> dto = result.Map(u => u.ToDto());   // failure flows through untouched
```

> **Drift — do NOT cite `ErrorOr<T>` or implicit `DomainError`→result conversions.** They appear only in [`src/Foundation/Errors/README.md`](../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/src/Foundation/Errors/README.md) (`public ErrorOr<User> GetUser(...) => ... DomainError.NotFound(...)`). No `ErrorOr` type and no `implicit operator` exists in any `.cs` under `Foundation/Results` or `Foundation/Errors`. Until the SDK ships them, return `Result<T>.Fail(error)` explicitly. The README is stale.

## DomainError

`WoW.Two.Sdk.Backend.Beta.Errors.DomainError` ([`src/Foundation/Errors/DomainError.cs`](../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/src/Foundation/Errors/DomainError.cs)) is the immutable failure payload:

```csharp
public sealed record DomainError(string Code, string Message, DomainErrorCategory Category, string? Detail = null)
```

- `Code` — stable, dotted, machine-readable (`orders.not_found`). Not localized.
- `Message` — human-readable; localize when possible.
- `Category` — a `DomainErrorCategory` member; drives the HTTP mapping.
- `Detail?` — optional extra context.
- `StatusCode` — computed `(int)Category`; no manual switch needed.

Prefer the convenience factories over the positional constructor — they pin the category:

| Factory | Category | HTTP |
|---|---|---|
| `DomainError.Validation(code, message, detail?)` | `Validation` | 400 |
| `DomainError.Unauthorized(...)` | `Unauthorized` | 401 |
| `DomainError.Forbidden(...)` | `Forbidden` | 403 |
| `DomainError.NotFound(...)` | `NotFound` | 404 |
| `DomainError.Conflict(...)` | `Conflict` | 409 |
| `DomainError.BusinessRule(...)` | `BusinessRule` | 422 |
| `DomainError.Unexpected(...)` | `Unexpected` | 500 |
| `DomainError.Unavailable(...)` | `Unavailable` | 503 |

`DomainErrorCategory` is an HTTP-status-valued enum — each member's integer value *is* its status code: `Validation = 400`, `Unauthorized = 401`, `Forbidden = 403`, `NotFound = 404`, `Conflict = 409`, `BusinessRule = 422`, `TooManyRequests = 429`, `Unexpected = 500`, `Unavailable = 503`. (`TooManyRequests` has no convenience factory yet — use the positional constructor with `DomainErrorCategory.TooManyRequests`.)

## When to use which

| Shape | Use when |
|---|---|
| **`Result` / `Result<T>` (railway)** | Default. One success value (or none) + one error. Composes via `Map`/`Match`; failure already HTTP-aware through `DomainError`. New CQRS handlers, service methods, repository ops. |
| **Named domain container** (sealed-class inheritance, *below*) | A single error payload is too coarse — the operation has **multiple distinct outcomes**, a **typed failure enum** (`SeedFailure`), or **variant-specific success data** that doesn't fit one `T`. The base name reads as the outcome category (`SeedResult<T>`). |
| **CQRS static container** (`{Domain}{Op}Result` with `ISuccessResult`/`IFailureResult`) | Product-side query/command result feeding the `ApiResponse` mapper. Lives in the product, not the SDK. See [api-endpoints.md](../presentation/api-endpoints.md). |

> `ISuccessResult` / `IFailureResult` are **product-side** marker interfaces, not SDK types — they don't exist under the SDK `Foundation`. Real SDK named containers (e.g. `EmailSendResult` in [`comms/email/IEmailSender.cs`](../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/src/comms/email/IEmailSender.cs), carrying its own `FailureReason`) follow the same *named-container* spirit without those interfaces.

## Named domain container — sealed-class inheritance

When the railway carrier is too coarse, model the outcome as **sealed class inheritance** — one abstract base with `Success` and `Failure` as sealed inner classes.

### Why this shape

- Pattern-matching exhaustiveness — `switch` over the base with `Success` and `Failure` cases is compiler-checked
- The base name reads as the outcome category (`SeedResult<T>`, `ChannelGetAllResult`)
- Different payloads on each variant — `Success` holds the data, `Failure` holds the error (and an optional typed failure enum the railway `DomainError` can't express)
- Sealed inner classes prevent external subclassing
- Static factory methods on each variant keep construction explicit

### File-per-type exception

`Success` and `Failure` are **nested inside** the abstract base — they exist only as variants of the parent. The whole hierarchy lives in **one file** (per [code-organization.md](../code-style/code-organization.md) nested-types rule).

### Modeling

#### Base class

- **Abstract class** with private constructor (prevents external subclassing)
- **Shared properties** — common to both outcomes (e.g. `Id`, `OperationVersion`)
- **`{ get; private init; }`** — properties set only via the static factory methods

#### Success / Failure inner classes

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

### Usage

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

See [api-endpoints.md](../presentation/api-endpoints.md) for full CQRS shape.

## Naming

| Type | Naming | Example |
|---|---|---|
| Railway carrier (SDK) | `Result` / `Result<T>` | — (don't rename per-domain) |
| Failure payload (SDK) | `DomainError` | `DomainError.NotFound("user.not_found", …)` |
| Domain operation result | `{Domain}{Operation}Result` | `SeedResult<T>`, `ChannelGetAllResult` |
| Failure reason enum | `{Domain}{Operation}Failure` or `{Domain}Failure` | `SeedFailure` |

## Documentation

Per [documentation.md](../code-style/documentation.md):

- **SDK carrier / abstract base** — `<summary>` starts with **Represents the outcome of**
- **Success variant** — `<summary>` describes the success state (no fixed starter)
- **Failure variant** — `<summary>` describes the failure state (no fixed starter)
- **Members on each variant** — follow the standard property rules

## See also

- [api-endpoints.md](../presentation/api-endpoints.md) — CQRS Result containers + ApiResponse / ProblemDetails mapping
- [code-organization.md](../code-style/code-organization.md) — nested-types file rule
- [documentation.md](../code-style/documentation.md) — XML doc + starter table
