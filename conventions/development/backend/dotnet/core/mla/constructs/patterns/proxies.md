# Proxies

*Last updated: 2026-09-10*

> A stand-in that carries an interface's calls to a real implementation living somewhere else.
> Purpose — let a caller depend on a plain interface while the transport, the generation or the hook stays invisible.
> Use case — reach here when the implementation is generated or intercepted rather than written.

## Shape

- must take a proxy from a source that generates it — Refit for an HTTP API (`AddRefitApiClient<TApi>`,
  `src/Http/Refit/`).
- must declare the interface the proxy implements as ours, and keep it free of the generator's attributes where the
  generator allows it.
- must not hand-write a runtime proxy — no `DispatchProxy`, no IL emit, no dynamic-proxy package.
- EF save interception → [EF mapping](../../domains/persistence/access/ef/ef-mapping.md); it is a callback, not a proxy.

```csharp
// ✅ the interface is the contract, Refit generates the implementation
public interface IBillingApi
{
    [Post("/v1/payment-intents")]
    Task<PaymentIntentResponse> CreateIntentAsync(CreateIntentRequest request, CancellationToken cancellationToken);
}

builder.Services.AddRefitApiClient<IBillingApi>("https://billing.internal");
```

---

## Use

- must reach for a generated proxy for a typed HTTP client — it is the default over a hand-written one
  ([client](../behavior/client.md)).
- may reach for a lazy proxy only where the framework supplies it and the cost is measured.

---

## Limits

- must not use a proxy to hide a network call from the caller — an interface that can time out says so in its shape
  (`Async`, `CancellationToken`).
- must not enable EF lazy-loading proxies — an N+1 that fires from a property read is invisible at the call site.
- must not proxy what a decorator already covers — a hand-written wrapper is readable, a generated one is not
  ([decorators](decorators.md)).

---

## Components

- [client](../behavior/client.md) — Refit registration, resilience, and the typed-client alternative.
- [entity](../data/entity.md) — the audit / soft-delete / tenant traits the interceptors act on.
- [decorators](decorators.md) — the hand-written wrapper, when the added behavior needs a name.
