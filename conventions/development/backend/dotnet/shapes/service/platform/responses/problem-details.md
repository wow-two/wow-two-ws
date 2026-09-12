# ProblemDetails

*Last updated: 2026-09-10*

> RFC 9457 errors at the HTTP boundary.

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

- must register the shared HTTP error pipeline through [startup defaults](../startup/startup-defaults.md).
- must enrich error responses with `traceId` and `requestId` through `AddTraceAwareProblemDetails`.
- must order `ValidationExceptionHandler`, `AppExceptionHandler`, and `UnhandledExceptionHandler` in that order.
- must use the [mediator bridge](results.md#throw-and-return-bridge) for exceptions inside its supported scope.
- must leave middleware, filters and non-mediator failures to the HTTP handlers.
- must backfill framework error codes through the shared `CustomizeProblemDetails` path.
- must not create a separate error payload in a controller or exception handler.
