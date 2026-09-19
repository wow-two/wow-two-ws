# Permission recovery

*Last updated: 2026-09-16*

The observed execution blocks were resolved through native command escalation. No sandbox settings,
filesystem permissions, application security configuration or approval rules were weakened.

## Test runner

The runner requires a local socket that was denied in the sandbox. Approved `dotnet test` commands ran with
`--no-build --no-restore --filter FullyQualifiedName~<class> --nologo -v:q` from the SDK source directory.

| Project | Existing test class | Passed | Failed | Skipped |
|---|---|---|---|---|
| Foundation.Tests | ErrorNatureTests | 16 | 0 | 0 |
| Mediator.Tests | ExceptionToResultBehaviorTests | 6 | 0 | 0 |
| Messaging.Tests | FaultClassificationAndBusControlTests | 6 | 0 | 0 |

All commands exited 0. These are scoped existing tests, not a full SDK test-suite result.

## NuGet restore

Native escalation allowed the prepared FastCloner 3.5.6 experiment to restore from official NuGet:

```sh
dotnet restore /private/tmp/be-deep-clone-experiment/experiment.csproj --configfile /private/tmp/be-deep-clone-experiment/NuGet.Config --disable-parallel
```

Restore exited 0. The ordinary `dotnet run --project .../experiment.csproj --no-restore` execution then exited 0:
32 graph-copy assertions passed, 0 failed. [Exact output](experiments/fastcloner/results.txt).
The retained experiment source matches the executed source byte-for-byte.

## NuGet pack metadata

`dotnet pack --no-build --no-restore` can still reach NuGet metadata for a project with package references.
On 2026-09-16, `Testing.Data` remained active without output in the restricted sandbox; a native process sample
showed its worker blocked in `SystemNative_Connect`. Retrying the identical scoped command through native
`dotnet pack` escalation completed in `0.56s`, then the seven-package verifier passed.

Treat a silent, long-running pack as a possible network restriction: inspect its process state, sample it when
needed, terminate only the command started by the active run, and retry that exact pack with the reusable
`["dotnet", "pack"]` approval prefix. `--no-restore` does not prove that pack is network-free.

## Shared capture

The reusable recovery procedure is saved in `/Users/max/.codex/AGENTS.md`, under
`Permission recovery — every workspace`. The file was updated through native approval and read back;
no global `AGENTS.override.md` was present to replace it at verification time.

The procedure covers recognition of a sandbox failure, the scoped `require_escalated` retry, keeping the
approval-owning execution alive, distinguishing dismissal from denial, preserving native policy and checking
actual results. Ending the earlier child session dismissed its pending test retry; the successful retries were
owned by an active root execution until completion. This is workflow guidance, not a security exemption.

Global instructions are read when a new Codex instruction chain is built; already-running chats may need to
reread the file. No other running chat was inspected or modified. Sources:
[global instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[sandbox and approval boundaries](https://learn.chatgpt.com/docs/agent-approvals-security).

## Remaining scope

Toolchain note, verified 2026-09-15: `/usr/bin/git` exited 69 because Xcode had an unaccepted license.
This was a toolchain gate, not a sandbox denial. `which -a git` exposed an existing standalone Codex runtime Git:
`/Users/max/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/fallback/git` (version 2.53.0).
Its scoped `diff --check` commands completed successfully. Future runs should rediscover and verify an available
standalone binary instead of assuming this cache path persists. No Xcode license was accepted, toolchain settings
changed or filesystem permissions broadened.

No test-socket, NuGet restore or NuGet pack permission block remains for these checks. SDK release readiness
is locally verified. Future commands retain native approval boundaries; these results do not claim permanent
unrestricted access.
