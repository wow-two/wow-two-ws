# Domain structuring

*Last updated: 2026-02-23*

Domains group related entities, enums, and operations. Large domains split into **subdomains** — each subdomain covers a distinct lifecycle phase or concern.

## Pattern

```
{Domain}/
  Core/           ← the entity itself: queries, models, DTOs, projections
  {Operation1}/   ← lifecycle phase or concern (e.g. Capturing, Processing)
  {Operation2}/
  ...
```

`Core/` is always present when a domain has subdomains. It contains the reusable read model — any consumer (CRM, API, reports, pipelines) can reference `Core` without pulling in operation-specific code.

## Example: a listings domain

A `Listings` domain spans the full lifecycle: scraping → classifying → querying → triaging → publishing. Each phase is a subdomain.

**Domain layer** (`{Repo}.Domain/Listings/`) — entities and enums:

| Subdomain | What it owns |
|---|---|
| `ListingsProcessing/` | The listing entity + classification outputs |
| `ListingCapturing/` | Raw external data before classification |
| `ListingsBoard/` | CRM triage state |

**Infrastructure layer** (`Infrastructure/Listings/`) — implementations grouped by subdomain:

| Subdomain | What it does |
|---|---|
| `Core/` | Read model — querying, filtering, projecting |
| `Capturing/` | Scraping raw listings from external sources |
| `Processing/` | Classifying raw → structured |
| `Publishing/` | Distributing to channels |

## `Core/` vs operation subdomains

| Put in `Core/` | Put in `{Operation}/` |
|---|---|
| Read queries (filter, search, paginate) | Write operations (scrape, classify, publish) |
| Request/response DTOs for API consumers | Pipeline nodes and orchestrators |
| Projections and view models | External API clients (LLM, scraper) |
| Shared constants or lookup helpers | Operation-specific models and settings |

## Naming rules

- **Domain folder** — PascalCase plural (`Listings/`, `Channels/`, `Locations/`)
- **Subdomain folder** — PascalCase gerund or noun describing the concern (`Capturing/`, `Processing/`, `Core/`)
- **Avoid generic names** — `Helpers/`, `Utils/`, `Misc/` are banned. If it doesn't fit a subdomain, it belongs in `Core/`
- **Mirror across layers** — if Domain has `Listings/ListingCapturing/`, Infrastructure has `Listings/Capturing/` (drop redundant prefix)

## Layer alignment

Domain and Infrastructure mirror each other but aren't forced to be 1:1. Infrastructure subdomains can exist without a Domain counterpart (e.g. `Publishing/` has no domain entities — it only formats and sends).

```
{Repo}.Domain/                          {Repo}.Service/Infrastructure/
  Listings/                               Listings/
    ListingsProcessing/   ←── mirrors ──→   Core/        (read model for the entity)
      Entities/                              Processing/  (classify pipeline)
      Enums/
    ListingCapturing/     ←── mirrors ──→   Capturing/   (scrape pipelines)
      General/
      Channels/Olx/
    ListingsBoard/        ←── (no infra) ── triage is DB-only, no infra logic yet
                          ←── (no domain) → Publishing/  (infra-only, formats + sends)
```

## See also

- [service-architecture.md](service-architecture.md) — the 5 layers
- [entities.md](../persistence/entities.md) — where entities live
- [enums.md](../persistence/enums.md) — where enums live
