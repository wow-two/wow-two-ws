# Registries

*Last updated: 2026-09-10*

> A type that owns a set of key-to-type bindings and answers lookups against it.
> Purpose — hold what callers registered at composition time, and fail loudly when the set is incomplete.
> Use case — reach here when a discriminator, a slug or an enum member must resolve to a type.

## Location

### Folder
- must sit in a `Registries/` folder under the domain whose types it binds.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Binds**.
- must name the key and what it resolves to.

```csharp
// ✅ key and target
/// <summary>Binds each content variant to its discriminator.</summary>
// ❌ Holds is the const field's starter, and names no key
/// <summary>Holds the content variants.</summary>
```

### Type name
- must suffix with `Registry`.

---

## Content

### Member docs

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a lookup with **Gets**, and a registration with **Adds**.

#### [Exceptions](../../../lla/notation/documentation/exceptions.md)
- must document the throw for an unbound key — completeness is the registry's to enforce.

#### [Params](../../../lla/notation/documentation/params.md)
- must apply the parameter rules to the lookup key.

#### [Returns](../../../lla/notation/documentation/returns.md)
- must name the binding returned by the lookup.

```csharp
// ✅ the incompleteness is the contract
/// <summary>Gets the type bound to the discriminator.</summary>
/// <param name="discriminator">The enum member to resolve.</param>
/// <returns>The type bound to the discriminator.</returns>
/// <exception cref="InvalidOperationException">No type is bound to the member.</exception>
```

### Members
- may mutate its binding set during composition, overriding the state-free baseline in
  [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.
- must freeze registrations before the first lookup.
- must throw when a key in the closed set has no binding — a silent miss hides a wiring fault.
- may use `=>` for a member that returns or delegates — a registry holds bindings, not logic that grows
  ([style](../../../lla/notation/style/style.md) § *The body*).

```csharp
// ✅ the miss is loud
public Type Get(CodeContentType key)
{
    return _bindings.TryGetValue(key, out var type)
        ? type
        : throw new InvalidOperationException($"No type bound to {key}.");
}

// ❌ a null hides a wiring fault until the caller dereferences it
public Type? Get(CodeContentType key) => _bindings.GetValueOrDefault(key);
```

---

## Neighbours

- [components](../constructs.md) — `Registry` vs `Repository`
- [mapper.md](mapper.md) — the type handed its data
