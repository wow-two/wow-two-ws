# Deep-copy library research and .NET 10 experiments

Date: 2026-09-12. Scope: data graphs only; isolated library experiments, not SDK source changes.

## Verdict status

**FastCloner is the confirmed library choice, recorded in the prototype convention on 2026-09-12.** Exact-package verification of the 3.5.6 runtime/reflection API remains outstanding under SDK sweep C26. The pending approval is the tool's network-access request for NuGet restore, not a request for another library decision. Selection does not claim the prepared experiment has passed. Its current metadata and explicit hash-collection handling support the selection; no general-purpose library receives an "any object" guarantee.

**DeepCloner 0.10.4 is rejected for the proposed general data-graph default:** four reproduced failures break lookup of cloned keys in reference-comparer HashSet/Dictionary collections on .NET 10. Its broader object-copy tests passed; the objection is concrete collection behavior, not age alone.

## Current stable packages and maintenance

Version dates are from the primary NuGet package pages retrieved for this analysis. "Compatible" metadata is distinguished from actual execution below.

| Package ID | Stable version/date | Repo / license | Assessment |
|---|---|---|---|
| `FastCloner` | `3.5.6`, 2026-08-18 | `lofcz/FastCloner`, MIT | Active 2026 releases; actual net10.0 asset and no package dependencies. Leading reflection candidate. |
| `FastCloner.SourceGenerator` | `1.2.4`, 2026-08-25 | `lofcz/FastCloner`, separate generator package | Separate API/semantics; not assumed equivalent to reflection. |
| `DeepCloner` | `0.10.4`, 2022-04-29 | `force-net/DeepCloner`, MIT | Old release, netstandard1.3/net40 assets; runs on net10 but fails two tested graph cases. |
| `DeepCloner.Core` | `0.1.0`, 2024-02-03 | `adimosh/DeepCloner`, MIT | Modernization fork with net6/7/8/net462 assets; net10 compatibility computed by NuGet, not locally tested. No stronger recent release evidence. |
| `PanoramicData.DeepCloner` | `1.0.8`, 2026-04-16 | `panoramicData/PanoramicData.DeepCloner`, MIT declared in package readme | Maintained fork, actual net10.0 asset; not tested. Readme still claims netstandard2.0; linked origin label says FastDeepCloner but points to force-net/DeepCloner. Documentation inconsistency reduces confidence. |
| `Riok.Mapperly` | `4.3.1`, 2025-12-22 | `riok/mapperly`, Apache-2.0 | Maintained generated mapping tool; latest preview is 5.0.0-next.11 (2026-09-01), not selected as stable. Better for declared transformations than transparent runtime graph duplication. |

Primary package sources: [FastCloner](https://www.nuget.org/packages/FastCloner), [generator](https://www.nuget.org/packages/FastCloner.SourceGenerator), [DeepCloner](https://www.nuget.org/packages/DeepCloner), [DeepCloner.Core](https://www.nuget.org/packages/DeepCloner.Core), [PanoramicData fork](https://www.nuget.org/packages/PanoramicData.DeepCloner), [Mapperly](https://www.nuget.org/packages/Riok.Mapperly).

## APIs and compatibility limits

### FastCloner

Use the explicit runtime API `FastCloner.FastCloner.DeepClone<T>(source)` for this experiment. The repository distinguishes this from generated `FastDeepClone()`. Current documentation discusses hybrid AOT fallback and selective identity preservation; the generator additionally needs identity and polymorphism declarations in some cases. This does not establish that reflection cloning is universally NativeAOT-safe. No NativeAOT/trimming publish is tested here. [Repository](https://github.com/lofcz/FastCloner)

The package documentation describes private-member support and rebuilding identity-hash collections, rather than blindly copying their stored hash tables. The prepared tests exercise those claims. No ignore/reference/shallow behaviors or custom global clone settings are configured. Those mechanisms would intentionally weaken whole-graph isolation and need explicit separate contracts. [Package contract](https://www.nuget.org/packages/FastCloner)

### DeepCloner and forks

Original DeepCloner describes runtime-generated cloning over internal state, rather than constructor/property mapping, and documents cycles and runtime-derived types. Full graph claims do not supersede measured failures. Reflection/runtime code generation is not an AOT promise. [Original repository](https://github.com/force-net/DeepCloner)

DeepCloner.Core describes the same runtime-generation/internal-state approach. Its latest package alone does not prove reference-key rehashing was fixed; this fork was not run. [Fork repository](https://github.com/adimosh/DeepCloner)

PanoramicData exposes the same style of deep/shallow clone API and runtime generation; no verified AOT claim or tested advantage over FastCloner was found in the reviewed package page. It remains a credible fallback candidate if FastCloner's exact package fails, not the selected default. [Package](https://www.nuget.org/packages/PanoramicData.DeepCloner)

### Mapperly

`UseDeepCloning = true` is opt-in; the default may reuse compatible objects. [Mapper configuration](https://mapperly.riok.app/docs/configuration/mapper/)

Shared identity/cycles require `UseReferenceHandling = true`, with runtime assets available for the reference handler. [Reference handling](https://mapperly.riok.app/docs/configuration/reference-handling/)

Private members can use explicitly enabled .NET 8+ unsafe accessors without reflection; they are not all automatically included by ordinary accessibility settings. [Private members](https://mapperly.riok.app/docs/configuration/private-members/)

Runtime-derived types need known derived mappings. It does not discover and duplicate arbitrary unseen runtime subtypes. [Derived mappings](https://mapperly.riok.app/docs/configuration/derived-type-mapping/)

Init-only/constructor reference loops have explicit diagnostic limitations. Get-only data and collection comparer preservation need inspection of the generated mapping/custom factories; no universal clone contract was verified for them here. [Diagnostics](https://mapperly.riok.app/docs/configuration/analyzer-diagnostics/)

**Rationale:** use Mapperly for an explicitly declared projection/transformation or bounded generated copy; it is not the preferred default for copying arbitrary supported data graphs while retaining runtime types, private state and aliases. No local Mapperly package test was performed in this bounded comparison.

## Executed control: DeepCloner 0.10.4

Environment: SDK `10.0.300`, target `net10.0`, runtime `.NET 10.0.8`, `Arm64`; cloner assembly informational version `0.10.4.0`. Restored from existing cache with cleared NuGet sources.

**32 assertions: 28 passed, 4 failed.**

Passed:

- Sealed record root receives a new reference.
- Runtime-derived class type and its mutable member are preserved/copied.
- Root/nested cycles point into the cloned graph.
- Shared aliases survive through properties, list, dictionary, private field and get-only property.
- Private readonly list, init property and get-only mutable list are isolated.
- Constructor is not rerun.
- OrdinalIgnoreCase dictionary/set behavior survives.
- A custom case-insensitive comparer works.
- Mutating all tested cloned members leaves the original graph intact.
- An acyclic graph also preserves aliases and original isolation.

Failed:

1. A cloned `HashSet<Node>(ReferenceEqualityComparer.Instance)` contains the cloned node by enumeration but cannot find it with `Contains(clonedNode)`.
2. A cloned `Dictionary<Node,string>(ReferenceEqualityComparer.Instance)` cannot look up the cloned node key.

3. A default-comparer `HashSet<CompositeKey>` cannot find its cloned record key when the record has `(int Id, List<string> Parts)` members.
4. A default-comparer dictionary with the same record key cannot look up its cloned key.

The record-key aliases are preserved and the nested list is isolated, but lookup fails. Scalar-only `(int Id, string Part)` record keys pass in both set and dictionary. This shows why merely overriding `GetHashCode` does not establish that a key's hash survives deep copying: synthesized record hashing includes each member's equality/hash behavior, and `List` contributes reference identity.

The cloned-key lookup failures are consistent with copied stored identity hashes; the test proves the broken lookups, not a full internal implementation trace. The same graph's ordinary string/comparer collections work. This matters for entity graph navigation collections, where reference comparers were the mitigation identified by the preceding EF experiment.

## FastCloner execution status

Prepared 32-assertion source: `/private/tmp/be-deep-clone-experiment/Program.cs`.

Initial sandbox restore failed `NU1301`, DNS resolution unavailable for `api.nuget.org`. Escalated restore request is pending; no denial or successful package result has been returned yet. The package has therefore **not yet been executed** in this report revision.

## Adopted boundary; executable verification outstanding

- Clone detached, owned, in-memory data graphs when independent mutable state is required.
- Treat a clone as a separate object graph with copied identity values, not a fresh database identity or a replacement for an already tracked entity.
- Preserve cycles/shared aliases and collection comparer behavior; test them at the SDK clone adapter contract.
- Use ordinary `with` when intentionally shallow copying scalar/immutable members; request deep cloning explicitly where nested mutable state must be isolated.
- Exclude service providers, live EF contexts/proxies, streams, sockets, native handles, synchronization objects, callbacks and other live resources from the general data-clone contract.
- Do not claim clone operations validate domain invariants. In particular, the demonstrated internal-state path does not rerun constructors.
- Keep NativeAOT support separate until the selected generated path is published and executed with representative graph types.
- Existing invalid hash collections are not repaired by a general cloning promise; custom/stateful comparers or new unusual data types need representative behavior checks.

These are bounded contract implications, not an obligation to invent a universal clone framework or expand the SDK's scope to resources.

## Commands and artifacts

Prepared candidate command (initial failure, escalation pending):

```sh
dotnet restore /private/tmp/be-deep-clone-experiment/experiment.csproj --configfile /private/tmp/be-deep-clone-experiment/NuGet.Config --disable-parallel
```

Executed control:

```sh
dotnet restore /private/tmp/be-deep-clone-control/experiment.csproj --configfile /private/tmp/be-deep-clone-control/NuGet.Config
dotnet run --project /private/tmp/be-deep-clone-control/experiment.csproj --no-restore
```

Control source uses the same assertions with `using CloneApi = Force.DeepCloner.DeepClonerExtensions;`; candidate uses `using CloneApi = FastCloner.FastCloner;`.

- `/private/tmp/be-deep-clone-experiment/Program.cs` — candidate source.
- `/private/tmp/be-deep-clone-experiment/experiment.csproj` — exact FastCloner pin.
- `/private/tmp/be-deep-clone-experiment/NuGet.Config` — only official NuGet source.
- `/private/tmp/be-deep-clone-experiment/global.json` — SDK pin.
- `/private/tmp/be-deep-clone-control/Program.cs` — executed control source.
- `/private/tmp/be-deep-clone-control/experiment.csproj` — DeepCloner pin.
- `/private/tmp/be-deep-clone-control/NuGet.Config` — offline cache-only restore.
- `/private/tmp/be-deep-clone-control/results.txt` — full observed control output.

Reproduction scripts: `sh /private/tmp/be-deep-clone-experiment/run.sh` and `sh /private/tmp/be-deep-clone-control/run.sh`. The control's program intentionally returns exit code 1 while its four assertions fail; the initial capture commands printed the output with a subsequent `cat`, so their outer shell result was 0. Judge the recorded `SUMMARY` rather than that wrapper status.
