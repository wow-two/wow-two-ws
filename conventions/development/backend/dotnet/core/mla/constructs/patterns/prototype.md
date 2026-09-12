# Prototype

*Last updated: 2026-09-12*

> A new value derived from an existing one by copying it and changing the parts that differ.
> Purpose — keep a variant close to its source without a constructor that repeats every unchanged member.
> Use case — reach here when one value differs from another in a member or two.

## Shape

- must use the `record` `with` expression for shallow variants.
- must not implement `ICloneable`, and must not call `MemberwiseClone` — neither states what the copy depth is.
- must not write a `Clone()` method on a model; `with` already produces the copy, typed.
- must treat `with` as shallow; assigning reference members from another instance in a class initializer is shallow too.
- must share referenced values only when they are immutable or sharing is intentional; use a deep copy when a mutable data graph must be isolated.

```csharp
// ✅ the variant names only what differs
var preview = spec with { Logo = null, Size = PreviewSize };

// ❌ an untyped copy of unstated depth
var preview = (StyleSpec)spec.Clone();
```

---

## Use

- must reach for `with` to derive a request, a spec or a settings value for one call.
- must reach for it in tests to vary one field off a shared fixture value.
- may reach for it inside a `Mapper` performing a `T → T` transform ([mapper](../behavior/mapper.md)).

---

## Deep copies

- must use [FastCloner](https://github.com/lofcz/FastCloner) for deep copies of owned, detached, in-memory data graphs.
- must use the explicit runtime API `FastCloner.FastCloner.DeepClone(source)`; keep its dependency pin in the consuming repository.
- must preserve runtime types, shared aliases, cycles and collection lookup semantics within the supported data graph; verification covers the exact package version and representative graph shapes.
- must exclude live resources from the general data-copy contract, including service providers, EF contexts/proxies, streams, native handles and callbacks.
- must not silently configure ignore, shallow or reference-preserving overrides for mutable data whose isolation the caller expects.
- must not substitute JSON round trips or handwritten recursive copying for this contract.
- must treat source-generated `FastDeepClone()` as a separate implementation choice; its identity/polymorphism behavior and NativeAOT support require their own verification.

---

## Limits

- may copy an [entity](../data/entity.md) for candidate state, calculation or a snapshot; copying preserves its database identity unless deliberately changed.
- must not treat an entity copy as an inserted row or automatically tracked replacement; the persistence operation must define how the accepted candidate reaches the tracked instance.
- must validate a candidate at its accepting boundary under [validation placement](../../domains/validation/validation.md#placement); copying is not validation.
- must preserve any exceptional constructor-enforced contract across every supported copy path; neither `with` nor a graph cloner promises to rerun the ordinary constructor.
- must not equate deep copying with deep equality; copied arrays and lists still have their declared equality semantics.

---

## Components

- [entity](../data/entity.md) — copying state preserves row identity.
- [mapper](../behavior/mapper.md) — where a `T → T` derivation belongs when it is more than one member.
- [constructs](../../../lla/constructs/constructs.md) — `record` rules, and what a copy costs.
