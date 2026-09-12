# Results

*Last updated: 2026-09-10*

> The outcome boundary between service handlers and HTTP controllers.

## Carriers

- must choose shared carriers through [result application](../../../../core/mla/components/result.md).
- must return `AppResult<TSuccess>` from application `IQueryHandler` and `ICommandHandler` implementations.
- must map an inner `Result<T>` into `AppResult<TSuccess>` in the handler.
- must map each typed failure to a catalog `AppError` at that handler boundary.
- must collapse the controller's `AppResult` with `.Match(onSuccess, onFailure)`.
- must translate failure arms through [problem details](problem-details.md).
- must not return HTTP results, DTOs or bare `Unit` from an application handler.
- may attach `IAppSuccessContext` or `IAppFailureContext` for cross-cutting response metadata.

---

## Throw and return bridge

- must apply the shared [failure policy](../../../../core/mla/components/result.md) to expected failures and guards.
- must install `ExceptionMappingInterceptor` through the SDK mediator registration when conversion is enabled.
- must keep the converter outermost around the request interceptors it protects.
- must limit the conversion guarantee to supported exceptions entering a result-capable request pipeline.
- must not promise conversion for failures during handler resolution or pipeline construction.
- must not promise conversion when the caller disabled the interceptor or the response has no failure arm.
- must preserve programmer/process-error exclusions; a `NullReferenceException` is not an expected failure.
- must distinguish caller cancellation from timeout using the request token.
- must preserve the original cause when a framework boundary requires converting a failure back to an exception.
- must route exceptions outside the mediator through the HTTP [exception handlers](problem-details.md#pipeline).
