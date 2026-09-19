# Approval routing diagnosis

*Verified: 2026-09-15; times below are Asia/Tashkent (UTC+5).*

## Finding

GitKraken's installed `PermissionRequest` hook blocks the request before ChatGPT's normal approval flow.
GitKraken also rotates between distinct live chats, marks the previous chat ended, and denies its pending request.
This explains both the absent ChatGPT prompt and the exact dismissal messages. The inspected evidence does not
establish a failure inside ChatGPT's automatic reviewer.

## Evidence

- `/Users/max/.codex/config.toml:62` enables `gitkraken-hooks@gitkraken`.
- `/Users/max/.codex/config.toml:143` contains trust for that plugin's permission-request hook.
- `/Users/max/.codex/plugins/cache/gitkraken/gitkraken-hooks/3.1.74/hooks/hooks.json:68` registers `PermissionRequest`.
  Its command at line 74 invokes `gk ai hook run --host claude-code --blocking`; line 75 sets a timeout of 86,400 seconds.
  The empty matcher includes every applicable permission request.
- ChatGPT's [hook documentation](https://learn.chatgpt.com/docs/hooks#permissionrequest) places this hook before normal
  approval routing. A hook may allow, deny, or return no decision; normal review follows only when no hook decides.
- The installed GitKraken application contains the exact error strings in
  `/Applications/GitKraken.app/Contents/Resources/app.asar`, archive member `src/main/static/960.main.bundle.js`.
  `applyBlockingPermissionRequest` keeps an unresolved promise in `pendingPermissionResolversBySessionId`.
  `upsertSessionRecord` calls `denyPendingPermission` when `runtimeState.isEnded` becomes true.
  The denial text is `GitKraken Desktop dismissed this permission request because the session ended.`
  The same provider also emits the previously observed `a newer request superseded it` dismissal.
- `/Users/max/Library/Application Support/GitKrakenCLI/gk_cli.log:2029` records `aihook: ending rotated session`
  for this task at 10:38:09, replaced by another chat. Line 2031 records the same at 10:44:47 with a different chat.
- The active transcript records the corresponding tool dismissals at 10:38:30 and 10:44:52.
  The second dismissal occurred while this task's same turn was still running; it was not the agent ending the turn.
- The transcript's 10:22 turn context selected `approvals_reviewer: auto_review`; its 10:38 context selected `user`.
  Both encountered the GitKraken interception. Switching reviewer alone does not remove the hook.
- The replacement request produced a native approval at 10:45:10, accepted at 10:47:18; the GitHub read succeeded.
  The desktop log records request ID `192`. This proves that native manual approval works when reached.

## Scope and limits

- ChatGPT desktop version: `26.908.40834`, build `8881`; GitKraken desktop: `12.4.1`.
- GitKraken plugin cache version: `3.1.74`.
- Both applications were running during inspection.
- GitKraken's exact rotation identity algorithm was not established; its log proves the cross-chat rotations.
- No evidence requires Full access, broader filesystem rights, or weakening workspace Git rules.
- Automatic review after disabling the conflicting hook completed two GitHub reads successfully.

## Applied correction

The owner approved disabling only the GitKraken `permission_request:0:0` hook in personal Codex hook state.
The one-line patch was applied through native escalation and verified in `/Users/max/.codex/config.toml:144`.
Native approval review and all other GitKraken/workspace hooks remain configured as before.

The installed ChatGPT UI implements individual hook toggles by writing `enabled` under `hooks.state` and reloading
user configuration. The applied one-line patch uses that same setting and preserves the existing trust hash:
`/private/tmp/gitkraken-permission-hook.diff`.

The setting is personal/global, not a workspace hook edit. Checked `.codex/config.toml` and `.codex/hooks.json`
in `10x-ws`, `eis-ws`, `mft-10x-ws` and `wow-two-ws`: none defines a conflicting GitKraken/permission-request override.
No per-workspace trust renewal is needed. The state key excludes the plugin cache version, so the correction does
not require editing each downloaded plugin copy. A future plugin identity change or external settings rewrite would
require rechecking; no software configuration can guarantee against those future changes.

Runtime verification: the desktop log selected `approvalsReviewer=auto_review` at 12:37:54 on September 15.
After the patch, `gh run list` and `gh run view 34934970480 --log-failed` both completed with exit code 0 through
native escalation. No application bundle, sandbox boundary or workspace Git enforcement was modified.

## Primary local traces

- Active transcript:
  `/Users/max/.codex/sessions/2026/09/12/rollout-2026-09-12T22-15-55-01a086ba-b096-7023-a63d-fa09c1fb4078_01a0969e-5b25-7180-aefa-c7d471ba2b70.jsonl`
- Desktop log:
  `/Users/max/Library/Logs/com.openai.codex/2026/09/15/codex-desktop-666df265-0f3b-45be-91f7-37f23c09cd80-42241-t0-i1-000104-0.log`
- GitKraken hook definition SHA-256:
  `91b825bee94af71a21d6ecdb936ba793747fb7a87a4c4ffc9f340bd30701027e`
