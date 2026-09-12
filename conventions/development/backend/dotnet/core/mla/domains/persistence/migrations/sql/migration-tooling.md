# Migration tooling

*Last updated: 2026-09-10*

> CLI composition and operational controls for the bespoke migration engine.

## Shape

- must keep argument parsing, configuration, composition, exit codes and confirmation in the CLI host.
- must delegate migration operations to `IMigrationRunnerService`.
- must keep `Program.cs` to composition, parse/invoke and terminal error mapping.
- must construct the command tree through the builder role and keep command bodies in the runner role.
- current tree → [CLI builder](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/Migrations/cli/CliCommandBuilder.cs).

---

## Packaging

- must distribute as a repo-local, exact-version-pinned `dotnet tool`.
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

- must return `0` for success.
- must return `1` for invalid input, configuration, drift or a failed migration precondition.
- must return `2` for execution failure or refusal of a destructive-operation guard.
- must classify both `Result` failures and thrown exceptions at the CLI boundary.
- must not depend on removed migration-specific exception types for returned failures.
- must print a concise sanitized failure description.
- current runner → [CLI runner source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/Migrations/cli/CliRunnerService.cs).

---

## Destructive operations

- must guard rollback, repair, truncate and reset against the resolved target, not only an environment name.
- must require `--i-understand-this-is <target>` to match that target with ordinal comparison.
- must prompt `[y/N]` after target confirmation unless `--force` is supplied.
- must return `2` on refusal and provide a sanitized rerun hint.
- must guard only the mutating mode of a mixed read/write verb.
- must enable engine rollback/repair only for the guarded operation.
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
