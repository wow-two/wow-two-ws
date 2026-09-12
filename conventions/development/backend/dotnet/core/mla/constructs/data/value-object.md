# Value objects

*Last updated: 2026-09-10*

> A type whose identity is its values, stored inside an entity's row instead of owning one.
> Purpose — the suffix is what separates a type that owns a row from one that rides inside one.
> Use case — a content block, a routing rule, an amount; anything an entity persists whole.

## Location

### Folder
- must sit in a `Models/` folder under the domain whose entity stores it.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- type summary baseline → [data](data.md) § *Shared rules*.
- must name what the values mean together, never how they are stored.

```csharp
// ✅ names the thing the values add up to
/// <summary>Represents the credentials of a Wi-Fi network.</summary>
// ❌ names the storage shape, which the type does not own
/// <summary>Represents the JSON payload of Wi-Fi fields.</summary>
```

### Construct
- declaration baseline → [data](data.md) § *Shared rules*.
- must declare `{ get; init; }` — a value object is written once, whole.
- must declare no key — a type carrying its own identity is an [entity](entity.md).

```csharp
// ✅
public sealed record WifiContentValueObject
// ❌ a key claims a row the type does not own
public sealed record WifiContentValueObject { public required Guid Id { get; init; } }
```

### Type name
- must suffix with `ValueObject` — `WifiContentValueObject`, `CodeRuleValueObject`.
- must reach for `Entity` instead when the type owns a row.
