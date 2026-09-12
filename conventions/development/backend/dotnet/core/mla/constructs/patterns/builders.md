# Builders

*Last updated: 2026-09-10*

> A type that accumulates a configuration across calls and closes it into one immutable value.
> Purpose — keep a many-optioned construction out of the constructor overload set and out of the caller.
> Use case — reach here when a value carries more optional parts than a constructor can express readably.

## Shape

- declaration and name → [builder](../behavior/builder.md).
- must close `EventSagaBuilder` into `EventSagaDefinition` (`src/Messaging/EventSaga/EventSagaBuilder.cs`).
- must return the builder from every configuring call, and close on a single terminal `Build()`.
- must return an immutable value from `Build()` — a `sealed record`, or `init`-only members.
- must validate in `Build()`, not per call — a half-configured chain stays legal until it closes.
- must keep the builder mutable and single-use; a builder is not a `Settings` record and never binds config.

```csharp
// ✅ the chain accumulates, Build closes it
public sealed class EventSagaBuilder
{
    public EventSagaBuilder Step<TStep>() where TStep : IEventSagaStep { _stepTypes.Add(typeof(TStep)); return this; }

    public EventSagaDefinition Build()
    {
        return new EventSagaDefinition(
            _name,
            _stepTypes.AsReadOnly(),
            _destinations.AsReadOnly());
    }
}
```

---

## Use

- must reach for a builder when the order of the parts is part of the meaning — a saga's steps, a pipeline's stages.
- must reach for it when a registration extension hands the caller a configuration surface — `Action<TBuilder>`.
- may reach for it in tests to assemble a fixture, where the alternative is a long positional constructor.

---

## Limits

- must not build a value an object initializer already expresses — `new Foo { A = 1, B = 2 }` needs no builder.
- must not use a builder for config binding — that is `Settings` via `IOptions<T>`
  ([settings](../../components/settings.md)).
- must not let `Build()` reach out-of-process; a builder assembles a value, it does not run work.
- must not expose a builder as a DI service — it is constructed at the call site and dropped.

---

## Components

- [factories](factories.md) — the sibling: a `Factory` picks *which* type, a `Builder` assembles *one* value.
- [settings](../../components/settings.md) — config-bound records, never assembled through a builder.
- [pipelines](pipelines.md) — the common consumer, where step order is what the builder fixes.
