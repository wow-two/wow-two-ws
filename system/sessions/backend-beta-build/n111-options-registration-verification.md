# N111 options registration verification

*Verified: 2026-09-16*

## Result

N111 is complete. SDK-owned code options now follow one of the documented registration paths:

- rule-free shared values are configured before `TryAddSingleton(instance)`;
- constrained values use `AddValidatedOptions<T>` with concrete rules and `ValidateOnStart`;
- provider topology defaults retain `PostConfigure<TDependency>` composition;
- SDK consumers inject the resolved options record directly.

Framework-owned options remain on their framework pipelines: request localization, response compression,
forwarded headers, host filtering, Kestrel limits and MVC JSON options.

## Changes

- Added startup rules for migration, EF migration, identity, TOTP, Telegram, JWT issuance, Google token,
  tenancy, email-provider, broker-provider, topology, request-client, retry, saga, outbox and webhook options.
- Preserved topology composition for Azure Service Bus, Kafka, NATS, RabbitMQ and Redis Streams.
- Replaced internal `IOptions<T>` consumption with direct SDK option records.
- Fixed delayed retry and second-level retry registration: resolving options no longer mutates
  `IServiceCollection` from inside a configuration callback.
- Kept direct singleton registration for rule-free `SesEmailOptions`, `SqlNamingOptions`,
  `ClaimNormalizationOptions`, `DeadLetterAdminOptions` and `SecondLevelRetryOptions`.

## Source inventory

The remaining production `AddOptions<T>` calls are intentional:

- two calls inside `OptionsRegistrationExtensions`, which implement the shared recipe;
- five provider `PostConfigure<TDependency>` calls that compose final `TopologyOptions`.

The remaining production `services.Configure` calls target framework-owned option types only.
No SDK-owned option record is consumed through `IOptions<T>` in production source.

## Verification

- `dotnet build WoW.Two.Sdk.Backend.Beta.csproj --no-restore -m:1` — passed, zero errors.
- focused `OptionsRegistrationTests` — 3 passed.
- `Identity.Tests` — 8 passed.
- `Migrations.Tests` — 17 passed.
- focused `DapperConventionLatchTests` — 4 passed.

The build still reports the dependency advisories and redundant `Microsoft.Extensions.Http` reference owned by
N115. Those warnings do not invalidate N111's registration behavior.
