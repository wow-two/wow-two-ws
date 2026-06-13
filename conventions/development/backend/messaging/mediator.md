# Mediator

*Last updated: 2026-06-13*

In-process request/response + fan-out via the SDK mediator. Use-cases are `IRequest<TResponse>` with one handler; cross-cutting concerns are `INotification` (many handlers) or `IPipelineBehavior<TRequest,TResponse>`. SDK source: `wow-two-sdk.backend.beta/src/Mediator/`.

## Contracts

Two message shapes. One handler per request; N handlers per notification.

| Message | Marker | Handler | Cardinality |
|---|---|---|---|
| Use-case (returns a value) | `IRequest<TResponse>` | `IRequestHandler<TRequest,TResponse>` | exactly 1 |
| Use-case (no value) | `IRequest` (= `IRequest<Unit>`) | `IRequestHandler<TRequest>` (= `IRequestHandler<TRequest,Unit>`) | exactly 1 |
| Domain event / fan-out | `INotification` | `INotificationHandler<TNotification>` | 0..N |

- A void use-case returns `Unit` — never `Task`/`void`. Return `Unit.Value` (or `Unit.Task`); `Send(IRequest)` dispatches as `Send<Unit>` under the hood.
- `IRequestHandler<,>.Handle` and `INotificationHandler<>.Handle` both take `(message, CancellationToken)` and return `Task<TResponse>` / `Task`.
- One application use-case = one request type + one handler. Don't reuse a request across handlers — that's what `INotification` is for.

## Dispatch — inject the abstraction

Never inject the concrete `Mediator`. Pick the narrowest abstraction:

| Inject | Method | Use in |
|---|---|---|
| `ISender` | `Send<TResponse>(IRequest<TResponse>, ct)` / `Send(IRequest, ct)` | controllers, handlers issuing a sub-request |
| `IPublisher` | `Publish<TNotification>(TNotification, ct)` | raising domain events |
| `IMediator` (= `ISender` + `IPublisher`) | both | only when a type genuinely needs both |

- Controllers dispatch via `ISender.Send` then map the result — see [../presentation/controllers.md](../presentation/controllers.md) (`ISender.Send` + `Result.Match`).
- `Publish` invokes notification handlers **sequentially** in registration order; a throwing handler aborts the rest. Don't assume isolation/parallelism.

## Registration — scan, don't hand-wire

Call `AddMediator(assembly)` **once per handler-bearing assembly** (typically the Application layer). It registers `IMediator`/`ISender`/`IPublisher` and scans for closed implementations of `IRequestHandler<,>` and `INotificationHandler<>` — binding each to its interface as transient.

```csharp
services.AddMediator(typeof(SomeApplicationMarker).Assembly);
```

- Handlers are discovered, never registered by hand. Adding a handler = adding the class; no DI edit.
- Parameterless `AddMediator()` scans `Assembly.GetCallingAssembly()` — pass the assembly explicitly when wiring from a different layer (e.g. composition root).
- `IMediator`/`ISender`/`IPublisher` use `TryAdd` — safe to call across assemblies; the mediator binds once.

## Cross-cutting — pipeline behaviors

Cross-cutting logic wrapping every request is an `IPipelineBehavior<TRequest,TResponse>` (open generic). Register with `AddMediatorBehavior(typeof(X<,>))`.

> **Registration order = execution order.** Behaviors stack outermost-first in the order registered (first registered runs first / wraps the rest). Order matters — register logging before validation if you want failed validations logged.

```csharp
services
    .AddMediatorLoggingBehavior()       // outermost — wraps everything
    .AddMediatorValidationBehavior()    // throws before the handler on invalid input
    .AddMediatorIdempotencyBehavior();  // dedup marked requests
```

Built-ins (each = `AddMediatorBehavior(typeof(<Behavior><,>))`):

| Extension | Behavior | Opt-in marker | Effect |
|---|---|---|---|
| `AddMediatorLoggingBehavior` | `LoggingBehavior<,>` | — (all requests) | logs request name + elapsed ms; failures at `Error` |
| `AddMediatorValidationBehavior` | `ValidationBehavior<,>` | — (`IValidator<TRequest>` present) | runs `IValidator<T>.ValidateAndThrow`, throws on invalid |
| `AddMediatorIdempotencyBehavior` | `IdempotencyBehavior<,>` | `IIdempotent` | dedups by `IIdempotent.IdempotencyKey`, caches + replays the response |
| `AddMediatorAuthorizationBehavior` | `AuthorizationBehavior<,>` | `IRequireAuthorization` | ASP.NET Core authz; throws `UnauthorizedAccessException` / `AuthorizationException` |

- **Idempotency:** a request opts in by implementing `IIdempotent` (`string IdempotencyKey`). First call runs + stores via `IIdempotencyStore`; repeats with the same key replay the cached response. `AddMediatorIdempotencyBehavior` wires the single-instance `InMemoryIdempotencyStore` — swap in a distributed `IIdempotencyStore` for multi-instance. TTL via `IdempotencyBehavior<,>.Ttl` (default 24h). Requests without the marker pass through untouched.
- **Authorization:** `IRequireAuthorization.PolicyName` (nullable → default policy); `AddMediatorAuthorizationBehavior` also wires `AddHttpContextAccessor()` + `AddAuthorization()`.
- Custom behavior: implement `IPipelineBehavior<TRequest,TResponse>` (`where TRequest : notnull`), call `next()` to continue, register via `AddMediatorBehavior(typeof(Yours<,>))`.

## See also

- [../presentation/controllers.md](../presentation/controllers.md) — controllers dispatch via `ISender.Send`, map with `Result.Match`
- [../foundation/result-pattern.md](../foundation/result-pattern.md) — `Result<T>` as the handler return carrier
- [../code-style/documentation.md](../code-style/documentation.md) — XML doc format for handlers/behaviors
- [backend-conventions.md](../backend-conventions.md) — backend sub-domain index
