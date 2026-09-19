# Agentic workflow

*Last updated: 2026-09-12*

> How parallel Claude chats / agents share one repo without clobbering each other — lane discipline, no-revert, scope containment.
> Purpose — multiple chats edit the same working tree at once; a wrong "cleanup" silently destroys another lane's uncommitted work.
> Use case — reach for this before spawning agents, before touching a tree you didn't just create, and any time you find unexpected changes.

## One tree, many lanes

- Repos are gitignored independent gits; multiple chats / agents operate on the **same working tree, on a single branch, at the same time**.
- **No worktrees** — don't `git worktree add` per agent. Coordinate by splitting files, not trees (worktree sprawl + duplicate `node_modules` + stale branches outweigh the isolation).
- Split work so concurrent agents touch **disjoint file sets** (different projects / folders / layers). Two agents on one file is the thing to design out, not manage.

---

## Assume existing changes are intentional

- A working tree you didn't just clean is **presumed to hold another lane's in-flight work**. Uncommitted ≠ scratch.
- A change that looks **incomplete, out-of-scope, or "wrong"** is **another agent's lane** or a crashed run mid-task — **not yours to revert**. Assume necessary until the human says otherwise.
- **Never** `git checkout -- .`, `git restore` to the worktree, `git stash`, `git reset --hard`, or delete files to "tidy" changes you didn't author — these silently destroy uncommitted work.
- Found unexpected changes? **Stop and verify with the human** before any destructive op. Provenance by mtime / log is **unreliable** when chats run concurrently (one chat's edit lands inside another's window) — ask, don't infer.

---

## Stay in your lane

- An agent edits **only its assigned files** — state the allowlist in its brief; everything else is read-only to it.
- A build / test failure rooted **outside your lane** → **STOP and report it** as a hand-off; don't "fix" it by editing or deleting another lane's files. A blocked `Api` build because a *library* changed is someone's hand-off, not your repair job.
- Deleting a project, editing a `.sln` / `.csproj`, or rewiring DI is almost never a presentation / frontend lane's job — if your task seems to need it, it's the wrong lane: stop and flag.

---

## Commit discipline

- Commits follow the [Git permission protocol](../development/repo/version-control/git.md); agents stage, and the developer always publishes.
- **The index is shared, one per repo — not per lane.** Two agents staging at once produce one index holding both. Stage and unstage only within the authorized task scope; an agreed batch iteration remains authorized.
- A pathless `git add -A` / `-u` / `.` is fine — staging only copies into the index and is trivially reversible; it changes no working-tree content. The hazard is the **commit** after it, which would ship another lane's work under this lane's message. The `guard-git` lane check stops `commit` / `pull` / `stash push` and names the foreign files before that happens; answer its question and re-run.
- Unstage task-owned paths with `git restore --staged -- <paths>` when needed. Foreign paths already staged → report and preserve unless the user authorizes changing them.
- Large uncommitted work in a shared tree is **fragile** — flag it for the human to commit so a later agent (or a careless revert) can't lose it.
