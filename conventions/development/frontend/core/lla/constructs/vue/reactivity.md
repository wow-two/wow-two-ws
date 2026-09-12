# Reactivity

*Last updated: 2026-09-10*

> Every reactive primitive Vue offers — boxes, derivations, watchers and their flush timings, and the scope.
> Purpose — a wrong primitive costs an identity compare, a missed update, or a watcher that outlives its component.
> Use case — reach here before storing state, deriving a value, or reacting to one changing.

## The constructs

| Construct | Is | Verdict |
| --- | --- | --- |
| `ref` | a deeply tracked box, unwrapped in a template | `use` |
| `shallowRef` | a box tracked on replacement only | `use` |
| `computed` | a cached derivation, re-run when a tracked source changes | `use` |
| `reactive` | a deep proxy standing in for the object itself | `use with care` |
| `shallowReactive` | the same proxy, one level deep | `banned` |
| `readonly` | a proxy rejecting writes, with development warnings | `use with care` |
| `markRaw` | a flag that keeps an object out of the proxy | `banned` |
| `toRaw` · `customRef` · `triggerRef` | the escape hatches out of the tracking system | `use with care` |
| `watch` | an effect over sources named at the call | `use` |
| `watchEffect` | an effect whose sources come from running it once | `use with care` |
| `watchPostEffect` · `flush: 'post'` | the same effect, run after the DOM patch | `use` |
| `flush: 'sync'` | an effect run inside the write itself | `use with care` |
| `watchSyncEffect` | the implicit-source form of `flush: 'sync'` | `banned` |
| `{ immediate: true }` | a first run at setup, before any change | `use` |
| `{ deep: true }` | traversal of every nested key on each check | `use with care` |
| `nextTick` | a promise resolving after the next patch | `use with care` |
| `toValue` | reads a value, a ref or a getter as a value | `use` |
| `MaybeRefOrGetter<T>` | the type of anything a composable will accept | `use` |
| `toRef` · `toRefs` | refs pointing into an existing reactive object | `banned` |
| `onScopeDispose` | teardown that runs when the owning scope stops | `use` |
| `effectScope` | a disposal scope with no component behind it | `use with care` |

- must reach for `shallowRef` when the box holds a DOM node, a class instance, or a value replaced, not edited.
- must reach for `computed` before `watch` — a `watch` whose body only assigns another ref is a `computed` twice.
- must name the sources on a `watch`; leave `watchEffect` for a body whose reads cannot be enumerated.
- must use `watchPostEffect` (or `flush: 'post'`) for anything that measures or focuses the DOM.
- must take a composable's argument as `MaybeRefOrGetter<T>` and read it through `toValue`, so a caller may pass either.
- must register `onScopeDispose` for every listener, timer or observer a composable starts.
- must register cleanup before an async boundary and release work when its scope ends.
- must invalidate an async watcher run when its source changes; ignore late results from obsolete runs.
- must guard DOM work until mount; an immediate watcher may run during server rendering.
- must stop asynchronously created watchers explicitly when they are not owned by the component scope.
- must not `deep: true` over a list to detect an item change; key the `watch` on the derived value.

```typescript
// ✅ the source is named, the read is deferred, teardown is registered
const query = computed(() => toValue(term).trim());
watch(query, (next) => run(next), { immediate: true });
onScopeDispose(() => controller.abort());

// ❌ reactive() hands back a proxy, so the caller's own object no longer === the stored one
const state = reactive({ user });
state.user === user; // false
```

---

## Banned

- **`shallowReactive`** — reach for `shallowRef`; it still returns a proxy, so `===` against the source object fails
  while buying nothing `shallowRef` does not already give.
- **`markRaw`** — reach for `shallowRef`; marking one leaf only matters once a deep proxy exists, and the sibling keys
  around the marked one stay proxied, so the identity bug moves rather than goes away.
- **`watchSyncEffect`** — use explicit `watch` sources under the house policy;
  effect dependencies are collected again on each run, not frozen to the first branch.
- **`toRef` · `toRefs`** — reach for `computed(() => …)`; `toRefs` snapshots the key set, so a key added later
  never becomes a ref, and `toRef(props, 'x')` re-wraps an already reactive prop.

---

## Identity

- must choose proxy identity deliberately; compare stable IDs or the same reactive view across a boundary.
- must not tighten a construct verdict solely because its remaining implementation count reached zero.

---

## Neighbours

- [vue](vue.md) — the full construct roster
- [macros](macros.md) — where props and emits enter the graph
- [hooks](../../../mla/constructs/behavior/hooks.md) — the composable shape these primitives are wrapped into
