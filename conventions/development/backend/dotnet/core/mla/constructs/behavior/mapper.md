# Mappers

*Last updated: 2026-09-10*

> A type that transforms what it is handed, with no store and no set of its own.
> Purpose — keep a translation out of the types on either side of it, so neither knows the other.
> Use case — reach here when one shape must become another and nothing else changes.

## Location

### Folder
- must sit in a `Mappers/` folder under the domain that owns the target shape.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Maps**.
- must name both shapes, and say when the transform runs both ways.

```csharp
// ✅ both ends, and the direction
/// <summary>Maps a paid plan to its Stripe price id and back.</summary>
// ❌ names one end, so the other is a guess
/// <summary>Maps the plan.</summary>
```

### Type name
- must suffix with `Mapper`.

---

## Content

### Member docs

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start each method with **Maps**.

#### [Returns](../../../lla/notation/documentation/returns.md)
- must name the produced shape.

#### [Params](../../../lla/notation/documentation/params.md)
- must apply the parameter rules to the mapping inputs.

```csharp
// ✅
/// <summary>Maps the create request to its application command.</summary>
/// <param name="request">The request to map.</param>
/// <returns>The command the handler consumes.</returns>
```

### Members
- must take every input as an argument — a mapper owns no state to read from.
- must produce a success value or an explicit failure for every supported input.
- failure modes, bare values and `TryX` pairs → [results](../../components/result.md).
- may use `=>` for a member that returns or delegates — growth means the type stopped being a `Mapper`
  ([style](../../../lla/notation/style/style.md) § *The body*).

```csharp
// ✅ every input reaches an output
public CodeCreateCommand Map(CreateCodeApiRequest request)
{
    return new() { Name = request.Name, Content = request.Content };
}

// ❌ hides the mapping failure in an undocumented null
public CodeCreateCommand? Map(CreateCodeApiRequest request) =>
    request.Name is null ? null : new() { Name = request.Name };
```

---

## Neighbours

- [components](../constructs.md) — `Mapper` vs `Registry`
- [registry.md](registry.md) — the type that owns its set
