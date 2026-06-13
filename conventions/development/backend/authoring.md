# Authoring conventions

*Last updated: 2026-06-13*

How to write a convention doc under `conventions/development/backend/**`. The rules here bind every other
doc in this tree and the output of the `create-repo` skill.

## Cite symbols + paths, never namespaces

A convention references the **exact symbol** — interface / class / method / type — and/or the **file path**.
It never names a namespace or package id.

- ✅ `IKeyedEntity<TId>`, `AddSqlMigrations`, `MigrationDescriptor`, `Result<T>.Fail`, `Migrations/NNN-name/Apply.sql`
- ✗ "the `Data.Abstractions` package", "types under `…Data.Dapper`", "the migrations namespace"

**Why:** namespaces and package ids go stale on every refactor or mono-lib collapse (the backend-beta SDK just
collapsed per-concern csprojs into a mono-lib while keeping namespaces — proof they are unstable). A reader greps
the symbol and finds it wherever it now lives.

## Symbol format

- Backtick every symbol. Include generic arity / params exactly as in source: `IKeyedEntity<TId>`,
  `IPipelineBehavior<TRequest,TResponse>`, `AddEntityFrameworkCore<TContext>`.
- For members use `Type.Member`: `MigrationOptions.AllowRollback`, `DomainError.NotFound`, `Result<T>.Ok`.
- Point at on-disk layout (`SqlFiles/Migrations/{NNN}-{name}/{Apply,Rollback}.sql`,
  `Api/Configurations/HostConfiguration.Extensions.cs`, `Properties/launchSettings.json`) over prose locations.

## Verify before you cite

Before citing a symbol, grep the source for it. If it appears only in a README / spec but not in `.cs`
(e.g. an aspirational `ErrorOr<T>`), **do not codify it** — cite the implemented symbol and flag the doc drift.

## Supersede, don't stack

When a cited symbol replaces an older pattern, update the old doc's note in the same pass rather than leaving
both live (e.g. the per-enum `MapEnum<T>`-twice note was superseded by `MapEnums` and had to be rewritten, not
left beside it).

## Doc shape

- `# Title` → `*Last updated: YYYY-MM-DD*` → one-line purpose → `##` sections → `## See also` with relative links.
- Deliverable-grade structure: tables for 3+ parallel items, short code fences, dense bullets — not prose.
- `README.md` lives **only** at a repo root (see [repo-structure.md](../repo/repo-structure.md) §3); a folder's
  lead doc is named `{folder}.md`, never `README.md`.

## Scope

Applies to every doc under `conventions/development/backend/**`. A repo-level `CLAUDE.md` / `.claude/rules/`
overrides per repo.

## See also

- [backend-conventions.md](backend-conventions.md) — the backend index (sub-domains)
- [repo-structure.md](../repo/repo-structure.md) — folder-docs rule (no `README.md` below root)
- [documentation.md](code-style/documentation.md) — XML doc-comment format (the in-code counterpart)
