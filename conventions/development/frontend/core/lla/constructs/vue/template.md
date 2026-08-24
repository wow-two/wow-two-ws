# Template

*Last updated: 2026-08-19*

> Every directive, slot form and template-ref form a `<template>` may carry, and the ones banned outright.
> Purpose — the template is compiled, so a directive's cost is a render decision, not a styling one.
> Use case — reach here before writing a directive or a slot this codebase has not written before.

## The constructs

| Construct | Is | Uses | Verdict |
|---|---|---|---|
| `v-if` · `v-else-if` · `v-else` | a branch that creates and destroys the subtree | 333 · 18 · 70 | `use` |
| `v-show` | a branch that toggles `display` and keeps the subtree | 1 | `use with care` |
| `v-for` | the list repeat | 103 | `use` |
| `:key` | the identity Vue diffs a keyed child on | 104 | `use` |
| `v-bind` · the `:` shorthand | one attribute or prop bound to an expression | 2454 | `use` |
| `v-bind="obj"` | a whole object spread onto the element | 354 | `use` |
| `v-on` · the `@` shorthand | a listener bound to a DOM event or an emit | 409 | `use` |
| event modifiers (`.stop` · `.self`) | the wrapper Vue compiles around a listener | 2 | `use with care` |
| key modifiers (`.enter` · `.esc` · `.delete`) | a listener gated on Vue's own key alias | 0 | `banned` |
| `v-model` · `v-model:{arg}` | a prop and its `update:` emit written as one binding | 9 | `use` |
| `v-model` modifiers (`.trim` · `.number` · `.lazy`) | a transform between the DOM value and state | 0 | `banned` |
| `v-html` | an element's `innerHTML` set from a string | 1 | `use with care` |
| `v-text` | the same interpolation `{{ }}` already does | 0 | `banned` |
| `v-once` · `v-memo` · `v-pre` · `v-cloak` | the update-skipping and pre-hydration directives | 0 | `banned` |
| custom directive (`vFocus` · `app.directive`) | behaviour attached to an element by name | 0 | `banned` |
| default slot | the children a parent passes | 443 | `use` |
| named slot (`<slot name="x">`) | a second, addressable content hole | 187 | `use` |
| scoped slot (`<slot :item="…">`) | a hole that hands data back out to the parent | 26 | `use` |
| `v-slot` · the `#` shorthand | the consumer half of a named or scoped slot | 1 | `use` |
| `$slots` | the runtime test for whether a slot was filled | 36 | `use` |
| `useTemplateRef('x')` · `ref="x"` | the script handle on a node, and its template half | 311 · 349 | `use` |
| function ref (`:ref="fn"`) | a callback invoked with the node on each patch | 0 | `banned` |

- must reach for `v-if` by default, and `v-show` only where the hidden subtree must keep DOM state or measurable size.
- must give every `v-for` a `:key` that identifies the item, never the loop index — a keyed reorder otherwise reuses
  the wrong child and carries its focus, its input value and its transition state to a different row.
- must gate a key press on the shared `Key` const object (`foundation/utils/KeyboardExtensions`), read off `event.key`.
- must take a node through `useTemplateRef`, paired with a matching literal `ref="x"` in the template.
- must reach for a named slot before a `VNodeChild` prop; the prop stays for React SDK parity.
- must not pass a string that arrived over the wire to `v-html` — the one live site runs a sanitising renderer first
  and carries its own `eslint-disable-next-line vue/no-v-html` with the reason on it.

```vue
<!-- ✅ the key identifies the row, so a reorder moves the row rather than its contents -->
<li v-for="code in codes" :key="code.id">{{ code.label }}</li>

<!-- ❌ the index is position, not identity — a prepend re-labels every existing row -->
<li v-for="(code, i) in codes" :key="i">{{ code.label }}</li>
```

---

## Banned

- **key modifiers** — reach for the shared `Key` const object and an `event.key` check (68 sites); Vue's aliases are a
  separate vocabulary, so a template alias and a script check drift apart on the same physical key.
- **`v-model` modifiers** — reach for a `computed` or the form layer ([forms](../../../mla/domains/forms/forms.md));
  they apply only to a native element's `v-model`, so the same prop behaves differently on a component than on an
  `<input>`, and the form engine never sees the value the user actually typed.
- **`v-text`** — reach for `{{ }}`; it sets the same `textContent` while hiding the expression from the template's own
  reading order.
- **`v-once` · `v-memo` · `v-pre` · `v-cloak`** — reach for a correct render; `v-memo`'s dependency list goes stale
  with no error, `v-once` and `v-pre` freeze a subtree the props still change, and `v-cloak` needs a CSS rule for a
  flash a bundled SPA never shows.
- **custom directive** — reach for a composable plus a wrapper component; a directive's hooks run outside the setup
  scope, so `onScopeDispose` never fires for it, and it carries no typed contract a consumer can check.
- **function ref** — reach for `useTemplateRef`; the callback fires with `null` and then the node on every patch, so
  any work inside it runs twice per update.

---

## Neighbours

- [vue](vue.md) — the full construct roster
- [html](../html/html.md) — the elements these directives are written on
- [built-ins](builtins.md) — the components a template may render without importing
