# Vue SFC

*Last updated: 2026-08-20*

> Block layout, in-file order, shared DOM vocabulary, and JSDoc verbs for a Vue Single-File Component.
> Use case — writing or reviewing any `.vue` file, above all in `@wow-two-beta/ui-vue`.

## Blocks

- must put exported types and module-scope constants in a plain `<script lang="ts">`.
- must put instance logic in `<script setup lang="ts">`.
- must order blocks `<script>` → `<script setup>` → `<template>`; a `<style>` block is banned
  ([css](../css/css.md) § *Banned*).
- must not repeat an import across the two blocks — Vue merges them into one module scope.
- must not add a plain `<script>` block that exports nothing.

---

## Order inside `<script setup>`

- must order **macros → constants → composables → reactive state → computed → watchers → functions**.
- must keep `defineOptions` · `defineProps` · `defineEmits` · `defineSlots` together at the top.
- must not declare a constant, state, or a `computed` between two functions.
- must declare a `computed` before any `watch` that reads it.

---

## Imports

- must import across a **published library's** `src/` with relative paths — an alias in the emitted `.d.ts`
  will not resolve; app code takes the `@/` alias ([imports](../../notation/style/imports.md)).
- must use the `@src/*` alias in `tests/` only.
- must ignore the IDE's "import can be shortened" hint inside a library's `src/`.
- group order and intra-group sort → [imports](../../notation/style/imports.md).

---

## Docs

- must anchor the component doc immediately above `defineOptions`
  ([constructs](../../../mla/constructs/constructs.md) § *Docs*).
- must doc a `computed` as the value it yields (`The …`), never `Computes …`.
- must doc a `watch` by the effect it causes (`Emits …` · `Syncs …` · `Resets …`), never `Watches …`.
- must doc a function with a third-person verb — `Copies …` · `Resolves …`.
- must mark a non-exported type, constant, or helper `@internal`.
- must keep a doc a **one-liner**; a non-JSDoc `/* */` comment is one line stating a role, with no exception.
- the multi-line exception, § *Scope*, and the verb table →
  [documentation](../../notation/documentation/documentation.md).

---

## Width

- must wrap every line at **120 columns**, comments included — Prettier never reflows a comment, `max-len` catches it.
- must run `pnpm format` before `pnpm lint`.

---

## Shared vocabulary

| Need | Take | Example |
|---|---|---|
| ARIA / DOM attribute name | `AriaAttribute` | `AriaAttribute.Label` |
| Boolean attribute value | `AttributeValue` | `AttributeValue.True` |
| Event name | `DomEvent` | `emit(DomEvent.Error, cause)` |
| The `onX` prop for an event | `HandlerProp<E>` | `HandlerProp<typeof DomEvent.Error>` |
| Element tag | `ElementTag` | `ElementTag.Div` |

- must take every DOM literal from `foundation/utils`, adding a missing one there rather than declaring it locally.
- constant casing → [naming](../../notation/naming/naming.md) § *Quick reference*.
- must not extract a DOM attribute **name** used once in a template — markup is not code.

---

## Types over literals

- must name another type's key as `keyof Pick<T, 'k'>`, never a bare `'k'` union.
- must declare a literal used in **both** a type and at runtime as one `as const` tuple, and derive the type from it.
- must not hoist a key already inside a `keyof Pick<…>` into a runtime tuple — the alias is the extraction.

```ts
const OwnedAttributes = [AriaAttribute.Label] as const;
type OwnedAttribute = (typeof OwnedAttributes)[number];
type ReplacedButtonProp = keyof Pick<ButtonProps, HandlerProp<typeof DomEvent.Error>>;
```

---

## Attributes

- must read an attribute Vue would camelize off `useAttrs()`, not `props`.
- must set `inheritAttrs: false` when the component re-renders an attribute under its own value.
- must filter the owned keys out of the forwarded set before `v-bind`.
- must mark a types-only heritage `/* @vue-ignore */`.
- must extend **one** named type, never a comma-separated heritage list — Prettier lifts the marker above a
  multi-entry `extends`, where the SFC compiler stops seeing it.
- must re-declare a heritage prop in the body when it needs a `withDefaults` default.
- must reach for `dataAttr()` for a boolean `data-*`; a value a standard pins comes from `AttributeValue`.

---

## Gates

Run all four; `check:sfc` is the one with no substitute.

| Gate | Catches |
|---|---|
| `pnpm format` | code width, quote style, trailing commas |
| `pnpm lint` | comment width, boundaries, unused code |
| `pnpm typecheck` | types **and** `check:sfc` — a heritage the SFC compiler cannot resolve |
| `pnpm test` | behaviour, SSR safety, mount smoke |

- no gate reads what a comment *says*; only review catches a rule-restating doc.

---

## Reference

`CopyButton.vue` in the Vue beta SDK — every rule above holds in it, at zero warnings across all four gates.
Path: `wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/actions/copyButton/`.
