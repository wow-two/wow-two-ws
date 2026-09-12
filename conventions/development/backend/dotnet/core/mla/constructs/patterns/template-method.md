# Template method

*Last updated: 2026-09-10*

> An abstract base that fixes the order of a flow and leaves named hooks for the parts that vary.
> Purpose — keep an order that must not vary out of every subclass, where each one could get it wrong.
> Use case — reach here when the framework or the SDK already owns the flow and only the steps are ours.

## Shape

- must make an owned template base `abstract` and its fixed entry non-virtual; only hooks vary.
- must preserve an inherited framework entry contract when it requires an override.
- must suffix a hook with `Core` when it sits inside a member the framework already defines —
  `ConfigureConventionsCore` under EF's `ConfigureConventions` (`src/Data/EntityFrameworkCore/AppDbContextBase.cs`).
- must give a `virtual` hook a no-op default and an `abstract` hook none — the modifier states whether the step
  is optional.
- must document any inherited framework base-call obligation in `<remarks>` on the override.
- must make an owned template call its hooks itself, without an ordering obligation on subclasses.
- must suffix the base `Base` only when it is a test or scaffold base — a shipped base is named for what it is.

```csharp
// Framework entry from AppDbContextBase; Core is the extension hook.
protected override void ConfigureConventions(ModelConfigurationBuilder configurationBuilder)
{
    ArgumentNullException.ThrowIfNull(configurationBuilder);
    ConfigureConventionsCore(configurationBuilder);
    base.ConfigureConventions(configurationBuilder);
}

protected virtual void ConfigureConventionsCore(ModelConfigurationBuilder configurationBuilder)
{
}
```

---

## Use

- must reach for it where a framework base already imposes the shape — `BackgroundService.ExecuteAsync`
  ([background service](../behavior/background-service.md)), a `DbContext`, a test fixture.
- must reach for it when a step's default is *do nothing* and most subclasses will keep it.
- must reach for it in a testing harness, where the setup and teardown order is the contract
  ([testing](../../../../shapes/service/architecture/clean/testing.md)).

---

## Limits

- must prefer composition when the varying part could be injected — a `Strategy` beats a subclass, and it is testable
  alone ([strategies](strategies.md)).
- must not go past one level of inheritance; a three-deep chain hides which override runs.
- must not add a subclass base-call obligation to an owned template; inherited framework obligations remain explicit.
- must not use a template method to share utility code — that is an `Extensions` class
  ([components](../../components/components.md)).

---

## Components

- [background service](../behavior/background-service.md) — the most common base we derive from.
- [strategies](strategies.md) — the composition alternative, and the default when either would work.
- [entity configuration](../../domains/persistence/access/ef/entity-configuration.md)
  — the EF hooks the context base applies.
