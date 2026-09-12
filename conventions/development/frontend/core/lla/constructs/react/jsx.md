# JSX

*Last updated: 2026-09-10*

> Grouping, keying, spreading and conditional rendering in JSX, plus the element API underneath it.
> Purpose — every one of these compiles to a `jsx()` call, so an idiom's cost is a render decision, not a style one.
> Use case — reach here before writing a render idiom or touching `children` as data.

## The constructs

| Construct | Is | Verdict |
| --- | --- | --- |
| fragment `<>…</>` | children grouped with no element around them | `use` |
| `<Fragment key>` | the same group, when the group itself needs a key | `use` |
| `key` | the identity React diffs a list child on | `use` |
| JSX spread `{...props}` | every remaining prop forwarded at once | `use` |
| `&&` in JSX | render-if, written as a short-circuit | `use` |
| ternary in JSX | render-one-of-two | `use` |
| `dangerouslySetInnerHTML` | an element's `innerHTML` set from a string | `use with care` |
| `createElement` | an element built without JSX | `use with care` |
| `cloneElement` | an element re-emitted with added props | `use with care` |
| `Children.map` · `Children.toArray` | the legacy walk over an opaque `children` | `use with care` |
| `isValidElement` | the guard that a `children` entry is an element | `use with care` |
| `startTransition` · `flushSync` | the imperative scheduling escapes | `use with care` |

- must spread the rest props last, after the props the component sets itself, so a consumer can override
  ([constructs](../../../mla/constructs/constructs.md) § *JSX attributes*).
- must key a list child on the item's identity — a positional key reuses the wrong child on a reorder and carries its
  focus, its input value and its scroll position to a different row.
- must reach for `<Fragment key={id}>` when a list entry renders two siblings; `<>` takes no key.
- must reach for a render prop or a slot-shaped prop before `Children` / `cloneElement` — walking `children` couples
  the parent to the exact element the consumer wrote.
- must not `&&` on a number — `{items.length && <List/>}` renders a literal `0`; write `items.length > 0 && …`.
- must not pass a string that arrived over the wire to `dangerouslySetInnerHTML`; the two live sites take a sanitised
  markdown render and an SVG this codebase generated itself.

```tsx
// ✅ the test is a boolean, and the key is the row's identity
{codes.length > 0 && codes.map((code) => <Row key={code.id} code={code} />)}

// ❌ a zero-length list renders the character 0, and the index re-labels every row on a prepend
{codes.length && codes.map((code, i) => <Row key={i} code={code} />)}
```

---

## Banned

- **`createElement` as the authoring form** — reach for JSX; it takes an untyped props object, so a misspelled or
  removed prop compiles clean and fails at render. The nine live sites all pass a component *reference* to an API
  (the router's `errorElement`), which is the one shape JSX cannot express.
- **`dangerouslySetInnerHTML` over wire data** — reach for text interpolation, or a sanitising renderer; a string
  that reached the app over the network executes as script the moment it is assigned. The two live sites take a
  sanitised markdown render and an SVG this codebase generated itself.
- **a positional `key`** — reach for the item's id; React treats the key as identity, so a prepend reuses row 0's
  DOM node for a different item and carries its focus, its uncommitted input value and its scroll offset across.

---

## React types — import named, never the UMD namespace

- must import React types by name and reference them bare — `import { type ReactNode } from "react"` → `ReactNode`.
- must not reference the `React.*` UMD global (`React.ReactNode`, `React.JSX.Element`, `React.MouseEvent`) — with
  `jsx: "react-jsx"` no `React` value is in scope, so `React.*` triggers TS `ts(2686)`.
- must spell `React.JSX.Element` as `ReactElement`, or reach `JSX.Element` through
  `import { type JSX } from "react"`.

---

## Neighbours

- [react](react.md) — the full construct roster
- [style](../../notation/style/style.md) — the in-file layout these imports sit in
- [html](../html/html.md) — the elements JSX resolves to
- [constructs](../../../mla/constructs/constructs.md) § *JSX attributes* — attribute order and `cn()`
