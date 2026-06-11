# Conventions — wow-two

*Last updated: 2026-06-10*

> **The single index to every convention.** When a task touches *how we build* — code, repo structure,
> naming, versioning — search HERE first, then open only the file(s) you need. Lookup table,
> **not auto-loaded**; do not pre-read the targets. Area indexes are named `{area}-conventions.md`; this is the root.

## How to use

1. Find what the task touches below.
2. Open that ONE file (leaf files live in the area sub-folders).
3. A repo-level rule (`workbench/{repo}/CLAUDE.md` or `.claude/rules/`) **overrides** a convention for that repo.

## Domains

| Domain | Covers | Status |
|---|---|---|
| **development** (below) | how we build — repo shape, backend & frontend code style | Active |
| **planning** (below) | how we plan — version docs (grows over time) | Active |
| deployment | VPS, Docker, Traefik, CI/CD, release | Planned |
| security | secrets handling, auth patterns, threat model | Planned |

---

## development — index: [development/development-conventions.md](development/development-conventions.md)

### repo/ — repo shape & setup · [repo-conventions.md](development/repo/repo-conventions.md)

| Need | File |
|---|---|
| Repo layout · `product/` + `engineering/` · code under `engineering/codebase/{backend,frontend}-services` · naming · folder-docs (no README below root) · archetypes · **audit** | [development/repo/repo-structure.md](development/repo/repo-structure.md) |
| Tech stack — backend + frontend + beta SDKs | [development/repo/tech-stack.md](development/repo/tech-stack.md) |
| Port ledger — allocated dev ports | [development/repo/ports.md](development/repo/ports.md) |

### backend/ — .NET code style · [backend-conventions.md](development/backend/backend-conventions.md)

`documentation` · `code-organization` · `models` · `entities` · `enums` · `services` · `clients` · `settings` · `result-pattern` · `service-architecture` · `domain-structuring` · `host-configuration` · `database` · `data-access` · `api-endpoints` · `launch-profiles`

### frontend/ — React / TS code style · [frontend-conventions.md](development/frontend/frontend-conventions.md)

`naming` · `documentation` · `code-organization` · `models` · `enums` · `components` · `hooks` · `extensions` · `forms` · `project-structure` · `state-and-data` · `styling`

---

## planning — index: [planning/planning-conventions.md](planning/planning-conventions.md)

| Area | File |
|---|---|
| Version docs — naming, lifecycle, cadence + iteration template | [planning/version-planning/version-docs.md](planning/version-planning/version-docs.md) |
| Engineering planning — repo roadmap + backlog | [planning/engineering-planning/engineering-planning-conventions.md](planning/engineering-planning/engineering-planning-conventions.md) |

## Scaffolding

- New conformant repo → skill **`create-repo`**. Template repo: `workbench/wow-two-sdk-beta/wow-two-sdk-beta.product-template/`.

## Precedence

A convention applies to **every** repo under `wow-two-ws/`; a repo-level rule overrides for that repo. The SDK's own `docs/conventions/` covers SDK-package concerns (naming, layout, registry) — no overlap.
