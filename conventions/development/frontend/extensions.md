# Extensions

*Last updated: 2026-06-09*

Static helper functions grouped by **domain noun**. Mirrors the C# static-class pattern using `const` objects — the FE counterpart of a `*Extensions` static class.

## Naming & shape

- **File:** `{Noun}Extensions.ts` (PascalCase) — `PersonExtensions.ts`, `DateExtensions.ts`.
- **Export:** `export const {Noun}Extensions = { ... } as const`.
- **Usage:** `PersonExtensions.getInitials("John Smith")`.

```typescript
// PersonExtensions.ts

/** Provides extensions for person-related formatting (initials, display names). */
export const PersonExtensions = {
  /** @internal Whitespace splitter for name tokenization. */
  WHITESPACE_REGEX: /\s+/,
  /** @internal Fallback when name is null or empty. */
  DEFAULT_INITIALS: "?",

  /** Extracts up to 2 uppercase initials from a name. */
  getInitials(name: string | null): string {
    if (!name) return PersonExtensions.DEFAULT_INITIALS;

    const parts = name.trim().split(PersonExtensions.WHITESPACE_REGEX);
    if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();

    return name.slice(0, 2).toUpperCase();
  },
} as const;
```

## Rules

- **`as const`** — prevents mutation, signals static intent.
- **No `class`** — `const` objects have no constructor overhead and can't be instantiated.
- **No `namespace`** — not tree-shakeable, breaks under `isolatedModules`.
- **Noun = the domain, not the action** — `PersonExtensions`, not `InitialsExtensions`.
- **One file per noun** — all person helpers together, all date helpers together.
- **Extract regex / magic values** as named `UPPER_CASE` fields inside the object — co-located, self-documenting.
- **Blank lines between logical groups** in a method body (guard → logic → return).

## JSDoc

- Object: `/** Provides extensions for {domain} (concerns). */`
- Method: 3rd-person verb — `/** Extracts … */`, `/** Formats … */`, `/** Resolves … */`.
- Internal field: `/** @internal {desc}. */`.

## Location

- **Cross-app** (pnpm workspace): `packages/common/src/lib/{Noun}Extensions.ts` → import from `@{brand}/common/lib`.
- **App-specific:** `{app}/src/common/lib/{Noun}Extensions.ts` → import via `@/common/lib/...`.
- **Single app:** `src/lib/{Noun}Extensions.ts`.

## See also

- [naming.md](naming.md) — helper-file suffixes
- [../backend/services.md](../backend/services.md) — the C# static-helper conventions this echoes
