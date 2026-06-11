# API endpoints

*Last updated: 2026-02-23*

CQRS, mediator wrappers, `ApiResponse<T>` envelope, controller pattern, `Problem()` errors.

## CQRS naming

All endpoint operations follow **query/command separation** — even without a mediator framework. Entity-first naming groups related models in IntelliSense and file explorers.

- **Queries** = reads (GET)
- **Commands** = writes (POST, PATCH, PUT, DELETE)
- **Domain singular** — `Listing`, `Channel`, `Pipeline` (not `Listings`, `Channels`)

## Mediator wrapper

A repo's `Mediator/` namespace wraps the underlying mediator (MediatR, custom, or the SDK's `Mediator` package) behind repo-owned interfaces. Controllers and services depend on `IMediator`, never on the underlying library directly.

| Interface | Purpose |
|---|---|
| `IMediator` | Repo's mediator — `SendAsync()` for queries and commands |
| `IQuery<TResult>` | Read-only operation marker |
| `ICommand<TResult>` / `ICommand` | Write operation markers |
| `IQueryHandler<TQuery, TResult>` | Handler for a query |
| `ICommandHandler<TCommand, TResult>` | Handler for a command |
| `ISuccessResult` | Marker for domain success types |
| `IFailureResult` | Marker for domain failure types |

## ApplicationResult — two-layer outcome

`ApplicationResult<TSuccess, TFailure>` is the **infrastructure-layer** outcome wrapping the **domain-layer** outcome. Each layer carries its own extensible context.

```csharp
// Domain result container — static class with nested Success/Failure
public static class ChannelGetAllResult
{
    public sealed record Success(IReadOnlyList<ChannelWithPipelinesDto> Channels) : ISuccessResult;
    public sealed record Failure(string ErrorMessage) : IFailureResult;
}

// ApplicationResult wraps it — compile-time enforced
ApplicationResult<ChannelGetAllResult.Success, ChannelGetAllResult.Failure>
```

Construction uses `new` directly (no factory methods):

```csharp
// Success
return new ApplicationResult<X.Success, X.Failure>.Success(new X.Success(data));

// Failure
return new ApplicationResult<X.Success, X.Failure>.Failure(new X.Failure("error message"));
```

## Queries

| Aspect | Convention |
|---|---|
| Naming | `{Domain}{Action}{Meta}Query` — `ChannelGetAllQuery`, `ListingFilterOptionsGetQuery` |
| Domain | Always **singular** |
| Location | `Application/{Domain}/Queries/{Name}.cs` |
| Shape | `sealed record` implementing `IQuery<ApplicationResult<XResult.Success, XResult.Failure>>` |
| Handler | `Infrastructure/{Domain}/QueryHandlers/{Name}Handler.cs` |
| Handler `<summary>` | `Handles <see cref="{QueryName}"/>.` — just the reference, nothing else |

```csharp
// Application/Channels/Queries/ChannelGetAllQuery.cs
public sealed record ChannelGetAllQuery : IQuery<ApplicationResult<ChannelGetAllResult.Success, ChannelGetAllResult.Failure>>;

// Infrastructure/Channels/QueryHandlers/ChannelGetAllQueryHandler.cs
/// <summary>Handles <see cref="ChannelGetAllQuery"/>.</summary>
public sealed class ChannelGetAllQueryHandler(PipelineRegistry registry)
    : IQueryHandler<ChannelGetAllQuery, ApplicationResult<ChannelGetAllResult.Success, ChannelGetAllResult.Failure>>
{
    public Task<ApplicationResult<ChannelGetAllResult.Success, ChannelGetAllResult.Failure>> Handle(
        ChannelGetAllQuery request, CancellationToken ct)
    {
        // ... build data ...
        return Task.FromResult(/* ApplicationResult<...>.Success or .Failure */);
    }
}
```

## Commands

| Aspect | Convention |
|---|---|
| Naming | `{Domain}{Action}{Meta}Command` — `PipelineExecuteCommand`, `PipelineToggleCommand` |
| Domain | Always **singular** |
| Location | `Application/{Domain}/Commands/{Name}.cs` |
| Shape | `sealed record` implementing `ICommand<ApplicationResult<XResult.Success, XResult.Failure>>` |
| Handler | `Infrastructure/{Domain}/CommandHandlers/{Name}Handler.cs` |
| Handler `<summary>` | `Handles <see cref="{CommandName}"/>.` — just the reference, nothing else |

## Domain result containers

| Aspect | Convention |
|---|---|
| Naming | `{Domain}{Action}{Meta}Result` — `ChannelGetAllResult`, `ListingFilterOptionsGetResult` |
| Domain | Always **singular** — matches Query/Command naming |
| Location | `Application/{Domain}/Models/{Name}.cs` |
| Shape | `static class` with nested `Success : ISuccessResult` and `Failure : IFailureResult` records |
| Failure | Always has `string ErrorMessage` property |

See [result-pattern.md](result-pattern.md) for the modeling rules.

## DTOs

DTOs carry **only the data payload** — no metadata, no envelope. Reusable across result containers and other DTOs.

### Naming

`{Entity}Dto` — entity-first, singular. Qualify with context only when the same entity has multiple projections (`ChannelWithPipelinesDto` vs `ChannelDto`).

| Concept | DTO | Description |
|---|---|---|
| Channel with pipelines | `ChannelWithPipelinesDto` | Channel + sources + embedded pipelines |
| Channel (flat) | `ChannelDto` | Channel fields only |
| Channel source | `ChannelSourceDto` | Source is channel-specific, prefix makes sense |
| Pipeline | `PipelineDto` | Pipeline is independent — no parent prefix |

### Rules

- **`sealed record`** with body properties (see [models.md](models.md))
- **`required`** on all non-nullable properties
- **Pure data** — no behavior, no metadata (pagination/status/timestamps live in the envelope)
- **Flat** — no nesting unless the entity genuinely has a sub-object
- **No parent prefix** for independent entities (`PipelineDto`, not `ChannelPipelineDto`). Use parent prefix only for context-bound entities (`ChannelSourceDto` — sources are always channel-scoped)
- **Location** — `Application/{Feature}/Models/`

## ApiResponse — HTTP envelope

**Location:** `{Repo}.Common/Models/ApiResponse.cs`

Two variants — generic for success, non-generic for errors:

```csharp
// Success — wraps typed data
public sealed record ApiResponse<T>
{
    public required T Data { get; init; }
    public string? Message { get; init; }

    public static ApiResponse<T> Ok(T data, string? message = null) => ...
}

// Error — no data, just errors
public sealed record ApiResponse
{
    public string? Message { get; init; }
    public required IReadOnlyList<string> Errors { get; init; }

    public static ApiResponse Fail(IReadOnlyList<string> errors, string? message = null) => ...
}
```

### Usage in controllers

```csharp
// Success — data only
return Ok(ApiResponse<IReadOnlyList<ChannelDto>>.Ok(channels));

// Success — with message
return Ok(ApiResponse<PipelineToggleResponse>.Ok(response, "Pipeline triggered"));

// Error — always use Problem() with detail, statusCode, and title
return Problem(
    detail: $"Pipeline '{id}' not found in registry",
    statusCode: StatusCodes.Status404NotFound,
    title: "Pipeline not found");
```

### Rules

- **Success → `ApiResponse<T>`** — wraps typed data in `.data`, optional `.message`
- **Error → always `Problem()`** — RFC 7807 ProblemDetails with `detail`, `statusCode`, `title`
- **Never use bare status methods** — no `NotFound()`, `BadRequest()`, `Conflict()` — always `Problem()` with details
- **`detail` is human-readable** — include the resource ID or validation constraint that failed
- **`title` is a short category** — e.g. "Pipeline not found", "Invalid batch size", "Pipeline already running"
- **`T` is always a DTO** — the envelope never wraps another envelope

## Controllers

### Pattern

Controllers are thin dispatchers — send query/command, pattern match result, map to API response:

```csharp
[HttpGet]
public async Task<IActionResult> GetChannels()
{
    var result = await mediator.SendAsync(new ChannelGetAllQuery());

    return result switch
    {
        ApplicationResult<ChannelGetAllResult.Success, ChannelGetAllResult.Failure>.Success ok
            => Ok(ApiResponse<ChannelGetAllResult.Success>.Ok(ok.Data)),

        ApplicationResult<ChannelGetAllResult.Success, ChannelGetAllResult.Failure>.Failure fail
            => Problem(detail: fail.Error.ErrorMessage, statusCode: StatusCodes.Status500InternalServerError),

        _ => Problem(statusCode: StatusCodes.Status500InternalServerError, title: "Unexpected result type")
    };
}
```

### Documentation

Every controller action gets `/// <summary>` one-liner — verb at start (per [documentation.md](documentation.md) starter table). Keep it **abstract** — don't list implementation details that go stale. Route and HTTP method are already visible from attributes.

```csharp
// ✅ Correct — short verb, abstract
/// <summary>Gets all channels with their pipelines.</summary>
/// <summary>Extracts content from external listing pages.</summary>
/// <summary>Gets per-pipeline stats for a channel.</summary>

// ❌ Wrong — too detailed, will go stale
/// <summary>Returns all channels with their embedded pipelines and live execution state.</summary>
```

### Error handling

- **Never use try/catch in controllers** — services handle their own exceptions and return result types
- For now (pre-mediator), if a service can throw, let it propagate — the global exception handler returns 500
- **All error responses use `Problem()`** — see ApiResponse rules above
- Future: services return Result types, controllers map failures to `Problem()`

## Three-layer model summary

```
┌──────────────────────────────────────────────────────────┐
│  Frontend                                                │
│  Always reads: response.data / response.message / .errors│
└──────────────────────┬───────────────────────────────────┘
                       │ HTTP JSON
┌──────────────────────▼───────────────────────────────────┐
│  ApiResponse<T>         ({Repo}.Common/Models/)          │
│  Stable HTTP envelope — wraps any DTO or Result.Success  │
└──────────────────────┬───────────────────────────────────┘
                       │ Controller pattern-matches
┌──────────────────────▼───────────────────────────────────┐
│  ApplicationResult<S, F> ({Repo}.Common/Mediator/)       │
│  Infrastructure outcome — Success(data) / Failure(error) │
│  Each side carries extensible context                    │
└──────────────────────┬───────────────────────────────────┘
                       │ Handler builds
┌──────────────────────▼───────────────────────────────────┐
│  XResult.Success/Failure (Application/{Domain}/Models/)  │
│  Domain outcome — typed data or typed error              │
└──────────────────────────────────────────────────────────┘
```

## See also

- [result-pattern.md](result-pattern.md) — Result type modeling
- [models.md](models.md) — DTO record style
- [service-architecture.md](service-architecture.md) — Application/Infrastructure split
- [host-configuration.md](host-configuration.md) — controller registration
- [documentation.md](documentation.md) — XML doc + starter table
