# Vue sweep commit identity repair

*Last updated: 2026-09-26*

## Status

- [x] Identified the five affected local commits and the prior personal identity.
- [x] Verified live `origin/main` still points to the base commit.
- [x] Prepared a human-operated repair with a read-only default; initial preflight passed.
- [x] Human executed the repair; the agent did not change Git configuration or history.
- [x] Verified identities, signatures and preserved trees/messages/dates; human script verified unchanged index/worktree.
- [x] Updated commit IDs in the batch manifest and session state; retained originals in the repair mapping.

## Original diagnosis

Repository: `workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui`.

All five new commits record **both author and committer** as
`Sultonbek Rakhimov <SRakhimov@EBSCO.COM>`. The preceding human commits use
`Sultonbek Rakhimov <sultonbek.rakhimov@gmail.com>`.

| Original commit | Subject |
|---|---|
| `a83856199935d64281e867fdfaf6870ee1c3f172` | fix: hardened Vue foundations and session lifecycle boundaries |
| `b0b1d2048e9ead6f211aa5db4e5590dbcd024766` | feat: completed breaking Vue control and exact-value APIs |
| `bd921078b0e2b3309aa5e6c642c6cbc6cd1a033a` | feat: revised breaking Vue interactions and Google identity APIs |
| `c0ab3e14d362ab887bfd394985a75748ab160b00` | test: expanded Vue browser and packed consumer release gates |
| `75dfb59a3912a86013546c1a475978ba44224fb8` | docs: recorded the full Vue SDK sweep and migration guidance |

Live `git ls-remote origin refs/heads/main` returned
`f4fe5c6477bc83a344e8c10cc4d6467dabf176b8`, the immediate predecessor.
These five commits are unpublished; this repair does not need a force-push.

The current effective author/committer identity already resolves to Gmail through global Git configuration.
No local identity override or active author/committer environment override was observed. The global
configuration modification time, `2026-09-26 01:14:06 +0500`, follows the five commits
(`01:05:09`–`01:08:34 +0500`). The effective configuration at commit creation was not captured;
the historical setting writer is unverified. This is commit metadata, not evidence of wrong GitHub authentication.

The five original commits are unsigned. Current configuration enables OpenPGP signing with
`119E538B8B337E67BE2A351E810EA6E9C7F8E6FC`. The repair honors the current signing setting and verifies
every signature it creates. It never disables signing to avoid a prompt or failure.

## Executed repair

[Human-operated script](/private/tmp/fix-vue-commit-identity.py); successfully executed by the owner on September 26.
Do not rerun: its exact-original-HEAD guard intentionally rejects the repaired state.

```sh
python3 /private/tmp/fix-vue-commit-identity.py --apply
```

The execution required other SDK tasks and GitKraken writes to be idle. Compare-and-swap rejects a moved branch;
it cannot lock arbitrary edits from another process, which the before/after snapshots detect.

The script requires the exact repository, branch, original range, and live remote base. It rejects
custom Git repository/configuration/identity environment overrides and reads canonical objects without
replacement refs. It preserves each tree, full message, author date, committer date, and timezone.
Both identities become `Sultonbek Rakhimov <sultonbek.rakhimov@gmail.com>`.

Replacement commits are validated before a transaction creates a unique backup ref and compare-and-swap
updates local `main`. The script pins `user.name` and `user.email` in this repository only. The original
commits remain reachable from the backup ref. It prints the old-to-new ID mapping for verification.

The script never checks out, resets, stashes, stages, or pushes. It checks index bytes, staged and unstaged
diffs, and changed/untracked file contents before and after the ref update. A concurrent change stops
execution; snapshots are never restored over another task's work. Signing failure can leave unreachable
replacement objects but does not update `main`. A failure after identity pinning may leave those correct
local configuration values in place; a post-update verification failure reports that refs already changed.

## Execution boundary

The enabled SDK switch permits ordinary commits only. [Commit permission:82](../../../.codex/commit-permission.md:82)
keeps history rewrites subject to their separate restrictions. The [Git guard](../../../.claude/hooks/guard-git.py:102)
blocks ref surgery and repository configuration writes. The agent prepared the correction without running
its mutation mode or weakening these guards. The human executed the command above.

Other tasks' staged React/Ocharo work and ongoing Vue-port files must remain untouched.

## Verification record

- Read-only live preflight passed: exact five local commits, remote base, personal identity, configured signing.
- Independent script review passed; all 12 mocked tests pass in
  [verification tests](/private/tmp/test_vue_identity_repair.py). Covered read-only default, exact metadata,
  signing, atomic backup/CAS, concurrent-index rejection, invalid tree/signature rejection, and environment guards.
- Human execution completed successfully, reporting unchanged index/worktree and no push.
- Independent live verification passed for all five replacement identities, trees, full messages, dates,
  linear parent order, and OpenPGP signatures. Native escalation recovered GPG's sandbox-blocked trustdb read.
- Repository-local `user.name` and `user.email` match the personal identity.
- Backup `refs/backup/vue-identity-755a111cbf97` resolves to the original `75dfb59a3912a86013546c1a475978ba44224fb8`.
- Corrected tip: `cbadbd416a662659908956b706a9219e3660ef0f`. The [batch manifest](commit-batches.json)
  retains all five old-to-new mappings and uses replacement IDs for the active batches.
- Live GitHub `main` remains `f4fe5c6477bc83a344e8c10cc4d6467dabf176b8`; normal push is appropriate.
- Build/test reruns are unnecessary for identical trees; verify metadata and tree equality instead.
