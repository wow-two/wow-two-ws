# Api

*Last updated: 2026-10-02*

> The HTTP surface a service exposes — what a client may send, and what it reads back.
> Purpose — the wire is a contract with a client, so it changes on the client's schedule, not the domain's.
> Use case — adding an endpoint, or changing what one accepts or returns.

## Contract

- must choose a body through the [request/body rule](api-messages.md#requests).
- must wrap a success in the envelope, and send an error as ProblemDetails → [api messages](api-messages.md).
- must keep caller context off the body — the edge merges it into the application message.
- must point the dependency api → application; an application message never references an api one.
- must map inbound `ApiRequest → Command` and outbound `Model → Dto`, both in the controller.
- project placement → [domain structuring](../../../../shapes/service/architecture/clean/domain-structuring.md).
- must hold no logic in the delivery type → [controller](../../constructs/behavior/controller.md).

---

## Action naming

- must name an action for the bare verb — the resource is implied by the controller.
- must add a suffix only to distinguish a variant or a nested resource — `CreateTimedToken`, `GetTokens`.

| HTTP + route | Action | Summary |
|---|---|---|
| `GET api/products` | `Get` | `Gets all {plural}.` |
| `GET api/products/{id}` | `GetById` | `Gets a {singular} by id.` |
| `POST api/products` | `Create` | `Creates a {singular}.` |
| `PUT api/products/{id}` | `UpdateById` | `Updates a {singular}.` |
| `DELETE api/products/{id}` | `DeleteById` | `Deletes a {singular}.` |

- must state the action in the summary, never the HTTP verb — `Sets the code's active state.`

---

## Action attributes

- must declare the success response type matching the actual body; no envelope type for a stream or `204`.
- must declare `ProblemDetails` or the actual `ValidationProblemDetails` schema for each supported failure status; the runtime must satisfy the [error contract](../../../../shapes/service/platform/responses/problem-details.md#wire-contract).
- may carry `[Consumes(mediaType)]` to constrain a non-JSON body.
- may carry `[Tags]`, `[EndpointSummary]` or `[EndpointDescription]` when the generated spec text needs help.

---

## Action content

- must return `Task<IActionResult>` unless the response is a stream.
- action body → [controller member content](../../constructs/behavior/controller.md#member-content).
- must use the [request/body rule](api-messages.md#requests) when binding a payload.
- must read the actor through `ICurrentUser` → [api context](api-context-building.md).
- must reach for `User` or `HttpContext` only for a fact `ICurrentUser` does not expose.
- must take a `CancellationToken` last, and pass it down.
- must build the application request through the request's own mapping method.
- must save the dispatch result to a local — never map, send and return on one line.
- must not catch, validate, orchestrate or hand-map.

---

## Response mapping

- must collapse the saved result with `.Match(onSuccess, onFailure)`.
- must take the failure status from the injected `IErrorHttpStatusCodeMapper`, never a literal.
- must map a failure through `Problem(...)` with context — never bare `NotFound()` or `BadRequest()`.

| Outcome | Return |
|---|---|
| list or single read | `Ok(ApiResponse<T>.Ok(dto))` |
| created, resource has an id | `CreatedAtAction(nameof(GetById), new { id }, value: null)` or a minimal command acknowledgement |
| mutated, no body | `NoContent()` |
| binary or stream | `File(bytes, contentType)` |

- `CreatedAtAction` points at `nameof(GetById)` so the `Location` header round-trips to the read action.

```csharp
// ✅ local, then Match, then a mapped status
var result = await sender.SendAsync(command, ct);

return result.Match<IActionResult>(
    ok => CreatedAtAction(nameof(GetById), new { id = ok.Data.Product.Id },
        value: null),
    fail => Problem(detail: fail.Error.Message, statusCode: statusMapper.ToStatusCode(fail.Error)));
// ❌ try/catch at the edge, raw body, bare status
try { return Ok(await sender.SendAsync(command, ct)); }
catch (NotFoundException) { return NotFound(); }
```

---

## Commands and reads

- must complete validation and durable persistence before acknowledging a synchronous mutation; neither backend nor frontend may present an optimistic persisted result.
- must use `202 Accepted` only for explicitly accepted asynchronous work, with a queryable operation state rather than a completed-resource claim.
- should acknowledge creation through `201` and `Location`, adding an id or revision receipt only when the caller needs it.
- should acknowledge a bodyless update or delete through `204`; retain an operation report when that report is the command's meaningful result.
- must keep grid, list and editor projections in independent read requests; a command does not choose a consumer's query projection.
- may return a created resource when the workflow requires that response, but must not treat it as every grid's complete projection.
- must retain existing documented success contracts during adoption until consumers are migrated together.
- must use query-specific endpoints or explicit projection options when reads need different fields; do not add GraphQL solely to refresh a grid.
- frontend acknowledgement and refresh lifecycle → [state and data](../../../../../../frontend/core/mla/domains/data/state-and-data.md#mutations).

---

## Providers

| Provider | Delivers through | Docs |
|---|---|---|
| MVC controllers | an attribute-routed `Controller` binding the body | [controller](../../constructs/behavior/controller.md) |
| minimal API | an endpoint delegate registered at composition | — |

- must pick one delivery style per service — two routing models over one surface hide which owns a path.
