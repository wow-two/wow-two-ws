# Clients

*Last updated: 2026-09-10*

> The call surface of one external provider, expressed in that provider's own model.
> Purpose — a client adds nothing of ours, so swapping the provider changes the seam above it, never the callers.
> Use case — a third-party or sibling API; the app-facing abstraction over it is a [broker](broker.md).

## Location

### Folder
- must sit in an `Integrations/{Provider}/` folder, one folder per provider.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Connects**, name the provider's API, and name what it reaches there.

```csharp
// ✅ the provider and the surface, both named
/// <summary>Connects to the Telegram Bot API for messages and topics.</summary>
// ❌ Integrates is the broker's starter — this type speaks the provider's model
/// <summary>Integrates Telegram messaging.</summary>
```

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.
- must declare the provider transport as a collaborator.

```csharp
// ✅
public sealed class TelegramClient(HttpClient http, IOptions<TelegramSettings> settings)
// ❌ hard-coded base address, and no injected transport
public sealed class TelegramClient { private readonly HttpClient http = new(); }
```

### Type name
- must suffix with `Client`, prefixed by the provider — `TelegramClient`, `LocationApiClient`.
- must qualify with the domain when one provider needs several — `GoogleMapsClient`, `GooglePlacesClient`.
- must name a Refit interface `I{Provider}Api` — `IBillingApi`.
- failure modes and carrier selection → [results](../../components/result.md).

Registration, resilience and cross-cutting handlers → [http integrations](../../domains/integrations/http/http.md).
