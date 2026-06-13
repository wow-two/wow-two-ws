# Documentation

*Last updated: 2026-06-09*

JSDoc on every public export. Mirrors the backend XML-doc starter table ([../backend/documentation.md](../backend/code-style/documentation.md)) so a type reads the same in C# and TS.

## Format

- **One-liner by default** — `/** ... */` on a single line.
- **Multi-line only** when documenting parameters or complex behavior (3+ lines of substance).

```typescript
// ✅ Correct — compact one-liner
/** Defines the supported currencies for listing prices and payments. */
export enum Currency { }

// ✅ OK — multi-line for genuinely complex docs
/**
 * Maps a raw ListingDto from the API to a domain Listing.
 * Resolves enum string fields to TS enum values; returns `{ listing, error }` —
 * on failure, listing is null.
 */
export function mapListingDto(dto: ListingDto): MapListingResult { }

// ❌ Wrong — multi-line for a simple doc
/**
 * Defines the supported currencies for listing prices and payments.
 */
export enum Currency { }
```

## Verb starters (the table)

| Target | Verb | Example |
|---|---|---|
| Enum | `Defines` | `/** Defines the contact type of a listing author. */` |
| Label Record | `Represents a container for {Enum} enum labels.` | `/** Represents a container for ContactType enum labels. */` |
| Interface — shape/contract | `Defines` | `/** Defines the editable fields for the listing edit form. */` |
| Interface — data holder | `Represents` | `/** Represents a domain listing with resolved enum values. */` |
| Props interface | `Defines` | `/** Defines props for the author contact strip. */` |
| Component fn | `Renders` | `/** Renders the author contact strip. */` |
| Utility fn | 3rd-person verb | `/** Resolves a raw API string to a TS enum value. */` |
| State hook | `Manages` | `/** Manages the supply listings fetch lifecycle. */` |
| Context-accessor hook | `Provides access to` | `/** Provides access to auth state from AuthContext. */` |
| Extension object | `Provides` | `/** Provides extensions for person formatting. */` |
| Extension method | 3rd-person verb | `/** Extracts up to 2 uppercase initials. */` |
| Internal constant | `@internal {desc}` | `/** @internal Whitespace splitter. */` |

> **"Provides"** is reserved for implementation objects (extensions, services). Interfaces use **"Defines"** (shape) or **"Represents"** (data). `Manages` ≈ 90% of hooks; `Provides access to` only for thin context unwrappers.

## Member-level docs

- **Props interfaces:** type-level JSDoc required; **member-level omitted** — the backend declares field semantics, so the FE doesn't restate them.
- **Domain interfaces / DTOs:** member docs optional; add `// ── Section ──` field groups instead (see [code-organization.md](code-organization.md)).

## See also

- [../backend/documentation.md](../backend/code-style/documentation.md) — the C# starter table this mirrors
- [components.md](components.md) · [enums.md](enums.md) · [extensions.md](extensions.md)
