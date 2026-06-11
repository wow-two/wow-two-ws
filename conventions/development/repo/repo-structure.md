# Repo Structure Standard

*Last updated: 2026-06-10*

> **Scope:** the on-disk layout + naming for **product / venture repos** under `wow-two-ws/workbench/`.
> The *structural* layer — folders + names, not code style (that lives in [`backend/`](../backend/) and
> [`frontend/`](../frontend/)).
>
> **Reference implementation:** `workbench/ventures/10x-ven-haven` (most built-out; this standard
> generalizes its shape). **Template:** `workbench/wow-two-sdk-beta/wow-two-sdk-beta.product-template`
> (stamped by the `create-repo` skill).

## 1. Two archetypes

| Archetype | Shape | Examples | Governed by |
|---|---|---|---|
| **Product / venture** | `product/` + `engineering/` (code under `engineering/codebase/`) | haven, drydock, smart-qr, secrets-vault | **this standard** |
| **SDK / library** | package-shaped (`src/` = the library; no product/engineering split) | `wow-two-sdk.*`, `wow-two-sdk-beta.ui` | SDK docs + `.claude/rules/templates/CLAUDE-sdk.md` |

A product repo *ships a thing to users*; a library repo *is consumed by other repos*. Don't force one shape into the other.

## 2. Canonical layout (product / venture repo)

```
{repo}/
├── README.md                     ← human entry — root ONLY
├── CLAUDE.md                     ← Claude entry: lazy-load rules, stack, structure
├── .claude/rules/
│   └── file-references.md        ← doc lookup table (never lists engineering/codebase/* files)
│
├── product/                      ← the DEFINITION — what · why · features · flows. NO code.
│   ├── product.md                ← what it is · who for · positioning · model (durable lead doc)
│   ├── context.md                ← current state + decisions (changes often)
│   ├── features/                 ← per-feature specs (features.md + one doc per feature)
│   ├── flows/                    ← user / product flows + diagrams (flows.md + …)
│   ├── planning/                 ← product milestones + roadmap (planning.md)
│   └── marketing/                ← GTM · channels · campaigns (marketing.md + …)
│
└── engineering/                  ← the EXECUTION — build · ship · run
    ├── engineering.md            ← technical overview · stack · map (lead doc)
    ├── architecture/             ← system + per-area design (architecture.md + …)
    ├── codebase/                 ← THE CODE — and the only place code lives
    │   ├── codebase.md           ← what services live here (lead doc)
    │   ├── backend-services/     ← .NET (Clean Arch) — solution + projects (+ tests/)
    │   ├── frontend-services/    ← React (Vite / pnpm)
    │   ├── database/             ← SQL / migrations, when managed apart (optional)
    │   └── pipelines/            ← data pipelines (optional)
    ├── development/              ← build guidelines + process
    │   ├── development.md        ← lead doc
    │   ├── backend-guidelines.md · frontend-guidelines.md · iteration-guide.md
    ├── deployment/              ← Dockerfile · compose · ops · domain setup (deployment.md + …)
    ├── planning/                ← planning.md (roadmap + tracker) · backlog.md · rules.md
    ├── versions/                ← per-version iteration docs (versions.md + v{X.Y}/v{X.Y}.md)
    ├── research/                ← technical research dumps (research.md + …)
    ├── scripts/                 ← dev / ops scripts (scripts.md + …)
    └── secrets/                 ← gitignored local env (optional)
```

## 3. Doc rule — no README below root

- **`README.md` lives only at the repo root** (GitHub entry), beside `CLAUDE.md`.
- **Every folder opens with a meaningfully-named lead doc `{folder}.md`** — `architecture/architecture.md`,
  `deployment/deployment.md`, `product/product.md`, `engineering/engineering.md` — **never** a generic
  `README.md`. The lead doc orients: what's here, why, pointers.
- Additional docs sit beside the lead with meaningful names (`planning/` → `planning.md` + `backlog.md` + `rules.md`).

## 4. Folders, not loose files — grow-ready by default

- **If a concern can grow past one file, it is a folder from day one** — don't start as a loose file and migrate later.
- **Create now the folders the repo will need**; omit only the truly-N/A ones (add when real).
- Proven set (Haven): product → `features/ flows/ planning/ marketing/`; engineering → `architecture/ codebase/ development/ deployment/ planning/ versions/ research/ scripts/`.

## 5. Naming rules — the non-negotiables

1. **Top-level dirs are exactly `product/` and `engineering/`** (lowercase). Plus root `README.md`, `CLAUDE.md`, `.claude/`.
2. **All code lives under `engineering/codebase/`.** Always a `codebase/` wrapper — never services directly under `engineering/`.
3. **The code dirs are exactly `codebase/backend-services/` and `codebase/frontend-services/`** (+ optional `database/`, `pipelines/`). Never `backend`/`frontend`, never `{name}.backend`, never a loose dir outside `codebase/`.
4. **`backend-services/` holds the solution + projects directly.** `.sln`/`.slnx` at its root; projects `{Brand}.{Domain}[.{SubDomain}]` PascalCase. Clean-Arch layers per [`backend/service-architecture.md`](../backend/service-architecture.md).
5. **`frontend-services/` holds the app directly (single) or a pnpm workspace (multi)** — app folders (lowercase) + `packages/` for shared (`@{brand}/common`, `@{brand}/ui`).
6. **Per-repo `development/` guidelines defer to shared conventions** (`wow-two-ws/conventions/*.md`) — only repo-specific deltas live in the repo.

## 6. Tests

- **Backend:** a `tests/` folder inside `codebase/backend-services/`, its projects in the same solution (`{Brand}.{Domain}.Tests`).
- **Frontend:** colocated with the code (`*.test.ts(x)` beside source, or `__tests__/`).

## 7. Typed clients / contracts

- A backend's typed client consumed by the **frontend** → lives in `codebase/frontend-services/` (generated / maintained there).
- A backend's typed client consumed by **another backend** → a package project inside `codebase/backend-services/` (`{Brand}.{Service}.Client` / `.Abstractions`), referenced or published like any package.
- **No** separate top-level `contracts/`.

## 8. Deployment

- **One image per deployable service is the unit;** `docker compose` *orchestrates* them — it is not an alternative to per-service images.
- **Single-service** → a `Dockerfile` is enough (+ optional compose for local env/volumes). **Multi-service** → per-service Dockerfiles + one compose.
- **Location:** `engineering/deployment/` holds `Dockerfile` + `docker-compose.yml`; **build context = `engineering/codebase/`** (compose: `context: ../codebase`, `dockerfile: ../deployment/Dockerfile`); `.dockerignore` at the context root (`codebase/`).

## 9. Single-service vs multi-service

| | `codebase/backend-services/` | `codebase/frontend-services/` |
|---|---|---|
| **Single** (drydock, smart-qr, secrets-vault) | solution + Clean-Arch projects directly | the Vite app directly (`package.json` at root) |
| **Multi** (haven) | one folder per service under a shared solution | pnpm workspace: app folders + `packages/` |

## 10. Migration ripple (do in lockstep with any rename)

- **`wow-two-ws/scripts/active.sh`** — the `PROJECTS` registry (backend `.sln` + frontend dir paths).
- Each repo's **deploy script** (SPA → `wwwroot` relative path), **`Dockerfile`** (`COPY` paths), and **compose** context.
- **`.sln`/`.slnx`:** moving the backend folder as a unit preserves its relative project refs; a depth change (introducing `codebase/`) re-paths only *external* references, not the solution internals.

## 11. Audit — product repos vs this standard (2026-06-10)

`✓` conforms · `✗` deviates. Targets are now `product/` + `engineering/` + `engineering/codebase/` + folder-docs.

| Repo | top-level | `codebase/` | folder-docs | CLAUDE | Fixes needed |
|---|:--:|:--:|:--:|:--:|---|
| secrets-vault | 🚧 | 🚧 | 🚧 | ✓ | rename pilot: `business-logic`→`product`, `platform-development`→`engineering`, `src`→`codebase`, READMEs→`{folder}.md`, `analysis`→`research` |
| smart-qr | ✗ | ✗ | ✗ | ✓ | full conform (next) |
| haven | ✗ (`business/`+`platform/`) | ✗ (`src/`) | ✗ | ✓ | top-level rename; `src`→`codebase`; folder-docs |
| drydock | ✗ | ✗ | ✗ | ✓ | top-level; `*.backend`→`codebase/backend-services`; folder-docs |
| trademark · yt-scraper · acquisition · pdf-editor | ✗ | ✗ | ✗ | ✗ | scaffold to standard |

> The 2026-06-09 audit is **superseded** — the top-level names changed (`business-logic/`+`platform-development/` → `product/`+`engineering/`) and `src/`→`codebase/`, plus the no-README rule.

## 12. Ecosystem naming

- **Orgs:** lowercase, hyphenated — `wow-two-sdk`.
- **Repos:** `{org}.{domain}[.{subdomain}]`, lowercase, dot-separated — `sdk.language.core`, `platform.storage.cache`.
- **NuGet:** PascalCase branded — `WoW.Two.Sdk.Language.Core`.
- **Branches:** `main` · `feature/*` · `fix/*` · `docs/*`. **Commits:** conventional (`feat:`/`fix:`/`docs:`/`refactor:`).
