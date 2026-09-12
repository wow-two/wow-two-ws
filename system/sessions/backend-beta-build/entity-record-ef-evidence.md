# Sealed record versus sealed class: EF Core experiment

Date: 2026-09-12. Decision under review: P01, entity representation. Scope: isolated temporary experiment; no workspace or SDK file changes.

## Result

All **20 assertions passed**. An assertion can confirm an expected failure: the duplicate-key exceptions and default-HashSet failures below were observed, not hidden by the pass count.

The tested `sealed record` entities inserted, materialized, tracked scalar changes, and persisted repeated mutations normally. A record `with` copy updated successfully in a fresh context. Attaching another instance with the same key to a context already tracking the original failed for **both** a record `with` copy and a manually cloned class. That conflict alone is not a record-specific disadvantage.

The concrete record-specific cost observed here is synthesized value equality in a navigation `HashSet`: equal transient children collapsed before EF saw both; changing a scalar used in the hash made a loaded child unfindable/removable through that set. `ReferenceEqualityComparer.Instance` fixed both cases. The plain class with default reference equality did not exhibit either problem.

These results do not justify a blanket claim that EF cannot track records. They support explicit collection-equality and copy/tracking rules if entity records remain the convention. They do not choose the convention on the user's behalf.

## Environment

| Item | Observed version |
|---|---|
| .NET SDK | `10.0.300` |
| Target framework | `net10.0` |
| Runtime | `.NET 10.0.8` |
| Process architecture | `Arm64` |
| EF Core / relational / SQLite provider | `10.0.3` |
| Microsoft.Data.Sqlite.Core | `10.0.3` |
| SQLitePCLRaw packages | `2.1.11` |
| Native SQLite | `3.49.1` |

SQLite ran through an open in-memory connection shared by fresh contexts. This uses a relational provider and actual SQL persistence, not EF's InMemory provider. `EnsureCreated` was used only for this temporary test database. Entity keys are generated integer primary keys; other properties are mutable string `Name` and nullable integer `GroupId`. Relationships are unidirectional, with a class parent and record/class dependent navigation sets. No custom entity equality implementation was added.

## Observations

Source locations below refer to `/private/tmp/be-record-ef-experiment/Program.cs`.

| Scenario | Record outcome | Class comparison | Source |
|---|---|---|---|
| Insert and generated key | Pass; ID assigned | Pass | `Program.cs:35` |
| Materialize, mutate, detect changes | `Modified` | `Modified` | `Program.cs:44` |
| Save, mutate again, save, fresh read | Both changes persist | Same | `Program.cs:52` |
| Track original, `Attach` same-key clone | `InvalidOperationException` | Identical category/message | `Program.cs:59` |
| Track original, `Update` same-key clone | `InvalidOperationException` | Identical category/message | `Program.cs:59` |
| Track original, attach value-equal `with { }` copy | `==` true; reference equality false; tracking conflict | Not needed for this additional equality case | `Program.cs:74` |
| Detached copy, fresh-context `Update` | Changed value persists | Manual class clone also persists | `Program.cs:82` |
| Detached copy, fresh-context `Attach` alone | Zero writes | General Attach behavior, class repetition omitted | `Program.cs:97` |
| Detached copy, `Attach`, mark `Name` modified | One row written; fresh read correct | General state-setting API, class repetition omitted | `Program.cs:102` |
| Tracked original, `CurrentValues.SetValues(copy)` | One row written; original remains tracked instance | Class repetition omitted | `Program.cs:111` |
| Default navigation HashSet, two equal new children | Second `Add` false; only 1 child reaches SQL | Both children persist | `Program.cs:119` |
| Reference-comparer navigation HashSet, two equal new children | Second `Add` true; both children persist | Both children persist | `Program.cs:119` |
| Loaded child, mutate scalar, default HashSet remove | `Contains` changes true→false; `Remove` false; relationship remains | `Remove` true | `Program.cs:141` |
| Loaded child, mutate scalar, reference-comparer set remove | `Contains` remains true; `Remove` true; relationship severed | `Remove` true | `Program.cs:141` |
| Mutate tracked record scalar, `Find` and `Entry` | Both return same original reference | Baseline class behavior already tested | `Program.cs:176` |

Expected exception text, substituting entity type:

```text
The instance of entity type 'RecordEntity' cannot be tracked because another instance with the same key value for {'Id'} is already being tracked. When attaching existing entities, ensure that only one entity instance with a given key value is attached. Consider using 'DbContextOptionsBuilder.EnableSensitiveDataLogging' to see the conflicting key values.
```

## Mechanisms kept separate

### Tracking and database identity

- Distinct references with the same persisted primary key conflict in one tracking context, regardless of whether a class was manually copied or a record was copied by `with`.
- The unchanged `with { }` copy compares equal to the original but still conflicts as a second instance. Value equality does not make the copy the tracked original.
- A changed record hash did not break the observed EF `Find`/`Entry` lookup or scalar persistence.
- A fresh context can update the record copy; `with` is useful in this detached workflow.
- `CurrentValues.SetValues(copy)` is a demonstrated way to transfer copied scalar values to the already tracked original.
- `Attach` alone does not infer that detached values differ from database values. Explicit property state or `Update` is necessary in the demonstrated copy workflow. This is not a record-specific defect.

### Navigation equality

- The two transient record children initially both had `Id = 0`, identical names and null `GroupId`. The default HashSet discarded the second before `db.Add(group)`. This is collection equality, not EF's primary-key identity resolution.
- In the loaded-child case, the record was inserted into the HashSet with its persisted key. Only `Name` changed. The changed synthesized hash meant default `Contains`/`Remove` could not find even the same reference. Because removal never happened, EF correctly retained the relationship when saving.
- With `ReferenceEqualityComparer.Instance`, scalar changes did not change set membership and removal severed the nullable relationship as intended.
- The class controls use compiler-default reference equality. A class that implements equivalent mutable value equality would inherit the same collection hazards; `sealed class` does not inherently prevent an explicit override.

## Boundaries

- This is evidence for the listed mechanisms on one EF Core/provider/runtime combination, not universal conformance proof across every EF feature or provider.
- No lazy-loading proxies, inheritance, owned/complex value objects, concurrency tokens, bidirectional record graphs, serializer behavior, graph-wide `Update`, or performance benchmarks were tested.
- `with` shallow-copy semantics and record `ToString`/validation issues belong to the parent's separate BCL analysis. The EF experiment does not use those concerns as a reason to change entity representation.
- SQL command text was not captured. Persistence was verified through row counts and values queried from fresh contexts where specified.
- The navigation hash-mutation loop selects a changed hash explicitly because string hashes are process-randomized; it does not assume a fixed hash value.
- No SDK source, build, dependency pin or convention file was modified.

## Reproduction and artifacts

Permanent source and captured output: [retained experiment](experiments/record-ef/record-ef.md).
The temporary paths below record the original execution location.

Run:

```sh
sh /private/tmp/be-record-ef-experiment/run.sh
```

Exact commands in the script:

```sh
cd /private/tmp/be-record-ef-experiment
dotnet --version
dotnet restore experiment.csproj --configfile NuGet.Config --ignore-failed-sources
dotnet run --project experiment.csproj --no-restore
```

Additional version inventory command run:

```sh
dotnet list /private/tmp/be-record-ef-experiment/experiment.csproj package --include-transitive --no-restore
```

`NuGet.Config` clears package sources; restore succeeded entirely using the existing global package cache. `global.json` pins SDK `10.0.300`. Warnings are treated as errors. Initial restore emitted a platform `CSSM_ModuleLoad` diagnostic but exited successfully; build/run exited `0` with `SUMMARY passed=20 failed=0`.

Files:

- `/private/tmp/be-record-ef-experiment/Program.cs` — complete source and assertions.
- `/private/tmp/be-record-ef-experiment/experiment.csproj` — exact target and package reference.
- `/private/tmp/be-record-ef-experiment/global.json` — SDK pin.
- `/private/tmp/be-record-ef-experiment/NuGet.Config` — cache-only restore configuration.
- `/private/tmp/be-record-ef-experiment/run.sh` — reproduction script.
- `/private/tmp/be-record-ef-experiment/results.txt` — complete captured run output.
- `/private/tmp/be-record-ef-experiment/packages.txt` — all resolved direct/transitive package versions.
- `/private/tmp/be-record-ef-experiment/obj/project.assets.json` — actual resolved restore graph.

This report's conclusions use executed local experiments; no external authority is required to accept them.
