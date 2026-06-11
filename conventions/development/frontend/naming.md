# Naming

*Last updated: 2026-06-09*

## Files — PascalCase (one rule, one exception)

**All `.ts` and `.tsx` files use PascalCase.** The file name matches the primary export.

**Exception:** `index.ts` barrel files are always **lowercase** — Node/TS module resolution depends on it (`import from "../foo"` → `foo/index.ts`). PascalCase `Index.ts` breaks on case-insensitive filesystems (macOS, Windows).

```
// ✅ Correct
ListingCard.tsx            ← component exports ListingCard
UseSupplyListings.ts       ← hook exports useSupplyListings
Constants.ts               ← exports constants
Filters.ts                 ← exports filter types
ListingDto.ts              ← exports ListingDto interface
ContactType.ts             ← exports ContactType enum
index.ts                   ← barrel export (always lowercase)

// ❌ Wrong
listingCard.tsx             ← camelCase file
use-supply-listings.ts      ← kebab-case file
contact-type.ts             ← kebab-case file
```

**Hooks file vs export mismatch is accepted:** the export `useSupplyListings` is camelCase (React convention), but the file is `UseSupplyListings.ts` (PascalCase). One universal file rule beats a per-kind carve-out.

## Folders — camelCase

```
// ✅ Correct
src/supply/components/
src/common/hooks/
packages/domain/src/listings/core/enums/
src/supply/propertyInfo/

// ❌ Wrong
src/Supply/Components/       ← PascalCase folders
src/property-info/           ← kebab-case folders
```

## Helper-file suffixes

Non-component utility files co-located in a folder use **descriptive PascalCase + role suffix**:

| Suffix | Use | Examples |
|---|---|---|
| `*Extensions.ts` | Helpers that extend a built-in/external type (see [extensions.md](extensions.md)) | `DateExtensions.ts`, `StringExtensions.ts` |
| `*Styles.ts` | Shared `tailwind-variants` configs (see [styling.md](styling.md)) | `ButtonStyles.ts`, `InputStyles.ts` |
| `*Helpers.ts` | Domain-specific fns that don't fit `Extensions` | `FormHelpers.ts` |

The `*Extensions` suffix is borrowed from .NET extension methods — a deliberate divergence from JS's camelCase-utilities norm, for consistency with the .NET-heavy wow-two ecosystem. **Internal** = absent from `index.ts`, not a naming signal.

## Exports

- **Named exports preferred** — avoid `export default` except for React page/view components used with lazy loading.
- **Barrel `index.ts`** in each folder that has a public API; it controls what is public.

## Quick reference

| Kind | Casing | Example |
|---|---|---|
| Component file | PascalCase | `FilterBar.tsx` |
| Component export | PascalCase | `FilterBar` |
| Hook file | PascalCase | `UseTheme.ts` |
| Hook export | camelCase `use*` | `useTheme` |
| Util / extensions file | PascalCase | `Currency.ts`, `PersonExtensions.ts` |
| Type file | PascalCase | `Listing.ts` |
| Type export | PascalCase | `Listing` |
| Enum / label Record | PascalCase, singular, no `Enum` suffix | `ContactType`, `ContactTypeLabels` |
| Folder | camelCase | `propertyInfo/` |
| Barrel | lowercase | `index.ts` |

## See also

- [enums.md](enums.md) — enums-as-`enum` + label Record
- [components.md](components.md) — one-component-per-folder
- [extensions.md](extensions.md) — `*Extensions` const objects
