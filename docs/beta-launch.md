# wow-two beta launch

*Last updated: 2026-04-28*

> **Single source of truth** for the beta-launch effort. Combines strategy, conventions, and the parallel-chat task tracker.
> Goal in 10x-ws: `car-wow-two-beta-launch` (Q2 2026).

---

## Strategy

**Beta-forever, ship-as-much-as-possible.** No graduation rule. No CHANGELOG, no PR review, no required tests, no semver guarantees. Push to main. Fix-forward when broken. Distill into clean `@wow-two/*` and `Wow.Two.*` packages only after the platform layer below stabilizes — that's a future-quarter problem.

**Why now:** haven needs UI + backend packages to expand to multiple channels. Standards aren't established yet — they emerge from real package iteration. Building the platform foundation requires running real packages first.

## Naming convention

The principle: **status goes before function.** Beta is a scope/org prefix, never a package-name suffix.

| Layer | Stable | Beta |
|---|---|---|
| npm scope | `@wow-two` | `@wow-two-beta` |
| npm package | `@wow-two/ui` | `@wow-two-beta/ui` |
| GitHub org | `wow-two-sdk` | `wow-two-sdk-beta` |
| GitHub repo | `wow-two-sdk.ui` | `wow-two-sdk-beta.ui` |
| Local path | `workbench/wow-two-sdk/` | `workbench/wow-two-sdk-beta/` |
| NuGet package | `Wow.Two.Sdk.{Name}` | `Wow.Two.Sdk.Beta.{Name}` |

Graduation later = republish to stable scope, no name change in the package itself.

Other beta orgs (`wow-two-platform-beta`, `wow-two-kb-beta`, etc.) are reserved lazily — only created when a package actually needs to live there.

## Repos

| Repo | Package surface | GitHub org |
|---|---|---|
| `wow-two-sdk-beta.ui` | `@wow-two-beta/ui` (npm), subpath exports per src/ folder | `wow-two-sdk-beta` |
| `wow-two-sdk-beta.backend` | `Wow.Two.Sdk.Beta.*` (NuGet), one package per project in repo | `wow-two-sdk-beta` |

Both are single repos containing many granular packages. **Not** a multi-repo split — too early for that.

## Conventions

- **Versioning**: `0.x.y` forever. CI auto-bumps `y` on every push to `main`.
- **Casing**: PascalCase files, camelCase folders, lowercase `index.ts` (matches haven).
- **Per-component shape**: `{group}/{componentName}/{ComponentName}.{tsx,spec.md,stories.tsx,variants.ts}` + `index.ts`. Spec written first.
- **Layering**: foundation (`tokens`, `tailwind`, `utils`, `hooks`, `icons`) cannot import upward; domains (`actions`, `display`, `feedback`, `forms`, `layout`) cannot import sibling domains. ESLint enforced.
- **No tests** in beta. CI runs build + lint + typecheck only.
- **GitHub repos are public** (forced by free GitHub Pages — private Pages requires Pro/Enterprise). Issues/Discussions disabled in repo settings to keep contributor surface minimal.

## Out of scope (deliberate)

- Tests
- CHANGELOG
- PR gates / branch protection
- Required reviewers
- Standards enforcement (no shared lint config across repos until a few cycles surface what's actually shared)
- Distill / graduation pipeline

---

## Tracks

Four parallel tracks. Each can own its own chat. Tasks within a track are sequential; tracks themselves are mostly independent.

### Track A — Namespace reservation (`car-t-003`)

**Owner chat:** `wow-two - track-a-reservation`
**Deadline:** 2026-05-05
**Outcome:** Three names locked: NuGet `Wow.Two.Sdk.Beta.*` prefix, npm `@wow-two` scope, npm `@wow-two-beta` scope.

| # | Task | Notes |
|---|---|---|
| A1 | Create `@wow-two` org on npm; register | Owns `@wow-two/*` packages |
| A2 | Create `@wow-two-beta` org on npm; register | Reserves the second scope (defensive — may not be used) |
| A3 | Publish stub `@wow-two-beta/ui@0.0.0` from current repo | Locks the package name |
| A4 | Publish stub `Wow.Two.Sdk.Beta.Placeholder` to NuGet | First publish required before applying for prefix reservation |
| A5 | Apply for NuGet prefix reservation `Wow.Two.Sdk.Beta.*` (and `Wow.Two.*` while at it) | Microsoft review takes days–weeks |
| A6 | Verify reservation: subsequent publishes show "reserved prefix" badge | |

### Track B — `@wow-two-beta/ui` operational (`car-t-004`)

**Owner chat:** `wow-two - track-b-ui-beta` (this chat continues here unless redirected)
**Deadline:** 2026-05-31
**Outcome:** Working repo, CI publishing on push, Storybook live, broad base-layer coverage.

| # | Task | Status |
|---|---|---|
| B1 | Scaffold repo (root configs, src/ skeleton, Button sample, Storybook, playground) | ✅ |
| B2 | Local sanity: `pnpm install` / `pnpm typecheck` / `pnpm build` / `pnpm storybook` | ✅ |
| B3 | GitHub Actions CI: build + typecheck + lint on push to main | ✅ |
| B4 | CI: auto-bump `0.0.y` + `npm publish` on push to main | ✅ |
| B5 | CI: build Storybook + deploy to GitHub Pages | ✅ |
| B6+ | Build out the package per phased roadmap | → see `ui-beta-roadmap.md` |

**Phased build-out** (P1–P7) is tracked in [`ui-beta-roadmap.md`](./ui-beta-roadmap.md). Day-to-day work happens in the [`ui-beta-build` session](../system/sessions/ui-beta-build/) — read `session-ui-beta-build.md` for procedure and `context.md` for current state. Track D (`car-t-006`) below = roadmap's P7.

### Track C — `Wow.Two.Sdk.Beta.*` backend operational (`car-t-005`)

**Owner chat:** `wow-two - track-c-backend-beta`
**Deadline:** 2026-06-15
**Outcome:** Working `wow-two-sdk-beta.backend` repo, CI publishing on push, first packages ported from haven.

| # | Task | Notes |
|---|---|---|
| C1 | Create empty `wow-two-sdk-beta.backend` repo on GitHub (manual) | Must precede C2 |
| C2 | Scaffold .NET solution with multi-project layout, one csproj per package | Mirror `ui.beta` philosophy: many packages, one repo |
| C3 | Set up GitHub Actions: build + test (skip)→ pack → push to NuGet on push to main | Auto-bump `0.0.y` |
| C4 | Decide first 3–5 backend packages to port from haven (likely: shared types, validation utilities, EF Core base patterns) | List in this doc once known |
| C5 | Port each package: extract from haven, publish, swap haven's reference | One PR per package |

### Track D — Haven migration (`car-t-006`)

**Owner chat:** `wow-two - track-d-haven-consume`
**Deadline:** 2026-06-30
**Outcome:** Haven imports come from `@wow-two-beta/ui` and `Wow.Two.Sdk.Beta.*` packages. Inline copies retired.

| # | Task | Notes |
|---|---|---|
| D1 | Audit haven for components/utilities that exist in both haven and beta packages (drift risk) | Spreadsheet or markdown table |
| D2 | Per duplicate: delete haven inline copy, import from beta package, smoke-test | Sequential per component |
| D3 | Audit haven for reusable components NOT yet ported — feed into Track B/C task lists | Loop back |
| D4 | Final pass: Storybook lists every haven UI component | Confirms B is done |

---

## Parallelism map

```
Track A ────┐
            ├─→ B3 (CI) needs A's npm scope created
Track B ────┤
            ├─→ B4 (publish) needs A3 stub to exist first
Track C ────┤  (C3 publish needs A4+A5 NuGet reservation)
            │
Track D ────┴─→ blocked until B and C have something to consume
```

Bare minimum unlock order: A1 + A2 (npm orgs) → B can publish | A4 + A5 (NuGet) → C can publish | B + C have packages → D can migrate.

A1–A4 are user actions (account creation, first publish). A5 is wait-time. Everything else can be chat-driven.

## Active chats

| Chat name | Track | State |
|---|---|---|
| `wow-two - track-a-reservation` | A | Not started |
| `wow-two - track-b-ui-beta` | B | This chat |
| `wow-two - track-c-backend-beta` | C | Not started |
| `wow-two - track-d-haven-consume` | D | Not started — blocked until B/C ship |

Update this table as chats spawn / finish.

---

## Steady-state operating rules

Once tracks A–C are operational:

1. **New component or package?** Spec first → code → stories → push to main. CI auto-publishes.
2. **Bug or breakage?** Fix commit to main. No revert ceremony. No issue tracker.
3. **Need something not in beta yet?** Add it. No ADR, no review, no spec template policing — just write `*.spec.md` first.
4. **Cross-domain duplication keeps appearing?** Promote to `utils/` or `hooks/`. ESLint will already block sibling-domain imports — that's the forcing function.
5. **Naming a new package?** `@wow-two-beta/{name}` (npm) or `Wow.Two.Sdk.Beta.{Name}` (NuGet). Always — see naming convention table at top.

This document moves from "launch plan" to "operating manual" once Track D ships.
