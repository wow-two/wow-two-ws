# Reactivity

*Last updated: 2026-08-19*

> Every reactive primitive Vue offers — boxes, derivations, watchers and their flush timings, and the scope.
> Purpose — a wrong primitive costs an identity compare, a missed update, or a watcher that outlives its component.
> Use case — reach here before storing state, deriving a value, or reacting to one changing.

## The constructs

| Construct | Is | Uses | Verdict |
|---|---|---|---|
| `ref` | a deeply tracked box, unwrapped in a template | 109 | `use` |
| `shallowRef` | a box tracked on replacement only | 120 | `use` |
| `computed` | a cached derivation, re-run when a tracked source changes | 1811 | `use` |
| `reactive` | a deep proxy standing in for the object itself | 1 | `use with care` |
| `shallowReactive` | the same proxy, one level deep | 0 | `banned` |
| `readonly` | a proxy that silently drops every write | 1 | `use with care` |
| `markRaw` | a flag that keeps an object out of the proxy | 0 | `banned` |
| `toRaw` · `customRef` · `triggerRef` | the escape hatches out of the tracking system | 0 | `use with care` |
| `watch` | an effect over sources named at the call | 107 | `use` |
| `watchEffect` | an effect whose sources come from running it once | 3 | `use with care` |
| `watchPostEffect` · `flush: 'post'` | the same effect, run after the DOM patch | 19 · 45 | `use` |
| `flush: 'sync'` | an effect run inside the write itself | 3 | `use with care` |
| `watchSyncEffect` | the implicit-source form of `flush: 'sync'` | 0 | `banned` |
| `{ immediate: true }` | a first run at setup, before any change | 63 | `use` |
| `{ deep: true }` | traversal of every nested key on each check | 2 | `use with care` |
| `nextTick` | a promise resolving after the next patch | 10 | `use with care` |
| `toValue` | reads a value, a ref or a getter as a value | 194 | `use` |
| `MaybeRefOrGetter<T>` | the type of anything a composable will accept | 198 | `use` |
| `toRef` · `toRefs` | refs pointing into an existing reactive object | 0 | `banned` |
| `onScopeDispose` | teardown that runs when the owning scope stops | 46 | `use` |
| `effectScope` | a disposal scope with no component behind it | 0 | `use with care` |

- must reach for `shallowRef` when the box holds a DOM node, a class instance, or a value replaced, not edited.
- must reach for `computed` before `watch` — a `watch` whose body only assigns another ref is a `computed` twice.
- must name the sources on a `watch`; leave `watchEffect` for a body whose reads cannot be enumerated.
- must use `watchPostEffect` (or `flush: 'post'`) for anything that measures or focuses the DOM.
- must take a composable's argument as `MaybeRefOrGetter<T>` and read it through `toValue`, so a caller may pass either.
- must register `onScopeDispose` for every listener, timer or observer a composable starts.
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
- **`watchSyncEffect`** — reach for `watch(source, fn, { flush: 'sync' })`; it pairs implicit sources with a sync
  flush, so a branch not taken on the first run never re-triggers inside the write.
- **`toRef` · `toRefs`** — reach for `computed(() => …)`; `toRefs` snapshots the key set, so a key added later
  never becomes a ref, and `toRef(props, 'x')` re-wraps an already reactive prop.

---

## Open

- `reactive` survives at `RovingFocusContext.ts:195` and `readonly` at `GoogleIdentity.ts:247`; both are the last
  sites, and six in-code comments already argue against the pattern. Convert them, then tighten both to `banned`.

---

## Neighbours

- [vue](vue.md) — the full construct roster
- [macros](macros.md) — where props and emits enter the graph
- [hooks](../../../mla/constructs/behavior/hooks.md) — the composable shape these primitives are wrapped into
