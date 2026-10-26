---
name: create-repo
description: >-
  Scaffold a NEW conformant product / venture repo for the wow-two workspace — copies the standard
  product-template's example product (a complete Clean-Arch .NET 10 backend + Vue 3 / Vite frontend workspace
  under engineering/codebase/, single-host serving, Docker) and rebrands it to the new name, then git
  init + registration in scripts/active.sh. Use this whenever the user wants to create / start / spin up
  / bootstrap / set up a new repo, project, product, venture, app, service, or POC in this workspace
  (e.g. "create a new repo for X", "scaffold a new venture", "start a new product repo", "spin up a new
  backend+frontend repo", "bootstrap a conformant repo named foo", "new wow-two-platform repo"). Trigger
  even when the user does NOT name the template, the IDE, or "conformant" — phrases like "make me a new
  repo for a QR tool" should use this skill. Covers single-service (default) and multi-service shapes, and
  SHAPE=domain — a new domain repo / library plus service repo / per-domain SDK repo (e.g. "scaffold the identity
  domain repo", "new wow-two-sdk-beta domain library with its service"): the domain template's NuGet family, npm
  package, service and image with tag-derived releases.
---

# create-repo

Scaffolds a **product / venture** repo that conforms to
`conventions/development/repo/structure/repo-structure.md` (top-level `product/` + `engineering/`;
**all code under `engineering/codebase/`**; the two code dirs are **exactly**
`codebase/{slug}.backend-services/` + `codebase/{slug}.frontend-services/` — dot-prefixed with the
repo `{slug}` = its last dot-segment, e.g. `secrets-vault`, so several open repos never collide on a
bare folder name in an IDE).

The product-template is the source of the `Sample` example — 5 Clean-Arch projects
(`Sample.{Api,Application,Domain,Infrastructure,Persistence}`), `Sample.BackendServices.slnx`,
`tests/Sample.Tests.{Unit,E2E,Migrations}`, a Vue frontend workspace, a descriptor 2 `deploy.yml`, and the
CI and publish workflows, wired to the be sdk `WoW2.Sdk.Beta.Be` and the fe sdk `@wow-two-beta/fe`.
**`scaffold.sh` copies that example and rebrands it** (`Sample` → `{Brand}`, file/dir renames, port
re-allocation) — there is **no code generation**. Claude's job afterward is to **verify the copy
builds and fill the doc `{{placeholders}}`**.

Framework selection follows `conventions/development/repo/repo-conventions.md#frontend-standard`.
Project layout follows `conventions/development/frontend/shapes/app/architecture/workspace.md`.
`validate-frontend.mjs` rejects an outdated React/root-app template before `scaffold.sh` creates anything.
If validation fails, report the template gap; do not report the copied legacy starter as conformant.

> **Doc rule:** no `README.md` below the repo root — every folder leads with a meaningfully-named
> `{folder}.md` doc (`engineering/engineering.md`, `architecture/architecture.md`,
> `deployment/deployment.md`, …). Root keeps the single `README.md` + `CLAUDE.md`.

> **Shapes.** `product` (default) stamps the product template. `SHAPE=domain` stamps
> `workbench/wow-two-sdk-beta/wow-two-sdk-beta.domain-template/`: one SDK domain's be packages, fe package, service
> and image in one repo, per `conventions/development/repo/structure/domain-structure.md`. Package-only repos (the be
> sdk, the fe sdk) stay out of this skill. A domain repo meant for GitHub, the registries and Wheelhouse goes through
> the `create-library` skill, which drives this scaffold with `INTO=clone`.

## 1 · Gather inputs

| Input | Meaning | Example / default |
|---|---|---|
| **repo name** | on-disk + git repo name | `wow-two-platform.foo` |
| **brand** | PascalCase .NET project/namespace prefix | `Foo` |
| **org** | `workbench/{org}/` subfolder | `wow-two` · `wow-two-platform` · `maxs-projects/ventures/{saas\|consumer\|labs}` |
| **mode** | `single` (default) vs `multi` service | `single` |
| **net** | .NET major (TargetFramework `net{N}.0`) | `10` |

Ask only for what's missing; infer brand from the last repo-name segment when obvious
(`wow-two-platform.foo` → `Foo`). Confirm the resolved `{repo, Brand, org, mode, shape}` before scaffolding.

A domain repo (`SHAPE=domain`) takes these instead:

| Input | `domain` meaning | Default |
|---|---|---|
| `SHAPE` (env) | `domain` | `product` |
| repo name | `wow-two-sdk-beta.{slug}` | — |
| Brand | PascalCase domain: namespaces `WoW.Two.Sdk.Beta.Be.{Brand}`, NuGet ids `WoW2.Sdk.Beta.Be.{Brand}.{Layer}` | last segment |
| org | `workbench/{org}` and the GitHub owner in package URLs | `wow-two-sdk-beta` |
| mode | ignored | — |
| `SLUG` (env) | code-dir prefix and `fe-{slug}`; pass it for dotted names | last dot-segment |
| `PRODUCT` (env) | product, service and catalog slug; must equal the Wheelhouse product | lowercased Brand |
| `CORE_VERSION`, `FE_VERSION` (env) | be sdk pin (`BackendSdkVersion`) and fe sdk pin (+ the fe package's peer floor) | the template's |
| `SCRATCH=1` (env) | scaffold into a temp dir (`SCRATCH_DIR`); no `active.sh`, no ports row, no `git init` | off |
| `INTO=clone` (env) | fill the empty clone at the target (`gh repo clone`, no commit, nothing beside `.git`); keeps its `.git` and `origin`, skips `git init` | off |

## 2 · Run the mechanical scaffold

```bash
scripts_dir=".claude/skills/create-repo"
"$scripts_dir/scaffold.sh" <repo-name> <Brand> <org> [single|multi]
SHAPE=domain "$scripts_dir/scaffold.sh" wow-two-sdk-beta.<slug> <Brand>          # a domain repo
SHAPE=domain SCRATCH=1 "$scripts_dir/scaffold.sh" wow-two-sdk-beta.<slug> <Brand>   # a template check, nothing kept
```

This (deterministic, no code-gen, no commit):
0. validates the template's private pnpm workspace and Vue `apps/web` app,
1. creates `workbench/{org}/{repo-name}/`,
2. copies the product-repo template — **including the working `Sample` example** —
   (`workbench/wow-two-sdk-beta/wow-two-sdk-beta.product-template/`) in, dropping its `.git` + build artifacts,
3. replaces `{{REPO_NAME}}` `{{Brand}}` `{{repo-slug}}` `{{NET_VERSION}}` `{{YYYY-MM-DD}}` across the docs,
4. **brand pass** — replaces `Sample` → `{Brand}` (and lowercase `sample` → `{brand}`) across all
   code/config (`.cs`, `.csproj` incl. `ProjectReference`, `.slnx`, `package.json`, `vite.config.ts`,
   `scripts/deploy.mjs`, `Dockerfile`/`docker-compose.yml`, `deploy.yml`, `.github/` workflows,
   `appsettings*.json`, `launchSettings.json`, `.gitignore`), and uppercase `SAMPLE` → `{BRAND}` (the dev
   check's `VERIFY_SERVICE_*` variable), then renames every `Sample*` **file/dir** → `{Brand}*`
   (`Sample.BackendServices.slnx`→`{Brand}.BackendServices.slnx`, the 5 project dirs, `tests/Sample.Tests.*`,
   `SampleDbContext.cs`, …),
5. **port pass** — the template binds `8220` https / `8221` http / `8224` vite; re-allocates to the
   next-free even/odd backend pair + free even vite port (seeded from `conventions/deployment/hosting/ports.md`
   "Next free", scanning existing `launchSettings.json`/`vite.config.ts` to avoid collisions), rewrites
   them across launchSettings/vite proxy/`.http`/appsettings/`docker-compose.yml` (the local port is the HTTP
   one)/the two docs that name them, and appends a `ports.md` row + bumps "Next free",
6. **slug-prefix pass** — the template ships its code dirs as `sample.backend-services/` +
   `sample.frontend-services/`; retargets the prefix to the repo `{slug}` (the **hyphenated** last
   dot-segment, e.g. `secrets-vault` — NOT the lowercased brand `secretsvault`) on disk AND in every
   content path-ref (`deploy.mjs`, `Dockerfile`, `.dockerignore`, `codebase.md`, doc tables),
7. keeps the template's root `.gitignore` (rebranded), clears what a local run left in the copy (built `wwwroot/`,
   SQLite files, local settings files), runs `git init` **only**,
8. appends the repo to the `PROJECTS` array in `scripts/active.sh`
   (`name|backend-sln|frontend-dir` — backend = `{slug}.backend-services/{Brand}.BackendServices.slnx`,
   frontend = `{slug}.frontend-services` — paths relative to `workbench/`).

`SHAPE=domain` changes these passes:

- template `wow-two-sdk-beta.domain-template`; its example ports are `8384` / `8385` / `8386`, which the port pass moves;
- before the generic brand pass: the template's repo name in the package URLs → `{owner}/{repo}`, `fe-sample` →
  `fe-{slug}` (content and the package dir), the module's `sample_` table prefix → `{product}_` in snake case;
- `CORE_VERSION` / `FE_VERSION` rewrite the pins; a changed fe pin refreshes `pnpm-lock.yaml` (`--lockfile-only`);
- printed, not applied: the `catalog.yml` entry and the `~git_on commit,push workbench/{org}/{repo}` line the developer
  sends once the remote exists.

Free-text placeholders (`{{ONE_LINE_WHAT_THIS_IS}}`, guideline bodies, the per-project rows in
`.claude/rules/file-references.md`) stay — fill them with the user's one-liner. **The `codebase/` code
is already in place and rebranded** — no authoring needed; just verify it builds.

**Resulting layout** (per `conventions/development/repo/structure/repo-structure.md` — each folder leads with its
`{folder}.md`, no README below root):

```
{repo}/
├── README.md · CLAUDE.md · .claude/rules/file-references.md
├── .github/                  renovate.json · workflows/{ci,publish-docker-image}.yml   (callers of the shared pipelines)
├── product/                  product.md · product.json · context.md
│   ├── features/  (one spec per feature, listed in the backlog)
│   ├── flows/     flows.md              └── marketing/  marketing.md
└── engineering/              engineering.md
    ├── architecture/   architecture.md
    ├── codebase/       codebase.md · {slug}.backend-services/ · {slug}.frontend-services/   ← ALL code here
    ├── development/    development.md · rules.md · backend-guidelines.md · frontend-guidelines.md · iteration-guide.md
    ├── deployment/     deployment.md · deploy.yml · Dockerfile · docker-compose.yml   (context = ../codebase)
    ├── planning/       backlog.md · version-track/v0.1/v0.1.md   (no lead doc; CI reads X.Y from the newest folder)
    ├── research/       research.md
    └── scripts/        scripts.md
```

Planning follows `conventions/planning/version-track/version-track.md`: one backlog plus one folder per version.

**Domain layout** (`SHAPE=domain`, per `domain-structure.md` § Layout):

```
{repo}/
├── README.md (artifacts table) · CLAUDE.md · LICENSE · .claude/rules/file-references.md
├── .github/                  renovate.json · workflows/{publish-docker-image,publish-packages,core-latest,conformance,codeql}.yml
├── product/                  product.md (the capability spec) · product.json · context.md · features/ · flows/ · brand/
└── engineering/
    ├── architecture/   architecture.md · contract.md · package-registry.md · decisions/ · flows/
    ├── codebase/       {slug}.backend-services/ (packages/ · service/ · tests/) · {slug}.frontend-services/ (packages/fe-{slug} · apps/web)
    ├── deployment/     deployment.md · deploy.yml · Dockerfile · docker-compose.yml
    ├── scripts/        next-version.sh · test-next-version.sh · verify-release-packages.sh · verify-published-packages.sh · pack-smoke.sh
    └── development/ · planning/ · research/   as in the product shape
```

The template already ships this conformant shape. If a copy ever hands back a stale name
(`business-logic/`, `platform-development/`, `src/`, `guidelines/`, a folder `README.md`) rename it to
the above — the target shape is non-negotiable — but normally there's nothing to fix.

## 3 · The backend is already in place — `engineering/codebase/{slug}.backend-services/`

`scaffold.sh` copied the template's working example and rebranded it. **Don't author code** — the 5
Clean-Arch projects already exist as `{Brand}.*` and build against the be sdk. Defer all code style to
`conventions/development/backend/`.

What's there (rebranded from `Sample` → `{Brand}`):

- **Solution** `{Brand}.BackendServices.slnx` (with `global.json`, `tests.runsettings`, `Directory.Build.props` and
  `Directory.Packages.props`) referencing the 5 projects + the three test tiers under `tests/`.
- **Projects** (`net{N}.0`, `Nullable`+`ImplicitUsings` via `Directory.Build.props`; central package
  versions via `Directory.Packages.props`, the be sdk pinned once as `BackendSdkVersion`), Clean-Arch layering per
  `conventions/development/backend/dotnet/shapes/service/architecture/clean/clean.md`. They use the be sdk
  `WoW2.Sdk.Beta.Be` (namespaces `WoW.Two.Sdk.Beta.Be.*`): `IQuery`/`IQueryHandler`, `AppResult`, `ApiResponse`,
  `AddApiDefaults`, the bespoke SQL migrator. No hand-rolled `Results/`, `Common/IEntity`, or local mediator.
  - `{Brand}.Domain` — `Greetings/Entities/GreetingLog : IKeyedEntity<Guid>` (be sdk trait).
  - `{Brand}.Application` — `ApplicationAssembly` marker; one CQRS vertical `Greetings/` (query, model, FluentValidation
    validator); time comes from `TimeProvider`.
  - `{Brand}.Infrastructure` — `InfrastructureAssembly` marker; the query handler under `Greetings/QueryHandlers/`.
  - `{Brand}.Persistence` — `{Brand}DbContext` (EF Core **SQLite**, a pure mapper), the entity configuration, and the
    schema as `Migrations/NNN-name/{Apply,Rollback}.sql` run by the bespoke migrator on boot (**no EF migrations**,
    no `dotnet-ef`).
  - `{Brand}.Api` — `Program.cs` in three groups (+ `public partial class Program`) → `Configurations/HostConfiguration.cs`
    + `HostConfiguration.Extensions.cs` (`AddApiDefaults` / `UseApiDefaults`, `AddSqliteDatabase`, `AddMediator`,
    `AddControllers`; no layer project registers itself); `Greetings/Controllers/GreetingController` and
    `Status/Controllers/SystemController` (`api/system/status`); `appsettings.json` (+`.Development`, defaults only);
    one `https` launch profile (`LOCAL_SETTINGS=true`); `wwwroot/` empty but for `.gitkeep`, filled by `BuildSpa`.
- **Tests** — `{Brand}.Tests.Unit` (handler + validator), `{Brand}.Tests.E2E` (the real host in-process over a
  throwaway SQLite file: greeting, `/health`, `api/system/status`, SPA serving, host filtering replayed from
  `deploy.yml`'s dev check), `{Brand}.Tests.Migrations` (the embedded SQL, apply / rollback). None needs Docker.
- **Settings** — load order `appsettings.json` → `appsettings.{Environment}.json` → `appsettings.Target.json` (a
  deployed target's) → `appsettings.Local.json` (this machine's, only with `LOCAL_SETTINGS=true` on a local run).
  `appsettings.Development.json` holds defaults only; Local and Target are git- and docker-ignored.
- **Ports** — already re-allocated by `scaffold.sh` (template's `8220`/`8221` https/http + `8224` vite →
  the next-free pair; see §2's port pass). Nothing to set by hand.

**Domain backend** (`SHAPE=domain`): `{Brand}.BackendServices.slnx` groups `Packages/` · `Services/` · `Tests/`.

- `packages/Abstractions` — the contract: `IGreetingsBroker`, model, constants, error catalogue; no DI, options or I/O.
- `packages/Module` — Form 1: `AddSample()` (→ `Add{Brand}()`), the broker over its own store, embedded migrations.
- `packages/Client` — Forms 2/3: `AddSampleClient(…)`, the broker over the service's HTTP API.
- `packages/Testing` — `FakeGreetingsBroker` and `GreetingsBrokerConformance`, the suite every implementation passes.
- `service/{Brand}.Api` — hosts Module by `ProjectReference`; adds hosting, the HTTP mirror and the hosted pages.
- `tests/{Brand}.Tests.{Unit,Integration,E2E,Conformance,Migrations}` — Conformance runs the one suite against the
  module, the client (against the host in process, or a running image with `CONFORMANCE_BASE_URL`) and the fake.
- Packable by path (`Directory.Build.props`); versions only from `-p:Version` (tags), else `APP_VERSION`, else `0.0.0-dev`.

> **Wheelhouse Canary is the nearest reference** (`workbench/wow-two-platform/wow-two-platform.wheelhouse-canary/`):
> the same shape on PostgreSQL. Wheelhouse itself is the richer, older one; neither is copied.

## 4 · Frontend workspace — `engineering/codebase/{slug}.frontend-services/`

- Workspace root: private `package.json`, pinned pnpm `packageManager`, `pnpm-workspace.yaml`, `pnpm-lock.yaml`.
- Initial app: `apps/web/`, named `@{brand-lc}/web`, with its manifest, `index.html`, Vite/TS config and Vue source.
- Root `dev`, `build` and `typecheck` scripts delegate to the app; run installation from the workspace root.
- `scripts/deploy.mjs` copies `apps/web/dist` to `{slug}.backend-services/{Brand}.Api/wwwroot`.
- `single` and `multi` use the same frontend workspace; add app siblings without moving `apps/web`.
- Shared packages follow the convention's extraction rule; empty placeholder packages are unnecessary.
- Verify `/api` proxy and ports against the deployment conventions after the mechanical port pass.
- Domain: `packages/fe-{slug}` is `@wow-two-beta/fe-{slug}` (`./contracts`, `./kit`: an embeddable widget through the
  contract, and a forward to the service's hosted page); `apps/web` routes the hosted pages and console with the fe
  sdk router and takes the package by `workspace:*`. Root `dev`, `typecheck` and `test` build the package first.

## 5 · Single-host serving, Docker and delivery (already wired)

The example already serves the SPA from the API host, ships Docker and delivers through the shared pipelines:

- `AddApiDefaults` sets `SpaHosting`, and `UseApiDefaults()` serves `wwwroot/`, the SPA fallback and `/health`
  (database readiness) — no hand-wired static files. The `BuildSpa` MSBuild target of `{Brand}.Api` installs and builds
  the frontend into `wwwroot/` on every backend build (`-p:BuildSpa=false` skips it).
- `engineering/deployment/` holds `deploy.yml` (descriptor 2: one service, one `app` site at `/` and `/api`, the
  `data` volume, `settings.required`, `dotnetEnvironment: true`, a `verify` dev check sending `Host: localhost`),
  `Dockerfile` (3-stage: node build SPA → dotnet publish with the SPA in `wwwroot` → aspnet runtime with `curl`;
  `APP_VERSION` build argument; no environment value in the image) and `docker-compose.yml` (local only, SQLite on a
  named volume). Build context `= engineering/codebase/`; `.dockerignore` at the context root. The brand pass already
  rewrote the `{Brand}.Api` / `{Brand}.Api.dll` / product / service / image names.
- `.github/workflows/ci.yml` (backend and frontend checks) and `publish-docker-image.yml` (the marker Wheelhouse
  detects) publish through the shared `publish.yml` of `wow-two-platform.pipelines`, pinned to `v0.8.1`; pipelines
  `v0.9.0` replaces both with one call of the shared `delivery.yml` — move the pin and the workflows together once
  the tag exists. `.github/renovate.json` extends the private Renovate preset (a public repo switches to
  `renovate-product` and adds `codeql.yml`). Nothing to wire.

A domain repo delivers through five workflows: `publish-docker-image.yml` (the image, shared `delivery.yml`),
`publish-packages.yml` (NuGet and npm from `be-v*` / `fe-v*` tags, OIDC, disarmed until the repository variable
`PUBLISH_PACKAGES` is `true`), `core-latest.yml` (nightly against the newest be sdk and fe sdk), `conformance.yml`
(the suite against the released image) and `codeql.yml`. No release commit, no GitHub Release for a package tag.

## 6 · Git & registration (already done by scaffold.sh — verify)

`scaffold.sh` ran `git init` (no commit) and added the `active.sh` entry (backend =
`{Brand}.BackendServices.slnx`). **Do not commit** — the developer manages git. Confirm: `scripts/active.sh -l` lists
the new short name.

A domain repo also gets, from the printed lines: the `catalog.yml` entry (fill purpose and status), then
`python3 scripts/gen-repo-registry.py`; and the developer's `~git_on commit,push workbench/{org}/{repo}` once the remote
exists. A `SCRATCH=1` run registers nothing.

## 7 · Verify, then report

The code is already present — just confirm it builds and passes, then fill placeholders. The schema comes from the
embedded SQL migrations (**no `dotnet ef migrations` step**). The backend build runs the frontend build, so Node and
pnpm must be on the `PATH`; no test tier needs Docker.

```bash
be="workbench/{org}/{repo-name}/engineering/codebase/{slug}.backend-services"
dotnet test "$be/{Brand}.BackendServices.slnx"

fe="workbench/{org}/{repo-name}/engineering/codebase/{slug}.frontend-services"
( cd "$fe" && pnpm install --frozen-lockfile && pnpm lint && pnpm test && pnpm build )
```

A domain repo:

```bash
be="workbench/wow-two-sdk-beta/{repo}/engineering/codebase/{slug}.backend-services"
dotnet test "$be/{Brand}.BackendServices.slnx"

fe="workbench/wow-two-sdk-beta/{repo}/engineering/codebase/{slug}.frontend-services"
( cd "$fe" && pnpm install --frozen-lockfile && pnpm lint && pnpm test && pnpm build && pnpm check:package )

bash workbench/wow-two-sdk-beta/{repo}/engineering/scripts/test-next-version.sh
```

Then fill the doc `{{placeholders}}` (`{{ONE_LINE_WHAT_THIS_IS}}`, guideline bodies, the per-project
rows in `.claude/rules/file-references.md`) with the user's one-liner.

Report: repo path, resolved `{Brand, org, mode}`, the **ports** chosen, backend test result,
frontend test and build result, the `active.sh` short name, and anything left as a `{{placeholder}}` for the
user to fill. If a build fails, fix against `conventions/development/backend/` and re-run before
reporting success.

Confirm the generated app remains in `apps/web`, workspace commands select it, and the host includes its built output.
The structural validator does not establish a successful frontend build or correct host serving.

## Notes

- **Conformance is the point:** never `src/`, never `business-logic/` or `platform-development/`, never a
  loose `{name}.backend` dir, never a **bare** `backend-services`/`frontend-services` — only `product/` +
  `engineering/` with all code under `engineering/codebase/{slug}.{backend-services,frontend-services}`
  (slug-prefixed). The template already ships this shape.
- **Be sdk, not pre-kit:** the example uses `WoW2.Sdk.Beta.Be` (mediator, `AppResult`, `IKeyedEntity`,
  `AddApiDefaults`). Do **not** reintroduce local `Results/` + `ResultError`, `Common/IEntity`,
  `ApiResults.ToStatusCode`, an `Add*` registration extension inside a layer project, or a hand-written `/health` — those
  are pre-kit. Code style: `conventions/development/backend/`.
- **No README below root.** Every folder leads with `{folder}.md`; if a copy still ships a stray
  `README.md` inside a folder, rename it to the folder-doc name.
- `scaffold.sh` refuses to clobber an existing repo dir and won't double-register in `active.sh`.
- Toolchain check (once): `dotnet --version` (≥ `net{N}`) and `node --version` (≥ 20) before verifying.
