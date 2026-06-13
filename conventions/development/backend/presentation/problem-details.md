# ProblemDetails

*Last updated: 2026-06-13*

API error responses are RFC-7807 `ProblemDetails` — registered once via the SDK, never hand-built in endpoints or handlers.

## Registration

`AddTraceAwareProblemDetails` (`src/Web/ProblemDetails/ProblemDetailsServiceCollectionExtensions.cs`) wraps the built-in `AddProblemDetails` and enriches every payload through `CustomizeProblemDetails`:

| Extension | `ProblemDetails.Extensions` key | Source |
|---|---|---|
| `traceId` | `System.Diagnostics.Activity.Current?.Id` | active trace span |
| `requestId` | `HttpContext.TraceIdentifier` | per-request id |

Both keys are set automatically — handlers never populate them. `AddApiDefaults` (`src/meta/ApiDefaultsExtensions.cs`) calls `AddTraceAwareProblemDetails` then `AddValidationExceptionHandler` as part of the P1 boot floor, so a `Program.cs` on the SDK defaults gets correlated ProblemDetails with no extra wiring.

## Validation → 400

A thrown `ValidationException` (`src/foundation/Validation/ValidationException.cs`, namespace `WoW.Two.Sdk.Backend.Beta.Validation`) maps to a 400 `ValidationProblemDetails` via `ValidationExceptionHandler` (`src/Web/ExceptionHandling/ValidationExceptionHandler.cs`), an `IExceptionHandler` registered by `AddValidationExceptionHandler` (`src/Web/ExceptionHandling/ExceptionHandlingServiceCollectionExtensions.cs` → `AddExceptionHandler<ValidationExceptionHandler>`).

- `ValidationException.Errors` (`IReadOnlyList<ValidationError>`) is grouped by `ValidationError.Property` into the `ValidationProblemDetails(errors)` dictionary; values are the `ValidationError.Message` strings per property.
- `Status` = `StatusCodes.Status400BadRequest`; `Title` = `"One or more validation errors occurred."`.
- The handler returns via `IProblemDetailsService.TryWriteAsync` — so the same `traceId` / `requestId` enrichment applies.

`ValidationError.Code` (the stable machine-readable rule id) is **not** emitted by the current handler — only `Property` + `Message` reach the response.

## Rules

- **Never hand-build error payloads** in endpoints or handlers — no `new ProblemDetails(...)`, no manual `BadRequest(obj)`. Throw `ValidationException` for input failures; return a `DomainError` failure for everything else.
- **`DomainError` → ProblemDetails** is a presentation-layer concern, not an SDK converter: `DomainError.StatusCode` (derived from `DomainErrorCategory`, see [result-pattern.md](../foundation/result-pattern.md)) feeds the controller's `Problem(detail:, statusCode:)` call — see [controllers.md](controllers.md) (`Result.Match` → `Problem()`). The SDK ships no `DomainError.ToProblemDetails()`; the mapping lives in the controller via the app-side `ApiResults.ToStatusCode`.
- **Unhandled throws** that aren't `ValidationException` fall through `ValidationExceptionHandler` (`TryHandleAsync` returns `false`) to the host's global handler → 500 ProblemDetails.

## See also

- [result-pattern.md](../foundation/result-pattern.md) — `DomainError` / `DomainErrorCategory` → HTTP status
- [controllers.md](controllers.md) — `Result.Match` → `Problem()` mapping in thin controllers
