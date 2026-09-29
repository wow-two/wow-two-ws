# Repo Structure Standard

*Last updated: 2026-09-29*

> **Scope:** the on-disk layout + naming for **product / venture repos** under `wow-two-ws/workbench/`.
> The *structural* layer — folders + names, not code style (that lives in [`backend/`](../../backend/) and
> [`frontend/`](../../frontend/)).
>
> **Reference implementation:** `workbench/ventures/10x-ven-haven` (most built-out; this standard
> generalizes its shape). **Template:** `workbench/wow-two-sdk-beta/wow-two-sdk-beta.product-template`
> (stamped by the `create-repo` skill).

## 1. Two archetypes

| Archetype | Shape | Examples | Governed by |
|---|---|---|---|
| **Product / venture** | `product/` + `engineering/` (code under `engineering/codebase/`) | haven, wheelhouse, forever-pin, secrets-vault | **this standard** |
| **SDK / library** | doc-bearing package — `engineering/` at root, the npm package under `engineering/codebase/{slug}/`, no `product/` | `wow-two-sdk.*`, `wow-two-sdk-beta.ui` | [sdk-structure.md](sdk-structure.md) |

A product repo *ships a thing to users*; a library repo *is consumed by other repos*. Don't force one shape into the other.

---

## 2. Canonical layout (product / venture repo)

Frontend framework selection → [frontend standard](../repo-conventions.md#frontend-standard).

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
│   ├── features/                 ← per-feature specs, one doc per feature (listed in the backlog's Features group)
│   ├── flows/                    ← user / product flows + diagrams (flows.md + …)
│   └── marketing/                ← GTM · channels · campaigns (marketing.md + …)
│
└── engineering/                  ← the EXECUTION — design · plan · build · ship · run
    ├── engineering.md            ← technical overview · stack · map (lead doc)
    ├── architecture/             ← DESIGN — system + per-area design
    │   ├── architecture.md       ← lead doc
    │   ├── flows/                ← per-flow docs (`{flow}-flow.md` — Overview + bottom-up layer table)
    │   ├── infra/                ← cross-cutting subsystem design
    │   └── {domain}/             ← per-domain / per-subsystem design docs
    ├── research/                 ← analyses + pre-decision investigation (research.md lead; graduates to a design doc)
    ├── planning/                ← PLAN — what + when (version-track.md; no lead doc here)
    │   ├── backlog.md           ← every unbuilt item, grouped, top = next · Features group
    │   └── version-track/       ← v{X.Y}/v{X.Y}.md per version; the newest folder is active, CI reads its X.Y
    ├── codebase/                 ← BUILD — THE CODE (the only place code lives)
    │   ├── codebase.md           ← what services live here (lead doc)
    │   ├── {slug}.backend-services/   ← .NET (Clean Arch) — solution + projects (+ tests/)
    │   ├── {slug}.frontend-services/  ← pnpm workspace: apps/web/ + optional packages/
    │   ├── database/             ← SQL / migrations, when managed apart (optional)
    │   └── pipelines/            ← data pipelines (optional)
    ├── development/              ← BUILD — guidelines + process
    │   ├── development.md        ← lead doc
    │   ├── rules.md              ← working rules for agents in this repo
    │   ├── backend-guidelines.md · frontend-guidelines.md · iteration-guide.md
    ├── deployment/              ← SHIP — Dockerfile · compose · domain setup (deployment.md)
    └── operations/              ← RUN — repo setup · scripts · runbooks · secrets/ (gitignored) (operations.md)
```

> **`{slug}`** = the repo's distinctive lowercase hyphenated name — its last dot-segment
> (`secrets-vault`, `wheelhouse`; the product-template's slug is `sample`). The two code dirs carry it
> as a **dot-prefix** so multiple open repos never collide on a bare `backend-services/` /
> `frontend-services/` folder name in an IDE.

---

## 2.1 Business-folder layout (the venture layer)

> The venture-side counterpart to `engineering/`. In repos still on the `business/`+`platform/` shape
> (haven), **`business/` is the venture layer** (the conceptual sibling of `product/` in §2);
> `platform/` stays the **technical** layer. Same folder discipline as §4 — folders the moment a concern
> can grow past one file. **Reference implementation:** `workbench/ventures/10x-ven-haven/business/`.

```
business/                          ← the venture layer — model · positioning · GTM. NO code.
├── business-context.md           ← current state + active business tasks + decisions (changes often)
├── business-knowledge.md         ← model · pricing · positioning · target users (durable lead doc)
│   …plus standalone analysis docs may sit at root until a folder earns them
├── analysis/                     ← product / feature / market research + analysis docs
├── marketing/                    ← GTM · channels · campaigns (mkt-context/knowledge/analysis/guides/tasks)
├── planning/                     ← business planning (business-planning.md) — distinct from platform/planning/
└── flows/                        ← business / supply / user flow diagrams (*.mermaid)
```

- **Core docs at root:** `business-context.md` (current state) + `business-knowledge.md` (model/pricing/positioning). Standalone analysis docs may also sit at root until a subfolder earns them.
- **Subfolders, created as needed** (omit until real, per §4): `analysis/` · `marketing/` · `planning/` · `flows/`.
- **`planning/` is the *business* roadmap** — keep it distinct from `platform/planning/` (the technical roadmap); cross-reference, don't merge.

---

## 3. Doc rule — no README below root

- **`README.md` lives only at the repo root** (GitHub entry), beside `CLAUDE.md`.
- **Every folder opens with a meaningfully-named lead doc `{folder}.md`** — `architecture/architecture.md`,
  `deployment/deployment.md`, `product/product.md`, `engineering/engineering.md` — **never** a generic
  `README.md`. The lead doc orients: what's here, why, pointers.
- Additional docs sit beside the lead with meaningful names (`development/` → `development.md` + `rules.md`).
- `engineering/planning/` is the one exception: it holds only `backlog.md` and `version-track/v{X.Y}/`, with no lead
  doc at either level ([version-track.md](../../../planning/version-track/version-track.md)).
- Functional package metadata is exempt: NuGet's declared `PackageReadmeFile`, and the npm package
  `README.md` beside `package.json` required by [SDK structure](sdk-structure.md). These files ship in
  the package; they do not replace a folder's lead doc.

---

## 4. Folders, not loose files — grow-ready by default

- **If a concern can grow past one file, it is a folder from day one** — don't start as a loose file and migrate later.
- **Create now the folders the repo will need**; omit only the truly-N/A ones (add when real).
- Proven set (Haven): product → `features/ flows/ marketing/`; engineering → `architecture/ codebase/ development/ deployment/ planning/ research/ scripts/`.

---

## 5. Naming rules — the non-negotiables

1. **Top-level dirs are exactly `product/` and `engineering/`** (lowercase). Plus root `README.md`, `CLAUDE.md`, `.claude/`.
2. **All code lives under `engineering/codebase/`.** Always a `codebase/` wrapper — never services directly under `engineering/`.
3. **The code dirs are exactly `codebase/{slug}.backend-services/` and `codebase/{slug}.frontend-services/`** (dot-prefixed with the repo `{slug}`; + optional `database/`, `pipelines/`). Never bare `backend-services`/`frontend-services`, never `backend`/`frontend`, never `{name}.backend`, never a loose dir outside `codebase/`. **Rationale:** the `{slug}.` prefix keeps the two folders uniquely named so several repos open side-by-side in IDEs never collide on identical `backend-services/` / `frontend-services/` folder names. (`{slug}` = the repo's distinctive lowercase hyphenated name — its last dot-segment, e.g. `secrets-vault`, `wheelhouse`; product-template = `sample`.)
4. **`{slug}.backend-services/` holds the solution + projects directly — solution file is `{Brand}.BackendServices.slnx`.** Exactly `.slnx` (the XML format, **not** legacy `.sln`), with the product brand and `BackendServices` in PascalCase (e.g. `ForeverPin.BackendServices.slnx`, `Wheelhouse.BackendServices.slnx`). Beside it sit `Directory.Packages.props` (Central Package Management) + `Directory.Build.props` (shared MSBuild props) — the MSBuild layer, inherited by every project → [`backend/build/build.md`](../../backend/dotnet/shapes/service/platform/build/build.md). Projects `{Brand}.{Domain}[.{SubDomain}]` PascalCase. Clean-Arch layers + **solution-folder grouping** (`Services/ Platform/ Libraries/ Tools/ Tests/`, the `product → platform` ref rule, `.slnx` encoding) → [backend architecture](../../backend/dotnet/shapes/service/architecture/architecture.md). (Apps only — library/SDK repos use their own package layout.)
5. **`{slug}.frontend-services/` holds a pnpm workspace from the first app** —
   canonical app paths and package ownership → [frontend workspace](../../frontend/shapes/app/architecture/workspace.md).
6. **Per-repo `development/` guidelines defer to shared conventions** (`wow-two-ws/conventions/*.md`) — only repo-specific deltas live in the repo.

---

## 6. Tests

- **Backend:** a `tests/` folder inside `codebase/{slug}.backend-services/`, its projects in the same solution (`{Brand}.{Domain}.Tests`).
- **Frontend:** colocated with the code (`*.test.ts(x)` beside source, or `__tests__/`).

---

## 7. Typed clients / contracts

- A backend's typed client consumed by the **frontend** → lives in `codebase/{slug}.frontend-services/` (generated / maintained there).
- A backend's typed client consumed by **another backend** → a package project inside `codebase/{slug}.backend-services/` (`{Brand}.{Service}.Client` / `.Abstractions`), referenced or published like any package.
- **No** separate top-level `contracts/`.

---

## 8. Deployment

- **One image per deployable service is the unit;** `docker compose` *orchestrates* them — it is not an alternative to per-service images.
- **Single-service** → a `Dockerfile` is enough (+ optional compose for local env/volumes). **Multi-service** → per-service Dockerfiles + one compose.
- **Location:** `engineering/deployment/` holds `Dockerfile` + `docker-compose.yml`; **build context = `engineering/codebase/`** (compose: `context: ../codebase`, `dockerfile: ../deployment/Dockerfile`); `.dockerignore` at the context root (`codebase/`). The `Dockerfile` `COPY`s the context's `{slug}.backend-services/` + `{slug}.frontend-services/` (prefixed paths).

---

## 9. Single-service vs multi-service

| | `codebase/{slug}.backend-services/` | `codebase/{slug}.frontend-services/` |
|---|---|---|
| **Single** | solution + Clean-Arch projects directly | workspace with `apps/web/` |
| **Multi** | one folder per service under a shared solution | same workspace; additional `apps/*` and shared `packages/*` |

---

## 10. Migration ripple (do in lockstep with any rename)

The two code dirs carry the repo `{slug}.` prefix (`{slug}.backend-services/`, `{slug}.frontend-services/`) — any rename touches every path that names them:

- **`wow-two-ws/scripts/active.sh`** — the `PROJECTS` registry (backend `.sln` + frontend dir paths → both prefixed).
- Each repo's **deploy script**, **`Dockerfile`**, **`.dockerignore`**, and **compose** context.
  Resolve SPA inputs from `apps/{app}/dist` and the host destination from the deployment script's own location.
- **`.sln`/`.slnx`:** moving/renaming the backend folder as a unit preserves its relative project refs; a depth change (introducing `codebase/`) re-paths only *external* references, not the solution internals.

---

## 11. Audit — product repos vs this standard (2026-06-10)

`✓` conforms · `✗` deviates. Targets are now `product/` + `engineering/` + `engineering/codebase/` + folder-docs.

| Repo | top-level | `codebase/` | folder-docs | CLAUDE | Fixes needed |
|---|:--:|:--:|:--:|:--:|---|
| secrets-vault | 🚧 | 🚧 | 🚧 | ✓ | rename pilot: `business-logic`→`product`, `platform-development`→`engineering`, `src`→`codebase`, READMEs→`{folder}.md`, `analysis`→`research` |
| forever-pin | ✗ | ✗ | ✗ | ✓ | full conform (next) |
| haven | ✗ (`business/`+`platform/`) | ✗ (`src/`) | ✗ | ✓ | top-level rename; `src`→`codebase`; folder-docs |
| wheelhouse | ✗ | ✗ | ✗ | ✓ | top-level; `*.backend`→`codebase/{slug}.backend-services`; folder-docs |
| trademark · transcript-forge · acquisition · pdf-editor | ✗ | ✗ | ✗ | ✗ | scaffold to standard |

> The 2026-06-09 audit is **superseded** — the top-level names changed (`business-logic/`+`platform-development/` → `product/`+`engineering/`) and `src/`→`codebase/`, plus the no-README rule.

---

## 12. Ecosystem naming

- **Orgs:** lowercase, hyphenated — `wow-two-sdk`.
- **Repos:** `{org}.{domain}[.{subdomain}]`, lowercase, dot-separated — `sdk.language.core`, `platform.storage.cache`.
- **NuGet:** PascalCase branded — `WoW.Two.Sdk.Language.Core`.
- **Branches:** `main` · `feature/*` · `fix/*` · `docs/*`. **Commits:** conventional (`feat:`/`fix:`/`docs:`/`refactor:`).

---

## 13. Image publishing (the deploy artifact)

A product repo publishes **one image per service** and a **release bundle** that pins them, through a fixed-name CI workflow, so the control plane (Wheelhouse) can both **detect** that the repo is publishable and **resolve** what to ship. What each service is, how it builds and which paths change it lives in the [deployment descriptor](../../../deployment/descriptor/deploy-descriptor.md) (`engineering/deployment/deploy.yml`).

- **Marker file:** `.github/workflows/publish-docker-image.yml` — its presence = the repo publishes deployables (Wheelhouse keys on this exact path).
- **Images:** each service pushes to **`ghcr.io/{owner}/{repo}/{service}`** (lowercased); a descriptor `image` keeps a legacy repository name.
- **Releases:** every `main` build that changes a service or the descriptor is a release `vX.Y.Z` (`Z` assigned by CI); it rebuilds only the changed services, tags them `X.Y.Z` and `latest`, and keeps its bundle for good; unchanged services keep their image and version.
- **Branch builds:** `dev` and `test` builds replace the previous one under `dev-latest` / `test-latest`; any other branch builds candidates tagged `sha-{commit}`, kept 14 days; Wheelhouse can start the build of a commit that has none.
- **Resolution contract:** Wheelhouse deploys a bundle's digest-pinned images, never a moving tag (reproducible deploy + rollback); dev takes any build, test takes releases and `test` builds, prod takes releases only.
- **Tag value:** apps use the **product version** (`X.Y.Z`, [versioning](../versioning/versioning.md)); a service shows the release in which it last changed. Libraries use the .NET-major scheme (`docs/versioning-strategy.md`). Full table: [deploy descriptor](../../../deployment/descriptor/deploy-descriptor.md) § *Builds and versions*.
