# Component forms

*Last updated: 2026-08-19*

> How a React component is declared, how a ref reaches it, and which of React's wrappers survive React 19.
> Purpose — React 19 turned `ref` into a prop, which retires the wrapper 233 of the SDK's files are still built on.
> Use case — reach here when declaring a component, forwarding a ref, or wondering whether a wrapper is still needed.

## The constructs

`SDK` counts `@wow-two-beta/ui`; `App` counts `smart-qr`.

| Construct | Is | SDK | App | Verdict |
|---|---|---|---|---|
| function component | a component declared as a function over props | 281 files | 49 files | `use` |
| class component | the `extends Component` form, with lifecycle methods | 0 | 0 | `banned` |
| ref as a prop | React 19's `ref` — a prop the props interface declares | 0 | 1 | `use` |
| `forwardRef` | the pre-19 wrapper that carried a ref past props | 324 | 0 | `banned` |
| `useImperativeHandle` | an object handed up in place of the node | 10 | 0 | `use with care` |
| `memo` | a component skipped when its props compare equal | 0 | 0 | `use with care` |
| `ComponentProps<T>` | the props of an element or component, ref included | 5 | 0 | `use` |
| `ComponentPropsWithoutRef<T>` | the same, minus the ref `forwardRef` re-added | 164 | 0 | `banned` |
| `lazy` | a component behind a dynamic `import()` | 1 | 0 | `use with care` |
| Server Component | a component rendered only on the server | 0 | 0 | `banned` |
| `'use client'` · `'use server'` | the directives that mark the RSC boundary | 0 | 0 | `banned` |

- must declare a component as an exported `function`; its folder shape is
  [constructs](../../../mla/constructs/constructs.md) § *Folder*.
- must take one `props` parameter, destructured in the signature — `readonly` carries through, inline
  defaults stay clean, and a destructured `const` holds a narrowing across closures that a `props.x` read
  re-widens ([constructs](../../../mla/constructs/constructs.md) § *Props interface*).
- must hoist a non-primitive default to module scope — an inline `{ items = [] }` mints a fresh identity
  every render, so every deps array that reads it churns.
- must declare `ref` on the props interface when a consumer needs the node, and pass it straight to the element.
- must reach for `ComponentProps<'button'>` over `ComponentPropsWithoutRef<'button'>` — the ref belongs in the props.
- must measure before reaching for `memo`; a memo over a component taking a fresh object prop never hits.
- must not split a component into a wrapper and an inner just so a ref can pass through it.

```tsx
// ✅ ref is a prop, so the props interface stays the single typed surface
export function SearchInput({ ref, ...rest }: SearchInputProps) {
  return <input ref={ref} {...rest} />;
}

// ❌ forwardRef — the ref's type lives outside SearchInputProps, and devtools names it ForwardRef
export const SearchInput = forwardRef<HTMLInputElement, SearchInputProps>((props, ref) => …);
```

---

## Banned

- **class component** — reach for a function plus hooks; no hook runs in a class, so every SDK hook, every
  context read and `ref`-as-a-prop are unreachable from one. The single exception is an error boundary, which React
  still ships no function form of ([boundaries](boundaries.md)).
- **`forwardRef`** — reach for `ref` on the props interface; React 19 deprecates it and will remove it, the wrapper
  loses the inferred display name, and it forces the props type to be spelled `WithoutRef` so the ref can be added
  back by the wrapper — two declarations of one prop.
- **`ComponentPropsWithoutRef<T>`** — reach for `ComponentProps<T>`; it exists only to strip the ref that
  `forwardRef` re-attached, so every one of its 164 sites is a `forwardRef` site by another name.
- **Server Components · `'use client'` · `'use server'`** — no replacement is needed; every app here is a Vite SPA
  ([single-host serving](../../../../../../deployment/hosting/single-host-serving.md)), so the directives are inert
  strings, and a file marked `'use server'` ships what it claims is server code straight to the browser.

---

## Neighbours

- [react](react.md) — the full construct roster
- [hooks](hooks.md) — `useImperativeHandle` and the rest of the hook set
- [constructs](../../../mla/constructs/constructs.md) — folder, doc, props interface and JSX rules
