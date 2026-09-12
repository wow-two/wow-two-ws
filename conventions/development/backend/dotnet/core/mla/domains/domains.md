# Domains

*Last updated: 2026-09-10*

> One folder per capability a service consumes — the contract it guarantees, and each provider that implements it.
> Purpose — an entity is not tied to a provider, an `IEntityTypeConfiguration<T>` is; the split keeps them apart.
> Use case — adding a technology, or reading how an existing one is wired end to end.

## The shape

```
{domain}/
  {domain}.md        ← the contract: what the capability guarantees, provider-free
  {provider}/        ← one folder per implementation, everything technology-tied
```

- must keep the lead doc provider-free — a rule naming a technology sits in that technology's folder.
- must give each provider its own folder, named for the technology — `ef/`, `dapper/`, `redis/`.
- must let a second domain cite this contract rather than restate it; a shared capability is its own domain.
- must not group domains by tier — a domain is the unit, and grouping hides which contract a provider serves.

---

## Built

| Domain | Contract | Providers |
|---|---|---|
| [persistence](persistence/persistence.md) | the entity, its schema, keys and traits | `ef/` · `dapper/` · `sql/` · `dbup/` |
| [messaging](messaging/messaging.md) | the message, its handler, and how it is dispatched | `mediator/`, transports |
| [api](api/api.md) | the HTTP surface — request, envelope, edge mapping | MVC controllers, minimal API |
| [identity](identity/identity.md) | claims, the account model, authorization | `jwt/`, cookie, OAuth |
| [integrations](integrations/integrations.md) | the client/broker seam and the transport guarantee | `http/`, vendor SDKs |
| [validation](validation/validation.md) | phases, field failures, layer independence | `fluentvalidation/` |
| [observability](observability/observability.md) | logs, tracing, metrics and diagnostic channels | SDK observability |

---

## Recognized

Named so a design in progress has somewhere to land; no folder until a rule needs writing.

- `caching` — the cache seam, key building, eviction · `memory` · `redis` · `hybrid`
- `blob` — the store seam, naming and lifetimes · `filesystem` · `s3` · `azure`
- must create a recognized domain's rules when a concrete requirement needs a shared contract;
  recognition alone does not request feature implementation.
