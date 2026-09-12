# Frontend LLA resolution

*Last updated: 2026-09-10*

> Resolution of the 65 LLA documents and four scope/index documents assigned in [LLA analysis](lla-analysis.md).
> Convention edits only; SDK implementation and release evidence remain separate.

## Status

- [x] Corrected L1–L10 factual and scope findings within the assigned owners.
- [x] Added controlled-state, ref lifetime, lifecycle and interaction invariants.
- [x] Removed package usage counts and implementation migration notes from platform rosters.
- [x] Reconciled document registers and linked new shape-owned contracts.
- [x] Verified representative TypeScript, Vue compiler, generated CSS and browser examples.
- [x] Checked local links, explicit fragments and Markdown table column counts in all 69 assigned files.
- No unresolved LLA design decision remains. Remaining SDK implementation work is not a convention choice.

---

## Finding resolution

| Finding | Resolution | Main task |
|---|---|---|
| L1 | Outline fallback accompanies shadow-based rings; forced colors verified | C05 |
| L2 | Important/arbitrary/custom utility behavior corrected; native button cursor house policy retained | C09 |
| L3 | Client actions, legacy context, transitions, refs and dialog capabilities corrected | C08 |
| L4 | Exposed roots require consumer inventory and documented replacement/lifetime; `$el` is not equivalent | C08 |
| L5 | Compile-time readonly and runtime freezing distinguished; arrays and namespace rules qualified | C10 |
| L6 | Shape subject-existence test used; app names, placement, aliases and CSS wiring link to shape owners | C01 |
| L7 | Responsive/semantic grids, static transforms, flex/grid stacking and motion/focus defaults reconciled | C09 |
| L8 | Generated IDs, caller IDs, page anchors and explicit landmark naming separated | C05 |
| L9 | Shared ownership contract plus independent React/Vue spellings; uncontrolled example typechecks | C03 |
| L10 | Imports cover Vue, prose pointer repaired, document template matches definition/application registers | C15 |

Scope/index edits also link domain/shape work for C11–C14; those agents own their detailed rules.

---

## Owners

- Controlled semantics: [props](../../../conventions/development/frontend/core/lla/notation/naming/props.md#controlled-state).
- Framework spelling: [React](../../../conventions/development/frontend/core/lla/constructs/react/components.md#controlled-props)
  and [Vue](../../../conventions/development/frontend/core/lla/constructs/vue/macros.md#controlled-props).
- Root API safety: [Vue macros](../../../conventions/development/frontend/core/lla/constructs/vue/macros.md).
- React lifecycle: [hooks](../../../conventions/development/frontend/core/lla/constructs/react/hooks.md#lifecycle).
- Vue lifecycle: [reactivity](../../../conventions/development/frontend/core/lla/constructs/vue/reactivity.md).
- Interaction: [HTML](../../../conventions/development/frontend/core/lla/constructs/html/interactive.md#interaction).
- Visual/assistive checks: [accessibility](../../../conventions/development/frontend/core/lla/constructs/tailwind/accessibility.md#verification).
- Register shapes: [MLA](../../../conventions/development/frontend/core/mla/mla.md#writing-a-doc-in-this-scope-required).
- App names, enum/extension locations, stylesheet placement and published alias handling are linked to their shape owners.
- The SDK's supported runtime matrix determines SSR/RSC support; a SPA application does not impose that restriction on a package.

---

## Representative verification

Fixtures use the Vue package's installed dependencies through `createRequire(packageJsonPath)` and temporary files only.
Versions at verification: TypeScript `5.9.3`, Tailwind `4.3.3`, Playwright `1.62.1`.

### TypeScript and Vue

- Strict `noEmit` + `isolatedModules` fixture: zero diagnostics.
- The corrected controlled and seed-only `InfoBannerProps` examples compile independently.
- `@ts-expect-error` assertions confirm that both `ReadonlyArray<T>` and `readonly T[]` reject `.push()`.
- An owned `Array<T>` permits `.push()`; a runtime namespace inside an ES module compiles under `isolatedModules`.
- A const assertion rejects direct typed mutation; transpiled runtime output remains mutable: `{ frozen: false, value: 2 }`.
- Vue SFC compilation emits `open: { type: Boolean, required: false, default: undefined }` for the controlled model example.
- These are type/compiler checks, not a full controlled-input or SDK regression suite.

### Class merging and CSS

| Input | Installed merger output |
|---|---|
| `p-[1rem] p-4` | `p-4` |
| `gap-[0.5rem] gap-2` | `gap-2` |
| `p-2! p-4!` | `p-4!` |
| `!p-2 !p-4` | `!p-4` |
| `p-2! p-4` | `p-2! p-4` |

- Tailwind generated `outline-hidden` with `outline: 2px solid transparent` under `forced-colors: active`.
- Generation and merger output were checked separately; these fixtures do not claim that every custom utility is merge-configured.

### Chromium

The fixture compiled utilities with the installed Tailwind theme and used `chromium.launch({ headless: true })`.
It rendered a dark button, a named section, an unnamed section containing a heading, responsive cards, a calendar and static positioning.

| Check | Result |
|---|---|
| Forced colors + keyboard focus | `focus-visible=true`, `outline=solid`, `width=2px`, `box-shadow=none` |
| Cards at 320px | One column |
| Cards at 800px | Three columns |
| Calendar at 320px | Seven columns retained |
| Static grid child stacking | `position=static`, `z-index=10` |
| Static centered child | `translate=-50% -50%` without animation |
| Named-region lookup | One region; the heading-only unnamed section is not a region |

This confirms the disputed platform mechanisms in Chromium. Manual screen-reader announcement behavior, the full browser matrix,
every component's focus restoration and SDK interaction coverage are not established by this fixture.

### Documents

- Relative Markdown links and explicit heading fragments: zero failures across 69 assigned files.
- Markdown table column checks: zero malformed tables across the same files.
- Removed the obsolete `React types` prose pointer to `style.md`; the owner is `react/jsx.md`.
- Removed usage-count columns from platform inventories; reviewed remaining numeric rules as contracts rather than snapshot counts.
- Inherited application/doc-field directives now link to their owners instead of requiring repeated example pairs.

---

## Primary evidence

- [React client actions](https://react.dev/reference/react/useActionState).
- [React Context](https://react.dev/reference/react/createContext) and [React 19](https://react.dev/blog/2024/12/05/react-19).
- [Vue instance `$el`](https://vuejs.org/api/component-instance#el).
- [Vue transition classes](https://vuejs.org/guide/built-ins/transition.html#custom-transition-classes).
- [Vue function refs](https://vuejs.org/guide/essentials/template-refs.html#function-refs).
- [Tailwind upgrade guide](https://tailwindcss.com/docs/upgrade-guide).
- [Tailwind merge features](https://github.com/dcastil/tailwind-merge/blob/main/docs/features.md).
- [Tailwind merge configuration](https://github.com/dcastil/tailwind-merge/blob/main/docs/configuration.md).
- [TypeScript const assertions](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-4.html#const-assertions).
- [TypeScript isolated modules](https://www.typescriptlang.org/tsconfig/isolatedModules.html).
- Additional original evidence remains in [LLA analysis](lla-analysis.md); this record does not duplicate the full audit.

## Package README clarification during the SDK pass

The SDK structure owner already requires an npm-packable README beside package.json. The general repository
README rule and root CLAUDE summary now explicitly preserve that functional metadata, alongside NuGet's
declared PackageReadmeFile. Folder lead documents still use the folder name. This reconciles the existing
specific SDK rule with its general summary; it does not add a second package documentation policy.
