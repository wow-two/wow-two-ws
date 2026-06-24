# Enums

*Last updated: 2026-06-12*

Domain enums use **TypeScript `enum`** with a companion **label Record**. The label Record is the display/translation bridge (later replaced by backend-served translations).

> **Two enum-shaped categories — don't conflate them.** This page covers **domain enums** (user-facing, translatable, API-mapped) → TS `enum` + label Record. Internal **UI value-sets** (`HtmlElement`, `ButtonType`, `Key`, `ButtonDataState`, `Environment`) are a *different* category → const-object `as const`, no label Record. Both are valid; pick by category. See [Domain enums vs. UI value-sets](#domain-enums-vs-ui-value-sets).

## Location

One file per enum + its labels, in the domain layer:
- pnpm workspace: `packages/domain/src/{subdomain}/core/enums/{EnumName}.ts`
- single app: `src/{feature}/enums/{EnumName}.ts`

## Pattern

```typescript
/** Defines the supported currencies for listing prices and payments. */
export enum Currency {
  Unresolved = "unresolved",
  Uzs = "uzs",
  Usd = "usd",
}

/** Represents a container for Currency enum labels. */
export const CurrencyLabels: Record<Currency, string> = {
  [Currency.Unresolved]: "Unresolved",
  [Currency.Uzs]: "UZS",
  [Currency.Usd]: "USD",
};
```

## Rules

- **Values are camelCase strings** — match the backend's `JsonStringEnumConverter(JsonNamingPolicy.CamelCase)` serialization, so API JSON maps directly.
- **`Unresolved` is the first member** — fallback when a classifier/mapper can't determine a value.
- **`Record<Enum, string>` labels** force a label for every member (compile error if one is missing).
- **No `Enum` suffix** — `Currency`, not `CurrencyEnum`.
- **Singular name** — `ContactType`, not `ContactTypes`.

## Usage

```typescript
// ✅ Comparison — enum constant directly
if (listing.priceCurrency === Currency.Usd) { }

// ✅ Display — label Record
const label = CurrencyLabels[listing.priceCurrency];

// ✅ Dropdowns — derive options from the labels
const options = enumOptions(CurrencyLabels);

// ❌ Wrong — magic-string comparison
if (listing.priceCurrency === "usd") { }

// ❌ Wrong — `.value` access (legacy wrapper-object pattern)
if (listing.priceCurrency?.value === "usd") { }
```

## Enums in models vs forms

- **Domain models** use the TS enum type directly on enum fields (`priceCurrency: Currency | null`) — see [models.md](models.md).
- **Form state** uses `string` for enum fields (HTML `<select>` works with strings) — see [forms.md](forms.md).
- **DTOs** (raw API shape) keep enum fields as plain `string`; a mapper resolves them at the boundary — see [models.md](models.md).

## Domain enums vs. UI value-sets

Two categories look alike (a fixed set of named values) but serve different jobs and use different patterns. **Both are valid** — choose by what the set *is*, not by syntax preference.

| | Domain enum | UI value-set |
|---|---|---|
| Pattern | TS `enum` + `Record` labels (this page) | const object `as const` (see [extensions.md](extensions.md) for the same shape) |
| Examples | `Currency`, `ContactType`, `ListingStatus` | `HtmlElement`, `ButtonType`, `Key`, `ButtonDataState`, `Environment` |
| User-facing? | **Yes** — rendered, filtered, translated | **No** — internal plumbing (DOM tags, key codes, build env, `data-state` tokens) |
| Label Record? | **Required** | None — no display layer to translate |
| Crosses the API? | Yes — values match backend camelCase JSON | No — never serialized to/from the domain API |

```typescript
// Domain enum — user-facing, translatable, API-mapped → TS enum + labels
export enum Currency { Unresolved = "unresolved", Uzs = "uzs", Usd = "usd" }
export const CurrencyLabels: Record<Currency, string> = { /* … */ };

// UI value-set — internal, no labels, never hits the API → const object as const
export const ButtonType = { Button: "button", Submit: "submit", Reset: "reset" } as const;
export type ButtonType = (typeof ButtonType)[keyof typeof ButtonType];
```

Rule of thumb: **needs a label / shows up in the UI / maps to backend → domain enum.** Pure UI/runtime plumbing → value-set.

## See also

- [../backend/enums.md](../backend/persistence/enums.md) — the C# enum these mirror (PascalCase ↔ camelCase wire values)
- [extensions.md](extensions.md) — the `as const` const-object shape UI value-sets reuse
- [models.md](models.md) · [forms.md](forms.md) · [naming.md](naming.md)
