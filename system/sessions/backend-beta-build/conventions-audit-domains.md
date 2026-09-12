# Backend convention audit — components and domains

Date: 2026-09-09. Read-only evidence pass; no convention or SDK source edits.

## Scope and evidence

- Read every Markdown file under `conventions/development/backend/dotnet/core/mla/components/` (11 files, 922 lines) and `domains/` (28 files, 3,054 lines).
- Read `conventions/conventions.md`, dotnet index, `be-forwards.md`, `be-components-lane.md`, SDK `be-convention-sweep.md`, and relevant construct definitions.
- SDK source was consulted only to verify convention citations and examples, not to execute the SDK sweep.
- All Markdown relative file targets in the assigned 39 files resolve. Section anchors and bare backticked legacy paths still require semantic repair.
- Paths below abbreviate `C = conventions/development/backend/dotnet/core/mla`; `S = workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src`.

## Findings and closure checks

### 1. Options registration has incompatible mandatory recipes

Evidence: `C/components/options.md:41-56` mandates construct/invoke/singleton, mandates `AddOptions<T>()`, then permits that same pipeline only for composition/validation. Both positive examples at `:63-82` use direct singletons, violating the mandatory pipeline. The text calls `.Validate()` boot enforcement at `:42-50` without requiring `ValidateOnStart()`. `settings.md:55-67` bypasses the already-shipped validated-settings recipe.

Existing work: N47 closed direct registration for rule-free types; N74 closed `AddValidatedOptions`/`AddValidatedSettings`; N106 closed configured-path bug; N111 remains open to classify registrations. This is conventions reconciliation riding those rows, not a new SDK registration design. `S/Foundation/Options/OptionsRegistrationExtensions.cs:20,44` confirms helpers exist.

Closure: one decision table covers argument-only, direct singleton, validated option/settings, and PostConfigure composition; examples implement it; invalid configured values fail at host startup in the validated path.

### 2. API bodies have three incompatible naming/model prescriptions

Evidence: `C/domains/api/api-messages.md:13` mandates noun-first `NounCreateUpdateApiRequest`; `:89` says top-level requests are verb-first; `C/constructs/data/api-request.md:41` agrees but its positive example `:47` is noun-first. `api-messages.md:24` endorses `StyleApiRequest`; `:88-90` expressly forbids that and requires nested `NounDto`. `api/api.md:11,54` requires ApiRequest per action while `messaging/mediator/mediator.md:85-89` binds Commands directly when no server-only inputs exist. `mediator.md:78` also incorrectly says both API/application requests implement `IRequest<T>`.

Existing work: mostly residual stale alternatives after API/model sweep; no live row fully captures reconciliation.

Closure: settle one top-level request rule, nested DTO rule, and one-model exception; update all examples and links to one owner.

### 3. API edge mapping exception is undocumented against file/folder rules

Evidence: `C/domains/api/api-messages.md:54-56` explicitly requires request and extension class in the same file; `C/mla.md` one-type-per-file exception is only generic/non-generic companion, and the request construct `C/constructs/data/api-request.md:15` inherits it. Also `api.md:16-19` declares project layout inside core, contrary to dotnet index rule that deliverable placement belongs to shapes.

Closure: declare a scoped co-location override with exact backlink or use separate files; route project placement to service architecture. Do not silently copy either contradictory side.

### 4. Messaging result and dispatch contracts contradict themselves

Evidence: `C/domains/messaging/messaging.md:24` mandates operation payload `Result`; `:40` positively returns `AppResult<CodeDto>` despite API model-to-DTO boundary (`api/api-messages.md:47-48`) and result construct `C/constructs/data/result.md:41`. `messaging.md:34` mandates AppResult for every handler, while `mediator/mediator.md:25,37` permits bare query/Unit command; this also ignores notification handlers. `messaging.md:66` forbids handler sub-dispatch while `mediator.md:105` explicitly allows handlers issuing a sub-request.

Existing work: N15/N2 model migration, N69/R3/R7 result decisions are historical; conventions still retain old obligations. Check main sweep for product rows moved out.

Closure: one owner for message kinds, response carriers, payload naming, and nested dispatch; examples demonstrate that owner; distinguish notifications from requests.

### 5. Renamed mediator/validation APIs remain prescribed

Evidence: `C/domains/messaging/mediator/mediator.md:119-142` cites `IPipelineBehavior`, `AddMediatorBehavior`, `LoggingBehavior`, `ValidationBehavior`, `IdempotencyBehavior`, `AuthorizationBehavior`, and `InMemoryIdempotencyStore`. `C/domains/validation/validation.md:50,220,341` repeats old behavior names; `:292-296` says Mapper interfaces still ship as Resolver in Foundation.

Source: `S/Mediator/MediatorServiceCollectionExtensions.cs:75` is `AddMediatorInterceptor`; validation registration `Mediator/Validation/ValidationBehaviorServiceCollectionExtensions.cs:12` is `AddMediatorValidatingInterceptor`; other registrations are Logging/Authorizing/Deduplicating/ExceptionMapping Interceptor. `S/Web/ErrorMapping/` holds `IErrorMessageMapper`/`IFieldErrorMessageMapper`.

Existing work: extend completed N98 (pipeline vocabulary), N12/N13 (Resolver rename), N90 (Web relocation) with convention citation closure. N94 current-user unification remains open; do not pre-rename that citation until implemented.

Closure: no removed public symbol in actionable snippets; inspect signatures rather than replacing suffix text blindly; preserve framework-owned names.

### 6. Result/application ownership is split and exceptions are inconsistent

Evidence: `C/components/result.md:13-19` owns role-independent failure policy but `extensions.md:60-62` encourages avoiding Result and bans all throws except name-marked methods (including ordinary argument guards). `mapper.md:48-51` permits argument guards. Result doc `:28-32` recognizes only `Result<T>` and absence/failure, omitting the shipped typed-failure carrier; `:56` says Match/IsFailure are the entire surface while shape results permits typed cases. `C/constructs/behavior/mapper.md:37` permits failed transformations but `:61,70` says rejected input makes it a Validator; component mapper explicitly permits unmappable tokens.

Existing work: N69, R8, N105 parser carve-out, N101 Parser coining. Settle totality over `Result<output>` vs success-only totality before using this contradiction to coin a new role.

Closure: one failure policy owner links all consumers; documented parser/TryX/throw bridges and programmer-error guard rule; typed failure remains available where intended.

### 7. Value-object rules cannot guarantee their stated invariants

Evidence: `C/components/value-object.md:24-25` demands invalid instances cannot be constructed, while `:34` prescribes init accessors and `:44-47` requires compiler equality, permits excluding members, then forbids hand equality. Constructor-only cross-member guards can be bypassed by `with` initializers; `init` is shallow and mutable member references remain mutable. Compiler equality compares member values with their equality behavior, not collection contents, and cannot omit an ordinary backing field by a comment.

Official verification: [C# records](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/record) documents shallow immutability, member equality, copy/with semantics and allowed typed Equals/GetHashCode overrides.

Closure: explicit construction strategy closes initializer/with bypass; immutable/deep-equality collection strategy; either permit justified custom equality or prohibit identity-excluded stored members. Representative invalid-copy and equal-collection checks should be required when implementing this rule.

### 8. PostgreSQL enum registration example both fails compilation and misses EF mapping

Evidence: `C/domains/persistence/database/postgres/postgres.md:99-103` passes `typeof(ChannelType).Assembly` as the third ordinary argument. Actual `S/Data/EntityFrameworkCore/Postgres/NpgsqlEnumMappingExtensions.cs:18-23` puts `Func<Type,string?>? pgTypeName` there; assembly needs named `assemblies:` or null placeholder. Convention `postgres.md:90-111` says only driver mapping and specifically no dual EF mapping. `ef/ef-mapping.md:75-80` uses external data source with no EF enum registration; `S/Data/EntityFrameworkCore/Postgres/PostgresExtensions.cs:42-46` only adds retry/timeout and optional callback, so no hidden EF mapping repairs this.

Official: [Npgsql enum mapping](https://www.npgsql.org/efcore/mapping/enum.html?tabs=with-datasource) and [Npgsql EF provider](https://www.npgsql.org/efcore/) require mapping both external data source and EF provider.

Closure: compile the example; one discovery helper may feed both levels but both must be configured. Verify insert/query round-trip of a multi-word PG enum with EF, not merely ADO/Dapper registration. This creates an SDK follow-up if bulk mapping currently only exposes driver registration.

### 9. Schema-first rules overreach the explicitly supported EF strategy

Evidence: `C/domains/persistence/access/ef/ef-mapping.md:11-16` universally prohibits Migrate/EF migrations; provider lead `ef.md:12` routes to the supported code-first EF strategy and `migrations/ef/ef-migrations.md:63-75` mandates it. `ef-mapping.md:130-132` narrows only its waste table. Root `persistence.md:11` universally says applied SQL is canonical. `postgres.md:11,17` requires Apply.sql even for code-first products. `entity-configuration.md:66-69` excludes DDL-only mapping for every EF configuration.

Closure: make migration strategy the explicit precondition for SQL-only mapping/DDL bans; keep shared access rules applicable to either strategy; one schema owner per product.

### 10. Entity schema rules contradict their own optional/composite contracts

Evidence: `C/domains/persistence/entities/entity-contracts.md:17,22` permits composite rows but `:20` says every row-owning type must implement IKeyedEntity. `:36` permits optional column members while `database/postgres/postgres.md:24` mandates every new column NOT NULL without an optionality exception. Entity contracts `:40` prescribes a PG enum array in the provider-free entity owner, duplicating Postgres `:55`.

Closure: single-column/composite/keyless rules are mutually exclusive with precise scope; optional storage column rule inherits actual domain optionality; move PG mapping mechanics to PG owner.

### 11. Dapper examples still reference removed global casing

Evidence: `C/domains/persistence/access/dapper/dapper.md:104,151-162` uses nonexistent SqlNamingMapper.ColumnCase/ParameterCase and defaulted Col/Par/ParRef calls. Actual `S/Data/Dapper/SqlNamingMapper.cs:20,26,32,48,53,65` requires explicit CaseStyle per call; its summary `:10-11` denies global state. Dapper doc `:213-222` presents async calls without CommandDefinition/ct despite `:165-166`, returns Task<List<T>> from QueryAsync<T> (normally Task<IEnumerable<T>>), and closing raw literal is two quotes `:222`.

Existing work: N27 closed; N28 marked closed but citations are only mechanically renamed and still wrong. Reopen convention closure without reverting the SDK API.

Closure: compile representative query snippets with current signatures; every cancellable call uses CommandDefinition; one caller-owned SqlNamingOptions flows explicitly.

### 12. SQL migration enum transaction prohibition is factually stale

Evidence: `C/domains/persistence/migrations/sql/migration-dialects.md:105-112,122,131` says ADD VALUE cannot run in a transaction. Supported PostgreSQL permits it but the new value cannot be used until commit.

Official: [PostgreSQL ALTER TYPE](https://www.postgresql.org/docs/current/sql-altertype.html) § Notes.

Closure: distinguish adding an enum label in a transactional migration from using it before commit; reserve no-transaction for actual forbidden statements or explicitly justified add-and-use workflow.

### 13. Concurrent-index recovery example can silently accept an invalid index

Evidence: same `migration-dialects.md:76-92` claims rerun after partial no-transaction execution succeeds through CREATE INDEX CONCURRENTLY IF NOT EXISTS. A failed concurrent build may leave an INVALID index; IF NOT EXISTS skips a same-name relation and does not certify its definition or validity. Retrying can mark the migration complete without a usable index.

Official: [PostgreSQL CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html) § Building Indexes Concurrently and IF NOT EXISTS.

Closure: recovery checks index validity and expected definition; rebuild/drop/retry invalid residue before journaling success. Include an interrupted/failed build scenario in SDK migration follow-up.

### 14. Migration concurrency/rollback contracts claim guarantees providers do not share

Evidence: `C/domains/persistence/migrations/migrations.md:54-56` claims every host's apply is serialized by a DB lock, then equates journal idempotency to locking for DbUp. Provider doc `dbup/dbup-migrations.md:16` expressly disclaims advisory-lock coordination; `:90-96` only describes journaling. Journal skip alone cannot serialize simultaneous pending checks. `sql/sql.md:19` permits missing Rollback when explained; `sql/bespoke-migrations.md:105-106` requires a rollback file and the broker throws if absent. A no-op file is supported by `migration-dialects.md:68`.

Closure: state provider-specific coordination and default deployment topology; distinguish repeatability from concurrency safety; require a no-op Rollback file for irreversible changes, or deliberately change scanner contract.

### 15. Migration docs prescribe obsolete symbols and obsolete surface

Evidence: `sql/bespoke-migrations.md:28-31,47,56-72,121-125,156` cites MigrationConventions, IMigrationSource/*Source, IMigrationScanner/MigrationScannerService, and drift/orphan exceptions. SDK uses MigrationConstants, IMigrationBroker/*Broker, MigrationRunnerService's internal scan, and Result failure paths. `dbup/dbup-migrations.md:29,72-78` cites removed DbUpProviderFactory; `migrations.md:22,32` omits required connectionString argument and `:27` still says bespoke extraction pending. `migration-tooling.md:65,75,85,110,218` prescribes removed CliCommands/CliRunner and MigrationDriftException instead of current CliCommandBuilder/CliRunnerService/result mapping.

Existing work: N6, N81, N87/N88/N89/N92/N98 completed SDK refactors. N104 remains for broker malformed-source failure; separate current failure behavior from pending change.

Closure: match current symbols/signatures in examples; remove rollout history and SDK method inventories from convention layer; retain operational rules and link SDK specs for surface.

### 16. SQLite enum rules conflict with portable enum policy

Evidence: `database/postgres/postgres.md:119` mandates styled string for non-native enum stores; `migrations/sql/migration-dialects.md:162,170` defaults to integer/permits either. `:171-172` permits CHECK(status IN (...)) then says adding a member is code-only; a new value violates that CHECK until migrated.

Closure: one explicit standard or scoped compatibility exception; enum member additions require constraint evolution when stored values are constrained.

### 17. JWT convention overstates shipped safeguards and contradicts config rules

Evidence: `identity/identity.md:20` keys all auth under Identity; `identity/jwt/jwt-auth.md:53,110` uses Jwt:Key/Auth:JwtKey. JWT `:38-39` demands exactly one key source, `:44` claims HTTPS metadata always required. Actual `S/Identity/Jwt/JwtServiceCollectionExtensions.cs:23` rejects neither-present but accepts both, and `:48` disables RequireHttpsMetadata for an http URI. JWT `:10` says SDK has no user model despite shipped Identity/Core models (verified file inventory).

Closure: decide code safeguard vs doc claim with precise trust context; valid/invalid dual-source and metadata-scheme tests during SDK sweep; examples bind Identity Settings through the agreed recipe. Do not broaden into a full security audit here.

### 18. Runtime/testing snippets have stale or unsafe operational assumptions

Evidence: `C/components/time.md:110-119` calls CronExpressionParser statically, but `S/Foundation/Time/CronExpressionParser.cs:8,13,25` is instance. Time `:55` says both registrations TryAdd; overload `TimeServiceCollectionExtensions.cs:30` uses AddSingleton. Its separately documented real-IClock drift is STILL TRUE (`:17,31`), so do not erase that warning as stale. `C/domains/persistence/testing/test-databases.md:112-116` uses process-global DB_CONNECTION and claims clearing on dispose keeps concurrent suites isolated; overlapping host builds still race before disposal.

Existing work: N6 already converted cron; N44 only fixed paths. Clock consistency and concurrent host fixture isolation are new follow-ups if the full SDK sweep confirms no existing row.

Closure: instance cron recipe, accurate registration precedence; deterministic two-clock test; scoped test host configuration or serialized/restored env lifecycle with explicit parallelism limit.

### 19. Validation phases have a self-conflict and incomplete ownership

Evidence: `C/domains/validation/validation.md:64` treats cross-aggregate uniqueness as ValidationError when field-fixable, while `:108-109` says cross-aggregate checks remain AppError. Both can fit only if AppError means umbrella (ValidationError subtype) there; state that explicitly. `:52-56` requires resolving in handler then validation but generic validating interceptor remains registered unless a skip/sequencing mechanism exists. The doc marks async prevalidation as deferred, so this is an operational coverage gap, not proof a particular product is wrong. `:17-20` plus `:134-192` hardwire FluentValidation/Ardalis inside a provider-free domain lead, violating `domains.md:17`.

Closure: unambiguous field-specific vs non-field failure rule; executable way to opt target-bearing commands out of pre-handler validation; provider implementation mechanics moved to provider docs. Preserve deliberately deferred async/ruleset design as open work.

### 20. Rule ownership and component form debt is systematic

Evidence: `components/components.md:59-67` requires Location/Declaration/Content, but added result/mapper/value-object docs omit that shape. Type-doc starters restate constructs in `components/constants.md:24`, `enums.md:24`, `settings.md:25`, `extensions.md:24`. Domain messaging repeats its own cardinality (`:12`/`:64`) and construct naming; Dapper repeats handler inventory at `:64-66`/`:234-236`; ef-mapping repeats entity-configuration call order, summary and location. EF configurations permit tightly-coupled multi-type files (`ef-mapping.md:90`, `entity-configuration.md:15`) without exact one-type-rule override linkage. Provider-rich JWT/HTTP/migrator/time docs inventory SDK option fields despite surface-register ban `components.md:22-23`.

Closure: one owner per obligation, links from other layers; decide whether the component template is still desired and apply consistently; move SDK option/default inventories beside SDK source. Sweep formatting once content is reconciled, not as separate semantic work per repeated sentence.

## Deliberate placeholders and non-findings

- `be-forwards.md` explicitly rejected mirroring every frontend component; result/value-object/mapper are now present. Do not invent 41 backend component gaps from stale counts in handoff.
- `domains/domains.md:39-43` recognizes caching/blob/observability without folders until rules are needed. Empty provider rows for cookie/OAuth/minimal API/vendor SDK are coverage candidates tied to actual rules, not automatically defective missing docs.
- `integrations/integrations.md:49-53` deliberately leaves broker shape/lifetime/config unresolved; async validation, rulesets and read-seam design are explicitly deferred in validation.
- `components/time.md:76-80` clock divergence is a verified limitation, not a stale-doc correction.
- SDK surface inventories are a convention ownership violation; their removal must retain useful operational rules and replace access with a working source/spec link.
- Excerpted examples may omit unrelated properties by the root convention's example rule; absent Id in a table-name illustration was NOT reported as a compilation defect. The Dapper malformed literal/return type and MapEnums argument mismatch concern the exact operations those samples demonstrate.

## Inventory — complete assigned files read
- `conventions/development/backend/dotnet/core/mla/components/components.md` (70 lines)
- `conventions/development/backend/dotnet/core/mla/components/constants.md` (94 lines)
- `conventions/development/backend/dotnet/core/mla/components/enums.md` (83 lines)
- `conventions/development/backend/dotnet/core/mla/components/extensions.md` (133 lines)
- `conventions/development/backend/dotnet/core/mla/components/json.md` (44 lines)
- `conventions/development/backend/dotnet/core/mla/components/mapper.md` (68 lines)
- `conventions/development/backend/dotnet/core/mla/components/options.md` (91 lines)
- `conventions/development/backend/dotnet/core/mla/components/result.md` (76 lines)
- `conventions/development/backend/dotnet/core/mla/components/settings.md` (70 lines)
- `conventions/development/backend/dotnet/core/mla/components/time.md` (129 lines)
- `conventions/development/backend/dotnet/core/mla/components/value-object.md` (64 lines)
- `conventions/development/backend/dotnet/core/mla/domains/api/api-context-building.md` (29 lines)
- `conventions/development/backend/dotnet/core/mla/domains/api/api-messages.md` (92 lines)
- `conventions/development/backend/dotnet/core/mla/domains/api/api.md` (101 lines)
- `conventions/development/backend/dotnet/core/mla/domains/domains.md` (43 lines)
- `conventions/development/backend/dotnet/core/mla/domains/identity/identity.md` (32 lines)
- `conventions/development/backend/dotnet/core/mla/domains/identity/jwt/jwt-auth.md` (148 lines)
- `conventions/development/backend/dotnet/core/mla/domains/integrations/http/http.md` (64 lines)
- `conventions/development/backend/dotnet/core/mla/domains/integrations/integrations.md` (64 lines)
- `conventions/development/backend/dotnet/core/mla/domains/messaging/mediator/mediator.md` (144 lines)
- `conventions/development/backend/dotnet/core/mla/domains/messaging/messaging.md` (78 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/access/access.md` (17 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/access/dapper/dapper.md` (264 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/access/ef/ef-mapping.md` (250 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/access/ef/ef.md` (19 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/access/ef/entity-configuration.md` (77 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/database/database.md` (16 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/database/postgres/postgres.md` (141 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/entities/entity-contracts.md` (77 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/migrations/dbup/dbup-migrations.md` (97 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/migrations/ef/ef-migrations.md` (84 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/migrations/migrations.md` (75 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/migrations/sql/bespoke-migrations.md` (181 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/migrations/sql/migration-dialects.md` (209 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/migrations/sql/migration-tooling.md` (218 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/migrations/sql/sql.md` (20 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/persistence.md` (48 lines)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/testing/test-databases.md` (118 lines)
- `conventions/development/backend/dotnet/core/mla/domains/validation/validation.md` (348 lines)
