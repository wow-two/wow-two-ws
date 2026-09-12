# Time

*Last updated: 2026-09-10*

> Our seam over the clock — the thing a type asks for the current instant instead of reading a static.
> Purpose — a static clock cannot be moved, so a test that depends on time either sleeps or lies.
> Use case — any timestamp, expiry, scheduling window or elapsed-time calculation.

## Location

### Folder
- must sit in a `Time/` folder, never beside a single consumer.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Provides**, and name what is read.
- must not restate that it wraps `TimeProvider` — the construct row already says so.

```csharp
// ✅ names what it provides
/// <summary>Provides the current UTC instant.</summary>
// ❌ names the implementation detail
/// <summary>Wraps TimeProvider.</summary>
```

### Construct
- clock contract and `TimeProvider` usage → [time](../../components/time.md).
- must be injected like any collaborator — never resolved from a static.
- must expose UTC; a local-time conversion is the caller's, at the edge.

### Type name
- must name the reading, not the mechanism — `IClock` over `ITimeProviderWrapper`.
- must not suffix with `Service` — reading the clock orchestrates nothing.

---

## Neighbours

- [time](../../components/time.md) — every condition for using the seam
- [settings](../data/settings.md) — where a configured offset or window is bound
