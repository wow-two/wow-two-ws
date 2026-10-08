# Conventions — Development — Repo

*Last updated: 2026-10-01*

> How a repo is shaped and equipped — repo **shape** splits by **archetype** (product / venture vs SDK / library),
> grouped under `structure/`; version control + the default tech stack are the shared, cross-archetype setup. Code
> style for each stack is in the siblings [../backend/](../backend/) + [../frontend/](../frontend/). Serving + dev-port
> allocation are a deployment concern → [../../deployment/deployment-conventions.md](../../deployment/deployment-conventions.md).

## Structure

Repo shape by archetype — product / venture (both stacks, one repo) vs SDK / library (one published package). Don't force one shape into the other.

| File | Covers |
|---|---|
| [structure/repo-structure.md](structure/repo-structure.md) | Product / venture — `product/` + `engineering/`, code under `engineering/codebase/`, slug, lead docs, naming, tests, deployment files |
| [structure/product-conformance.md](structure/product-conformance.md) | Product / venture — every check a product repo owes, each linked to its owning convention |
| [structure/sdk-structure.md](structure/sdk-structure.md) | SDK / library — `engineering/` + npm package nested under `engineering/codebase/{slug}/`, `src/` source-only + `tests/{unit,stories}`, config repoint, dist-only publish |

---

## Version control

| File | Covers |
|---|---|
| [version-control/git.md](version-control/git.md) | Commit messages, scoped index handover, independent repository Git flags and large-file handling |

---

## Versioning

| File | Covers |
|---|---|
| [versioning/versioning.md](versioning/versioning.md) | The product version — `X.Y` from the version track, `Z` from CI, injected into builds, reported by services and shown in apps |

---

## Tech stack

> The default stack for wow-two product / venture repos; an SDK repo runs the same floor. Code-style per layer: [../backend/](../backend/) · [../frontend/](../frontend/).

- **Backend** — .NET 10 · ASP.NET Core · EF Core · MediatR (CQRS) · Clean Architecture. DB: SQLite (single-user / POC) → Postgres (when scaling / multi-instance). CI: GitHub Actions → GHCR.
- **Frontend** — [frontend standard](#frontend-standard).
- **Beta SDKs** — consume these first; build-locally-then-migrate if a capability is missing.
  - frontend package and framework selection → [frontend standard](#frontend-standard).
  - `WoW2.Sdk.Backend.Beta` (nuget.org; namespace `WoW.Two.Sdk.Backend.Beta`) — hosting, observability, mediator, data.

---

## Frontend standard

- must use Vue 3, strict TypeScript, Vite and Tailwind v4 for new product frontends and UI work.
- must build reusable frontend capabilities in `@wow-two-beta/ui-vue`; products consume its public exports.
- must follow [Vue constructs](../frontend/core/lla/constructs/vue/vue.md) and the shared frontend conventions.
- must use `lucide-vue-next` as the icon set ([lucide](../frontend/core/mla/domains/icons/lucide/lucide.md)).
- must treat existing React frontends and `@wow-two-beta/ui` as legacy migration targets.
- may maintain existing React behavior while its product's explicitly scoped Vue migration remains incomplete.
- must implement new frontend features and SDK capabilities on the Vue track.
- must obtain an explicit user decision for a temporary React exception, naming its repository and scope.
- must record that exception and its migration exit condition in the repository's planning track.
- must not infer an exception from existing React code, examples, templates, skills or stale repository instructions.
- must preserve required React behavior until the replacement's scoped verification passes.
- must not treat this framework decision as authorization to delete a product or execute an unscoped migration.

### Scaffolding

- must apply this standard and the [frontend workspace](../frontend/shapes/app/architecture/workspace.md)
  when using `create-repo`.
- must validate the template's Vue app and workspace layout before copying it as a conformant starter.
- must verify the generated Vue workspace before reporting a new frontend scaffold complete.
