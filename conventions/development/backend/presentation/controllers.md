# Controllers

*Last updated: 2026-06-17*

> API Controllers documentation.

## Controller shape

### Documentation

#### Summary

- see [baseline summary docs](../code-style/documentation/summary.md)
- resource controllers, keyword - `Manages {resource}`, e.g. `Manages products.`
- non-resource controllers (status / health), keyword - `Reports {what}`, e.g. `Reports the vault's seal state.`
- mustn't spill details — where the endpoints are used, whether a supporting controller exists, etc.

### Attributes

- `[ApiController]` - declare as an API controller
- `[Route("api/{noun}")]` - declare the literal route, kebab-case, e.g. `[Route("api/products")]`

### Declaration

- must be non-inheritable - `sealed`
- must inherit - `ControllerBase`
- must have a plural resource / process noun name - e.g. `ProductsController`, `IdentityController`
- must use a primary ctor

### Dependencies

- may inject a caller-context accessor or other helper dependencies
- must inject [mediator components](../messaging/mediator.md) for application-layer communication
- must not inject services, repositories, or validators directly

### Examples

#### Good

```csharp
/// <summary>Manages portfolio products.</summary>
[ApiController]
[Route("api/products")]
public sealed class ProductsController(ISender sender) : ControllerBase
```

#### Bad

```csharp
// ❌ not sealed · `[controller]` token route · injects a repo, not the mediator · summary spills detail
/// <summary>Controller that exposes all product endpoints used by the dashboard and the public API.</summary>
[ApiController]
[Route("api/[controller]")]
public class ProductsController(IProductRepository repository) : ControllerBase
```

---

## Method shape

### Documentation

#### Summary

- see [baseline summary docs](../code-style/documentation/summary.md)
- must not restate the HTTP verb
- must state the action - e.g. `Sends the given message.`, `Sets the code's active state.`
- must use the specified verbs for standard CRUD actions:

| Method       | `<summary>`                |
|--------------|----------------------------|
| `Get`        | `Gets all {plural}.`       |
| `GetById`    | `Gets a {singular} by id.` |
| `Create`     | `Creates a {singular}.`    |
| `UpdateById` | `Updates a {singular}.`    |
| `DeleteById` | `Deletes a {singular}.`    |

### Attributes

- must have `[ProducesResponseType<ApiResponse<T>>(2xx)]` - the one typed success body
- must have `[ProducesResponseType(status)]` per failure it returns - `400` / `404` / `409`, no payload type
- may have `[Consumes(mediaType)]` - constrain a non-JSON body, e.g. a multipart upload
- may have `[Tags("…")]` - regroup the action in the spec
- may have `[EndpointSummary("…")]` / `[EndpointDescription("…")]` - spec text when the generated name needs help

### Naming

- bare verb for the controller's resource - the resource is implied, e.g. `Create`, not `CreateProduct`
- add a suffix only to distinguish variants or a nested resource - `CreateTimedToken`, `CreateSlidingToken`, `GetTokens`
- must use the specified names for standard CRUD actions:

| HTTP + route               | Method       |
|----------------------------|--------------|
| `GET api/products`         | `Get`        |
| `GET api/products/{id}`    | `GetById`    |
| `POST api/products`        | `Create`     |
| `PUT api/products/{id}`    | `UpdateById` |
| `DELETE api/products/{id}` | `DeleteById` |

### Shape

- see [baseline method docs](../code-style/members.md)

### Return type

- must return `Task<IActionResult>`, unless it's a streaming or otherwise specific response

---

## Method content

### API request binding

- must bind the payload via an [api request model](request-models.md)
- must read the actor through [`ICurrentUser`](api-context-building.md) for user context
- must use `User` / `HttpContext` only for facts `ICurrentUser` doesn't expose

### Cancellation

- must take and pass down a `CancellationToken`, last

### Application request mapping

- each api request declares its own [mapping method](request-models.md) to its application request
- must build the application request via that mapping method

### No business logic

- must delegate business logic to internal components — for application requests, via [mediator components](../messaging/mediator.md)
- must not catch exceptions, validate, orchestrate, or hand-map
- must save the dispatch result to a local — never request-map, send, and return on one line

### Response mapping

- must `.Match` the saved result ([members.md](../code-style/members.md))
- for [`AppResult`](../foundation/result-pattern.md) - collapse via `.Match(onSuccess, onFailure)`: success → `ApiResponse<T>.Ok(dto)`, failure → `Problem(...)`

**Success mapping**

| Outcome                      | Return                                                                 |
|------------------------------|------------------------------------------------------------------------|
| List / single read           | `Ok(ApiResponse<T>.Ok(dto))`                                           |
| Created (resource has an id) | `CreatedAtAction(nameof(GetById), new { id }, ApiResponse<T>.Ok(dto))` |
| Mutated, no body             | `NoContent()`                                                          |
| Binary / stream              | `File(bytes, contentType)`                                             |

- `CreatedAtAction` points at `nameof(GetById)` with the new `{ id }` — the `Location` header round-trips to the read action
- `T` is always a DTO; `ApiResponse<T>` never wraps another envelope ([response-models.md](response-models.md))

**Failure mapping — `Problem`**

- must map a failure to `Problem(...)` with context, never bare `NotFound()` / `Conflict()` / `BadRequest()`
- status comes from `ApiResults.ToStatusCode(fail.Error.Category)` — the single app-side category→status map; never inline a status literal ([result-pattern.md](../foundation/result-pattern.md))
- `fail.Error` is the typed `I{App}Failure` — reach `.ErrorMessage` (detail) + `.Category` (status); RFC-7807 wiring → [problem-details.md](problem-details.md)

### Examples

#### Good

```csharp
/// <summary>Creates a product.</summary>
[HttpPost]
[ProducesResponseType<ApiResponse<ProductDto>>(StatusCodes.Status201Created)]
[ProducesResponseType(StatusCodes.Status400BadRequest)]
public async Task<IActionResult> Create([FromBody] CreateProductCommand command, CancellationToken ct)
{
    var result = await sender.SendAsync(command, ct);

    return result.Match<IActionResult>(
        ok => CreatedAtAction(nameof(GetById), new { id = ok.Data.Product.Id }, ApiResponse<ProductDto>.Ok(ok.Data.Product)),
        fail => Problem(detail: fail.Error.ErrorMessage, statusCode: ApiResults.ToStatusCode(fail.Error.Category)));
}
```

#### Bad

```csharp
// ❌ summary spills detail · try/catch · expression body, no local · raw DTO without ApiResponse · bare helper, not Problem + category
/// <summary>Returns the created product including all its embedded relations.</summary>
[HttpPost]
public async Task<IActionResult> Create(CreateProductCommand command, CancellationToken ct)
{
    try { return Ok(await sender.SendAsync(command, ct)); }
    catch (NotFoundException) { return NotFound(); }
}
```
