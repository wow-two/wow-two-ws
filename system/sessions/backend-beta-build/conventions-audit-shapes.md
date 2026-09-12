# Backend shapes audit

Inspected 2026-09-09. Read-only conventions and SDK audit. No workspace edits. All 27 shapes docs read, 1,929 lines. Paths below relative to conventions/development/backend/dotnet/ unless prefixed. SDK source root: workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/.

## Confirmed material findings

### S01 Test selector misses every conforming product test
- shapes/service/platform/build/directory-build-props.md:49-55 wires runsettings and IsPackable=false under MSBuildProjectName.EndsWith('.Tests').
- shapes/service/architecture/clean/testing.md:53-67 requires .Tests.{Type} and bans bare .Tests. Thus the prescribed selector matches none of the prescribed product project names.
- Closure: use an import-order-safe common test-property mechanism covering Unit/Integration/E2E/specialized tiers. Evaluate resulting properties for each name.
- Secondary correction: directory-build-props.md:49-51 says dotnet test uses Production. This overgeneralizes generic-host behavior to the required WebApplicationFactory host, which defaults to Development. Official source: [Microsoft documentation](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-10.0#sut-environment)
- New convention gap; no corresponding open sweep row.

### S02 Test tiers carry contradictory DB and fixture rules
- shapes/service/architecture/clean/testing.md:27 forbids SQLite in Integration, yet :57-58 defines Integration as below-HTTP repositories/handlers; core/mla/domains/persistence/testing/test-databases.md:22-23,52-65 explicitly permits SQLite for that tier.
- testing.md:92 requires HTTP status in every Integration method name even though Integration has no HTTP. :96 conflates Integration and E2E again.
- testing.md:110-116 tells products to copy an API-identical generic harness for later extraction; test-databases.md:12 mandates consuming the existing SDK harness and forbids hand-rolled fixtures.
- Closure: testing owns tier/name rules; persistence owns DB/fixture selection. Restrict HTTP naming to HTTP tests and replace stale harness-extraction recipe with current SDK entry point.
- New convention gap, not permission to rewrite currently passing tests blindly.

### S03 Test documentation and solution folder naming contradict owners
- testing.md:62 mandates nested README.md; conventions/development/repo/structure/repo-structure.md:97-102 bans it.
- testing.md:5,52,125 and clean/clean.md:17 say lowercase tests/ solution folder; shapes/service/architecture/architecture.md:55-58 mandates PascalCase virtual Tests/.
- Closure: correct folder lead doc and distinguish physical folders from virtual solution folders. New convention gap.

### S04 No-throw mediator claim remains after scoped implementation landed
- shapes/service/platform/responses/results.md:76-77 and problem-details.md:35-36 promise mediator never throws for AppResult and cite ExceptionToResultBehavior.
- Current SDK Mediator/ExceptionHandling/ExceptionMappingInterceptor.cs:13,34-35 carries new name and excludes NullReferenceException/ObjectDisposedException/StackOverflowException/OutOfMemoryException.
- Sweep R5/C11/N98 are closed and document scope: result-capable requests entering pipeline, exclusions preserved.
- Closure: state guarantee once with pre-pipeline/opt-out/no-failure-arm/programmer-process-error boundaries, update symbol, link other docs. Convention follow-through of closed work, not another broad SDK conversion.

### S05 Results have incompatible core and transport scopes
- results.md:33-40 selects Result by failure mode; core/mla/constructs/behavior/service.md:42 mandates Result for every Service and bans bare return. Sweep N69 explicitly rejects role-based blanket wrapping.
- results.md:65 requires failures crossing boundaries to be AppError/subtype; :19,86-93 permits typed enum/sealed failures that are explicitly not AppError subclasses.
- results.md:21-26 mandates shared carrier representation/style, while core/mla/constructs/data/result.md:36-51 mandates operation-named sealed records. Core obligations are duplicated in a service shape, contrary to shapes/shapes.md:36-37.
- Closure: shared failure/carrier rule under core, service mapping at HTTP owner, explicit boundary for typed-to-AppError map. Coordinate with core audit; do not coin a new taxonomy independently.

### S06 JSON recipe fails its strict wire promise
- shapes/service/platform/responses/serialization.md:12-13 forbids numeric enum output but names JsonStringEnumConverter(JsonNamingPolicy.CamelCase), whose allowIntegerValues default is true. Undefined enum values serialize as numbers. Current SDK Web/Json/JsonControllerBuilderExtensions.cs:16,47 uses same constructor.
- Official source: [Microsoft documentation](https://learn.microsoft.com/en-us/dotnet/api/system.text.json.serialization.jsonstringenumconverter.-ctor?view=net-10.0)
- serialization.md:25-26 recommends AddControllers().AddJsonStringEnums() over preset but never installs preset. SDK JsonControllerBuilderExtensions.cs:13-17 changes only converters; :22-27 has actual AddControllersWithSdkJson() preset method. AddApiDefaults registers no controllers.
- Closure: document actual full-preset method; settle strict enum behavior; verify named/unnamed enums, null omission, dictionary keys through configured controller. Add SDK implementation rows if convention retained. Existing N24 concerns storage, not this wire gap.

### S07 TimeSpan ISO-duration promise has no implementation
- serialization.md:16 promises ISO-8601 for TimeSpan. SDK Foundation/Serialization/JsonOptionsConstants.cs:18-34 installs Web/NodaTime with no ISO TimeSpan converter.
- Framework format is e.g. 2.00:00:01, not ISO duration P2DT1S. Official source: [Microsoft documentation](https://learn.microsoft.com/en-us/dotnet/core/compatibility/serialization/6.0/timespan-serialization-format)
- Closure: name actual format or approve ISO converter and add SDK task; one interoperable example. New gap beyond N24.

### S08 Host recipe contradicts host ownership and itself
- shapes/service/platform/startup/host-configuration.md:16-22 bans non-host config and registration, but illustrates layer setting injection as AddPersistence(IServiceCollection,IConfiguration), passing whole config instead of bound setting; same name explicitly banned :140-141.
- :202-203 requires every domain concern, including settings, in one domain method; :191 and :254-257 require every Settings record in separate AddSettings(). core/mla/components/settings.md:55 duplicates that requirement.
- :264 mandates AddEnvironmentOverrides without declaring a body, despite :146-147 banning phantom methods and sweep Phantom symbols recording its removal. Default CreateBuilder already loads env sources; whitelist rule supplies no provider-removal/precedence recipe.
- Closure: one coherent bound-settings/host-ownership example; settle domain-vs-global settings placement; specify actual env mapping/precedence. Linked to closed phantom and N49/N74 work, not request to revive dead SDK symbols.

### S09 One-owner rule violated by host and folder obligations
- Host-only binding repeats in platform/platform.md:23; startup/startup.md:21; host-configuration.md:16-26,238-243; architecture/clean/clean.md:54.
- Three-group Program/partial class rules repeat in clean.md:51-54; host-configuration.md:38-71,111-124,244-250,560-562.
- Source-folder and role-folder rules repeat in architecture/clean/domain-structuring.md:61-80, while core owns notation/construct naming. :86 assigns folder names to components whereas architecture.md:81-82,102 assigns them to constructs.
- Closure: retain each obligation at lowest shared owner and link inheritors; audit preserves substantive details during compaction. One ownership task, not independent edits per duplicate.

### S10 Clean parent mis-scopes architecture rules
- architecture/architecture.md:38-40 says pattern owns layer/project relationships, no component lists; :84-100 nevertheless enumerates Clean-specific layer placements in arrangement parent.
- clean/clean.md:19 makes every layer class-library although Api is executable host (:16); :20 puts every implementation in Infrastructure although Persistence owns repositories.
- clean.md:43 bans every outbound Domain reference; platform/build/directory-build-props.md:62-73 shows Domain referencing SDK and Common.Domain.
- Closure: Clean placement under Clean; scope implementation/class-library obligations; distinguish forbidden outward architectural dependencies from allowed shared model/value references. Preserve house architecture rather than replace with external preference.

### S11 Domain structuring examples violate its rules
- architecture/clean/domain-structuring.md:19 requires Core with subdomains, but Domain examples :29-35,104-113 have subdomains and no Core.
- :61-62 uses concern names; :70 mirrors Listings/ListingCapturing into Listings/Capturing, duplicating prefixes on one side. :104 still shows Service/Infrastructure despite required project split.
- Closure: one coherent worked tree satisfying selected domain/layer/role rules. New convention gap.

### S12 Boot-floor doc is stale copied SDK surface
- startup/startup-defaults.md:17,36-37 promises root namespace import resolves defaults; current Meta/ApiDefaultsExtensions.cs:21 declares .Meta namespace.
- :71-95 says every concern defaults on, ExposeOpenApi bool/true. SDK Meta/ApiDefaultsOptions.cs:29-30 is bool?/null; ApiDefaultsExtensions.cs:133-135 defaults to Development-only. HTTPS redirect, AllowedHosts, COOP/COEP now exist but copied inventory omits them.
- :114 forbids per-area direct calls; :127-128 advertises per-area composition escape hatch.
- Closure: keep bundle obligation, link source-owned API docs rather than duplicate option inventory; correct import/default/composition posture. C5 already covers COOP/COEP code, no duplicate implementation row.

### S13 Universal middleware sequence lacks conditional constraints
- host-configuration.md:474-475 says fixed slots and equal numbers interchangeable; :507,509 puts rate limiting before authentication universally. An authenticated-principal limiter needs identity established first. Current SDK limiter is per-IP, so no claim that current IP limiting is wrong.
- :498 fixes localization before routing even when provider needs route data. Generic branches marked any inherit dependencies of their contents.
- startup-defaults.md:104-105 requires auth after UseApiDefaults, but it already installs output cache and limiter (SDK ApiDefaultsExtensions.cs:118-125); universal host table places output cache after authorization (:509-514).
- Closure: dependency constraints with explicit policy/provider qualifications, then verify bundle composition for supported cases. Runtime pipeline repro not run; source order read directly.
- Official rate-limit context: [Microsoft documentation](https://learn.microsoft.com/en-us/aspnet/core/performance/rate-limit?view=aspnetcore-10.0)

### S14 Reproducibility is unspecified in build baseline
- platform/build/directory-build-props.md:28,39-44 mandates LangVersion latest but shape has no compiler SDK pin/roll-forward policy; stricter sample :93 uses latest-recommended analyzers too.
- Official warning: latest depends on installed compiler and varies between machines: [Microsoft documentation](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/configure-language-version)
- Closure: define SDK/compiler pin/update policy or use TFM-aligned language default; preserve intentional opt-in if user chooses latest. Missing repeatability rule, not demand to freeze package versions.
- Same pass: shapes/shapes.md:28 incorrectly says Directory.Build.props centralizes package versions, while build/build.md:18-21 correctly says Directory.Packages.props.

### S15 SDK shape openly lacks release and test contract
- shapes/sdk/sdk.md:5 points to dotnet-conventions section Building the SDK itself, now moved into this doc; :27-29 calls restructuring queued although core/shapes exists; :31-35 repeats separators.
- :39-41 declares SDK architecture/delivery/testing unwritten. service/platform/build/directory-build-props.md:116-124 carries SDK package guidance inside service shape instead.
- Closure: add shared SDK build/package-test/release obligations needed by this task; link actual repo layout/release procedure. Define artifact set, version source, restore/build/test/pack evidence, package metadata/assets validation and human-publishing boundary. No invented production-consumer compatibility blocker: user explicitly authorizes radical changes.
- Deliberately unfinished scope now relevant to task, not covert implementation defect.

### S16 Move stale inventories and rationale out of normative owners
- host-configuration.md:271-556 is API inventory, :166-175 rationale; startup-defaults.md:48-95 copies SDK options. Root authoring rules keep surface beside code and rationale elsewhere.
- central-package-management.md:25-35 is history/rationale; testing.md:73,116 is migration history/elided obsolete path; known-endpoints.md:53-62 is one-off migration procedure.
- Closure: retain rules, relocate needed references/rationale to maintained owners, normalize remaining document shape after semantic fixes. This is maintenance/ownership scope, not a cosmetic leaf count.

## Deliberate placeholders and non-findings
- library/library.md:5-11, cli/cli.md:5-11 are explicit shells; CLI's tentative split must not become universal service policy by accident.
- service/topology/topology.md:5-9 and delivery/delivery.md:5-9 are explicit shells. Existing external deployment/repo rules should be linked, not duplicated.
- onion/hexagonal/vertical-slice shells explicitly do not authorize those alternatives; filling them is not necessary to clear an empty-doc count.
- testing.md:134-141 deliberately defers AAA/gist convention. Carry decision; missing XML docs are not violation.
- Old handoff frontend path repairs already exist: serialization.md:7 and launch-profiles.md:18 resolve to frontend core paths.
- Broken host async anchors confirmed: :67,221 target #async-startup, heading :151 is Async startup [REQUIRED] => #async-startup-required. Root owns mechanical repair.
- Package ID WoW2.Sdk.Backend.Beta is real: SDK WoW.Two.Sdk.Backend.Beta.csproj:23. Registry dotted branding is not evidence of a phantom package.
- AppErrorProblemDetailsFactory remains static in SDK Web/ExceptionHandling/AppErrorProblemDetailsFactory.cs:10 despite N60 closed; convention citation is real. Root owns sweep/source status reconciliation.
- Age of version examples alone does not prove invalid recipe.
- AddValidation's Web SDK packaging is contextual; no unsupported claim that every Web SDK host needs manual PackageReference.

## Inventory
Read every line of all files below (not samples):
      11 conventions/development/backend/dotnet/shapes/library/library.md
      11 conventions/development/backend/dotnet/shapes/cli/cli.md
      56 conventions/development/backend/dotnet/shapes/shapes.md
      41 conventions/development/backend/dotnet/shapes/sdk/sdk.md
       9 conventions/development/backend/dotnet/shapes/service/topology/topology.md
      24 conventions/development/backend/dotnet/shapes/service/platform/platform.md
      56 conventions/development/backend/dotnet/shapes/service/platform/responses/problem-details.md
      31 conventions/development/backend/dotnet/shapes/service/platform/responses/serialization.md
      62 conventions/development/backend/dotnet/shapes/service/platform/responses/known-endpoints.md
      93 conventions/development/backend/dotnet/shapes/service/platform/responses/results.md
      21 conventions/development/backend/dotnet/shapes/service/platform/responses/responses.md
      36 conventions/development/backend/dotnet/shapes/service/platform/build/build.md
     120 conventions/development/backend/dotnet/shapes/service/platform/build/central-package-management.md
     124 conventions/development/backend/dotnet/shapes/service/platform/build/directory-build-props.md
     562 conventions/development/backend/dotnet/shapes/service/platform/startup/host-configuration.md
      35 conventions/development/backend/dotnet/shapes/service/platform/startup/launch-profiles.md
      21 conventions/development/backend/dotnet/shapes/service/platform/startup/startup.md
     128 conventions/development/backend/dotnet/shapes/service/platform/startup/startup-defaults.md
       9 conventions/development/backend/dotnet/shapes/service/architecture/hexagonal/hexagonal.md
     111 conventions/development/backend/dotnet/shapes/service/architecture/architecture.md
       9 conventions/development/backend/dotnet/shapes/service/architecture/vertical-slice/vertical-slice.md
       9 conventions/development/backend/dotnet/shapes/service/architecture/onion/onion.md
     141 conventions/development/backend/dotnet/shapes/service/architecture/clean/testing.md
      63 conventions/development/backend/dotnet/shapes/service/architecture/clean/clean.md
     117 conventions/development/backend/dotnet/shapes/service/architecture/clean/domain-structuring.md
       9 conventions/development/backend/dotnet/shapes/service/delivery/delivery.md
      20 conventions/development/backend/dotnet/shapes/service/service.md
    1929 total

Additional reads: conventions/conventions.md, be-forwards.md, be-components-lane.md, SDK sweep (large initial output truncated; affected remaining rows read by targeted queries), full core result doc, full persistence testing doc. SDK full reads: ApiDefaultsExtensions, ApiDefaultsOptions, JsonOptionsConstants, JsonControllerBuilderExtensions, ExceptionMappingInterceptor, AppErrorProblemDetailsFactory. Targeted sections: settings registration, service return rule, repository README/solution rule, package id/version, SDK registry row. Memory search had no relevant hits; no memory evidence used. No runtime tests executed; this is a document and source audit.
