# Extensions

*Last updated: 2026-08-24*

> Static helper functions grouped by the domain noun they operate on, declared as a `const` object.
> Purpose — a loose helper has no home, so it is rewritten in every file that needs it.
> Use case — adding a helper, or deciding which noun's object it belongs to.

## Naming & shape

- **File:** `{Noun}Extensions.ts` (PascalCase) — `PersonExtensions.ts`, `DateExtensions.ts`.
- **Export:** `export const {Noun}Extensions = { ... } as const`.
- **Usage:** `PersonExtensions.getInitials("John Smith")`.

```typescript
// PersonExtensions.ts

/** Extends `Person` for display formatting (initials, display names). */
export const PersonExtensions = {
  /** @internal Whitespace splitter for name tokenization. */
  WhitespaceRegex: /\s+/,
  /** @internal Fallback when name is null or empty. */
  DefaultInitials: "?",

  /** Extracts up to 2 uppercase initials from a name. */
  getInitials(name: string | null): string {
    if (!name) return PersonExtensions.DefaultInitials;

    const parts = name.trim().split(PersonExtensions.WhitespaceRegex);
    if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();

    return name.slice(0, 2).toUpperCase();
  },
} as const;
```

---

## Rules

- **`as const`** — prevents mutation, signals static intent.
- **No `class` in this role** — a `const` object has no constructor and cannot be instantiated, which is
  the whole point of an extension. Where a `class` is allowed instead →
  [typescript](../constructs/typescript/typescript.md) § *Absence*.
- **No `namespace`** — not tree-shakeable, breaks under `isolatedModules`.
- **Noun = the domain, not the action** — `PersonExtensions`, not `InitialsExtensions`.
- **One file per noun** — all person helpers together, all date helpers together.
- **Extract regex / magic values** as named fields inside the object; casing is
  [naming](../notation/naming/naming.md)'s.
- **Blank lines between logical groups** in a method body (guard → logic → return).

---

## JSDoc

Verbs → [documentation](../notation/documentation/documentation.md) § *Verb starters* — the object, the method
and the internal field each have a row there.

---

## Location

- layer and slice → [architecture](../../../shapes/app/architecture/architecture.md), beside the type it extends.
- a cross-app one ships from the repo's shared package
  ([boundaries](../../../shapes/app/architecture/boundaries.md) § *Packaging*).

---

## Neighbours

- [naming](../notation/naming/naming.md) — helper-file suffixes
- [service](../../../../backend/dotnet/core/mla/constructs/behavior/service.md) — the C# static-helper peer
