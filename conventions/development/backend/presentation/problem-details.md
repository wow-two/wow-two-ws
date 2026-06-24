# ProblemDetails

*Last updated: 2026-06-22*

> API error responses are RFC 9457 `ProblemDetails`, built once by the shared factory and never hand-rolled. Code: `src/Web/ExceptionHandling/`, `src/Web/ErrorMapping/`.

## The factory — one builder, every path

`AppErrorProblemDetailsFactory.Create(error, httpContext, statusMapper, messageResolver)` is the single builder, used by **both** the controller failure-arm (`.Match`) and the global exception handlers. It:

- sets `status` (via `IErrorHttpStatusCodeMapper`), `detail` (via `IErrorMessageResolver`), `code` (= `error.Type`), `type` (`urn:wow-two:error:{Type}`).
- emits `errors:[{property,code,message}]` for a `ValidationError` / `AppAggregateError` — `FieldError.Code` now reaches the wire.
- promotes reserved `Metadata` keys to response headers — `retryAfter`→`Retry-After`, `wwwAuthenticate`→`WWW-Authenticate`.
- **never** emits `AppError.Origin`.

## Status mapping

`IErrorHttpStatusCodeMapper.ToStatusCode(AppError) → int` — SDK `DefaultErrorHttpStatusCodeMapper` keyed on `AppErrorType`; apps register their own to override. Returns `int` (admits non-standard codes, e.g. `Canceled`→499).

## Pipeline — `AddApiDefaults` → `AddAppExceptionHandling`

- `AddTraceAwareProblemDetails` — enriches every payload with `traceId` (`Activity.Current?.Id`) + `requestId` (`HttpContext.TraceIdentifier`).
- chained `IExceptionHandler`s: `ValidationExceptionHandler` (400 + `errors[]`) → `AppExceptionHandler` (any `AppException`) → `UnhandledExceptionHandler` (500, no internal leak).
- **the mediator never throws** for `AppResult` requests — `ExceptionToResultBehavior` converts to a `Failure`; controllers `.Match` → the factory. The handlers are the **outside-mediator** path (middleware, filters, non-mediator code).
- framework errors (route 404/405, model-binding 400) get `code` backfilled from the status via `CustomizeProblemDetails`.

## Rules

| | Rule |
|---|---|
| must | build error responses via `AppErrorProblemDetailsFactory` — never `new ProblemDetails(...)` / `BadRequest(obj)` |
| must | status comes from `IErrorHttpStatusCodeMapper`, never an inline literal |
| must not | emit `Origin`, raw exception messages, or stack traces to the client |
| may | apps override the status mapper / message resolver / nature classifier via DI |

## See also

- [result-pattern.md](../foundation/result-pattern.md) · [validation.md](../foundation/validation.md) · [controllers.md](controllers.md)
