# Constants

*Last updated: 2026-08-24*

> A single fixed value, or an unrelated group of them, declared once and read everywhere.
> Purpose — a literal repeated across files drifts, and nothing names what the value means.
> Use case — adding a fixed value, or choosing between a constant and an enum for a closed set.

## Const vs enum

- a single scalar, or unrelated values → a **`const`** (this file).
- a fixed **set** of related string values (a closed vocabulary) → an **enum** ([enums](enums.md)).

---

## Declaration

- must name a module-level constant **PascalCase** — `PresetIconSize`, `DefaultGradientEnd` — never `UPPER_SNAKE`
  ([naming](../notation/naming/naming.md)). Existing `UPPER_SNAKE` migrates gradually.
- must freeze an object / array / tuple constant with `as const`.
- must co-locate constants with the module that owns them (`design/gradient.ts`); reserve a dedicated `Constants.ts`
  for a slice-wide set.
- prefer a named factory over an inlined literal for a repeated shape — `makeDefaultGradient(fg)`, not a hand-built
  object at each call site.

```typescript
/** Preset-icon glyph size (px). */
export const PresetIconSize = 16;

/** Linear-gradient direction presets — angle (deg) + arrow. */
export const Angles = [/* … */] as const;
```

---

## Comments

- must JSDoc every exported constant with a one-liner `/** … */` — include units / range when not obvious, `(px)`,
  `(0..1 extent)` ([documentation](../notation/documentation/documentation.md)).
- an internal (unexported) constant uses `/** @internal … */`.

---

## Neighbours

- [enums](enums.md) — the value-**set** sibling
- [extensions](extensions.md) — `{Noun}Extensions` helper objects
- [naming](../notation/naming/naming.md) — the casing rules these follow
