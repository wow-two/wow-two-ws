# Agentic workflow

*Last updated: 2026-10-01*

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

## Handoff docs — write-once, read-once, delete [REQUIRED]

A handoff (`handoff.md`) exists for exactly one purpose: **loading a fresh chat with the context the previous chat is about to lose.** It is a courier, not a record. The version doc and the backlog are the record ([version-track.md](../planning/version-track/version-track.md)).

- must write it only when a chat is ending with work in flight, and only for the chat that picks that work up.
- must not maintain it. A handoff updated turn by turn has become a second plan doc, and it will disagree with the version doc — the numbering drift that produced a phantom "Iteration 7.5" started exactly this way.
- **the chat that loads a handoff owns its disposal.** On load: move anything durable into the version doc, the backlog or the architecture docs (a settled fork, a measured figure, a trap worth keeping), then **delete the file**. Everything else was transport.
- must not let two chats load the same handoff. Once read, it is spent; a second reader is reading a stale snapshot of a tree that has moved.
- must delete it on load when nothing in it is durable — a handoff carrying only what the version doc already says has already done its job, and keeping it guarantees a later reader trusts the older of two records.
- must never cite a handoff as the source of a decision. If a decision only lives there, it was never recorded — move it first.

**Precedence:** version doc > handoff, always. A handoff that contradicts the version doc is wrong by definition, whichever is newer.

Distinguish it from the version-track's **transient iteration plan** (`v{X.Y}/{iter-slug}.md`), which is also delete-when-done but serves the *current* chat's own build, not the next chat's start.

---

## Commit discipline

- must stage, commit and push per [git](../development/repo/version-control/git.md) § *Protocol*; the repository
  git flags decide who commits and who publishes.
- must treat the index as shared — one per repo, not per lane; two agents staging at once produce one index
  holding both.
- must report foreign staged paths and preserve them; the lane check and the unstaging rules are
  [git](../development/repo/version-control/git.md) § *Discipline*.
- must flag large uncommitted work in a shared tree for a commit — a later agent or a careless revert can lose it.
