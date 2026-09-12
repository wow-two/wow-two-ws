# Extensions

*Last updated: 2026-09-10*

> The static tier over a **domain**'s types — logic that needs no collaborator and owns no state.
> Purpose — behaviour that needs nothing injected does not earn a service, and does not belong on the type it acts on.
> Use case — encoding, projection, mapping-in-the-small, or registration logic over one domain's types.

## Location

### Folder
- must sit in an `Extensions/` folder under the domain it extends.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Extends**, and name whichever the type name carries — the domain, the capability, or the
  primitive.
- must not name one of our own receiver types — a class extends a domain, not one type.

```csharp
// ✅ names the domain
/// <summary>Extends the codes domain with content encoding.</summary>
// ❌ names one type, so a second receiver has nowhere to go
/// <summary>Extends CodeEntity.</summary>
```

### Construct
- must declare a `public static class` → [constructs](../../../lla/constructs/constructs.md) § *Behavior components*.
- must take no collaborator — a method needing one belongs to a [service](service.md).
- must hold no mutable state.
- must carry only logic that admits no variant → [constructs](../constructs.md) § *Static or instance*.

### Type name
- must be named `{Domain}Extensions` after the domain the logic belongs to, `{Capability}Extensions` when the
  logic is one named capability rather than a domain's spread — `CasingExtensions`, `EncodingExtensions`.
- must name the receiver when it is a BCL primitive — `StringExtensions`, `DateExtensions`,
  `NumericExtensions`; a primitive belongs to no domain of ours, so its own name is the only one available.
- must reach for the capability over the primitive once the methods share one subject — `StringExtensions`
  holding only casing methods hides what it is, and the next unrelated method has nowhere else to go.
- must not name one of our own types — `CodeExtensions` covers `CodeEntity` and `CodeModel` alike.
- must not name the layer — no `ApplicationExtensions`.

---

## Neighbours

- [extensions](../../components/extensions.md) — receivers, members, and the `TryX` ladder
- [service](service.md) — where the same logic goes once it needs a collaborator
