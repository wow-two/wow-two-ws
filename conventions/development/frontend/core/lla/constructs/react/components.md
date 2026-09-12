# Component forms

*Last updated: 2026-09-10*

> How a React component is declared, how a ref reaches it, and which of React's wrappers survive React 19.
> Purpose — keep the consumer ref in the component's declared props surface.
> Use case — reach here when declaring a component, forwarding a ref, or wondering whether a wrapper is still needed.

## The constructs

| Construct | Is | Verdict |
| --- | --- | --- |
| function component | a component declared as a function over props | `use` |
| class component | the `extends Component` form, with lifecycle methods | `banned` |
| ref as a prop | React 19's `ref` — a prop the props interface declares | `use` |
| `forwardRef` | the pre-19 wrapper that carried a ref past props | `banned` |
| `useImperativeHandle` | an object handed up in place of the node | `use with care` |
| `memo` | a component skipped when its props compare equal | `use with care` |
| `ComponentProps<T>` | the props of an element or component, ref included | `use` |
| `ComponentPropsWithoutRef<T>` | the same, minus the ref `forwardRef` re-added | `banned` |
| `lazy` | a component behind a dynamic `import()` | `use with care` |
| Server Component | a component rendered only on the server | `use with care` |
| `'use client'` · `'use server'` | the directives that mark the RSC boundary | `use with care` |

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
- **`forwardRef`** — use the React 19 ref prop under the house migration rule; the wrapper remains supported.
- **`ComponentPropsWithoutRef<T>`** — use `ComponentProps<T>` for a ref-forwarding surface;
  may use `Omit<ComponentProps<T>, 'ref'>` when the documented API intentionally does not expose a ref.

---

## Delivery

- must use Server Components and `'use client'` / `'use server'` only for an explicitly supported delivery target.
- app deployment → [app shape](../../../../shapes/app/app.md); library support →
  [compatibility](../../../../shapes/library/platform/compatibility.md). A directive alone supplies no server runtime.

---

## Controlled props

- state semantics → [controlled state](../../notation/naming/props.md#controlled-state).
- must use `value/defaultValue/onValueChange`, `checked/defaultChecked/onCheckedChange`, or
  `open/defaultOpen/onOpenChange` for their respective axes.
- must leave the model prop optional when uncontrolled use is supported; do not default it before selecting mode.
- must keep native event handlers separate from proposed-value callbacks when both are exposed.

---

## Ref lifetime

- must assign a consumer ref to the documented target, including clearing it when that target is removed.
- must release callback-ref resources through cleanup or the null path; never depend on a single attach call.
- must use a block-bodied callback for assignment so it does not accidentally return the assigned node.
- must validate ref composition when a primitive and consumer both need the same target.

---

## Neighbours

- [react](react.md) — the full construct roster
- [hooks](hooks.md) — `useImperativeHandle` and the rest of the hook set
- [constructs](../../../mla/constructs/constructs.md) — folder, doc, props interface and JSX rules
