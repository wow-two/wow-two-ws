# React 19

*Last updated: 2026-08-23*

> Every construct React 19 offers a component or a hook, and the ones banned outright.
> Purpose — React 19 retired a set of constructs the SDK still leans on, so a verdict here is also a migration order.
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

Exhaustive through React 19.1. `SDK` counts non-comment call sites in `@wow-two-beta/ui` (281 `.tsx`); `App` counts
`smart-qr` (49 `.tsx`). A construct we have never written still carries a verdict.

| Construct | Is | SDK | App | Verdict |
|---|---|---|---|---|
| function component | a component declared as a function | 281 files | 49 files | `use` |
| class component | the `extends Component` form | 0 | 0 | `banned` |
| `useState` | a state slot and its setter | 167 | 27 | `use` |
| `useReducer` | a state slot driven by a reducer | 1 | 0 | `use with care` |
| `useRef` | a mutable box that survives a render | 247 | 4 | `use` |
| `useMemo` · `useCallback` | a value or a function cached across renders | 108 · 209 | 1 · 2 | `use` |
| `useEffect` | a post-commit effect with a cleanup | 156 | 9 | `use` |
| `useLayoutEffect` | the same effect, run before paint | 12 | 0 | `use with care` |
| `useInsertionEffect` | the CSS-in-JS injection point | 0 | 0 | `banned` |
| `useId` | an id stable across server and client | 49 | 0 | `use` |
| `useSyncExternalStore` | a subscription to a store outside React | 16 | 0 | `use` |
| `useTransition` · `useDeferredValue` | a render marked non-urgent | 0 | 0 | `use with care` |
| `useOptimistic` | state shown ahead of the server's answer | 0 | 0 | `banned` |
| `useActionState` | form state driven by a Server Action | 0 | 0 | `banned` |
| `use(promise)` · `use(context)` | a conditional read of a promise or a context | 0 | 0 | `use with care` |
| `useContext` · `createContext` | the shared-state read, and the context itself | 51 · 48 | 0 | `use` |
| `useImperativeHandle` | the instance API a parent reaches through a ref | 10 | 0 | `use with care` |
| `useDebugValue` | a devtools label on a custom hook | 0 | 0 | `banned` |
| `forwardRef` | the pre-19 wrapper that passed a ref past props | 324 | 0 | `banned` |
| ref as a prop | React 19's own `ref` — a prop like any other | 0 | 1 | `use` |
| `memo` | a component skipped when its props compare equal | 0 | 0 | `use with care` |
| `createPortal` | children rendered under a different DOM parent | 1 | 0 | `use with care` |
| `<Suspense>` · `lazy` | an await boundary, and a dynamically imported child | 1 · 1 | 0 | `use with care` |
| error boundary (`componentDidCatch`) | the class React still requires for a throw | 0 | 0 | `use with care` |
| Server Components · `'use client'` · `'use server'` | the RSC split and its directives | 0 | 0 | `banned` |
| fragment `<>` · `<Fragment key>` | children grouped with no element | 20 · 4 | 22 · 1 | `use` |
| `key` | the identity React diffs a list child on | 105 | 29 | `use` |
| JSX spread `{...props}` | every remaining prop forwarded at once | 355 | 0 | `use` |
| `&&` · ternary in JSX | the two conditional-render idioms | 260 · 181 | 49 · 12 | `use` |
| `dangerouslySetInnerHTML` | an element's `innerHTML` set from a string | 1 | 1 | `use with care` |
| `createElement` · `cloneElement` | an element built or re-emitted without JSX | 9 · 12 | 0 | `use with care` |
| `Children.*` · `isValidElement` | the legacy walk over an opaque `children` | 19 · 17 | 0 | `use with care` |
| `startTransition` · `flushSync` | the imperative scheduling escapes | 0 | 0 | `use with care` |

```tsx
// ✅ React 19 — ref is a prop, and the props interface owns it
export function SearchInput({ ref, ...rest }: SearchInputProps) { … }

// ❌ forwardRef — deprecated in 19, and it splits the ref's type off the props interface
export const SearchInput = forwardRef<HTMLInputElement, SearchInputProps>((props, ref) => …);
```

---

## Banned

Each verdict and its reason live in the sub-doc named beside it; this roster only indexes them.

- **class component** · **`forwardRef`** · **Server Components** · **`'use client'`** · **`'use server'`** →
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
