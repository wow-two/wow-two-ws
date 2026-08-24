# Hooks

*Last updated: 2026-08-19*

> Every hook React 19 ships, what each one is for, and the ones banned outright.
> Purpose — the hook is the whole of a function component's memory, so a wrong pick is a stale read or a torn render.
> Use case — reach here before calling a built-in hook this codebase has not called before.

## The constructs

`SDK` counts `@wow-two-beta/ui`; `App` counts `smart-qr`.

| Construct | Is | SDK | App | Verdict |
|---|---|---|---|---|
| `useState` | a state slot and its setter | 167 | 27 | `use` |
| `useReducer` | a state slot driven by a reducer function | 1 | 0 | `use with care` |
| `useRef` | a mutable box that survives a render without causing one | 247 | 4 | `use` |
| `useMemo` | a value recomputed only when its deps change | 108 | 1 | `use` |
| `useCallback` | the same, for a function identity | 209 | 2 | `use` |
| `useEffect` | an effect run after commit, with a cleanup | 156 | 9 | `use` |
| `useLayoutEffect` | the same effect, run synchronously before paint | 12 | 0 | `use with care` |
| `useInsertionEffect` | the injection point a CSS-in-JS runtime needs | 0 | 0 | `banned` |
| `useId` | an id stable across a server render and hydration | 49 | 0 | `use` |
| `useSyncExternalStore` | a tear-free subscription to a store outside React | 16 | 0 | `use` |
| `useTransition` | a state update marked non-urgent, with a pending flag | 0 | 0 | `use with care` |
| `useDeferredValue` | a lagging copy of a value, for an expensive subtree | 0 | 0 | `use with care` |
| `useOptimistic` | state shown before the server confirms it | 0 | 0 | `banned` |
| `useActionState` | form state driven by an action's return | 0 | 0 | `banned` |
| `use(promise)` · `use(context)` | a read allowed inside a condition or a loop | 0 | 0 | `use with care` |
| `useContext` | the current value of a context | 51 | 0 | `use` |
| `useImperativeHandle` | the object a parent gets instead of the node | 10 | 0 | `use with care` |
| `useDebugValue` | a devtools label on a custom hook | 0 | 0 | `banned` |

- must reach for `useState` first; `useReducer` earns itself only where three or more fields change together.
- must reach for `useSyncExternalStore` for anything React does not own — a media query, a browser permission, a
  queue. The SDK's 16 sites are all of that shape, and every one of them avoids the effect-plus-state tearing bug.
- must keep an effect to one concern, and abort in-flight work in its cleanup
  ([hooks](../../../mla/constructs/behavior/hooks.md) § *Lifecycle rules*).
- must reach for `useLayoutEffect` only where a measurement must land before paint; it blocks the frame.
- must not use `useImperativeHandle` to hand a DOM node upward — assign the ref instead; keep it for a real
  imperative API (`focus()`, `scrollToIndex()`). All 10 SDK sites return `someRef.current` unchanged, which
  React 19 already does by passing `ref` down as a prop.
- must not add `useMemo` / `useCallback` without a measured render cost; each one costs a deps array that goes stale.

```tsx
// ✅ the store is outside React, so the subscription is tear-free and needs no effect
const matches = useSyncExternalStore(subscribe, () => query.matches, () => false);

// ❌ effect + state — the first paint reads the wrong value, and a concurrent render tears
const [matches, setMatches] = useState(false);
useEffect(() => subscribe(() => setMatches(query.matches)), []);
```

---

## Banned

- **`useInsertionEffect`** — no replacement is needed; it exists so a CSS-in-JS runtime can inject a rule before
  layout, and every such runtime is banned in [css](../css/css.md).
- **`useDebugValue`** — reach for a named hook; it is stripped from a production build, so a label a debugging session
  depends on is absent exactly where an incident happens.
- **`useOptimistic`** — reach for a passive mutation plus a refetch
  ([state & data](../../../mla/domains/data/state-and-data.md) § *Mutations*); the hook reverts to the real value when
  the action settles, and there is nothing here to reconcile a rejection against.
- **`useActionState`** — reach for the form engine ([forms](../../../mla/domains/forms/forms.md)); it reads an
  action's return, which needs a Server Action runtime no app here ships.

---

## Neighbours

- [react](react.md) — the full construct roster
- [hooks](../../../mla/constructs/behavior/hooks.md) — naming, return shape and JSDoc for a custom hook
- [state & data](../../../mla/domains/data/state-and-data.md) — which state a hook is even allowed to hold
