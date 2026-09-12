# Dtos

*Last updated: 2026-09-10*

> A projection of a domain shape onto the wire — data a caller reads, and no behavior.
> Purpose — keep the entity off the wire, so a stored shape and a published shape change independently.
> Use case — every payload a handler returns; the `T` an endpoint serializes.

## Location

### Folder
- must sit in a `Models/` folder under the domain that returns it.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- type summary baseline → [data](data.md) § *Shared rules*.
- must name which projection it is when the entity carries more than one.

```csharp
// ✅ names the projection, so a second one is tellable apart
/// <summary>Represents a code projection for the dashboard.</summary>
// ❌ restates the type name
/// <summary>Represents a code DTO.</summary>
```

### Construct
- declaration baseline → [data](data.md) § *Shared rules*.
- must declare `{ get; init; }` unless a projection is built in steps; then `set`, and say why.

### Type name
- must suffix with `Dto`, entity-first and singular — `CodeDto`, `RuleDto`.
- must qualify only when the entity carries more than one projection — `ChannelWithPipelinesDto`.
- must prefix with the parent only when the entity is context-bound — `ChannelSourceDto`.
- must reach for `Dto` even when the payload is composite or maps to no entity — `CurrentUserDto`.

```csharp
// ✅
public sealed record CodeDto
// ❌ `Response` is the envelope's word, never a payload's
public sealed record MeResponse
```
