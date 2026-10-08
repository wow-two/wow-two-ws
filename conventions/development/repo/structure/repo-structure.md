# Repo structure

*Last updated: 2026-10-01*

> On-disk layout and naming of a product / venture repo under `wow-two-ws/workbench/` — folders and names, not code.
> Use case — scaffolding a repo, placing a folder, or checking an existing repo's shape.

## Archetypes

| Archetype | Shape | Governed by |
|---|---|---|
| product / venture | `product/` + `engineering/`, code under `engineering/codebase/` | this doc |
| SDK / library | `engineering/` only, one package under `engineering/codebase/{slug}/` | [SDK structure](sdk-structure.md) |

- must scaffold a product repo with the `create-repo` skill, from `wow-two-sdk-beta.product-template`.
- must not force one archetype's shape onto the other.

---

## Layout

Framework selection → [frontend standard](../repo-conventions.md#frontend-standard).

```
{repo}/
├── README.md                     human entry — root only
├── CLAUDE.md                     agent entry — lazy-load rules, stack, structure
├── .claude/rules/
│   └── file-references.md        doc lookup table; never lists `engineering/codebase/` files
├── .github/workflows/
│   ├── ci.yml                    build and test on every push
│   └── publish-docker-image.yml  the image-publish marker
│
├── product/                      the definition — what, why, features, flows; no code
│   ├── product.md                what it is, who for, positioning, model (lead doc)
│   ├── context.md                current state and binding decisions
│   ├── features/                 one spec per feature, listed in the backlog's Features group
│   ├── flows/                    user and product flows (flows.md)
│   └── marketing/                go-to-market, channels, campaigns (marketing.md)
│
└── engineering/                  the execution — design, plan, build, ship, run
    ├── engineering.md            technical overview, stack, map (lead doc)
    ├── architecture/             system and per-area design (architecture.md)
    │   ├── flows/                one `{flow}-flow.md` per flow
    │   ├── infra/                cross-cutting subsystem design
    │   └── {domain}/             per-domain design docs
    ├── research/                 analyses before a decision (research.md)
    ├── planning/                 backlog.md + version-track/v{X.Y}/ — no lead doc
    ├── codebase/                 the only place code lives (codebase.md)
    │   ├── {slug}.backend-services/    .NET solution, projects and tests/
    │   ├── {slug}.frontend-services/   pnpm workspace: apps/web/ + optional packages/
    │   ├── database/             SQL managed apart from a service (optional)
    │   └── pipelines/            data pipelines (optional)
    ├── development/              development.md · rules.md · backend-guidelines.md ·
    │                             frontend-guidelines.md · iteration-guide.md
    ├── deployment/               deployment.md · deploy.yml · Dockerfile · docker-compose.yml
    ├── scripts/                  development and operations scripts (scripts.md)
    └── operations/               runbooks, verification records, secrets/ (gitignored) (operations.md)
```

- must create `operations/` only once a runbook, a verification record or a secret exists.
- must plan under `engineering/planning/` per the
  [version track](../../../planning/version-track/version-track.md).
- must describe deployables in `deploy.yml` per the
  [deploy descriptor](../../../deployment/descriptor/deploy-descriptor.md).
- must keep the per-app design spec where
  [design conventions](../../../design/design-conventions.md#per-app-specs) place it.

---

## Slug

- must derive `{slug}` from the repo name's last dot-segment, lowercase and hyphenated — `secrets-vault`.
- must prefix both code directories with `{slug}.`, so several open repos never share a folder name in an IDE.
- must keep the hyphens — `secrets-vault`, never the lowercased brand `secretsvault`.

---

## Documents

- must keep `README.md` at the repo root only, beside `CLAUDE.md`.
- must open every folder with a lead doc named `{folder}.md` — `architecture/architecture.md`, never `README.md`.
- must name further docs for their subject beside the lead — `development/rules.md`.
- must leave `engineering/planning/` without a lead doc; it holds `backlog.md` and `version-track/` only.
- may keep a package `README.md` beside `package.json`, and a declared NuGet `PackageReadmeFile` — both ship.

---

## Folders

- must make a concern a folder from the first file when it can grow past one.
- must omit a folder that has nothing to hold; add it when real.
- must keep code out of `product/` and out of every `engineering/` folder except `codebase/`.

---

## Naming

- must name the two top-level folders exactly `product/` and `engineering/`.
- must wrap all code in `engineering/codebase/` — never a service directly under `engineering/`.
- must name the code directories exactly `{slug}.backend-services/` and `{slug}.frontend-services/`.
- must not use `backend/`, `frontend/`, `src/`, `{name}.backend` or a bare `backend-services/`.
- must name the backend solution `{Brand}.BackendServices.slnx` — `.slnx`, never the classic `.sln`.
- must keep `Directory.Build.props` and `Directory.Packages.props` beside the solution
  ([build](../../backend/dotnet/shapes/service/platform/build/build.md)).
- must name backend projects in PascalCase under the brand; the layer names are
  [Clean Architecture](../../backend/dotnet/shapes/service/architecture/clean/clean.md#layers)'s.
- must group them in solution folders per
  [solution organization](../../backend/dotnet/shapes/service/architecture/architecture.md#solution-organization).
- must keep the frontend a pnpm workspace from the first app
  ([frontend workspace](../../frontend/shapes/app/architecture/workspace.md)).
- must keep only repo-specific deltas in `engineering/development/`; shared rules stay in these conventions.

---

## Tests

- must place backend test projects in `{slug}.backend-services/tests/`, inside the same solution.
- must name them by tier —
  [service testing](../../backend/dotnet/shapes/service/architecture/clean/testing.md#layout).
- must place frontend tests with their app —
  [frontend workspace](../../frontend/shapes/app/architecture/workspace.md#layout).

---

## Typed clients

- must keep a backend's client for its own frontend inside `{slug}.frontend-services/`.
- must ship a client for another backend as a project in `{slug}.backend-services/` — `{Brand}.{Service}.Client`.
- must not add a top-level `contracts/` folder.

---

## Deployment files

- must build one image per deployable service; `docker compose` orchestrates them and replaces none.
- must keep `deploy.yml`, every `Dockerfile` and the local `docker-compose.yml` in `engineering/deployment/`.
- must set the build context to `engineering/codebase/`, with `.dockerignore` at that context root.
- must copy both code directories in the `Dockerfile` by their `{slug}.`-prefixed names.

---

## Service count

| | `{slug}.backend-services/` | `{slug}.frontend-services/` |
|---|---|---|
| single service | the solution and its Clean projects | a workspace with `apps/web/` |
| multi service | one folder per service under one solution | the same workspace, more `apps/*` and `packages/*` |

---

## Renames

- must update every path that names a code directory in the same change as the rename.
- must update the `PROJECTS` registry in `wow-two-ws/scripts/active.sh` — the solution path and the frontend folder.
- must update the repo's `deploy.yml` paths, `Dockerfile`, `.dockerignore`, compose context and deploy script.
- must resolve the SPA artifact from `apps/{app}/dist` and the host destination from the script's own location.
- must move the backend folder as one unit, so project references inside the solution stay valid.

---

## Ecosystem naming

- must name an org lowercase and hyphenated — `wow-two-sdk`.
- must name a repo `{org}.{domain}[.{subdomain}]`, lowercase and dot-separated — `wow-two-platform.wheelhouse`.
- must name a NuGet package PascalCase and branded — `WoW2.Sdk.Backend.Beta`.

---

## Image publishing

- must keep `.github/workflows/publish-docker-image.yml` at exactly that path; Wheelhouse detects a publishable
  repo by it.
- must take images, tags, branch builds and retention from the
  [deploy descriptor](../../../deployment/descriptor/deploy-descriptor.md#builds-and-versions).
