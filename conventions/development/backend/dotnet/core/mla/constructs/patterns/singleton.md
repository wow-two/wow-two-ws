# Singleton

*Last updated: 2026-09-10*

> One instance per process, owned by the container rather than by the type.
> Purpose — keep the single-instance decision at the composition root, where it can be changed and tested.
> Use case — reach here when a type is stateless, thread-safe and expensive to construct.

## Shape

- must express a singleton as a **DI lifetime**, registered in `HostConfiguration.Extensions.cs`
  ([host configuration](../../../../shapes/service/platform/startup/host-configuration.md)).
- must not declare a static `Instance` property, a private constructor, or a `Lazy<T>` self-holder.
- must be thread-safe when registered singleton — a singleton is entered concurrently by every request.
- static eligibility and forms → [constructs](../constructs.md) § *Static or instance*.

```csharp
// ✅ the container owns the lifetime
services.AddSingleton<IQrMatrixGenerator, QrMatrixGenerator>();

// ❌ the type owns it, and no test can replace it
public sealed class QrMatrixGenerator
{
    public static QrMatrixGenerator Instance { get; } = new();
}
```

---

## Use

- must register singleton for a stateless, thread-safe collaborator — a mapper, a generator, a cipher.
- must register singleton for a type holding process-wide state deliberately — a `Registry`, a `Tracker`.
- must register singleton for a connection factory, which pools underneath — `DataSourceConnectionFactory`.

---

## Limits

- must not register singleton anything holding a `DbContext`, a request identity, or a tenant — those are scoped.
- must not capture a scoped service in a singleton constructor.
- may create and dispose a scope per operation when the singleton owns that operation's lifetime.
- must keep every scoped value inside the operation that resolved it → [service locator](service-locator.md).
- must not use the lifetime as a cache — a cache is a named collaborator with an eviction policy.
- must not reach a singleton through a static accessor once registered; inject its interface.

---

## Components

- [host configuration](../../../../shapes/service/platform/startup/host-configuration.md) — where every lifetime is declared.
- [service](../behavior/service.md) — the lifetime table per service kind.
- [registry](../behavior/registry.md) · [ambient context](ambient-context.md) — the two types most often
  mistaken for a static singleton.
