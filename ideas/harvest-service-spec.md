# WoW Two Harvest — One 24/7 Harvester for Every Product

*Last updated: 2026-10-27*

> `harvest`: a standardized harvester that runs scheduled pipelines over sources — web pages, public channels, feeds,
> official provider APIs — captures what they publish, extracts records into a schema the consumer names, and delivers
> them. A WoW2 app, free to self-host, shipped in the [capability forms](../conventions/development/capability-forms.md).
>
> **Status:** chosen 2026-10-25 as one shared harvester grown from ListingShelf; analysis confirmed by the developer on
> 2026-10-27 (lead doc Inputs § *fourth answer*). First consumer [Events](events-service-spec.md); code scaffolded in
> `wow-two-sdk-beta.harvest`, slice 1 in progress.

## Problem

- Several products each need the same thing: a listings product captures marketplace ads; a rentals product pulls
  finished runs and classifies them; a fashion product needs events. Each would otherwise grow its own crawler,
  scheduler and classifier.
- A capture service that runs 24/7 for any scheduled request is built once and every product subscribes (T4 § 9).

---

## Concepts

| Concept | Is | Source |
|---|---|---|
| source | one harvestable origin: a site, a public channel, a feed, an official API — with its family, host policy and posture | T5 § 2.2 |
| source adapter | an adapter for one source family that declares step brokers, not a single read call | T9 § 1 |
| container | the visibility boundary: the shared `pool`, or a `private` container per tenant; a post lives in exactly one | T5 § 6 |
| pipeline | a standing harvest of a source in a container, identified by `(container, source, scope_key)` | T7 § 2.1 |
| subscription | one tenant's interest — a `channel`, a `tag` set or a `keyword` set — with its own delivery, schema, AI switch and budget | T7 § 3.1 |
| schedule | one cadence row of a pipeline: kind, mode, spec, window, `next_due_at` | T7 § 2.5 |
| run | one execution of one schedule or trigger, with status, counts, steps and outcomes | T7 § 2.6 |
| capture | an immutable (inside its retention window) dated snapshot of one link, written only on content change | T5 § 2.2 |
| link · reading | one post at one source URL or id (`post_links`); the latest extraction of that link (`link_readings`) | T5 § 2.2 |
| post | the canonical record, derived from its links' readings with provenance per field, never patched in place | T5 § 4 |
| item | one delivered reading in a consumer's schema; Events' `observation` is this delivered reading (names must not collide) | T5, T8 § 6.3 |
| schema | a versioned JSON Schema a consumer registers, such as `wow2.event.v1`, over Harvest's base `wow2.post.v1` | T6 § 1, § 3 |
| delivery | an event sent to a consumer, signed, at least once, idempotent on item id | T7 § 5 |

- the layers run `source` → `capture` → `link_readings` → `post_links` → `posts`, each inside a `container` (T5 § 2.2).

### Source families

`SourceFamily` (contract, `Abstractions/Sources`): `page` · `structured` · `site` · `render` · `api` · `feed` · `link` ·
`listing` · `telegram` · `whatsapp` · `instagram` · `facebook` · `youtube` · `threads` · `x` · `intake` · `manual`.

| Group | Families | Read route |
|---|---|---|
| web | `page`, `structured` (JSON-LD / microdata / OpenGraph `Event`), `site` (sitemap + `lastmod`), `listing`, `render` | direct polite fetch; `render` headless where a page needs it (T3 § 2, T9-25) |
| feeds | `feed` (RSS, ICS) | direct fetch (T3 § 2.6) |
| messaging | `telegram` public channels (web preview, no account), `whatsapp` (consented intake + public channel snapshots) | public preview and consented intake only (T1 § 5, P6) |
| official APIs | `api`, `youtube`, `threads`, `x`, `instagram`/`facebook` business discovery | the platform's own API, under its terms (T9-5) |
| intake · manual | `link`, `intake` (forwards, uploads, webhooks), `manual` (hand-typed entry) | consumer- or user-submitted (T1, T7 § 6) |

- **must** prefer an official API or a feed over page capture when the source offers one (T3).
- the generic family readers — RSS, ICS, JSON-LD `Event`, sitemap, link cards — are public in Harvest, so a
  self-hosted Harvest reads something on day one (T9-26). A named source is a broker in the private adapters repo
  (*Placement*).

---

## Steps

A pipeline is a declared list of steps; an adapter declares step brokers over its family. The step and capability
contract lives in **`Harvest.Abstractions`** (contract § *Engine seams*), where the code put it — not in a core or
Social package.

| Role (`StepRole`) | Does | Emits |
|---|---|---|
| `enumerate` | lists what exists | `detail` targets, the next page, an enumeration-complete flag |
| `detail` | fetches one post — a page or an API object | a capture; `media`, `thread` targets |
| `media` | copies images and video into File Storage | media refs |
| `thread` | reads comments and replies | child links (`role = reply`) |
| `check` | probes whether a post still exists | a link signal (T5 § 5.3) |
| `metrics` | snapshots counters outside the content hash | a metric series (T1-P10) |
| `extract` | the extraction cascade (T6) | a reading |
| `contact` | reads contact points from captured text (keyed, T5 § 3.5) | contacts on the reading |

- `AdapterDescriptor` maps work kinds to step plans; `WorkKind` (contract) = `capture` · `discover` · `refresh` ·
  `sweep` · `check` · `metrics` · `link` · `intake` (T9 § 1.3). A `sweep` is `discover` + `refresh` + `check` on one
  frontier with a night window.
- **render is a capability a `detail` step may require, not a step of its own** (T9 § 1.2); its home is a core companion
  package (*Placement*).
- fan-out: a step enqueues work items for later steps of the same run (list → details → media). This is the frontier,
  generalized from URLs to step items (T9 § 1.2).
- the contract carries capability seams (`Abstractions/Capabilities`, `Steps/StepRequirements`). **Slice 1 binds only
  direct polite fetch**; a step a source blocks records the block as an outcome and the run backs off (contract § *Engine
  seams*: `R0`–`R1` live, richer rungs report `capabilityUnavailable`). Harvest does not work a block around (*Posture*).
- `ProviderJob` and `AccountOp` roles exist in the contract enum; this slice exercises only the direct-fetch roles
  above (contract § *Engine seams*).

---

## Posts: model, dedup, deletion checks

### Model (T5 § 4, § 2.2)

- a capture is **immutable inside its retention window**, written **only on content change**; unchanged polls touch
  `link_schedule`, not a new capture (T5-2).
- the canonical post is **derived** from its links' readings by rule, with provenance per field (`field_prov`). This
  makes unmerge, purge propagation and after-the-fact `ai_allowed` revocation recomputations, not data repairs (T5 § 4).

### Dedup (T5 § 3)

A deterministic ladder, inside a container; tiers 0–2 run in the ingest transaction, 3–6 in a job within minutes.

| Tier | Evidence | Decision |
|---|---|---|
| 0 link identity | `(source_id, external_key)`, platform id, normalized URL | upsert |
| 1 exact cross-link keys | forward origin, `rel=canonical`, JSON-LD `url`/`@id`, `hreflang`, locale-path swap | auto-merge, confidence 1.0 |
| 2 normalized text | equal `text_norm_hash` (≥ 80 chars), no veto | auto when same publisher or ≥ 1 corroboration; else review |
| 3 near-duplicate | `pg_trgm` on Latin-transliterated `match_text`, bounded by kind and time | auto with corroboration and no veto; else review |
| 4 media | perceptual hash within 6 bits, non-generic | corroboration, or review |
| 5 contacts | keyed phone hash, author handle | corroboration, or review |
| 6 embeddings | pgvector cosine — review suggestion only, never auto, gated by `ai_allowed` and container flag | review only |

- **merge guards (vetoes):** different `kind`; number-token Jaccard < 0.8; event dates differing beyond precision;
  disjoint contact-key sets; across containers; a `non_matches` pair; cross-locale unless tier 1 (T5 § 3.6).
- merges are `move_link` and **undoable**; a private container matches the pool at tiers 0–1 only, to make an alias
  (T5 § 3.9, § 6.1).

### Deletion checks (T5 § 5)

- link states (`LinkState`): `live` · `suspect` · `gone` · `relisted`; post states (`PostState`): `live` · `suspect` ·
  `gone`.
- a `suspect` precedes `gone`; **only** a `completed` run over a `complete` enumeration may infer absence, and a block,
  challenge, rate limit, render need or network error is never an authoritative negative (T5 § 5.2).
- post rollup: `live` if any link lives; `suspect` if none live but one suspect; `gone` only when every verifiable link
  is gone; unverifiable sources abstain (`verifiable = false`) (T5 § 5.4).
- a source `unavailable` for 30 days is retired by a human, never auto-`gone` (T5-22).

---

## Extraction and AI gates

### The cascade (T6 § 2.1)

Fixed order **D → R → E → S → L**; every capture yields the base envelope `wow2.post.v1`; a later tier fills only gaps.

| Tier | Fills | Cost |
|---|---|---|
| **D** deterministic | API fields, JSON-LD / microdata / OpenGraph, selectors, ICS / RSS | CPU only, never skipped |
| **R** rules | regex, lexicons, gazetteer, script and language rules (prices, phones, dates in uz/ru/en, tags) | CPU only, never skipped |
| **E** embeddings | one multilingual vector; nearest-centroid tags for posts the lexicons miss | ~$0.008 / 1,000 |
| **S** small model | zero-shot tags, gap-fill of base fields, simple consumer schemas | ~$0.12 / 1,000 |
| **L** large model | many-field or hard consumer schemas | ~$5.7–11.3 / 1,000 |

- Harvest **always delivers captures**; D and R run on every post; **E/S/L run only when the gates allow** (T6 § 2.1,
  spec decision 2026-10-26). The build runs end to end on D and R alone.
- a consumer schema is a **mapping first** (JSON-pointer paths + a closed function set); the model fills only gaps
  (T6 § 3). A JSON-LD `Event` page maps to `wow2.event.v1` with no model call.
- an out-of-scope post yields no item and the verdict is cached; instructions narrow what to keep, such as "fashion
  events in Central Asia" (T6 § 3.2).

### AI gates (T6 § 2.2)

`ceiling = min(G1..G5)`; D and R are never gated.

| Gate | Decides | Default |
|---|---|---|
| G1 pipeline `AiMode` (`off` · `gaps` · `full`) | tier ceiling | `off`; an events consumer `gaps` |
| G2 source `ai_allowed` | whether E/S/L may read this source's text | permissive per contract; a platform action or consumer contract flips one row |
| G3 host `ai-input` content signal | blocks E/S/L for that host when set | read from `robots.txt` per host |
| G4 data class | provider allow-list for public pool vs a private container | per class |
| G5 budget | monthly USD cap per pipeline and provider; soft 80%, hard stop | §5 (T6) |

- **contact numbers:** Harvest stores **keyed hashes only** — `HMAC-SHA256(pepper, kind‖value)`, phone to the last nine
  digits (T5 § 3.5). **No raw contact value is stored until Uzbekistan's personal-data law is read** (T5-12); raw values
  are masked before any model sees text unless a schema sets `needsContacts` (T6-15). A plain hash of nine digits is
  brute-forceable, so the key is an HMAC with a vault-held pepper (T5 § 3.5).
- extraction caches on `(inputHash, schemaId, schemaVersion, promptVersion)`; a changed capture re-extracts, an
  unchanged one reuses items (T6 § 3.3).

---

## Pipelines and subscriptions

- **pipeline vs subscription (T7, P10):** the pipeline `(container, source, scope_key)` is the shared harvesting unit;
  the subscription is per consumer, with its own delivery, schema, AI switch and budget share. The effective pipeline
  config is a pure function of its active subscriptions, source policy and operator overrides (T7 § 3.3).
- a whole-site pipeline is a **singleton per source and container**; consumers join, never duplicate. A filtered
  pipeline joins only on an identical `scope_key` (T7 § 2.1).
- **subscription kinds:** `channel` (creates or joins a pipeline, reads every post), `tag` and `keyword` (read the shared
  pool, never create a pipeline; a keyword may *propose* one) (T7 § 3.1, § 4.3).
- **config merge:** freshness as a max-staleness bound merged by min; limits by max, clamped to the adapter cap; AI per
  subscription; posture is source-level and a subscriber cannot widen it (T7 § 3.3).
- **budget:** a public pipeline's fetch cost is the operator's; a private pipeline's is the tenant's; AI is charged to the
  subscription that asked; a hard stop is on the pipeline, provider and global cap, never on a share (T7 § 3.4).
- **schedules** (`ScheduleMode`): `manual` · `interval` (≥ 5 min floor) · `cron` (IANA zone, default `Asia/Tashkent`) ·
  `adaptive`; `sweep` and bulk `refresh` run inside a night window; misfires coalesce (T7 § 2.5).
- **claim by host, not by run** (T7 § 7.3): the frontier is the queue (`FOR UPDATE SKIP LOCKED`); `host_state` holds
  concurrency (1), `min_delay` (≥ 2 s, adaptive), `crawl_delay` (robots, ≤ 30 s), `Retry-After` and backoff; a block on
  one host never stops another; results are fenced against a lost lease. A restart resumes, never reruns.

---

## Delivery

- one durable **event log per subscription**; rows hold references, the payload is rendered at send or read time
  (T7 § 5.1).
- **event types** (`DeliveryEventTypes`): `post.new` · `post.changed` · `post.extracted` · `link.state` ·
  `pipeline.run` · `pipeline.health` · `post.merged` · `post.unmerged` · `post.purged` · `post.relisted` (T7 § 5.2).
  `post.extracted` is optional; its absence is not an error.
- `pipeline.run{complete}` lets a consumer tell "nothing new" from "unchecked"; a `partial` or `failed` run never
  advances "last verified" or emits an absence inference (T7 § 2.7).
- **two doors on one log:** webhook push (Standard Webhooks signing; `webhook-id` stable across retries; 11 attempts over
  ~72 h; `410` suspends) and a **pull cursor** (`(xid8, id)` with the `pg_snapshot_xmin` horizon so a late-committing row
  is never skipped) (T7 § 5.3, § 5.5).
- at least once, per-post FIFO on push, `Idempotency-Key` on writes; a consumer dedups on `event_id` and applies the
  highest `revision` (T7 § 5.6).
- deliveries carry `retention_class` and `delete_by`, and a consumer must honour `post.purged` (T5 § 7.2, T7).
- the be sdk's inline `WebhookPublisher` is not at-least-once; a **durable dispatcher joins the be sdk**, shared with
  Identity; pull-cursor delivery ships first, webhook push after it releases (T7 § 5.4, T8-8).

---

## Storage (PostgreSQL)

- **PostgreSQL 16+, UTF-8, `pg_trgm`** (contract § *Store*); SQLite leaves with ListingShelf's code (T4).
- startup creates the database, refuses a non-UTF-8 one or one without `pg_trgm`, applies the named migration set
  `harvest`, and **refuses a database whose `show_trgm('привет')` is empty** — PostgreSQL has no Uzbek text-search
  configuration, so `simple` with prefix matching over Latin-transliterated text is used (T6 § 4.4, T5-5).
- tables carry the `harvest_` prefix in `public` beside a Form 1 host's own; `harvest_captures` and `harvest_link_metrics`
  are **monthly-partitioned**, referenced softly by `(id, timestamp)` with no foreign keys into them; a `maintenance` job
  creates months ahead (T5 § 2.3, § 9.3, contract § *Store*).
- the ~28-table inventory (containers, sources, host and retention and check policies, enumerations, captures, links and
  readings, posts and texts, contact keys, media, dedup tables; engine tables tenants, API keys, pipelines, schedules,
  runs, work items, host state, subscriptions, the event log) is T5 § 2.3 plus T7's engine set.
- captures and media go to WoW2's own File Storage instance through `ICaptureStore`; slice 1 runs on core `Storage/`
  until `Harvest.Files` binds Files (T8-9). A consumer that references a capture's file keeps it alive past pruning
  (T5 § 7). A self-hosted bundle ships its own File Storage instance.

---

## Retention

- classes (`retention_policies`, T5 § 7.1): `standard` · `youtube` · `meta` · `x` · `telegram` · `intake`. A class is
  data; `captures.expires_at` is computed at insert, so a later edit never lengthens a platform duty already stored.
- the purge job deletes the stored file, keeps a scrubbed stub for expiry, deletes the whole row for a data-subject
  request, then runs `ResolvePost` without the purged link and emits `post.purged` (T5 § 7.2).
- derived data — embeddings, tags, items — **inherits its capture's retention** (T6 § 7, P18).
- retention duties **travel downstream**: platform terms bind data received, so deliveries carry `retention_class` and
  `delete_by` and consumers must honour `post.purged` (T5 § 7.2, P18).
- official API routes force their class on; an operator cannot loosen it (T5 § 7.1, T9-5).

---

## Posture at sources

**Harvest fetches directly and politely.** The posture fields are switches (`permission`, `ai_allowed`, `robots_policy`,
`pool_shareable`, `posture`, `consent_basis`), permissive by default, so a takedown or ban is a one-row `UPDATE`
(T5 § 2.5, contract § *Registration*).

- **must** obey `robots.txt` (RFC 9309), honour per-host pacing and `Crawl-delay`, send conditional requests, honour
  `Retry-After`, keep a run-scoped anonymous cookie jar, and send one honest, identifying `User-Agent` naming the
  operator and a contact page (T3 W6, W13, W14; the operator names the domain).
- **must** record a block, rate limit or challenge as an **outcome** (`FetchOutcome`: `blocked` · `rateLimited` ·
  `challenge` · `waitingRoom` · `robotsDisallowed` · …) and back the run off; a block is reported, never worked around
  (T7 § 2.7, T5 § 5.2).
- **must** honour each platform's terms on **official API routes** (YouTube refresh windows, X compliance events, Meta
  sharing rules): the platform enforces by revoking the key, so Harvest keeps `retention_class` and `pool_shareable`
  honest there (T9-5).
- **may** render a page headlessly when its content needs it, through the core render companion (*Placement*); rendering
  is for reading the page, not for defeating a defence.
- a source family that offers an official API or a feed is read that way in preference to page capture (T3).

---

## Placement

- **Repos** (T8-4, T8-5, T9 § 8):
  - **`wow-two-sdk-beta.harvest`** (public) — the engine: steps, scheduler, runs and stats, containers of harvested
    posts, dedup, extraction, subscriptions, delivery, retention, and the generic family readers (RSS, ICS, JSON-LD,
    sitemap, link cards).
  - **`wow-two-sdk-beta.social`** (sibling domain) — the organization's own platform integrations: publish with
    receipts, own metrics, verification, and official-API transport. Social never depends on Harvest; Harvest's
    official-API adapters call Social's read brokers (T8-1, T8-2).
  - **a private adapters repo** — one broker package per named source, each referencing `Harvest.Abstractions`; it
    publishes to a private feed and builds WoW2's own Harvest image. Its internals stay out of this spec and the public
    repo (T9-19, P2d).
- **Chain:** core → Identity → Files → Social → Harvest → Events; `Harvest.Module` references core and
  `Social.Abstractions` only (T8-6, P2b).
- **Render → a core companion package** (Playwright is heavy and stateless per call), not a Harvest or Social package
  (T9-25, the latest; supersedes the earlier `Social.Browser` pick).
- **Packages** (contract, package registry): `Harvest.Abstractions` (contract) · `Harvest.Module` (Form 1) ·
  `Harvest.Client` (Forms 2/3) · `Harvest.Testing` · `@wow-two-beta/fe-harvest`; `Harvest.Files` and `Harvest.Social`
  are extension packages bound by the host.
- **Forms** (capability forms): **1 · library** — `Harvest.Module` in the host's process, schema `harvest` in its
  PostgreSQL. **2 · self-hosted** — the `harvest` image, one tenant, its own PostgreSQL and File Storage. **3 · provided**
  — WoW2's instance, `Tenancy:Mode = Shared`, serving Events and other apps. One image, `Tenancy:Mode = Single | Shared`
  (T8 § 5).

---

## First slice

**Scope: only what the Harvest build needs first** (T8 § 7). Product integrations are outside it.

1. scaffold `wow-two-sdk-beta.harvest` from the domain template; `Harvest.Api`, `apps/web`; this spec → `product/`, the
   analysis → `engineering/research/` after the private-fact strip (P2d).
2. SQL set `001`: the T5 post tables plus the engine tables; monthly `captures` partitions; the `show_trgm('привет')`
   boot self-test.
3. fetch lane (`Module/Web/`): a direct client over core `Http/Safety`; robots (RFC 9309), `host_state`, conditional
   GET, `Retry-After`, run-scoped cookies, outcomes.
4. engine lane: scheduler (`next_due_at`, coalescing), run model, claim-by-host with `SKIP LOCKED`, leases, fenced
   writes, frontier, work kinds `capture` · `discover` · `refresh` · `sweep` · `check`.
5. adapter lane: `structured` (JSON-LD `Event`), `site` (sitemap + `lastmod`), `page`, `feed` (RSS, ICS), public
   Telegram preview, `listing` (marketplace fixtures ported from ListingShelf).
6. extraction D and R: `wow2.post.v1`, dates with precision, prices, keyed contact hashes, script and language by rule,
   the JSON-LD `Event` → `wow2.event.v1` mapper.
7. post layer: link upsert, dedup tiers 0–2, post resolve, link state machine and rollup.
8. delivery: the transactional event log and pull cursor (`xid8` horizon), tenants and API keys over core
   `Identity/ApiKeys`; webhook push once the core durable dispatcher releases.
9. console: pipelines, runs, queue and hosts, subscriptions and deliveries — the `fe-harvest` minimum.
10. image, `deploy.yml`, dev rollout through Wheelhouse.

- **Gate:** two JSON-LD event sources are harvested on schedule; a fake Events intake receives each event once with
  source, dates and precision; a removed page becomes `suspect` then `gone`; a worker killed mid-sweep resumes with an
  intact frontier; one marketplace-listing fixture proves the second family.
- **Out of the slice:** Social; social-platform and official-API adapters; WhatsApp; the render tier; the E/S/L tiers;
  link intake and manual entries; tag and keyword subscriptions; retention purge beyond a stub; the shelf importer.

---

## Console

- built on the fe SDK, served single-host, SignalR merged by revision (T7 § 10) — **in Wheelhouse's look, refined after
  the developer's review**.
- screens: Overview · Pipelines (requested vs effective config per subscriber) · Runs (steps, counts, outcomes) ·
  Captures and posts · Queue and hosts · Sources (posture switches) · Subscriptions and deliveries (lag, dead letters,
  redrive) · Budgets · Review queues (low-confidence items, `suspect` gone, unrecognized pages, consent and deletion
  requests) · Tenants and keys · Settings.
- a tenant admin sees only its own containers, its subscriptions and the public pipelines it joined.

---

## Points

### Closed

- [x] H1 — repository → **a new `wow-two-sdk-beta.harvest`** from the domain template, ListingShelf's generic core
  copied with its source commit cited; ListingShelf stays the shelf view and keeps serving its dependants until it cuts
  over (T8-4, confirmed 2026-10-27).
- [x] H2 — first adapters → the **generic family readers** (`structured` JSON-LD, `site`, `page`, `feed` RSS/ICS) and
  public Telegram preview ship in slice 1; events sites are read by JSON-LD `Event`; an events site that requires
  permission waits for it (T8 § 7, W1, confirmed 2026-10-27).
- [x] H3 — consumer authentication until Identity lands → **per-tenant API keys** (`hv_` prefix, only the SHA-256 kept)
  plus an operator key holding every scope, over core `Identity/ApiKeys`; OIDC client credentials later (contract
  § *Access*, T7 § 9.1, confirmed 2026-10-27).

### Open

- [ ] secrets custody → **Secrets Vault** (T1, T5, T7) **vs** host files for static keys plus sealed database columns for
  mutable sessions and tokens (T8 § 5.2). Unresolved.
