# Domains

*Last updated: 2026-09-10*

> Capability contracts, provider adapters and their shared lifetime boundary.

## Ownership

- must keep the capability contract provider-free; a vendor-specific rule belongs in a named provider folder.
- must describe guarantees here and published signatures beside the code.
- must keep framework syntax in framework/provider leaves, not in the capability contract.
- must let another domain link the owning contract rather than restate it.
- must keep source layout in [library architecture](../../../shapes/library/library.md).
- must keep optional-peer and import isolation in [delivery](../../../shapes/library/delivery/delivery.md).

---

## Lifetime

- must scope mutable clients, caches and buses to an app instance, or one request when server-rendering.
- must expose non-component access through an explicit instance handle, not a process-global user singleton.
- must return a disposer from a subscription and detach it with its owning scope.
- must dispose timers, listeners, observers, streams and owned requests when their owner ends.
- must revoke owned object URLs and release retained payloads on removal/disposal.
- must suppress stale async completion after reset, disposal, identity change or provider replacement.
- must distinguish consumer-owned work from shared work before cancelling it on unmount.
- must follow [compatibility](../../../shapes/library/platform/compatibility.md) for import, SSR and hydration guarantees.
- must follow [security](security/security.md) for configuration, session and payload trust.
- must keep registration opt-in under [product principles](../../../../../conventions.md#product-principles).

---

## Capabilities

| Domain | Owns |
|---|---|
| [analytics](analytics/analytics.md) | consent-gated product events |
| [api](api/type-mapping.md) | wire values and typed codecs |
| [auth](auth/auth.md) | session resolution and strategies |
| [config](config/config.md) | typed startup configuration |
| [data](data/state-and-data.md) | request outcomes and server caches |
| [feedback](feedback/feedback.md) | notice publication and rendering |
| [flags](flags/flags.md) | total flag evaluation |
| [forms](forms/forms.md) | editing, parsing and field binding |
| [i18n](i18n/i18n.md) | locale, messages and formatting |
| [icons](icons/icons.md) | decorative and semantic glyphs |
| [observability](observability/observability.md) | structured local records |
| [storage](storage/storage.md) | small synchronous persistence |
| [uploads](uploads/uploads.md) | admission and queue scheduling |
| [validation](validation/validation.md) | Standard Schema validation |

- must keep routing in the [app shape](../../../shapes/app/routing/routing.md).
