# Template

*Last updated: 2026-09-10*

> Every directive, slot form and template-ref form a `<template>` may carry, and the ones banned outright.
> Purpose — the template is compiled, so a directive's cost is a render decision, not a styling one.
> Use case — reach here before writing a directive or a slot this codebase has not written before.

## The constructs

| Construct | Is | Verdict |
| --- | --- | --- |
| `v-if` · `v-else-if` · `v-else` | a branch that creates and destroys the subtree | `use` |
| `v-show` | a branch that toggles `display` and keeps the subtree | `use with care` |
| `v-for` | the list repeat | `use` |
| `:key` | the identity Vue diffs a keyed child on | `use` |
| `v-bind` · the `:` shorthand | one attribute or prop bound to an expression | `use` |
| `v-bind="obj"` | a whole object spread onto the element | `use` |
| `v-on` · the `@` shorthand | a listener bound to a DOM event or an emit | `use` |
| event modifiers (`.stop` · `.self`) | the wrapper Vue compiles around a listener | `use with care` |
| key modifiers (`.enter` · `.esc` · `.delete`) | a listener gated on Vue's own key alias | `banned` |
| `v-model` · `v-model:{arg}` | a prop and its `update:` emit written as one binding | `use` |
| `v-model` modifiers (`.trim` · `.number` · `.lazy`) | a transform between the DOM value and state | `banned` |
| `v-html` | an element's `innerHTML` set from a string | `use with care` |
| `v-text` | the same interpolation `{{ }}` already does | `banned` |
| `v-once` · `v-memo` · `v-pre` · `v-cloak` | the update-skipping and pre-hydration directives | `banned` |
| custom directive (`vFocus` · `app.directive`) | behaviour attached to an element by name | `banned` |
| default slot | the children a parent passes | `use` |
| named slot (`<slot name="x">`) | a second, addressable content hole | `use` |
| scoped slot (`<slot :item="…">`) | a hole that hands data back out to the parent | `use` |
| `v-slot` · the `#` shorthand | the consumer half of a named or scoped slot | `use` |
| `$slots` | the runtime test for whether a slot was filled | `use` |
| `useTemplateRef('x')` · `ref="x"` | the script handle on a node, and its template half | `use` |
| function ref (`:ref="fn"`) | a callback invoked with the node on each patch | `banned` |

- must default to `v-if`; use `v-show` to preserve instance/DOM state, not measurable layout while hidden.
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

- **key modifiers** — reach for the shared `Key` const object and an `event.key` check; Vue's aliases are a
  separate vocabulary, so a template alias and a script check drift apart on the same physical key.
- **`v-model` modifiers** — use an explicit parser or the [form layer](../../../mla/domains/forms/forms.md);
  custom components may implement modifiers, but this codebase keeps normalization at the parsing boundary.
- **`v-text`** — reach for `{{ }}`; it sets the same `textContent` while hiding the expression from the template's own
  reading order.
- **`v-once` · `v-memo` · `v-pre` · `v-cloak`** — reach for a correct render; `v-memo`'s dependency list goes stale
  with no error, `v-once` and `v-pre` freeze a subtree the props still change, and `v-cloak` needs a CSS rule for a
  flash a bundled SPA never shows.
- **custom directive** — use a composable plus wrapper under the house ownership policy;
  directives have typed hooks and explicit unmount cleanup, but follow a separate lifecycle.
- **function ref** — default to `useTemplateRef`; Vue calls function refs on updates and passes null on unmount,
  not an unconditional null/node pair on every patch.

---

## Neighbours

- [vue](vue.md) — the full construct roster
- [html](../html/html.md) — the elements these directives are written on
- [built-ins](builtins.md) — the components a template may render without importing
