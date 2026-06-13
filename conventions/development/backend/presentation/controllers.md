# Controllers

*Last updated: 2026-06-13*

> **Draft — for review.** Controller conventions for the current **Result + MediatR** pattern (Drydock / secrets-vault). [`api-endpoints.md`](api-endpoints.md) documents an older `ApiResponse<T>` envelope variant — reconcile the two during polish.

Controllers are **thin dispatchers**: build a request → `ISender.Send` → `Match` the `Result` to HTTP. No business logic, no data access, no try/catch.

## Shape

- **`ControllerBase`** (never `Controller` — no views), `sealed`.
- **`[ApiController]`** + **`[Route("api/{resource}")]`** — lowercase plural resource (`api/products`).
- **Primary-constructor injection of `ISender`** only.
- One controller per resource; every action takes a trailing `CancellationToken ct`.

## Method naming — mirrors the route

The method name states the operation; **an `{id}` route param adds a `ById` suffix.**

| Operation | HTTP + route | Method |
|---|---|---|
| List all | `GET api/products` | **`Get`** |
| One by id | `GET api/products/{id}` | **`GetById`** |
| Create | `POST api/products` | **`Create`** |
| Update by id | `PUT api/products/{id}` | **`UpdateById`** |
| Delete by id | `DELETE api/products/{id}` | **`DeleteById`** |

- **`Get`**, not `List` / `GetAll` — the unqualified read *is* the list.
- Never bare `Get` / `Update` / `Delete` when the route carries `{id}` — suffix it `ById`.

## Returning a Result

`Send` the request, then **`Match`** the `Result` — success → the right 2xx, error → `Problem()` (RFC 7807) via the shared `ApiResults.ToStatusCode`.

```csharp
/// <summary>Gets all products.</summary>
[HttpGet]
public async Task<IActionResult> Get(CancellationToken ct)
{
    var result = await sender.Send(new ListProductsQuery(), ct);
    return result.Match<IActionResult>(
        dtos => Ok(dtos),
        (error, message) => Problem(detail: message, statusCode: ApiResults.ToStatusCode(error)));
}
```

- **Success** → `Ok(dto)` (read), `CreatedAtAction(nameof(GetById), new { id }, dto)` (create), `NoContent()` (delete / no-body update).
- **Error** → always `Problem(detail: message, statusCode: ApiResults.ToStatusCode(error))`. Never bare `NotFound()` / `BadRequest()` / `Conflict()` — the `ResultError` → status mapping owns it.
- **No try/catch** — handlers return `Result`; an unexpected throw hits the global handler → 500.

## Documentation

- **Controller** → one-line `/// <summary>` naming the resource it manages.
- **Each action** → one-line `/// <summary>`, **verb first**, abstract — route + verb are already on the attributes; don't restate them or list impl detail that goes stale.

```csharp
// ✅ /// <summary>Gets a product by id.</summary>
// ❌ /// <summary>Returns the product row from SQLite by its GUID primary key.</summary>
```

## See also

- [result-pattern.md](../foundation/result-pattern.md) — `Result` / `ResultError` modeling
- [api-endpoints.md](api-endpoints.md) — request / handler (CQRS) naming
- [documentation.md](../code-style/documentation.md) — XML doc starter table
