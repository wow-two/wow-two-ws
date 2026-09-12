# Json

*Last updated: 2026-09-10*

> One type's storage seam — the options its stored bytes are written with, and the pair that reads and writes them.
> Purpose — stored bytes outlive the code that wrote them, so their options must be pinned per type, not shared with the wire.
> Use case — a column, a cache entry or a file holding one type as JSON.

## Location

### Folder
- must sit beside the type it persists, in that type's own folder.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Serializes**, and name the type it persists.
- must state the storage it is written for when more than one exists.

```csharp
// ✅ names the type and where the bytes land
/// <summary>Serializes code content for its jsonb column.</summary>
// ❌ names the format, which the suffix already carries
/// <summary>Serializes to JSON.</summary>
```

### Construct
- must declare a `static class` — the seam holds options and two methods, never state.
- must hold its `JsonSerializerOptions` as a single `static readonly` instance, built once.
- must not reuse the host's API options — the wire contract and the stored contract change on different schedules.

### Type name
- must suffix with `Json`, prefixed by the type it persists — `CodeContentJson`.
- must name the format rather than the operation; the type is already in the prefix.
- must reach for [serialization](../../../../shapes/service/platform/responses/serialization.md) instead when the contract is the HTTP wire.

---

## Neighbours

- [json](../../components/json.md) — every condition for using the seam
- [mapper](mapper.md) — the transform role a seam is not
