# Constants

*Last updated: 2026-09-10*

> A static class holding values the codebase names once.
> Purpose — one home for a value's authority, so a literal never has to be explained twice.
> Use case — reach here when a value is fixed by a spec, a wire format, or a third-party contract.

> Defined at [constants — the construct](../constructs/data/constants.md); this doc carries every condition for using one.

## Location

Where it sits is part of what it is → [constants](../constructs/data/constants.md) § *Location*.

---

## Declaration

What it is, how it is declared and what it is called → [constants](../constructs/data/constants.md) § *Declaration*.

### Type doc

- must inherit [constant type documentation](../constructs/data/constants.md#type-doc).

```csharp
// ✅
/// <summary>Holds the canonical kebab-case slugs for every channel.</summary>
// ❌ names no set
/// <summary>Holds constants.</summary>
```

---

## Content

### Member docs

#### [Summary](../../lla/notation/documentation/summary.md)
- must start with **Holds**.
- must name the authority that fixes the value — a spec, a wire format, a third-party contract.
- must state the shape of a format string, never its slots.

#### [Remarks](../../lla/notation/documentation/remarks.md)
- must carry `<remarks>` only to name the spec the value answers to — `Follows RFC 6068.`

```csharp
// ✅ the authority, not the literal
/// <summary>Holds the token an open network carries in a WIFI payload.</summary>
public const string OpenNetwork = "nopass";

// ❌ restates what the line already shows
/// <summary>Holds the value "nopass".</summary>
```

### Members
- must use the [constant declaration](../constructs/data/constants.md#construct).
- must assign a fixed value, or build a fixed shared object once; no mutable per-call state.
- must not put a behavior method in a constants holder.
- must order from the primitive value to the composed one, or in the order the flow consumes them.
- must separate every constant from the next with one blank line.
- must split a group into its own file once the class passes 60 lines — regions hide length, files state it.

```csharp
// ✅ literals, primitive first, the composed shape after
public const string Scheme = "WIFI:";
public const string PayloadShape = Scheme + "T:{0};S:{1};P:{2};;";

// ❌ reaches out for its value, so the class no longer holds the authority
public static readonly string PayloadShape = WifiFormats.BuildShape();
```

---

## When a literal earns a constant

A literal with fixed structural parts is a **contract shape**, not an implementation detail.

- must lift a payload, URI or template literal into a named `const` built with `string.Format` once it
  carries any constant segment beyond a single prefix.
- must keep a bare prefix inline — `$"tel:{phone}"` has no shape to see.
- must give a conditionally appearing segment its own constant, so the parent shape stays readable.
- the constant shows the whole shape in one place, which interpolation scatters across the expression.

---

## Neighbours

- [summary](../../lla/notation/documentation/summary.md) — the starter table
- [style](../../lla/notation/style/style.md) — lifting a structured literal into a named `const`
