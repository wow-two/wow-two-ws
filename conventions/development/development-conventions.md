# Conventions — Development

*Last updated: 2026-06-09*

> The **development** domain: how we structure repos and write code. Lookup table, not auto-loaded.
> Each area has its own `{area}-conventions.md` index.

| Area | Covers |
|---|---|
| [repo/](repo/repo-conventions.md) | Repo shape — layout & naming ([repo-structure](repo/repo-structure.md)) · tech stack · ports |
| [backend/](backend/backend-conventions.md) | .NET code style — documentation, code-org, entities, enums, services, architecture, db, API, launch-profiles |
| [frontend/](frontend/frontend-conventions.md) | React / TS code style — naming, components, hooks, forms, state/data, styling, project-structure |

Versioning moved to the sibling **planning** domain → [`../planning/`](../planning/planning-conventions.md).

## Using & evolving conventions

- develop **against** the conventions — read the relevant one before / while writing the code, and follow it
- found a gap or a clearly better way? don't silently diverge — implement, then **propose the convention add / update with the reason(s)**, after the implementation
- the convention change rides in with the work that motivated it — so we keep shipping while closing convention gaps
