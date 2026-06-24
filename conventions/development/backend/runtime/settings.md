# Settings

*Last updated: 2026-06-22*

Configuration classes that bind to `appsettings.json` sections via `IOptions<T>` or direct configuration binding.

## Location

`{Service}/Infrastructure/Settings/{Name}Settings.cs` — one file per settings class (per [code-organization.md](../code-style/code-organization.md)).

| Layer | Folder | Examples |
|---|---|---|
| Service-specific | `Infrastructure/Settings/` | `ClassificationSettings`, `ScrapeSettings` |
| Common (shared) | `{Repo}.Common/Settings/` | `CorsSettings`, `DbSettings` |

## Modeling

### Class shape

- **`sealed record`** — immutable after binding
- **Naming** — suffix with `Settings` (`ClassificationSettings`, `ScrapeSettings`)
- **No positional constructor** — body properties only (see [models.md](../code-style/models.md))

### Members

- **`{ get; init; }`** — set once by config binding, never mutated
- **Non-nullable** — `required` on every property unless the setting is genuinely optional
- **No defaults** — config binder must provide values; missing values should fail loudly

```csharp
/// <summary>Configuration for AI classification pipeline behavior.</summary>
public sealed record ClassificationSettings
{
    /// <summary>Gets the maximum number of listings per AI classification batch.</summary>
    public required int MaxBatchSize { get; init; }

    /// <summary>Gets the timeout in seconds for a single classification API call.</summary>
    public required int TimeoutSeconds { get; init; }
}
```

## Registration

Register in `HostConfigurationExtensions.AddSettings()` via `IOptions<T>` binding — see [host-configuration.md](../architecture/host-configuration.md):

```csharp
public static WebApplicationBuilder AddSettings(this WebApplicationBuilder builder)
{
    builder.Services
        .AddOptions<ClassificationSettings>()
        .Bind(builder.Configuration.GetSection("Classification"))
        .ValidateDataAnnotations()
        .ValidateOnStart();

    return builder;
}
```

- Use `ValidateOnStart()` — fail fast on missing/invalid settings
- Use `ValidateDataAnnotations()` when properties have `[Required]`, `[Range]`, etc.
- Prefer **source-gen options validation** (`[OptionsValidator]`) for runtime-free validation when the type is complex

## Documentation

Per the starter table in [documentation.md](../code-style/documentation.md):

### Settings class

- `/// <summary>` starts with **Configuration for**

### Properties

- `/// <summary>` starts with **"Gets the {property}"** — settings are init-only, so "Gets" not "Gets or sets"

```csharp
/// <summary>Gets the maximum number of listings per AI classification batch.</summary>
public required int MaxBatchSize { get; init; }
```

## Identity / auth config

Auth, OAuth, sign-in, and token concerns use the keyword **`Identity`** — aligning with the beta SDK (`WoW.Two.Sdk.Backend.Beta.Identity`). Apply where it fits:

- **Config section:** `Identity:` — `Identity:GitHub:ClientId`, `Identity:AllowedGitHubLogins`. Not `OAuth:` / `Auth:`.
- **Namespaces / folders:** `Identity` / `Identity/` (OAuth providers nest under it: `Identity.OAuth.GitHub`).

## Multiple environments

- Per-environment overrides via `appsettings.{Environment}.json`
- Env var overrides registered in `HostConfigurationExtensions.AddEnvironmentOverrides()` — map specific env vars to config keys, don't auto-bind everything
- **No product/brand prefix on env-var names** — UPPER_SNAKE by **role**, not by app: `DB_CONNECTION`, `REDIS_CONNECTION`, `BILLING_SECRET_KEY` — never `SMARTQR_DB_CONNECTION`. The repo / deployment scopes the env; the name states the role.
- Secrets (API keys, connection strings) — never in `appsettings.json`; use env vars, Azure Key Vault, or user secrets in dev

## See also

- [host-configuration.md](../architecture/host-configuration.md) — registration
- [models.md](../code-style/models.md) — record style
- [documentation.md](../code-style/documentation.md) — XML doc + starter table
