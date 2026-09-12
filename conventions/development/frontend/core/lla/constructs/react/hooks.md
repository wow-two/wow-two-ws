# Hooks

*Last updated: 2026-09-10*

> Every hook React 19 ships, what each one is for, and the ones banned outright.
> Purpose — the hook is the whole of a function component's memory, so a wrong pick is a stale read or a torn render.
> Use case — reach here before calling a built-in hook this codebase has not called before.

## The constructs

| Construct | Is | Verdict |
| --- | --- | --- |
| `useState` | a state slot and its setter | `use` |
| `useReducer` | a state slot driven by a reducer function | `use with care` |
| `useRef` | a mutable box that survives a render without causing one | `use` |
| `useMemo` | a value recomputed only when its deps change | `use` |
| `useCallback` | the same, for a function identity | `use` |
| `useEffect` | an effect run after commit, with a cleanup | `use` |
| `useLayoutEffect` | the same effect, run synchronously before paint | `use with care` |
| `useInsertionEffect` | the injection point a CSS-in-JS runtime needs | `banned` |
| `useId` | an id stable across a server render and hydration | `use` |
| `useSyncExternalStore` | a tear-free subscription to a store outside React | `use` |
| `useTransition` | a state update marked non-urgent, with a pending flag | `use with care` |
| `useDeferredValue` | a lagging copy of a value, for an expensive subtree | `use with care` |
| `useOptimistic` | state shown before the server confirms it | `banned` |
| `useActionState` | form state driven by an action's return | `banned` |
| `use(promise)` · `use(context)` | a read allowed inside a condition or a loop | `use with care` |
| `useContext` | the current value of a context | `use` |
| `useImperativeHandle` | the object a parent gets instead of the node | `use with care` |
| `useDebugValue` | a devtools label on a custom hook | `banned` |

- must reach for `useState` first; `useReducer` earns itself only where three or more fields change together.
- must use `useSyncExternalStore` for render-visible external store state, such as a media query or permission.
- must keep an effect to one concern, and abort in-flight work in its cleanup
  ([hooks](../../../mla/constructs/behavior/hooks.md) § *Lifecycle rules*).
- must reach for `useLayoutEffect` only where a measurement must land before paint; it blocks the frame.
- must assign a DOM ref directly; reserve `useImperativeHandle` for a documented imperative API.
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
- **`useActionState`** — use the [form engine](../../../mla/domains/forms/forms.md) under the house policy;
  the hook also supports client actions and does not require a Server Action runtime.

---

## Lifecycle

- must keep rendering pure; start external work in an event handler or effect, not during render.
- must call hooks unconditionally at component/custom-hook top level; `use` follows its documented special rules.
- must include every reactive dependency an effect reads; change the effect instead of suppressing dependency checks.
- must pair each setup with cleanup that releases its listeners, subscriptions, timers and owned resources.
- must tolerate Strict Mode setup → cleanup → setup without duplicate resources or visible state corruption.
- must cancel stale async work where supported and ignore late results once its request or owner is obsolete.
- must not rely on `useMemo` or `useCallback` for correctness; caches may be discarded.
- must keep server snapshots stable when using `useSyncExternalStore` in a server-compatible entry.

---

## Neighbours

- [react](react.md) — the full construct roster
- [hooks](../../../mla/constructs/behavior/hooks.md) — naming, return shape and JSDoc for a custom hook
- [state & data](../../../mla/domains/data/state-and-data.md) — which state a hook is even allowed to hold
