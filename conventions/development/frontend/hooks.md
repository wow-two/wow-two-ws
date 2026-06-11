# Hooks

*Last updated: 2026-06-09*

Custom hooks encapsulate state, lifecycle, and operations. Data-fetching hooks own the API call + mapping (see [state-and-data.md](state-and-data.md)).

## Naming

- **Always prefix `use`** — `useAuth`, `useSupplyListings`.
- **Name the resource or action, not the noun** — `useFilterOptions`, not `useFilters`.
- File is PascalCase (`UseSupplyListings.ts`), export is camelCase (`useSupplyListings`) — see [naming.md](naming.md).

## Location

- pnpm workspace: cross-app hooks in `packages/common/src/hooks/`; app-specific (domain data) in `{app}/src/hooks/`.
- single app: `src/hooks/` (or `src/{feature}/hooks/`).

## Return shape

- **Object return** for multiple values: `{ listings, loading, error, refetch }`.
- **Tuple return** only for simple state-like hooks: `[value, setValue]`.

```typescript
/** Manages the supply listings fetch lifecycle with pagination and filtering. */
export function useSupplyListings() {
  return { listings, loading, error, refetch };
}

/** Manages dropdown open/close state with outside-click-to-close behavior. */
export function useDropdown(): [boolean, () => void] { }
```

## JSDoc

| Hook kind | Verb | Example |
|---|---|---|
| State / lifecycle (≈90%) | `Manages` | `/** Manages the supply listings fetch lifecycle. */` |
| Thin context accessor | `Provides access to` | `/** Provides access to auth state from AuthContext. */` |

## Lifecycle rules

- Abort in-flight fetches on unmount / dependency change with `AbortController`; ignore `AbortError`.
- Keep effects narrow — one concern per `useEffect`; don't fetch + subscribe in the same effect.

## See also

- [state-and-data.md](state-and-data.md) — the API client these wrap
- [documentation.md](documentation.md) — verb table · [naming.md](naming.md)
