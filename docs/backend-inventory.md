# Backend inventory

*Last updated: 2026-08-16*

> What backend functionality already exists across this workspace — beta SDK, platform org, product backends.
> Purpose — groundwork for the backend conventions still to be written; it is an inventory, not a convention.
> Use case — checking whether a capability already exists before building it or writing a rule about it.

## Status

- **First pass. Not exhaustive.** Breadth over depth — every area was sampled at its registration entry points,
  not read end to end. Absence from this doc is not evidence of absence in source.
- Every symbol cited was grepped in source on 2026-08-16. Nothing here is taken on a doc's word.
- Where a repo doc disagreed with source, source won and the drift is recorded in *Doc drift*.

### Maturity vocabulary

| Term | Means |
|---|---|
| shipped · used | real implementation, referenced by ≥1 product backend |
| shipped · unused | real implementation, zero product consumers |
| partial | core path works, named gaps remain |
| stub | folder / csproj / marker type only, no implementation |

Usage counted by grepping the 11 SDK-consuming product backends for each symbol.

---

## Source trees

| Tree | Holds | Verdict |
|---|---|---|
| `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/` | the beta backend SDK mono-lib | the real platform |
| `workbench/wow-two-platform/` | 17 repos | 14 empty, 1 stub, 2 products |
| `workbench/wow-two-sdk/` | 7 repos | 5 empty, 2 with code |
| `workbench/ventures/` + drydock + secrets-vault | 11 product backends | the consumers |

**Headline: the platform org is empty.** Every shared backend capability lives in the beta SDK mono-lib.

### The mono-lib

- code dir `engineering/codebase/wow-two-back-beta-sdk/src/`; a bare `src/…` below is relative to it
- 7 packable projects only — the per-concern csproj split was collapsed

| Package id | Project | What |
|---|---|---|
| `WoW2.Sdk.Backend.Beta` | `src/WoW.Two.Sdk.Backend.Beta.csproj` | the mono-lib, all shipping concerns |
| `WoW2.Sdk.Backend.Beta.Data.Abstractions` | `src/Data/Abstractions/` | zero-dep entity + repository contracts |
| `WoW2.Sdk.Backend.Beta.Testing` | `src/Testing/` | host, fixtures, containers |
| `WoW2.Sdk.Backend.Beta.Testing.Data` | `src/Testing.Data/` | EF + migrator harnesses |
| `WoW2.Sdk.Backend.Beta.Testing.Messaging` | `src/Testing.Messaging/` | bus + saga recorders |
| `WoW2.Sdk.Backend.Beta.Testing.Integrations` | `src/Testing.Integrations/` | fake GitHub / GHCR clients |
| `WoW2.Sdk.Backend.Beta.Data.Migrations.Cli` | `src/Data/Migrations/cli/` | `wow-migrate` dotnet tool |

- namespaces are `WoW.Two.Sdk.Backend.Beta.*`; package ids are `WoW2.Sdk.*` — the two differ by design
- 203 public `Add*` / `Use*` / `Map*` registration methods across `src/`
- products pin `10.0.45-beta` (forever-pin, drydock) or `10.0.40-beta`; testing companions lag at `10.0.40-beta`

---

## Capability map

| Capability | Area | Maturity |
|---|---|---|
| Startup defaults | `src/Meta/` | shipped · used |
| Results and errors | `src/Foundation/{Results,Errors}/` | shipped · used |
| Validation | `src/Foundation/Validation/` | shipped · used |
| Serialization | `src/Foundation/Serialization/`, `src/Web/Json/` | shipped · used |
| Time | `src/Foundation/Time/` | shipped · used |
| Naming / casing | `src/Foundation/Naming/` | shipped · used |
| Security primitives | `src/Foundation/{Security,Audit}/` | shipped · used |
| Configuration loading | `src/Foundation/Configuration/` | shipped · used |
| Web surface | `src/Web/` | shipped · used |
| Mediator + CQRS | `src/Mediator/` | shipped · used |
| Identity and auth | `src/Identity/` | shipped · used |
| Persistence | `src/Data/` | shipped · used |
| Migrations | `src/Data/Migrations/` | shipped · used |
| Testing harnesses | `src/Testing*/` | shipped · used |
| Observability | `src/Observability/` | shipped · used |
| Codes (QR / barcode) | `src/Codes/` | shipped · used |
| Integrations (GitHub, GHCR) | `src/Integrations/` | shipped · used |
| Media (captions, CSV, Excel) | `src/Media/` | partial · used |
| Messaging and the bus | `src/Messaging/` | shipped · unused |
| Caching | `src/Caching/` | shipped · unused |
| HTTP clients and resilience | `src/Http/` | shipped · unused |
| Background jobs | `src/Jobs/` | shipped · unused |
| Comms (email) | `src/Comms/` | shipped · unused |
| Blob storage | `src/Storage/` | partial · unused |
| Realtime | `src/Realtime/` | shipped · unused |
| Tenancy | `src/Tenancy/` | shipped · unused |
| Feature flags | `src/FeatureFlags/` | partial · unused |
| Geo | `src/Geo/` | shipped · unused |
| Localization | `src/Localization/` | shipped · unused |
| AI | `src/Ai/` | partial · unused |
| Code generation | — | stub (no source generators) |

---

## Startup and configuration defaults

Two paired calls stand up a production-shaped host; auth, mediator and data stay explicit after them.

- lives in `src/Meta/ApiDefaultsExtensions.cs` + `ApiDefaultsOptions.cs`
- `AddApiDefaults(this WebApplicationBuilder, Action<ApiDefaultsOptions>?)` · `UseApiDefaults(this WebApplication)`
- folds in: `UseSerilogConventional` `AddTimeProviders` `AddOpenTelemetryTracing` `AddOpenTelemetryMetrics`
  `AddOtlpExporters` `AddHealthChecksBuilder` `AddFluentValidatorsFromAssemblies` `AddProxyAwareHosting`
  `AddOpenApiDefaults` `AddTraceAwareProblemDetails` `AddAppExceptionHandling` `AddPerIpSlidingWindowRateLimit`
  `AddDefaultOutputCache` `AddBrotliGzipCompression` `AddDefaultCorsPolicy`
- use-side adds `UseExceptionHandler` `UseProxyAwareHosting` `UseHttpsRedirection` `UseOwaspSecureHeaders`
  `UseCors` `UseRateLimiter` `UseOutputCache` `UseResponseCompression`, maps OpenAPI + `MapHealthChecks`
- OpenAPI is exposed only in Development unless `ExposeOpenApi` is set; the health endpoint is `AllowAnonymous`
- maturity — **shipped · used** by 6 product backends
- configuration loading is separate: `ConfigurationMapper.Load<T>(IConfiguration, section)` +
  `EnvironmentVariableAttribute` + `AddEnvironmentOverlaidOptions`, in `src/Foundation/Configuration/`

---

## Results and errors

One error model spans the mediator result, the HTTP status map and the ProblemDetails writer.

- lives in `src/Foundation/{Results,Errors}/`, `src/Mediator/Result/`, `src/Web/{ErrorMapping,ExceptionHandling}/`
- error model — `AppError`, `AppAggregateError`, `AppErrorFactory`, `AppException`, `ErrorMessageConstants`,
  `ErrorOrigin`, `ErrorNature` + `IErrorNatureClassifier` / `DefaultErrorNatureClassifier`
- `AppErrorType` — 18 members: `Unexpected` `Validation` `NotFound` `Conflict` `Unauthorized` `Forbidden`
  `TooManyRequests` `DbTimeout` `OperationTimeout` `ExternalUnauthorized` `ExternalUnavailable` `FileNotFound`
  `SerializationFailed` `DataIntegrity` `BusinessRule` `PaymentRequired` `Gone` `Canceled`
- result types — `Result`, `Result<T>` (`Success` / `Failure` cases), `ResultExtensions`, `AttemptExtensions`
- mediator-facing — `AppResult<TSuccess>`, `AppResultFactory`, `IAppSuccessContext`, `IAppFailureContext`
- exception mapping — `IExceptionMapper` / `ExceptionMapper`, `IExceptionMappingRule`, `AddExceptionMapping`,
  `AddExceptionMappingRule`; DB rules ship separately as `DbExceptionMappingRule` + `AddDbExceptionMapping`
- HTTP mapping — `IErrorHttpStatusCodeMapper` / `DefaultErrorHttpStatusCodeMapper`, `AddErrorHttpStatusMapping`
- handler chain — `AddAppExceptionHandling` registers `ValidationExceptionHandler`, `AppExceptionHandler`,
  `UnhandledExceptionHandler` plus `AddAppErrorObserver` and `AddExceptionMapping`
- MVC path is separate: `AddValidationExceptionFilter` (a filter, because the handler misses MVC endpoints)
- rendering — `AppErrorProblemDetailsFactory`, `IErrorMessageResolver` / `DefaultErrorMessageResolver`
- wire contract — `ApiResponse` / `ApiResponse<T>` with `Success` / `Failure` cases (`src/Web/Contracts/`)
- maturity — **shipped · used**; `AppResult` alone appears 65× in forever-pin

**Two result models coexist**: `Foundation.Results.Result<T>` and `Mediator.Result.AppResult<TSuccess>`.
Products split by generation — 5 repos use `Result<`, the rest use `AppResult`. A convention has to pick one.

---

## Validation

- lives in `src/Foundation/Validation/`
- `IValidator<in T>`, `ValidationError`, `FieldError`, `ValidationException`, `ValidationSeverity`
- `ISensitiveMembers` marks members redacted from validation output; `IFieldErrorMessageResolver` localizes
- FluentValidation is an adapter, not the contract — `FluentValidationAdapter` +
  `AddFluentValidatorsFromAssemblies(params Assembly[])`
- pipeline entry is `AddMediatorValidationBehavior()`; HTTP entry is `AddValidationExceptionFilter` (MVC)
  or `AddValidationExceptionHandler` (minimal API)
- maturity — **shipped · used** by 6 backends

---

## Serialization, time, naming

| Concern | Lives in | Entry points |
|---|---|---|
| JSON presets | `src/Foundation/Serialization/` | `JsonOptionsConstants` |
| MVC JSON | `src/Web/Json/` | `AddControllersWithSdkJson`, `AddJsonStringEnums` |
| Time | `src/Foundation/Time/` | `AddTimeProviders`, `TimeZoneMapper`, `CronExpressionParser` |
| Casing | `src/Foundation/Naming/` | `CaseStyle`, `CaseMapper`, `WordMapper`, `EnumNameMapper<TEnum>` |

- `Naming` is the single casing authority — zero deps, and the source for column, enum-label and SQL casing
- `CasingExtensions` carries the string-level surface
- maturity — all three **shipped · used**; `AddJsonStringEnums` alone is used by 6 backends

---

## Security primitives

Two independent capabilities, both real and both proven by secrets-vault.

**Envelope cryptography** — `src/Foundation/Security/`

- `AddEnvelopeCryptography`, `ICryptoCore` / `CryptoCore`, `AesGcmCipher`, `EncryptedPayload`, `KeySizes`
- key seam — `IMasterKeyProvider` / `EnvironmentMasterKeyProvider`, `ISealKeeper` / `MasterKeySealKeeper`
- `EnvelopeCryptographyOptions`, `MasterKeyFormatException`

**Hash-chained audit** — `src/Foundation/Audit/`

- `AddHashChain`, `IHashChainSealer<TEntry>` / `HashChainSealer`, `IHashChainVerifier<in TEntry>` / `HashChainVerifier`
- `IHashChainedEntry`, `IChainedEntryCanonicalizer<in TEntry>`, `ICanonicalPayloadBuilder` / `CanonicalPayloadBuilder`
- `HashChainAlgorithm`, `HashChainHasher`, `HashChainOptions`, `HashChainVerificationResult`
- maturity — **shipped · used**, by secrets-vault only

---

## Web surface

Every concern is its own extension; `AddApiDefaults` composes them and is the intended entry.

| Concern | Folder | Entry points |
|---|---|---|
| Hosting | `src/Web/Hosting/` | `AddProxyAwareHosting`, `UseProxyAwareHosting` |
| SPA hosting | `src/Web/Hosting/` | `UseSpaHosting`, `MapSpaFallback`, `SpaHostingOptions` |
| Request limits | `src/Web/RequestLimits/` | `AddRequestLimits`, `RequestLimitsOptions` |
| OpenAPI | `src/Web/OpenApi/` | `AddOpenApiDefaults`, `MapOpenApiEndpoint` |
| ProblemDetails | `src/Web/ProblemDetails/` | `AddTraceAwareProblemDetails` |
| Rate limit | `src/Web/RateLimit/` | `AddPerIpSlidingWindowRateLimit` |
| Output cache | `src/Web/OutputCache/` | `AddDefaultOutputCache` |
| Compression | `src/Web/Compression/` | `AddBrotliGzipCompression` |
| Secure headers | `src/Web/SecureHeaders/` | `UseOwaspSecureHeaders` |
| CORS | `src/Web/Cors/` | `AddDefaultCorsPolicy`, `AddCredentialedCorsPolicy` |
| Versioning | `src/Web/Versioning/` | `AddDefaultApiVersioning` |

- `UseOwaspSecureHeaders` hard-codes `AddCrossOriginOpenerPolicy(SameOrigin)` +
  `AddCrossOriginEmbedderPolicy(RequireCorp)` with no opt-out — forever-pin writes a local override to run
  Google Identity Services popups. That is an SDK gap, not a product concern.
- maturity — **shipped · used**

---

## Mediator and CQRS

A MediatR-API-compatible facade with no MediatR dependency.

- lives in `src/Mediator/`
- core — `IMediator`, `ISender`, `IPublisher`, `IRequest`, `IRequest<TResponse>`, `IBaseRequest`,
  `IRequestHandler<in TRequest, TResponse>`, `INotification`, `INotificationHandler<in TNotification>`,
  `IPipelineBehavior<in TRequest, TResponse>`
- CQRS layer (`src/Mediator/Cqrs/`) — `ICommand`, `ICommand<TResult>`, `ICommandHandler<in TCommand>`,
  `ICommandHandler<in TCommand, TResult>`, `IQuery<TResult>`, `IQueryHandler<in TQuery, TResult>`
- registration — `AddMediator(params Assembly[])`, `AddMediatorBehavior`

| Behavior | Entry point | Extra contract |
|---|---|---|
| Validation | `AddMediatorValidationBehavior` | — |
| Logging | `AddMediatorLoggingBehavior` | — |
| Authorization | `AddMediatorAuthorizationBehavior` | `IRequireAuthorization` |
| Idempotency | `AddMediatorIdempotencyBehavior` | `IIdempotent`, `IIdempotencyRepository` |
| Exception → result | `AddMediatorExceptionToResultBehavior` | — |

- maturity — **shipped · used**; `AddMediator` is the single most-adopted SDK symbol (15 consumer repos)

---

## Identity and auth

The broadest area in the SDK — 84 source files, 33 registration methods.

**Own user model** (`src/Identity/Core/`) — `AddUserAccounts`, `IdentityUser`, `IdentityRole`, `IdentityRelations`,
`IdentitySchema`, `IUserRepository<TUser, in TKey>` / `EfUserRepository`, `UserAccountManager`, `IdentityBuilder`,
`IdentityResult`, `ILookupNormalizer` / `LookupNormalizer`.

**Authentication schemes**

| Scheme | Entry point |
|---|---|
| JWT bearer | `AddJwtBearerAuthentication` |
| Cookies | `AddCookieAuthentication` |
| OIDC | `AddOpenIdConnectAuthentication` |
| Identity API endpoints | `AddIdentityApiEndpoints` |
| Google ID-token verify | `AddGoogleIdTokenVerifier`, `IGoogleIdTokenVerifier`, `GoogleVerifiedIdentity` |

**OAuth providers — 17**, each `Add{Provider}Authentication`: Amazon · Apple · Discord · Facebook · GitHub ·
GitLab · Google · LinkedIn · Microsoft · Notion · Reddit · Slack · Spotify · Twitch · Twitter · Vkontakte ·
Yandex. Shared baseline in `OAuthBaseline.cs`.

**Adjacent capabilities**

| Capability | Entry point | Contracts |
|---|---|---|
| Current user | `AddCurrentUser` | `ICurrentUser`, `UserKind`, `CookieCurrentUser` |
| Guest session | `AddGuestSession` | `IGuestSession`, `CookieGuestSession` |
| Claim normalization | `AddClaimNormalization` | `ClaimNormalizer`, `ClaimProviderProfileFactory`, `NormalizedClaimTypeConstants` |
| Token issuance | `AddJwtTokenIssuance` | `ITokenIssuer`, `JwtTokenIssuer` |
| OTP | `AddOtpService`, `AddTelegramOtpDelivery` | `IOtpService`, `IOtpRepository`, `IOtpDeliveryHandler` |
| TOTP MFA | — | `TotpService` |
| WebAuthn MFA | `AddFido2WebAuthn` | — |
| Password hashing | `UseArgon2PasswordHasher` | `Argon2PasswordHasher` |
| Role policy | `AddRolePolicy` | `IRolePolicy`, `DictionaryRolePolicy` |
| Allowlist | `AddPrincipalAllowlist`, `AddDefaultDenyAuthorization` | `AllowlistRequirement`, `AllowlistOptions` |

- OTP code generation is its own seam — `IOtpCodeGenerator` / `NumericOtpCodeGenerator`, with `MemoryOtpStore`
  as the default store
- maturity — **shipped · used**, but adoption is thin and split: cookies in 2 repos, everything else in 1 each.
  `AddUserAccounts` has **zero** product consumers despite being the identity-rebuild step 1.

---

## Persistence

**Contracts** — `src/Data/Abstractions/`, a separate zero-dep package

- entity — `IEntity`, `IKeyedEntity<out TId>`, `IHasTableName`, `IVersioned`, `IRowVersioned`, `IHasXmin`,
  `IHasTenant<TTenantId>`
- audit — `IAuditable`, `ICreationAuditable`, `IModificationAuditable` + `…By<TUserId>` actor variants
- soft delete — `ISoftDeletable`, `ISoftDeletableBy<TUserId>`
- repository — `IReadRepository<TEntity, in TId>`, `IWriteRepository<TEntity, in TId>`, `IRepository<TEntity, TId>`;
  verbs `GetByIdAsync` `ExistsAsync` `CountAsync` `CreateAsync` `DeleteByIdAsync`
- connection — `IDbConnectionFactory`, `DataSourceConnectionFactory`, `AddDbConnectionFactory`,
  `AddDataSourceConnectionFactory`

**EF Core** — `src/Data/EntityFrameworkCore/`

- `AppDbContextBase`, `AddEntityFrameworkCore<TContext>`, `AddDatabaseOptions`, `EntityModelExtensions`

| Provider | Entry point |
|---|---|
| Postgres | `UseNpgsqlConventional`, `AddNpgsqlDataSource`, `MapEnums`, `CaseStyleNameTranslator` |
| SQL Server | `UseSqlServerConventional` |
| SQLite | `UseSqliteConventional`, `AddSqliteConnectionFactory` |
| Cosmos | `UseCosmosConventional` |

- interceptors — `AuditInterceptor` + `IAuditCurrentUserAccessor` + `AddEfCoreAuditInterceptor` /
  `UseAuditInterceptor`; `SoftDeleteInterceptor` + `AddEfCoreSoftDeleteFilter` / `UseSoftDeleteInterceptor`;
  generic wiring via `AddEfInterceptor`, `AddEfSaveChangesInterceptor`, `AddRegisteredInterceptors`,
  `EfInterceptorExtensions`, `EfInterceptorWiringValidator`
- mapping — `JsonValueConverter<T>` / `JsonValueComparer<T>`, `EnumCaseMapper<TEnum>`, naming conventions
  extensions, `UseTriggersConventional` + `AddTriggersFromAssemblies`, `UseProjectablesConventional`
- repositories — `EfRepository<TEntity, TId>`, `AddEfRepositories`, `AddEfRepository`, `AddEfWriteRepositories`,
  `AddCqrsRepository`

**Dapper** — `src/Data/Dapper/`

- `AddDapperConventions`, `SqlNamingMapper`, `EnumTypeHandler<TEnum>` + `AddEnumTypeHandler`, `DateOnlyTypeHandler`,
  `ListTypeHandler`, `SqliteConnectionFactory`
- `DapperRepository<TEntity, TId>`, `AddDapperRepository`, `AddDapperReadRepository`

**The composed entry** — `AddPostgresPersistence<TContext>(IConfiguration, …)` in `src/Data/`

- composes data source + connection factory + audit interceptor + snake-case EF context + bespoke migrator
- paired with `MigrateBespokeOnStartupAsync(this IServiceProvider, CancellationToken)` at boot
- maturity — **shipped · used** by 6 backends; it is the de-facto product persistence entry point

**Repository abstractions are shipped · unused.** No product references `IRepository<>` or `IReadRepository<>` —
products derive from `AppDbContextBase` and query inside CQRS handlers or product-local repository interfaces.

---

## Migrations

Three runners plus a CLI. The bespoke SQL migrator is the one products actually use.

**Bespoke SQL migrator** — `src/Data/Migrations/Bespoke/`

- `AddDatabaseBespokeMigrations` (2 overloads), `MigrationOptions`, `MigrationConventions`, `MigrationStatus`
- sources — `IMigrationSource`, `FileSystemMigrationSource`, `EmbeddedResourceMigrationSource`, `RawMigration`
- dialects — `IMigrationDialect`, `PostgresMigrationDialect`, `SqliteMigrationDialect`, `DatabaseProvider`
- engine — `IMigrationRunnerService` / `MigrationRunnerService`, `IMigrationScanner` / `MigrationScannerService`,
  `IMigrationHistoryRepository` / `MigrationHistoryRepository`, `MigrationHistoryEntry`, `MigrationDescriptor`
- integrity — `MigrationChecksumExtensions`, `MigrationDriftException`, `MigrationOrphanException`
- product shape — paired `Migrations/NNN-name/{Apply,Rollback}.sql` shipped as embedded resources

**Other runners**

| Runner | Entry point | Backing |
|---|---|---|
| EF Core | `AddEfMigrationsRunner` | `EfMigrationsBackgroundService`, connect-retry |
| DbUp | `AddDbUpRunner` | `DbUpBackgroundService`, `DbUpProviderFactory` |

**CLI** — `src/Data/Migrations/cli/`, `PackAsTool`, command `wow-migrate`

- verbs `apply` `new` `promote` `rollback` `status` `verify`; `MigrationsPathResolver`, `CliRunner`, `CliCommands`
- maturity — **shipped · used**; forever-pin, drydock and secrets-vault all run the bespoke path

---

## Messaging and the bus

The largest unused area — 57 source files, 39 registration methods, 25 test files, zero product consumers.

- lives in `src/Messaging/`; event-centric (`IEvent` only), topology-free
- core — `IEventBus`, `IEvent`, `IEventHandler<TEvent>`, `IBusControl`, `AddEventHandlersFromAssemblies`
- transport seam — `ISendTransport`, `IReceiveTransport`, `ITransportCapabilities`, `ReceiveContext`,
  `TransportEventBus`, `MessagePump`, `TransportConsumerBackgroundService`, `EventProcessingPipeline`

| Transport | Entry point | File |
|---|---|---|
| In-memory | `AddInMemoryEventBus`, `AddInMemoryEventTransport` | `InMemory/InMemoryTransport.cs` |
| RabbitMQ | `AddRabbitMqEventBus` | `RabbitMq/RabbitMqTransport.cs` |
| Kafka | `AddKafkaEventBus` | `Kafka/KafkaTransport.cs` |
| NATS | `AddNatsEventBus` | `Nats/NatsTransport.cs` |
| Redis Streams | `AddRedisStreamsEventBus` | `RedisStreams/RedisStreamsTransport.cs` |
| Azure Service Bus | `AddAzureServiceBusEventBus` | `AzureServiceBus/AzureServiceBusTransport.cs` |

- reliability — `IOutbox` / `EfOutbox` + `AddEfOutbox`, `IOutboxDispatcher` + `AddEfOutboxDispatcher`,
  `IInboxProcessor` + `AddEfInbox`, `IOutboxClaimStrategy` / `PostgresSkipLockedOutboxClaimStrategy`
- retry + DLQ — `AddDelayedEventRetry`, `AddSecondLevelEventRetry`, `IRetryPolicy`, `IDeadLetterRepository`,
  `IDeadLetterAdmin` + `AddDeadLetterAdmin`, `IDeadLetterQueryRepository` + `AddInMemoryDeadLetterQueryStore`
- resilience — `IEventResiliencePipeline`, `AddEventResilienceDefaults`, `AddPollyEventResilience`,
  `IEventFaultClassifier` + `AddEventFaultClassification`
- sagas — two models: `EventSaga` / `IEventSagaRunner` / `IEventSagaStep` routing slip (`AddEventSaga`), and
  `SagaStateMachine<TState>` / `ISagaState` / `ISagaRepository<TState>` / `SagaCoordinator` (`AddSaga`,
  `AddSagaRepository`, `SagaTimeouts`)
- serialization — `IMessageSerializer`, `CloudEventsMessageSerializer`, `MessagePackMessageSerializer`,
  `MessageSerializerRegistry`, `AddMessageSerializer`, `AddReceiveOnlyMessageSerializer`
- topology + routing — `ITopologyProvider`, `IEndpointNameMapper`, `IMessageTypeResolver`, `MapMessageType`,
  `AddMessageTopology`, `AddDestinationBinding`, `AddReplyAddressProvider`
- request/reply — `IRequestClient<in TRequest, TResponse>`, `AddRequestClient`
- observability — `IMessagingMetrics` + `AddMessagingMetrics`, `IConsumeObserver`, `IPublishObserver`,
  `IReceiveObserver`, `AddMessageObserver`, `MessagingDiagnostics`
- other seams — `IConsumeFilter` + `AddConsumeFilter`, `AddEventClaimCheck`, `AddMessagingConcurrency`,
  `IMessageHeaderPropagationPolicy` + `AddMessageHeaderPropagation`
- webhooks — `AddWebhooks`, `IWebhookPublisher` / `WebhookPublisher`, `IWebhookSubscriptionRepository`,
  `IWebhookDeliveryLog`, `WebhookSignatureHasher`, `WebhookSsrfGuard`
- maturity — **shipped · unused**. CAP adapters are folder-only (`src/Messaging/Cap/`); AWS SQS, Azure Event Hubs
  and MQTT folders exist with no transport file.

---

## Caching

- lives in `src/Caching/`; house contract `ICacheRepository` + `ICacheKeyBuilder` / `CacheKeyBuilder`, `CacheEntryOptions`

| Backing | Entry point |
|---|---|
| In-process | `AddInMemoryCaching` |
| HybridCache | `AddHybridCaching`, `HybridCacheRepository`, `HybridCacheConventionOptions` |
| Redis (L2) | `AddRedisDistributedCache` |

- maturity — **shipped · unused**. Cosmos, SQL Server and FusionCache folders exist but hold no source.

---

## HTTP clients and resilience

- lives in `src/Http/`

| Concern | Entry point | Backing |
|---|---|---|
| Resilience | `AddSdkResilience`, `HttpResilienceOptions` | `Microsoft.Extensions.Http.Resilience` (Polly v8) |
| Hedging | `AddSdkHedging`, `HttpHedgingOptions` | standard-hedging preset |
| Typed clients | `AddResilientClient` | plain typed / named `HttpClient` |
| Refit | `AddRefitApiClient` | Refit + SDK JSON |
| Headers | `AddConventionalHeaderPropagation`, `AddPropagatedHeaders` | `Microsoft.AspNetCore.HeaderPropagation` |
| OAuth2 client creds | `AddOAuth2ClientCredentials` | `OAuth2ClientCredentialsHandler`, `OAuth2TokenCache` |
| Mutual TLS | `AddMutualTls`, `MutualTlsOptions` | `SocketsHttpHandler` + client cert |

- maturity — **shipped · unused** by every product backend

---

## Observability

- lives in `src/Observability/`, 8 files, all thin registration wrappers

| Signal | Entry point |
|---|---|
| Logging | `UseSerilogConventional` (on `IHostBuilder`) |
| Tracing | `AddOpenTelemetryTracing` |
| Metrics | `AddOpenTelemetryMetrics` |
| Health | `AddHealthChecksBuilder` |
| OTLP export | `AddOtlpExporters` |
| Prometheus | `AddPrometheusMetricsExporter` |
| Azure Monitor | `AddAzureMonitorExporter` |
| Error observation | `AddAppErrorObserver`, `AppErrorObserver` |

- maturity — **shipped · used**, but always transitively through `AddApiDefaults`; no product calls them directly

---

## Testing harnesses

Four packages, split by tier.

**`Testing`** — `src/Testing/`

- host — `WebApiTestHost`, `WebApiTestBase<TEntryPoint>`, `MultiHostFixture`
- fixtures — `IAsyncTestFixture`, `IAsyncFixtureCollection`, `AsyncFixtureCollection`,
  `ContainerFixtureBase<TContainer>`
- containers — `PostgresFixture` `RedisFixture` `RabbitMqFixture` `KafkaFixture` `MongoDbFixture` `AzuriteFixture`
- auth — `AddTestAuth`, `UseTestUser`, `TestAuthHandler`, `TestCurrentUser`, `TestClaimTypeConstants`, `CookieExtensions`
- helpers — `Polling.UntilAsync`, `HttpExtensions` (`PostJsonAsync` `PutJsonAsync` `PatchJsonAsync`
  `ReadEnvelopeAsync` `AttachCookie` `AsJson`), `BogusFakerFactory`, `VerifyDefaultConstants.Initialize`
- `Testing/Assertions/` holds only `Assertions.md` — the assertions bundle is documented, not implemented

**`Testing.Data`** — `src/Testing.Data/`

- EF — `RelationalTestDb<TContext>` (`CreatePostgres` / `CreateSqlite`), `RelationalTestBase<TDb, TContext>`,
  `AddTestEntityFrameworkCore`, fixture-owned `RelationalTestDb<TContext>.Provider`, `RemoveAllForDbContext`, `RepointDbContext`
- migrator — `MigratorHarness`, `MigratorPostgresFixture`, `MigratorTestBase`, `MigrationsWorkspace`,
  `MigrationHistoryRow`, `NoOpBespokeMigrator` + `DisableBespokeMigrator`

**`Testing.Messaging`** — `MessagingTestHarness`, `MessagingRecorder` + `AddMessagingRecorder`, `SagaTestHarness`,
`SagaRecorder` + `AddSagaRecorder`, `RecordedMessage`, `RecordedTransition`. Unused.

**`Testing.Integrations`** — `FakeGitHubClient`, `FakeContainerRegistryClient`. Used by drydock.

- maturity — **shipped · used**; `RelationalTestDb` in 3 repos, `MigratorTestBase` in forever-pin

---

## Distributed extras

- **Email** — `src/Comms/Email/`; `AddEmailDefaults`, `IEmailSender`, `EmailOptions`. shipped · unused
- **Blob storage** — `src/Storage/`; `AddLocalBlobStorage`, `IBlobRepository`, `BlobInfo`. partial · unused
- **Jobs** — `src/Jobs/Hangfire/`; `AddHangfireJobs`, `UseHangfireJobsDashboard`. shipped · unused
- **Realtime** — `src/Realtime/`; `AddConventionalSignalR`, `UseConventionalWebSockets`. shipped · unused

- email providers — `AddMailKitEmailSender` (SMTP) · `AddSendGridEmailSender` · `AddSesEmailSender`
- job storages — `AddInMemoryHangfireJobs` (dev) · `AddPostgresHangfireJobs`
- realtime detail — `SdkHub<TClient>`, `IUserConnectionTracker` / `InMemoryUserConnectionTracker` +
  `AddUserConnectionTracking`, `AddRedisBackplane`, SSE via `SseEndpointExtensions` / `SseWriter` / `SseEvent`,
  raw sockets via `IWebSocketConnectionHandler` / `WebSocketAcceptExtensions`
- storage is partial — only the local filesystem backing (`LocalFileBlobRepository`); no S3, Azure or GCS

---

## SaaS extras

- **Tenancy** — `src/Tenancy/`; `AddTenancy`, `UseTenantResolution`, `AddTenantRowStamping`. shipped · unused
- **Feature flags** — `src/FeatureFlags/`; `AddFeatureFlags`, `AddOpenFeatureClient`. partial · unused
- **AI** — `src/Ai/`; `AddOllamaChatClient`, `AddTiktokenTokenCounter`, `ITokenCounter`. partial · unused

- tenancy detail — `ISettableTenantContext`, `AmbientTenantContext`, `ITenantRepository` / `InMemoryTenantStore`,
  `RequestTenantResolver`, `TenantResolutionMiddleware`, `TenantStampInterceptor`, `TenantModelBuilderExtensions`,
  `TenantInfo`, `TenancyConventionOptions`
- flags are partial — `FeatureManagerAdapter` over `Microsoft.FeatureManagement` + an OpenFeature seam only;
  LaunchDarkly, ConfigCat, Unleash, GrowthBook and Esquio folders hold no source
- AI is partial — Ollama chat + embeddings (`AddOllamaEmbeddingGenerator`) and a tiktoken counter only;
  OpenAI, Anthropic, Bedrock, Gemini, Llama, Vector, Mcp, SemanticKernel and KernelMemory folders hold no source

---

## Domain extras

| Capability | Lives in | Entry points | Maturity |
|---|---|---|---|
| Codes (QR / barcode) | `src/Codes/` | `AddCodeRendering` | shipped · used |
| Captions | `src/Media/Captions/` | `AddCaptionParsing`, `AddVttCaptionParser` | shipped · used |
| Tabular export | `src/Media/{Csv,Excel,Tabular}/` | `AddCsvExport`, `AddExcelExport` | shipped · unused |
| Geo | `src/Geo/` | `AddGeo` | shipped · unused |
| Localization | `src/Localization/` | `AddResxLocalization`, `AddHumanizing` | shipped · unused |
| Integrations | `src/Integrations/` | `AddGitHubIntegration`, `AddGhcrIntegration` | shipped · used |

- codes — `ICodeRenderer` / `CodeRenderer`, `IQrCodeRenderer`, `IBarcodeRenderer`, `IQrMatrixGenerator`,
  `ISvgRasterizer` / `SkiaSvgRasterizer`, `SvgRenderer`, `ModuleMatrix`, `CodeRenderRequest`, `RenderedCode`,
  plus a style model (`StyleSpec`, `GradientSpec`, `LogoSpec`, `EmojiSpec`, `ModuleShape`, `FinderShape`,
  `QuietZoneConstants`, `StyleSpecNormalizer`) — extracted from forever-pin, consumed back by it
- captions — `ICaptionParser` + VTT / SRT / TTML / JSON3 parsers, `ICaptionWriter` (VTT, SRT),
  `CompositeCaptionParser`, `CaptionFormatDetector`, `CaptionTrack`, `CaptionSegment`, `CaptionTimecode`
- geo — `GeoCoordinate`, `GeoBoundingBox`, `IGeoDistanceCalculator`, `GeohashEncoder`, `GeoJsonSerializer`
- localization — `ITextHumanizer`, `IRelativeTimeFormatter`, `AddRequestLocalizationConventions`
- integrations — `IGitHubClient` / `GitHubClient`, `IContainerRegistryClient` / `GhcrClient`,
  `IAccessTokenProvider` + `AddHttpContextAccessTokenProvider`

---

## Code generation

- **No Roslyn source generators exist.** Zero matches for `IIncrementalGenerator`, `ISourceGenerator`, `[Generator]`
  anywhere in the SDK, despite the repo `CLAUDE.md` naming "source-gen first" as a working rule.
- the only generation tool is `wow-migrate new` — scaffolds an `Apply.sql` / `Rollback.sql` migration pair
- repo scaffolding is a workspace concern, not an SDK one — the `create-repo` skill copies
  `wow-two-sdk-beta.product-template/`
- maturity — **stub**

---

## Product backends

11 backends reference the SDK. All are Clean-Arch .NET 10 over Postgres.

| Backend | Repo | Notes |
|---|---|---|
| forever-pin | `ventures/10x-venture-forever-pin` | the reference; 2 hosts, 4 test tiers |
| drydock | `wow-two-platform.drydock` | deploy control plane; 94 `.cs` |
| secrets-vault | `wow-two-platform.secrets-vault` | densest app layer; 109 `.cs` |
| transcript-forge | `ventures/10x-ventures-transcript-forge` | full 5-project split |
| tnis | `ventures/ventures.tnis` | plus an ingestion CLI |
| tbs | `ventures/track-2-transportbrain` | full 5-project split |
| sift · arcade · museums-gallery · tnis-mintrans | `ventures/…` | 3-project (Api / Application / Domain) |
| sample | `wow-two-sdk-beta.product-template` | the scaffold template |

### The reference backend — forever-pin

- layers — `Common.Domain` · `Domain` · `Application` · `Infrastructure` · `Persistence`, over two hosts
  (`Api`, `Redirect.Api`)
- SDK adoption at startup — `AddApiDefaults` · `AddPostgresPersistence<AppDbContext>` · `AddMediator` ·
  `AddMediatorValidationBehavior` · `AddCodeRendering` · `AddGuestSession` · `AddCurrentUser` ·
  `AddGoogleIdTokenVerifier` · `AddCookieAuthentication` · `AddValidationExceptionFilter` · `AddJsonStringEnums` ·
  `ConfigurationMapper.Load<T>` · `MigrateBespokeOnStartupAsync` · `UseApiDefaults`
- persistence — `AppDbContext : AppDbContextBase`, Postgres, snake_case, 10 bespoke SQL migration pairs
- tests — Unit (15) · Integration (6, `RelationalTestDb`) · E2E (12, `MultiHostFixture` + `PostgresFixture`) ·
  Migrations (8, `MigratorTestBase`)
- extraction candidates it carries — `IBillingBroker` + the Stripe slice, `ISlugGenerator`, `IDeviceMapper`,
  `IScanRecorder` channel-batching, `SubtypeRegistry` polymorphic-JSON plumbing, `ToProblem(AppError)`
- no `Directory.Packages.props` — versions are inline per csproj, against the CPM convention

### Adoption ranking

Registration methods by consumer-repo count: `AddMediator` 15 · `AddApiDefaults` / `UseApiDefaults` /
`AddPostgresPersistence` / `AddMediatorValidationBehavior` / `AddJsonStringEnums` 6 ·
`AddValidationExceptionFilter` 3 · `AddTimeProviders` / `AddMediatorLoggingBehavior` /
`AddMediatorExceptionToResultBehavior` / `AddCookieAuthentication` 2 · everything else 1 or 0.

**19 of 32 capabilities have zero product consumers.** That is the vector-completeness doctrine working as
designed — but it means most of the SDK surface is unproven against a real product.

---

## Platform and legacy orgs

### `wow-two-platform` — 17 repos, 14 empty

- 14 hold only a `.sln` with zero `Project(` entries, a `.gitignore`, sometimes a title-only `README.md`:
  `comms.infra` `core.app` `core.di` `core.exceptions` `core.validations` `data.relational` `data.transport`
  `design-patterns` `docs.api` `storage.cache` `storage.file` `contrimap` `main` `pipelines`
- their solution names carry a `Backbone.*` generation the beta SDK superseded
- `templates.ai` is a **stub** — 4 wired csprojs whose entire content is `public class Class1` ×4
- `drydock` and `secrets-vault` are the only real code, and they are products, not packages

### `wow-two-sdk` — 7 repos, 5 empty

- empty: `language.core` `language.linq` `ai.nlp` `ai.semantic-kernel` `package-analyzer`
- `language.serialization` — 15 `.cs`, 3 packages: `WoW2.Sdk.Language.Serialization.Json.System`,
  `…Json.Newtonsoft`, `…Json.Newtonsoft.Converters`
- `resilience-patterns` — 64 `.cs` across numbered sample projects (`N2_Reactive.CircuitBreaker`,
  `N4_ProActive.RateLimiter`, `N5_Reactive.Fallback`, …); reads as a KB-style catalogue, not a library
- neither is referenced by any product backend

---

## Doc drift

Found while verifying. Each is source-vs-doc, not opinion. `conventions/development/backend/` was mid-restructure
in the working tree on this date — re-check the two convention entries before acting on them.

- `engineering/architecture/package-registry.md` marks the whole **Caching** group `planned`; `AddInMemoryCaching`,
  `AddHybridCaching` and `AddRedisDistributedCache` are all implemented.
- the same file marks every **Data** row `scaffold`; `src/Data/` is the largest area (106 `.cs`) and 6 products
  depend on it in production.
- the same file lists `UseMySqlConventional` and a `Data.EntityFrameworkCore.MySql` package. Neither exists —
  the surviving EF providers are Postgres, SQL Server, SQLite and Cosmos.
- the same file lists `WoW.Two.Sdk.Backend.Beta.Testing.Assertions` as shipped; `src/Testing/Assertions/` holds
  only `Assertions.md`.
- the same file counts **16 OAuth providers**; source has **17** — it omits `AddTwitterAuthentication`.
- `conventions/development/backend/dotnet/mla/platform/startup-defaults.md` says `AddApiDefaults` folds in
  `AddValidationExceptionHandler`. Source calls `AddAppExceptionHandling`, which registers three handlers
  (`ValidationExceptionHandler`, `AppExceptionHandler`, `UnhandledExceptionHandler`) plus `AddAppErrorObserver`
  and `AddExceptionMapping`. The convention's fold-in table is a generation behind.
- the same doc cites the path `src/meta/ApiDefaultsExtensions.cs`; the folder is `src/Meta/`, and the mono-lib
  rule is that area folders are PascalCase.
- the repo `CLAUDE.md` states "**Source-gen first**" as a working rule; the SDK ships no source generator.
- drydock's `README.md` says EF Core / SQLite; the code calls `AddPostgresPersistence<DrydockDbContext>` and
  no `UseSqlite` appears anywhere in that repo.

---

## Not reached

Named so a later pass knows where to start, not as a to-do.

- `wow-two-kb` — 21 knowledge-base repos of runnable samples; excluded as learning material, not functionality
- per-symbol behavior — this pass reads registrations and contracts, never the bodies behind them
- the 8 non-reference product backends — sampled through package references and symbol greps only
- `src/Web/Contracts/`, `src/Foundation/Guards/` and `src/Localization/` were confirmed to exist but not
  examined beyond their public type names
- test coverage per area — file counts only (`Messaging.Tests` 25 · `Mediator.Tests` 11 · `Migrations.Tests` 10 ·
  `Foundation.Tests` 10 · `Data.Tests` 10 · `Web.Tests` 3 · `Identity.Tests` 1)
