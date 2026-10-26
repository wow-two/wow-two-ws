# Repository git flags

*Last updated: 2026-10-26 01:00 PM*

> Claude Code integration for the workspace git flags in `wow-two-ws`. Only commands that are risky and
> used often get a flag; risky commands that are rarely needed never run; safe commands need no flag.

## Contract

- flag, directive and consent rules: [personal Git conventions](/Users/max/.claude/conventions/git.md#repository-commit-permission); not repeated here.
- staging and batch handover: [workspace Git protocol](../conventions/development/repo/version-control/git.md#protocol-agent--human).
- analysis and decisions (G0–G8): [docs/git-flags.md](../docs/git-flags.md).
- this integration applies to `wow-two-ws` and every repository inside it; each other workspace runs its own hooks.

---

## Hooks

- `.claude/hooks/commit_permission.py` owns the workspace store and answers each kind's permission check.
- `.claude/hooks/commit-switch.py` feeds it `SessionStart` and exact prompts (tail-called by
  `expand-markers.sh`); `.claude/hooks/guard-git.py` consults it for gated commands and guards the store against
  `Write` / `Edit` / `MultiEdit` / `NotebookEdit`.
- must resolve directive paths against the workspace root; `.` selects the workspace repository, `<folder>/*` every
  repository under an existing folder, present and future, and `*` the workspace default.
- must make the entire user message one directive: `~commit_*` / `~push_*` and one target, or
  `~git_on|off <kind>[,<kind>...] <target>...` / `~git_status <target>...`.
- must name each kind once; `all` only disables; one unresolvable target voids the whole directive: a missing
  repository, a folder that does not exist or lies outside the workspace, `./*` (use `*`), or a folder named without
  `/*` that is not a repository root (`workbench/wow-two-sdk-beta`, a repository's `src`), which would otherwise set
  the enclosing repository's flag.
- `history` and `gh` merged into `commit` and `push` on 2026-09-29; a directive naming them changes nothing.

## Kinds

| Kind | While `ON` for the target repository |
|---|---|
| `commit` | `git -C <repo> commit -m "subject"`; `commit --amend`, `rebase`, `cherry-pick`, `revert`, `merge`, `am`, `subtree`, soft / mixed `reset` to a commit |
| `push` | `git -C <repo> push [-u] [<remote> [<refspec>...]]` with `<remote>` a remote the repository already has; every gh write: pull requests, issues, releases, workflow runs, secrets, variables, repository settings and creation, API writes |

- a rewrite never replaces a commit a remote-tracking branch already holds: amend checks `HEAD`, rebase
  `<upstream>..<branch>` (or everything with `--root`), reset `<commit>..HEAD`; a range the guard cannot resolve
  blocks. Merge, cherry-pick, revert, am and subtree add commits and replace none.
- allowed without a flag (safe): read-only git and gh, `fetch`, `pull`, `git clone` and `gh repo clone` (a clone
  writes only the new repository and its own `origin`), staging, `stash`, branch and tag writes, unforced `mv` and
  `rm`, `apply` unless reversed, `submodule init|update|sync`, `notes` writes.
- never, whatever the flags (risky and rarely needed): forcing, deleting, mirror, pruning and hook-skipping pushes;
  pushes to a URL, a path or a remote the repository does not have (a remote write in disguise); clones with
  `--config` / `-c`, `--template` or `--upload-pack` / `-u`, including after `gh repo clone ... --`; worktree discards (worktree `restore`, path / `.` / forced `checkout`, forced `switch`,
  `reset --hard|--merge|--keep`, `clean`, forced `rm` / `mv`, reversed `apply`, `checkout-index`); every `config`
  write; `remote` and `worktree` writes; `submodule add|deinit|set-url|set-branch|absorbgitdirs`; ref and object
  surgery (`filter-*`, `fast-import`, `update-ref`, `update-index`, `replace`, `gc`, `prune`, `reflog` and
  `symbolic-ref` writes); `send-email`; `gh repo delete` and direct repository DELETE API calls;
  `gh repo create --source|--remote|--push`, short forms `-s` / `-r` included; LFS installation, direct upload,
  pruning and migration writes.
- LFS inspection, `migrate info`, hydration (`fetch|pull|checkout`) and scoped attribute changes
  (`track|untrack`) need no flag. Other LFS verbs remain human operations.
- Checkout path and patch forms remain worktree discards when the optional `--` separator is omitted.
- a new category earns a flag only when it is both risky and used often; otherwise it joins one of the two lists.
- a gated git command acts on `git -C <repo>`, else the working directory; a `cd`, `pushd`, `--git-dir` or
  `--work-tree` in the same command blocks it.
- a gh write acts on `-R owner/name`, a `repos/owner/name` API path or `repo <verb> owner/name`;
  the matching managed repository holds the flag. An `owner/name` no checked-out repository matches reads `OFF`,
  and so does a write that names its repository through `GH_REPO`. Every `gh api graphql` mutation reads `OFF`:
  its target is a node ID the guard cannot match, and a document it cannot read (`@file`, `--input`, a shell
  expansion) counts as a mutation. A write that names none (`gh pr create` in a repository, gh's `{owner}/{repo}`
  placeholders, graphql queries) reads the working repository. Lookup follows nested `workbench`
  ownership without a fixed depth; it skips dependency trees and directory symlinks.
- repository creation reads the flag of the path the new repository will be cloned into, through folder overrides:
  bare `gh repo create owner/name`, `POST orgs/{owner}/repos -f name=…`, template generation
  (`POST repos/…/generate -f owner=… -f name=…`) and forks into an org. The path follows
  [workbench layout](../conventions/development/repo/layout/workbench-layout.md) (`CLONE_FOLDERS` in the guard):
  `wow-two*` → `workbench/{org}/{name}`, `ocharo-hq` → the ocharo-ws `workbench/{name}`, and an org whose folder
  already exists under `maxs-projects/clients/` or `maxs-projects/ventures/`. It reads `OFF` when no single folder
  fits (personal repositories, `POST user/repos`), when `owner/name` is not stated plainly (no owner, `--input`,
  `@file` fields), or when the path already exists and is not empty. Creation with `--source` remains blocked
  because it also changes local configuration.
- history rewrites still meet the lane check, which stops once on another lane's uncommitted files.

The following fenced examples are documentation, not consent:

```text
~commit_on workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe
```

```text
~push_off workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe
```

```text
~git_on commit,push workbench/wow-two-platform/wow-two-platform.wheelhouse
```

```text
~git_on commit *
```

```text
~git_on commit,push workbench/wow-two-sdk-beta/*
```

```text
~git_off push workbench/maxs-projects/ventures/saas/10x-venture-forever-pin
```

```text
~git_status *
```

---

## Store

- one store per workspace: `.claude/git-flags.json`, gitignored, beside this engine; `.claude/git-flags.log` holds the
  hash-chained change log and `.claude/git-flags.lock` the writer lock.
- `defaults` holds the workspace default per kind; `repositories` holds overrides keyed by the path inside the
  workspace: a repository's (`.` for the workspace repository) or a folder's, followed by `/*`
  (`workbench/wow-two-sdk-beta/*`). Kind by kind, the effective flag is the repository's override, else the longest
  folder override above it, else the default.
- `~git_on|off <kinds> *` sets or clears the default for every repository, present and future; a per-repository
  directive records an override, `OFF` included, so one repository can opt out of an `ON` default.
- `~git_on|off <kinds> <folder>/*` records one override for every repository under that folder, present and future,
  in the store that owns the folder; a deeper folder or a repository override wins over it.
- a repository's flags live in the innermost workspace store that contains it: a nested workspace with its own store
  (ocharo-ws) owns its repositories, whichever workspace the chat runs in; without one, its repositories fall under
  this store.
- every change appends one log entry (revision, time, changes, session, turn, prompt, recording workspace, the store
  hash, the previous entry's hash), then replaces the store atomically under the lock.
- a store that fails its schema or disagrees with its log reads as every flag `OFF`; an `on` directive is refused and
  any `_off` directive resets it to every flag `OFF` with a repair entry that commits to the broken log before it.
- `seen_consents` rejects a replayed event; `UserPromptSubmit` owns every transition, shell checks only read, and
  `Stop` leaves the store unchanged.
- must change the store only through a directive; no tool edits, moves or names it (both agents' guards block it).
  Hooks stay a guardrail, not a security boundary.

---

## Status

The helper is read-only and prints one repository's flags, one folder's, or the whole store with `*`; it exposes no
`on`, `off`, or mutation command:

```sh
python3 -B .claude/hooks/commit_permission.py status --repo workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe
python3 -B .claude/hooks/commit_permission.py status --repo 'workbench/wow-two-sdk-beta/*'
python3 -B .claude/hooks/commit_permission.py status --repo '*'
```

- each effective flag names its source: `(override)`, `(folder workbench/wow-two-sdk-beta/*)` or `(default)`.
- `~git_status <folder>/*` prints what a new repository under the folder gets, then the overrides under it that win.
- session start shows the working repository's effective flags in both agents.
- must report an invalid store or unavailable repository as blocked, preserving the stored state.
- unavailable or untrusted hooks cannot activate permission; offline fixtures must use isolated temporary state.

---

## Commit and push forms

```sh
git -C <absolute-repository> commit -m "subject"                  # commit flag ON
git -C <absolute-repository> push [-u] [<remote> [<refspec>...]]   # push flag ON
```

- must use explicit `git -C` for managed repositories; shell hook working-directory metadata may name the workspace.
- must name a remote the repository already has (`git -C <repo> remote -v`) or none; a URL or a path never runs.
- may use `git commit -m "subject"` only when the hook resolves the target repository unambiguously.
- must inspect staged paths, their diff, and whitespace; state the batch and proposed subject before committing.
- must preserve unrelated staged paths and exclude them from the reviewed batch.
- must report the resulting SHA after a commit or rewrite, and the pushed branch and range after a push.
- forcing, deleting and mirror pushes, implicit staging and pathspec commits never run.
- must reject compound shell forms and alternative Git configurations for the ordinary commit and push exceptions.
- must preserve configured signing; a signing-socket block uses native escalation for the same authorized command.
- this workflow guard does not claim a security boundary against arbitrary executable code.

---

## Verification

```sh
python3 -B .claude/hooks/tests/test_commit_permission.py
python3 -B .claude/hooks/tests/test_commit_switch.py
```

- must test persistence across chats, revocation, defaults, folder and repository overrides with their precedence,
  nested stores, tampering and repair.
- must test each kind's gated commands, pushed-history refusal, the never-run and flag-free lists, multi-kind and
  multi-repository directives, hidden targets, gh origin matching, unmatched gh targets, repository creation by
  checkout folder, clones, named-remote pushes and the store edit guard.
- must test prompt provenance, replayed transitions, concurrency, and rejected commit forms without making commits.
- offline passing tests do not prove hook trust or a live permission change.
