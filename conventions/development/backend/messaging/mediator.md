# Mediator

*Last updated: 2026-06-14*

> In-process request/response mediator component conventions.
> Purpose — decouple presentation from infrastructure so a use-case is dispatched, not called directly.
> Use case — between the presentation and infrastructure layers; not for infrastructure-to-infrastructure calls.

## Queries, Commands, Events and their Handlers

### Common

- A **query, command and event are all request messages** — declared, named and handled separately for separation of concerns. Query = read, command =
  write, event = fan-out fact ("X happened").
- **Naming** — `{Domain}{Action}[{Meta}]{Kind}`, **domain-first, singular** (`Code`, `Product`, `Channel` — not `Codes`) so related types sort
  together. Action mirrors the controller method stem.
- **Shape** — messages = `public sealed record` (carry inputs as members); handlers = `public sealed class`.
- **Cardinality** — a query and a command have **exactly one** handler each; an event has **0..N** handlers.
- SDK markers rebase onto `IRequest` / `INotification`; SDK handler interfaces refine `IRequestHandler` / `INotificationHandler` — same DI scan, same
  pipeline, no extra wiring.
- **Result** — result-carrying requests return `AppResult<TSuccess, TFailure>` as their `TResult` — construction, shape and `.Match` collapse in
  [result-pattern.md](../foundation/result-pattern.md). Cannot-fail: a value type directly (query) or no value (`ICommand`, returns `Unit`).

### Query

- **Marker** — `IQuery<TResult>` (invariant — result type fixed per query)
- **Handler** — `IQueryHandler<TQuery,TResult>`
- **Verb** — `GET`
- **Location** — `Application/{Domain}/Queries/`
- **Example** — `CodeGetByIdQuery`

### Command

- **Markers** — `ICommand` (no value) / `ICommand<TResult>` (value)
- **Handlers** — `ICommandHandler<TCommand>` / `ICommandHandler<TCommand,TResult>`
- **Verbs** — `POST` `PUT` `PATCH` `DELETE`
- **Location** — `Application/{Domain}/Commands/`
- **Examples** — `CodeSetActiveCommand` (no value) · `CodeCreateCommand` (value)

### Events

> Document now, deferred use — uses what the SDK mediator already offers.

- **Marker** — `INotification`
- **Handler** — `INotificationHandler<TEvent>` (0..N)
- **Raised via** — `IPublisher.PublishAsync` — sequential, registration order; a throwing handler aborts the rest
- **Location** — `Application/{Domain}/Events/`
- **Example** — `CodeCreatedEvent` (naming `{Domain}{Action}Event`)

### Comments

XML doc summaries — byte-identical to the SDK marker source. No `<example>` blocks (go stale).

- **Definition** (SDK markers / handler interfaces) → `Defines …` — e.g. `Defines a query that returns TResult` ·
  `Defines a handler for the TQuery query`. Keep `<typeparam>` lines.
- **Message** (concrete query/command/event) → `Represents a {query/command/event} to {action}` — e.g. `Represents a query to get all channels`.
- **Handler** (concrete) → `Handles <see cref="{Request}"/>.`

---

## Registration & usage

`AddMediator(assembly)` **once per handler-bearing assembly** (typically Application) — registers `IMediator`/`ISender`/
`IPublisher` (`TryAdd`, safe across assemblies) + scans closed `IRequestHandler<,>`/`INotificationHandler<>` as
transient. Adding a handler = adding the class; no DI edit. Parameterless overload scans
`Assembly.GetCallingAssembly()` — pass explicitly from a different layer.

Never inject concrete `Mediator`. Pick the narrowest abstraction:

| Inject                                   | Method      | Use in                                      |
|------------------------------------------|-------------|---------------------------------------------|
| `ISender`                                | `SendAsync`    | controllers, handlers issuing a sub-request |
| `IPublisher`                             | `PublishAsync` | raising domain events                       |
| `IMediator` (= `ISender` + `IPublisher`) | both        | only when a type genuinely needs both       |

- **Dispatch** — `ISender.SendAsync` — strongly-typed `IRequest<TResponse>` overload returns `ValueTask<TResponse>`; no-response `IRequest` overload returns `ValueTask<Unit>`. Events → `IPublisher.PublishAsync` (`ValueTask`). Handlers implement `HandleAsync`.
- Controllers dispatch via `ISender.SendAsync` then `.Match` — see [../presentation/controllers.md](../presentation/controllers.md).
- A query/command **is** an `IRequest<T>`, so `SendAsync` binds to it natively — no extension layer.

---

## Pipeline behaviors

Cross-cutting logic wrapping every request = `IPipelineBehavior<TRequest,TResponse>` (open generic,
`where TRequest : notnull`); implement `HandleAsync(request, RequestHandlerDelegate<TResponse> nextStep, ct)` and `await nextStep()`
**exactly once** to continue. Register via `AddMediatorBehavior(typeof(X<,>))`.

> **Registration order = execution order.** First registered runs first / wraps the rest. Register logging before
> validation to log failed validations.

Built-ins (each = `AddMediatorBehavior(typeof(<Behavior><,>))`):

| Extension                          | Behavior                   | Opt-in marker                      | Effect                                                                              |
|------------------------------------|----------------------------|------------------------------------|-------------------------------------------------------------------------------------|
| `AddMediatorLoggingBehavior`       | `LoggingBehavior<,>`       | — (all)                            | logs request name + elapsed ms; failures at `Error`                                 |
| `AddMediatorValidationBehavior`    | `ValidationBehavior<,>`    | — (`IValidator<TRequest>` present) | `IValidator<T>.ValidateAndThrow`, throws on invalid                                 |
| `AddMediatorIdempotencyBehavior`   | `IdempotencyBehavior<,>`   | `IIdempotent`                      | dedups by `IdempotencyKey`, caches + replays response                               |
| `AddMediatorAuthorizationBehavior` | `AuthorizationBehavior<,>` | `IRequireAuthorization`            | ASP.NET Core authz; throws `UnauthorizedAccessException` / `AuthorizationException` |

- **Idempotency:** opt in via `IIdempotent.IdempotencyKey`. First call stores via `IIdempotencyStore` (wires
  single-instance `InMemoryIdempotencyStore` — swap a distributed store for multi-instance); repeats replay. TTL via
  `IdempotencyBehavior<,>.Ttl` (default 24h). Unmarked requests pass through.
- **Authorization:** `IRequireAuthorization.PolicyName` (nullable → default policy); also wires
  `AddHttpContextAccessor()` + `AddAuthorization()`.
