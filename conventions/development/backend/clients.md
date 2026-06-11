# Clients

*Last updated: 2026-02-23*

External HTTP/API integration classes that wrap a single provider's API.

## Location

Clients live in integration folders grouped by provider:

| Layer | Folder | Examples |
|---|---|---|
| Common (shared across services) | `{Repo}.Common/Integrations/{Provider}/` | `TelegramClient` |
| Service-specific | `{Service}/Infrastructure/Integrations/{Provider}/` | `LocationApiClient` |

## Modeling

### Class shape

- **Non-static** class
- **`HttpClient`** injected via primary constructor (typed `HttpClient` pattern) — or provider-specific SDK type when wrapping an SDK
- **Sealed** unless inheritance is needed
- **Naming** — suffix with `Client`, prefixed with provider name

### Lifetime

Register via `AddHttpClient<T>()` for typed HTTP clients — handled by `IHttpClientFactory`:

```csharp
builder.Services.AddHttpClient<TelegramClient>(c =>
{
    c.BaseAddress = new Uri("https://api.telegram.org/");
    c.DefaultRequestHeaders.Add("Accept", "application/json");
});
```

### Configuration

- Settings injected via `IOptions<TSettings>` — base URL, API key, timeout
- Settings type follows [settings.md](settings.md) rules — `sealed record`, `init`-only
- Never hard-code base URLs or credentials in the client

## Naming

| Pattern | When | Example |
|---|---|---|
| `{Provider}Client` | Single-provider HTTP wrapper | `TelegramClient`, `ClaudeClient` |
| `{Provider}{Domain}Client` | Multi-domain provider with separate clients | `GoogleMapsClient`, `GooglePlacesClient` |
| `{Provider}ApiClient` | Generic wrapper around a provider's REST API | `LocationApiClient` |

## Documentation

Per the starter table in [documentation.md](documentation.md):

### Client class

- `/// <summary>` starts with **Wraps** or **Integrates with**
- `/// <remarks>` describes the provider, base URL strategy, and key operations

```csharp
/// <summary>Wraps the Telegram Bot API for sending messages and managing topics.</summary>
/// <remarks>
/// Uses raw HTTP — no Telegram.Bot NuGet dependency.
/// Bot token and chat ID configured via TelegramSettings.
/// </remarks>
public sealed class TelegramClient(HttpClient http, IOptions<TelegramSettings> settings)
{
    public Task SendMessageAsync(...) { ... }
}
```

### Method docs

- `/// <summary>` one-liner — verb start (`Sends`, `Gets`, `Posts`, `Uploads`)

## Error handling

- HTTP errors bubble up — let the calling service handle / translate
- Don't catch `HttpRequestException` inside the client (loses context)
- Provider-specific error responses get deserialized to a typed model — return Result or throw a typed exception

## See also

- [services.md](services.md) — service naming + DI lifetime
- [settings.md](settings.md) — settings records
- [documentation.md](documentation.md) — XML doc + starter table
