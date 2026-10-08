# Product conformance

*Last updated: 2026-10-01*

> Every check a product / venture repo owes, each linked to the convention that owns the rule.
> Purpose — one list to audit a repo against, so a gap sweep reads the same way for every product.
> Use case — auditing a product repo, writing its gap handoff, or validating a fresh scaffold.

## Use

- must read a row as a pointer — the linked owner states the rule, and wins when the two differ.
- must add a row when a convention gains an obligation a product repo can be checked for.
- must skip a row whose subject the repo lacks — a frontend-only product owes no backend row.
- must check the product template first; a gap there is stamped into every new repo.

---

## Repo

| Check | Owner |
|---|---|
| top level is `product/` + `engineering/`; code only under `engineering/codebase/` | [repo structure](repo-structure.md#layout) |
| code directories are `{slug}.backend-services/` and `{slug}.frontend-services/` | [repo structure](repo-structure.md#naming) |
| every folder opens with `{folder}.md`; no `README.md` below the root | [repo structure](repo-structure.md#documents) |
| `CLAUDE.md`, the file-reference table and the product / engineering lead docs exist | [repo structure](repo-structure.md#layout) |
| the repo is in `scripts/active.sh` and its ports are in the ledger | [ports](../../../deployment/hosting/ports.md) |
| a binary over 1 MB is ignored, regenerated or in LFS | [git](../version-control/git.md#large-files) |

---

## Planning

| Check | Owner |
|---|---|
| `backlog.md` opens with a `Features` group; items are grouped, top = next | [version track](../../../planning/version-track/version-track.md#backlog) |
| the newest `version-track/v{X.Y}/v{X.Y}.md` is the active version | [version track](../../../planning/version-track/version-track.md#location--naming) |
| no other planning file — no roadmap, `planning.md` or second track | [version track](../../../planning/version-track/version-track.md#planning-files-required) |
| no loaded `handoff.md` left behind | [agentic workflow](../../../agentic-workflow/agentic-workflow.md) |

---

## Backend

| Check | Owner |
|---|---|
| solution is `{Brand}.BackendServices.slnx`, beside the two `Directory.*.props` | [repo structure](repo-structure.md#naming) |
| projects are Domain, Application, Infrastructure, Persistence and Api | [Clean Architecture](../../backend/dotnet/shapes/service/architecture/clean/clean.md#layers) |
| handlers, contracts and row access sit in their Clean project | [Clean Architecture](../../backend/dotnet/shapes/service/architecture/clean/clean.md#placement) |
| source is grouped by domain before role | [domain structuring](../../backend/dotnet/shapes/service/architecture/clean/domain-structuring.md) |
| tests sit in `tests/`, named `{Product}.Tests.{Unit,Integration,E2E}` | [testing](../../backend/dotnet/shapes/service/architecture/clean/testing.md#layout) |
| `Program.cs` holds three groups; registration lives in `HostConfiguration` | [host configuration](../../backend/dotnet/shapes/service/platform/startup/host-configuration.md) |
| no `Add*` registration extension inside a layer project | [host configuration](../../backend/dotnet/shapes/service/platform/startup/host-configuration.md#configuration-source) |
| the host boots through `AddApiDefaults()` / `UseApiDefaults()` | [startup defaults](../../backend/dotnet/shapes/service/platform/startup/startup-defaults.md) |
| package versions are central; the SDK pins a published version | [central packages](../../backend/dotnet/shapes/service/platform/build/central-package-management.md) |
| one `https` launch profile on the ledger's even / odd pair | [launch profiles](../../backend/dotnet/shapes/service/platform/startup/launch-profiles.md) |
| identity lives at `api/identity/*`, status at `api/system/status` | [known endpoints](../../backend/dotnet/shapes/service/platform/responses/known-endpoints.md) |
| `/health` comes from the boot bundle, with a readiness check per dependency | [startup defaults](../../backend/dotnet/shapes/service/platform/startup/startup-defaults.md#health) |
| failures leave as ProblemDetails; handlers return `AppResult` | [problem details](../../backend/dotnet/shapes/service/platform/responses/problem-details.md) |
| controller JSON comes from `AddControllersWithSdkJson()` | [serialization](../../backend/dotnet/shapes/service/platform/responses/serialization.md#wiring) |
| time comes from `TimeProvider` | [time](../../backend/dotnet/core/mla/components/time.md) |
| schema changes run through migrations stamped with the product version | [migrations](../../backend/dotnet/core/mla/domains/persistence/migrations/migrations.md) |

---

## Frontend

| Check | Owner |
|---|---|
| Vue 3, strict TypeScript, Vite, Tailwind v4, on a published `@wow-two-beta/ui-vue` | [frontend standard](../repo-conventions.md#frontend-standard) |
| a pnpm workspace with the app at `apps/web/`, one lockfile, a pinned `packageManager` | [workspace](../../frontend/shapes/app/architecture/workspace.md) |
| `src/` holds the five layers, each sliced by domain | [architecture](../../frontend/shapes/app/architecture/architecture.md) |
| layer and slice boundaries are linted and tested | [architecture](../../frontend/shapes/app/architecture/architecture.md#layers-required) |
| files are PascalCase, folders camelCase | [naming](../../frontend/core/lla/notation/naming/naming.md) |
| `bootstrap/index.css` imports Tailwind and the SDK tokens at the right `@source` depth | [styling](../../frontend/shapes/app/platform/styling.md) |
| colour mode runs through `ColorModeProvider`, with a pre-paint `theme.js` | [styling](../../frontend/shapes/app/platform/styling.md#colour-mode) |
| `index.html` carries the head, a favicon and the touch icon | [document](../../frontend/shapes/app/platform/document.md) |
| one `AppLayout` built from `AppShell` and `Navbar`; version in the bar | [shell](../../frontend/shapes/app/shell/shell.md) |
| the router comes from `createAppRouter`; not-found, guards and titles are declared | [routing](../../frontend/shapes/app/routing/routing.md) |
| icons come from `lucide-vue-next` alone | [lucide](../../frontend/core/mla/domains/icons/lucide/lucide.md) |
| each wait uses its loading surface; the first load has a splash | [feedback](../../frontend/core/mla/components/feedback/feedback.md#loading) |
| notices render through one `FeedbackToastHost`; a defect failure offers Report | [feedback](../../frontend/core/mla/domains/feedback/feedback.md) |
| an expected request failure returns a `Result`, never a throw | [state and data](../../frontend/core/mla/domains/data/state-and-data.md#transport) |
| HTTPS dev server on its ledger port, `/api` proxied, an HTTP fallback | [dev server](../../frontend/shapes/app/platform/dev-server.md) |
| no app-local wrapper over an SDK primitive | [extract, keep, remove](../../sdk-extraction.md#remove) |

---

## Deployment

| Check | Owner |
|---|---|
| `engineering/deployment/deploy.yml` describes every service | [deploy descriptor](../../../deployment/descriptor/deploy-descriptor.md) |
| `publish-docker-image.yml` calls the shared workflow at a tag | [deploy descriptor](../../../deployment/descriptor/deploy-descriptor.md#ci-workflow) |
| `ci.yml` builds and tests on every push | [repo structure](repo-structure.md#layout) |
| the SPA builds into `apps/web/dist` and reaches `wwwroot/` through `BuildSpa` | [single-host serving](../../../deployment/hosting/single-host-serving.md) |
| the host serves the SPA through the SDK's `SpaHosting`, not hand-wired static files | [single-host serving](../../../deployment/hosting/single-host-serving.md#backend-serving) |
| CI injects the version; no file declares it | [versioning](../versioning/versioning.md#source) |
| the running version shows in the app and on `api/system/status` | [versioning](../versioning/versioning.md#reporting) |

---

## Design

| Check | Owner |
|---|---|
| the design spec sits at its path and opens with `## Screens` | [design conventions](../../../design/design-conventions.md#per-app-specs) |
| every declared screen class is laid out and verified | [responsive](../../frontend/shapes/app/responsive/responsive.md) |
| screens carry only the copy that changes what the reader does | [UI copy](../../../design/content/ui-copy.md) |
| a platform app's logo follows the family system | [logo system](../../../design/identity/logo-system.md) |

---

## Principles

| Check | Owner |
|---|---|
| nothing registers, subscribes or wires itself | [product principles](../../../conventions.md#product-principles) |
| no ad, nag, engagement prompt or unrequested email | [product principles](../../../conventions.md#product-principles) |
