# Composition

*Last updated: 2026-08-19*

> The instance-bound constructs — lifecycle hooks, `provide` / `inject`, and the render-function escape.
> Purpose — each one binds to the current instance, so calling it in the wrong place fails at runtime, not at compile.
> Use case — a component needs the DOM, a subtree needs a value, or a template cannot express a render.

## The constructs

| Construct | Is | Uses | Verdict |
|---|---|---|---|
| `onMounted` | the first point the rendered DOM exists | 56 | `use` |
| `onBeforeUnmount` | teardown while the DOM is still attached | 18 | `use` |
| `onUnmounted` | teardown after the node is gone | 6 | `use with care` |
| `onUpdated` | a callback after every patch of this component | 3 | `use with care` |
| `onErrorCaptured` | a hook for a throw from a descendant | 1 | `use with care` |
| `onBeforeMount` · `onBeforeUpdate` | the pre-render pair | 0 | `banned` |
| `onActivated` · `onDeactivated` | the hooks only `<KeepAlive>` fires | 0 | `banned` |
| `onRenderTracked` · `onRenderTriggered` | the dev-only dependency probes | 0 | `banned` |
| `onServerPrefetch` | the SSR-only await point | 0 | `banned` |
| `provide` · `inject` | a value handed down a subtree by key | 57 · 56 | `use` |
| `InjectionKey<T>` | the typed token a provide / inject pair agrees on | 55 | `use` |
| `useAttrs` | the attributes neither a prop nor a declared emit claimed | 335 | `use` |
| `useSlots` | the runtime slot set | 55 | `use` |
| `useId` | an id stable across server and client | 49 | `use` |
| `defineComponent` | a component authored as an object rather than an SFC | 17 | `use with care` |
| `h()` · render function | a vnode built in TypeScript | 8 | `use with care` |
| `cloneVNode` · `mergeProps` | a vnode re-emitted with added props | 6 · 5 | `use with care` |
| `getCurrentInstance` | the internal handle on the running instance | 9 | `use with care` |

- must call every hook synchronously in `setup()` — after an `await` there is no current instance to bind to.
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
- **`onServerPrefetch`** — no replacement is needed; every app here ships as a Vite SPA
  ([single-host serving](../../../../../../deployment/hosting/single-host-serving.md)), so the hook never fires.

---

## Neighbours

- [vue](vue.md) — the full construct roster
- [reactivity](reactivity.md) — `onScopeDispose`, the teardown these hooks share
- [built-ins](builtins.md) — the components whose hooks are banned here
