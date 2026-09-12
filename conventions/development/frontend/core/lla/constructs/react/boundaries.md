# Boundaries

*Last updated: 2026-09-10*

> The constructs that cross the tree — Context, portals, `Suspense`, error boundaries and `lazy`.
> Purpose — each one moves a value or a render past the parent that would otherwise own it, so each needs a verdict.
> Use case — reach here when state has to skip levels, or a subtree has to render somewhere else.

## The constructs

| Construct | Is | Verdict |
| --- | --- | --- |
| `createContext` | a value channel any descendant may read | `use` |
| `useContext` | the read half of that channel | `use` |
| `<Context>` as a provider | React 19's provider — the context itself, no `.Provider` | `use` |
| `<Context.Provider>` | the legacy provider spelling | `banned` |
| `createPortal` | children rendered under a DOM parent outside the tree | `use with care` |
| `<Suspense>` | a boundary that renders a fallback while a child awaits | `use with care` |
| `lazy` | a component behind a dynamic `import()` | `use with care` |
| error boundary (`componentDidCatch`) | the class that catches a throw below it | `use with care` |
| `getDerivedStateFromError` | the static that turns that throw into state | `use with care` |
| router `errorElement` | the route-level failure surface | `use` |

- must reach a portal through `Portal.tsx`, which owns the target lookup and the mount gate.
- must reach for the router's `errorElement` for a route-level failure; `AppErrorBoundary` is the one that exists.
- must write an error boundary as a class when one is needed below route level — it is the only construct React still
  offers no function form of, and the [class ban](components.md) carves it out by name.
- must pair `lazy` with a `<Suspense>` fallback in the same file, so the boundary cannot be forgotten at the call site.
- must not put app state behind Context that the query layer already caches
  ([state & data](../../../mla/domains/data/state-and-data.md)).
- must not let a context default stand in for a missing provider — throw, so the failure names the missing ancestor.

```tsx
// ✅ a missing provider fails where it is missing, not at the first undefined read
const context = useContext(FieldContext);
if (!context) throw new Error('Field parts must render inside <Field>.');

// ❌ the default silently renders a disconnected component forever
const context = useContext(FieldContext) ?? emptyField;
```

---

## Banned

- **`<Context.Provider>`** — use `<Context>` under the React 19 house policy;
  the legacy spelling remains supported, with deprecation announced for a future version.

---

## Neighbours

- [react](react.md) — the full construct roster
- [components](components.md) — the class ban this doc carves an exception out of
- [state & data](../../../mla/domains/data/state-and-data.md) — what belongs in Context at all
