# Result pattern

*Last updated: 2026-06-22*

> Every handler and endpoint returns a result carrying a typed success **or** an `AppError`. Two carriers, one error model. Code: `src/Mediator/Result/`, `src/Foundation/Results/`, `src/Foundation/Errors/`.

## Carriers

| Carrier | Use | Shape |
|---|---|---|
| `Result` / `Result<T>` | everywhere (domain / service / foundation / infra) | `Success` \| `Failure(AppError)` — lightweight, no context |
| `AppResult<TSuccess>` | mediator handlers ↔ controllers | `Success(TSuccess Data, ctx?)` \| `Failure(AppError Error, ctx?)` |

- both are **closed DUs** (private ctor + sealed nested cases); `where T : notnull` / `where TSuccess : notnull` → non-null, side-owned (no `bool IsSuccess; T?`, no null-checks).
- collapse with `.Match(onSuccess, onFailure)` — the mandated consume path.
- an inner `Result<T>` (service) maps up into an `AppResult<TSuccess>` in the handler.

## `AppError` — the one failure value

`AppError(AppErrorType Type, string Message, IReadOnlyDictionary<string,object?>? Metadata = null) { ErrorOrigin? Origin }` — open `record` (subclassed by `ValidationError`, `AppAggregateError`).

- **must** author errors via a catalog — SDK `AppErrors.{Kind}(...)`, app `OrderErrors.*` — never `new AppError { … }` at a call site.
- **must not** put an HTTP status on the error — `AppErrorType` is transport-agnostic; status maps at the edge ([problem-details.md](../presentation/problem-details.md)).
- `Type` (name) is the wire `code`; `Origin` is log-only (never serialized); `Metadata` carries message args + reserved header keys.

## Rules

| | Rule |
|---|---|
| must | every `IQueryHandler` / `ICommandHandler` returns `AppResult<TSuccess>`; controllers `.Match` it |
| must | failures travel as `AppError` (or a subtype) — never a bare string, exception, or per-op flag across the boundary |
| must not | `Ok(dto)` / `return dto` / `return Unit` from a handler; `DomainError` / `FailureCategory` / `I{App}Failure` / `ISuccessResult` / `IFailureResult` (all removed) |
| may | attach `Success.Context` / `Failure.Context` (`IAppSuccessContext` / `IAppFailureContext`) for cross-cutting metadata |

## Throw ⇄ return bridge

A failure is expressible either way over the **same** `AppError`: `error.Throw()` · `result.ValueOrThrow()` · `result.ThrowIfFailure()` · `(() => op()).Attempt()` (catch → `Result`). The mediator **never throws** for `AppResult` requests — `ExceptionToResultBehavior` converts a throw to a `Failure` ([problem-details.md](../presentation/problem-details.md)).

## See also

- [validation.md](validation.md) · [problem-details.md](../presentation/problem-details.md) · [controllers.md](../presentation/controllers.md) · [mediator.md](../messaging/mediator.md)
