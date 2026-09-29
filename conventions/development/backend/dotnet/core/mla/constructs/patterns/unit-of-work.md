# Unit of work

*Last updated: 2026-09-26*

> One transactional boundary around every change a use-case makes, committed once at its end.
> Purpose — keep the commit point at the use-case, so a partial write is impossible rather than merely unlikely.
> Use case — reach here when a handler writes more than one row and both writes must land together.

## Shape

- must use `DbContext` for EF tracking and flushing; `SaveChangesAsync` commits only when no explicit transaction owns the flush.
- must not declare an `IUnitOfWork` interface wrapping it; the wrapper adds a name and hides the tracker
  ([database](../../domains/persistence/database/database.md)).
- must give the use-case one commit boundary when several writes must succeed together.
- may use one `SaveChangesAsync` call when the complete operation remains tracked in one context.
- must open an explicit unit when combining eager repository writes, multiple flushes, EF and raw SQL, or commit callbacks.
- must opt into `AddDataSession<TContext>()` for SDK transaction coordination; it retains the existing context and factory.
- must pass a session lease's connection and transaction together to Dapper.
- must keep direct factory operations autonomous; only participating session calls join the unit.
- must retain the SDK's eager repository flush behavior until a separate manual-flush contract is implemented.

```csharp
await using var unit = await session.BeginAsync(ct);
await orders.CreateAsync(order, ct);
await inventory.ReserveAsync(order.Items, ct);
await unit.CompleteAsync(ct);
```

---

## Use

- must reach for the pattern in a command handler writing more than one aggregate.
- must reach for it when an outbox row must commit with the state change ([outbox](outbox.md)).
- must reach for an explicit transaction when a migration-time or admin operation spans several statements.

---

## Limits

- must distinguish repository flush from transaction commit: eager SDK writes flush inside the caller's explicit unit.
- must use an explicit unit for atomic multi-write use-cases; autonomous eager writes commit independently.
- must opt transactional mediator requests into `ITransactionalRequest`; register data units before deduplication.
- must reload tracked references after nested rollback; database savepoints do not restore CLR graphs.
- must not enable automatic execution-strategy retries for explicit sessions.
- must reconcile an uncertain commit before retrying; cleanup is not evidence of rollback.
- must use an outbox for durable external effects; completion callbacks are in-process and can be lost.
- must not span a transaction across an out-of-process call — a broker call inside one holds a lock on the network.
- must not share a `DbContext` across requests or across threads — it is scoped, and it is not thread-safe.
- must not use a transaction to make a query consistent; that is an isolation level, set deliberately.

---

## Components

- [repository](../behavior/repository.md) — the storage access seam.
- [database](../../domains/persistence/database/database.md) — the `DbContext` contract and the schema-first rule.
- [outbox](outbox.md) — the messaging half that must share the same commit.
- [handler](../behavior/handler.md) — the handler that owns the boundary.
