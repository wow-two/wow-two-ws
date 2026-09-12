# Composition

*Last updated: 2026-09-10*

> The instance-bound constructs — lifecycle hooks, `provide` / `inject`, and the render-function escape.
> Purpose — each one binds to the current instance, so calling it in the wrong place fails at runtime, not at compile.
> Use case — a component needs the DOM, a subtree needs a value, or a template cannot express a render.

## The constructs

| Construct | Is | Verdict |
| --- | --- | --- |
| `onMounted` | the first point the rendered DOM exists | `use` |
| `onBeforeUnmount` | teardown while the DOM is still attached | `use` |
| `onUnmounted` | teardown after the node is gone | `use with care` |
| `onUpdated` | a callback after every patch of this component | `use with care` |
| `onErrorCaptured` | a hook for a throw from a descendant | `use with care` |
| `onBeforeMount` · `onBeforeUpdate` | the pre-render pair | `banned` |
| `onActivated` · `onDeactivated` | the hooks only `<KeepAlive>` fires | `banned` |
| `onRenderTracked` · `onRenderTriggered` | the dev-only dependency probes | `banned` |
| `onServerPrefetch` | the SSR-only await point | `use with care` |
| `provide` · `inject` | a value handed down a subtree by key | `use` |
| `InjectionKey<T>` | the typed token a provide / inject pair agrees on | `use` |
| `useAttrs` | the attributes neither a prop nor a declared emit claimed | `use` |
| `useSlots` | the runtime slot set | `use` |
| `useId` | an id stable across server and client | `use` |
| `defineComponent` | a component authored as an object rather than an SFC | `use with care` |
| `h()` · render function | a vnode built in TypeScript | `use with care` |
| `cloneVNode` · `mergeProps` | a vnode re-emitted with added props | `use with care` |
| `getCurrentInstance` | the internal handle on the running instance | `use with care` |

- must register lifecycle hooks synchronously in setup; do not rely on instance context in arbitrary async callbacks.
  Compiler-managed top-level await in `<script setup>` has distinct context restoration semantics.
- must release in `onBeforeUnmount` anything that reads the DOM, and leave `onUnmounted` for teardown that does not.
- must declare each `provide` / `inject` pair against an exported `InjectionKey<T>`, and give `inject` a default or a
  thrown error — an un-provided key returns `undefined` and fails at the first read, far from the missing provider.
- must reach for `defineComponent` only where the job is vnode manipulation a template cannot express — `Slot`,
  `Primitive`, `Presence`, `AnimatedLayout`, the form-engine field wrappers, and a `VNodeChild` prop rendered inline.
- must reach for `useAttrs` for an attribute Vue would camelize; `props.ariaLabel` is not what the consumer wrote
  ([vue SFC](vue-sfc.md) § *Attributes*).
- must not reach for `getCurrentInstance` to read state a prop or an `inject` can carry.

```typescript
// ✅ typed key, provider and consumer agree, and a missing provider throws where it is missed
export const FieldKey: InjectionKey<FieldContext> = Symbol('Field');
const field = inject(FieldKey);
if (!field) throw new Error('Field parts must render inside <Field>.');

// ❌ a string key type-checks against nothing, and a rename misses the consumer
provide('field', context);
```

---

## Banned

- **`onBeforeMount` · `onBeforeUpdate`** — reach for `setup()`'s body and a `watch`; both run before the DOM
  reaches the state they describe, so their work is re-checked after the patch anyway.
- **`onActivated` · `onDeactivated`** — no replacement is needed; they fire only under `<KeepAlive>`, banned in
  [built-ins](builtins.md), so a component carrying them silently never runs that code.
- **`onRenderTracked` · `onRenderTriggered`** — reach for the Vue devtools; a production build strips them,
  so a fix that depends on one works in dev and disappears on release.

---

## Execution

- must use `onServerPrefetch` only in an explicitly supported SSR delivery target;
  [library compatibility](../../../../shapes/library/platform/compatibility.md) owns that support claim.

---

## Neighbours

- [vue](vue.md) — the full construct roster
- [reactivity](reactivity.md) — `onScopeDispose`, the teardown these hooks share
- [built-ins](builtins.md) — the components whose hooks are banned here
