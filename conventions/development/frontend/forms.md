# Forms

*Last updated: 2026-06-09*

## String form state (not enum types)

Forms that edit domain models with enum fields use **string** form state — HTML `<select>` / inputs work with strings, and partial edits need a forgiving shape. The `EditableFields` pattern:

```typescript
/** Defines the editable fields for the listing edit form. */
export interface EditableFields {
  contactType: string | null;     // ← string, NOT ContactType
  priceCurrency: string | null;   // ← string, NOT Currency
  priceAmount: number | null;     // ← scalar, unchanged
}
```

- **Enum fields → `string | null`** in form state.
- **Scalars stay as-is** (`number | null`, `boolean`).
- Resolve strings back to enum values on submit (reuse the domain mapper — see [models.md](models.md)), and surface validation errors instead of silently coercing.

## Flow

```
domain model (enum types)
   → EditableFields (strings)        ← seed form from model
   → user edits
   → resolve + validate on submit    ← strings back to enums
   → domain model / DTO              ← send to API
```

## Inputs

- Prefer `@wow-two-beta/ui` form components (`TextInput`, …) before hand-rolling — see [components.md](components.md).
- Controlled inputs; keep form state local (`useState`) unless it must be shared, then lift to a hook.
- Dropdown options derive from enum **label Records** via `enumOptions(Labels)` — see [enums.md](enums.md).

## See also

- [models.md](models.md) — domain model ↔ DTO ↔ form fields
- [enums.md](enums.md) — label Records → dropdown options
- [components.md](components.md) — props, `Form` terminology
