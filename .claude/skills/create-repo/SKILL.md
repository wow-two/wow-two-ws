---
name: create-repo
description: >-
  Scaffold a NEW conformant product / venture repo for the wow-two workspace — copies the standard
  product-template's example product (a complete Clean-Arch .NET 10 backend + React 19 / Vite frontend
  under engineering/codebase/, single-host serving, Docker) and rebrands it to the new name, then git
  init + registration in scripts/active.sh. Use this whenever the user wants to create / start / spin up
  / bootstrap / set up a new repo, project, product, venture, app, service, or POC in this workspace
  (e.g. "create a new repo for X", "scaffold a new venture", "start a new product repo", "spin up a new
  backend+frontend repo", "bootstrap a conformant repo named foo", "new wow-two-platform repo"). Trigger
  even when the user does NOT name the template, the IDE, or "conformant" — phrases like "make me a new
  repo for a QR tool" should use this skill. Covers single-service (default) and multi-service shapes.
---

# create-repo

Scaffolds a **product / venture** repo that conforms to
`conventions/development/repo/repo-structure.md` (top-level `product/` + `engineering/`;
**all code under `engineering/codebase/`**; the two code dirs are **exactly**
`codebase/{slug}.backend-services/` + `codebase/{slug}.frontend-services/` — dot-prefixed with the
repo `{slug}` = its last dot-segment, e.g. `secrets-vault`, so several open repos never collide on a
bare folder name in an IDE).

The product-template now **ships a complete, working `Sample` example** — 5 Clean-Arch projects
(`Sample.{Api,Application,Domain,Infrastructure,Persistence}`), a classic `Sample.sln`,
`tests/Sample.Tests`, and a Vite/React frontend, all wired to the kit `WoW2.Sdk.Backend.Beta`. So
**`scaffold.sh` copies that example and rebrands it** (`Sample` → `{Brand}`, file/dir renames, port
re-allocation) — there is **no code generation**. Claude's job afterward is to **verify the copy
builds and fill the doc `{{placeholders}}`**, not to author code.

> **Doc rule:** no `README.md` below the repo root — every folder leads with a meaningfully-named
> `{folder}.md` doc (`engineering/engineering.md`, `architecture/architecture.md`,
> `deployment/deployment.md`, …). Root keeps the single `README.md` + `CLAUDE.md`.

> **Not for SDK / library repos.** Those are package-shaped — use the SDK docs +
> `.claude/rules/templates/CLAUDE-sdk.md`, not this skill.

## 1 · Gather inputs

| Input | Meaning | Example / default |
|---|---|---|
| **repo name** | on-disk + git repo name | `wow-two-platform.foo` |
| **brand** | PascalCase .NET project/namespace prefix | `Foo` |
| **org** | `workbench/{org}/` subfolder | `wow-two` · `wow-two-platform` · `ventures` |
| **mode** | `single` (default) vs `multi` service | `single` |
| **net** | .NET major (TargetFramework `net{N}.0`) | `10` |

Ask only for what's missing; infer brand from the last repo-name segment when obvious
(`wow-two-platform.foo` → `Foo`). Confirm the resolved `{repo, Brand, org, mode}` before scaffolding.

## 2 · Run the mechanical scaffold

```bash
scripts_dir=".claude/skills/create-repo"
"$scripts_dir/scaffold.sh" <repo-name> <Brand> <org> [single|multi]
```

This (deterministic, no code-gen, no commit):
1. creates `workbench/{org}/{repo-name}/`,
2. copies the product-repo template — **including the working `Sample` example** —
   (`workbench/wow-two-sdk-beta/wow-two-sdk-beta.product-template/`) in, dropping its `.git` + build artifacts,
3. replaces `{{REPO_NAME}}` `{{Brand}}` `{{repo-slug}}` `{{NET_VERSION}}` `{{YYYY-MM-DD}}` across the docs,
4. **brand pass** — replaces `Sample` → `{Brand}` (and lowercase `sample` → `{brand}`) across all
   code/config (`.cs`, `.csproj` incl. `InternalsVisibleTo`+`ProjectReference`, `.sln`, `package.json`,
   `vite.config.ts`, `scripts/deploy.mjs`, `Dockerfile`/`docker-compose.yml`, `appsettings*.json`,
   `launchSettings.json`), then renames every `Sample*` **file/dir** → `{Brand}*`
   (`Sample.sln`→`{Brand}.sln`, the 5 project dirs, `tests/Sample.Tests`, `SampleDbContext.cs`, …),
5. **port pass** — the template binds `8220` https / `8221` http / `8225` vite; re-allocates to the
   next-free even/odd backend pair + free vite port (seeded from `conventions/development/repo/ports.md`
   "Next free", scanning existing `launchSettings.json`/`vite.config.ts` to avoid collisions), rewrites
   them across launchSettings/vite proxy/`.http`/appsettings, and appends a `ports.md` row + bumps "Next free",
6. **slug-prefix pass** — the template ships its code dirs as `sample.backend-services/` +
   `sample.frontend-services/`; retargets the prefix to the repo `{slug}` (the **hyphenated** last
   dot-segment, e.g. `secrets-vault` — NOT the lowercased brand `secretsvault`) on disk AND in every
   content path-ref (`deploy.mjs`, `Dockerfile`, `.dockerignore`, `codebase.md`, doc tables),
7. writes a root `.gitignore`, runs `git init` **only**,
8. appends the repo to the `PROJECTS` array in `scripts/active.sh`
   (`name|backend-sln|frontend-dir` — **classic `.sln`**, backend = `{slug}.backend-services/{Brand}.sln`,
   frontend = `{slug}.frontend-services` — paths relative to `workbench/`).

Free-text placeholders (`{{ONE_LINE_WHAT_THIS_IS}}`, guideline bodies, the per-project rows in
`.claude/rules/file-references.md`) stay — fill them with the user's one-liner. **The `codebase/` code
is already in place and rebranded** — no authoring needed; just verify it builds.

**Resulting layout** (per `conventions/development/repo/repo-structure.md` — each folder leads with its
`{folder}.md`, no README below root):

```
{repo}/
├── README.md · CLAUDE.md · .claude/rules/file-references.md
├── product/                  product.md · context.md
│   ├── features/  features.md           ├── planning/   planning.md
│   ├── flows/     flows.md              └── marketing/  marketing.md
└── engineering/              engineering.md
    ├── architecture/   architecture.md
    ├── codebase/       codebase.md · {slug}.backend-services/ · {slug}.frontend-services/   ← ALL code here
    ├── development/    development.md · backend-guidelines.md · frontend-guidelines.md · iteration-guide.md
    ├── deployment/     deployment.md · Dockerfile · docker-compose.yml   (context = ../codebase)
    ├── planning/       planning.md · backlog.md · rules.md
    ├── versions/       versions.md
    ├── research/       research.md
    └── scripts/        scripts.md
```

The template already ships this conformant shape. If a copy ever hands back a stale name
(`business-logic/`, `platform-development/`, `src/`, `guidelines/`, a folder `README.md`) rename it to
the above — the target shape is non-negotiable — but normally there's nothing to fix.

## 3 · The backend is already in place — `engineering/codebase/{slug}.backend-services/`

`scaffold.sh` copied the template's working example and rebranded it. **Don't author code** — the 5
Clean-Arch projects already exist as `{Brand}.*` and build against the kit. Defer all code style to
`conventions/development/backend/`.

What's there (rebranded from `Sample` → `{Brand}`):

- **Solution** `{Brand}.sln` (classic `.sln`) referencing the 5 projects + `tests/{Brand}.Tests`.
- **Projects** (`net{N}.0`, `Nullable`+`ImplicitUsings` via `Directory.Build.props`; central package
  versions via `Directory.Packages.props`), Clean-Arch layering per
  `conventions/development/backend/service-architecture.md`. They use the **kit**
  `WoW2.Sdk.Backend.Beta` — its mediator (`ISender`/`IRequest`/`IRequestHandler`), `Result`/`Result<T>`
  + `DomainError`, and `IKeyedEntity<T>`. No hand-rolled `Results/`, `Common/IEntity`, or local mediator.
  - `{Brand}.Domain` — `Greetings/Entities/GreetingLog : IKeyedEntity<Guid>` (kit base).
  - `{Brand}.Application` — `DependencyInjection.AddApplication` → kit `AddMediator(assembly)`;
    `Abstractions/IClock`; one CQRS vertical `Greetings/Queries/GetGreeting/*` returning `Result<string>`.
  - `{Brand}.Infrastructure` — `Time/SystemClock : IClock`, `DependencyInjection.AddInfrastructure`.
  - `{Brand}.Persistence` — `{Brand}DbContext` (EF Core **SQLite**), `DependencyInjection.AddPersistence`
    + `InitializeDatabaseAsync` using **`EnsureCreatedAsync`** — schema is created on boot, **no migration
    files** and no `dotnet-ef` tooling.
  - `{Brand}.Api` — slim `Program.cs` → `Configurations/HostConfiguration`(+`Extensions`) +
    `AppInitialization`; `Controllers/GreetingController` (`ISender` + `result switch → Ok / Problem`);
    `wwwroot/index.html` placeholder; `appsettings.json`(+`.Development`); `Properties/launchSettings.json`.
- **Ports** — already re-allocated by `scaffold.sh` (template's `8220`/`8221` https/http + `8225` vite →
  the next-free pair; see §2's port pass). Nothing to set by hand.

> **Drydock is an optional richer reference only** — for deeper patterns (more verticals, controllers,
> commands) consult `workbench/wow-two-platform/wow-two-platform.drydock/`, but it is **not** the code
> source and is not copied. Note Drydock predates the kit (local `Results/` etc.) — prefer the kit.

## 4 · The frontend is already in place — `engineering/codebase/{slug}.frontend-services/`

Also copied + rebranded. A minimal Vite 6 + React 19 app at the `{slug}.frontend-services/` root: `package.json`
name `{brand-lc}-frontend` (scripts `dev`/`build`/`deploy`); `vite.config.ts` (`base:'/'`, dev
`server.proxy['/api'] → http://localhost:{HTTP_PORT}` — already pointed at the new http port);
`src/main.tsx` (StrictMode root) + `src/App.tsx` (fetches `GET /api/greeting`, shows it) + `index.html`;
`scripts/deploy.mjs` (build → copy `dist` into `{slug}.backend-services/{Brand}.Api/wwwroot` — path already
rebranded). For `multi` mode, fan this single app out into a pnpm workspace as the product grows.

## 5 · Single-host serving + Docker (already wired)

The example already serves the SPA from the API host and ships Docker:

- `HostConfiguration` does `UseDefaultFiles()` + `UseStaticFiles()` + `MapControllers()` +
  `MapGet("/health", …)` + `MapFallbackToFile("index.html")` — one host serves API + SPA.
- `engineering/deployment/` holds `Dockerfile` + `docker-compose.yml` (3-stage: node build SPA →
  dotnet publish with SPA in `wwwroot` → aspnet runtime; SQLite on a `/data` volume). Build context
  `= engineering/codebase/` (compose `context: ../codebase` + `dockerfile: ../deployment/Dockerfile`);
  `.dockerignore` at the context root. The brand pass already rewrote the `{Brand}.Api` /
  `{Brand}.Api.dll` / image / container / volume names. Nothing to wire — just verify if you touch it.

## 6 · Git & registration (already done by scaffold.sh — verify)

`scaffold.sh` ran `git init` (no commit) and added the `active.sh` entry (backend = the classic
`{Brand}.sln`). **Do not commit** — the developer manages git. Confirm: `scripts/active.sh -l` lists the
new short name.

## 7 · Verify, then report

The code is already present — just confirm it builds, then fill placeholders. Schema is created on boot
via `EnsureCreated` (**no `dotnet ef migrations` step**).

```bash
be="workbench/{org}/{repo-name}/engineering/codebase/{slug}.backend-services"
dotnet build "$be/{Brand}.sln"

fe="workbench/{org}/{repo-name}/engineering/codebase/{slug}.frontend-services"
( cd "$fe" && npm install && npm run build )
```

Then fill the doc `{{placeholders}}` (`{{ONE_LINE_WHAT_THIS_IS}}`, guideline bodies, the per-project
rows in `.claude/rules/file-references.md`) with the user's one-liner.

Report: repo path, resolved `{Brand, org, mode}`, the **ports** chosen, backend build result,
frontend build result, the `active.sh` short name, and anything left as a `{{placeholder}}` for the
user to fill. If a build fails, fix against `conventions/development/backend/` and re-run before
reporting success.

## Notes

- **Conformance is the point:** never `src/`, never `business-logic/` or `platform-development/`, never a
  loose `{name}.backend` dir, never a **bare** `backend-services`/`frontend-services` — only `product/` +
  `engineering/` with all code under `engineering/codebase/{slug}.{backend-services,frontend-services}`
  (slug-prefixed). The template already ships this shape.
- **Kit, not pre-kit:** the example uses `WoW2.Sdk.Backend.Beta` (kit mediator, `Result`/`DomainError`,
  `IKeyedEntity`). Do **not** reintroduce local `Results/` + `ResultError`, `Common/IEntity`,
  `ApiResults.ToStatusCode`, or a MediatR `AddApplication` — those are pre-kit. Code style:
  `conventions/development/backend/`.
- **No README below root.** Every folder leads with `{folder}.md`; if a copy still ships a stray
  `README.md` inside a folder, rename it to the folder-doc name.
- `scaffold.sh` refuses to clobber an existing repo dir and won't double-register in `active.sh`.
- Toolchain check (once): `dotnet --version` (≥ `net{N}`) and `node --version` (≥ 20) before verifying.
