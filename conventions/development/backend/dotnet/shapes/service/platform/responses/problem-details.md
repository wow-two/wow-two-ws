# ProblemDetails

*Last updated: 2026-10-02*

> RFC 9457 errors at the HTTP boundary.

## Wire contract

- must return a `ProblemDetails` object with `application/problem+json` for every writable HTTP `4xx` or `5xx` response, including endpoint, middleware, proxy and framework failures.
- must set `status` to the HTTP status and provide a stable `type`, safe `title`, and request correlation identifiers.
- must retain field errors in `ValidationProblemDetails` or the shared application validation extension.
- must normalize empty status responses and existing string or alternate JSON error bodies at their owning boundary.
- must cover malformed requests, validation, authentication, authorization, missing routes, unsupported methods, rate limits and unhandled exceptions.
- must provide a JSON fallback when the client's `Accept` header does not select the default problem writer.
- must preserve `WWW-Authenticate`, `Retry-After`, `Allow`, correlation and cache-control headers while writing the error body.
- must keep `HEAD` bodyless and respect an already-started response or disconnected client; those boundaries cannot safely acquire a replacement body.
- must verify representative error contracts through HTTP tests, including an incompatible `Accept` header and middleware-generated failures.

---

## Factory

- must build an application failure through `AppErrorProblemDetailsFactory.Create`.
- must share that factory between controller failure arms and global exception handlers.
- must obtain status through `IErrorHttpStatusCodeMapper`, never an inline status literal.
- must obtain display text through `IErrorMessageMapper` and field text through `IFieldErrorMessageMapper`.
- may override those mapping seams through DI.
- must emit `code` from the `AppErrorType` name and `type` as `urn:wow-two:error:{Type}`.
- must include `errors` entries with `property`, `code` and `message` from `ValidationError` and aggregate validation failures.
- must promote reserved metadata `retryAfter` and `wwwAuthenticate` to their HTTP headers.
- must not emit `Origin`, raw internal exception messages or stack traces to the client.

---

## Pipeline

- must register `AddHttpProblemDetails()` and activate `UseHttpProblemDetails()` before product middleware; service registration alone does not handle requests.
- must compose that opt-in boundary alongside [startup defaults](../startup/startup-defaults.md); keep policy registration in the host composition root.
- must enrich error responses with `traceId` and `requestId` through `AddTraceAwareProblemDetails`.
- must order `ValidationExceptionHandler`, `AppExceptionHandler`, and `UnhandledExceptionHandler` in that order.
- must use the [mediator bridge](results.md#throw-and-return-bridge) for exceptions inside its supported scope.
- must leave middleware, filters and non-mediator failures to the HTTP handlers.
- must backfill framework error codes through the shared `CustomizeProblemDetails` path.
- must not create a separate error payload in a controller or exception handler.
- must replace development exception HTML/text on API routes with the same safe problem contract; detailed diagnostics stay in server logs.
