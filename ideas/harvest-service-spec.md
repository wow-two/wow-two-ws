# WoW Two Harvest — One 24/7 Harvester for Every Product

*Last updated: 2026-10-27*

> `harvest`: a standardized harvester that runs scheduled pipelines over sources — sites, Telegram channels, feeds,
> provider APIs — captures what they publish, extracts records into a schema the consumer names, and delivers them.
> A WoW2 app, free to self-host, shipped in the [capability forms](../conventions/development/capability-forms.md).
>
> **Status:** chosen 2026-10-25 as one shared harvester grown from ListingShelf; first consumer
> [Events](events-service-spec.md). Afisha intake is researched in the build chat.

## Problem

- ListingShelf captures OLX and Domtut listings; Haven pulls its finished runs over HTTP and classifies them with an
  LLM, with Telegram groups next in its backlog; Ocharo needs events from Afisha and fashion sources. Each would
  otherwise grow its own crawler, scheduler and classifier.
- A capture service that runs 24/7 for any scheduled request is built once and every product subscribes.

---

## Concepts

| Concept | Is |
|---|---|
| source adapter | how one kind of source is read: web page, provider API, RSS or ICS feed, Telegram channel |
| pipeline | a consumer's standing request: sources, schedule, limits, target schema, instructions, delivery |
| run | one execution of a pipeline, with status, counts, steps and errors |
| capture | an immutable, dated snapshot of one page or post, with its media and content hash |
| item | one record extracted from a capture into the target schema, with confidence and provenance |
| schema | a versioned JSON Schema the consumer registers, such as `wow2.event.v1` or `wow2.listing.v1` |
| delivery | an item sent to the consumer's endpoint, signed, at least once, idempotent on item id |

---

## From ListingShelf

- keeps: pipelines with `capture` · `discover` · `refresh` work, schedules, page and item limits, runs with status
  (`queued` · `running` · `completed` · `partial` · `failed` · `cancelled` · `interrupted`), immutable captures,
  change detection (`new` · `changed` · `gone` · `unchanged`), provider blocks surfaced as outcomes, live run events.
- adds: consumers and their schemas, LLM extraction into items, signed deliveries, File Storage for media, tenancy
  per consumer, authentication.
- the listings shelf itself becomes a consumer view on `wow2.listing.v1` items.

---

## Extraction

- a capture is extracted once per schema version and prompt version; the cache key is content hash + both versions.
- a changed capture extracts again; an unchanged one reuses its items.
- the model is configuration through the AI gateway: DeepSeek, OpenAI or Anthropic, with a fallback order.
- every item carries model, prompt version and confidence; low confidence still delivers, flagged for review.
- instructions narrow what to keep, such as "fashion events in Central Asia"; out-of-scope posts yield no item.

---

## Storage

- captures and their media go to WoW2's own File Storage instance —
  [instances per owner](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.files/blob/main/product/product.md#instances-per-owner).
- captures are pruned by retention; a consumer that references a capture's file keeps it alive.
- a self-hosted Harvest ships with its own File Storage instance in the same bundle.

---

## Behaviour at sources

- reads a source through the capabilities its pipeline steps require — sign-in, captcha avoidance, an IP server —
  instead of stopping at its terms: Telegram, Meta and Afisha offer no proper API to integrate with (developer
  2026-10-26). The capability framework is analysed in
  [T9](harvest-analysis-2026-10/t9-capabilities.md).
- keeps per-source rate limits and backoff; a block that no capability clears stays an outcome.
- prefers a provider API or feed over page capture when the source offers one.

---

## Placement

- **Repos** — decided 2026-10-26 and 2026-10-27:
  - `social` holds everything social media: trends, posting, monitoring, platform clients and account pools.
  - Harvest holds pipelines, steps, runs and stats, the container of harvested posts, dedup, extraction,
    subscriptions and trends learning, on top of Social's libraries.
  - a private repo holds one broker package per source, with the per-site workarounds; WoW2's own Harvest image
    references them.
  - IP servers and proxies are connection infrastructure in the be sdk, not Social
    ([T9 § 8](harvest-analysis-2026-10/t9-capabilities.md#8--developer-2026-10-27)).
- **Form 1 · library** — source adapters, pipeline runner and extraction in the be SDK.
- **Form 2 · self-hosted service** — the `harvest` image with its console of pipelines, runs and captures.
- **Form 3 · provided service** — WoW2's own instance serving Events and other WoW2 apps.

---

## Points

- [ ] H1 — repository: a new `wow-two-platform.harvest`, or ListingShelf widened and renamed
- [ ] H2 — first adapters: Afisha, Telegram channels, web pages, RSS and ICS — which ship with Events
- [ ] H3 — consumer authentication until Identity lands: API keys per consumer
