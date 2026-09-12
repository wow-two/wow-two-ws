# Builders

*Last updated: 2026-09-10*

> A type that accumulates one value across calls and ends in `Build()`.
> Purpose — a value with many optional parts stays readable when it is assembled rather than parameterised.
> Use case — a saga definition, a cache key, a query the caller composes in steps.

## Location

### Folder
- must sit beside the type it builds, in the same folder.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Builds**, and `<see cref>` the type it returns.
- must name the parts a caller may add when the builder is optional-heavy.

```csharp
// ✅ names what comes out
/// <summary>Builds an <see cref="EventSaga"/> from its ordered steps.</summary>
// ❌ names the builder, not the value
/// <summary>Builds a saga builder.</summary>
```

### Construct
- construct → [behavior](behavior.md) § *Shared rules*.
- may hold mutable construction state until `Build()` closes the value, overriding
  [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.
- must return the built type from `Build()`, never a partially-assembled shape.

### Type name
- must suffix with `Builder`, prefixed by what it returns — `EventSagaBuilder`, `CacheKeyBuilder`.
- must reach for `Factory` instead when the instance is built in one call.

```csharp
// ✅
public sealed class EventSagaBuilder
// ❌ one call and no accumulation, so it is a `Factory`
public sealed class ClientBuilder { public HttpClient Build(string name) => …; }
```
