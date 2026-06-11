---
name: create-repo
description: >-
  Scaffold a NEW conformant product / venture repo for the wow-two workspace from the standard
  template + the Drydock reference pattern — a copyable Clean-Arch .NET 10 backend + React 19 / Vite
  frontend under engineering/codebase/, single-host serving, Docker, git init, and registration in
  scripts/active.sh. Use this whenever the user wants to create / start / spin up / bootstrap / set up
  a new repo, project, product, venture, app, service, or POC in this workspace (e.g. "create a new
  repo for X", "scaffold a new venture", "start a new product repo", "spin up a new backend+frontend
  repo", "bootstrap a conformant repo named foo", "new wow-two-platform repo"). Trigger even when the
  user does NOT name the template, Drydock, the IDE, or "conformant" — phrases like "make me a new repo
  for a QR tool" should use this skill. Covers single-service (default) and multi-service shapes.
---

# create-repo

Scaffolds a **product / venture** repo that conforms to
`conventions/development/repo/repo-structure.md` (top-level `product/` + `engineering/`;
**all code under `engineering/codebase/`**; the two code dirs are **exactly**
`codebase/backend-services/` + `codebase/frontend-services/`). Mechanics live in `scaffold.sh`; the
code generation (which depends on brand/name) is driven here by Claude.

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
2. copies the product-repo template (`workbench/wow-two-sdk-beta/wow-two-sdk-beta.product-template/`) in,
3. replaces `{{REPO_NAME}}` `{{Brand}}` `{{repo-slug}}` `{{NET_VERSION}}` `{{YYYY-MM-DD}}` across the docs,
4. writes a root `.gitignore`, runs `git init` **only**,
5. appends the repo to the `PROJECTS` array in `scripts/active.sh`
   (`name|backend-slnx|frontend-dir`, paths relative to `workbench/`).

Free-text placeholders (`{{ONE_LINE_WHAT_THIS_IS}}`, guideline bodies) stay — fill them with the
user's one-liner. The two `codebase/` code dirs are left empty for the next steps.

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
    ├── codebase/       codebase.md · backend-services/ · frontend-services/   ← ALL code here
    ├── development/    development.md · backend-guidelines.md · frontend-guidelines.md · iteration-guide.md
    ├── deployment/     deployment.md · Dockerfile · docker-compose.yml   (context = ../codebase)
    ├── planning/       planning.md · backlog.md · rules.md
    ├── versions/       versions.md
    ├── research/       research.md
    └── scripts/        scripts.md
```

If the template hands back stale names (`business-logic/`, `platform-development/`, `src/`,
`platform-planning.md`, `guidelines/`, folder `README.md`s) rename them to the above before generating
code — the target shape is non-negotiable.

## 3 · Generate the backend — `engineering/codebase/backend-services/`

Mirror the **Drydock backend** exactly, renamed to `{Brand}` and at the conformant path. Reference:
`workbench/wow-two-platform/wow-two-platform.drydock/platform/src/drydock.backend/` (Drydock's own
dir names are non-conformant — copy its contents/shape, not its folder names). Defer all code style
to `conventions/development/backend/`.

- **Solution** `{Brand}.slnx` (XML format) referencing the 5 projects below.
- **Projects** (`net{N}.0`, `Nullable`+`ImplicitUsings` enabled), Clean-Arch layering per
  `conventions/development/backend/service-architecture.md`:
  - `{Brand}.Domain` — `Results/` (Result, Result<T>, ResultError), `Common/IEntity`+`IKeyedEntity<T>`,
    one trivial entity + enum (e.g. `Items/Entities/Item`, `Items/Enums/ItemStatus`).
  - `{Brand}.Application` — MediatR (`DependencyInjection.AddApplication`), `Abstractions/IClock`,
    one CQRS vertical (a `Query` + `Command` under `Items/`) + a `Models/ItemDto`, a store abstraction.
  - `{Brand}.Infrastructure` — `Time/SystemClock : IClock`, `DependencyInjection.AddInfrastructure`.
  - `{Brand}.Persistence` — `{Brand}DbContext` (EF Core **SQLite**), `{Brand}DbContextFactory`
    (design-time), an EF store impl, `DependencyInjection.AddPersistence` + `InitializeDatabaseAsync`
    (`MigrateAsync`). Generate the initial migration in step 7.
  - `{Brand}.Api` — slim `Program.cs` delegating to `Configurations/HostConfiguration`(+`Extensions`)
    + `AppInitialization`; `ApiResults.ToStatusCode(ResultError)`; `Controllers/SystemController`
    (`GET /api/system/status`) + the `Items` controller (`ISender` + `result.Match → Problem(...)`);
    `wwwroot/.gitkeep`; `appsettings.json`(+`.Development`); `.config/dotnet-tools.json` pinning
    `dotnet-ef`; `{Brand}.Api.http` with `@host` = the HTTPS port; `Properties/launchSettings.json`.
- **Ports** — pick the **next free even/odd pair** (HTTPS even, HTTP odd = even+1) not used by any
  existing project: scan `grep -rho 'localhost:[0-9]*' workbench/*/*/platform*/**/launchSettings.json`
  (Drydock = 8210/8211). `https` profile binds **both** URLs; `http` binds only HTTP. Set the Vite
  proxy + `.http` `@host` to match.
- Slim `Program.cs`, file-per-type, Result pattern, `ResultError → ApiResults` — exactly Drydock's shape.

## 4 · Generate the frontend — `engineering/codebase/frontend-services/`

Mirror the **Drydock frontend** (single app at the `frontend-services/` root for `single` mode; a
pnpm workspace with app folders + `packages/` for `multi`). Reference:
`.../drydock.frontend/`.

- React 19 + Vite 6 + **Tailwind v4** + **`@wow-two-beta/ui`**; `package.json` name `{repo-slug}-frontend`,
  scripts `dev` / `build` / `deploy`.
- `vite.config.ts` — `base:'/'`, `@tailwindcss/vite`, dev `server.proxy['/api'] → http://localhost:{HTTP_PORT}`.
- `index.css` — `@import 'tailwindcss'`, `@import '@wow-two-beta/ui/styles.css'`,
  `@source '../node_modules/@wow-two-beta/ui/dist'`.
- `main.tsx` (StrictMode root) · `App.tsx` (header + a Badge pinging `GET /api/system/status` online/offline) ·
  `api/client.ts` (same-origin `/api`, ProblemDetails-aware) · `tsconfig*.json` · `vite-env.d.ts`.
- **`scripts/deploy.mjs`** — build then copy `dist` → the backend `wwwroot`. The relative path is
  load-bearing and **changes with the conformant naming**: target
  `resolve(here, '..', '..', 'backend-services', '{Brand}.Api', 'wwwroot')`
  (Drydock's `'drydock.backend'` segment becomes `'backend-services'`).

## 5 · Single-host serving + Docker

- In `HostConfiguration` (app side): `UseDefaultFiles()` + `UseStaticFiles()` + `MapControllers()` +
  `MapGet("/health", …)` + `MapFallbackToFile("index.html")` — one host serves API + SPA.
- `engineering/deployment/` holds `Dockerfile` + `docker-compose.yml` (3-stage: node build SPA →
  dotnet publish with SPA in `wwwroot` → aspnet runtime; SQLite on a `/data` volume). **Build context
  = `engineering/codebase/`** — compose uses `context: ../codebase` + `dockerfile: ../deployment/Dockerfile`;
  `.dockerignore` sits at the context root (`engineering/codebase/.dockerignore`). Inside the Dockerfile
  the `COPY` paths are relative to `codebase/` → `COPY backend-services …` / `COPY frontend-services …`
  and `{Brand}.Api.dll`. Mirror Drydock's `platform/` shape; rewrite its `src/drydock.{backend,frontend}`
  paths to `backend-services` / `frontend-services`.

## 6 · Git & registration (already done by scaffold.sh — verify)

`scaffold.sh` ran `git init` (no commit) and added the `active.sh` entry. **Do not commit** — the
developer manages git. Confirm the entry: `scripts/active.sh -l` should list the new short name.

## 7 · Verify, then report

```bash
be="workbench/{org}/{repo-name}/engineering/codebase/backend-services"
dotnet tool restore --tool-manifest "$be/{Brand}.Api/.config/dotnet-tools.json"
dotnet ef migrations add InitialCreate \
  --project "$be/{Brand}.Persistence" --startup-project "$be/{Brand}.Api"   # creates schema
dotnet build "$be/{Brand}.slnx"

fe="workbench/{org}/{repo-name}/engineering/codebase/frontend-services"
( cd "$fe" && npm install && npm run build )
```

Report: repo path, resolved `{Brand, org, mode}`, the **ports** chosen, backend build result,
frontend build result, the `active.sh` short name, and anything left as a `{{placeholder}}` for the
user to fill. If a build fails, fix against `conventions/development/backend/` + the Drydock pattern
and re-run before reporting success.

## Notes

- **Conformance is the point:** never emit `drydock.backend` / `{name}.backend` / loose `backend`
  dirs, never `src/`, never `business-logic/` or `platform-development/` — only `product/` +
  `engineering/` with all code under `engineering/codebase/{backend-services,frontend-services}`.
  Drydock's own dir names are non-conformant; copy its *contents/shape*, not its folder names.
- **No README below root.** Every folder leads with `{folder}.md`; if the template still ships a
  stray `README.md` inside a folder, rename it to the folder-doc name.
- `scaffold.sh` refuses to clobber an existing repo dir and won't double-register in `active.sh`.
- Toolchain check (once): `dotnet --version` (≥ `net{N}`) and `node --version` (≥ 20) before verifying.
