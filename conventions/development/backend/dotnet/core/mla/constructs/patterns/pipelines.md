# Pipelines

*Last updated: 2026-09-10*

> An ordered set of steps wrapping one call, each free to run before, after, or instead of the next.
> Purpose — declare cross-cutting behavior once, in one visible order, instead of nesting it per call site.
> Use case — reach here when three or more behaviors must run around every call of the same kind.

## Shape

- must declare the order at registration, and treat **registration order as execution order** — the first registered
  wraps the rest ([mediator](../../domains/messaging/mediator/mediator.md) § *Pipeline behaviors*).
- must call the next step **exactly once** to continue, and short-circuit by not calling it at all.
- step roles and names → [interceptors](../behavior/interceptor.md) · [constructs](../constructs.md).
- must give each step one concern.
- must keep a step generic in the message it wraps; a step that inspects one concrete request is a handler's job.
- must name a step's opt-in marker as the capability it gates — `IIdempotent`, `IRequireAuthorization`.

```csharp
// ✅ one concern, next called once, short-circuit by returning without it
public sealed class LoggingInterceptor<TRequest, TResponse> : IRequestInterceptor<TRequest, TResponse>
    where TRequest : notnull
{
    public async ValueTask<TResponse> HandleAsync(
        TRequest request,
        RequestHandlerDelegate<TResponse> nextStep,
        CancellationToken cancellationToken)
    {
        TResponse response = await nextStep();
        return response;
    }
}
```

---

## Use

- must reach for a mediator behavior for anything every request needs — logging, validation, authorization,
  idempotency, exception-to-result.
- must reach for ASP.NET middleware for anything the **transport** owns — correlation ids, exception handling, CORS.
- must reach for our own `Pipeline` + `PipelineStep` only for a domain flow with named stages the user can see.

---

## Limits

- must not put a business rule in a pipeline step — a step that knows one use case has moved a handler upward.
- must not source caller context in a pipeline; the actor is merged at the edge into the application request
  ([api context building](../../domains/api/api-context-building.md)).
- must not call `nextStep()` twice — the retry it looks like belongs to the resilience pipeline
  ([circuit breaker](circuit-breaker.md)).
- must not nest a hand-written wrapper chain where a pipeline exists — two decorators are the ceiling
  ([decorators](decorators.md)).

---

## Components

- [mediator](../../domains/messaging/mediator/mediator.md) — `IRequestInterceptor<,>`, `AddMediatorBehavior`,
  the built-in set.
- [validator](../behavior/validator.md) — the validation step and what it throws.
- [handler](../behavior/handler.md) — what the pipeline wraps: one message, one handler.
- [decorators](decorators.md) — the one-wrap sibling, when the behavior applies to a single interface.
