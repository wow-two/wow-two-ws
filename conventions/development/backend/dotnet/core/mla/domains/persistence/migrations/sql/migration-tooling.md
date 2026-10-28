# Migration tooling

*Last updated: 2026-10-28*

> How the `migrate` command tree is composed and hosted: the image helper, the `wow-migrate` tool, exit mapping,
> guards, secrets and configuration. The verbs and their contract live in [actions](../migrations.md#actions).
> Point ids cite the [migrations analysis](../../../../../../../../../../ideas/migrations-analysis-2026-10/migrations-analysis-2026-10.md).

## Shape

- must build the verb tree once, in the be sdk library that `wow-migrate` and every host share (M11, M57).
- must delegate migration operations to `IMigrationRunnerService`.
- must keep argument parsing, configuration, exit mapping and confirmation in the tree, out of the engine.
- must construct the tree through the builder role and keep command bodies in the runner role.
- must keep `Program.cs` to composition, parse/invoke and terminal error mapping.
- current tree → [verb tree builder](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src/Data/Migrations/Commands/MigrateCommandBuilder.cs).

---

## Host

- must run a verb before the web host starts: `MigrateCommand.IsCommand(args)`, then
  `app.RunMigrateCommandAsync(args)`, ahead of `app.Run()` (M11).
- must exit with the verb's code instead of starting the web host (M57).
- must serve `sets --json` from the service provider alone, with no settings file and no database (M78).
- must answer the tree for EF and DbUp sets through the same helper (M11).

---

## Packaging

- must distribute `wow-migrate` as a repo-local, exact-version-pinned `dotnet tool`.
- must use `PackAsTool`, an explicit `ToolCommandName`, and a dotted package id.
- must keep one platform-agnostic package unless the tool deliberately ships platform-specific assets.
- must set `CreateRidSpecificToolPackages=false` for that platform-agnostic .NET 10 tool package.
- must keep package dependencies in central package management.
- must keep the local manifest under `.config/dotnet-tools.json` and run restore from its repository tree.
- must not use wildcard versions in the manifest.

---

## Commands

- must use the pinned `System.CommandLine` API rather than beta-version examples.
- must declare shared options once as recursive options.
- must have `SetAction` delegate to the runner with the supplied cancellation token.
- must disable the default exception handler when the host supplies its own sanitized terminal mapping.
- must honor cancellation through configuration, connection and engine calls.

---

## Exit codes

- must map every outcome to the [exit contract](../migrations.md#actions): `0`, `1`, `2`, `3` (M10, M17).
- must classify both `Result` failures and thrown exceptions at the tree's boundary.
- must not depend on removed migration-specific exception types for returned failures.
- must print a concise sanitized failure description, then the `migrate-result` line last (M37).
- current runner → [verb tree runner](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src/Data/Migrations/Commands/MigrateCommandRunner.cs).

---

## Guards

- must compare `--confirm <database>` ordinally with the resolved database's name, never an environment name (M2).
- must exit `1` on a missing or mismatched `--confirm`, with a sanitized rerun hint (M2).
- must take the typed `--confirm` as the whole confirmation; no prompt and no `--force` (M34).
- must guard only the mutating mode of a mixed read/write verb.
- must enable the engine's guard (`AllowRollback`) only for the guarded verb's run (M2).
- must not hard-wire `AllowRollback` on for every invocation.

---

## Secrets

- must redact connection strings and credentials from logs, errors and searched-location diagnostics.
- must prefer environment or stdin input over a plaintext command-line secret.
- must fail when a required environment substitution is unset.
- must commit only secret-free configuration templates.
- must not imply an env/stdin flag exists unless the current CLI exposes it.

---

## Configuration

- must connect every set through `Migrations:ConnectionString` when it is set, else the host's connection (M8).
- must resolve explicit flag, environment, discovered default in that precedence order.
- must fail with sanitized searched locations on a true miss.
- must require an explicit path when source discovery is ambiguous.
- must restrict a local default connection to the canonical development layout.

---

## Composition

- must build and dispose a provider for each invocation.
- must register the connection seam, logging and `AddDatabaseBespokeMigrations` before resolving the runner.
- must consume the runner's result and map it to the exit-code contract.
- must dispose externally constructed data sources explicitly; registering an instance does not transfer disposal ownership.
