# Built-ins

*Last updated: 2026-09-10*

> The components Vue registers globally — `Teleport`, the transition pair, `KeepAlive`, `Suspense`, `<component>`.
> Purpose — each one takes over a job the codebase already solves with a primitive, so the verdict is which owns it.
> Use case — reach here before rendering a component the template never imported.

## The constructs

| Construct | Is | Verdict |
| --- | --- | --- |
| `<Teleport to>` | children rendered under a different DOM parent | `use with care` |
| `<Transition>` | class hooks around one child's enter and leave | `banned` |
| `<TransitionGroup>` | the same, plus a FLIP move over a keyed list | `banned` |
| `<KeepAlive>` | an instance cached instead of unmounted | `banned` |
| `<Suspense>` | a boundary that waits on a child's async `setup()` | `banned` |
| `<component :is>` | the element or component chosen at runtime | `use` |
| `defineAsyncComponent` | a component resolved through a dynamic `import()` | `use with care` |
| `Presence` | the SDK primitive that holds a node until its transition ends | `use` |
| `AnimatedLayout` | the SDK primitive that FLIPs surviving keyed children | `use` |

- must reach `<Teleport>` through `Portal.vue`, which adds the mount gate the raw element has no place for.
- must reach for `Presence` for enter / leave, and `AnimatedLayout` for a reorder — both read the computed duration
  off the node, so the timing follows the Tailwind motion tokens rather than a second class vocabulary.
- must give `<component :is>` a value from a `const` object, never a raw string
  ([enums](../../components/enums.md)).
- must keep `defineAsyncComponent` out of a published package; a consumer's app is where a route split belongs.
- must not reach for a built-in to hide a component that should not be rendered — that is `v-if`
  ([template](template.md)).

```vue
<!-- ✅ Presence holds the node until the transition it measures has finished -->
<Presence :is-present="open"><div class="transition-opacity">…</div></Presence>

<!-- ❌ bypasses the house Presence abstraction -->
<Transition enter-active-class="fade-enter"><div v-if="open">…</div></Transition>
```

---

## Banned

- **`<Transition>` · `<TransitionGroup>`** — use `Presence` / `AnimatedLayout` under the house motion policy;
  Vue's custom transition-class props can take utility classes without `@apply`.
- **`<KeepAlive>`** — reach for the query layer's cache ([state & data](../../../mla/domains/data/state-and-data.md));
  a cached instance keeps its watchers, timers and subscriptions running off-screen, and makes `onActivated` /
  `onDeactivated` mandatory on every child that touches the DOM.
- **`<Suspense>`** — use the query layer's loading state under the house policy;
  handle async setup errors explicitly through Vue error capture rather than assuming Suspense catches them.

---

## Neighbours

- [vue](vue.md) — the full construct roster
- [template](template.md) — the directives these components are written beside
- [visual kinds](../../../mla/constructs/visual/visual.md) — the SDK components to reach for first
