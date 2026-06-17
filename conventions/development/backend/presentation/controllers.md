# Controllers

*Last updated: 2026-06-14*

Thin HTTP dispatchers — build a request → `ISender.SendAsync` → `AppResult.Match` → HTTP. No logic, data access, or `try/catch`.

## Controller shape

### Documentation

- Controller `/// <summary>` is `Manages {resource}.` — e.g. `Manages products.`. (Verb/noun-first one-line rule detailed under [Method shape › Documentation](#documentation-1).)

### Attributes

- `[ApiController]` + literal `[Route("api/{noun}")]` — lowercase, no token (`[Route("api/products")]`, not `[Route("api/[controller]")]`).

### Declaration & dependencies

- `sealed`, inherits `ControllerBase` — never `Controller` (no views).
- Primary-ctor inject `ISender` only (see [../messaging/mediator.md](../messaging/mediator.md)); every action takes `CancellationToken ct` **last**.

```csharp
/// <summary>Manages portfolio products.</summary>
[ApiController]
[Route("api/products")]
public sealed class ProductsController(ISender sender) : ControllerBase
```

---

## Method shape

### Documentation

- Controller + every action: one-line `/// <summary>`, **verb first**, abstract — the route + HTTP verb are on the attributes, don't restate them. See [../code-style/documentation.md](../code-style/documentation.md).
- **The action's summary verb mirrors the method stem** — present-3rd-person of the method name + object. Never `Lists` / `Returns` / `Retrieves`; the verb is always the stem.

| Method | `<summary>` |
|---|---|
| `Get` | `Gets all {plural}.` |
| `GetById` | `Gets a {singular} by id.` |
| `Create` | `Creates a {singular}.` |
| `UpdateById` | `Updates a {singular}.` |
| `DeleteById` | `Deletes a {singular}.` |

```csharp
// ✅  /// <summary>Gets a single product by id.</summary>
// ❌  /// <summary>Returns the product with the given id including all embedded relations and live state.</summary>
```

### Attributes

`[ProducesResponseType]` on **every** action — typed for success, bare for the error statuses the action can emit. .NET 10 generic form preferred. These attributes sit directly above the method signature.

| Attribute | Use | Example |
|---|---|---|
| `[ProducesResponseType<T>(status)]` | typed success body — `T` is the `ApiResponse<...>` returned | `[ProducesResponseType<ApiResponse<ProductDto>>(StatusCodes.Status200OK)]` |
| `[ProducesResponseType(status)]` | error / no-body statuses (no payload type) | `[ProducesResponseType(StatusCodes.Status404NotFound)]` |
| `[Consumes(mediaType)]` | constrain the request body type — only when non-JSON or worth pinning | `[Consumes(MediaTypeNames.Multipart.FormData)]` |
| `[Tags("…")]` | group actions in the spec under a custom tag (override the controller-name default) | `[Tags("Codes")]` |
| `[EndpointSummary("…")]` | one-line operation summary in the spec (.NET 10 — pairs with / replaces the XML `<summary>`) | `[EndpointSummary("List all products")]` |
| `[EndpointDescription("…")]` | longer operation description when the summary isn't enough | `[EndpointDescription("Returns every product owned by the caller.")]` |

- **Always:** one typed `[ProducesResponseType<ApiResponse<T>>(200)]` (or `201`) + one bare `[ProducesResponseType(status)]` per failure the action returns (commonly `400` / `404` / `409`).
- `[Consumes]` only when it adds signal — multipart uploads, `text/plain` bodies; skip it for the default JSON case.
- `[Tags]` / `[EndpointSummary]` / `[EndpointDescription]` are optional polish — reach for them when the generated spec needs a clearer name or grouping.
- **Not used:** output-cache, OData, or API-versioning attributes — out of scope for our stack.

### Name — id-suffix

`api/{noun}` is plural; an `{id}` route param → a `ById` suffix. These five names are fixed.

| HTTP + route | Method |
|---|---|
| `GET api/products` | `Get` |
| `GET api/products/{id}` | `GetById` |
| `POST api/products` | `Create` |
| `PUT api/products/{id}` | `UpdateById` |
| `DELETE api/products/{id}` | `DeleteById` |

- `Get` for the list — not `List` / `GetAll`. Never bare `Update` / `Delete` when the route carries `{id}`.
- Non-CRUD actions name the verb + sub-resource (`SetActiveById`, `GetImageById`) — same `ById` rule.

### Return type

- Every action returns `Task<IActionResult>` — **never** `ActionResult<T>`.
- One return type covers JSON, `NoContent`, `Problem`, and `File`/streaming alike — a `File(bytes, contentType)` action is still `IActionResult`.

---

## Method content

### No business logic

- **No `try/catch`** — handlers own their failures and return an `AppResult` failure; an uncaught throw falls through to the host's global handler → 500 ([problem-details.md](problem-details.md)).
- No data access, no mapping, no orchestration in the action — build the request, send, map. Everything else is the handler's job.

### Mediator dispatch

- Send the request via `ISender.SendAsync(request, ct)` (see [../messaging/mediator.md](../messaging/mediator.md)); `ct` is the **last** argument to `SendAsync`.

### Mapping — `AppResult.Match`

Collapse the [`AppResult`](../foundation/result-pattern.md) via `.Match(onSuccess, onFailure)` — success wrapped in `ApiResponse<T>` (see [response-models.md](response-models.md)), failure → `Problem`.

- **Block body, dispatch result saved to a local first** — never an expression body. A one-liner can't be breakpointed/inspected; the local lets you see `result` on the spot.

```csharp
/// <summary>Gets all registered products.</summary>
[HttpGet]
[ProducesResponseType<ApiResponse<IReadOnlyList<ProductDto>>>(StatusCodes.Status200OK)]
public async Task<IActionResult> Get(CancellationToken ct)
{
    var result = await sender.SendAsync(new GetProductsQuery(), ct);

    return result.Match<IActionResult>(
        ok => Ok(ApiResponse<IReadOnlyList<ProductDto>>.Ok(ok.Data.Products)),
        fail => Problem(detail: fail.Error.ErrorMessage, statusCode: ApiResults.ToStatusCode(fail.Error.Category)));
}

/// <summary>Creates a product.</summary>
[HttpPost]
[ProducesResponseType<ApiResponse<ProductDto>>(StatusCodes.Status201Created)]
[ProducesResponseType(StatusCodes.Status400BadRequest)]
public async Task<IActionResult> Create([FromBody] CreateProductRequest request, CancellationToken ct)
{
    var result = await sender.SendAsync(new CreateProductCommand(request.Slug, request.Name), ct);

    return result.Match<IActionResult>(
        ok => CreatedAtAction(nameof(GetById), new { id = ok.Data.Product.Id }, ApiResponse<ProductDto>.Ok(ok.Data.Product)),
        fail => Problem(detail: fail.Error.ErrorMessage, statusCode: ApiResults.ToStatusCode(fail.Error.Category)));
}

/// <summary>Deletes a product.</summary>
[HttpDelete("{id:guid}")]
[ProducesResponseType(StatusCodes.Status204NoContent)]
[ProducesResponseType(StatusCodes.Status404NotFound)]
public async Task<IActionResult> DeleteById(Guid id, CancellationToken ct)
{
    var result = await sender.SendAsync(new DeleteProductCommand(id), ct);

    return result.Match<IActionResult>(
        NoContent,
        fail => Problem(detail: fail.Error.ErrorMessage, statusCode: ApiResults.ToStatusCode(fail.Error.Category)));
}
```

- Each arm receives the **case object**, not a deconstructed DTO and not an `(error, message)` tuple — success arm reaches `ok.Data` (then the container's DTO field) / `ok.Context`; failure arm reaches `fail.Error` / `fail.Context`. `.Match<IActionResult>(...)` — annotate `TOut` so both arms unify.
- Two `onSuccess` shapes: `Func<AppResult<…>.Success, TOut>` (case object) for queries/creates; `Func<TOut>` (no arg) for void commands → `NoContent()`.

**Success mapping**

| Outcome | Return |
|---|---|
| List / single read | `Ok(ApiResponse<T>.Ok(dto))` |
| Created (resource has an id) | `CreatedAtAction(nameof(GetById), new { id }, ApiResponse<T>.Ok(dto))` |
| Mutated, no body | `NoContent()` |
| Binary / stream | `File(bytes, contentType)` |

- `CreatedAtAction` always points at `nameof(GetById)` with the new `{ id }` — the `Location` header round-trips to the read action.
- `T` is always a DTO; `ApiResponse<T>` never wraps another envelope — see [response-models.md](response-models.md).

**Failure mapping — `Problem`**

- Failure arm is always `Problem(detail: fail.Error.ErrorMessage, statusCode: ApiResults.ToStatusCode(fail.Error.Category))` — never bare `NotFound()` / `Conflict()` / `BadRequest()`.
- `ApiResults.ToStatusCode(FailureCategory)` is the single app-side category→status map; the controller never inlines a status literal for a failure. `IFailureResult` carries **no** `StatusCode` — the `Category` lives on the product's `I{App}Failure` and the failure→HTTP mapping stays product-side here (category pattern → [result-pattern.md](../foundation/result-pattern.md)). RFC-7807 wiring lives in [problem-details.md](problem-details.md).
- `fail.Error` is the typed `I{App}Failure` off the `AppResult` `.Failure` case ([result-pattern.md](../foundation/result-pattern.md)); reach its `ErrorMessage` for the detail and `.Category` for the status map.
