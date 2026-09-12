# WoW 2.0 — Workspace Root

Full-stack .NET + React developer ecosystem. `wow-two-ws` is a meta-repo (workspace config only); managed repos are independent gits under `workbench/` (gitignored as a whole).

## Instruction sources

General response and collaboration conventions: `.claude/rules/response-style.md` imports the personal shared source. Required instruction files load at startup; indexes and domain content remain on demand.

## Response style

Shared source and workspace overrides: `.claude/rules/response-style.md`; reinforced by local hooks.

## Conventions

- Touching code · repo structure · naming · versioning → read **`conventions/conventions.md` first** (the single index to all conventions), then open only the file you need. Don't pre-read; don't skip.
- A convention applies to every repo; a repo-level `CLAUDE.md` / `.claude/rules/` overrides for that repo.

## SDK doctrine — build the whole vector

- The SDK's main frame: a product's need is the **trigger** to build a vector, **not** its scope. Ship the essential slice for that product, then **complete the whole vector** in a dedicated pass — inventory every capability, build to completeness — so the *next* product finds it already there. A known domain (forms, validation, auth, tables) is built proactively; the real cost is integration, paid once in the SDK. Full rule: `conventions/development/dev-cycle.md` § *Vector completeness*. Applies to both the backend and frontend SDKs.
- **The SDK is ours, and breaking it is cheap.** A product blocked on a missing or wrong SDK API fixes the SDK rather than working around it in the product — add the export, correct the type, widen the prop. Both SDKs are beta-forever; the developer publishes and the consumer re-pins. A workaround in a product is the more expensive outcome, because it hides the gap from every later consumer.

## Layout

```
CLAUDE.md · .claude/repo-registry.md (lazy index) · .claude/rules/ (auto-load: response-style · behavior-rules · templates/) · conventions/ (how we build)
docs/ (strategy, playbooks) · system/sessions/ · ideas/ · scripts/ · workbench/ (all repos, gitignored)
```

## Orgs & repos

- 7 orgs, folder = org name: `wow-two` (core) · `-meta` (off-ecosystem) · `-platform` (infra) · `-sdk` (public libs) · `-sdk-beta` (beta libs) · `-kb` (knowledge base) · `-apps` (products). Full index: `.claude/repo-registry.md`.

## Sessions

- Durable work → `system/sessions/{name}/`: read `context.md` first (state), `session-{name}.md` for the procedure. Update `context.md` at milestones; keep it compact (git log is the journal).

## Working rules

- 2–3 related repos per session. Updating a lib → check consumers for breaking changes.
- Each repo's own `CLAUDE.md` overrides this root. Conventional commits (`feat`/`fix`/`docs`/`refactor`).
- Passive language — describe where things are; never instruct to pre-read.
- **Git:** agents stage and commit; agents **never** `git push` — the developer publishes. The same hook (`.claude/hooks/guard-git.py`) blocks worktree destruction (`reset --hard`, `restore`, `checkout -- <path>`, `clean`) and every `gh` write, gates history rewrites (`merge` / `rebase` / `cherry-pick` / `revert` / `commit --amend` / soft `reset`) behind a rapid-building marker the developer writes, and stops `commit` / `pull` / `stash push` once when the tree holds files this session never wrote — answer its lane question, then re-run. Protocol: `conventions/development/repo/version-control/git.md`.
- **No `README.md` below a repo root.** Folder lead docs use `{folder}.md` (e.g. `Data/Migrations/migrations.md`). See `conventions/development/repo/structure/repo-structure.md` §3. **Exception:** declared NuGet `PackageReadmeFile` and npm `README.md` beside `package.json` are functional package metadata; preserve them as required by SDK structure.
- **Skills** (`.claude/skills/`): `open-active` (open the working set in Rider/WebStorm) · `create-repo` (scaffold a conformant repo).
- **Live state / roadmap:** `workbench/wow-two/wow-two.refinement`.

## Agentic workflow (parallel chats)

> Multiple chats / agents edit the **same working tree on one branch** at once. Full rule: `conventions/agentic-workflow/agentic-workflow.md`.

- **Assume existing changes are intentional** — another lane's in-flight (or crashed-mid-task) work. A change that looks incomplete / out-of-scope is **not yours to revert**.
- **Never** `git checkout -- .` / `restore` / `stash` / `reset --hard` to "clean up" changes you didn't author — it silently destroys uncommitted work. Found unexpected changes → **stop and ask the human**.
- **Stay in your lane** — each agent edits only its allowlisted files; a build break rooted outside your lane is a **hand-off (STOP + report)**, not a repair. Deleting projects / editing `.sln`·`.csproj` is not a controllers / frontend lane's job.
- **No worktrees** — coordinate by disjoint file sets.
