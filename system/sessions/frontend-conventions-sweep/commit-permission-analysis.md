# Commit permission analysis

*Last updated: 2026-09-26*

> Existing switch, reproduced failures, and a proposed repository/chat consent protocol.

## Status

- [x] Located the old switch and reproduced parent/subagent state collisions.
- [x] Owner selected one persistent flag per repository on September 26.
- [x] Implemented exact user directives and new-chat reconfirmation in `wow-two-ws`.
- [x] Updated the shared Git convention and local entrypoints.
- [x] Passed 44 isolated policy/adapter, 23 lifecycle, and four staging tests.
- Current SDK and workspace permission: **OFF**; no flag file was created by installation.
- Live ON activation and a real commit were not attempted; the developer has not enabled this repository.
- The prepared SDK index remains 445 files. No commit, push, native-policy change, or trust edit occurred.

The [shared contract](/Users/max/.codex/conventions/git.md#repository-commit-permission) and
[local guide](../../../.codex/commit-permission.md) describe the installed behavior.

---

## Installed switch

- one `enabled` flag inside `<resolved Git directory>/codex-commit-permission.json`
- OFF persists across turns, chats, subagents, and Stop events
- ON persists for the confirmed chat and its subagents, independent of their turn IDs
- a different chat must ask whether to keep ON; the stored flag stays unchanged while confirmation is pending
- only the last confirmed chat may commit; returning to an older chat requires reconfirmation
- exact native user directives own mutations; the CLI offers read-only `status --repo <repo>`
- records include the confirmed chat, revision, exact consent, timestamp, and replay fingerprints
- updates lock the complete transition and atomically replace the record
- malformed state blocks commits; an explicit OFF repairs a malformed non-symlink record
- old per-turn temporary grants are ignored, never migrated into enabled state
- new-chat checks run on the current repository at startup/prompt, explicit Git reads, and every ordinary commit
- managed-repository commits retain the explicit `git -C <absolute-repository>` form
- native execution review, configured signing, staging scope, publishing, and history restrictions remain separate

The runtime's `UserPromptSubmit` provenance is trusted by the workflow guard. Arbitrary local code can still
forge input or change files; this is not a security boundary against executable code. Agents must not replay
synthetic events against live repositories. Tests create their own isolated Git metadata.

---

## Reproduced former blocking mechanism

`observe()` at `commit_permission.py:44` replaces the entire state whenever the incoming turn differs.
`guard()` at `claude_adapter.py:139` invokes it for every supported shell command, including reads.

Official [Codex hook documentation](https://learn.chatgpt.com/docs/hooks#common-input-fields) says subagent hooks
use the parent `session_id`. Consequently, different agent turns write the same file:

```text
parent turn: grant ON for SDK
child shell: same session, different turn → replace file with repo=null
parent commit: parent turn differs again → replace file with repo=null → deny
```

Offline tests reproduce this sequence. A read-only native child command also confirmed the live mutation:

- parent chat: `01a086ba-b096-7023-a63d-fa09c1fb4078`
- parent turn: `01a0d9da-0ea9-7d02-996e-b05ff946b00b`
- child `CODEX_THREAD_ID`: `01a0d9dd-79f3-7752-a0a7-bf1d0abe66af`
- parent-keyed state observed by that child: turn `01a0d9e0-02cf-7473-b409-42c57eb03c8f`
- permission remained OFF throughout the live observation; no synthetic event or activation was sent

Historical evidence from this chat on September 25, UTC:

- `16:44:20`: helper activation and status both reported ON for the Vue SDK repository.
- `16:44:36–16:44:52`: three audit subagents were resumed.
- `16:45:39`: the ordinary commit was blocked with the generic workspace prohibition.
- The failed command used `git -C <absolute SDK repository> commit -m '…'` correctly.

Subagent interference was verified in the former implementation and fits that sequence. The exact historical state writer
cannot be established because the implementation recorded no transitions. The earlier description of a
separate legacy hook overriding valid consent is unproven: the adapter itself invokes the legacy guard when
`permits()` returns false, hiding the underlying reason behind the same message.

---

## Former implementation defects

| Finding | Evidence | Required repair |
|---|---|---|
| Any differing turn replaces the shared grant | `observe():44–53`; offline/live evidence above | Separate grant ownership from observed child turns |
| Interleaving loses the closed-turn record | Closed parent → child → parent can be rearmed offline | Preserve closed records; reject stale lifecycle events |
| Concurrent activation can overwrite revocation | Repository resolution pauses between read/write | Lock complete transitions; validate the expected revision |
| Incomplete JSON is accepted | Missing `closed` permits; missing `turn_id` can display ON | Validate schema, identity, types, and lifetime together |
| Repeated OFF can fail | `set_permission():68–74` throws after `Stop` | Make exact-scope revocation idempotent |
| Helper can name another chat | Public `--session` at `:162` | Remove cross-chat mutation override from live commands |
| Consent is not evidenced in state | Helper takes repo/session but no user-confirmation binding | Record native user event and exact confirmed scope |
| Denial conceals its cause | Adapter falls through to generic legacy prohibition | Report OFF, scope mismatch, closed, invalid, or unsupported form |

The former implementation passed its original 14 tests; they did not cover these interleavings.
The installed replacement passes 44 policy/adapter tests, including the missing cases.

Temporary characterization script: `/private/tmp/commit-permission-reproduce.py`.
It passed all six defect-characterization assertions with isolated temporary storage and mocked repository
resolution. Passing means the defects were reproduced, not repaired. No Git commit was executed.

The hook remains a workflow guardrail, not protection against arbitrary local code rewriting its files.
Native sandbox, review, signing, hook trust, and publishing restrictions remain independent.

---

## Rollout scope

| Workspace | Current ordinary-commit handling | Scoped switch |
|---|---|---|
| `wow-two-ws` | Persistent repository flag with new-chat confirmation | Installed September 26 |
| `10x-ws` | Plain commits allowed subject to its lane guard | Absent |
| `eis-ws` | Commits forbidden by its strict local Git guard | Absent |
| `mft-10x-ws` | Codex shell guard validates input but performs no Git policy check | Absent |

Sources: each workspace's `.codex/hooks/claude_adapter.py`; existing `.claude/hooks/guard-git.py` files;
`10x-ws/.claude/rules/git.md`. This is a local implementation comparison, not a native-permission guarantee.

Do not copy an enabled grant across workspaces or silently reinterpret `10x-ws`/EIS defaults.
Installing a common switch is a separate policy rollout from enabling any particular repository/chat pair.

---

## Ownership

- shared operator contract: `/Users/max/.codex/conventions/git.md`
- workspace implementation guide: `.codex/commit-permission.md`
- runtime state: the target repository's Git metadata; no versioned status copy
- local policy adapters link the shared contract; other workspaces retain their installed policies

---

## Verification — 2026-09-26

- `python3 -B .codex/tests/test_commit_permission.py`: 44 tests passed
- `python3 -B .codex/tests/test_codex_hooks.py`: 23 tests passed
- `python3 -B .codex/tests/test_index_operations.py`: four tests passed
- managed SDK status command reports OFF through the installed helper
- workspace and SDK flag files remain absent, meaning OFF; installation created no grants
- policy and documentation whitespace checks pass
- native hook configuration, trust entries, sandbox settings, signing, and SDK staged paths remain unchanged

The suite covers persistent ON/OFF, child turns, new-chat blocking/reconfirmation, independent repositories,
concurrent transitions, duplicate/stale directive replay, exact consent metadata, corrupt-state revocation,
symlink refusal, read-only CLI behavior, command restrictions, and native adapter input normalization.

The replacement also rejects ambiguous shell argument arrays and conflicting `cmd`/`command` fields, ensuring
its policy checks the script that the shell would execute. All commit command strings in tests are assessed
without executing Git commits.

A future live ON verification requires the owner's exact repository directive. This configuration work grants
no such permission. Resume the SDK batch using the existing human-commit workflow while permission stays OFF.
