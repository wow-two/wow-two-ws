# Git

*Last updated: 2026-09-12*

> Commit-message format **and** the agent⇄human commit protocol, for every repo under `wow-two-ws/`.
> Purpose — a uniform, scannable history whose subject reads as *what changed* (past tense); and one unambiguous rule for who publishes (the human, always).

## Shared defaults

Message format, type vocabulary, cohesive scope and index operations: [personal Git conventions](/Users/max/.codex/conventions/git.md).

---

## Large files

A binary in git is permanent. Every later version of it stays in the pack forever, and every clone pays for all of them. The decision is made **before the first commit that introduces it**, because after the first push the only fix is a history rewrite.

Route a file over **1 MB** by asking one question — *can it be regenerated?*

| The file | Route |
|---|---|
| Regenerable from a script in the repo (a bake, a build, a dump) | gitignore it; the script is the source of truth |
| Regenerable, but the product promises a clone that runs with no bake and no network | **LFS** |
| Not regenerable — a supplied export, a licensed asset, a captured fixture | **LFS** |
| Text that diffs and compresses — `.sql`, `.csv`, `.jsonl`, `.json` | plain git, whatever the size |
| Under 1 MB | plain git — LFS is not worth its client dependency at that size |

- must run `git lfs install` and `git lfs track` **before** staging the file, never after — `.gitattributes` only governs what has not been committed yet
- must commit `.gitattributes` in the same commit as the first tracked binary
- must track by extension, not by path — `*.pmtiles`, not `public/tiles/*.pmtiles`; a moved file silently leaves LFS otherwise
- must state the LFS requirement in the repo `README.md` — a clone without `git-lfs` checks out **pointer text**, and the failure is silent until something reads the file
- must watch the GitHub free tier — 1 GB storage and 1 GB/month bandwidth per account, and every CI checkout spends bandwidth
- should keep a large artefact out of git entirely when a release asset or an object store will do — LFS is the answer when the file must be *in the tree*, not merely *available*

Repairing a binary already in pushed history:

- must treat it as a rewrite, never a `.gitattributes` add — the blobs are in the pack and adding a pattern changes nothing
- must run it **before parallel lanes open** — a rewrite mid-flight strands every other chat's local branch
- must expect every SHA from the first affected commit onward to change, and must re-point the commits cited in the repo's own docs
- must measure first — `git lfs migrate info --everything --above=1MB` names the patterns and their weight
- the rewrite itself is `git lfs migrate import --everything --include="…"` followed by a force-push, and it is the **developer's** to run (see *Discipline*)
- must run **`git lfs checkout`** after the migrate — it leaves every tracked file in the working copy as a 133-byte pointer, and nothing warns you; the app 404s its own assets until the smudge runs
- must not trust a backup ref through a rewrite — `--everything` rewrites `backup/*` too, and a following `gc --prune=now` deletes the originals; clone the repo elsewhere first if a rollback is wanted
- must re-point every commit SHA the repo's own docs cite — map old to new by commit subject, `git log --oneline --grep`

---

## Discipline

- **must not** ever run `git push` (every form, force included), `git reset --hard`, `git restore` to the worktree, `git checkout -- <path>`, `git clean`, or any `gh` write (`pr create`, `issue comment`, `release create`, `api -X POST`, …) — the human is the **only** one who publishes, and no agent discards a working tree. Enforced by the `guard-git` PreToolUse hook ([../../../../.claude/hooks/guard-git.py](../../../../.claude/hooks/guard-git.py)).
- **may** run `git add`, `git commit` (plain — **not** `--amend`), `git pull`, `git stash`, branch create / switch, `git fetch`, and every read-only git. Commits require user authorization; approval to commit a scoped batch covers its constituent commits without repeated confirmation.
- history rewrites — `merge`, `rebase`, `cherry-pick`, `revert`, `commit --amend`, soft/mixed `reset` — are blocked unless a **rapid-building session** is live: `.claude/.rapid-build` holding one future ISO-8601 UTC expiry (`2026-08-13T18:30:00Z`). The developer writes that marker; agents never create it, and an expired one is no session.
- **lane check** — `commit`, `pull` and `stash push` stop once, naming the files, when the tree carries modified / staged paths this session never wrote. That is probably a parallel chat's in-flight work. Ask the developer *is another lane working right now?*; if none is, the dirt is completed-but-uncommitted work and the retry goes through. The hook knows "this session wrote it" from the ledger `.claude/hooks/track-touch.py` keeps.
- may stage and unstage explicit task paths; prefer `git restore --staged -- <paths>`. Index-only path resets and cached patches/removals are permitted without a rapid-building marker.
- must follow the authorized task scope and handover cadence; an agreed batch iteration does not require repeated staging approval.
- must treat "push it" as a cue to propose the file set and message; it authorizes neither staging nor publishing; "commit this" authorizes the commit once the staged set has been reported.
- parallel-lane rules (assume-intentional · no-revert · stage only your own files): [../../../agentic-workflow/agentic-workflow.md](../../../agentic-workflow/agentic-workflow.md).

---

## Protocol (agent ⇄ human)

Per commit, in this order:

1. within the authorized task scope, agent **carves the index** using explicit paths. Stage and unstage task-owned paths as needed; preserve unrelated staged work.
2. agent prints the **staged path list** + the commit message (`{type}: {past-tense} {what}`).
3. agent commits within the developer-authorized scope; the human reviews and pushes — `git push` is never the agent's.
4. an agreed batch iteration authorizes subsequent batches; wait for the human commit when that is the requested cadence.

- **carve** = shape the index so the staged set is exactly one lane's cohesive change, nothing else.
- read the result with `git status --short` — staged column commits, unstaged column stays behind.
- may `git add -A` / `-u` / `.` — a pathless add requires the entire resolved file set to be within the authorized scope: it copies into the index and is trivially reversible, changing no working-tree content. The risk is the **commit** that follows, which would claim another lane's work as this lane's — and that is what the lane check above stops, by name, before the commit lands.
- must print the staged paths, not only the message — a shared index makes the message alone unprovable.
- must re-check `git status` right before printing — a concurrent lane can stage between add and report.
- must preserve another lane's prepared commit unless the user authorizes changing that staged set.
- found foreign paths staged → report them; don't quietly unstage.
- must keep each commit buildable where practical; flag a split that can't be (e.g. rename-only) before staging.
