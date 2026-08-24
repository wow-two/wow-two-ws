# Style

*Last updated: 2026-08-24*

> How a file is laid out inside — the language baseline, the dividers, and the order its members run in.
> Purpose — two files holding the same contents in a different order cost a reader twice to compare.
> Use case — opening a new file, or deciding where a helper goes once one already exists.

- must read file-per-type and one-component-per-folder at [naming](../naming/naming.md) and
  [constructs](../../../mla/constructs/constructs.md); this file covers in-file layout only.

## Language baseline

- must not write `var` — `const` by default, `let` only when reassigning, in `.ts`, `.tsx` and an inline
  `<script>` alike.
- must keep TypeScript **strict** mode on.

---

## Section dividers

- must mark a field group inside an interface or a large object with `// ── Section ──`.
- must use a plain comment for a logical section inside JSX — no dashes, no decorators.
- should not divide 2-3 fields; a divider there costs more than it saves.

```typescript
// ✅ lightweight label for field groups
export interface Listing {
  // ── Meta ──
  id: string;
  isValid: boolean;

  // ── Property ──
  propertyType: PropertyType | null;
}

// ✅ plain comment sections in JSX
{/* Image carousel */}
<div>...</div>

// ❌ dashed decorators
{/* ---- Image carousel ---- */}
// ---- Helpers ----
```

---

## Import order

- must take group order, intra-group sort and the `type`-import form from [imports](imports.md) —
  `side-effect → third-party → SDK → @/ alias → relative`, blank-line-separated.

---

## File-internal order

- must order a component file imports → types → constants → helpers → component → sub-components
  ([constructs](../../../mla/constructs/constructs.md)).
- must order a non-component module imports → types → constants → exported members.

---

## Neighbours

- [naming](../naming/naming.md) · [constructs](../../../mla/constructs/constructs.md)
- [imports](imports.md) — the group order this file's rule defers to
- [the C# sibling](../../../../../backend/dotnet/core/lla/notation/style/style.md) — same section order
