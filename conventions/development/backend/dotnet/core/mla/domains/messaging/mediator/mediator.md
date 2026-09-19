# Mediator

*Last updated: 2026-09-13*

> Applying the in-process mediator to requests, notifications and their interception pipeline.

## Messages

- must inherit the [messaging contract](../messaging.md#contract).
- must use `IQuery<TResult>` for reads and `ICommand<TResult>` for writes that return a value.
- must bind them to `IQueryHandler<TQuery, TResult>` or `ICommandHandler<TCommand, TResult>`.
- must use the service's [result carrier](../../../../../shapes/service/platform/responses/results.md)
  on query/command paths serving controllers.
- may use `ICommand` and its `Unit` response at a non-HTTP seam whose contract explicitly carries no value.
- must use `INotification` and `INotificationHandler<TEvent>` for fan-out events.
- must keep message naming, declaration and doc rules in [application requests](../../../constructs/data/application-request.md).
- must use [api messages](../../api/api-messages.md#requests) to choose direct binding or a separate wire body.

---

## Inputs

- must put replayable caller inputs on the request.
- must keep repositories, clocks and brokers in the handler's constructor.
- must acquire caller context through [api context building](../../api/api-context-building.md).
- must not read `ICurrentUser` or `HttpContext` inside a handler.

---

## Registration

- must register each handler-bearing assembly once through `AddMediator(assembly)`.
- must pass the assembly explicitly across a layer boundary; the parameterless overload scans its calling assembly.
- must inject `ISender` for requests, `IPublisher` for notifications, or `IMediator` only when both are needed.
- must use shared services for handler reuse under the domain's [dispatch policy](../messaging.md#dispatch); examples must not demonstrate handler-to-handler command/query sends.
- must account for sequential notification dispatch: a throwing handler stops later handlers.

---

## Interceptors

- must implement `IRequestInterceptor<TRequest, TResponse>` for owned request-pipeline steps.
- must register an open generic through `AddMediatorInterceptor(typeof(Interceptor<,>))`.
- must invoke the continuation exactly once on a path that continues; a terminating step may short-circuit.
- must register outside-to-inside: the first registered interceptor wraps subsequent ones.
- must call `AddMediator` before additional interceptors when using its default exception-mapping wrapper.
- must not assume the wrapper catches pre-dispatch failures or programmer errors.
- exception mapping scope → [service results](../../../../../shapes/service/platform/responses/results.md).

---

## Capabilities

- logging → `AddMediatorLoggingInterceptor()`.
- validation → `AddMediatorValidatingInterceptor()`, subject to [phase ordering](../../validation/validation.md#phases).
- deduplication → `AddMediatorDeduplicatingInterceptor()`, with `IIdempotent` and an appropriate repository.
- authorization → `AddMediatorAuthorizingInterceptor()`, with `IRequireAuthorization`.
- must use a shared durable idempotency store when duplicate requests can reach different instances.
- API and registration contracts → [mediator source](../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Mediator/MediatorServiceCollectionExtensions.cs).
