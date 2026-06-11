# Conventions — Development — Frontend (React / TypeScript)

*Last updated: 2026-06-09*

> React 19 / TypeScript (strict) / Vite / Tailwind v4 / `@wow-two-beta/ui` code-style conventions for
> every frontend under `wow-two-ws/`. Lookup table — open a file when the task touches it; do not
> pre-read. Repo layout is one level up: [../repo/repo-structure.md](../repo/repo-structure.md). The .NET
> sibling: [../backend/](../backend/).

## Language

| File | What it covers |
|---|---|
| [naming.md](naming.md) | Files PascalCase (barrels lowercase), folders camelCase, `*Extensions`/`*Styles`/`*Helpers` suffixes, exports |
| [documentation.md](documentation.md) | JSDoc one-liner rule + verb-starter table (Defines / Renders / Manages / Provides) |
| [code-organization.md](code-organization.md) | `const`/`let`, `// ── Section ──` dividers, 7-group import order, file-internal order |
| [models.md](models.md) | Domain model vs DTO vs form-fields, `interface`/`type`, collections (`Array` vs `ReadonlyArray`) |

## Type-kinds

| File | What it covers |
|---|---|
| [enums.md](enums.md) | TS `enum` + label `Record`, camelCase wire values, `Unresolved` first, dropdown options |
| [components.md](components.md) | One-component-per-folder, props (`readonly`, no destructure), file structure, UI terminology, variants |
| [hooks.md](hooks.md) | `use*` naming, object vs tuple return, `Manages`/`Provides access to`, abort on unmount |
| [extensions.md](extensions.md) | `{Noun}Extensions` `as const` objects (no class/namespace) — the C# static-helper analog |
| [forms.md](forms.md) | String form state (`EditableFields`), resolve-on-submit, enum-as-string |

## Architecture

| File | What it covers |
|---|---|
| [project-structure.md](project-structure.md) | Single Vite app vs pnpm workspace + `packages/` (`@{brand}/ui`·`common`·`domain`), boundaries, ports |
| [state-and-data.md](state-and-data.md) | Same-origin `/api` client, dev proxy, `ApiError`/ProblemDetails, Context+hooks, localStorage keys |
| [styling.md](styling.md) | Tailwind v4 `@import`/`@theme`/`@source`-ing `@wow-two-beta/ui`, tokens, `cn()`, `tailwind-variants`, dark mode |

## Notes

- Initial extraction (2026-06-09) generalized from Haven's `frontend-development-guidelines.md` +
  `frontend-architecture.md`, the `@wow-two-beta/ui` `CLAUDE.md`, and current drydock practice.
- Haven-specifics stripped: `@haven/*` → `@{brand}/*`; Supabase/n8n/i18n details dropped as product-level.
- These apply to **every** frontend repo under `wow-two-ws/`; a repo-level rule overrides for that repo.
- Backend sibling: [../backend/](../backend/).

## Gap analysis — conventions still missing

Not yet covered (no source content exists, or needs a deliberate decision). Prioritized; write each as a
focused file when the supporting practice lands in a repo.

### P1 — needed before more apps ship

| Gap | Why it matters | Note |
|---|---|---|
| **Testing** | Beta UI is explicitly "no tests"; products need a real stance (Vitest + RTL? Playwright? what's required vs optional) | No FE test convention exists in any source today |
| **Error & loading states** | `ApiError` exists ([state-and-data.md](state-and-data.md)) but no shared pattern for error boundaries, loading skeletons, empty states (`EmptyState`/`Alert`/`Spinner` exist in beta UI but usage isn't codified) | Partially implied; needs its own file |
| **Routing** | Today: URL-hash routing for light apps. No decision for multi-route apps (React Router? TanStack Router? file-based?) | `useHashRouter` is Haven-only; not generalized |

### P2 — soon

| Gap | Why it matters |
|---|---|
| **Accessibility (a11y)** | No keyboard/ARIA/focus-management baseline; beta UI uses Radix/floating-ui primitives but consumer rules aren't stated |
| **i18n** | Haven landing uses EN/RU/UZ ad-hoc; no shared translation/locale convention (ties into the enum label-Record → backend-translation migration) |
| **Server-state / data-fetching library** | Current rule is hand-rolled hooks + `fetch`. If TanStack Query (or similar) is adopted, caching/invalidation/retry conventions need codifying |
| **Environment & config** | `.env`/`import.meta.env` handling, build-time vs runtime config, secrets boundary |

### P3 — later

| Gap | Why it matters |
|---|---|
| **Code-splitting / performance** | Lazy `React.lazy`/`Suspense` boundaries, bundle budgets, `default` export carve-out exists but no perf guidance |
| **Linting / formatting** | ESLint flat-config + Prettier baseline (beta UI uses `eslint-plugin-boundaries`; products have no stated config) |
| **Icons & assets** | `lucide-react` is the de-facto icon set but it's not written as a rule; static asset handling unspecified |
| **Storybook** | Required in the beta UI library; unspecified (likely not required) for product apps |
| **Analytics / logging** | Client error reporting + telemetry boundary (intersects the GWDNBM no-engagement-bait principle) |
