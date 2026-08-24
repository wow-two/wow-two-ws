# Constructs

*Last updated: 2026-08-19*

> Every baseline the platform hands us — TypeScript declarations, HTML elements, CSS features, Tailwind utilities.
> Purpose — settle *what we build on* once, so no component doc re-argues `<button>` against `<div role="button">`.
> Use case — reach here before writing a declaration, an element, a property or a class new to this codebase.

## The platforms

A construct is anything the language or the framework offers as a baseline to define something on top of.

| Platform | Offers | Index |
|---|---|---|
| TypeScript | declarations | [typescript](typescript/typescript.md) |
| Vue 3 | macros, reactivity, directives, slots, built-in components | [vue](vue/vue.md) |
| React 19 | hooks, component forms, boundaries, JSX | [react](react/react.md) |
| HTML | elements and global attributes | [html](html/html.md) |
| CSS | custom properties, at-rules, selectors, values | [css](css/css.md) |
| Tailwind v4 | utilities, variants, authoring at-rules | [tailwind](tailwind/tailwind.md) |

---

## The verdict

- must read `use` as the default form for its job, and `use with care` as allowed but argued in review.
- must treat `banned` as never written; every group doc names the replacement in its own `## Banned` section.
- must state a ban in the group doc that owns the construct — a rejected construct gets no separate file.
- must carry both halves in one doc: what the construct is, **and** whether we use it.
- must link out to the fuller convention where one exists ([one owner per rule](../../../../../conventions.md)).
- must give a construct we have never written a verdict anyway; an absent row reads as unconsidered.

---

## Neighbours

- [mla constructs](../../mla/constructs/constructs.md) — the app roles these language constructs are shaped into
- [components](../components/components.md) — these same forms used end to end: constants, enums, extensions
- [notation](../notation/notation.md) — how a construct is named and documented
- [styling](../../../shapes/app/platform/styling.md) — how an app wires Tailwind and consumes the tokens
