# Models

*Last updated: 2026-06-09*

Domain models, DTOs, and the mapper between them. The FE mirrors the backend's "entity vs DTO" split: a clean domain shape for the app, a raw shape at the wire boundary.

## Three model kinds

| Kind | Enum fields | Lives in | Mutability |
|---|---|---|---|
| **Domain model** (`Listing`) | TS enum types | `entities/` (or domain package) | `Array<T>` (consumers may transform) |
| **DTO** (`ListingDto`) | plain `string` | `mappers/` — transient, between fetch + map | `Array<T>` (mirrors backend) |
| **Editable form fields** (`EditableFields`) | `string \| null` | `forms/` — see [forms.md](forms.md) | — |

## Domain model

Enum fields carry the **TS enum type directly** — not strings, not wrapper objects.

```typescript
/** Represents a domain listing with resolved enum values. */
export interface Listing {
  // ── Meta ──
  id: string;
  isValid: boolean;

  // ── Property ──
  propertyType: PropertyType | null;   // ✅ TS enum
  contactType: ContactType;            // ✅ TS enum (required)
  priceCurrency: Currency | null;      // ✅ TS enum
  priceAmount: number | null;          // scalar — unchanged
  phoneNumbers: Array<string>;         // mutable — see Collections
}
```

## DTO + mapper

- **DTO** = raw API response. All enum fields are plain `string`. Lives in `mappers/` (not `entities/`) because it's transient — used only between API fetch and mapping.
- **Mapper** (`mapListingDto`) resolves raw strings → TS enum values at the API boundary (inside the data hook). Bad data must not crash the UI: collect + log errors, fall back to `Unresolved`.

```typescript
/** Maps a raw ListingDto to a domain Listing, resolving enum strings. */
export function mapListingDto(dto: ListingDto): MapListingResult { }
```

## Member rules

- **`interface` for shapes/contracts**, `type` for unions and computed types.
- **Non-nullable by default** — add `| null` only when genuinely optional.
- **No member-level JSDoc on DTO/model fields** by default — backend owns field semantics; use `// ── Section ──` groups instead.

## Collections

Immutability is enforced at the **consumer boundary**, not the data source. Use **explicit generics** (`Array<T>`), never bracket shorthand.

```typescript
// ✅ explicit generics
phones: ReadonlyArray<string>
items: Array<string>

// ✅ bracket syntax only for an assignment annotation
const phones: ReadonlyArray<string> = [];

// ❌ bracket syntax in a declaration
phones: string[]
phones: readonly string[]
```

| Context | Type | Why |
|---|---|---|
| Domain entity / DTO field | `Array<T>` | data source — consumers may transform |
| Component props | `ReadonlyArray<T>` | consumer must not mutate parent data |
| Function / hook **input** param | `ReadonlyArray<T>` | won't mutate caller's data |
| Function return (built internally) | `Array<T>` | caller decides mutability |
| Mutable local state (builders) | `Array<T>` | needs push/splice |
| Dedup / uniqueness | `Set<T>` internally, return `Array<T>` | Set for logic, Array for consumers |

| Type | Mutable | Unique | C# equivalent |
|---|---|---|---|
| `Array<T>` | yes | no | `List<T>` |
| `ReadonlyArray<T>` | no | no | `IReadOnlyList<T>` |
| `Set<T>` | yes | yes | `HashSet<T>` |
| `ReadonlySet<T>` | no | yes | `IReadOnlySet<T>` |
| `Map<K,V>` | yes | keys | `Dictionary<K,V>` |
| `ReadonlyMap<K,V>` | no | keys | `IReadOnlyDictionary<K,V>` |

## Naming

| Kind | Suffix | Example |
|---|---|---|
| Domain model | — | `Listing` |
| Raw API model | `Dto` | `ListingDto` |
| Form fields | `Fields` / `EditableFields` | `EditableFields` |
| Mapper result | `Result` | `MapListingResult` |

## See also

- [enums.md](enums.md) · [forms.md](forms.md) · [components.md](components.md)
- [../backend/models.md](../backend/code-style/models.md) — the C# record rules this mirrors
