# Request models

*Last updated: 2026-06-17*

> **API request** — the presentation-layer body a client sends, named `{Verb}{Noun}ApiRequest`; a controller binds it and maps it to its **application request** (the mediator `Command` / `Query` — see [mediator.md](../messaging/mediator.md)).
> Both are requests — the `Api` / `Application` qualifier tells the layers apart.

## Request shape

### Documentation

#### Summary

- [Summary doc block conventions](../code-style/documentation.md)
- keyword - `Represents the {verb}-{noun} request body.`, e.g. `Represents the create-code request body.`

#### Remarks

- omit — a request model is a plain body DTO; there's nothing to direct the consumer to

### Declaration

- must be a `public sealed record`
- must be named `{Verb}{Noun}ApiRequest`, verb-first - e.g. `CreateCodeApiRequest`, `UpdateCodeApiRequest`
- `Api` marks the presentation layer - never bare `Request` or `Dto` (the response suffix)
- must live in the API project under `Requests/` - never in `Application/`

### Members

- **body-only** - only what the client sends; never the actor, source IP, route id, or a server timestamp (those are caller context, merged in the mapping)
- `required` on every non-nullable property; each carries a `Gets {what}.` summary (property doc rule → [documentation.md](../code-style/documentation.md))
- nested body types take the same suffix - `RuleApiRequest` inside `CreateCodeApiRequest`
- no validation attributes - business validation is the application request's, in the pipeline ([validation.md](../foundation/validation.md))

### Examples

#### Good

```csharp
/// <summary>Represents the create-namespace request body.</summary>
public sealed record CreateNamespaceApiRequest
{
    /// <summary>Gets the namespace slug.</summary>
    public required string Slug { get; init; }

    /// <summary>Gets the namespace display name.</summary>
    public required string Name { get; init; }
}
```

#### Bad

```csharp
// ❌ actor on the body (server-set) · bare `Request` name · mutable class · no member docs
public class CreateNamespaceRequest
{
    public Guid Actor { get; set; }
    public string Slug { get; set; }
    public string Name { get; set; }
}
```

---

## Mapping

The application request is built **at the edge** by an extension method co-located with the api request (same file — not a separate mapper class). It merges the caller context + route ids the body can't carry.

- one `static` extensions class per request, in the request's file - `{Verb}{Noun}ApiRequestExtensions`
- method named by the target's role - `ToCommand(...)` / `ToQuery(...)`
- summary refs the target via `cref` - `Maps the request to its <see cref="{Command|Query}"/>.`
- pass caller context + route ids explicitly - `request.ToCommand(callerContext, id)`; never read them in the handler
- the application request **never references the api request** - the dependency points one way (api request → application request)
- the mapping method **builds + returns** the application request — block body, not `=>` ([members.md](../code-style/members.md))

#### Good

```csharp
/// <summary>Provides mapping for <see cref="CreateNamespaceApiRequest"/>.</summary>
public static class CreateNamespaceApiRequestExtensions
{
    /// <summary>Maps the request to its <see cref="CreateNamespaceCommand"/>.</summary>
    public static CreateNamespaceCommand ToCommand(this CreateNamespaceApiRequest request, string actor)
    {
        return new CreateNamespaceCommand(request.Slug, request.Name, actor);
    }
}
```

#### Bad

```csharp
// ❌ a separate mapper class far from the request · reads the actor instead of taking it as a param
public sealed class RequestMapper(ICurrentUser user)
{
    public CreateNamespaceCommand Map(CreateNamespaceApiRequest request) => new(request.Slug, request.Name, user.Id);
}
```
