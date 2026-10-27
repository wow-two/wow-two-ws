# Harvest — full analysis before the build

*Last updated: 2026-10-27*

> The analysis batch behind Harvest (#17 in [platform apps](../../docs/platform-apps.md)): every source family,
> what Ocharo and Haven need from it, the post model with dedup and deletion checks, extraction and subscriptions,
> and where social-media logic lives. The [service spec](../harvest-service-spec.md) stays the build source; settled
> findings move into it, and this folder keeps the evidence.

## Inputs

- spec: [harvest-service-spec.md](../harvest-service-spec.md) — one shared harvester grown from ListingShelf
  (developer 2026-10-25); first consumer [Events](../events-service-spec.md).
- code today, read 2026-10-26:
  - ListingShelf — generic pipeline, run and capture core; OLX and Domtut HTML brokers behind `IListingBroker`;
    SQLite, one run at a time, no LLM, no auth; listing, change, absence and photo endpoints plus run exports, all
    unauthenticated and loopback-only.
  - Haven — no Telegram ingest; its supply `channels` are `olx-uz` and `domtut-uz`, pulled from ListingShelf run
    exports every 15 minutes and classified by an LLM (Sonnet, OpenAI fallback) into a rental listing schema.
  - Ocharo Desk Events — built and verified locally, never deployed; ingest is manual entry, bundle import, and a
    weekly Claude scheduled task (web search → bundle → import); no crawler.
- capability forms: [capability-forms.md](../../conventions/development/capability-forms.md); domain repos:
  [domain structure](../../conventions/development/repo/structure/domain-structure.md).

### Developer, 2026-10-26

- scope: Harvest's infrastructure and what Ocharo and Haven need from it; how and when Ocharo and Haven change is
  later work, outside this analysis.
- sources are many adapter families: Telegram, WhatsApp, browser, provider API, one tailored adapter per social
  platform (X, Reddit, Facebook, Instagram …), and hand-typed entry for certain user roles only.
- a product such as Ocharo submits links and manual entries; a link goes to Harvest's private container for that
  product (Ocharo's private events container) unless its domain is already harvested publicly.
- small sites such as iticket and afisha are harvested whole — every available post — on manual or automatic
  schedules, unlike OLX's filtered pipelines.
- dedup: one improved post with every source linked to it, in separate tables; deletion checks run on automatic and
  configurable schedules.
- extraction: Harvest analyses high-level fields per source and stores them; each product breaks them down further
  and stores them its own way.
- Harvest always delivers captures, and AI runs optionally per pipeline — less AI usage; analysed further later.
- subscriptions: a product subscribes to channels, which creates or joins a pipeline, and to tags or keywords, which
  read the shared pool of classified posts from many channels.
- storage: PostgreSQL, per convention; SQLite leaves with ListingShelf's code.
- asked: should one social-media repo hold Harvest, since Ocharo and other products need social integration for
  other logic too (publishing, metrics, sign-in)?

### Developer, 2026-10-26, second answer

- repos: two. `social` holds everything social media — trends, posting, monitoring — and the shared integration
  libraries, such as IP servers. Harvest runs mass actions over posts, trends learning included, on top of Social's
  libraries.
- harvesting: integrations act as brokers, and pipelines define steps. One site needs sign-in, another needs captcha
  avoidance (OLX, in Haven's case), another needs an IP server for one exact step — so a framework of capabilities
  that each source can use.
- terms: not honoured, because Telegram, Meta and Afisha offer no proper API to integrate with; if a platform blocks
  us, an IP server or similar handles it.

### Developer, 2026-10-27

- IP servers belong in neither Social nor Events: they are infrastructure for connections, perhaps a separate library
  in the be sdk.
- per-site workarounds go to a private repo of adapters that publishes its own libraries, one broker per source; the
  platform references them and integrates them directly.
- Harvest stays about pipelines, stats and the container of harvested posts.
- asked: is robots.txt our configuration, and should it use another format?

### Developer, 2026-10-27, fourth answer

- all points confirmed as their provisional picks, except the defence-bypass parts, which are not pursued.
- Harvest fetches directly and politely — robots policy, per-host pacing, `Retry-After`, conditional requests,
  run-scoped anonymous cookies, one honest User-Agent — and records a block, rate limit or challenge as an outcome,
  then backs off; it never works a block around.
- not pursued: captcha solving; proxy or IP rotation and the "IP server" used to avoid blocks; the escalation ladder;
  account or session pools for signing in to scrape; disguised or rotating client profiles; per-site bypass recipes
  (the phone-reveal flow); ignoring source terms.
- official API routes honour their platforms' terms (T9-5).
- the console takes Wheelhouse's look, refined after the developer's review.
- the spec is rewritten from this answer (2026-10-27); the defence-bypass picks are kept here as the record, marked
  `not pursued`.

---

## Tracks

| # | Track | File | Wave | State |
|---|---|---|---|---|
| T1 | Messaging sources: Telegram and WhatsApp | [t1-messaging-sources.md](t1-messaging-sources.md) | 1 | ✅ |
| T2 | Social platforms: Instagram, Facebook, X, Reddit, TikTok, YouTube, Threads, LinkedIn | [t2-social-sources.md](t2-social-sources.md) | 1 | ✅ |
| T3 | Web sources: pages, browser, whole-site, provider APIs, feeds, link intake; build vs wrap | [t3-web-sources.md](t3-web-sources.md) | 1 | ✅ |
| T4 | Consumer needs (Ocharo, Haven, others) and the social-integration inventory | [t4-consumers-and-social.md](t4-consumers-and-social.md) | 1 | ✅ |
| T5 | Post model: captures, sources, canonical posts, dedup, deletion checks, containers | [t5-post-model.md](t5-post-model.md) | 2 | ✅ |
| T6 | Extraction and classification: per-source fields, tags, AI tiers, cost | [t6-extraction.md](t6-extraction.md) | 2 | ✅ |
| T7 | Pipelines, schedules, subscriptions, workers, delivery, roles | [t7-pipelines-delivery.md](t7-pipelines-delivery.md) | 2 | ✅ |
| T8 | Placement: social domain vs Harvest domain, ListingShelf reuse (H1), forms | [t8-placement.md](t8-placement.md) | 3 | ✅ |
| T9 | Steps and capabilities: pipeline steps, the capability framework, the Social cut redrawn | [t9-capabilities.md](t9-capabilities.md) | 4 | ✅ |

- all four waves landed 2026-10-26; wave 4 (T9) followed the developer's second answer.

---

## Points

The decision queue: parents before children, blocking first. Each line: the question → the pick, and the track
holding the evidence. Tick a line when the developer answers; the answer moves into the spec.

### A · Placement — blocks the build

- [x] P1 social media and Harvest → answered 2026-10-26: two repos. `social` holds everything social media —
  trends, posting, monitoring — and the shared integration libraries, such as IP servers; Harvest runs mass actions
  over posts, trends learning included, on top of Social's libraries (T4, T8-1)
  - T8 § 1.4 kept platform readers and the Telegram pool in Harvest; T9 redraws that cut under this answer
  - 2026-10-27: IP servers leave Social for connection infrastructure in the be sdk (T9-24)
- [x] P2 (H1) Harvest's repo → confirmed 2026-10-27: a new `wow-two-sdk-beta.harvest` from the domain template with
  ListingShelf's generic core copied and its source commit cited; ListingShelf stays the shelf view (T8-4)
- [x] P2a org → confirmed 2026-10-27: `wow-two-sdk-beta` for Harvest, Social and Events, which repoints their catalog
  entries and edits platform-apps rows 16 and 17 (T8-5)
- [x] P2b chain → confirmed 2026-10-27: core → Identity → Files → Social → Harvest → Events, no cycle over 33 package
  nodes; Events renames its tracking `pipeline` to `workflow` (T8-6, T8-13)
- [x] P2c slug for Social → answered 2026-10-26: `social` (T8-2)
- [x] P2d research in a public repo → confirmed 2026-10-27: strip the analysis' private facts before it moves into the
  public Harvest repo (T8-5)

### B · Source terms — blocks the source picks

- [ ] P3 posture: the spec says "must honour each source's terms", and three terms collide with the plan →
  not pursued 2026-10-27: Harvest reports blocks as outcomes and does not escalate — the 2026-10-26 answer was: not honoured, since these platforms offer no proper API; a block routes through a capability
  such as an IP server (T9). The counsel gates in T1-P1, S1, W1, W5 and P4 fall away; T9 re-reads the defaults
  (T1-P1, S1, W1, W5)
  - Telegram API Terms §1.5: no Telegram data for AI "development, enhancement or deployment" (read 2026-10-26)
  - Meta Automated Data Collection Terms (2024): no automated collection without written permission
  - Afisha terms: prior written permission to copy or use material
- [ ] P4 licensed providers (Apify) for Instagram, Facebook and TikTok public pages → not pursued 2026-10-27: Harvest reports blocks as outcomes and does not escalate — the provisional pick was: yes,
  logged-out public data only, behind counsel's read in P3 (S1, S8)
- [ ] P5 Telegram read route → not pursued 2026-10-27: Harvest reports blocks as outcomes and does not escalate — the provisional pick was: `t.me/s` web preview first; two UZ-SIM user accounts for groups,
  comments and deletion checks; a human approves each join (T1-P2, T1-P3, T1-P6)
- [x] P6 WhatsApp v1 → confirmed 2026-10-27: an intake number plus channel page snapshots; no unofficial sidecar
  (T1-P7)
- [x] P7 Events' first web sources → confirmed 2026-10-27: mstar.uz and voyage.uz (JSON-LD `Event`); Afisha once it
  grants permission; iticket deferred to the render tier (W1, W2, T4-12)
- [x] P8 credential owner for Meta, X, Google and the Telegram SIMs → confirmed 2026-10-27: the parent company of
  `ven-t-012` (S2, T1-P3)
- [x] P9 discovery by search, as Ocharo's scans do today → confirmed 2026-10-27: a `search` adapter family after the
  first slice (T4-3)

The tracks' own Points (T1-P1…14, S1–S12, W1–W18, T4-1…13) hold the children.

### C · Model, extraction and pipelines — from wave 2

- [x] P10 pipeline and subscription split: the pipeline `(container, source, scope_key)` is the shared harvesting
  unit; the subscription is per consumer with its own delivery, AI switch and budget share; the effective config
  derives from the subscriptions → confirmed 2026-10-27: yes (T7)
- [x] P11 post layers: `source` → `capture` → `link_readings` → `post_links` → `posts`, each in a `container`; the
  canonical post is derived from its links' readings with provenance per field, never patched in place; captures
  written only on content change → confirmed 2026-10-27: yes (T5)
- [x] P12 dedup: a deterministic ladder — exact keys, normalized-text hash, `pg_trgm` on transliterated text;
  merges undoable with a `non_matches` veto; embeddings review-only and never over `ai_allowed = false` text →
  confirmed 2026-10-27: yes (T5)
- [x] P13 deletion: `suspect` before `gone`; only a completed run over a complete enumeration may infer it; a post
  is gone when all its verifiable links are; unverifiable sources abstain → confirmed 2026-10-27: yes (T5, T7)
- [x] P14 extraction: a deterministic → rules → embeddings → small model → large model cascade that always yields
  `wow2.post.v1`; a consumer schema is a declared mapping first and the model fills only gaps → confirmed 2026-10-27:
  yes (T6)
- [x] P15 AI gates: pipeline `off` · `gaps` · `full`, source `ai_allowed` `yes` · `no` · `unreviewed`, host
  `ai-input` signal, budget cap; the build runs end to end without AI → confirmed 2026-10-27: yes; Telegram defaults wait
  on P3 (T6)
- [x] P16 delivery: one durable event log per subscription feeds webhooks, pull cursors, replay and dead letters;
  the be sdk's inline `WebhookPublisher` is not at-least-once, so a durable dispatcher joins the SDK, shared with
  Identity → confirmed 2026-10-27: yes (T7, T8)
- [x] P17 text search: PostgreSQL has no Uzbek configuration; `simple` with prefix matching over Latin-transliterated
  text, a UTF-8 database locale and a boot self-test → confirmed 2026-10-27: yes (T6, T5)
- [x] P18 retention travels downstream: deliveries carry `retention_class` and `delete_by`, and `post.purged`
  reaches consumers; derived items, tags and embeddings die with their capture → confirmed 2026-10-27: yes (T5, T6, T2)
- [x] P19 contact keys: an HMAC with a vault-held pepper, not a plain hash of nine digits → superseded 2026-10-27:
  contact numbers are stored as plain text (developer)
  (T5)

The tracks' own Points (T5-1…22, T6-1…17, T7-P1…P20) hold the children.

### D · Steps and capabilities — from wave 4

- [ ] P20 the capability framework: pipelines as steps, integrations as brokers, and capabilities each step may
  require — sign-in, captcha avoidance, an IP server, rendering — with the cut between Social and Harvest →
  not pursued 2026-10-27: Harvest reports blocks as outcomes and does not escalate — the provisional pick was: pipelines are declared step plans; each step states a floor, a ladder and a ceiling of
  capabilities; the resolver picks the cheapest working rung per `(host, lane)` at claim, reserves budget and leases
  egress and sessions (T9-1)
  - cut, revised 2026-10-27: Social holds platform clients and account pools, the Telegram MTProto pool included;
    egress goes to a core module `Http/Egress`; named-source brokers go to a private repo, one package per source;
    Harvest holds the engine and the generic family readers (T9-2, T9-24, T9-19, T9-26)
  - timing: slice 1 builds direct egress, cookie jars, challenge detection and pacing inline behind Social-shaped
    contracts, which move to Social at the next +0.1; Afisha joins slice 1 (T9-3, T9-23)
  - posture: 24 earlier picks change; the posture fields stay as switches with permissive defaults (T9-4)
  - forks for the developer: honour official-API terms only (T9-5), robots.txt obeyed by default (T9-17); T9-19
    answered 2026-10-27 — a private adapters repo

The track's own Points (T9-1…23) hold the children.
