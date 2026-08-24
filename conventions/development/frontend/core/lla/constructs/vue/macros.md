# Macros

*Last updated: 2026-08-19*

> The `<script setup>` block, the seven compiler macros it may call, and `withDefaults`.
> Purpose — the macros are the whole typed surface of a component, so a missing one is a prop nobody can see.
> Use case — reach here when opening a new `.vue` file, or when a parent needs something the child does not declare.

## The constructs

| Construct | Is | Uses | Verdict |
|---|---|---|---|
| `<script setup>` | the block compiled into the instance's `setup()` | 406 SFCs | `use` |
| plain `<script lang="ts">` | the module-scope block that may hold an `export` | 404 SFCs | `use` |
| Options API (`data` · `methods` · `computed:`) | the pre-Composition object component | 0 | `banned` |
| `defineOptions` | the component name and the `inheritAttrs` gate | 407 | `use` |
| `defineProps<T>()` | the typed input surface, compiled to a runtime declaration | 330 | `use` |
| `withDefaults` | the value an optional prop takes when omitted | 279 | `use` |
| `defineEmits<T>()` | the output names, removed from `useAttrs()` once declared | 123 | `use` |
| `defineSlots<T>()` | the slot names and each slot's scope type | 210 | `use` |
| `defineExpose` | the members a parent reaches through its template ref | 316 | `use` |
| `defineModel` | one ref standing for a prop and its `update:` emit | 0 | `banned` |
| reactive props destructure (`const { x } = defineProps()`) | 3.5's compiler-tracked destructure | 0 | `banned` |

- must call every macro at the top of `<script setup>`, in the order
  [vue SFC](vue-sfc.md) § *Order inside `<script setup>`* fixes.
- must type `defineProps` through a named `interface`, never an inline object literal — the interface is what
  [constructs](../../../mla/constructs/constructs.md) § *Props interface* marks `readonly` and documents.
- must read a prop as `props.x` at the point of use, never through a `const` copied at setup root — the copy
  snapshots, and the template renders the stale value.
- may snapshot a **seed** prop, and only a seed — one named `default*` / `initial*`, or one feeding a
  documented read-once option such as `useControlled`'s `default:`. The name is what marks the intent.
- must hand a prop that crosses a boundary as a getter or a `computed`, never as a plain value —
  `provide`, a register call and a composable argument all freeze what they receive.
A snapshot read is legitimate in four shapes, and in no others:

| Shape | Why it holds |
|---|---|
| `ref(props.defaultOpen)` · `ref(props.initialSnap)` | seeds uncontrolled state once; the prop name is the contract |
| `useControlled({ default: props.x })` | the option is read-once by contract; `controlled:` takes a getter |
| `provide(key, props.client)` for a single instance | a query client or a flag client is created once, never swapped |
| a plain read paired with a `watch` that re-syncs it | the watch restores what the read dropped |

- must not hand a live prop to `provide`, a register call or a composable as a plain value — every consumer
  freezes at the first value it saw.

- must take a default through `withDefaults`, never a destructure default — the props `interface` stays the
  one typed surface, and the member is declared optional (`size?: number`) for the default to fill.
- must give a non-primitive default a factory (`items: () => []`); Vue calls it once per instance.
- must pair every controlled prop with an `'update:{prop}'` emit so a consumer may write `v-model:{prop}`.
- must declare a slot in `defineSlots` before rendering it; an undeclared slot type-checks as `any` at the call site.
- must keep `defineExpose` to the imperative API — a parent already reads the root node off `$el`.
- must not read a declared emit's listener back out of `useAttrs()`; Vue removes it, so presence cannot be
  detected — a callback whose *presence* changes what renders stays a prop instead.

```ts
// ✅ named interface, defaults through withDefaults, the write travels back as an emit
const props = withDefaults(defineProps<TagProps>(), { closable: false });
const emit = defineEmits<{ 'update:modelValue': [value: string]; 'value-change': [value: string] }>();

// ❌ inline literal — no interface to mark readonly, no member to document
const props = defineProps<{ closable?: boolean }>();
```

---

## Banned

- **Options API** — reach for `<script setup>`; `this` is typed through a declaration-merging shim, so a prop a macro
  added is invisible to it, and `defineExpose` / `defineSlots` have no object key to live under.
- **`defineModel`** — reach for `defineProps` + an `'update:x'` emit; the prop it declares sits outside the props
  `interface`, so it cannot be `readonly`, cannot be documented, and cannot carry the alias spelling
  (`open` / `isOpen`) that all 14 dual-surface components ship.
- **reactive props destructure** — reach for `props.x` or a `computed` over it; the binding is a compiler rewrite,
  so a helper that receives it outside the template gets a plain value and stops tracking silently.

---

## Neighbours

- [vue](vue.md) — the full construct roster
- [reactivity](reactivity.md) — what the macros' values are read through
- [vue SFC](vue-sfc.md) — block order, attribute forwarding, JSDoc verbs
