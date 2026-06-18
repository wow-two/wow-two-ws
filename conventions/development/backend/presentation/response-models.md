# Response models

*Last updated: 2026-06-17*

> Response models — the `{Entity}Dto` payload an action returns, wrapped in the `ApiResponse<T>` success envelope. Errors are never wrapped (they go out as ProblemDetails — see [problem-details.md](problem-details.md)).

## The envelope rule

- **Success → wrapped** in `ApiResponse<T>` — the client always reads `.data`.
- **Error → never wrapped** — RFC-7807 ProblemDetails ([problem-details.md](problem-details.md)). The envelope never carries an error shape.
- Disjoint channels: a 2xx body is always `ApiResponse<T>.Success`; a non-2xx body is always `ProblemDetails`. The client branches on status, not a flag in the body.
- `204 No Content` / file streams aren't wrapped — no payload for `.data`.

---

## `ApiResponse<T>` envelope

Lives in the product's shared lib today (`{Product}.Common/Models/ApiResponse.cs`); SDK-extract pending. A discriminated union — `abstract record` + private ctor, so the only instances are the nested cases.

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

- `Success.Data` (`required T`) — the typed payload, serialized as `.data`.
- `Failure` — **client-side only**: how an API client deserializes a non-2xx body to pattern-match instead of catching. Servers never emit `Failure` (that channel is ProblemDetails).
- `ApiResponse<T>.Ok(data)` — the **only** way a controller builds a success body; used in the success arm of `.Match` → see [controllers.md](controllers.md).
- `Success` carries `Data` and nothing else — no `message` / `meta`. Anything beyond the payload belongs in the DTO.

---

## Response shape — the DTO

The payload `T`. Pure data, entity-first; record + property style is owned by [models.md](../code-style/models.md), the summary starter (`Represents …`) by [documentation.md](../code-style/documentation.md).

### Naming

- `{Entity}Dto`, entity-first, singular - `CodeDto`, `RuleDto`, `ChannelDto`
- **`Response` is the envelope's word, never a payload's** - a payload is always `{Entity}Dto`, even a composite / non-entity one: `CurrentUserDto` (not `MeResponse`), `BillingStatusDto` (not `BillingResponse`)
- qualify only for multiple projections - `ChannelWithPipelinesDto` vs `ChannelDto`
- parent prefix only for context-bound entities - `ChannelSourceDto` (always channel-scoped); independent entities stay bare (`PipelineDto`, not `ChannelPipelineDto`)

### Members

- `sealed record`, `required` on every non-nullable property; each carries a `Gets {what}.` summary ([documentation.md](../code-style/documentation.md))
- flat - no nesting unless the entity genuinely has a sub-object
- no metadata - pagination / status / timestamps that aren't entity fields don't go in the DTO or the envelope
- location - `Application/{Feature}/Models/{Name}.cs`

### Examples

#### Good

```csharp
/// <summary>Represents a code projection for the dashboard.</summary>
public sealed record CodeDto
{
    /// <summary>Gets the code's id.</summary>
    public required Guid Id { get; init; }

    /// <summary>Gets the code's display name.</summary>
    public required string Name { get; init; }

    /// <summary>Gets the routing rules of the code.</summary>
    public required IReadOnlyList<RuleDto> Rules { get; init; }
}
```

#### Bad

```csharp
// ❌ `Response` suffix on a payload (that word is the envelope's) · mutable · no member docs · usage metadata in the DTO
public class MeResponse
{
    public Guid UserId { get; set; }
    public int CodesUsedThisMonth { get; set; }
}
```
