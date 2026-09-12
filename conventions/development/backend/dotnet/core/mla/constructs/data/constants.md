# Constants

*Last updated: 2026-09-10*

> A class that owns a value's authority — the one place a literal is named.
> Purpose — a literal repeated across files has no owner, so a change to it is a search rather than an edit.
> Use case — any value fixed by a spec, a wire format, a third-party contract, or our own decision.

## Location

### Folder
- must sit in a `Constants/` folder under the domain whose values it names, never a shared `Common/` bucket.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Holds**, and name what the values belong to.
- must not describe the values one by one — the members carry their own summaries.

```csharp
// ✅ names the owner
/// <summary>Holds the limits a code's rule chain is bound by.</summary>
// ❌ names the construct, which the suffix already carries
/// <summary>Constants for codes.</summary>
```

### Construct
- must declare a `public static class` → [constructs](../../../lla/constructs/constructs.md) § *Data components*.
- must hold `const` where the value is fixed at compile time, `static readonly` where it is built.
- must not hold behaviour — a method on a `Constants` class is an [extensions](../behavior/extensions.md) class.

### Type name
- must suffix with `Constants` — `CodeConstants`, `BillingConstants`.
- must drop the suffix only when the noun already reads as a set — `HttpHeaders`, `PostgresColumnTypes`.
- must name the domain, never the layer — no `ApplicationConstants`.

---

## Neighbours

- [constants](../../components/constants.md) — every condition for using one
- [extensions](../behavior/extensions.md) — where behaviour over the same domain goes
