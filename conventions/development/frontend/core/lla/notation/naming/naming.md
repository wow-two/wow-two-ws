# Naming

*Last updated: 2026-09-10*

> How a frontend file, folder, export and constant is spelled — casing, role suffixes, and the banned names.
> Purpose — one universal rule per axis, so a name is derivable rather than remembered.
> Use case — creating a file, or checking an existing name still says what the thing is.

## Files [REQUIRED]

- must name every `.ts`, `.tsx` and `.vue` file `PascalCase`, matching its primary export.
- must keep an `index.ts` barrel **lowercase** — `Index.ts` breaks on a case-insensitive filesystem.
- must accept the hook mismatch — `useSupplyListings` lives in `UseSupplyListings.ts`, on one file rule.

```txt
✅ ListingCard.tsx · UseSupplyListings.ts · ListingDto.ts · ContactType.ts · index.ts
❌ listingCard.tsx · use-supply-listings.ts · contact-type.ts · Index.ts
```

---

## Folders

- must name every folder `camelCase` — `src/supply/propertyInfo/`, never `Supply/` or `property-info/`.

---

## Acronyms

- must write an acronym as a capitalized word, never all-caps — `Api` not `API`, `Id` not `ID`, `Html`, `Json`.
- must lowercase the whole run where the position is camelCase — `apiUrl`, `htmlId`, never `apiURL`.
- must apply it to file, folder, type, export, prop and constant names alike.
- must leave a mixed-case proper name alone — `OAuth`, `TypeScript`; the rule governs all-caps runs only.
- the casing is ecosystem-wide, matching the
  [backend](../../../../../backend/dotnet/core/lla/notation/naming/naming.md).

---

## Co-located file suffixes

A non-component file co-located in a folder takes a descriptive PascalCase name plus a role suffix.

- must suffix dependency-free logic over a type `*Extensions.ts` ([extensions](../../components/extensions.md)).
- must suffix a shared `tailwind-variants` config `*Styles.ts` ([styling](../../../../shapes/app/platform/styling.md)).
- must not read internal-ness off a name — internal means absent from `index.ts`.

---

## Resource seams — `*Broker`

- must name a swappable seam over a **client-side resource** (`localStorage`, a store, an in-memory map)
  `*Broker` — the contract `StorageBroker`, instances `localStorageBroker` / `memoryBroker`, a `broker` param.
- must reach for it only for a resource seam; dependency-free logic stays `*Extensions`.
- the word matches the backend `Broker` ([components](../../../../../backend/dotnet/core/mla/components/components.md)).

---

## App-shell baselines — `App*`

- app singleton names and their source placement → [routing](../../../../shapes/app/routing/routing.md).

---

## Exports

- must prefer named exports, reaching for `export default` only for a lazily loaded page or view.
- must give every folder with a public API a barrel `index.ts` — it decides what is public.

---

## Quick reference

| Kind | Casing | Example |
|---|---|---|
| Component file · export | PascalCase | `FilterBar.tsx` · `FilterBar` |
| Hook file · export | PascalCase file, camelCase `use*` export | `UseTheme.ts` · `useTheme` |
| Util / extensions file | PascalCase | `Currency.ts` · `PersonExtensions.ts` |
| Type file · export | PascalCase | `Listing.ts` · `Listing` |
| Domain enum · label Record | PascalCase, singular, no `Enum` suffix | `ContactType` · `ContactTypeLabels` |
| UI value-set (`as const`) | PascalCase, singular, no labels | `HtmlElement` · `ButtonType` · `Key` |
| Constant — scalar or data | PascalCase, `as const` for objects | `PresetIconSize` · `DefaultRadius` |
| Folder · barrel | camelCase · lowercase | `propertyInfo/` · `index.ts` |

- must name a constant PascalCase, the same category as an enum or value-set, never `UPPER_SNAKE`.
- may migrate an existing `UPPER_SNAKE` constant gradually; new code is PascalCase.

---

## Banned names

- must not name a file, type or object `Helper` · `Helpers` · `Util` · `Utils` · `Common` · `Manager` — a name
  describing no role names nothing, and the folder becomes where work goes to be lost.
- must route dependency-free logic over a domain to `*Extensions` instead.
- must split a would-be `Helpers` file by the role each function actually plays when no single domain owns them.
- the ban is language-wide — the
  [backend](../../../../../backend/dotnet/core/lla/notation/naming/naming.md) bans them too.

```typescript
// ❌ FormHelpers.ts — names no role, so every later utility lands here too
export function toFieldErrors(problem: ProblemDetails) { }

// ✅ FormExtensions.ts — names the domain it extends
export const FormExtensions = { toFieldErrors(problem: ProblemDetails) { } } as const;
```

---

## Specific naming lives by area

- which **suffix** names which component kind
  → [visual kinds](../../../mla/constructs/visual/visual.md) § *Suffix routing*
- what every component name owes — the trailing suffix, the modifiers, the coining gate
  → [constructs](../../../mla/constructs/constructs.md) § *Naming*
- a seam a component consumes — `*Client` · `*Bus` · `*Policy`
  → [headless suffixes](../../../mla/constructs/behavior/headless-suffixes.md)
- a prop name → [props](props.md)

---

## Neighbours

- [props](props.md) — the prop-name vocabulary every component reads the same way
- [enums](../../components/enums.md) — the domain-enum and UI value-set split
- [constructs](../../../mla/constructs/constructs.md) — the prop **shape** rules that pair with those names
