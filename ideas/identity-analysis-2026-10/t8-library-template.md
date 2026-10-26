# T8 — Domain library repo template

*Last updated: 2026-10-25*

> One template, `wow-two-sdk-beta.domain-template`, stamps every per-domain repo (be packages, fe package, service,
> image) through a `SHAPE=domain` mode of `create-repo`; the capability spec moves into the repo, and the hub keeps a
> catalog entry, a platform-apps row and cross-capability decisions.

- `W` = workspace root; `(U)` = unverified; aliases and track names as in [T5](t5-sdk-breakdown.md).
- Package layer names (`Abstractions`, `Module`, `Client`, `Testing`) are placeholders until T7 settles the cut.
- Facts come from reads on 2026-10-25 of the product template, `create-repo`, both SDK repos, pipelines `v0.10.0`,
  the catalog, the conventions and T5/T6; nothing was built, run or edited.

---

## Verdict

- Build a second template beside the product template: `wow-two-sdk-beta.domain-template`, local-only like it.
- `create-repo` gains `SHAPE=domain`; the mechanics stay (copy, rebrand, ports, `active.sh`), the template differs.
- The shell is the product template's; the backend splits into `packages/` · `service/` · `tests/`, the frontend gains `packages/fe-{slug}`.
- Three version lines: NuGet `10.y.z-beta` and npm `0.0.z` from tags, image `X.Y.Z` from the version track.
- Images go through shared `delivery.yml@v0.10.0`; packages go through a repo-local `publish-packages.yml` with OIDC and no stored secret.
- The spec becomes `product/product.md` of the domain repo; `ideas/` keeps a spec only while no repo exists.
- The rollout is 27 steps; 8 need the developer's hands (repo, settings, remote and flags, NuGet policy, first npm publish, GHCR access, Wheelhouse secrets, Ocharo secrets).
- Two findings change T5: `catalog.yml` has no Identity entry to edit, and a GitHub Release per package tag would break the pipelines' base-release lookup.

---

## 1 · Template design

### Name and home

| Option | For | Against |
|---|---|---|
| `wow-two-sdk-beta.domain-template`, separate repo | beside `product-template`; `domain` names what it stamps; the product template stays small | a second template to keep in step |
| `wow-two-sdk-beta.library-template`, separate repo | the name in the brief | reads as a package-only repo, like the be and fe sdks |
| a `domain` folder inside `product-template` | one template repo | two shapes in one tree; `scaffold.sh` would copy and then prune |

- Pick the first: `workbench/wow-two-sdk-beta/wow-two-sdk-beta.domain-template/`, git-initialised, no remote.
- Catalog entry `wow-two-sdk-beta-domain-template`: `kind: template`, `deploy: none`, `repositories: []`, `local:` set — as `product-template`.
- The example domain is `Sample`, as in the product template; its capability is `Greetings`: one broker, two registrations, one conformance suite.
- The example proves the [capability-forms](../../conventions/development/capability-forms.md) contract: Form 1 over the module, Forms 2/3 over the client, one suite against both.

### Folder tree

`sample.` and `Sample` are the rebrand tokens (§5). Paths under `engineering/codebase/` are relative to it.

```
wow-two-sdk-beta.domain-template/
├── README.md                          artifacts table (NuGet ids, npm, image), install snippets, run and test
├── CLAUDE.md                          lazy-load rules, structure, domain hop, tag-versioning and no-Release rules
├── LICENSE                            MIT, matching PackageLicenseExpression and the fe package copy
├── .gitignore                         build output, *.nupkg, local settings, built wwwroot, *.db
├── .claude/rules/file-references.md   doc lookup table; never lists codebase files
├── .github/
│   ├── renovate.json                  extends renovate-product (the repo is public)
│   └── workflows/
│       ├── publish-docker-image.yml   delivery marker; calls pipelines delivery.yml@v0.10.0
│       ├── publish-packages.yml       NuGet + npm in one file; tag-derived; OIDC; the trusted-publisher identity
│       ├── core-latest.yml            nightly + dispatch: build and test against the newest be sdk and fe sdk
│       ├── conformance.yml            Conformance tier against the released image
│       └── codeql.yml                 shared CodeQL scan
├── product/                           the capability definition; no code
│   ├── product.md                     the capability spec: problem, forms, model, phases (lead doc)
│   ├── product.json                   name and description read by consoles
│   ├── context.md                     current state, binding decisions, decision log
│   ├── features/                      one spec per feature group, listed in the backlog
│   ├── flows/flows.md                 user and product flows
│   └── brand/                         icons and brand guide for the hosted pages (brand.md lead)
└── engineering/
    ├── engineering.md                 technical overview, stack, map
    ├── architecture/
    │   ├── architecture.md            system design: forms map, package graph, service role
    │   ├── contract.md                the broker contract, one per capability, every form
    │   ├── package-registry.md        package, layer, heavy deps, forms, consumers
    │   ├── decisions/                 one ADR per decision
    │   └── flows/                     one {flow}-flow.md per flow
    ├── research/                      research.md lead; analysis batches in dated folders
    ├── planning/
    │   ├── backlog.md                 every unbuilt item, Features group first
    │   └── version-track/v0.1/v0.1.md active version; X.Y drives the image version only
    ├── development/                   development.md · rules.md · backend-guidelines.md · frontend-guidelines.md · iteration-guide.md
    ├── deployment/
    │   ├── deployment.md              lead doc: image, settings, verify, rollback
    │   ├── deploy.yml                 descriptor 2: one service, sites app and console, settings, verify
    │   ├── Dockerfile                 three stages; copies packages/ and the whole fe workspace
    │   └── docker-compose.yml         local verification only
    ├── scripts/
    │   ├── scripts.md                 lead doc
    │   ├── next-version.sh            next be-v / fe-v version from tags (and npm for fe)
    │   ├── test-next-version.sh       throwaway-repo tests for the version logic
    │   ├── verify-release-packages.sh nuspec ids, versions, core floor, readme, symbols, commit
    │   ├── verify-published-packages.sh  the feed shows each id at the version
    │   └── pack-smoke.sh              restores the packed nupkgs in a throwaway consumer
    └── codebase/
        ├── codebase.md                what lives where; how the pieces build
        ├── .dockerignore              excludes tests, bin, obj, node_modules
        ├── sample.backend-services/
        │   ├── Sample.BackendServices.slnx    solution folders Packages · Service · Tests
        │   ├── Directory.Build.props          base + pack metadata; Version from -p:Version, else APP_VERSION, else 0.0.0-dev
        │   ├── Directory.Packages.props       BackendSdkVersion pin of core; third-party floors
        │   ├── global.json · tests.runsettings · .editorconfig
        │   ├── packages/                      the NuGets; id WoW2.Sdk.Beta.Be.Sample.{Part}; one README.md beside each csproj
        │   │   ├── Abstractions/              contract: brokers, models, IEvent records, error catalogue; no heavy deps
        │   │   ├── Module/                    Form 1 implementation, AddSample(), Migrations/NNN-name/{Apply,Rollback}.sql
        │   │   ├── Client/                    Forms 2/3: HTTP client brokers, receivers, AddSampleClient()
        │   │   ├── Testing/                   fakes, personas, test-host helpers
        │   │   └── {extra parts}              per domain (Identity: Providers, Server)
        │   ├── service/                       the deployable; hosts Module, adds only hosting, admin and routing
        │   │   ├── Sample.Api/                Program.cs · Configurations/ · Controllers/ · wwwroot/ · appsettings*.json · launchSettings.json
        │   │   ├── Sample.Application/        admin-console use cases; omitted until the console needs them
        │   │   └── Sample.Infrastructure/     admin-only handlers; omitted until needed
        │   └── tests/
        │       ├── Sample.Tests.Unit/         per-package logic
        │       ├── Sample.Tests.Integration/  Module over a real database
        │       ├── Sample.Tests.E2E/          the service host in-process: SPA, /health, the descriptor's dev check
        │       ├── Sample.Tests.Conformance/  one broker suite; fixtures: in-process Module, running host or image
        │       └── Sample.Tests.Migrations/   embedded SQL apply and rollback
        └── sample.frontend-services/
            ├── package.json · pnpm-workspace.yaml · pnpm-lock.yaml · .nvmrc · .gitignore
            ├── packages/fe-sample/            @wow-two-beta/fe-sample: files [dist, README.md, LICENSE]; exports ./kit ./admin; src/ · tests/
            ├── apps/web/                      hosted pages + console (Vue, five-layer src); takes fe-sample by workspace:*
            └── scripts/deploy.mjs             copies apps/web/dist to service/Sample.Api/wwwroot
```

### Rules the tree encodes

- `packages/` projects are packable; `service/` and `tests/` are not (`IsPackable` false by path in `Directory.Build.props`).
- `service/Sample.Api` references `packages/*` by `ProjectReference`; the nuspec floor on core comes from the `PackageReference` on `WoW2.Sdk.Beta.Be`.
- Migrations ship in `Module`; the service applies them on boot, and a Form 1 consumer applies the same files.
- The service has no Domain or Persistence project; a store lives in `Module` (and `Server` for OIDC state).
- Every `packages/*` csproj adds `<FrameworkReference Include="Microsoft.AspNetCore.App" />` (NU1109 lesson, T5 § 3).
- `TreatWarningsAsErrors` and XML docs apply under `packages/` only, as the be sdk does for its public surface.
- `AssemblyVersion` stays `10.0.0.0`; `Version` comes from the pack step; the image build sets it from `APP_VERSION`.
- Hosted pages and the console are one Vue app (`apps/web`) built into `wwwroot/` by the `BuildSpa` target, as in the product template.
- `fe-sample` stays free of `apps/` imports; the app consumes it the way a product would, through `exports`.
- The template takes the next free port pair from `ports.md` (8384 / 8385 on 2026-10-25) and a free Vite port; its ledger row names the `Sample` example.

---

## 2 · Shared with the product template, and what differs

| Aspect | Product template | Domain template | Kind |
|---|---|---|---|
| Shell docs | `README.md` · `CLAUDE.md` · `.claude/rules/file-references.md` | same files; the README adds the artifacts table, `CLAUDE.md` adds the domain hop and the tag rules | shared |
| `product/` | `product.md` · `context.md` · `features/` · `flows/` · `marketing/` | same minus `marketing/`, plus `brand/`; `product.md` is the capability spec | differs |
| `engineering/` lead docs, `development/`, `scripts/` | as listed | same set; `scripts/` gains the release helpers | shared |
| `planning/` | `backlog.md` + `version-track/` | same; X.Y drives the image only, never the packages | shared |
| `architecture/` | `architecture.md`, `flows/` | adds `contract.md`, `package-registry.md`, `decisions/` | differs |
| `deployment/` | `deploy.yml` (descriptor 2) · `Dockerfile` · compose · `deployment.md` | same files; the Dockerfile also copies `packages/`, `deploy.yml` adds `needs: [postgres]`, a `console` site and typed settings keys | differs |
| Code dir names | `{slug}.backend-services` · `{slug}.frontend-services` | same | shared |
| Solution | `{Brand}.BackendServices.slnx`, five Clean projects flat | same name; folders `packages/` · `service/` · `tests/` | differs |
| Service projects | Domain · Application · Infrastructure · Persistence · Api | Api (+ Application · Infrastructure for the console); no Domain or Persistence | differs |
| Test tiers | `Unit` · `E2E` · `Migrations` | adds `Integration` and `Conformance` | differs |
| `Directory.Build.props` | target, nullable, `APP_VERSION` → `Version` | adds pack metadata, symbols, `-p:Version` precedence, path-based `IsPackable` | differs |
| `Directory.Packages.props` | `BackendSdkVersion` pin of core | same pin; the family's own packages arrive by `ProjectReference` | differs |
| Core dependency | published core, always | published core for packages and service; own packages in-repo | differs |
| Frontend | `apps/web` only | adds `packages/fe-{slug}`, published to npm | differs |
| `BuildSpa` and `deploy.mjs` paths | `{slug}.backend-services/{Brand}.Api` | `…/service/{Brand}.Api` (one level deeper) | differs |
| Versions | one: image `vX.Y.Z` | three: image, NuGet family, npm package | differs |
| Registries | GHCR | GHCR + nuget.org + npm | differs |
| Image CI | `ci.yml` + `publish.yml@v0.9.1` (stale: pipelines is at `v0.10.0`) | `delivery.yml@v0.10.0` with `backends` and `frontends` inputs | differs |
| Renovate | `renovate-private` | `renovate-product` (public repo) + `codeql.yml` | differs |
| Port pass, `active.sh` row, `ports.md` row | yes | yes | shared |
| Catalog entry | `kind` by product type | `kind: platform`, workspace `wow2-platform`, owner org `wow-two-sdk-beta` | differs |
| Conformance doc | product rows in `product-conformance.md` | a "Domain repo" section of exceptions in the same doc | differs |

- Database: PostgreSQL in the deployed service, SQLite-first in tests through the be sdk's provider switch (U: Module SQL on both).
- The product template's stale pin is a separate chore; the domain template starts on `delivery.yml`.
- Both templates keep `validate-frontend.mjs` green: `apps/web`, the literal `packages/*` glob and `@{brand}/web` all exist in the domain tree.

---

## 3 · CI and release

### Workflows

| File | Trigger | Does | Source |
|---|---|---|---|
| `publish-docker-image.yml` | push, pull request, dispatch | PR: ci only. Push: `current → plan → ci → publish`; image to GHCR; bundle on a `vX.Y.Z` release | shared `delivery.yml@v0.10.0` |
| `publish-packages.yml` | push to `main`, dispatch | job `be`: test, pack, verify, tag, NuGet. Job `fe`: check, pack, tag, npm | repo-local, copied from the template |
| `core-latest.yml` | nightly, dispatch | build and test against the newest be sdk and fe sdk | repo-local |
| `conformance.yml` | `workflow_run` of the image publish, nightly, dispatch | pull the released image, start it with PostgreSQL in test mode, run `Tests.Conformance` | repo-local |
| `codeql.yml` | `main` pushes with code, weekly | CodeQL without a build | shared `codeql.yml@v0.10.0` |

- `publish-docker-image.yml` keeps exactly that path; Wheelhouse detects a publishable repo by it.
- `delivery.yml` inputs: `backends` = `dotnet test {Brand}.BackendServices.slnx` with the `global.json` and `.nvmrc`; `frontends` = `lint typecheck test build` at the workspace root.
- Workspace root scripts run `pnpm -r` so `packages/fe-{slug}` builds before `apps/web`.
- The image rebuilds on any change under either code dir; a library change releases packages and image together.
- Every action is pinned to a commit and every job has a timeout, as the pipelines do.
- The repo is public, so duplicate test runs between `delivery` and `publish-packages` cost no minutes.

### `publish-packages.yml`

- `concurrency: publish-packages`, `cancel-in-progress: false`; permissions `contents: write` (tags) and `id-token: write`.
- Both jobs run only when the repository variable `PUBLISH_PACKAGES` is `true`; the scaffold's first push would otherwise publish the `Sample` packages.
- The variable is set at rollout step 20, after the registries trust the workflow.
- Plan step: compare `HEAD` with the commit of the newest `be-v*` tag; no change under `packages/`, `Directory.*.props` or `global.json` skips job `be`.
- Plan step for `fe`: the same against `fe-v*` and `packages/fe-{slug}/`.
- Job `be`: restore, build, run `Tests.Unit`, `Tests.Integration`, `Tests.Migrations` and in-process `Tests.Conformance`.
- Then `next-version.sh be`, `dotnet pack -p:Version=… -p:ContinuousIntegrationBuild=true -p:RepositoryCommit=$GITHUB_SHA`.
- Then `verify-release-packages.sh` and `pack-smoke.sh`; the nupkgs stay as a run artifact.
- Then push the annotated tag `be-v{version}`; a rejected push means another run took the number, so the job fails and a rerun recomputes.
- Then `NuGet/login@v1` (the nuget.org user, as the be sdk does), `dotnet nuget push --skip-duplicate`, and `verify-published-packages.sh`.
- Job `fe`: `pnpm install --frozen-lockfile`, typecheck, lint, test, build, then the packed-consumer check from the fe sdk's `check:package` pattern.
- Then `next-version.sh fe`, set the version in the checkout only, `pnpm pack`, tag `fe-v{version}`, `npm publish <tgz> --access public --provenance`.
- The tag is pushed before the publish, so a failed publish burns a number and never reuses it.
- No job commits to `main`: no `chore: release` commit, no `[skip ci]`, no release-sync wait, no race between `be` and `fe`.

### Versioning

| Artifact | Registry | Line | Derived from | Tag | Workflow |
|---|---|---|---|---|---|
| NuGet family (all parts, one line) | nuget.org | `10.y.z-beta`, first `10.0.0-beta` | newest `be-v10.*` tag + 1; `z` rolls to `y+1` at 100 | `be-v10.y.z-beta` | `publish-packages.yml`, job `be` |
| `@wow-two-beta/fe-{slug}` | npm | `0.0.z` | highest of newest `fe-v*` tag and the registry + 1 | `fe-v0.0.z` | `publish-packages.yml`, job `fe` |
| `{slug}` image | GHCR | `X.Y.Z` | newest `version-track/v{X.Y}/` folder; `Z` from `v*` tags | `vX.Y.Z` | `publish-docker-image.yml` |

- `x = 10` keeps the .NET-major rule of [versioning strategy](../../docs/versioning-strategy.md); the fe line is `0.0.z` like the fe sdk.
- `be-v` and `fe-v` tags never match the pipelines' `v*` filter, so the image patch never moves for a package release.
- Create tags only. A GitHub Release for a package tag would become the "previous release" that `publish.yml` reads with `gh release list --exclude-pre-releases`; it holds no `<product>-release.tar.gz`, so the base bundle is lost and the notes start from the wrong tag.
- Package notes are the commit log between tags; the image release carries the notes Wheelhouse shows.
- Each package's nuspec floor on `WoW2.Sdk.Beta.Be` is the `BackendSdkVersion` pin, enforced by NU1605 in a consumer.
- `fe-{slug}` peers `@wow-two-beta/fe` at `>=0.0.n <0.1.0`; `workspace:*` joins it to `apps/web`.
- Release notes name the core version each release was built against, taken from the pin.

### Shared pipelines or repo-local

| Concern | Choice | Reason |
|---|---|---|
| Image delivery | shared `delivery.yml` | images are what the pipelines own; Wheelhouse reads the bundle |
| Package publish | repo-local workflow, logic in `engineering/scripts/` | the registries trust one workflow file; trusted publishing through a reusable workflow is untested (U) |
| Reuse after the second domain repo | composite actions in pipelines (`next-version`, `verify-packages`) | a composite action runs inside the caller's job, so the OIDC identity stays this file's (U) |
| Compat and conformance | repo-local | they use the repo's pins and suites |

### Secrets and trusted publishing

| Item | Setup | Who | Note |
|---|---|---|---|
| NuGet | trusted-publishing policy on nuget.org: repo owner `wow-two-sdk-beta`, the repo, workflow `publish-packages.yml` | developer, once per repo | whether the minted key can create ids that do not exist yet is untested (U); fallback: push the first versions by hand with a scoped key |
| npm | first publish by hand (`npm login --auth-type=web`), then the package's trusted publisher: repo + `publish-packages.yml` | developer, once per package | the form cannot be edited, only deleted and recreated; the template fixes the file name first |
| GHCR | `GITHUB_TOKEN` with `packages: write` | none | package visibility and Wheelhouse's pull access under the `wow-two-sdk-beta` org are untested (U) |
| Stored secrets | none | — | no `NPM_TOKEN`, no PAT |
| Repo settings | Actions on, default workflow permissions read, Issues and Discussions off | developer | the org defaults may already cover these (U) |
| Renovate | the Mend app must see the repo | developer | only when the installation is scoped to selected repos (U) |

### Compat job and skew

- `core-latest.yml` resolves the newest `WoW2.Sdk.Beta.Be` from the nuget.org flat container and the newest `@wow-two-beta/fe` from npm.
- Job `be` runs `dotnet test … -p:BackendSdkVersion={newest}`; job `fe` updates the dependency without the frozen lockfile and runs the checks.
- Both skip when the newest equals the pin; the run summary records the tested pair.
- A failure is a signal, not a gate: it names the core break before a product meets it.
- Trigger is nightly plus dispatch; a `repository_dispatch` from core's publish would need a PAT stored in core (Open 4).
- Products keep two pins side by side: `BackendSdkVersion` and one `{Domain}SdkVersion` per domain repo (T5 § 4).
- The domain hop of an SDK change: product chat, then domain repo, then core when needed; each hop is a push and a pin (T5 § 4, § 9).

### Gates

- Pull request: `delivery` ci only (solution tests, frontend checks).
- Packages: Unit, Integration, Migrations and in-process Conformance, then pack verification and the packed-consumer restore.
- Image: ci, then publish; Wheelhouse's dev rollout runs the descriptor `verify` check before auto-promote.
- Image conformance (`conformance.yml`) runs after publish and cannot block it; the `verify` check is the promotion gate.
- Domain-specific heavy suites join `conformance.yml`; Identity's OIDF run follows T6 § 6, on tags and nightly.

---

## 4 · Docs placement

### Where each doc lives

| Doc | While no repo exists | Once the repo exists | Hub keeps |
|---|---|---|---|
| Capability spec | `ideas/{capability}-service-spec.md` | `product/product.md`; feature groups in `product/features/{feature}.md` | one link in the `platform-apps.md` row |
| State and decision log | the spec head | `product/context.md` | decisions that span capabilities, in `docs/platform-decisions.md` |
| Contract and design | the spec | `engineering/architecture/` | — |
| Analysis batch and its decision queue | `ideas/{capability}-analysis-{yyyy-mm}/` | `engineering/research/{capability}-analysis-{yyyy-mm}/` | — |
| Plan and sequencing | the spec § Sequencing | `engineering/planning/backlog.md` + `version-track/` | the cross-app order in `platform-apps.md` |
| Package inventory | be `package-registry.md` | `engineering/architecture/package-registry.md` | — |
| Per-domain research in a core repo | be `engineering/research/{vector}/` | `engineering/research/` | a pointer row in the core registry |
| Catalog entry, registry row, ports row | hub | hub | yes |

### What the hub keeps

- the `catalog.yml` entry: slug, workspace, kind, deploy, status, one-line purpose, repositories.
- the `docs/platform-apps.md` row: order, one-line what, state, ship gate, needs, and a link to the repo's `product/product.md`.
- cross-capability decisions in `docs/platform-decisions.md` (D-numbers that touch two or more capabilities).
- the generated `.claude/repo-registry.md` row and the `ports.md` row.
- the conventions that govern every domain repo; no capability's own rules.

### Identity move map

| From | To |
|---|---|
| `ideas/identity-service-spec.md` § Problem, Placement, Build path | `product/product.md` |
| § Status line, D1–D3, What already exists, Gaps | `product/context.md` |
| § Features (nine groups) | `product/features/{sign-in,accounts,passwords,second-factors,sessions-tokens,abuse-protection,admin-console,self-service,developer-surface}.md`; one row each in `backlog.md` § Features |
| § Ocharo slice (P1) | `engineering/planning/version-track/v0.1/v0.1.md` iterations |
| § Sequencing | `backlog.md` and `v0.1.md`; the cross-app order stays in `platform-apps.md` |
| § Sources | a link list at the foot of `product/product.md` |
| `ideas/identity-analysis-2026-10/` (index, T1–T8) | `engineering/research/identity-analysis-2026-10/`, same file names |
| the index's `## Points` queue | stays in the moved index until empty; each answer lands in `product/context.md` |
| be `engineering/research/identity/` (3 files) | `engineering/research/` |

- 22 hub-relative links inside the moved files (18 in the tracks, 4 in the spec) become `wow-two-ws/…` path text, as the product template cites conventions.
- Links among the moved files, and from the tracks to the spec, are re-pointed to the new paths (`product/product.md`).
- 4 hub files link into the moved set and are fixed in the same pass: `platform-apps.md`, `platform-decisions.md`, `file-storage-service-spec.md`, `own-ideas-review-2026-10.md`.
- 2 links sit outside the hub: be `identity-slices.md` (moves with its folder) and `ocharo-ws/docs/architecture.md` (an Ocharo chat edits it).
- T6 § Real hosts names providers and regions; a public repo indexes better than the hub, so trim that table first (Open 5).
- The move is the repo's first docs commit; it cites the hub commit it copies, and the hub deletion follows in the hub's own commit.

### Convention bullets

Home: a new `## Docs` section in [capability forms](../../conventions/development/capability-forms.md), one owner for the rule.

```markdown
## Docs

- must keep a capability's spec, research and plan in its domain repo once the repo exists.
- must write the spec as the repo's `product/product.md`; a feature group grows into `product/features/{feature}.md`.
- must keep the capability's state and decision log in `product/context.md`.
- must file the contract and design in `engineering/architecture/`, analyses in `engineering/research/`.
- must plan in `engineering/planning/`; the repo's version track drives its image version only.
- must keep in the hub the catalog entry, the platform-apps row and decisions that span capabilities.
- must link the spec from the platform-apps row; must not copy spec text into the hub.
- must start a spec in `ideas/{capability}-service-spec.md` while no repo exists.
- must move the spec and its analysis batch in the repo's first docs commit, decision queue included.
- must delete the hub copies in the same pass and update every inbound link.
- must name hub documents in the repo's docs as `wow-two-ws/…` paths, never relative links.
```

Replacement for § Layout of the same doc:

```markdown
| Half | Lives in | Holds |
|---|---|---|
| core seams | be sdk · fe sdk | primitives other areas import: results, events, auth primitives |
| capability | `wow-two-sdk-beta.{capability}` | contract, Form 1 module, HTTP client, fe package, host, admin UI, Dockerfile, `deploy.yml` |

- must build the service in the repo that publishes the packages it hosts, by project reference.
- must build the service by hosting the Form 1 module, never by implementing the logic a second time.
- must keep the service's HTTP API a mirror of the contract; the service adds hosting, admin and app routing.
- must pin core to a published version; a core change goes core first, then a pin bump.
- must publish the image per [deploy descriptor](../deployment/descriptor/deploy-descriptor.md) § Rules.
- must publish packages from the repo's own workflow, tag-derived, with no release commit.
- must keep UI parts form-agnostic; they call the consumer's backend or the service API through the contract.
```

---

## 5 · `create-repo` changes

### Inputs

| Input | `product` (today) | `domain` (new) |
|---|---|---|
| `SHAPE` (env, new) | default | `domain` |
| repo name | `wow-two-platform.foo` | `wow-two-sdk-beta.{capability}` |
| Brand | PascalCase project prefix | PascalCase domain: namespace root `WoW.Two.Sdk.Beta.Be.{Brand}`, ids `WoW2.Sdk.Beta.Be.{Brand}.{Part}` |
| org | `workbench/{org}` | default `wow-two-sdk-beta` |
| mode | `single` · `multi` | ignored |
| `SLUG` (env, new) | last dot-segment | same; passed explicitly for dotted names such as `storage.file` |
| `PRODUCT` (env, new) | lowercased Brand | same; must equal the catalog slug and the Wheelhouse product |
| `CORE_VERSION`, `FE_VERSION` (env, new) | — | pins written to `BackendSdkVersion` and the `@wow-two-beta/fe` dependency; default the template's |
| `SCRATCH=1` (env, new) | — | scaffold into a temp dir; no `active.sh`, no ports row, no `git init` |

### `scaffold.sh` passes

- Template path: `TEMPLATE` is chosen by `SHAPE`; the rest of the flow is unchanged.
- Validation: `validate-frontend.mjs` runs on the domain template's `sample.frontend-services` as is (reads: `apps/web`, `packages/*` glob, `@{brand}/web`).
- New rebrand rule before the generic pass: `fe-sample` → `fe-{slug}` (the hyphenated slug differs from the lowercased Brand for names like `FileStorage`).
- New rebrand rule: the template's repo name in `PackageProjectUrl`, `RepositoryUrl` and `repository.directory` → the new repo.
- Existing rules cover `Sample` → Brand, `sample.{backend,frontend}-services` → slug dirs, `sample` → product, `SAMPLE` → upper product.
- Port pass: `TPL_*` become per-shape constants (the domain template's pair), so a rewrite never touches the product template's ports.
- Registration: `active.sh` row `slug|…/{slug}.backend-services/{Brand}.BackendServices.slnx|…/{slug}.frontend-services`; ports row; `git init` only.
- Printed, not applied: the `catalog.yml` entry (free text and quoting rules) and the `~git_on commit,push` line for the developer.
- `SCRATCH=1` leaves nothing in the workbench to remove, which keeps template checks clear of the blocked `rm -rf`.

### Skill text (`SKILL.md`)

- Description: add triggers "new domain repo", "library plus service repo", "per-domain SDK repo"; keep the product triggers.
- Replace "Not for SDK / library repos" with: package-only repos (be sdk, fe sdk) stay out; a domain library with a service uses `SHAPE=domain`.
- § 1: add the shape row and the input table above; confirm `{repo, Brand, org, shape}` before scaffolding.
- § 2: add the domain passes; add the resulting-layout block from § 1 of this track.
- § 3–5: a domain variant of the backend, frontend and delivery notes (`packages/` · `service/` · `tests/`, `fe-{slug}`, three workflows).
- § 6: registration adds the catalog entry, the registry regeneration and the git-flag line.
- § 7: domain verify commands below.
- Drop `.claude/templates/CLAUDE-sdk.md` from the pointer; it describes a single-package SemVer repo and fits neither SDK repo today.

```bash
be="workbench/wow-two-sdk-beta/{repo}/engineering/codebase/{slug}.backend-services"
dotnet test "$be/{Brand}.BackendServices.slnx"

fe="workbench/wow-two-sdk-beta/{repo}/engineering/codebase/{slug}.frontend-services"
( cd "$fe" && pnpm install --frozen-lockfile && pnpm -r build && pnpm lint && pnpm test )

bash workbench/wow-two-sdk-beta/{repo}/engineering/scripts/test-next-version.sh
```

---

## 6 · Rollout checklist

`[by hand]` marks a step only the developer can run. `needs` names the steps or decisions that block it.

### A · Prepare, before the repo exists

1. (developer) Answer queue A of the [index](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.identity/blob/main/engineering/research/identity-analysis-2026-10/identity-analysis-2026-10.md) — Q1, Q1a–d — and approve T7's package cut. Needs: T7. Blocks 8 onward.
2. (agent) Build `wow-two-sdk-beta.domain-template` per § 1; `git init`, no remote; ledger row; catalog `template` entry. Needs: T7 layer names.
3. (agent) Extend `create-repo` (§ 5) and prove the template with a `SCRATCH=1` scaffold: slnx tests, pnpm build, `test-next-version.sh`. Needs: 2.
4. (agent) Edit the conventions in one pass. Needs: 1 (org and name), 2.
   - `capability-forms.md`: § Layout replaced, § Docs added (§ 4).
   - `sdk-structure.md`: a domain archetype — shell + `product/` + `deployment/`; two code dirs `{slug}.backend-services` (`packages/` · `service/` · `tests/`) and `{slug}.frontend-services` (`packages/` · `apps/`).
   - Same doc: naming `wow-two-sdk-beta.{capability}`, `WoW2.Sdk.Beta.Be.{Domain}.{Part}`, `@wow-two-beta/fe-{domain}`.
   - `repo-structure.md` § Archetypes: a third row, domain repo, pointing at `sdk-structure.md`.
   - `product-conformance.md`: a "Domain repo" section — own packages by `ProjectReference`, no service Domain or Persistence, tiers `Integration` and `Conformance`.
   - `dev-cycle.md`: the domain hop in § SDK change loop; § SDK release sync does not apply to tag-derived repos.
   - `docs/versioning-strategy.md`: three artifacts, three tags (`be-v`, `fe-v`, `v`).
   - `W/CLAUDE.md` § SDK doctrine names the domain repos and the extra hop; `conventions.md` indexes the changed docs.
5. (agent, core lane) Release core `10.0.N`, non-breaking: the error-text contribution seam in `Web/ErrorTranslation`, delete `IdentityApi/` and `Policies/`; wait for the release commit, `git pull --ff-only`. Needs: core `commit` and `push` flags. Runs beside 2–4.

### B · Create the repo

6. (developer) `[by hand]` Create `wow-two-sdk-beta/wow-two-sdk-beta.identity` on GitHub: public, empty (no README or license), default branch `main`. Needs: 1.
7. (developer) `[by hand]` Repo settings: Actions on, default workflow permissions read, Issues and Discussions off, no branch protection; add the repo to the Mend Renovate installation if it is scoped (U). Needs: 6.
8. (agent) `SHAPE=domain .claude/skills/create-repo/scaffold.sh wow-two-sdk-beta.identity Identity wow-two-sdk-beta`; fill placeholders from the spec's one-liner. Needs: 1, 3, 4.
9. (developer) `[by hand]` `git remote add origin …` (agents never write remotes), then send `~git_on commit,push` for the repo path as one whole-message directive. Needs: 6, 8.
10. (agent) Verify the scaffold with the § 5 commands, plus `docker build` when Docker runs; commit the scaffold; push when the flag allows. Needs: 8, 9.
    - The first push publishes a `Sample`-content image as `v0.1.1`, as any new product repo does; `PUBLISH_PACKAGES` keeps the packages workflow disarmed.

### C · Hub and docs

11. (agent) Hub registration: create the `identity` entry in `catalog.yml` (`kind: platform`, `deploy: none`, status "Planned", the new repository), set the repo name in the `platform-apps.md` row, run `scripts/gen-repo-registry.py`. Needs: 6.
    - T5 said "the existing Identity entry"; none exists today, so this creates it.
    - The generator files it under org `wow-two-sdk-beta`, by repository owner, not under `wow-two-platform`.
12. (agent) Move the spec and the analysis batch per § 4: first docs commit in the repo, then the hub deletions and the 4 hub link fixes in the hub's own commit. Needs: 10, 11, Open 5.
    - An Ocharo chat fixes `ocharo-ws/docs/architecture.md`.

### D · Move and cut the code

13. (agent) Copy the 7 folders, 62 tests, 38 docs and `research/identity/` into `packages/` per T7; add csprojs; cite the core commit in the first commit; do not build yet. Needs: 5, 10.
    - Core `10.0.N` still holds the same types, so a build against it fails with duplicate types (CS0433).
14. (agent) Dry run: remove the folders and the 24 references from core locally, pack `N+1` into an uncommitted local feed, build and test Identity against it. Needs: 13.
15. (agent, core lane) Release core `10.0.N+1`, the one breaking release: removal, the `Auth` rename (Q1c), be docs (`package-registry.md`, `package-layout.md`, `CLAUDE.md`, backlog rows, a pointer for `research/identity/`). Push, wait for the release commit, `git pull --ff-only`. Needs: 14 green, core `push` flag.
16. (agent) Set `BackendSdkVersion` to `N+1`, build, test, commit. Needs: 15.

### E · Implement

17. (agent) P1 in lanes by folder — Server, Client, Module slices, `fe-identity`, `apps/web` — per `version-track/v0.1`. Needs: 16.

### F · Publish

18. (developer) `[by hand]` NuGet trusted-publishing policy for the repo and `publish-packages.yml`; if the key cannot create new ids (U), push the first versions by hand with a scoped key. Needs: 6.
19. (developer) `[by hand]` First npm publish of `@wow-two-beta/fe-identity` from a packed tarball, then its trusted publisher. Needs: the package has its first screens (17).
20. (agent) Set `PUBLISH_PACKAGES=true` (a gh write: needs the `push` flag, else the developer sets it), push `main`; `publish-packages.yml` publishes the family at `10.0.0-beta`; run `verify-published-packages.sh`; tag the hand-published npm version `fe-v0.0.1` so the next number follows. Needs: 16, 18, and 19 for the npm job.
21. (developer) `[by hand]` After an image build lands at `ghcr.io/wow-two-sdk-beta/wow-two-sdk-beta.identity/identity` (step 10's push already made one), set the package's visibility or access so Wheelhouse can pull (U). Needs: 10.
22. (agent) Dispatch `core-latest.yml` and `conformance.yml` once; both green before consumers move. Needs: 20, 21.

### G · Register and bind

23. (agent) Flip the catalog entry to `deploy: wheelhouse` with the real status; regenerate the registry. Needs: 21.
24. (developer) `[by hand]` In Wheelhouse: register product `identity`, pick the server, enter the required settings and secrets (database, signing keys, bot and channel keys), bind `id` public and `console` private, confirm the dev `verify` check passes. Needs: 21, 23; Q4 (Form 3 host), Q5 (two owners' instances of one image), Q25 (keys).

### H · Integrate

25. (agent) Consumer sweep, one commit per repo: re-pin core to `N+1`, add the `IdentitySdkVersion` pin and package refs (Module, Providers or Client), apply the `Auth` namespace edits. Needs: 20; each consumer's flags (the developer sends one `~git_on` per repo, or a `*` default).
    - Order: pilots ×10, Wheelhouse (stays Form 1), Haven, ForeverPin, TranscriptForge; Ocharo Desk runs in an Ocharo chat.
    - Repos with no identity use stay on core ≤ N or re-pin only.
26. (agent + developer) Ocharo's Form 2 instance: the agent builds the migration of Desk's accounts, memberships and `telegram_links` and moves the apps to OIDC clients one by one; the developer `[by hand]` supplies the bot, secrets and DNS. Needs: 24, 25; Q5, Q30 (domain binding, off-host backups), Q32.
27. (agents, parallel) Apps and the identity server build side by side: a product chat fixes the domain repo instead of working around it, the push publishes, the product re-pins; core-first when core must change. Needs: 20.

### Developer-only steps

| # | What | Why only the developer | Unblocks |
|---|---|---|---|
| 6 | create the GitHub repo | the `push` flag is per repository and none exists for a repo not yet created; the org login is the developer's | 7–12 |
| 7 | repo settings, Renovate access | account and org settings | 20, 25 |
| 9 | `git remote add`, `~git_on` | agents never write remotes; flags change only by a whole-message directive | 10 |
| 18 | NuGet trusted-publishing policy | nuget.org account login | 20 |
| 19 | first npm publish, trusted publisher | npm login with a browser 2FA approval; no publisher form before version 1 | 20 |
| 21 | GHCR package access | package settings in GitHub | 22, 24 |
| 24 | Wheelhouse secrets, server, domains | secrets and DNS stay with the developer | 26 |
| 26 | Ocharo bot, secrets, DNS | same | cutover |

- Pushes in steps 5, 15 and 20 are the agent's when the repository's `push` flag is `ON`, else the developer's.
- Step 27 repeats for File Storage: its chat runs steps 6–12 and 18–21 with `Brand=FileStorage`; the second repo is the trigger to promote the scripts into pipelines composite actions.

---

## Open

1. Template name and home: `wow-two-sdk-beta.domain-template`, or `library-template`, or a shape inside the product template?
   - Pick `domain-template`, a separate local-only repo; `library-template` reads as a package-only repo.
2. Where the capability spec lives in the repo: `product/product.md` with `product/features/`, or `engineering/architecture/`?
   - Pick `product/`: it is the definition (what, why, features), and the product template already treats it so.
3. Package publish reuse: repo-local workflow now, or a reusable `packages.yml` in pipelines before File Storage starts?
   - Pick repo-local with the logic in `engineering/scripts/`; promote composite actions after the second repo, once OIDC through one is tested.
4. Compat trigger: nightly plus dispatch, or `repository_dispatch` from core's publish with a PAT stored in core?
   - Pick nightly plus dispatch: no secret, no core workflow edit; add the dispatch if a day's lag hurts.
5. T6 § Real hosts names providers and regions; trim them before the public repo receives the file, or move as is?
   - Pick trim to "a products host" and keep the detail in Wheelhouse's private notes.
