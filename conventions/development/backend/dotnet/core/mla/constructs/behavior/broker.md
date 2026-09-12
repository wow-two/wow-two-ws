# Brokers

*Last updated: 2026-09-10*

> The app-side seam over an external dependency, speaking our model rather than the provider's.
> Purpose — one place the app names an outside capability in its own words, so a provider swap stops here.
> Use case — when the app needs a capability rather than an endpoint: charge a card, store a file, resolve a place.

## Location

### Folder
- must sit in a `Brokers/` folder under the domain that consumes the capability.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Integrates**, and name the provider it fronts.

#### [Remarks](../../../lla/notation/documentation/remarks.md)
- must state the degradation in `<remarks>` when a caller has to act on it.

```csharp
// ✅ names the provider behind our vocabulary
/// <summary>Integrates the Stripe payment provider.</summary>
// ❌ Connects is the client's starter — this type speaks our model
/// <summary>Connects to the Stripe API.</summary>
```

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.
- must expose the integration through one interface.

### Type name
- must name the interface for the capability — `IBillingBroker`.
- must suffix with `Broker`, carrying both the capability and the provider — `StripeBillingBroker`.
- must keep the provider's name out of the interface; only the implementation names it.

```csharp
// ✅
public sealed class StripeBillingBroker(IStripeClient client) : IBillingBroker
// ❌ the interface names the provider, so a swap renames every call site
public interface IStripeBroker
```

---

## Content

- failure modes and carrier selection → [results](../../components/result.md).
