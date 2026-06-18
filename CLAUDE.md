# WoW 2.0 — Workspace Root

Full-stack .NET + React developer ecosystem. `wow-two-ws` is a meta-repo (workspace config only); managed repos are independent gits under `workbench/` (gitignored as a whole).

## Lazy loading

- Don't pre-read or scan at startup — open a file only when the task needs it; read the minimum.
- `.claude/rules/repo-registry.md` and `conventions/conventions.md` are lookup tables, not reading lists.

## Response style

> Highest-priority style rule: **`.claude/rules/response-style.md`** (auto-loaded). Super-compact default — density over length. Runtime-enforced via `.claude/settings.json` hook.

Most-violated cuts (enforce hard; full list lives in that file):

- **No self-narration — pre OR post-action.** Pre: "Let me check…", "I'll search…". Post: "Searched the registry:", "Checked the doc:". Both shapes cut — just give the result.
- **Compact format for analyses / lookups** — `from X:` + bullets over prose.
- **No scaffolding openers / closing recap.** "Looked through…", "So to summarize…" → delete.
- **Imperatives over first-person.** "I'll bump the version" → `Directory.Packages.props:12 → 2.0.0`.
- **Multiple items** (comments / findings / options) → one `###` header each + `---` between groups.

A reply violating any of these is a style miss regardless of correctness.

## Conventions

- Touching code · repo structure · naming · versioning → read **`conventions/conventions.md` first** (the single index to all conventions), then open only the file you need. Don't pre-read; don't skip.
- A convention applies to every repo; a repo-level `CLAUDE.md` / `.claude/rules/` overrides for that repo.

## Layout

```
CLAUDE.md · .claude/rules/ (response-style · repo-registry · behavior-rules · templates/) · conventions/ (how we build)
docs/ (strategy, playbooks) · system/sessions/ · ideas/ · scripts/ · workbench/ (all repos, gitignored)
```

## Orgs & repos

- 7 orgs, folder = org name: `wow-two` (core) · `-meta` (off-ecosystem) · `-platform` (infra) · `-sdk` (public libs) · `-sdk-beta` (beta libs) · `-kb` (knowledge base) · `-apps` (products). Full index: `.claude/rules/repo-registry.md`.

## Sessions

- Durable work → `system/sessions/{name}/`: read `context.md` first (state), `session-{name}.md` for the procedure. Update `context.md` at milestones; keep it compact (git log is the journal).

## Working rules

- 2–3 related repos per session. Updating a lib → check consumers for breaking changes.
- Each repo's own `CLAUDE.md` overrides this root. Conventional commits (`feat`/`fix`/`docs`/`refactor`).
- Passive language — describe where things are; never instruct to pre-read.
- **Git:** only commit/push when explicitly asked — the developer manages git manually.
- **No `README.md` below a repo root.** Only a repo's top-level `README.md` is allowed; every other folder's lead doc is `{folder}.md` (e.g. `Data/Migrations/migrations.md`, not `.../README.md`). See `conventions/development/repo/repo-structure.md` §3. **Exception:** a packable project's NuGet `PackageReadmeFile` README (e.g. `src/README.md` next to the `.csproj`) is a functional package file, not a folder doc — leave it.
- **Skills** (`.claude/skills/`): `open-active` (open the working set in Rider/WebStorm) · `create-repo` (scaffold a conformant repo).
- **Live state / roadmap:** `workbench/wow-two/wow-two.refinement`.

## Agentic workflow (parallel chats)

> Multiple chats / agents edit the **same working tree on one branch** at once. Full rule: `conventions/agentic-workflow/agentic-workflow.md`.

- **Assume existing changes are intentional** — another lane's in-flight (or crashed-mid-task) work. A change that looks incomplete / out-of-scope is **not yours to revert**.
- **Never** `git checkout -- .` / `restore` / `stash` / `reset --hard` to "clean up" changes you didn't author — it silently destroys uncommitted work. Found unexpected changes → **stop and ask the human**.
- **Stay in your lane** — each agent edits only its allowlisted files; a build break rooted outside your lane is a **hand-off (STOP + report)**, not a repair. Deleting projects / editing `.sln`·`.csproj` is not a controllers / frontend lane's job.
- **No worktrees** — coordinate by disjoint file sets.
