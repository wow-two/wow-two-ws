# SDK structure

*Last updated: 2026-10-01*

> On-disk layout and naming of an SDK / library repo under `wow-two-ws/workbench/` — the package-shaped
> counterpart of [repo structure](repo-structure.md).
> Use case — placing a package, its tests or its sandboxes, or relocating a package inside its repo.

## Archetype

- must treat an SDK / library repo — `wow-two-sdk.*`, `wow-two-sdk-beta.*` — as its own archetype.
- must adopt the doc-bearing shell: `engineering/` at the repo root, as a product repo has.
- must omit `product/`; the shipped thing is the package.
- must nest each package under `engineering/codebase/{slug}/` — one package, one code directory.
- must name that directory with the package's bare `{slug}`, never a `.frontend-services` suffix.

---

## Layout

```
{repo}/                              e.g. wow-two-sdk-beta.ui
├── README.md · CLAUDE.md            entry docs — root only
├── .claude/ · .gitignore
├── .github/workflows/               CI runs from the repo root only
└── engineering/
    ├── engineering.md
    ├── planning/                    backlog.md · version-track/v{X.Y}/v{X.Y}.md
    ├── architecture/                architecture.md · decisions/ · testing.md
    ├── research/                    analyses and completeness maps (research.md)
    ├── development/                 rules.md — working rules for agents
    └── codebase/
        ├── codebase.md
        └── {slug}/                  the package, e.g. wow-two-front-vue-beta-sdk
            ├── package.json · pnpm-lock.yaml · pnpm-workspace.yaml
            ├── tsconfig*.json · vite.config.ts · vitest.config.ts · eslint.config.js
            ├── src/                 source only
            ├── tests/               unit/ · support/ · types/
            ├── apps/                workspace sandboxes — playground, atlas
            ├── scripts/             build and release helpers
            └── LICENSE · README.md  the copies npm packs
```

- must keep the package's manifest, lockfile and every tool config inside `engineering/codebase/{slug}/`.
- must take a .NET package family's inner layout from the
  [SDK shape](../../backend/dotnet/shapes/sdk/sdk.md); this doc fixes only the repo shell around it.

---

## Package boundary

- must treat `package.json` with its lockfile, configs, `src/`, `tests/` and `apps/` as one unit.
- must move the package as that unit; every path inside stays package-root-relative.
- must keep `.git/`, `.gitignore`, `.github/workflows/`, `.claude/`, `CLAUDE.md` and `README.md` at the repo root.
- must place a `LICENSE` copy and a package `README.md` beside `package.json`; npm cannot pack files above it.
- may leave cascade config — `.editorconfig`, `.prettierrc`, `.npmrc` — at the repo root.
- must reach the package from CI with `working-directory: engineering/codebase/{slug}`.
- must set `repository.directory` in `package.json` to `engineering/codebase/{slug}`.
- must update the `wow-two-ws/scripts/active.sh` entry when the package moves.

---

## Planning

- must plan with `engineering/planning/backlog.md` and `version-track/v{X.Y}/v{X.Y}.md` only
  ([version track](../../../planning/version-track/version-track.md)).
- must track the SDK's vectors and every ecosystem-wide extraction in its backlog.
- must put design docs under `engineering/architecture/`, analyses under `engineering/research/`.

---

## Tests

- must keep `src/` source-only — no `*.test.*`, no stories, no test infrastructure.
- must mirror `src/` under `tests/unit/`; shared fixtures sit in `tests/support/`, type-level checks in `tests/types/`.
- must keep a module that ships, such as a `./query/testing` export, in `src/`; it is source.
- must point the test runner's `include` globs at `tests/**`, never at `src/**`.
- must import source in a test through the `@src/*` alias, declared in `tsconfig.json` and resolved by the runner.
- must include `tests/**` in the typecheck project, and keep the build project on `src/**` alone.
- tiers, the interaction matrix and gates → [library testing](../../frontend/shapes/library/testing/testing.md).

---

## Publish

- must keep the published artifact dist-only — `files: ["dist", "README.md", "LICENSE"]`.
- must not ship `src/`, `tests/`, `apps/`, `engineering/` or any other `.md`, wherever they sit.
- exports, peers, CSS and release verification →
  [library delivery](../../frontend/shapes/library/delivery/delivery.md).

---

## Apps

- must keep sandboxes in `apps/*` inside the package, as workspace members.
- must not publish `apps/*`; they stay out of the `files` allowlist.
