# Nullability and Fixtures

*Last updated: 2026-08-17*

> What — what the null-forgiving operator, guards and test fixtures actually look like across the backend-beta SDK and
> forever-pin, and which of the two would-be conventions each finding belongs to.
> Purpose — research feeding a nullability convention and a testing-ownership split; it states findings, not rules.
> Use case — reach for it when drafting either convention, or when a `!` / fixture review needs a measured baseline.

Two trees, measured at their source roots:

- SDK — `wow-two-sdk-beta/…/wow-two-back-beta-sdk/src` — 637 `.cs`, 46 826 lines.
- forever-pin — `ventures/10x-venture-forever-pin/engineering/codebase/forever-pin.backend-services` — 215 `.cs`, 9 622 lines.

Paths below are relative to those roots. Counts come from `rg` sweeps excluding `bin/` and `obj/`.

---

## Verdict

- `!` runs 141 times — 100 in tests (assert-then-dereference), 41 in production; 40 of those 41 are the SDK's.
- That split is an enforcement artefact: the SDK sets `TreatWarningsAsErrors` (`Directory.Build.props:9`), forever-pin has
  **no** `Directory.Build.props` and no `TreatWarningsAsErrors`, so a nullable warning there never has to be silenced.
- Biggest nullability gap — the flow attributes are unruled and unused: **one** `[MaybeNullWhen]` in 56 k lines
  (`Messaging/Transport/EventDispatch.cs:34`), so `out x!` and `default!` launder null through non-null signatures.
- 103 fixture / harness types are declared; of the 63 the SDK ships as packages, only 8 are domain-neutral — the rest
  are persistence (17), messaging (22), identity (7), api (6), integrations (3), all under one `testing.md`.
- Biggest fixture gap — no test-data builder exists in either repo: entities are inline object initializers plus a
  per-file `private static NewX()`; nothing rules fixture naming, the reset contract, or what a fixture may share.

---

## Nullability today

`Nullable` is `enable` everywhere: SDK via `Directory.Build.props:9`, forever-pin per-`.csproj` (12 of 12, e.g.
`ForeverPin.Domain/ForeverPin.Domain.csproj:6`). No `#pragma warning disable CS8…` and no `NoWarn` in either tree.

Counts are `SDK · forever-pin`.

| Pattern | Count | Where (one of) | Verdict |
|---|---|---|---|
| `ArgumentNullException.ThrowIfNull` | 670 · 0 | SDK-wide; `Messaging` 199, `Identity` 93, `Data` 77 | honest |
| `ThrowIfNullOrWhiteSpace` | 126 · 0 | SDK public entry points | honest |
| `ThrowIfNullOrEmpty` | 22 · 0 | SDK public entry points | honest |
| `Guard.Against.*` | 4 · 0 | `Foundation/Errors/AppError.cs:36,49` | honest, near-dead |
| `?? throw` | 18 · 3 | `Testing/Containers/Postgres/PostgresFixture.cs:42` | honest |
| `null!` | 10 · 0 | `Foundation.Tests/Errors/ExceptionChainTests.cs:63` | honest — all in tests |
| `!` in tests | 64 · 36 | `ForeverPin.Tests.Integration/Tests/CodeRepositoryTests.cs:67` | honest, weak signal |
| `!` prod — reflection | 9 · 0 | `Mediator/Mediator.cs:57,61,84,87` | honest |
| `!` prod — `= default!` store-filled | 9 · 0 | `Identity/Core/IdentityUser.cs:15` | honest |
| `!` prod — lifecycle field | 10 · 0 | `Messaging/Kafka/KafkaTransport.cs:296` | honest, repairable |
| `!` prod — `default!` sentinel | 2 · 0 | `Mediator/Result/AppResultFactory.cs:24` | **lie** |
| `!` prod — `out x!` | 2 · 0 | `Messaging/Serialization/MessageSerialization.cs:125` | **lie** |
| `!` prod — deserialize result | 2 · 0 | `Data/EntityFrameworkCore/Json/JsonValueConverter.cs:20` | **lie** |
| `!` prod — checked-then-used | 3 · 1 | `Codes/Rendering/Svg/SvgRenderer.cs:55` | honest |
| `!` prod — 3rd-party gap | 1 · 0 | `Messaging/Kafka/KafkaTransport.cs:153` | honest, commented |
| `!` prod — other | 2 · 0 | `Mediator/Idempotency/IdempotencyBehavior.cs:55` | borderline |
| nullable method return | 60 · 16 | `Data/Errors/DbExceptionMappingRule.cs:12` | honest |
| `Task<T?>` / `ValueTask<T?>` | 46 · 18 | `Task<CodeEntity?> GetByIdAsync` — `ICodeRepository.cs` | honest |
| nullable property | 152 · 63 | `ForeverPin.Domain/…/ScanEventEntity.cs:25,29,32,35,38` | honest |
| nullable private field | 35 · 0 | `Foundation/Security/MasterKeySealKeeper.cs:14` | honest |
| `required` member | 101 · 117 | `ForeverPin.Domain/…/CodeEntity.cs:16,22,25,35` | honest |
| `required T?` | 6 · 0 | `Testing.Messaging/RecordedTransition.cs:50,53` | honest, unruled |
| `where T : notnull` | 45 · 0 | generic constraints across the SDK | honest |
| `[MaybeNullWhen]` | 1 · 0 | `Messaging/Transport/EventDispatch.cs:34` | honest |
| every other nullable attribute | 0 · 0 | `[NotNullWhen]` `[MemberNotNull]` `[NotNullIfNotNull]` | absent |

---

## Where `!` is honest

- **Reflection** — `GetMethod(nameof(DispatchTyped), …)!` names a method declared in the same type; a null there is a
  build error the compiler cannot express. `Activator.CreateInstance(t)!` on a known type is the same shape.
  Sites: `Mediator/Mediator.cs:57,61,84,87` · `Mediator/Result/AppResultFactory.cs:29` ·
  `Messaging/Saga/SagaServiceCollectionExtensions.cs:81` · `Messaging/Reliability/Ef/OutboxDispatcher.cs:26`.
- **A store-filled member** — `public TKey Id { get; set; } = default!;` (`Identity/Core/IdentityUser.cs:15`,
  `IdentityRole.cs:11`, `IdentityRelations.cs:11,14,26,44,68,77`). The store writes it; `required` cannot be used
  because the key is store-generated. This is the generic-key twin of the `null!` case already ruled in
  [entity contracts](../conventions/development/backend/dotnet/mla/domains/persistence/schema/entity-contracts.md)
  § *Members*.
- **A checked-then-used local** — `SvgRenderer.cs:55` reads `style.Gradient!` under a `hasGradient` bool the compiler
  cannot follow back to its pattern match. Capturing in the pattern (`is { Stops.Count: >= 2 } gradient`) removes it.
  Same shape: `Storage/FileSystem/LocalFileBlobStorage.cs:30` · `Identity/Core/UserAccountManager.cs:45`.
- **A third-party annotation gap** — `KafkaTransport.cs:153`: Confluent's `TKey` carries no nullable annotation but a
  null key is valid on the wire. The only production `!` in either tree with a written justification.
- **A test asserting the arg-null contract** — `Flatten(null!)` (`Foundation.Tests/Errors/ExceptionChainTests.cs:63`).
  The `!` *is* the test. All 10 `null!` uses are this; production has none.

---

## Where `!` is a lie

- `MessageSerialization.cs:125` — `public bool TryGetToken(Type type, out string token)` ending in `out token!`. The
  signature promises non-null; on `false` it is null. `EventDispatch.cs:34` in the same assembly answers the identical
  question with `[MaybeNullWhen(false)]`. Two answers to one question, 90 lines apart in one domain. Also `:130`.
- `JsonValueConverter.cs:20` — `v => JsonSerializer.Deserialize<T>(v, options)!`. A column holding the JSON literal
  `null` deserializes to null and the `!` carries it into EF materialization. Same at `JsonValueComparer.cs:30`.
- `AppResultFactory.cs:24` — `failure = default!` on the `false` path of `TryCreateFailure<TResponse>`; a caller reading
  `failure` after `false` gets null through a non-null `out`. Needs `[MaybeNullWhen(false)]`.
- `IdempotencyBehavior.cs:82` — `return cached is TResponse t ? t : default!;` returns null typed as a non-null
  `TResponse` when the cached payload's type does not match.

Lifecycle fields sit between the two. `MasterKeySealKeeper.cs:42,49` dereference `_masterKey!` right after
`EnsureUnsealed()` (`:62`), which throws when the field is null — honest, and `[MemberNotNull(nameof(_masterKey))]`
would delete both `!`. `KafkaTransport` (`_consumer`, `_deadLetterProducer`) and `NatsTransport` (`_js`) are the same
shape with no guard method at all: the field is assumed set because the consume loop only runs after start.

---

## Guards

- **`ArgumentNullException.ThrowIfNull` is the house style by 168:1** — 670 uses against 4 `Guard.Against`.
- `Ardalis.GuardClauses` 5.0.0 is referenced (`Directory.Packages.props:135`) and re-exported with a package story
  (`Foundation/Guards/guards.md`), but its two custom guards `NotSlug` / `NotUlid`
  (`Foundation/Guards/IdentifierGuardExtensions.cs:19,32`) have **zero callers** in either tree.
- **forever-pin guards nothing** — 0 `ThrowIfNull`, 0 `Guard.`, 0 manual arg-null `if`. Its 19 `is null` sites are flow
  control (`CodeRepository.cs:61`, `RedirectEndpoints.cs:27` → 404), never argument validation.
- No manual `if (x is null) throw new ArgumentNullException(…)` survives. The one legacy
  `?? throw new ArgumentNullException` is `Testing.Data/EntityFrameworkCore/RelationalTestDb.cs:32`.
- The `Try` shape is split with no rule: `bool TryX(out T)` at `EventDispatch.cs:34` and `MessageSerialization.cs:125`,
  `T? TryX()` at `EnvironmentMasterKeyProvider.cs:13` and `Data/Errors/DbExceptionMappingRule.cs:12`.

---

## Nullability rules

Directive bullets a convention would carry. Each is backed by a site above.

- must leave `Nullable` at `enable`, and must add `TreatWarningsAsErrors` to a product's build props — a nullable
  warning that does not block is a nullable warning nobody fixes.
- must not use `!` to silence a warning the type system can express — reach for the annotation first.
- may use `!` for exactly five cases: reflection on a symbol declared in the same assembly, a store-filled member, a
  local the compiler cannot follow through a pattern match, a third-party annotation gap, and a test asserting an
  arg-null contract.
- must carry a one-line `// null-forgiving: {why}` comment on every production `!` — `KafkaTransport.cs:153` models it.
- must not `!` the result of `JsonSerializer.Deserialize<T>` — handle the null, or throw naming the column.
- must annotate a `bool TryX(out T)` with `[MaybeNullWhen(false)]` rather than writing `out x!`.
- must annotate a member-setting guard with `[MemberNotNull]` rather than `!`-ing the field at every read.
- must use `[NotNullWhen(true)]` on a `bool` check helper and `[NotNullIfNotNull]` on a pass-through mapper.
- must treat a nullable return as honest only when null carries a **domain meaning** — not-found, no-match, not-yet-set
  — and must say which in the `<summary>`, as `ICodeRepository.GetByIdAsync` does.
- must not return `T?` to mean *failed* — a failure is `AppResult` / `AppError`, never a null.
- must pick one `Try` shape per return kind: `bool TryX([MaybeNullWhen(false)] out T)` when the caller keeps the value,
  `T? TryX()` when there is nothing else to return. Both exist today with no rule.
- must use `required` when the caller must decide the value, and initialize with `null!` / `default!` only when the
  store supplies it — the *entity contracts* § *Members* rule, extended to a generic key (`= default!`).
- must remember `required` binds object-initializer callers only — EF materialization bypasses it, so `required` is a
  construction contract, not a read-time not-null guarantee.
- may combine `required T?` — "the author must decide, and null is a valid decision"; `RecordedTransition.cs:50` is the
  live example, and the two features are orthogonal rather than contradictory.
- must guard every **public SDK** entry point with `ArgumentNullException.ThrowIfNull` / `ThrowIfNullOrWhiteSpace`.
- must not guard inside a product — forever-pin's zero-guard internals are correct; validation runs at the API edge and
  `is null` inside is flow control.
- must either stop adding `Guard.Against` calls or delete the near-dead `Ardalis.GuardClauses` surface — one of the
  two, not the present limbo.
- must assert-then-narrow in a test (`.Should().NotBeNull()`, then use the returned value) rather than `x!.Member`, so
  a null fails as an assertion instead of an `NRE`.

---

## Fixtures today

103 declared types: 63 shipped by the SDK as four packages (`Testing`, `Testing.Data`, `Testing.Integrations`,
`Testing.Messaging`), 26 more declared inside the SDK `*.Tests` projects, 14 in forever-pin. Owner split of the shipped 63:
**persistence 17 · messaging 22 · identity 7 · api 6 · integrations 3 · neutral 8**.

### Domain-neutral — 8

- `IAsyncTestFixture` · `IAsyncFixtureCollection` — `Testing/IAsyncTestFixture.cs:8,29` — the
  `Name` / `StartAsync` / `ResetAsync` contract every fixture implements.
- `AsyncFixtureCollection` — `Testing/AsyncFixtureCollection.cs:7` — starts and resets in order, disposes in reverse.
- `ContainerFixtureBase<TContainer>` — `Testing/Containers/ContainerFixtureBase.cs:10` — Testcontainers start /
  dispose; `ResetAsync` is a **no-op** by default (`:34`).
- `Polling` — `Testing/Polling.cs:11` — retry-until-predicate for eventual consistency.
- `BogusFakerFactory` — `Testing/Bogus/BogusFakerFactory.cs:8` — seeded `Faker<T>` (seed 1337). **No callers.**
- `VerifyDefaults` — `Testing/Verify/VerifyDefaults.cs:20` — Verify snapshot scrubbers and settings.
- `ServiceCollectionInternalExtensions` — `Testing/WebApiTestHost.cs:59` — `RemoveAll<T>()` DI helper.

### Persistence

- `PostgresFixture` — `Testing/Containers/Postgres/PostgresFixture.cs:20` — PG container + Respawn, ignoring
  `migration_history` (`:23`); reset at `:67`.
- `RedisFixture` · `MongoDbFixture` · `AzuriteFixture` — `Testing/Containers/{Redis,MongoDb,Azurite}/*.cs:7` —
  container + connection string, **no reset**.
- `RelationalTestDb<TContext>` — `Testing.Data/EntityFrameworkCore/RelationalTestDb.cs:17` — provider-switchable EF DB:
  PG + Respawn, or in-memory SQLite recreated per reset (`:119`).
- `RelationalTestBase<TDb,TContext>` — `…/RelationalTestBase.cs:11` — per-test reset over a shared collection fixture.
- `RelationalTestDb<TContext>.Provider` — fixture-owned Postgres / SQLite selection.
- `RelationalTestDbServiceCollectionExtensions` · `DbContextProviderSwapExtensions` —
  `…/RelationalTestDbServiceCollectionExtensions.cs:9` · `…/DbContextProviderSwapExtensions.cs:7` — DI-built context;
  repoint a host's `DbContext` at the test provider.
- `MigratorPostgresFixture` — `Testing.Data/Migrations/MigratorPostgresFixture.cs:10` — pinned PG; reset is
  `drop schema public cascade; create schema public;` (`:31`).
- `MigratorTestBase` · `MigratorHarness` — `…/MigratorTestBase.cs:8` · `…/MigratorHarness.cs:14` — schema reset per
  test; the migrator DI graph plus SQL assertions.
- `MigrationsWorkspace` · `MigrationHistoryRow` — `…/MigrationsWorkspace.cs:5` · `…/MigrationHistoryRow.cs:5` —
  throwaway `NNN-name/{Apply,Rollback}.sql` tree; a Dapper projection of the history table.
- `NoOpBespokeMigrator*` — `…/NoOpBespokeMigrator.cs:9,26,45` — neuters the startup migrate hook.
- `DataTestDb` · `DataTestCollection` · `DataTestDbContext` — `Data.Tests/Harness/DataTestDb.cs:9,32` ·
  `DataTestDbContext.cs:48` — suite DB with snake_case conventions and outbox mapping.
- `Widget` · `SoftWidget` — `Data.Tests/Harness/DataTestDbContext.cs:9,28` — audited / soft-deletable test entities.
- `InterceptorLog` + four recording interceptors — `Data.Tests/Harness/RecordingInterceptors.cs:8,26,54,65,86` —
  ordered interceptor invocation log and savepoint event stream.
- `SqliteMigratorTestBase` — `Migrations.Tests/Harness/SqliteMigratorTestBase.cs:11` — a fresh temp `.db` per test;
  isolation by construction, no reset.
- `ForeverPinTestDb` · `RepositoryTestCollection` · `RepositoryTestBase` — `ForeverPin.Tests.Integration/Harness/
  ForeverPinTestDb.cs:10` · `RepositoryTestBase.cs:7,15` — app context on the test provider; reset at `:24`.
- `TestModuleInit` — `ForeverPin.Tests.Integration/Harness/TestModuleInit.cs:9` — `[ModuleInitializer]` picks the provider.
- `MigratorCollection` — `ForeverPin.Tests.Migrations/Harness/MigratorCollection.cs:7` — shares the drop-schema fixture.

### Api

- `WebApiTestHost<TEntryPoint>` — `Testing/WebApiTestHost.cs:18` — in-proc host, `FakeTimeProvider`, service hooks.
- `WebApiTestBase<TEntryPoint>` — `Testing/WebApiTestBase.cs:11` — lazy host + `HttpClient` + fake clock per test.
- `MultiHostFixture` — `Testing/MultiHost/MultiHostFixture.cs:51` — N hosts over one container set; env injection.
- `HttpExtensions` · `TestJson` · `ApiEnvelope<T>` — `Testing/Web/HttpExtensions.cs:11` · `Web/ApiContracts.cs:21,65` —
  JSON verbs and a test-side mirror of the success envelope.
- `AppFixture` · `AppCollection` · `E2EBase` — `ForeverPin.Tests.E2E/Harness/AppFixture.cs:31,211,218` — Api + Redirect
  hosts on one PG container; per-test reset at `:235`.
- `CodeRequests` — `ForeverPin.Tests.E2E/Support/HttpExtensions.cs:7` — anonymous-object **request-body** builders.
- Ten `*DtoModel` wire mirrors — `ForeverPin.Tests.E2E/Support/ApiContracts.cs:10–110`.

### Identity

- `TestAuthHandler` · `TestAuthOptions` · `TestClaimTypes` — `Testing/Auth/TestAuthHandler.cs:31` ·
  `TestAuthOptions.cs:15` · `TestClaimTypes.cs:11` — fixed-identity auth scheme with an optional header gate.
- `TestCurrentUser` · `TestUserKind` — `Testing/Auth/TestCurrentUser.cs:38,4` — current-user stub, no HTTP.
- `TestAuthServiceCollectionExtensions` — `Testing/Auth/TestAuthServiceCollectionExtensions.cs:10` — `AddTestAuth`.
- `CookieExtraction` — `Testing/Auth/CookieExtraction.cs:12` — lifts `Set-Cookie` back onto the client.
- `GuestClient` — `ForeverPin.Tests.E2E/Harness/AppFixture.cs:207` — a provisioned guest plus a cookie-carrying client.
- `FakeGoogleTokenVerifier` — `ForeverPin.Tests.E2E/Harness/FakeGoogleTokenVerifier.cs:6` — accepts only
  `fake:{sub}:{email}:{name}`.

### Integrations

- `WireMockFixture` — `Testing/WireMock/WireMockFixture.cs:9` — in-proc WireMock; reset clears stubs + history (`:33`).
- `FakeGitHubClient` · `FakeContainerRegistryClient` — `Testing.Integrations/FakeGitHubClient.cs:16` ·
  `FakeContainerRegistryClient.cs:16` — canned GitHub repo / release / CI and GHCR image-exists outcomes.
- `FakeBillingBroker` — `ForeverPin.Tests.E2E/Harness/FakeBillingBroker.cs:7` — staged Stripe checkout / portal / webhook
  plus captured arguments; reset at `:56`.

### Messaging

- `RabbitMqFixture` · `KafkaFixture` — `Testing/Containers/{RabbitMq,Kafka}/*.cs:7` — broker container + connection
  string, **no reset**.
- `MessagingTestHarness` · `MessagingHarnessOptions` — `Testing.Messaging/MessagingTestHarness.cs:49,13` — in-memory
  bus host, published / consumed / faulted / DLQ logs, `WaitForIdleAsync`.
- `MessagingRecorder` · `RecordedMessage` · `RecordedMessageLog` — `Testing.Messaging/MessagingRecorder.cs:30` ·
  `RecordedMessage.cs:11,61` — publish / receive / consume observer and an awaitable per-phase log.
- `SagaTestHarness<TState>` · `SagaRecorder<TState>` — `Testing.Messaging/SagaTestHarness.cs:121` ·
  `SagaRecorder.cs:44` — saga + in-memory bus + `FakeTimeProvider`; records transitions via the repository seam.
- `RecordedTransition<TState>` · `RecordedSagaTimeout` — `Testing.Messaging/RecordedTransition.cs:43,278`.
- `EventCollector` · `HarnessGate` + handlers — `Messaging.Tests/TestSupport.cs:15,68,45,55,106`.
- `AdapterOwnedHeaderContract` — `Messaging.Tests/AdapterOwnedHeaderContract.cs:33` — the shared `wt-` header contract
  asserted per broker.

### Product-specific

- `QrCoderReference` — `ForeverPin.Tests.Unit/QrCoderReference.cs:6` — live QRCoder SVG parity reference.

---

## What is missing

- **No test-data builder anywhere.** Nothing named `*Builder`, `*Mother` or `*Seeder` constructs a domain entity.
  Entities are inline object initializers, occasionally lifted to a `private static` in the same file —
  `ForeverPin.Tests.Integration/Tests/CodeRepositoryTests.cs:15` (`NewCode`), `SubscriptionRepositoryTests.cs:11`
  (`NewSub`), `ForeverPin.Tests.E2E/Tests/BillingTests.cs:366,381`. All private, so nothing is shared across files.
- **No fixture naming rule.** Live suffixes: `*Fixture` (owns a container), `*TestDb` (owns an EF context), `*Harness`
  (owns an in-process runtime), `*Base` (per-test hook), `*Collection` (xUnit sharing), `Fake*` (double), `*Recorder`
  (observer). Coherent, none written down.
- **No reset contract.** `ContainerFixtureBase.ResetAsync` is a no-op (`Testing/Containers/ContainerFixtureBase.cs:34`),
  so `RedisFixture`, `RabbitMqFixture`, `KafkaFixture`, `MongoDbFixture` and `AzuriteFixture` carry state between tests
  and nothing says so.
- **No rule for what a fixture may share.** Four `[CollectionDefinition]`s exist with four ad-hoc name strings: `"data"`
  (`Data.Tests/Harness/DataTestDb.cs:31`), `"forever-pin-e2e"` (`ForeverPin.Tests.E2E/Harness/AppFixture.cs:210`),
  `"ForeverPin repository tests"` (`ForeverPin.Tests.Integration/Harness/RepositoryTestBase.cs:6`), `"forever-pin-migrator"`
  (`ForeverPin.Tests.Migrations/Harness/MigratorCollection.cs:6`). No `IClassFixture<T>` anywhere.
- **The one-assertion-library rule is already broken.** `testing.md` § *E2E / integration stack* names one fluent lib;
  forever-pin runs 216 `.Should()` against 193 `Assert.*` — `Tests.Unit` (135) and `Tests.Integration` (51) are raw xUnit,
  `Tests.E2E` (165) is fluent, `Tests.Migrations` mixes both.
- **Nine broker suites bypass the SDK container fixtures**, newing a container inline in the test class —
  `Messaging.Tests/RabbitMqEventBusTests.cs:15`, `KafkaEventBusTests.cs:13`, `NatsEventBusTests.cs:16`,
  `RedisStreamsEventBusTests.cs:33`, `OutboxSkipLockedTests.cs:14`, four `*AdapterOwnedHeaderTests`. `test-databases.md`
  § *Test tiers* says each tier MUST use the SDK harness; the messaging tier has no equivalent sentence.
- **`NSubstitute` 5.3.0 is pinned** (`Directory.Packages.props:293`) and referenced by no project — every double is
  hand-rolled. Either the rule is "no mocking library" or it is not; the pin says neither.

---

## Testing ownership split

`testing.md` and `test-databases.md` both sit under `architecture/clean/`. Under the structural rule — a testing
convention specific to a domain belongs inside that domain — `test-databases.md` is already a **persistence** doc filed
in the wrong place: its entire subject is which provider a `DbContext` test runs against, and that differs per provider.

**`testing.md` keeps** only what holds regardless of domain: the E2E-first principle, project layout and
`{Product}.Tests.{Type}` naming, the tier ladder, method naming, the runner and assertion-library choice, the
`IAsyncTestFixture` / `AsyncFixtureCollection` / `ContainerFixtureBase` / `Polling` contracts, and harness extraction.

### `persistence` — the largest section, absorbs `test-databases.md` wholesale

- `RelationalTestDb<TContext>` subclassing · fixture-owned Postgres / SQLite selection.
- Respawn reset and the `migration_history` exclusion · `DbContextProviderSwapExtensions`.
- The migrator tier — `MigratorPostgresFixture` drop-schema, `MigratorHarness`, `MigrationsWorkspace`.
- Test-entity and seeding rules (`Widget` / `SoftWidget` as the shape).

### `api`

- `WebApiTestHost<T>` / `WebApiTestBase<T>` / `MultiHostFixture`.
- The host-local `ConfigureConfigurationHook` seam in `test-databases.md` § *E2E host-boot*.
- Request-body builders (`CodeRequests`) · DTO wire mirrors, and when a mirror beats referencing the contract type.

### `messaging`

- `MessagingTestHarness` + `MessagingRecorder` · `SagaTestHarness` and its fake clock.
- Broker container fixtures and their **no-reset** consequence.
- "Assert async work via poll-with-timeout" — today in `testing.md`, true only of messaging.
- The per-broker `wt-` header contract.

### `identity`

- `TestAuthHandler` / `TestAuthOptions` / `AddTestAuth`.
- `TestCurrentUser` and the anonymous / guest / member ladder.
- `CookieExtraction` for cookie-mode suites.
- How a product fakes its external verifier (`FakeGoogleTokenVerifier`).

### `integrations`

- `WireMockFixture` and its reset-between-tests contract.
- When a hand-rolled `Fake*` client beats a WireMock stub (`FakeGitHubClient`, `FakeBillingBroker`).
- "Only stub genuinely-external 3rd-party APIs" — today in `testing.md`, an integrations rule.

### `validation` — thinnest, possibly not yet worth a section

- The unit-tier shape for a validator (`Foundation.Tests/Validation/FluentValidationAdapterTests.cs:14–49` declares
  five inline validators).
- Whether a rule-code assertion belongs to the unit tier or the E2E tier.

---

## Proposed rules

The fixture / testing half. The nullability half is *Nullability rules* above.

- must keep in `testing.md` only what holds for every domain — tiers, project naming, method naming, runner, assertion
  library, and the generic fixture contracts.
- must place a fixture rule that differs per provider, per broker, or per auth scheme inside its domain doc.
- must move `test-databases.md` under `domains/persistence/`, leaving one link from `testing.md`.
- must name a fixture by what it owns: `*Fixture` owns a container or server, `*TestDb` owns an EF context, `*Harness`
  owns an in-process runtime, `*Base` owns the per-test hook, `*Collection` is the xUnit sharing declaration.
- must prefix a hand-rolled double with `Fake` and name the interface it replaces — `FakeBillingBroker : IBillingBroker`
- must not use a mocking library — every double is a hand-rolled `Fake*`, so the unused `NSubstitute` pin must go.
- must declare a fixture that owns a container as an `ICollectionFixture<T>`, never an `IClassFixture<T>`.
- must derive a collection's name from its fixture type and expose it as `public const string Name` on the collection
  class — the four live names follow no shared form.
- must implement `ResetAsync` on any fixture that accumulates state, and must state in the type's `<summary>` when it
  deliberately does not — the five container fixtures inheriting the no-op reset are silent about it today.
- must reset in the `*Base` class's `InitializeAsync`, never per test method.
- must share only what is expensive to build — a container, a host, a migrated schema.
- must not let a fixture share seeded domain rows; a test seeds its own.
- must build test entities through a shared `{Entity}Builder` with a valid default and per-test overrides, placed
  beside the tests that use it, and must not repeat an inline object initializer across files.
- must not let a builder reach the database — it returns an entity, and the test decides whether to persist it.
- must use one assertion library per repo, and must convert `ForeverPin.Tests.Unit` and `Tests.Integration` off raw
  `Assert.*` to match `testing.md`.
- must use the SDK container fixture for a broker suite, as the DB tiers already must.

---

## Open

- Does the SDK-vs-product guard split hold as a rule — public SDK entry points guard, product internals never — or is
  the real line "any public API of any assembly"?
- Should every production `!` carry a `// null-forgiving:` comment, or is reflection exempt because the shape is
  self-evident? Nine of the 40 are reflection.
- Delete `Ardalis.GuardClauses` and its two zero-caller custom guards, or adopt it as the guard style and leave the 670
  `ThrowIfNull` calls as they are?
- Does `validation` earn a testing section now, or does its rule ride inside `testing.md` § *Coverage* until a second
  product exercises it?
- Do product-local API DTO mirrors (`ForeverPin.Tests.E2E/Support/ApiContracts.cs`) stay product-local, or does the api
  domain rule that a test references the real contract type whenever the assembly is reachable?
