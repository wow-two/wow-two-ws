# WoW 2.0 — npm Library Playbook

*Last updated: 2026-04-20*

> **Scope:** All npm-published libraries under `wow-two-sdk` (UI components, TS utilities, design tokens). Distinct from the .NET/NuGet strategy in `branching-strategy.md` which keeps `dev` + `main` and dual-publishes to GitHub Packages + NuGet.org.
> **Status:** Living document. Pin decisions here first, restructure into a dedicated `wow-two.handbook` repo later.

---

## Why this exists

The .NET side has `branching-strategy.md` + `versioning-strategy.md` optimized for NuGet + dev-alpha channels. The npm/UI side has different constraints (monorepos, per-package versioning, Changesets tooling, OSS PR flow). This playbook codifies the npm-side decisions so every new UI repo starts identical.

---

## Ecosystem shape

~9 monorepos, ~50 published packages eventually. Taxonomy:

| Layer | Repo | Contains |
|---|---|---|
| Foundation | `wow-two-sdk.ts.*` | Framework-agnostic TS (utils, async, validation, date, http, state) |
| Design system | `wow-two-sdk.ui.tokens` | Design tokens (JSON + CSS vars) |
| Design system | `wow-two-sdk.ui.tailwind` | Tailwind preset consuming tokens |
| Design system | `wow-two-sdk.ui.icons` | Icon set |
| React primitives | `wow-two-sdk.ui.react.core` | Button, Input, Dialog, Tooltip, Menu (Radix-wrapped) |
| React primitives | `wow-two-sdk.ui.react.form` | Forms + validation integration |
| React primitives | `wow-two-sdk.ui.react.layout` | Stack, Grid, Container, Split |
| React primitives | `wow-two-sdk.ui.react.hooks` | Shared hooks |
| React domain | `wow-two-sdk.ui.react.media` | Image, video, audio, gallery, cropper |
| React domain | `wow-two-sdk.ui.react.geo` | Maps, markers, geocoder |
| React domain | `wow-two-sdk.ui.react.data` | Table, tree, charts, kanban |
| React domain | `wow-two-sdk.ui.react.editor` | Rich text, code, markdown |
| React domain | `wow-two-sdk.ui.react.feedback` | Toast, modal, banner, progress |
| React domain | `wow-two-sdk.ui.react.nav` | Sidebar, tabs, breadcrumbs, command palette |
| React domain | `wow-two-sdk.ui.react.files` | Upload, dropzone, file picker |
| React domain | `wow-two-sdk.ui.react.auth` | Login forms, OAuth buttons |
| React domain | `wow-two-sdk.ui.react.ai` | Chat UI, message stream, prompt box |
| Showcase | `wow-two-sdk.ui.react.sandbox` | Vite app consuming published packages (extracted once 2–3 domain repos are live) |

Starting set: `ui.tokens`, `ui.tailwind`, `ui.react.core`.

---

## License

**MIT** for all npm libraries. Allows reuse, repackaging, editing, commercial use. Widest corporate acceptance. No patent-clause complications.

---

## Stack (every repo)

| Concern | Pick |
|---|---|
| Package manager | pnpm (local + CI) |
| Language | TypeScript, `strict: true` |
| Lib bundler | tsup (ESM + CJS + d.ts) |
| App bundler | Vite (Storybook, playground, sandbox) |
| Styling | Tailwind + CSS variables (tokens → preset) |
| Primitives | Radix UI (React-only, production-proven) |
| Testing | Vitest + Testing Library |
| E2E (later) | Playwright (smoke only) |
| Component catalog | Storybook 8 |
| Versioning / publish | Changesets |
| Registry | npm public |
| CI | GitHub Actions |

Radix chosen over Ark UI — reliability & production adoption > cross-framework. Future Vue port rebuilds primitives on Reka UI, reusing tokens.

---

## Branching strategy — GitHub Flow

```
main (protected, always releasable, always green)
  ↑ PR (squash merge)
  │
  ├── feat/core-button
  ├── fix/tokens-color-export
  ├── docs/readme-setup
  └── chore/ci-pnpm-cache
```

### Rules

- `main` is the only long-lived branch. No `develop`, no `release/*`.
- Short-lived branches off `main`: `feat/*`, `fix/*`, `docs/*`, `refactor/*`, `chore/*`, `test/*`, `ci/*`.
- Delete branch after merge (GitHub auto-delete setting ON).
- Branch naming: `{type}/{scope}-{short-kebab}` — e.g. `feat/button-variants`. In monorepos add package scope: `feat/core/button`.

### Main protection

| Setting | Value |
|---|---|
| Require PR before merge | ✅ |
| Require CI green | ✅ (lint + typecheck + test + build + changeset status) |
| Require changeset file | ✅ strict — every PR, label `skip-changeset` only for docs/chore/ci |
| Required approvals | 0 (solo dev phase — revisit when contributors arrive) |
| Include administrators | ✅ (no owner bypass — force yourself through PRs) |
| Allow force push | ❌ |
| Allow deletion | ❌ |
| Require linear history | ✅ |

### Merge method

- **Squash merge only.** Disable merge commits and rebase-merge in repo settings.
- PR title = conventional commit (`feat(core): add Button`) — becomes the squashed commit message on main.
- One commit per PR. Changesets reads clean history.

### Commit / PR title convention

Conventional Commits:
- `feat(scope): ...`
- `fix(scope): ...`
- `docs(scope): ...`
- `refactor(scope): ...`
- `chore(scope): ...`
- `test(scope): ...`
- `ci(scope): ...`
- Breaking: `feat(core)!: ...` or `BREAKING CHANGE:` footer

Enforced via `commitlint` in CI on PR titles.

---

## Release flow (Changesets)

1. Contributor PR includes `.changeset/*.md` describing bump type + changelog line per affected package.
2. PR squash-merged to `main`.
3. Changesets GitHub Action opens (or updates) a **"Version Packages"** PR aggregating pending changesets — bumps `package.json` versions, regenerates `CHANGELOG.md` per package, updates internal dep ranges, deletes consumed changeset files.
4. Merging the "Version Packages" PR runs `changeset publish` in CI: publishes each bumped package to npm, creates git tags (`@wow-two-sdk/ui-tokens@0.2.0`), creates GitHub releases with changelog body.

No manual tagging. No release branches. No version bumps in feature PRs.

### Hotfixes

Same as features: `fix/*` branch → PR → merge → Changesets ships patch. Separate flow only needed when maintaining multiple majors simultaneously.

### Snapshot / preview releases

For PR previews: `pnpm changeset version --snapshot pr-42 && pnpm changeset publish --tag next`. Published under `next` dist-tag, not `latest`.

---

## Issue & task tracking

- **GitHub Issues** from day one — permanent public log, auto-linked to PRs (`Fixes #12`), OSS-ready.
- **GitHub Projects v2** — one board `WoW 2.0 UI` aggregating issues across all `wow-two-sdk.ui.*` repos. Single inbox despite multi-repo layout.
- **Labels** (applied in every repo): `area:{package}`, `type:bug|feat|docs|chore|refactor`, `priority:high|med|low`, `good-first-issue`, `skip-changeset`, `breaking`.
- High-level roadmap/vision lives in `wow-two.refinement` + `wow-two.roadmap`; concrete tasks live as issues.
- Personal OS tasks (`10x-ws/system/planning/pln-tasks.md`) only track *your* next actions — not project backlog.

---

## Repo template (every UI repo)

```
{repo}/
├── .changeset/                      ← config + pending changesets
│   └── config.json
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                   ← lint + typecheck + test + build + changeset status
│   │   └── release.yml              ← changesets/action → publish
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
├── packages/                        ← monorepo: multiple publishable packages
│   └── {name}/
│       ├── src/
│       ├── package.json
│       ├── tsconfig.json
│       ├── tsup.config.ts
│       └── README.md
├── apps/                            ← non-published apps
│   ├── docs/                        ← Storybook
│   └── playground/                  ← Vite sandbox for manual QA
├── CLAUDE.md                        ← from template
├── README.md
├── LICENSE                          ← MIT
├── CHANGELOG.md                     ← root, optional summary
├── .gitignore
├── .npmrc
├── pnpm-workspace.yaml
├── tsconfig.base.json
├── package.json                     ← root, private: true
└── commitlint.config.js
```

Single-package repos (e.g. `ui.tokens`) skip `packages/` + `pnpm-workspace.yaml` and put source at root `src/`.

---

## Cross-cutting decisions

| Decision | Choice | Rationale |
|---|---|---|
| Monorepo vs multirepo | Monorepo per layer/domain (~9 repos, ~50 pkgs) | 50 separate repos = CI hell; 1 repo = coupling risk; layer monorepos = fast CI + independent shipping |
| Independent or fixed versioning | Independent per package | Consumers cherry-pick, domain packages version at their own pace |
| Internal deps (intra-monorepo) | `workspace:^` ranges | pnpm rewrites on publish, keeps dev graph clean |
| CSS strategy | Tailwind + CSS vars from tokens | Single source of design truth, no CSS-in-JS runtime cost |
| Publish target | npm public only | GitHub Packages not needed — no internal-only layer for UI |
| Supported Node | Active LTS only | Drops in sync with Node release schedule |
| Test runner | Vitest | Vite-native, ESM-first, fast |

---

## Related docs

- `docs/branching-strategy.md` — .NET/NuGet side (kept separate, different constraints)
- `docs/versioning-strategy.md` — .NET/NuGet versioning
- `docs/wow-two-refinement.md` — overall project state & roadmap
- `.claude/rules/repo-registry.md` — live list of all repos
