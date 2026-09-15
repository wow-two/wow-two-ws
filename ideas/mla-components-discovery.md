# MLA components discovery

*Last updated: 2026-08-17*

> Every small self-sufficient thing our .NET codebases declare, sorted against the layer-3 gate.
> Purpose — decide which earn a doc in `mla/components/`, now that `mla/constructs/` holds the layer-2 roles.
> Use case — read before writing a component doc; carries the evidence, the sort, and the developer-only calls.

Read: `wow-two-sdk.backend.beta` (637 `.cs`) · `forever-pin` · `ventures.tnis` · `wow-two-platform/*`.

## Verdict

- 5 genuine layer-3 components beyond `time`: `Settings` · `Json` · `Exception` · `LogMessages` · `Diagnostics`.
- Strongest three: `Settings` (49 declared), `Json` (4 seams, keep-list authority `—`), `Exception` (25, no owner).
- `Settings` passes — the config binder is framework, not a collaborator; the reading that also lets `time.md` pass.
- 6 fail as inert-alone → `constructs/`: `Options` (109) · `Spec` · marker · attribute · assembly · delegate.
- 1 unresolved: 11 pure static transforms contradict `constructs/behavior/mapper.md` — § *Open* 1.

**Calibration.** The gate demonstrates by "declare it in a service with no domain, and use it" — so framework
machinery (`IServiceCollection`, the config binder, `ILogger`, `ActivitySource`) counts as present. A candidate
fails only when it needs **another type of ours**. `time.md` passes on that reading: `TimeProvider` is BCL.

---

## Candidates

| Candidate | What it is | n | Example `file:line` | Gate | Home |
|---|---|---|---|---|---|
| `Settings` | a config section bound into a record | 49 | `ClassifierSettings.cs:5` | yes | `components/` |
| `Json` | one type's persisted JSON seam | 4 | `StyleSpecJson.cs:7` | yes | `components/` |
| `Exception` | a thrown type carrying one failure | 25 | `MasterKeyFormatException.cs:5` | yes | `components/` |
| `LogMessages` | a `[LoggerMessage]` partial static class | 30 | `SagaCoordinator.cs:253` | yes | `components/` |
| `Diagnostics` | an `ActivitySource` + instrument names | 2 | `MessagingDiagnostics.cs:6` | yes | `components/` |
| static transform | `static class` of pure in→out methods | 11 | `WordTokenizer.cs:6` | yes | contested — Open 1 |
| named-value holder | `const` block, non-`Constants` name | 22 | `TransportContracts.cs:8` | yes | `lla:constants` |
| enum | a closed set of named options | 164 | `CaseStyle.cs:4` | yes | `lla:enums` |
| guard extension | throwing `IGuardClause` extension | 1 | `IdentifierGuardExtensions.cs:7` | yes | `lla:extensions` |
| `Options` | knobs a single owner reads | 109 | `HashChainOptions.cs:4` | no | `constructs/` |
| `Spec` | declarative shape a renderer consumes | 7 | `StyleSpec.cs:5` | no | `constructs/` |
| marker interface | empty interface a scanner finds types by | 6 | `MessagingContracts.cs:13` | no | `constructs/` |
| attribute | a property mark a reflector reads | 1 | `EnvironmentVariableAttribute.cs:5` | no | `constructs/` |
| assembly marker | empty `static class` naming an assembly | 4 | `ApplicationAssembly.cs:4` | no | `constructs/` |
| delegate | a named signature a pipeline invokes | 2 | `ConsumeFilter.cs:6` | no | `constructs/` |

SDK paths are under `wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/`; the full path is
given in § *Passes* and § *Fails* wherever it is not.

---

## Passes

### `Settings`

Documented today at `mla/constructs/data/settings.md` — layer 2. It also clears layer 3, so the rules below belong
in a `components/settings.md`; the construct doc would keep only the role and the `Settings` vs `Options` line.

- self-sufficient: a record, a section, and `AddEnvironmentOverlaidOptions<T>` make a complete runnable service.
- naming — `sealed record`, suffix `Settings`, named for the section: `ClassifierSettings`, `GitHubOAuthSettings`.
- location — a `Settings/` folder, one file per record; every repo sampled does this.
- shape — `init`-only properties, `required` wherever the value has no safe absence.
- no defaults — `Tnis.Infrastructure/Settings/ClassifierSettings.cs:11,15` uses `required`; a missing value fails
  at startup rather than running wrong.
- section name — a `public const string SectionName` (`ClassifierSettings.cs:8`), or the type name, which
  `Foundation/Configuration/ConfigurationLoader.cs:21` defaults to.
- env overlay — secrets carry `[EnvironmentVariable("…")]`:
  `Drydock.Infrastructure/Settings/GitHubOAuthSettings.cs:13,18`.
- registration — `AddEnvironmentOverlaidOptions<T>` registers `T` and `IOptions<T>` as singletons
  (`Foundation/Configuration/ConfigurationLoaderServiceCollectionExtensions.cs:16`).
- doc starter — `Configuration for …`, already fixed by `constructs/data/settings.md`.
- drift to `class` — `ForeverPin.Application/Settings/AuthSettings.cs:4` and
  `SecretsVault.Infrastructure/Settings/AdminAuthSettings.cs:10` declare `class` with `get; set;`.
- drift to defaults — `GitHubOAuthSettings.cs:14,19` seeds `= ""`, trading a startup failure for an `IsConfigured`
  check at `:22`; the no-defaults rule forbids it.

### `Json`

The keep-list row `Json` cites no authority. `mla/platform/responses/serialization.md` governs the **API wire**
contract host-wide — a different lifetime and a different failure mode from one type's persisted seam.

- self-sufficient: the type, a `private static readonly JsonSerializerOptions`, and two methods.
- naming — `{Type}Json` for a seam over one type (`Codes/Models/Style/StyleSpecJson.cs:7`); `{Domain}Options` where
  it builds options for callers (`ForeverPin.Common.Domain/Serialization/Json/JsonbOptions.cs:8`).
- members — `Serialize(T)` then `Deserialize(string?)`; the options stay private.
- lenient read — `StyleSpecJson.cs:21` returns `StyleSpec.Default` on null, blank, or `JsonException`, so an
  unreadable stored descriptor still renders rather than failing the request.
- presets are the sibling shape — `Foundation/Serialization/JsonOptionsPresets.cs:10` exposes `Default` /
  `Indented` as pre-built statics and calls `MakeReadOnly` at `:33`.
- a frozen-instance trap worth its own rule: `Realtime/SignalR/SignalRConventions.cs:39` copies the preset because
  SignalR mutates the options it is handed.

### `Exception`

25 declarations across the SDK, tnis and the platform repos, and nothing documents the type.
`lla/notation/documentation/exceptions.md` governs the `<exception>` doc field, not the declaration.

- self-sufficient: `throw` and `catch` need nothing else present.
- naming — suffix `Exception`, named for the violated rule: `Foundation/Security/MasterKeyFormatException.cs:5`,
  `Messaging/Saga/SagaContracts.cs:131`.
- `sealed` unless something derives — `Foundation/Errors/AppException.cs:4` is the one open base, and
  `Foundation/Validation/ValidationException.cs:6` its only subclass.
- location — an `Exceptions/` folder once a project has more than one; the tnis CLI does
  (`tools/Tnis.Ingestion.Cli/Core/Exceptions/UndeclaredDefectException.cs:7`), the SDK co-locates with the owner.
- throw-versus-return-`AppError` is already under analysis in `ideas/exceptions-analysis.md` — reuse it, § *Open* 4.

### `LogMessages`

30 files use `[LoggerMessage]`. The class takes `ILogger` as a parameter, injects nothing, stores nothing.

- self-sufficient: source-generated statics; `SagaLog.Uncorrelated(logger, …)` compiles and runs alone.
- shape — `internal static partial class`, one `public static partial void` per message.
- name drift is the reason to write it — `SagaLog` (`Messaging/Saga/SagaCoordinator.cs:253`) against
  `MessageObserverNotifications` (`Messaging/Transport/MessageObservers.cs:159`) for the same role.
- `EventId` is hand-allocated in per-module ranges — saga holds `6111`–`6117`; no doc fixes the ranges.
- the generator emits into the declaring type, so a generic owner needs a separate non-generic log class —
  `SagaCoordinator.cs:252` states this in a comment.
- the method name is the event, not the sentence: `InstanceNotFound`, `ConcurrencyExhausted`.

### `Diagnostics`

Thin — 2 instances — but it clears the gate and nothing owns it.

- self-sufficient: `MessagingDiagnostics.Source.StartActivity()` runs with no collector registered.
- shape — the `ActivitySourceName` const, then `public static readonly ActivitySource Source = new(...)`
  (`Messaging/MessagingDiagnostics.cs:9,18`).
- the metrics half is names only — `Messaging/MessagingMetrics.cs:42` holds the meter name plus one const per
  instrument, deferring to OpenTelemetry semantic conventions where one exists.
- naming — `{Module}Diagnostics` for traces, `{Module}Meter` for metrics.
- document it here, or fold both halves into an observability domain doc — § *Open* 5.

---

## Fails

Each is small, and inert until another type of ours exists.

- `Options` — 109 declared, each defined by the one type that reads it; `Foundation/Audit/HashChainOptions.cs:4`
  does nothing until `HashChainSealer` is constructed. No binding, no validation, no registration of its own.
- `Spec` — `Codes/Models/Style/StyleSpec.cs:5` and its 5 siblings are inert until a renderer consumes them.
- marker interface — `Messaging/MessagingContracts.cs:13`, `Data/Abstractions/IEntity.cs:4`,
  `Mediator/Contracts.cs:11,14` exist to be discovered; without the scanner the mark means nothing.
- attribute — `Foundation/Configuration/EnvironmentVariableAttribute.cs:5` needs the reflector at
  `Foundation/Configuration/ConfigurationLoader.cs:28`. 1 instance across every repo read.
- assembly marker — `Tnis.Application/ApplicationAssembly.cs:4` and its 3 siblings need the host scan pointing at
  them; the type is deliberately empty.
- delegate — `Messaging/Transport/ConsumeFilter.cs:6` needs its filter pipeline, `Mediator/Contracts.cs:48` its
  mediator.

---

## Open

1. Pure static transforms — 11 ship as `static class` (`WordTokenizer`, `CaseConverter`, `EnumNameConverter<TEnum>`,
   `CronExpressionParser`, `BlobStoragePath`, `Geohash`, `SqlNaming`, `ComplaintTextNormalizer`,
   `RollingStockNormalizer`, `Geodesy`, `OutcomeAvailabilityMapper`) and only the last carries the `Mapper` suffix
   that `constructs/behavior/mapper.md` mandates. Rename all 11, or recognise the static form as its own component?
2. 22 static classes hold `const` blocks under a non-`Constants` name — `MessageHeaders`, `NormalizedClaimTypes`,
   `KeySizes`, `QuietZone`, `AdminAuthDefaults`, `TrafficAssumptions`. Does `lla/components/constants.md` enforce the
   suffix, or is a domain noun the better name once the values share a subject?
3. `Settings` clears both gates. Does it get a `components/settings.md` beside the construct doc, or does the
   construct doc absorb the layer-3 rules and `constructs/` stay its only home?
4. `ideas/exceptions-analysis.md` (2026-08-18) already covers throw-versus-`Result`. Does the `Exception` component
   doc absorb that analysis, or cite it and carry only naming, `sealed`-ness and folder?
5. `Diagnostics` and `LogMessages` are both observability. One doc each in `components/`, or one `observability`
   doc under `mla/domains/` carrying both?
