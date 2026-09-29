# SDK Repo Structure

*Last updated: 2026-09-29*

On-disk layout + naming for **SDK / library repos** under `wow-two-ws/workbench/` — the package-shaped counterpart to [repo-structure.md](repo-structure.md) (product / venture repos). Reference: `wow-two-sdk-beta.ui` (`@wow-two-beta/ui`). Not yet executed — see *Application*.

---

## Archetype

- must treat an SDK / library repo (`wow-two-sdk.*`, `wow-two-sdk-beta.*`) as its own archetype — supersedes the "package-shaped, exempt" SDK row in [repo-structure.md](repo-structure.md) §1
- must adopt the doc-bearing shell — `engineering/` (planning + architecture) at the repo root, same as a product repo
- must omit `product/` — a library has no user-product surface; the shipped thing is the npm package
- must nest the whole npm package under `engineering/codebase/{slug}/` — one package = one code dir, the SDK counterpart of `{slug}.backend-services/` / `{slug}.frontend-services/`
- must name the code dir with the package `{slug}` (bare) — never the `.frontend-services` suffix, which reads as an app frontend, not a library

---

## Layout

```
{repo}/                              ← e.g. wow-two-sdk-beta.ui
├── README.md · CLAUDE.md            ← entry docs — root ONLY
├── .claude/ · .git/ · .gitignore
├── .github/workflows/               ← CI runs from repo-root .github only
└── engineering/
    ├── engineering.md
    ├── planning/                    ← backlog.md · version-track/v{X.Y}/v{X.Y}.md
    ├── architecture/                ← architecture.md · decisions/ · testing.md
    ├── research/                    ← analyses and deep-dives (research.md lead)
    ├── development/                 ← rules.md — working rules for agents
    └── codebase/
        ├── codebase.md
        └── {slug}/                  ← THE npm package
            ├── package.json · pnpm-lock.yaml · pnpm-workspace.yaml
            ├── tsconfig*.json · tsup.config.ts · vitest.config.ts · eslint.config.js
            ├── .storybook/          ← catalog + vitest-setup config
            ├── src/                 ← SOURCE ONLY — components · *.variants.ts · index.ts
            ├── tests/
            │   ├── unit/            ← *.test.ts(x) — vitest unit + browser projects
            │   └── stories/         ← *.stories.tsx — interaction tier + Storybook catalog
            ├── apps/                ← pnpm-workspace sandboxes (playground · showcase · theme-studio)
            └── LICENSE · README.md  ← npm-packable copies (files allowlist can't reach above package.json)
```

- must keep `src/` source-only — components, `*.variants.ts`, `index.ts` barrels; no `*.test.*`, no `*.stories.*`, no test infra
- must split hand-written verification out of `src/` into `tests/` (see *Tests*)
- must keep the package's own `package.json`, lockfile, and every tool config inside `engineering/codebase/{slug}/`

---

## Package boundary

The package is defined by where `package.json` sits — it plus the lockfile, configs, `src/`, `tests/`, `apps/` are one atomic unit.

- must move the package as one unit — every path inside stays package-root-relative (`./src/**`, `../src`, `./tsconfig.json`), so relocation is ~0 edits to the src-globbing configs
- must keep root-pinned at the repo root: `.git/`, `.gitignore`, `.github/workflows/`, `.claude/`, `CLAUDE.md`, `README.md` — git / GitHub / Claude entry points
- must place a `LICENSE` copy + a package `README.md` beside `package.json` — npm's `files` allowlist can't pack files above `package.json`
- may leave cascade config (`.editorconfig`, `.prettierrc`, `.npmrc`) at the repo root — nearest-upward wins, still governs the nested package
- must reach into the package from CI via `working-directory: engineering/codebase/{slug}` — GitHub only runs workflows from repo-root `.github/`
- must set `package.json` `repository.directory` to `engineering/codebase/{slug}`, and re-path any `.gitignore` negation + the `wow-two-ws/scripts/active.sh` frontend entry

---

## Planning

- must plan with `engineering/planning/backlog.md` and `engineering/planning/version-track/v{X.Y}/v{X.Y}.md` only, per [version-track.md](../../../planning/version-track/version-track.md) — no flat `v0.1.md`, no polish track, no planning lead doc
- must track the SDK's vectors and every ecosystem-wide extraction in its backlog
- must put design docs under `engineering/architecture/` — `architecture.md` · `decisions/` · `testing.md`; analyses and deep-dives under `engineering/research/`
- must keep `product/` absent — `planning/`, `architecture/` and `research/` are the only `engineering/` design surfaces an SDK needs

---

## Tests

- must mirror `src/` under `tests/`, split by nature: `tests/unit/` = pure-logic `*.test.ts(x)`; `tests/stories/` = `*.stories.tsx` (catalog + interaction tier)
- must move the build-excluded test infra out of `src/` too — the local kit (`src/testing/`), engine conformance (`src/forms-engine/conformance/`), and `*.shared.*` suites are test-only (already in `tsconfig.json` `exclude`) → under `tests/`
- must not move `src/query/testing.ts` — it ships (the `./query/testing` export) and is source, unlike the internal `src/testing/` kit
- must repoint the vitest `unit` + `browser` project `include` globs from `src/**` to `tests/unit/**` — keep both test-file kinds in one home
- must repoint the `.storybook/main.ts` `stories` glob `../src/**/*.stories.@(ts|tsx)` → `../tests/stories/**/*.stories.@(ts|tsx)` — the vitest `storybook` project derives its file list from it
- must add one tsconfig path alias `"@src/*": ["src/*"]` and resolve it in `vitest.config.ts` (`resolve.alias` or `vite-tsconfig-paths`) — tests import `@src/...`, not `../../src/...`
- must repoint the eslint test/story override `files` (`src/**/*.{test,stories,shared}.*`, `src/testing/**`) → `tests/**`; keep the `boundaries/elements` patterns on `src/**` (source-only, now exact)
- must include `tests/**` in `tsconfig.typecheck.json` so story / test drift still fails `pnpm typecheck`; the build `tsconfig.json` includes `src/**/*` only → tests never emit to `dist`
- may keep an import-coupled `*.shared.*` suite beside its engine — verify resolution after the move (the one edge the prior analysis flagged)

---

## Story extraction

Empirically proven viable — probe (2026-07-12): one Button story relocated to a non-`src/` path (`tests/stories-probe/`), then fully reverted.

- `*.stories.tsx` may live outside `src/` — only two things change: the `.storybook/main.ts` `stories` glob + the story's component import (`./Button` → `@src/presentation/actions/button/Button`)
- the Storybook catalog builds — the relocated story + its `autodocs` docs entry index normally (`pnpm build:storybook` clean)
- react-docgen props still populate — docgen is keyed to the `component:` ref (the source file in `src/`), independent of the story's location
- the addon-vitest `storybook` project runs the story's `play()` from the new path — 6/6 (render smoke + 5 interaction tests) green via `pnpm vitest run --project storybook tests/stories`
- reverses the earlier "stories stay colocated" recommendation — the `src/` ↔ `tests/` split is the chosen shape and it holds

---

## Publish

- must keep the publish artifact dist-only — `files: ["dist", "README.md", "LICENSE"]`; `src/`, `tests/`, `apps/`, `engineering/`, every `.md` never ship, wherever they sit
- relocating the package does not change the tarball — `prepublishOnly` (`pnpm typecheck && pnpm build`) runs from the package root; subpath `exports` resolve `./dist/**` unchanged
- must point npm + GitHub at the subdir via `package.json` `repository.directory`

---

## Apps

- must keep `apps/*` (sandboxes: `playground` · `showcase` · `theme-studio`) inside the package at `engineering/codebase/{slug}/apps/` — pnpm-workspace members (`pnpm-workspace.yaml`), package-root-relative
- must not publish `apps/*` — absent from the `files` allowlist

---

## Slug — decided

- code-dir `{slug}` = **`wow-two-front-beta-sdk`** (owner, 2026-07-11) — explicit + ecosystem-descriptive, aligns with the backend SDK naming
- the npm package stays `@wow-two-beta/ui` for now; it is renamed later to match the backend SDK (separate task) — the code-dir slug leads that rename

---

## Application

- APPLY LATER — this doc is the reviewable spec, not yet executed against the SDK
- must adopt it in `engineering/planning/version-track/v0.1.md` Iteration 1 (row 1): whole package → `engineering/codebase/{slug}/` · `tests/{unit,stories}` split · `engineering/` planning + architecture
- must verify green after the move — `pnpm -C engineering/codebase/{slug} build|test|lint|typecheck` + an `npm pack` dry-run (dist contents unchanged)
