# Controllers

*Last updated: 2026-06-17*

> API Controllers documentation.

## Controller shape

### Documentation

- Controller documentation should include summary and remark

#### Summary

- See [baseline summary docs](../code-style/documentation.md)
- resource controllers, keyword - `Manages {resource}`, e.g. `Manages products.`
- non-resource controllers (status / health), keyword - `Reports {what}`, e.g. `Reports the vault's seal state.`
- mustn't spill details, like where the endpoints are used, is there any supportive controller etc

#### Remarks

- optional — a load-bearing caveat that won't fit the one-line summary (e.g. a data-plane gate covering every action)
- omit on most controllers; never restate the summary

### Attributes

- `[ApiController]` - declare as an API controller
- `[Route("api/{noun}")]` - declare the literal route, with kebab-case, e.g. `[Route("api/products")]`

### Declaration

- must be non-inheritable - `sealed`
- must inherit - `ControllerBase`
- must have plural or resource / process matching noun name - e.g. `ProductsController`, `IdentityController`
- must use primary ctor

### Dependencies

- may inject a caller-context accessor or other helper dependencies
- must inject [mediator components](../messaging/mediator.md) for application-layer communication
- must not inject services, repositories, validators directly

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

- See [baseline summary docs](../code-style/documentation.md)
- must not restate HTTP verbs
- must state the action - e.g. `Sends the given message`, `Sets the x status y`
- must use specified verbs for the standard CRUD actions :

| Method       | `<summary>`                |
|--------------|----------------------------|
| `Get`        | `Gets all {plural}.`       |
| `GetById`    | `Gets a {singular} by id.` |
| `Create`     | `Creates a {singular}.`    |
| `UpdateById` | `Updates a {singular}.`    |
| `DeleteById` | `Deletes a {singular}.`    |

  - load-bearing caveat → `<remarks>`

```csharp
// ✅  /// <summary>Gets a single product by id.</summary>
// ❌  /// <summary>Returns the product with the given id including all embedded relations and live state.</summary>
```

### Attributes

- must have `[ProducesResponseType]` - 
- must have `[ProducesResponseType<T>(status)]` - 
- must have `[ProducesResponseType(status)]` - 
- must have `[Consumes(mediaType)]` - 
- must have `[Tags("…")]` - 
- must have `[EndpointSummary("…")]`
- must have `[EndpointDescription("…")]`

### Naming

- must have plural resource / process name - e.g. - 
- must use suffixes that makes the method distinct if needed - e.g. `Create` -> `CreateTimedToken`, `CreateSlidingToken`
- must use specified names for the standard CRUD actions :

| HTTP + route               | Method       |
|----------------------------|--------------|
| `GET api/products`         | `Get`        |
| `GET api/products/{id}`    | `GetById`    |
| `POST api/products`        | `Create`     |
| `PUT api/products/{id}`    | `UpdateById` |
| `DELETE api/products/{id}` | `DeleteById` |


### Shape

- See (baseline method docs)[insert baseline method docs here for no-lambda body etc]

### Return type

- must return `Task<IActionResult>`, unless it's a streaming or specific response

---

## Method content

### API Request binding

- must use [api request models](request models link) to bind request payload
- must use the [`ICurrentUser`](need to build api-context-building.md and add link here) for user context
- must use `User` / `HttpContext` for other things that are not supported by the `ICurrentUser`

### Cancellation

- must take and pass down a `CancellationToken`

### Application request mapping

- each request declares it's own mapping method for a correct application request ( mapping extension method link)
- must use that mapping method to build the application request

### No business logic

- must delegate any business logic into internal components, for application requests - using [mediator components](../messaging/mediator.md)
- must not have exception catching, validation, orchestration, manual mapping
- must use existing mapping logic for success or failure results and return without branching
- must save the result into a variable instead of doing request mapping, mediator call and return in a single line

### Response model mapping 

- muse use - .Match - need to rewrite **Block body** — save the dispatch result in a local first, then `.Match` on it ([members.md](../code-style/members.md)).
- for [Application Result](insert application result link) - must  

### Response mapping

**Success mapping**

| Outcome                      | Return                                                                 |
|------------------------------|------------------------------------------------------------------------|
| List / single read           | `Ok(ApiResponse<T>.Ok(dto))`                                           |
| Created (resource has an id) | `CreatedAtAction(nameof(GetById), new { id }, ApiResponse<T>.Ok(dto))` |
| Mutated, no body             | `NoContent()`                                                          |
| Binary / stream              | `File(bytes, contentType)`                                             |

- `CreatedAtAction` always points at `nameof(GetById)` with the new `{ id }` — the `Location` header round-trips to the
  read action.
- `T` is always a DTO; `ApiResponse<T>` never wraps another envelope — see [response-models.md](response-models.md).

**Failure mapping — `Problem`**

- must use `ProblemDetails` for failures that must have context, not bare `NotFound()` / `Conflict()` / `BadRequest()`
- `ApiResults.ToStatusCode(FailureCategory)` is the single app-side category→status map; the controller never inlines a
  status literal for a failure. `IFailureResult` carries **no** `StatusCode` — the `Category` lives on the product's
  `I{App}Failure` and the failure→HTTP mapping stays product-side here (category
  pattern → [result-pattern.md](../foundation/result-pattern.md)). RFC-7807 wiring lives
  in [problem-details.md](problem-details.md).
- `fail.Error` is the typed `I{App}Failure` off the `AppResult` `.Failure`
  case ([result-pattern.md](../foundation/result-pattern.md)); reach its `ErrorMessage` for the detail and `.Category`
  for the status map.

#### Good

- include all necessary attributes in the examples :

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
// ❌ try/catch · expression body, no local · raw DTO without ApiResponse · bare helper, not Problem + category
[HttpPost]
public async Task<IActionResult> Create(CreateProductCommand command, CancellationToken ct)
{
    try { return Ok(await sender.SendAsync(command, ct)); }
    catch (NotFoundException) { return NotFound(); }
}
```

---

## Known endpoints

Identity and system endpoints have **fixed, cross-app names** — don't invent per-app variants (`auth/login`,
`admin/session`).

- Identity → `IdentityController` at `api/identity`: `sign-in` · `sign-out` · `me` · `guest` (· `sign-up` · `refresh` ·
  `callback` where the app has them). Summary `Manages identity.`
- System → `SystemController` at `api/system`: `status`. Non-resource → verb-first summary (`Reports …`).
- An app implements only the capabilities it has; the **name and path are canonical**, the HTTP verb may vary by
  mechanism (OAuth challenge `GET sign-in` vs credential `POST sign-in`).
- Full table + per-mechanism notes + legacy-controller
  migration → [controllers-known-endpoints.md](controllers-known-endpoints.md).
