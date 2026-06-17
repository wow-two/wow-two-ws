# Response models

*Last updated: 2026-06-13*

The HTTP success envelope `ApiResponse<T>` and the DTOs it carries — every success is wrapped; errors are not (they go out as ProblemDetails, see [problem-details.md](problem-details.md)).

## The envelope rule

- **Success → wrapped** in `ApiResponse<T>` — the client always reads `.data`.
- **Error → never wrapped** — RFC-7807 ProblemDetails, owned by [problem-details.md](problem-details.md). The envelope never carries an error shape.
- The two channels are disjoint: a 2xx body is always an `ApiResponse<T>.Success`; a non-2xx body is always a `ProblemDetails`. The client branches on status, not on a flag inside the body.

---

## `ApiResponse<T>` shape

Lives in the product's shared lib (`{Product}.Common/Models/ApiResponse.cs` — `Haven.Common`, `SmartQr.Platform.Core`). A discriminated union: `abstract record` + private ctor so the only instances are the nested cases.

```csharp
public abstract record ApiResponse<T> : ApiResponse
{
    private ApiResponse() { }

    public sealed record Success : ApiResponse<T>
    {
        public required T Data { get; init; }
    }

    public sealed record Failure : ApiResponse<T>
    {
        public required HttpStatusCode StatusCode { get; init; }
        public required string Error { get; init; }
    }

    public static Success Ok(T data) => new() { Data = data };
}
```

| Member | Role |
|---|---|
| `Success.Data` (`required T`) | the typed payload — serialized as `.data` |
| `Failure.StatusCode` + `Failure.Error` | **client-side only** — how an API client deserializes a non-2xx response so callers pattern-match instead of catching. Servers never emit `Failure` — that channel is ProblemDetails. |
| `ApiResponse<T>.Ok(data)` | the **only** way a controller builds a success body |

- Success carries **`Data` and nothing else** — no `message` / `meta` field exists in the envelope today. Anything beyond the payload belongs in the DTO. (If a per-response message is ever needed, it's added here as an optional `init` property, not improvised at call sites.)
- Base non-generic `ApiResponse` holds shared constants only — `const string UnexpectedErrorMessage = "Unexpected error"` for the fall-through `Problem(title:)` of an unmatched result.

---

## Building it in a controller

Wrap the domain success payload via `ApiResponse<T>.Ok(...)`, hand it to MVC's `Ok(...)`; map the failure to `Problem(...)` (never to a `Failure` body).

```csharp
return result switch
{
    ApplicationResult<CodeListResult.Success, CodeListResult.Failure>.Success ok
        => Ok(ApiResponse<IReadOnlyList<CodeDto>>.Ok(ok.Data.Codes)),

    ApplicationResult<CodeListResult.Success, CodeListResult.Failure>.Failure fail
        => Problem(detail: fail.Error.ErrorMessage, statusCode: ApiResults.ToStatusCode(fail.Error)),

    _ => Problem(statusCode: StatusCodes.Status500InternalServerError, title: ApiResponse.UnexpectedErrorMessage)
};
```

- `T` is **always a DTO** (or `IReadOnlyList<TDto>`, or a `Result.Success` carrying DTOs) — the envelope never wraps another envelope.
- `204 No Content` / file streams are **not** wrapped — there's no payload to put in `.data`.
- Failure mapping is the controller's job — see [controllers.md](controllers.md) (`AppResult.Match` → `Problem()`).

---

## DTOs — what `T` is

The payload type. Pure data, entity-first, reusable across result containers. Record style (`sealed record`, body props, `required`) is owned by [models.md](../code-style/models.md) — not restated here.

| Rule | Detail |
|---|---|
| Naming | `{Entity}Dto`, entity-first, singular — `CodeDto`, `RuleDto`, `ChannelDto` |
| Qualify | only when one entity has multiple projections — `ChannelWithPipelinesDto` vs `ChannelDto` |
| Parent prefix | only for context-bound entities (`ChannelSourceDto` — always channel-scoped); independent entities stay bare (`PipelineDto`, not `ChannelPipelineDto`) |
| Shape | `sealed record`, `required` on every non-nullable property — pure data, no behavior |
| Flat | no nesting unless the entity genuinely has a sub-object |
| No metadata | pagination / status / timestamps that aren't entity fields don't go in the DTO and don't go in the envelope |
| Location | `Application/{Feature}/Models/{Name}.cs` |

Reference: `CodeDto` (`SmartQr.Api/Application/Codes/Core/Models/CodeDto.cs`) — `sealed record`, all `required`, `IReadOnlyList<RuleDto> Rules`.
