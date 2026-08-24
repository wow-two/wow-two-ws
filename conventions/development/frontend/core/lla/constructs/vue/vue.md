# Vue 3

*Last updated: 2026-08-23*

> Every construct Vue 3 offers a `.vue` file or a composable, and the ones banned outright.
> Purpose — Vue is a second baseline under TypeScript, and a wrong pick costs a lost update, a leak, or an XSS.
> Use case — reach here before writing a macro, a directive or a reactive primitive new to this codebase.

## The groups

| Group | Covers | Doc |
|---|---|---|
| script + macros | `<script setup>` · the seven `define*` macros · `withDefaults` | [macros](macros.md) |
| reactivity | `ref` · `computed` · the `watch` family · flush timing · scope | [reactivity](reactivity.md) |
| template | directives · slots · template refs | [template](template.md) |
| built-ins | `Teleport` · `Transition` · `KeepAlive` · `Suspense` · `<component>` | [built-ins](builtins.md) |
| composition | lifecycle hooks · `provide` / `inject` · `h()` · `defineComponent` | [composition](composition.md) |

Block layout, in-file order and the JSDoc verbs live in [vue SFC](vue-sfc.md), not here.

---

## The constructs

Exhaustive through Vue 3.5. `Uses` counts non-comment call sites in `@wow-two-beta/ui-vue` (406 SFCs); a construct we
have never written still carries a verdict.

| Construct | Is | Uses | Verdict |
|---|---|---|---|
| `<script setup>` | the compiled instance block | 406 | `use` |
| Options API (`data` · `methods`) | the pre-Composition object component | 0 | `banned` |
| `defineOptions` · `defineProps` | the name / `inheritAttrs` gate, and the input shape | 407 · 330 | `use` |
| `defineEmits` · `defineSlots` | the declared output names, and the typed slot surface | 123 · 210 | `use` |
| `defineExpose` · `withDefaults` | the instance API a parent may call, and a prop's default | 316 · 279 | `use` |
| `defineModel` | a prop and its `update:` emit declared as one ref | 0 | `banned` |
| `ref` · `shallowRef` | a tracked box, deep or one level | 109 · 120 | `use` |
| `computed` | a cached value derived from tracked sources | 1811 | `use` |
| `reactive` | a deep proxy standing in for the object | 1 | `use with care` |
| `shallowReactive` · `markRaw` | the one-level proxy, and the opt-out from proxying | 0 · 0 | `banned` |
| `readonly` | a proxy that drops writes | 1 | `use with care` |
| `watch` | an effect over named sources | 107 | `use` |
| `watchEffect` | an effect whose sources come from running it | 3 | `use with care` |
| `watchPostEffect` · `flush: 'post'` | an effect that runs after the DOM patch | 19 · 45 | `use` |
| `flush: 'sync'` · `watchSyncEffect` | an effect that runs inside the write | 3 · 0 | `use with care` · `banned` |
| `nextTick` | a promise resolving after the next patch | 10 | `use with care` |
| `toValue` · `MaybeRefOrGetter` | the read, and the type of anything a composable accepts | 194 · 198 | `use` |
| `toRef` · `toRefs` | a ref pointing into a reactive object | 0 · 0 | `banned` |
| `onScopeDispose` | teardown that runs when the owning scope stops | 46 | `use` |
| `effectScope` | a disposal scope with no component behind it | 0 | `use with care` |
| `onMounted` · `onBeforeUnmount` | the DOM-ready point, and teardown | 56 · 18 | `use` |
| `onUnmounted` · `onUpdated` · `onErrorCaptured` | late hooks; a descendant throw | 6 · 3 · 1 | `use with care` |
| `onActivated` · `onRenderTracked` · `onServerPrefetch` | the `KeepAlive`, debug and SSR hooks | 0 | `banned` |
| `provide` · `inject` | a value passed down a subtree by key | 57 · 56 | `use` |
| `useAttrs` · `useSlots` · `useId` | the undeclared attrs, the slot set, an SSR-safe id | 335 · 55 · 49 | `use` |
| `Teleport` | children rendered under a different DOM parent | 1 | `use with care` |
| `Transition` · `TransitionGroup` | class-driven enter / leave choreography | 0 · 0 | `banned` |
| `KeepAlive` · `Suspense` | a cached instance, and an async-setup boundary | 0 · 0 | `banned` |
| `<component :is>` | the element or component chosen at runtime | 27 | `use` |
| `defineAsyncComponent` | a component resolved through a dynamic `import()` | 0 | `use with care` |
| `v-if` · `v-else-if` · `v-else` | branches that create and destroy the subtree | 333 · 18 · 70 | `use` |
| `v-show` | a branch that toggles `display` only | 1 | `use with care` |
| `v-for` · `:key` | the list repeat, and the identity Vue diffs on | 103 · 104 | `use` |
| `v-bind` · `:` shorthand · `v-bind="obj"` | one attribute bound, or a whole object spread | 2454 · 354 | `use` |
| `v-on` · `@` shorthand | a listener bound to an event | 409 | `use` |
| event modifiers (`.stop` · `.prevent`) | the listener wrapper Vue generates | 2 | `use with care` |
| key modifiers (`.enter` · `.esc`) | a listener gated on Vue's own key alias | 0 | `banned` |
| `v-model` · `v-model:arg` | the prop / `update:` pair written as one binding | 9 | `use` |
| `v-model` modifiers (`.trim` · `.number` · `.lazy`) | a transform applied between DOM and state | 0 | `banned` |
| `v-html` | an element's inner HTML set from a string | 1 | `use with care` |
| `v-text` · `v-once` · `v-memo` · `v-pre` · `v-cloak` | interpolation and update-skipping | 0 | `banned` |
| custom directive (`vFocus` · `app.directive`) | behaviour attached to an element by name | 0 | `banned` |
| slots — default · named · scoped | content the parent supplies | 443 · 187 · 26 | `use` |
| `useTemplateRef` · `ref="x"` | the script handle on a rendered node, and its template half | 311 · 349 | `use` |
| `h()` · render function · `defineComponent` | vnodes authored in TypeScript | 8 · 17 | `use with care` |
| `cloneVNode` · `mergeProps` | a vnode re-emitted with added props | 6 · 5 | `use with care` |

```ts
// ✅ the props interface stays the typed surface, and the emit carries the write back
const props = withDefaults(defineProps<ModalProps>(), { open: undefined });
const emit = defineEmits<{ 'update:open': [open: boolean] }>();

// ❌ defineModel declares the prop outside ModalProps, so no member is readonly and none is documented
const open = defineModel<boolean>('open');
```

---

## Banned

Each verdict and its reason live in the sub-doc named beside it; this roster only indexes them.

- **Options API** · **`defineModel`** → [macros](macros.md)
- **`Transition`** · **`TransitionGroup`** · **`KeepAlive`** · **`Suspense`** → [built-ins](builtins.md)
- **custom directive** → [template](template.md)
- **`toRef`** · **`toRefs`** → [reactivity](reactivity.md)

---

## Neighbours

- [react](../react/react.md) — the same roster for the other framework
- [typescript](../typescript/typescript.md) — the language layer every construct here sits on
- [vue SFC](vue-sfc.md) — block layout, in-file order, attribute forwarding
- [constructs](../../../mla/constructs/constructs.md) — the app roles these constructs are shaped into
