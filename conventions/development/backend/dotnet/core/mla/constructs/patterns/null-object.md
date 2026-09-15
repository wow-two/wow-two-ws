# Null object

*Last updated: 2026-08-19*

> An implementation that satisfies a contract by doing nothing, registered where the real one is absent.
> Purpose — keep the null check out of every caller, so an unconfigured capability is a registration, not a branch.
> Use case — reach here when a capability is optional and its absence must change nothing at the call site.

## Shape

- must prefix the type `NoOp` and keep the contract's noun — `NoOpMessagingMetrics`
  (`src/Messaging/MessagingMetrics.cs`), `NoOpMigrationRunner`
  (`src/Testing.Data/Migrations/NoOpBespokeMigrator.cs`), `NoopGeoBroker`
  (`forever-pin/…/ForeverPin.Redirect.Api/Infrastructure/Routing/`).
- must return the contract's defined empty value — `null` for a lookup, an empty sequence, a completed task —
  never throw.
- must state in `<remarks>` what replaces it, because a no-op is a placeholder and the reader must know the swap
  — *"Swap in MaxMind GeoLite2 to make country rules match."*
- must register it like any implementation, in `HostConfiguration.Extensions.cs`, so the swap is one line.
- must stay behaviourless: no logging beyond a single startup line, no counters, no config.

```csharp
// ✅ the contract is satisfied, the absence is a registration
/// <summary>Provides the no-op geo lookup that resolves no country.</summary>
/// <remarks>Swap in MaxMind GeoLite2 to make country rules match.</remarks>
public sealed class NoopGeoBroker : IGeoBroker
{
    public string? ResolveCountry(string? ipAddress) => null;
}
```

---

## Use

- must reach for a null object when a capability is genuinely optional — metrics, geo enrichment, a webhook log.
- must reach for it to keep a seam declared before its implementation exists, so callers are written once.
- must reach for it in tests where the real collaborator is irrelevant to the assertion.

---

## Limits

- must not use a null object for a **domain** outcome — a missing order is a `Failure(AppError)`, not a blank entity
  ([result](../data/result.md)).
- must not use one where the absence must be visible — a no-op cipher or a no-op authenticator hides a security hole.
- must not let a null object stand in production for a capability the product promises; it is a default, not a decision.
- must not swallow an argument a real implementation would reject — the no-op keeps the contract's guards.

---

## Components

- [broker](../behavior/broker.md) — the usual seam a no-op fills before the provider lands.
- [result](../data/result.md) — where a *domain* absence is expressed instead.
- [host configuration](../../../../shapes/service/platform/startup/host-configuration.md) — the one-line swap.
- [strategies](strategies.md) — a no-op is the degenerate strategy, and it is registered the same way.
