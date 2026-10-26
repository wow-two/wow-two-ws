# Domain structure

*Last updated: 2026-10-26*

> Shape of a domain repo — one SDK domain's be packages, fe package, service and image in one repo: when a domain
> earns one, naming, layout, layers, docs and releases.
> Use case — splitting a domain out of core, scaffolding its repo (Identity, File Storage), or placing a package in it.

Evidence and the options weighed → [SDK breakdown](../../../../ideas/identity-analysis-2026-10/t5-sdk-breakdown.md) ·
[library architecture](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.identity/blob/main/engineering/research/identity-analysis-2026-10/t7-library-architecture.md) ·
[library template](../../../../ideas/identity-analysis-2026-10/t8-library-template.md).

---

## Scope

- must give a domain its own repo when it falls under [capability forms](../../capability-forms.md#scope) and has a
  broker contract to version.
- must split it from core only once core's own code reads nothing of it but [kernel](#kernel) seams.
- must keep a stateless library with heavy dependencies and no contract — media, codes, AI providers — in the core
  repo as a companion package.
- must treat a domain repo as an archetype of its own, whatever its org; [SDK structure](sdk-structure.md) governs
  package-only repos.
- must follow [repo structure](repo-structure.md) wherever this doc states no delta.

---

## Naming

| Part | Pattern | Identity |
|---|---|---|
| repo | `{org}.{slug}` | `{org}.identity` |
| code dirs | `{slug}.backend-services/` · `{slug}.frontend-services/` | `identity.backend-services/` |
| NuGet package | `WoW2.Sdk.Beta.Be.{Domain}.{Layer}` | `WoW2.Sdk.Beta.Be.Identity.Abstractions` |
| namespace root | `WoW.Two.Sdk.Beta.Be.{Domain}` | `WoW.Two.Sdk.Beta.Be.Identity` |
| npm package | `@wow-two-beta/fe-{slug}` | `@wow-two-beta/fe-identity` |

- must name the repo per [ecosystem naming](repo-structure.md#ecosystem-naming); its org is `wow-two-sdk-beta`, which also owns the image.
- must derive `{slug}` per [repo structure](repo-structure.md#slug), and `{Domain}` as its PascalCase brand —
  `file-storage` → `FileStorage`.
- must name each NuGet package `WoW2.Sdk.Beta.Be.{Domain}.{Layer}`, with `{Layer}` from [Layers](#layers).
- must root every package's namespaces at `WoW.Two.Sdk.Beta.Be.{Domain}`.
- must keep the namespace of code moved out of core, so consumers change no `using`.
- must publish one npm package per repo, named `@wow-two-beta/fe-{slug}`.

---

## Layout

```
{org}.{slug}/
├── README.md · CLAUDE.md · LICENSE            root only
├── .github/workflows/
│   ├── publish-docker-image.yml               the image, through the shared delivery workflow
│   ├── publish-packages.yml                   NuGet and npm, versions from tags
│   ├── core-latest.yml                        compat job against the newest core
│   ├── conformance.yml                        the contract suite against the released image
│   └── codeql.yml
├── product/                                   spec, state, features, flows, brand
└── engineering/
    ├── architecture/                          architecture.md · contract.md · package-registry.md · decisions/
    ├── scripts/                               release helpers publish-packages.yml calls
    ├── deployment/                            deploy.yml · Dockerfile · docker-compose.yml
    └── codebase/
        ├── {slug}.backend-services/
        │   ├── {Domain}.BackendServices.slnx · Directory.Build.props · Directory.Packages.props
        │   ├── packages/{Layer}/              one packable project per package
        │   ├── service/{Domain}.Api/          the deployable host
        │   └── tests/{Domain}.Tests.{Tier}/
        └── {slug}.frontend-services/
            ├── packages/fe-{slug}/            the npm package
            └── apps/web/                      hosted pages and the admin console
```

- must keep the [repo structure](repo-structure.md#layout) shell; the tree marks what a domain repo adds inside it.
- must list every artifact — NuGet ids, the npm package, the image — with its install line in the root `README.md`.
- must keep one `LICENSE` at the root; the packages' license metadata and the fe package's copy match it.

---

## Docs

- must keep a domain's spec, research and planning in its repo from the day the repo exists.
- must write the spec as `product/product.md`; a feature group grows into `product/features/{feature}.md`.
- must keep the domain's state and decision log in `product/context.md`.
- must document the contract in `engineering/architecture/contract.md`.
- must list the domain's packages, their layers and consumers in `engineering/architecture/package-registry.md`.
- must file an analysis batch, its decision queue included, in `engineering/research/{slug}-analysis-{yyyy-mm}/`.
- must plan in `engineering/planning/` per the [version track](../../../planning/version-track/version-track.md).
- must keep in the hub only the `catalog.yml` entry, the `docs/platform-apps.md` row and cross-capability decisions in
  `docs/platform-decisions.md`.
- must link the repo's `product/product.md` from the platform-apps row.
- must not copy spec text into the hub.
- must start a spec as the hub's `ideas/{slug}-service-spec.md` while no repo exists.
- must move the spec and its analysis batch into the repo in the repo's first docs commit.
- must delete the hub copies in the same pass and update every inbound link.
- must move a domain's research out of a core repo into the domain repo; core's package registry keeps a pointer row.
- must cite a hub document from the repo as `wow-two-ws/…` path text, never as a relative link.

---

## Backend

- must place each packable project in `packages/{Layer}/`, its package `README.md` beside the csproj.
- must place the deployable host in `service/{Domain}.Api/`.
- may add `service/{Domain}.Application/` and `service/{Domain}.Infrastructure/` once admin use cases need them.
- must not give the service a Domain or Persistence project; the domain's store ships in its packages.
- must build the service from the repo's own packages by `ProjectReference`, never by a published version.
- must make `packages/*` packable and `service/`, `tests/` not packable, by path in `Directory.Build.props`.
- must group the solution in the virtual folders `Packages/`, `Services/` and `Tests/`
  ([solution organization](../../backend/dotnet/shapes/service/architecture/architecture.md#solution-organization)).
- must name test suites per [service testing](../../backend/dotnet/shapes/service/architecture/clean/testing.md#layout);
  the capability's conformance suite is `{Domain}.Tests.Conformance`.

---

## Frontend

- must place the npm package in `packages/fe-{slug}/`.
- must build the hosted pages and the admin console as one app, `apps/web/`.
- must shape the package per [SDK structure](sdk-structure.md#tests) § Tests and § Publish.
- must set the package's `repository.directory` to its path from the repo root.
- must let `apps/web` take the package by `workspace:*`, through its `exports` only.
- must not import `apps/` from the package.
- must keep session and transport strategies (`auth`) in the fe sdk; the package holds the domain's contract
  models, components and widgets, and can forward a flow to the hosted pages instead of embedding it.
- must ship management screens in the package's `./admin` export; `apps/web` composes them into the console,
  and a central console or a product's own admin page imports the same export.
- must serve `apps/web` from `service/{Domain}.Api` per
  [single-host serving](../../../deployment/hosting/single-host-serving.md).

---

## Layers

| Layer | Package | Holds | References |
|---|---|---|---|
| kernel | `WoW2.Sdk.Beta.Be.Abstractions` | value types contracts share; seams core reads | BCL only |
| core | `WoW2.Sdk.Beta.Be` | infrastructure — web, data, mediator, http | kernel |
| contract | `…{Domain}.Abstractions` | brokers, models, `IEvent` records, constants, errors | kernel |
| edge | `…{Domain}.{Edge}`, optional | the store-less part products use alone | contract, core |
| forms | `…{Domain}.Module` · `…{Domain}.Client` | Form 1 module · Forms 2/3 HTTP client | edge, contract, core |
| extension | `…{Domain}.{Extension}`, optional | heavy adapters; a protocol host | forms, core |
| test kit | `…{Domain}.Testing` | fakes over the contract, personas, conformance base | contract, `…Be.Testing` |
| service | not packed | host, admin, hosted pages | any package above |

- must keep each package to the references its row names.
- must not reference a domain package from the kernel or core.
- must declare the [capability contract](../../capability-forms.md#contract) in `{Domain}.Abstractions`.
- must keep the contract free of a `FrameworkReference` and of third-party packages.
- must keep options binding, DI registration and I/O out of the contract.
- must add the `Microsoft.AspNetCore.App` framework reference to every package that references core
  ([framework references](../../backend/dotnet/shapes/service/platform/build/central-package-management.md)).
- must add an edge only when products use part of the domain without its store.
- must add an extension only to isolate heavy dependencies or a server role.
- must reference another domain's contract from a package, never its implementation.
- must keep references between domain repos one-way; two domains never reference each other.
- must declare a port in the domain's own contract when it needs a capability of a domain that references it; the
  host binds the port.
- must let a product's Domain and Application projects reference contracts only; its composition root picks `Module`
  or `Client`.

---

## Kernel

- must place a seam core and a domain share in the kernel `WoW2.Sdk.Beta.Be.Abstractions`, in the core repo.
- must admit a type only when it is BCL-only and core's own code reads it or the contracts of two repos use it.
- must move a seam core's code reads into the kernel as an interface; its implementation leaves with the domain.
- must keep a moved type's namespace and forward it from core with `TypeForwardedTo`.
- must release the kernel with core, on core's version line.

---

## Core

- must pin core by its published version: `BackendSdkVersion` in `Directory.Packages.props`, an exact
  `@wow-two-beta/fe` in the frontend workspace.
- must peer `@wow-two-beta/fe` from `fe-{slug}` at `>=0.0.n <0.1.0`, with `n` the pinned version.
- must change core first when a domain needs it: release core, re-pin the domain, then change the domain.
- must fix a domain repo from a product chat as the
  [SDK change loop](../../dev-cycle.md#sdk-change-loop--from-a-product-chat) fixes core; the product re-pins after.
- must pin a domain in a consumer through one `{Domain}SdkVersion` property beside `BackendSdkVersion`.
- must run `core-latest.yml` nightly and on dispatch: build and test the domain against the newest be sdk and fe sdk.
- must treat a red compat run as a break to fix in the domain, never as a release gate.

---

## Repository

- must create a domain repo public in its org, with the `create-library` skill (phase 1), never by hand.
- must turn off issues, wiki, projects and discussions.
- must set the workflow token to read-only by default; a workflow raises permissions per job.
- must protect `main` with the `main-guard` ruleset (`scripts/release/main-guard.json` in the hub): no deletion,
  no force push, no review rule.
- must take `origin` from `gh repo clone`; never `git remote add`.

---

## Releases

| Artifact | Line | Tag | Next version from | Workflow |
|---|---|---|---|---|
| NuGet family | `10.y.z-beta` | `be-v{version}` | the newest `be-v*` tag | `publish-packages.yml` |
| `fe-{slug}` | `0.0.z` | `fe-v{version}` | the newest `fe-v*` tag or npm, the higher | `publish-packages.yml` |
| image | `X.Y.Z` | `vX.Y.Z` | [versioning](../versioning/versioning.md) | `publish-docker-image.yml` |

- must release every package of one repo on one version line; each repo keeps its own line.
- must let the version track drive the image only; the package lines ignore it.
- must derive a package version from tags and pass it to the pack step; CI never commits a version.
- must not make a release commit in a domain repo;
  [SDK release sync](../../dev-cycle.md#sdk-release-sync--after-every-push) does not apply to it.
- must gate a package release on the package tests and the in-process conformance suite.
- must push the tag before publishing, so a failed publish burns its number.
- must not create a GitHub Release for a `be-v` or `fe-v` tag.
- must publish packages only from `publish-packages.yml`, by registry trusted publishing; the repo stores no token.
- must keep each publish job disarmed until its registry trusts `publish-packages.yml`.
- must scaffold a domain repo from `wow-two-sdk-beta.domain-template` with `create-repo SHAPE=domain`.
- must create a domain repo and carry it to its first releases with the `create-library` skill:
  `scripts/release/library.py plan` probes each phase and prints the next commands; the agent runs each write alone.

