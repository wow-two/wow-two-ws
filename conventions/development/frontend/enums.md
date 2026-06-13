# Enums

*Last updated: 2026-06-09*

Domain enums use **TypeScript `enum`** with a companion **label Record**. The label Record is the display/translation bridge (later replaced by backend-served translations).

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

## See also

- [../backend/enums.md](../backend/persistence/enums.md) — the C# enum these mirror (PascalCase ↔ camelCase wire values)
- [models.md](models.md) · [forms.md](forms.md) · [naming.md](naming.md)
