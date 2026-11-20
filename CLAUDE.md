# WoW 2.0 — Workspace Root

Full-stack .NET + Vue developer ecosystem. `wow-two-ws` is a meta-repo (workspace config only); managed repos are independent gits under `workbench/` (gitignored as a whole). Shared conventions load from `~/.claude/CLAUDE.md` -- `agentic-workflow.md` is the main workflow here; `.claude/rules/` holds workspace overrides, reinforced by local hooks.

## Conventions

- Touching code, repo structure, naming or versioning → read **`conventions/conventions.md` first** (the index to every convention), then open only the file you need -- never pre-read, never skip
- A convention applies to every repo; a repo's own `CLAUDE.md` / `.claude/rules/` overrides it for that repo
- Frontend selection, React migration and exceptions → [frontend standard](conventions/development/repo/repo-conventions.md#frontend-standard)

## SDK doctrine — build the whole vector

- A product's need is the **trigger** to build a vector, **not** its scope: ship the product's slice, then complete the whole vector in a dedicated pass so the next product finds it there; a known domain (forms, validation, auth, tables) is built proactively -> `conventions/development/dev-cycle.md` § *Vector completeness* (be and fe SDKs)
- **The SDK is ours, and breaking it is cheap.** A product blocked on a missing or wrong SDK API fixes the SDK, never works around it: commit the SDK change, push when its push flag is ON (main CI bumps and publishes), re-pin the product -> § *SDK change loop*; domain repos (Identity first) follow it -> [domain structure](conventions/development/repo/structure/domain-structure.md)
- After every core SDK push, wait for CI's release commit and `git pull --ff-only` before the next commit there -> § *SDK release sync*
- Breaking changes in the SDKs and products, their data included, are allowed whenever they improve something while products have no external users -> [breaking changes](conventions/development/breaking-changes.md)

## Layout

```
CLAUDE.md · catalog.yml (every wow2 repo and app; the wow2 hub) · .claude/repo-registry.md (generated lazy index of every hub) · .claude/rules/ (auto-load: response-style · behavior-rules) · .claude/templates/ · .claude/skills/ · conventions/ (how we build)
docs/ (strategy, playbooks) · system/sessions/ · ideas/ · scripts/ · workbench/ (all repos, gitignored)
```

## Orgs & repos

- 8 orgs, folder = org name: `wow-two` (core) · `-meta` (off-ecosystem) · `-platform` (infra) · `-sdk` (public libs) · `-sdk-beta` (beta libs) · `-kb` (knowledge base) · `-apps` (products) · `-games` (games platform)
- Source: `catalog.yml` -- every wow2 repo and app, one entry per product; ventures and Ocharo keep their own hub catalogs ([catalog](conventions/development/repo/catalog/catalog.md)); `.claude/repo-registry.md` is generated from all three by `scripts/gen-repo-registry.py`
- Ventures, client work and Ocharo sit in the owner folders `workbench/maxs-projects/` · `workbench/mfts-projects/` -- [workbench layout](conventions/development/repo/layout/workbench-layout.md)

## Sessions

- Durable work → `system/sessions/{name}/`: read `context.md` first (state), `session-{name}.md` for the procedure; update `context.md` at milestones and keep it compact (git log is the journal)

## Working rules

- 2–3 related repos per session; updating a lib → check its consumers for breaking changes
- Each repo's own `CLAUDE.md` overrides this root; conventional commits (`feat` / `fix` / `docs` / `refactor`)
- Passive language -- describe where things are; never instruct to pre-read
- **Git:** per-repository flags in the workspace store `.claude/git-flags.json` -> [shared git flags](/Users/max/.claude/conventions/git.md#repository-commit-permission); local adapter [repository git flags](.claude/commit-permission.md); protocol `conventions/development/repo/version-control/git.md`
- **No `README.md` below a repo root** -- folder lead docs are `{folder}.md` (`Data/Migrations/migrations.md`) -> `conventions/development/repo/structure/repo-structure.md` § *Documents*; exception: a declared NuGet `PackageReadmeFile` and an npm `README.md` beside `package.json`
- Live state and roadmap: `workbench/wow-two/wow-two.refinement`; platform app order: `docs/platform-apps.md` (Wheelhouse, Identity, Files, then top down); venture product order: `system/planning/pln-tasks.md` § *Venture product order*

## Agentic workflow (parallel chats)

Many chats and agents edit the **same working tree on one branch** at once; `conventions/agentic-workflow/agentic-workflow.md` adds the rules for that.

- **Assume existing changes are intentional** -- another lane's in-flight or crashed work; a change that looks incomplete or out of scope is **not yours to revert**
- **Never** `git checkout -- .` / `restore` / `stash` / `reset --hard` to clean up changes you didn't author -- unexpected changes → **stop and ask the human**
- **Stay in your lane** -- edit only your allowlisted files; a build break rooted outside your lane is a hand-off (stop and report), not a repair; deleting projects or editing `.sln` / `.csproj` is not a controllers or frontend lane's job
