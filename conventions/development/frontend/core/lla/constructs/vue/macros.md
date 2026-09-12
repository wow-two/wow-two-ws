# Macros

*Last updated: 2026-09-10*

> The `<script setup>` block, the seven compiler macros it may call, and `withDefaults`.
> Purpose — the macros are the whole typed surface of a component, so a missing one is a prop nobody can see.
> Use case — reach here when opening a new `.vue` file, or when a parent needs something the child does not declare.

## The constructs

| Construct | Is | Verdict |
| --- | --- | --- |
| `<script setup>` | the block compiled into the instance's `setup()` | `use` |
| plain `<script lang="ts">` | the module-scope block that may hold an `export` | `use` |
| Options API (`data` · `methods` · `computed:`) | the pre-Composition object component | `banned` |
| `defineOptions` | the component name and the `inheritAttrs` gate | `use` |
| `defineProps<T>()` | the typed input surface, compiled to a runtime declaration | `use` |
| `withDefaults` | the value an optional prop takes when omitted | `use` |
| `defineEmits<T>()` | the output names, removed from `useAttrs()` once declared | `use` |
| `defineSlots<T>()` | the slot names and each slot's scope type | `use` |
| `defineExpose` | the members a parent reaches through its template ref | `use` |
| `defineModel` | one ref standing for a prop and its `update:` emit | `banned` |
| reactive props destructure (`const { x } = defineProps()`) | 3.5's compiler-tracked destructure | `banned` |

- must call every macro at the top of `<script setup>`, in the order
  [vue SFC](vue-sfc.md) § *Order inside `<script setup>`* fixes.
- must type `defineProps` through a named `interface`, never an inline object literal — the interface is what
  [constructs](../../../mla/constructs/constructs.md) § *Props interface* marks `readonly` and documents.
- must read a prop as `props.x` at the point of use, never through a `const` copied at setup root — the copy
  snapshots, and the template renders the stale value.
- may snapshot a **seed** prop, and only a seed — one named `default*` / `initial*`, or one feeding a
  documented read-once option such as `useControlled`'s `default:`. The name is what marks the intent.
- must preserve live prop reads across a boundary with a getter, ref or `computed`; a plain value is a snapshot.
A snapshot read is legitimate in four shapes, and in no others:

| Shape | Why it holds |
|---|---|
| `ref(props.defaultOpen)` · `ref(props.initialSnap)` | seeds uncontrolled state once; the prop name is the contract |
| `useControlled({ default: props.x })` | the option is read-once by contract; `controlled:` takes a getter |
| `provide(key, props.client)` for a single instance | a query client or a flag client is created once, never swapped |
| a plain read paired with a `watch` that re-syncs it | the watch restores what the read dropped |

- must take a default through `withDefaults`, never a destructure default — the props `interface` stays the
  one typed surface, and the member is declared optional (`size?: number`) for the default to fill.
- must give a non-primitive default a factory (`items: () => []`); Vue calls it once per instance.
- controlled prop and emit spelling → [Controlled props](#controlled-props).
- must declare a slot in `defineSlots` before rendering it; an undeclared slot type-checks as `any` at the call site.
- must expose only a documented imperative or element-handle contract; do not substitute `$el` for that contract.
- must inventory consumers before removing an exposed root; preserve focus, positioning and measurement access.
- must define the handle's target and null lifetime across mount, conditional roots, multiple roots and portals.
- must not rely on `$el` as a stable `HTMLElement`; it may be undefined, a text node or a comment placeholder.
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
- **`defineModel`** — use a named props interface plus an `update:*` emit under the house source-form policy;
  the macro itself supports named models and typed options.
- **reactive props destructure** — reach for `props.x` or a `computed` over it; the binding is a compiler rewrite,
  so a helper that receives it outside the template gets a plain value and stops tracking silently.

---

## Controlled props

- state semantics → [controlled state](../../notation/naming/props.md#controlled-state).
- must use `modelValue/defaultValue/update:modelValue` for the primary value.
- must use `open/defaultOpen/update:open` or `checked/defaultChecked/update:checked` for named state axes.
- must keep the controlled prop optional when uncontrolled use is supported.
- must default an optional Boolean model to `undefined`; Vue's absent Boolean cast must not select controlled mode.
- must not add a second model alias such as `isOpen` or emit a duplicate change event for the same intent.

```ts
interface DisclosureProps {
  readonly open?: boolean;
  readonly defaultOpen?: boolean;
}
const props = withDefaults(defineProps<DisclosureProps>(), { open: undefined, defaultOpen: false });
const emit = defineEmits<{ 'update:open': [value: boolean] }>();
// The owner chooses mode from props.open !== undefined before applying the seed.
```

---

## Neighbours

- [vue](vue.md) — the full construct roster
- [reactivity](reactivity.md) — what the macros' values are read through
- [vue SFC](vue-sfc.md) — block order, attribute forwarding, JSDoc verbs
