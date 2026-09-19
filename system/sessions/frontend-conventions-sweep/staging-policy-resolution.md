# Staging policy resolution

*Last updated: 2026-09-12*

## Verified local result

- Removed the wow-two Codex adapter's staging-only escalation-metadata check and its obsolete guard file.
- Allowed index-only staging, unstaging, explicit path resets and cached patches/removals in the local Git guard and conventions.
- Preserved native sandbox approval, worktree protection, publishing restrictions and existing history/lane checks.
- All 24 local hook tests passed, including metadata-free shell payloads and protected non-index operations.
- Live `git add`, `git restore --staged` and re-staging succeeded through the current chat's `functions.exec` shell route. No new chat was needed.
- SDK index verified: the six files under Vue `src/foundation/results/` plus `tests/unit/foundation/results/results.test.ts`. Cached whitespace check passed. The human commits; no commit or push was performed.

## Completed shared scope

The user explicitly approved personal Codex defaults plus all four workspaces. The remaining 31-file patch was approved by native review and applied after verifying that its recorded originals still matched disk. Personal defaults and the wow-two, 10x, EIS and MFT convention/hook copies now permit staging and unstaging within the authorized task scope. The supplemental staging-only prompt rule is removed; native sandbox approval remains authoritative.

All 58 hook tests passed: wow-two 24, 10x 24, EIS 4, MFT 6. Active instruction-path checks found no stale references to the removed metadata gate or blanket unstaging prohibition. Existing non-index Git restrictions remain in place. No hook trust storage was changed.

## Hook review commands

The user uses ChatGPT desktop only. The installed desktop bundle verifies the `codex://threads/new?path=...` workspace route and `codex://settings` settings route. Its Hooks settings component includes project selection, **Reload hooks**, and **Trust**. No interactive CLI session is needed.

```zsh
workspaces=(
  "/Users/max/Projects/10x-ws"
  "/Users/max/Projects/Company/EPAM/eis/eis-ws"
  "/Users/max/Projects/10x-ws/workbench/fam/mft-10x-ws"
  "/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws"
)

for workspace in "${workspaces[@]}"; do
  open -a "ChatGPT" "codex://threads/new?path=$workspace"
done

open -a "ChatGPT" "codex://settings"
```

In desktop settings, select **Hooks**, choose **Reload hooks**, and review/trust changed hooks for each of the four projects. Source evidence: `window-all-closed-BxbCP6YG.js` and `hooks-settings-3ea21b15a380.js` inside the installed `/Applications/ChatGPT.app/Contents/Resources/app.asar`. The commands were checked against the installed route parser, not executed on the user's behalf.

## Cause

The failed tool call requested `sandbox_permissions=require_escalated`, but the local hook rejected it because its input did not contain the expected metadata. The hook depended on transport-specific metadata rather than the Git operation. Previous synthetic tests supplied that metadata directly and therefore did not establish that the live execution route worked. Written conventions additionally contradicted the existing guard by forbidding all unstaging.
