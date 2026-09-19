# Messaging

*Last updated: 2026-09-13*

> Dispatching a message to its handlers without binding the message to its transport.

## Contract

- must bind exactly one handler to a command or query and zero or more handlers to an event.
- must carry every input on the message; collaborators arrive through the handler's constructor.
- must dispatch through an abstraction, not a concrete dispatcher.
- must keep transport choice out of the message.
- message and handler definitions → [application request](../../constructs/data/application-request.md)
  and [handler](../../constructs/behavior/handler.md).

---

## Members

- must order application inputs as route id, body, caller context.
- must keep caller-context acquisition at the [edge](../api/api-context-building.md).
- must use [service result carriers](../../../../shapes/service/platform/responses/results.md)
  for mediator query/command handlers serving a controller.
- must name a returned application shape through the [model construct](../../constructs/data/model.md).
- must not make notification handlers return request/response carriers.

```csharp
public sealed record CodeGetByIdQuery : IQuery<AppResult<CodeModel>>
{
    /// <summary>Gets the identifier of the code to load.</summary>
    public required Guid Id { get; init; }
}
```

---

## Dispatch

- must use `ISender` for a request and `IPublisher` for an event when using the [mediator](mediator/mediator.md).
- must not compose a command/query handler by dispatching another command/query through the mediator.
- must extract shared work into an injected [service](../../constructs/behavior/service.md) and call that service from each handler.
- must not bypass this rule by directly invoking another handler or hiding nested request dispatch behind a service.
- must keep required validation and permission checks in the shared operation's contract; extracting work must not silently drop checks previously supplied by a child request's pipeline.
- must keep the composition's transaction ownership explicit; a reused service must not silently commit the caller's unit of work.
- must treat this as a request-composition rule; event publication follows its declared event and delivery contract, including the outbox when required.

Shared services reuse the operation without entering a second request interception pipeline. Nested request
dispatch can repeat validation, authorization and transaction interceptors, making their ordering depend on
the handler call graph. WoW2 chooses explicit service composition for this work.

---

## Delivery

- must treat transport delivery as at-least-once, never claim transport-level exactly-once execution.
- must preserve logical message identity across redelivery.
- must make retried effects idempotent or commit the deduplication mark atomically with the effect.
- must use an outbox when publication must commit with a state change.
- must not classify host-shutdown cancellation as a failed handler delivery.
- must bound retries and route exhausted failures through the configured dead-letter policy.
- must apply backpressure rather than buffer unbounded pending work in the process.
- transport contract → [messaging standard](../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Messaging/Messaging.standard.md).

---

## Providers

- [mediator](mediator/mediator.md) — in-process request/response and notifications.
- event bus — transport-specific event delivery; no provider convention is declared here yet.
- [outbox](../../constructs/patterns/outbox.md) — stage in the state transaction and dispatch after commit.
