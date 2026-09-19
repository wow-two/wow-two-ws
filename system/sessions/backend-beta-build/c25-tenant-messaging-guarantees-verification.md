# C25 tenant and messaging guarantees verification

*Last updated: 2026-09-16*

## Result

C25 is complete. Tenant-owned EF and generated Dapper CRUD now use the ambient tenant as the server-authoritative read/write scope. Messaging retains at-least-once transport semantics, atomically commits durable inbox markers with same-context effects, bounds in-process queues and retry budgets, preserves failed outbox evidence, and fixes claim-check rehydration at the innermost interceptor position.

## Tenant scope

- `TenancyConventionOptions` enables authenticated-claim resolution by default. Route, header and subdomain sources require explicit opt-in.
- `TenantIdService` resolves claim → route → header → subdomain, preventing an enabled client header from overriding the authenticated claim.
- `TenantResolutionMiddleware` clears ambient state before resolution and in `finally`, including exceptional request exits.
- `ApplyTenantFilter` restricts EF reads for `IHasTenant<string>` while a tenant is present.
- `TenantStampInterceptor` overwrites inserted tenant ids, reads the stored tenant before update/delete, rejects cross-tenant writes and preserves the authoritative tenant column.
- `DapperRepository<TEntity,TId>` now stamps tenant-owned inserts/updates and adds the current tenant predicate to every generated read, update and delete.
- No ambient tenant means an explicit system/admin scope. Hand-written SQL remains responsible for its own tenant predicate.

## Messaging guarantees

- Every broker adapter feeds the shared `EventProcessingPipeline`; logical `MessageId` remains the inbox key across redelivery.
- Transport delivery is documented as at-least-once. The SDK no longer calls the inbox/outbox path true exactly-once.
- `InMemoryInboxProcessor` serializes concurrent duplicates per message id and releases its per-message gate after the final waiter.
- `EfInboxProcessor` inserts the inbox marker and commits same-context handler effects in one transaction. A database exception counts as a duplicate only when the marker is proven to exist; other provider failures propagate unchanged.
- `EfOutbox` stages rows in the caller transaction. `UnlockedOutboxClaimRepository` remains single-instance; `PostgresSkipLockedOutboxClaimRepository` owns multi-instance row claims.
- Outbox dispatch is at-least-once across the publish/stamp crash window. Exhausted rows retain their error and successful-row pruning excludes them.
- Retry budgets, delayed retry and dead-letter settlement remain bounded. Host-shutdown cancellation bypasses retry and dead-letter classification.
- `InMemoryEventChannel` and `MessagePump` use bounded channels with wait-mode backpressure.
- `EventProcessingPipeline` always moves `ClaimCheckRehydratingConsumeInterceptor` closest to dispatch, independent of registration order.

## Verification

- `dotnet build WoW.Two.Sdk.Backend.Beta.slnx --no-restore -m:1`: passed, 0 errors.
- `Data.Tests`: 27 passed, 0 failed.
- `Web.Tests`: 63 passed, 0 failed.
- `Messaging.Tests`: 122 passed, 0 failed, 1 intentionally skipped Kafka integration case.
- Focused Dapper tenant scope: 1 passed.
- Focused web tenant resolution/lifetime: 2 passed.
- Focused concurrent in-memory inbox dedupe: 1 passed.

## Retained provider limits

- In-memory inbox state lasts only for the process lifetime; it cannot make external effects atomic.
- EF inbox atomicity covers effects written through the same `TContext` transaction. External effects require their own idempotency or an outbox.
- The default unlocked outbox claim is single-instance only. PostgreSQL scale-out requires `ReplaceWithPostgresSkipLockedOutboxClaim<TContext>()`.
- Per-database, per-schema and Finbuckle tenancy remain deferred in `Tenancy.md`.
