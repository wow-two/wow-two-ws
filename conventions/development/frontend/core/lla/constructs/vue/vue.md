# Vue 3

*Last updated: 2026-09-10*

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

| Construct | Is | Verdict |
| --- | --- | --- |
| `<script setup>` | the compiled instance block | `use` |
| Options API (`data` · `methods`) | the pre-Composition object component | `banned` |
| `defineOptions` · `defineProps` | the name / `inheritAttrs` gate, and the input shape | `use` |
| `defineEmits` · `defineSlots` | the declared output names, and the typed slot surface | `use` |
| `defineExpose` · `withDefaults` | the instance API a parent may call, and a prop's default | `use` |
| `defineModel` | a prop and its `update:` emit declared as one ref | `banned` |
| `ref` · `shallowRef` | a tracked box, deep or one level | `use` |
| `computed` | a cached value derived from tracked sources | `use` |
| `reactive` | a deep proxy standing in for the object | `use with care` |
| `shallowReactive` · `markRaw` | the one-level proxy, and the opt-out from proxying | `banned` |
| `readonly` | a proxy that drops writes | `use with care` |
| `watch` | an effect over named sources | `use` |
| `watchEffect` | an effect whose sources come from running it | `use with care` |
| `watchPostEffect` · `flush: 'post'` | an effect that runs after the DOM patch | `use` |
| `flush: 'sync'` · `watchSyncEffect` | an effect that runs inside the write | `use with care` · `banned` |
| `nextTick` | a promise resolving after the next patch | `use with care` |
| `toValue` · `MaybeRefOrGetter` | the read, and the type of anything a composable accepts | `use` |
| `toRef` · `toRefs` | a ref pointing into a reactive object | `banned` |
| `onScopeDispose` | teardown that runs when the owning scope stops | `use` |
| `effectScope` | a disposal scope with no component behind it | `use with care` |
| `onMounted` · `onBeforeUnmount` | the DOM-ready point, and teardown | `use` |
| `onUnmounted` · `onUpdated` · `onErrorCaptured` | late hooks; a descendant throw | `use with care` |
| `onActivated` · `onRenderTracked` | the `KeepAlive` and debug hooks | `banned` |
| `onServerPrefetch` | an explicit SSR delivery target's hook | `use with care` |
| `provide` · `inject` | a value passed down a subtree by key | `use` |
| `useAttrs` · `useSlots` · `useId` | the undeclared attrs, the slot set, an SSR-safe id | `use` |
| `Teleport` | children rendered under a different DOM parent | `use with care` |
| `Transition` · `TransitionGroup` | class-driven enter / leave choreography | `banned` |
| `KeepAlive` · `Suspense` | a cached instance, and an async-setup boundary | `banned` |
| `<component :is>` | the element or component chosen at runtime | `use` |
| `defineAsyncComponent` | a component resolved through a dynamic `import()` | `use with care` |
| `v-if` · `v-else-if` · `v-else` | branches that create and destroy the subtree | `use` |
| `v-show` | a branch that toggles `display` only | `use with care` |
| `v-for` · `:key` | the list repeat, and the identity Vue diffs on | `use` |
| `v-bind` · `:` shorthand · `v-bind="obj"` | one attribute bound, or a whole object spread | `use` |
| `v-on` · `@` shorthand | a listener bound to an event | `use` |
| event modifiers (`.stop` · `.prevent`) | the listener wrapper Vue generates | `use with care` |
| key modifiers (`.enter` · `.esc`) | a listener gated on Vue's own key alias | `banned` |
| `v-model` · `v-model:arg` | the prop / `update:` pair written as one binding | `use` |
| `v-model` modifiers (`.trim` · `.number` · `.lazy`) | a transform applied between DOM and state | `banned` |
| `v-html` | an element's inner HTML set from a string | `use with care` |
| `v-text` · `v-once` · `v-memo` · `v-pre` · `v-cloak` | interpolation and update-skipping | `banned` |
| custom directive (`vFocus` · `app.directive`) | behaviour attached to an element by name | `banned` |
| slots — default · named · scoped | content the parent supplies | `use` |
| `useTemplateRef` · `ref="x"` | the script handle on a rendered node, and its template half | `use` |
| `h()` · render function · `defineComponent` | vnodes authored in TypeScript | `use with care` |
| `cloneVNode` · `mergeProps` | a vnode re-emitted with added props | `use with care` |

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
