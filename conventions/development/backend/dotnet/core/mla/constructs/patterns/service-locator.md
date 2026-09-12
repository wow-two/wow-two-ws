# Service locator

*Last updated: 2026-09-10*

> Resolving a collaborator from the container at the point of use instead of taking it through the constructor.
> Purpose — record why this is banned, and the three places a container reference is still legitimate.
> Use case — reach here when a type is about to inject `IServiceProvider`.

## Shape

- constructor injection → [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.
- must not inject `IServiceProvider` into a service, a handler, a controller, or a repository.
- must not call `GetRequiredService` from inside a member whose type could have declared the dependency.
- must not reach a collaborator through a static container accessor or a `ServiceLocator` type — neither exists here,
  and neither may be introduced.

```csharp
// ✅ the constructor states the dependency
public sealed class CodeCreateCommandHandler(ICodeRepository codes, IOutbox outbox) { }

// ❌ the dependency is invisible until the line runs
public sealed class CodeCreateCommandHandler(IServiceProvider services) { }
```

---

## Use

Three exceptions, and nothing else:

- must allow it at the **composition root** — `HostConfiguration.Extensions.cs` builds the graph, so it holds the provider
  ([host configuration](../../../../shapes/service/platform/startup/host-configuration.md)).
- may use `IServiceScopeFactory` when a long-lived consumer owns a bounded operation.
- must dispose that operation's scope before returning, including on cancellation and failure.
- host-run operations → [background work](../../../../shapes/service/platform/startup/host-configuration.md#background-work).
- must allow resolution inside a `Factory` that dispatches on a runtime key — that dispatch is the factory's whole
  reason to exist ([factories](factories.md)).

---

## Limits

- must not treat a factory-delegate registration as a licence to resolve elsewhere; the delegate runs at the root.
- must not retain scoped state between operations; resolve within each operation's scope instead.
- singleton lifetime selection → [singleton](singleton.md).
- must not resolve an optional dependency conditionally; register a no-op instead ([null object](null-object.md)).
- must not keep a resolved instance past the scope that produced it — a captured `DbContext` outlives its transaction.

---

## Components

- [factories](factories.md) — the sanctioned per-key resolution, and its shape.
- [background service](../behavior/background-service.md) — the scope-per-iteration rule.
- [host configuration](../../../../shapes/service/platform/startup/host-configuration.md) — the only layer holding the provider by design.
- [ambient context](ambient-context.md) — the sibling: a hidden value rather than a hidden dependency.
