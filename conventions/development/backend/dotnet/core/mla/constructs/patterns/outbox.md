# Outbox

*Last updated: 2026-09-10*

> A message staged as a row in the same transaction as the state change, published after that transaction commits.
> Purpose — remove the dual write: a state change and its event either both land or neither does.
> Use case — reach here when a handler both writes rows and publishes an event another service acts on.

## Shape

- must stage through `IOutbox.EnqueueAsync` inside the business transaction — the row and the state change share one
  `SaveChangesAsync` (`src/Messaging/Reliability/MessagingReliability.cs`).
- must register the EF-backed outbox with `AddEfOutbox<TContext>`, map it with `modelBuilder.ApplyOutboxModel()`, and
  own the `outbox_messages` DDL in a migration ([migrations](../../domains/persistence/migrations/migrations.md)).
- must dispatch out of band — `AddEfOutboxDispatcher<TContext>` runs the drain, never the request thread.
- must pair the outbox with an **inbox** on the consuming side — `AddEfInbox<TContext>`, `IInboxProcessor` — because
  at-least-once delivery means a duplicate arrives.
- must claim rows through an `IOutboxClaimRepository`; scale-out takes `PostgresSkipLockedOutboxClaimRepository`, a single
  instance takes the polling default ([strategies](strategies.md)).
- must prune processed rows on a retention window — `PruneProcessedAsync`, not a manual cleanup script.

```csharp
// ✅ the row and the staged message share one commit
context.Orders.Add(order);
OutboxRecord message = new()
{
    Id = id,
    Type = typeName,
    Payload = payload,
    OccurredOnUtc = occurredOnUtc,
    Headers = headers,
};
await outbox.EnqueueAsync(message, ct);
await context.SaveChangesAsync(ct);
```

---

## Use

- must reach for an outbox whenever a commit and a publish must agree — an order placed, a payment settled.
- must reach for it when the broker is a separate process, whatever the broker is; the failure mode is the transport's,
  not the vendor's.
- must reach for the inbox half whenever a consumer's handler is not naturally idempotent.

---

## Limits

- must not publish directly from a handler that also writes rows — that is the dual write the pattern removes.
- must not treat the outbox as a queue for in-process work; a background job is a `BackgroundService`
  ([background service](../behavior/background-service.md)).
- must not stage a large payload — store it and stage the pointer (claim check).
- must not assume ordering across rows; a consumer that needs a sequence carries it on the message.
- must not use an outbox for a mediator notification inside one process — `IPublisher` already runs in the same scope
  ([mediator](../../domains/messaging/mediator/mediator.md)).

---

## Components

- [handler](../behavior/handler.md) — the event staged, and the handler that consumes it.
- [entity](../data/entity.md) — `OutboxMessageEntity` / `InboxMessageEntity` are rows, with the same key contract.
- [unit of work](unit-of-work.md) — the transaction the staging rides inside.
- [sagas](sagas.md) — the consumer of last resort when the flow spans several services.
