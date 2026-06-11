# Components

*Last updated: 2026-06-09*

## One component per folder (REQUIRED)

Every component gets its own folder. Folder = camelCase, main file = PascalCase matching the component, `index.ts` barrel controls the public API. Never flatten files next to folders.

```
// ✅ Correct
components/
  phoneChip/
    PhoneChip.tsx
    index.ts                  ← export { PhoneChip } from "./PhoneChip.js"
  listingDetailModal/
    ListingDetailModal.tsx
    ListingDetailHeader.tsx   ← internal sub-component
    ClassificationInfo.tsx    ← internal sub-component
    index.ts                  ← only exports ListingDetailModal

// ❌ Wrong — flat files mixed with folders
components/
  PhoneChip.tsx
  listingDetailModal/
    ListingDetailModal.tsx
```

- Applies to **components only** — not views, pages, hooks, or lib files.
- Sub-components in a folder are **internal by default**; only what `index.ts` exports is public.
- In the beta UI library this is also enforced per top-level domain folder (`forms/`, `display/`, …), each component carrying `*.stories.tsx` (+ `*.variants.ts` when needed).

## File structure (order within a component file)

1. Imports (see import order in [code-organization.md](code-organization.md))
2. Types / interfaces (props, local types)
3. Constants (options arrays, config objects)
4. Helper functions (pure, no hooks)
5. Component function
6. Sub-components (only if small + tightly coupled)

## Props

| Rule | Why |
|---|---|
| **Do not destructure** — access via `props.x` | destructuring drops `readonly` protection |
| **Parameter always named `props`** | consistent grep-based audits |
| **All members `readonly`** | blocks `props.x = …` inside the component |
| **Array props `ReadonlyArray<T>`** | blocks `.push()`/`.splice()` |
| **`interface` for props**, `type` for unions | shape vs computed |
| **Type-level + component-level JSDoc** required | `Defines` props, `Renders` component |

```typescript
/** Defines props for the author contact strip. */
interface AuthorContactProps {
  readonly authorName: string;
  readonly contactType: ContactType;
  readonly phones: ReadonlyArray<string>;
}

/** Renders the author contact strip. */
export function AuthorContact(props: AuthorContactProps) {
  props.authorName;          // ✅ read
  props.phones[0];           // ✅ index
  props.phones.push("x");   // ❌ ReadonlyArray
  props.authorName = "x";   // ❌ readonly property
}

// ❌ Wrong — destructuring loses readonly protection
export function AuthorContact({ authorName, phones }: AuthorContactProps) {
  authorName = "x";   // compiles — no protection
}
```

## UI terminology (what kind of component is it?)

| Term | Owns | Example |
|---|---|---|
| **Page** | the entire viewport — outermost shell; decides sidebar/topbar/none | `SignInPage`, `MainLayout` |
| **View** | content area inside a page — swaps on navigation, layout persists | `InboxView`, `OutreachView` |
| **Modal** | overlay above the current page+view — backdrop, floats | confirm dialog, detail preview |
| **Form** | reusable input component — pluggable into any page/view/modal | `SignInForm`, `FilterForm` |

## Styling & variants

- Tailwind utilities only; conditional classes via `cn()`. See [styling.md](styling.md).
- Multi-variant components define their class map with **`tailwind-variants`** in a co-located `*.variants.ts` / `*Styles.ts` file — don't inline large conditional class strings.
- **Prefer `@wow-two-beta/ui` components** (Button, Card, Badge, Heading, Text, Alert, Spinner, EmptyState, TextInput, …) before hand-rolling. Missing one? Build locally, then migrate upstream.

## See also

- [styling.md](styling.md) · [forms.md](forms.md) · [hooks.md](hooks.md)
- [code-organization.md](code-organization.md) — import order, section dividers
- [project-structure.md](project-structure.md) — where components live
