# Brief — move one repository onto the version track

*Last updated: 2026-09-29*

> Handed to each per-repository subagent with that repository's notes; state lives in [context.md](context.md).

You migrate exactly ONE repository (named in your prompt) onto the wow-two planning standard. Docs only. Work only
inside that repository. Read the standard first:
`/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/conventions/planning/version-track/version-track.md`
(sections "Planning files", "Backlog", "Location & naming", "Polish iterations", templates at the end).

## Target state

A repository plans with exactly two things:

- `engineering/planning/backlog.md` — every unbuilt item (feature, fix, engineering, product work) in grouped tables
  `Item · Type · Notes`, top of each group = next; opens with a `## Features` group (`Feature · State · Spec`).
- `engineering/planning/version-track/v{X.Y}/v{X.Y}.md` — one folder per version; the newest folder is the active
  version (CI reads `X.Y` from it). Never a flat `v{X.Y}.md`, never `engineering/versions/`.

Nothing else plans: no `planning.md` (engineering or product), no roadmap file, no `features.md`, no version-track lead
doc (`version-track/version-track.md`), no polish / rough / vector track.

## Steps

1. **Snapshot first.** Run `git -C <repo> status --short` and `git -C <repo> diff --cached --name-only`. Every path
   listed now is another lane's work: never revert, restore, stash, reset or delete it. Paths already staged are
   another lane's prepared commit ("foreign staged").
2. **Inventory** every planning file: `engineering/versions/**`, `engineering/planning/**`, `product/planning/**`,
   `product/features/features.md` (and any other feature index), `*roadmap*.md` outside `engineering/codebase/`,
   `version-track/version-track.md`, `polish-track/`, `rough-track/`, `vector-track/`.
3. **Versions.** Move `engineering/versions/v{X.Y}/` into `engineering/planning/version-track/v{X.Y}/` (when both
   exist for one version, merge into one doc). Turn a flat `v{X.Y}.md` into `v{X.Y}/v{X.Y}.md`. Keep each version
   doc's content; only fix its links, and add the meta line `**Status:** … · **Type:** … · **Started:** … ·
   **Completed:** …` when it is missing (Type `Feature` unless the version is an SDK extraction or adoption; take
   Status and dates from the doc or `git log`, `—` when unknown). A transient iteration plan inside a version folder
   stays only while its iteration is open. Delete `engineering/versions/` once empty.
4. **Other tracks.** Polish track: each polish iteration becomes a `Polish` iteration (`### Iteration N — {Area}
   polish`, tasks opening with `Refactor` · `Rename` · `Remove` · `Split`) — a done one inside the version doc that
   covers its period (match by date, `git log`), an open one inside the active version if that version is still open,
   else as rows in the backlog. Rough track: each `r{X.Y}` becomes an ordinary version doc continuing the repo's `v`
   numbering (odd minor = Feature). Vector track: fold each lane's recorded iterations into version docs — completed
   work as completed iterations, open work into the active version or the backlog. Delete the track folders and their
   lead docs after folding. Keep task lines compact (the standard's Task form); drop re-scoping notes and logs.
5. **Backlog.** Write `engineering/planning/backlog.md` from the template, merging every unbuilt item from the old
   `backlog.md`, `engineering/planning/planning.md`, `product/planning/planning.md`, roadmap files, the version-track
   lead doc and track docs. One row per item, no duplicates, no strike-through, no future-version tags; drop shipped
   items (the version docs record them). The `Features` group lists every feature of the product, one compact line
   each, from `features.md` and every per-feature spec file: State `shipped v{X.Y}` or `planned`, Spec a relative
   link to its spec file when one exists, else `—`. Keep per-feature spec files where they are.
6. **Decisions and history.** A settled decision that still binds moves to `product/context.md` (product; append to
   its decisions section, deduplicated) or `engineering/architecture/` (technical; `architecture.md` or the matching
   design doc). Logs, dated evidence of finished work, status tables of shipped work and superseded decisions are
   deleted — git keeps them. When unsure whether a fact still binds, keep it in the destination doc rather than lose it.
7. **Moves.** `engineering/planning/rules.md` → `engineering/development/rules.md` (add a one-line link in
   `engineering/development/development.md` when that lead doc exists). Analyses, audits, reviews and deep-dive
   folders under a planning folder → `engineering/research/` (keep their names; add a row to `research.md` when that
   lead doc exists). Scripts under a planning folder → `engineering/scripts/`. Diagrams or scripts under
   `product/planning/` → `product/flows/` (diagrams) or `product/research/` (analyses). Leave every `handoff.md` where
   it is — the chat that loads a handoff disposes of it — and name it in your report.
8. **Delete** the merged sources: `engineering/planning/planning.md`, `product/planning/planning.md` (and
   `product/planning/` once empty), `features.md`, roadmap files, `version-track/version-track.md`, the old track
   folders, `engineering/versions/`.
9. **References.** Fix every path inside this repository that points at a moved or deleted file: `CLAUDE.md`,
   `AGENTS.md`, `README.md`, `.claude/rules/file-references.md`, and doc links (grep for `engineering/versions`,
   `planning/planning.md`, `product/planning`, `features.md`, `planning/rules.md`, `version-track/version-track.md`,
   `polish-track`, `rough-track`, `vector-track`, and each moved analysis). `file-references.md` rows: backlog,
   active version (`newest engineering/planning/version-track/v{X.Y}/v{X.Y}.md`), `engineering/development/rules.md`,
   moved research. Never edit code under `engineering/codebase/`.
10. **Ecosystem-wide items** (an SDK upgrade or an extraction spanning products, a wow-two-ws convention task) do not
    go into this repository's backlog unless they are this product's own adoption work; list them in your report
    instead, with their source line.

## Git

- History-preserving moves: `git -C <abs-repo> mv <old> <new>` only for tracked files AND only when the repository has
  no foreign staged paths; otherwise a plain `mv`. Untracked files: plain `mv`.
- Never `git restore`, `checkout --`, `stash`, `reset`, `clean` or `rm -f`; never touch another lane's files beyond
  moving a planning file that carries their uncommitted edits (moving keeps their content).
- Stage only when the repository has no foreign staged paths: `git -C <abs-repo> add -A -- <each path you touched>`
  (deletions included). Do not stage a file that had uncommitted changes before you started (step 1 list) — report it.
- Commit only when BOTH hold: no foreign staged paths, and the repository's commit flag is ON. Check the flag with
  `python3 -B /Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/.codex/hooks/commit_permission.py status --repo <abs-repo>`
  (read `COMMIT PERMISSION: ON`). Print the staged paths (`git -C <abs-repo> diff --cached --name-status`), then run
  exactly `git -C <abs-repo> commit -m "docs: moved planning onto one backlog and the version track"`.
- Never push, never amend, never rebase. A blocked git command is final: do not work around the guard.
- Shell commands must never contain the text `git-flags.` followed by json, log or lock.

## Report (your final message, compact)

- Repo · outcome: `committed <sha>` | `staged, commit flag OFF` | `unstaged: foreign staged paths` | `unstaged: untracked repo`
- Created / moved / deleted paths (short list)
- Features group row count and backlog item count
- Ecosystem-wide items for the SDK or wow-two-ws, with source
- Files with another lane's edits that you changed but did not stage; `handoff.md` files left in place
- Any fact that contradicts this brief, stated in one line (do not guess around it)
