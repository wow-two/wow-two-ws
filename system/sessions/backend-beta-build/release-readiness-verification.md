# Backend beta release-readiness verification

*Verified: 2026-09-16*

## Verdict

The convention-sweep SDK revision is locally ready for the developer-owned commit and publish flow.
This evidence verifies the current working tree; it does not claim that NuGet or the Git tag exists.

## Release checks

- Version under test: `10.0.55-beta` from `src/Directory.Build.props`.
- Expected CI version after its automatic bump: `10.0.56-beta`.
- Release build: passed with `0` errors and `406` existing analyzer warnings.
- Release tests: `453` passed, `0` failed and `1` skipped across seven suites.
- Intentional skip: `KafkaEventBusTests.Dead_letters_failing_message_to_dlq_topic`.
- Packaging: all seven `.nupkg` and seven `.snupkg` files were created.
- Package verifier: passed for IDs, versions, licenses, repository revision, required assets,
  family dependency versions, production dependency boundaries and manifest generation.

## Suite results

| Suite | Passed | Skipped |
|---|---:|---:|
| Data | 28 | 0 |
| Foundation | 125 | 0 |
| Identity | 20 | 0 |
| Mediator | 69 | 0 |
| Messaging | 122 | 1 |
| Migrations | 26 | 0 |
| Web | 63 | 0 |

## Packages

- `WoW2.Sdk.Backend.Beta`
- `WoW2.Sdk.Backend.Beta.Data.Abstractions`
- `WoW2.Sdk.Backend.Beta.Data.Migrations.Cli`
- `WoW2.Sdk.Backend.Beta.Testing`
- `WoW2.Sdk.Backend.Beta.Testing.Data`
- `WoW2.Sdk.Backend.Beta.Testing.Integrations`
- `WoW2.Sdk.Backend.Beta.Testing.Messaging`

## Local permission recovery

One local `Testing.Data` pack waited on a network connection inside the restricted sandbox even with
`--no-restore`; a process sample confirmed the connect wait. The same unchanged command completed in `0.56s`
through native `dotnet pack` escalation. CI already has the required network access, so its command stays unchanged.
The reusable recovery note now includes this pack case in `permission-recovery.md`.

## Publish boundary

The developer commits and pushes. The workflow bumps `10.0.55-beta` to `10.0.56-beta`, restores, builds,
tests, packs and verifies the release revision, publishes through NuGet trusted publishing, pushes the release
commit and tag, then verifies all seven NuGet packages and the tag. Consumer repins begin only after that succeeds.
