# Settings

*Last updated: 2026-02-23*

Configuration classes that bind to `appsettings.json` sections via `IOptions<T>` or direct configuration binding.

## Location

`{Service}/Infrastructure/Settings/{Name}Settings.cs` — one file per settings class (per [code-organization.md](code-organization.md)).

| Layer | Folder | Examples |
|---|---|---|
| Service-specific | `Infrastructure/Settings/` | `ClassificationSettings`, `ScrapeSettings` |
| Common (shared) | `{Repo}.Common/Settings/` | `CorsSettings`, `DbSettings` |

## Modeling

### Class shape

- **`sealed record`** — immutable after binding
- **Naming** — suffix with `Settings` (`ClassificationSettings`, `ScrapeSettings`)
- **No positional constructor** — body properties only (see [models.md](models.md))

### Members

- **`{ get; init; }`** — set once by config binding, never mutated
- **Non-nullable** — `required` on every property unless the setting is genuinely optional
- **No defaults** — config binder must provide values; missing values should fail loudly

```csharp
/// <summary>Configuration for AI classification pipeline behavior.</summary>
/// <example>ClassificationSettings</example>
public sealed record ClassificationSettings
{
    /// <summary>Gets the maximum number of listings per AI classification batch.</summary>
    /// <example>25</example>
    public required int MaxBatchSize { get; init; }

    /// <summary>Gets the timeout in seconds for a single classification API call.</summary>
    /// <example>30</example>
    public required int TimeoutSeconds { get; init; }
}
```

## Registration

Register in `HostConfigurationExtensions.AddSettings()` via `IOptions<T>` binding — see [host-configuration.md](host-configuration.md):

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

Per the starter table in [documentation.md](documentation.md):

### Settings class

- `/// <summary>` starts with **Configuration for**
- `/// <example>` contains the `appsettings.json` section name (the binding key)

### Properties

- `/// <summary>` starts with **"Gets the {property}"** — settings are init-only, so "Gets" not "Gets or sets"
- `/// <example>` — concrete value the section would contain

```csharp
/// <summary>Gets the maximum number of listings per AI classification batch.</summary>
/// <example>25</example>
public required int MaxBatchSize { get; init; }
```

## Multiple environments

- Per-environment overrides via `appsettings.{Environment}.json`
- Env var overrides registered in `HostConfigurationExtensions.AddEnvironmentOverrides()` — map specific env vars to config keys, don't auto-bind everything
- Secrets (API keys, connection strings) — never in `appsettings.json`; use env vars, Azure Key Vault, or user secrets in dev

## See also

- [host-configuration.md](host-configuration.md) — registration
- [models.md](models.md) — record style
- [documentation.md](documentation.md) — XML doc + starter table
