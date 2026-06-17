# Migration Tooling

*Last updated: 2026-06-16*

> How the bespoke migrator ships as a `dotnet tool` CLI — a thin host over the engine: packaging, verb tree, exit codes, destructive-op guard.
> Purpose — give CI and operators a version-pinned, scriptable migration command that branches cleanly on outcome and refuses destructive ops.
> Use case — wiring the CLI host of a bespoke-migrator repo. `smart-qr-migrate` is the first consumer; `wow-migrate` is the SDK target.

---

## Shape

- The CLI is a **thin host** over the migrator engine — one of three hosts (the others: an HTTP endpoint, a hosted service).
- It owns: arg parsing · config resolution · the composition root · exit codes · confirmation prompts — **nothing else**.
- The engine owns the migration operation and is resolved from DI ([bespoke-migrations.md](bespoke-migrations.md) — `AddDatabaseBespokeMigrations`,
  `IMigrationRunnerService`).

---

## Packaging

Pack as a tool, not a published app. The csproj head:

```xml
<PropertyGroup>
  <OutputType>Exe</OutputType>
  <PackAsTool>true</PackAsTool>
  <ToolCommandName>{verb-noun}</ToolCommandName>            <!-- the invoked command, e.g. smart-qr-migrate -->
  <PackageId>{Brand}.{Domain}.Cli</PackageId>               <!-- dotted, matches the ecosystem -->
  <CreateRidSpecificToolPackages>false</CreateRidSpecificToolPackages> <!-- .NET 10: keep one platform-agnostic package -->
</PropertyGroup>
```

- `ToolCommandName` = the shell command (`smart-qr-migrate`); `AssemblyName` SHOULD match it.
- `PackageId` carries the dotted brand (`{Brand}.{Domain}.Cli`).
- `CreateRidSpecificToolPackages=false` — on .NET 10, `dotnet pack` with **any** `RuntimeIdentifiers` present emits RID-specific tool packages
  instead of the framework-dependent platform-agnostic one (documented breaking change). Set the flag false, keep `RuntimeIdentifiers` out of the
  csproj → one `dotnet-tools.json` entry works on every OS. Use `ToolPackageRuntimeIdentifiers` only if multi-RID is ever wanted.
- CPM — versions are central. With `ManagePackageVersionsCentrally=true`, a versionless `<PackageReference>` resolves only when a `<PackageVersion>`
  exists in `Directory.Packages.props`. Add the CLI's deps (`System.CommandLine`, any standalone provider); pin exact lines, never `2.0.0-beta*`.

---

## Local manifest, not global install

- Distribute via a repo-local `.config/dotnet-tools.json` manifest (mirrors `dotnet ef`) — version-pinned per repo, `dotnet tool restore` on clone,
  no global pollution, CI-friendly.

```jsonc
// .config/dotnet-tools.json
{ "version": 1, "isRoot": true,
  "tools": { "{Brand}.{Domain}.Cli": { "version": "0.0.*", "commands": ["{verb-noun}"] } } }
```

- Manifest discovery walks up from the **cwd**. Invoking from a directory outside the manifest tree silently fails to restore — run from the repo
  subtree, or pass the explicit path flags.

---

## Command tree (System.CommandLine 2.0)

Build the tree in a `static CliCommands.Build()`; keep command **bodies** in a separate `CliRunner`.

- **Root** carries the **global, recursive** options — `new Option<string?>("--name") { Recursive = true }` applies to every subcommand without
  re-declaring.
- **Verbs** are `Command` objects added to `root.Subcommands`. Verb-local options/arguments declared on the verb.
- **`SetAction`** reads parsed values and **delegates to the runner** — the command knows nothing about the operation:

```csharp
var command = new Command("apply", "Ensure the target exists, then apply pending work.");
command.SetAction((parseResult, ct) =>
    CliRunner.ApplyAsync(parseResult.GetValue(connectionOption), parseResult.GetValue(sqlDirOption), ct));
```

- `SetAction`'s delegate receives a `CancellationToken` — thread it through the runner and the engine. Sync body → wrap in `Task.FromResult(...)`.
- **Disable the default exception handler** so action exceptions surface as a clean one-liner, not a stack trace, and map to exit codes:

```csharp
var configuration = new InvocationConfiguration { EnableDefaultExceptionHandler = false };
return await CliCommands.Build().Parse(args).InvokeAsync(configuration);
```

- **Pin an exact `System.CommandLine` 2.0 line.** The package churned through `2.0.0-beta*` (breaking changes across betas) before the non-prerelease
  line landed in 2026. Write handler signatures against the **final 2.0 API**, not a beta tutorial. The copy inside the `dotnet` muxer is
  un-referenceable — add the NuGet package explicitly.

---

## Exit codes — three tiers

Map exceptions to codes in the top-level `catch`. A consumer (CI, a script) branches on the tier:

| Code | Meaning | Sources |
|---|---|---|
| `0` | success | normal operation |
| `1` | **validation** | bad config, missing file/dir (`DirectoryNotFoundException` / `FileNotFoundException`), drift (`MigrationDriftException`) |
| `2` | **execution** | runtime/DB failure, **destructive-op guard tripped** |

```csharp
catch (Exception ex)
{
    Console.Error.WriteLine($"✗ {ex.Message}");
    return ex switch
    {
        MigrationDriftException                              => 1,   // validation: drift is a validation failure
        DirectoryNotFoundException or FileNotFoundException  => 1,
        _                                                    => 2,   // execution
    };
}
```

- **Drift / precondition mismatch is `1`, not `2`** — a validation failure, not an execution failure. Don't blanket-map every non-zero outcome
  to `2`.
- The **guard-tripped** path returns `2` directly from the runner, without throwing.

---

## Destructive-op guard

Any verb that mutates or removes state (rollback, repair, truncate, force-reset) MUST gate on the **target resource**, not on the environment.

- **Gate on the target, not `ASPNETCORE_ENVIRONMENT`.** A standalone local tool runs under whatever the developer's shell has (often unset → looks
  non-prod) while the connection flag may point straight at production. Env is at most an **additional** block, never the sole axis.
- Require **`--i-understand-this-is <target>`** to match the operation's actual target — derive the target from the resolved input (e.g.
  `new NpgsqlConnectionStringBuilder(conn).Database`), compare with `StringComparison.Ordinal`, refuse on mismatch.
- Then prompt **`[y/N]`** unless **`--force`** is passed.
- On refusal, write the correct re-run hint and **return the execution code (`2`)** — do not throw.

```csharp
private static bool ConfirmDestructiveTarget(string? connection, string? confirmTarget, bool force)
{
    var target = new NpgsqlConnectionStringBuilder(ResolveConnection(connection)).Database ?? "(unknown)";

    if (!string.Equals(confirmTarget, target, StringComparison.Ordinal))
    {
        Console.Error.WriteLine($"✗ Destructive op refused. Re-run with --i-understand-this-is {target} to confirm.");
        return false;   // caller returns 2
    }
    if (force) return true;

    Console.Write($"This will modify '{target}'. Continue? [y/N] ");
    return Console.ReadLine()?.Trim() is "y" or "Y" or "yes" or "YES";
}
```

- Scope the guard to the path that actually mutates. A read-only verb with a destructive sub-mode (e.g. `verify` vs `verify --repair`) guards **only**
  the destructive flag, leaving the read path prompt-free.
- The engine's destructive surface stays disabled by default — the host opts in per-call (`AddDatabaseBespokeMigrations(dir, o => o.AllowRollback =
  true)` only on the guarded verbs). Never hard-wire the engine open.

---

## Secret hygiene

- **Never echo the connection / password** — not in logs, not in error output, not in the fail-fast searched-list. Redact before printing.
- **Prefer env or stdin over a plaintext flag.** A `--connection` value lands in shell history and `ps`. Offer `--connection-env NAME` /
  `--connection-stdin`; treat the raw `--connection` flag as a one-off convenience, not the recommended path.
- Commit only **templates** with `${ENV}` interpolation. An **unset `${VAR}` is a hard fail**, never a silent empty password.

---

## Config resolution order

Resolve each input **flag → env → discovered default**, highest precedence first, in a single helper per input. Fail fast on a true miss with the
**full searched list** (password redacted):

```csharp
public static string ResolveConnection(string? flag) =>
    flag
    ?? Environment.GetEnvironmentVariable("{TOOL}_DB_CONNECTION")
    ?? DefaultConnection;                               // localhost default for the canonical dev layout only
```

| # | Source | Notes |
|---|---|---|
| 1 | CLI flag (`--connection`, `--sql-dir`) | one-offs; secrets prefer env/stdin (above) |
| 2 | Env var (`{TOOL}_DB_CONNECTION`, `{TOOL}_SQL_DIR`) | preferred for secrets |
| 3 | Discovered default | a localhost/convention default for the **canonical layout only** — overridable, never a universal hardcoded path |

- When discovery is ambiguous (multi-project repo, manifest root ≠ source dir), the flag is **required** rather than guessed.

---

## Composition root + cancellation

The CLI brings the concrete DI container; the engine references only `*.Abstractions`. Build a `ServiceProvider` per invocation, register the engine
via `AddDatabaseBespokeMigrations`, resolve `IMigrationRunnerService`, run:

```csharp
await using var provider = new ServiceCollection()
    .AddSingleton(dataSource)
    .AddLogging()
    .AddDatabaseBespokeMigrations(ResolveSqlDir(sqlDir), options => options.AllowRollback = allowRollback)
    .BuildServiceProvider();

return await provider.GetRequiredService<IMigrationRunnerService>().ApplyPendingAsync("cli", ct);
```

- `await using` the provider — engine resources (data sources, connections) dispose on exit.
- **Honor Ctrl-C.** System.CommandLine supplies the `CancellationToken` to `SetAction`; thread it through the runner into every engine call so an
  interrupted operation cancels cleanly rather than tearing down mid-write.
- Keep `Program.cs` thin: set provider-wide knobs (e.g. `DefaultTypeMap.MatchNamesWithUnderscores = true` for Dapper snake_case), build + parse +
  invoke, map exit codes. Tree shape lives in `CliCommands`; bodies + DI in `CliRunner`.
