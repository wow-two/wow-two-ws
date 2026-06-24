# Naming

*Last updated: 2026-06-22*

> What — cross-cutting naming for backend types, members, and extension methods (the symbol name itself — not its file, namespace, or project).
> Purpose — the name says what a thing *does*; the brand lives in the package, never repeated inside the code it ships.
> Use case — reach for it whenever you name a class, method, extension, or a bool-returning member.

## No brand / product prefix

- a **type, member, or extension-method** name carries **no product / brand prefix** — the project and package already carry it, so repeating it inside is noise
- `MigrateDatabaseAsync` not `MigrateSmartQrDatabaseAsync` · `AddCors` not `AddSmartQrCors` · `DatabaseContext` not `SmartQrDbContext`
- **project / package names keep the brand** — `SmartQr.Api`, `WoW.Two.Sdk.Backend.Beta` — the carve-out is the name that identifies the *assembly*, not the code inside it
- every symbol under `SmartQr.*` is already smart-qr's; the prefix tells a reader nothing the namespace doesn't

---

## Registration and extension-method naming

For a library that ships `IServiceCollection` / host extensions (the SDK pattern). The `## No brand / product prefix` rule applies in full: the *package* carries the brand, the *method* carries the meaning.

- **extension class** — on `IServiceCollection`, name `<Area>ServiceCollectionExtensions` (Microsoft's pattern); on any other type, `<Target>Extensions` or `<Area><Target>Extensions` — `TimeProviderExtensions`, `LoggingBuilderExtensions`, `EndpointConventionBuilderExtensions`
- **registration methods carry NO brand prefix** — describe what the call concretely registers, not who built the wrapper — `AddJwtBearerAuthentication` not `AddWowTwoJwt`, `AddOpenTelemetryTracing` not `AddWowTwoTracing`
- **acid test** — if you'd want to add `// these are wow-two's defaults`, the name is wrong; bake the meaning in so a reader who never heard of wow-two knows what it does

| Pattern | Example | When |
|---|---|---|
| `Add<Concrete>` | `AddJwtBearerAuthentication`, `AddOpenTelemetryTracing` | scheme / system-specific registration |
| `Add<Default><Thing>` | `AddDefaultCorsPolicy`, `AddDefaultOutputCache` | pre-set policy / configuration |
| `Add<Specific><Thing>` | `AddPerIpSlidingWindowRateLimit`, `AddBrotliGzipCompression` | picks one strategy among many |
| `Use<Concrete>` | `UseOwaspSecureHeaders`, `UseSerilogConventional` | pipeline middleware |
| `Map<Endpoint>` | `MapOpenApiEndpoint` | endpoint routing |
| `Add<Lib>FromAssemblies` | `AddFluentValidatorsFromAssemblies` | assembly-scanning registration |

- **stable consumer-visible identifiers stay brand-free** — cookie names (`.app.auth`), policy names (`"default"`) need system-wide uniqueness and may collide with consumer-defined names; never bake `wow-two` in
- **exception — `ActivitySource` / `Meter` names DO use the brand**: `WoW.Two.<Area>` is an *intentional* prefix so trace / metric filtering works at scale across services; this is the one place the brand belongs inside the code

---

## Predicates — `Is` / `Has` / `Can`

- a **bool-returning** method or property starts with `Is` / `Has` / `Can` (or `Should` / `Was` when tense fits), never `Be`
- `IsAbsoluteHttpUrl` not `BeAbsoluteHttpUrl` · `HasPendingChanges` · `CanRetry`
- `Be*` is FluentValidation predicate slang (`.Must(BeValid)`) — it reads as an assertion, not a state query; keep it out of method names even when the method backs a `.Must(...)`

---

## Specific naming lives by area

- service / client / factory → [services.md](../architecture/services.md) · query / command / handler → [mediator.md](../messaging/mediator.md) · entity / settings / DTO → [models.md](models.md)
