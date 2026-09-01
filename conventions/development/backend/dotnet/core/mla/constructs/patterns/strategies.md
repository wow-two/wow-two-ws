# Strategies

*Last updated: 2026-08-19*

> One interface with interchangeable implementations, the one in force chosen at composition rather than at the call.
> Purpose — keep a swappable decision out of a `switch` that every caller would have to repeat.
> Use case — reach here when the same operation has two or more correct algorithms and the environment picks.

## Shape

- must declare a narrow interface naming the decision, carrying the role the decision serves —
  `IOutboxClaimRepository` (`src/Messaging/Reliability/Ef/OutboxDispatcher.cs`), implemented by the
  skip-locked and the unlocked-read variants.
- must name each implementation for **how** it decides, never for the caller that happens to use it.
- must bind exactly one implementation per host, in `HostConfiguration.Extensions.cs` — composition picks, not runtime.
- must resolve a per-key choice through a `Registry` or a `Factory`, never a `switch` inside the consumer
  ([registry](../behavior/registry.md) · [factories](factories.md)).
- must ship a second implementation with the first — a one-implementation interface is not a strategy, it is a seam.

```csharp
// ✅ the interface names the decision, the host picks the implementation
public interface IOutboxClaimStrategy
{
    Task<IReadOnlyList<OutboxMessageEntity>> ClaimPendingAsync(
        DbContext context, int batchSize, CancellationToken cancellationToken);
}
```

---

## Use

- must reach for a strategy when the provider decides — a Postgres path and a portable fallback.
- must reach for it when a policy is tuned per deployment — a retry policy, a header-propagation policy.
- must reach for it when a test needs a deterministic stand-in for a nondeterministic algorithm.

---

## Limits

- must not create a strategy for a branch that never varies per host — that is a private method.
- must not name a strategy `{Consumer}Strategy`; the name would go stale the first time a second consumer arrives.
- must not let a strategy carry state across calls — state belongs to the type that owns the flow.
- must not coin the `Strategy` suffix for a type that reaches out-of-process; that is a `Broker`
  ([components](../constructs.md) § *Adding a new suffix*).

---

## Components

- [registry](../behavior/registry.md) — when the choice is per key rather than per host.
- [factories](factories.md) — when the choice is per call and depends on a runtime value.
- [host configuration](../../../../shapes/service/platform/startup/host-configuration.md) — where the binding is declared.
- [swappable modules](../../../../../../swappable-modules.md) — the packaged form: contract, adapters, one suite.

---

## Naming

- must not suffix the type `Strategy` — swappability is a shape, and a suffix names a responsibility
  ([components](../constructs.md) § *Banned*).
- must name the type for what it decides or produces.
  - `Policy` for a decision, `Mapper` for a value, `Service` for work.
- the pattern stays in use; only its name as a suffix is refused.
