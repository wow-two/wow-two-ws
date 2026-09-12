# Factories

*Last updated: 2026-09-10*

> A type that builds instances the container cannot resolve on its own.
> Purpose — keep per-key or per-request construction out of the consumer, which would otherwise know every variant.
> Use case — reach here when the instance to build depends on a value known only at call time.

## Location

### Folder
- must sit in a `Factories/` folder under the domain whose types it builds.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Creates**.
- must name what varies — the key, the tier, the provider.

```csharp
// ✅ names the axis it dispatches on
/// <summary>Creates AI clients keyed by provider and model tier.</summary>
// ❌ names no axis, so the type could be anything
/// <summary>Creates AI clients.</summary>
```

### Type name
- must suffix with `Factory`.

---

## Content

### Member docs

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start the create method with **Creates**.

#### [Returns](../../../lla/notation/documentation/returns.md)
- must name the instance and the case where none matches.

```csharp
// ✅
/// <summary>Creates the client for the given provider.</summary>
/// <param name="provider">The provider to build for.</param>
/// <returns>The client, or <c>null</c> when the provider is unregistered.</returns>
```

### Members
- must expose one create method per axis it dispatches on.
- must resolve its dependencies through the container, never construct them.
- must use a block body `{ }` from the start — a create method gains a branch with every variant it builds
  ([style](../../../lla/notation/style/style.md) § *The body*).

---

## Components

- [patterns](patterns.md) — the gate a pattern passes to earn a doc
- [components](../constructs.md) — the suffix keep-list
