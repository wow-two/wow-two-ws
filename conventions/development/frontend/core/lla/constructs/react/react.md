# React 19

*Last updated: 2026-09-10*

> Every construct React 19 offers a component or a hook, and the ones banned outright.
> Purpose — separate framework support from the house source-form policy.
> Use case — reach here before writing a hook, a ref or a render idiom new to this codebase.

## The groups

| Group | Covers | Doc |
|---|---|---|
| hooks | the 17 built-in hooks, and which of them earn a call | [hooks](hooks.md) |
| components | function vs class · `forwardRef` · refs as props · `memo` · RSC | [components](components.md) |
| boundaries | Context · portals · `Suspense` · error boundaries · `lazy` | [boundaries](boundaries.md) |
| JSX | fragments · `key` · spread · conditional idioms · the element API | [jsx](jsx.md) |

Hook naming, return shape and JSDoc verbs are not construct rules — they live in
[hooks](../../../mla/constructs/behavior/hooks.md).

---

## The constructs

| Construct | Is | Verdict |
| --- | --- | --- |
| function component | a component declared as a function | `use` |
| class component | the `extends Component` form | `banned` |
| `useState` | a state slot and its setter | `use` |
| `useReducer` | a state slot driven by a reducer | `use with care` |
| `useRef` | a mutable box that survives a render | `use` |
| `useMemo` · `useCallback` | a value or a function cached across renders | `use` |
| `useEffect` | a post-commit effect with a cleanup | `use` |
| `useLayoutEffect` | the same effect, run before paint | `use with care` |
| `useInsertionEffect` | the CSS-in-JS injection point | `banned` |
| `useId` | an id stable across server and client | `use` |
| `useSyncExternalStore` | a subscription to a store outside React | `use` |
| `useTransition` · `useDeferredValue` | a render marked non-urgent | `use with care` |
| `useOptimistic` | state shown ahead of the server's answer | `banned` |
| `useActionState` | state driven by a client or server action | `banned` |
| `use(promise)` · `use(context)` | a conditional read of a promise or a context | `use with care` |
| `useContext` · `createContext` | the shared-state read, and the context itself | `use` |
| `useImperativeHandle` | the instance API a parent reaches through a ref | `use with care` |
| `useDebugValue` | a devtools label on a custom hook | `banned` |
| `forwardRef` | the pre-19 wrapper that passed a ref past props | `banned` |
| ref as a prop | React 19's own `ref` — a prop like any other | `use` |
| `memo` | a component skipped when its props compare equal | `use with care` |
| `createPortal` | children rendered under a different DOM parent | `use with care` |
| `<Suspense>` · `lazy` | an await boundary, and a dynamically imported child | `use with care` |
| error boundary (`componentDidCatch`) | the class React still requires for a throw | `use with care` |
| Server Components · `'use client'` · `'use server'` | explicit delivery-target support | `use with care` |
| fragment `<>` · `<Fragment key>` | children grouped with no element | `use` |
| `key` | the identity React diffs a list child on | `use` |
| JSX spread `{...props}` | every remaining prop forwarded at once | `use` |
| `&&` · ternary in JSX | the two conditional-render idioms | `use` |
| `dangerouslySetInnerHTML` | an element's `innerHTML` set from a string | `use with care` |
| `createElement` · `cloneElement` | an element built or re-emitted without JSX | `use with care` |
| `Children.*` · `isValidElement` | the legacy walk over an opaque `children` | `use with care` |
| `startTransition` · `flushSync` | the imperative scheduling escapes | `use with care` |

```tsx
// ✅ React 19 — ref is a prop, and the props interface owns it
export function SearchInput({ ref, ...rest }: SearchInputProps) { … }

// ❌ house migration rule — use a ref prop in React 19
export const SearchInput = forwardRef<HTMLInputElement, SearchInputProps>((props, ref) => …);
```

---

## Banned

Each verdict and its reason live in the sub-doc named beside it; this roster only indexes them.

- **class component** · **`forwardRef`** →
  [components](components.md)
- **`useOptimistic`** → [state & data](../../../mla/domains/data/state-and-data.md) § *Mutations*
- **`useInsertionEffect`** · **`useDebugValue`** · **`useActionState`** → [hooks](hooks.md)

---

## Neighbours

- [vue](../vue/vue.md) — the same roster for the other framework
- [typescript](../typescript/typescript.md) — the language layer every construct here sits on
- [constructs](../../../mla/constructs/constructs.md) — the app roles these constructs are shaped into
- [hooks](../../../mla/constructs/behavior/hooks.md) — naming, return shape and lifecycle for a custom hook
- [state & data](../../../mla/domains/data/state-and-data.md) — where shared state is allowed to live
