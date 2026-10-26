# Harvest — full analysis before the build

*Last updated: 2026-10-26*

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

---

## Tracks

| # | Track | File | Wave | State |
|---|---|---|---|---|
| T1 | Messaging sources: Telegram and WhatsApp | [t1-messaging-sources.md](t1-messaging-sources.md) | 1 | ✅ |
| T2 | Social platforms: Instagram, Facebook, X, Reddit, TikTok, YouTube, Threads, LinkedIn | [t2-social-sources.md](t2-social-sources.md) | 1 | ✅ |
| T3 | Web sources: pages, browser, whole-site, provider APIs, feeds, link intake; build vs wrap | [t3-web-sources.md](t3-web-sources.md) | 1 | ✅ |
| T4 | Consumer needs (Ocharo, Haven, others) and the social-integration inventory | [t4-consumers-and-social.md](t4-consumers-and-social.md) | 1 | ✅ |
| T5 | Post model: captures, sources, canonical posts, dedup, deletion checks, containers | [t5-post-model.md](t5-post-model.md) | 2 | ✅ |
| T6 | Extraction and classification: per-source fields, tags, AI tiers, cost | [t6-extraction.md](t6-extraction.md) | 2 | 🔄 |
| T7 | Pipelines, schedules, subscriptions, workers, delivery, roles | [t7-pipelines-delivery.md](t7-pipelines-delivery.md) | 2 | ✅ |
| T8 | Placement: social domain vs Harvest domain, ListingShelf reuse (H1), forms | t8-placement.md | 3 | ⬜ |

- wave 1 runs 2026-10-26; wave 2 reads wave 1; wave 3 reads both.

---

## Points

The decision queue: parents before children, blocking first. Each line: the question → the pick, and the track
holding the evidence. Tick a line when the developer answers; the answer moves into the spec.

### A · Placement — blocks the build

- [ ] P1 social media and Harvest: one social repo holding Harvest, or a social connectors domain beside a Harvest
  domain → provisional pick: two domains, Harvest's social adapters calling the connectors (T4, T8)
- [ ] P2 (H1) Harvest's repo: ListingShelf widened and renamed, or a new repo seeded from its core (T8)

### B · Source terms — blocks the source picks

- [ ] P3 posture: the spec says "must honour each source's terms", and three terms collide with the plan →
  provisional pick: keep the rule; every route carries a posture tag (official · licensed provider · own fetch ·
  consented intake) and every source `permission` and `ai_allowed` fields; counsel reads the Telegram and Meta
  terms before Route B or Telegram AI (T1-P1, S1, W1, W5)
  - Telegram API Terms §1.5: no Telegram data for AI "development, enhancement or deployment" (read 2026-10-26)
  - Meta Automated Data Collection Terms (2024): no automated collection without written permission
  - Afisha terms: prior written permission to copy or use material
- [ ] P4 licensed providers (Apify) for Instagram, Facebook and TikTok public pages → provisional pick: yes,
  logged-out public data only, behind counsel's read in P3 (S1, S8)
- [ ] P5 Telegram read route → provisional pick: `t.me/s` web preview first; two UZ-SIM user accounts for groups,
  comments and deletion checks; a human approves each join (T1-P2, T1-P3, T1-P6)
- [ ] P6 WhatsApp v1 → provisional pick: an intake number plus channel page snapshots; no unofficial sidecar
  (T1-P7)
- [ ] P7 Events' first web sources → provisional pick: mstar.uz and voyage.uz (JSON-LD `Event`); Afisha once it
  grants permission; iticket deferred to the render tier (W1, W2, T4-12)
- [ ] P8 credential owner for Meta, X, Google and the Telegram SIMs → provisional pick: the parent company of
  `ven-t-012` (S2, T1-P3)
- [ ] P9 discovery by search, as Ocharo's scans do today → provisional pick: a `search` adapter family after the
  first slice (T4-3)

The tracks' own Points (T1-P1…14, S1–S12, W1–W18, T4-1…13) hold the children.

### C · Model, extraction and pipelines — from wave 2

- [ ] P10 pipeline and subscription split: the pipeline `(container, source, scope_key)` is the shared harvesting
  unit; the subscription is per consumer with its own delivery, AI switch and budget share; the effective config
  derives from the subscriptions → provisional pick: yes (T7)
- [ ] P11 post layers: `source` → `capture` → `link_readings` → `post_links` → `posts`, each in a `container`; the
  canonical post is derived from its links' readings with provenance per field, never patched in place; captures
  written only on content change → provisional pick: yes (T5)
- [ ] P12 dedup: a deterministic ladder — exact keys, normalized-text hash, `pg_trgm` on transliterated text;
  merges undoable with a `non_matches` veto; embeddings review-only and never over `ai_allowed = false` text →
  provisional pick: yes (T5)
- [ ] P13 deletion: `suspect` before `gone`; only a completed run over a complete enumeration may infer it; a post
  is gone when all its verifiable links are; unverifiable sources abstain → provisional pick: yes (T5, T7)
- [ ] P14 extraction: a deterministic → rules → embeddings → small model → large model cascade that always yields
  `wow2.post.v1`; a consumer schema is a declared mapping first and the model fills only gaps → provisional pick:
  yes (T6)
- [ ] P15 AI gates: pipeline `off` · `gaps` · `full`, source `ai_allowed` `yes` · `no` · `unreviewed`, host
  `ai-input` signal, budget cap; the build runs end to end without AI → provisional pick: yes; Telegram defaults wait
  on P3 (T6)
- [ ] P16 delivery: one durable event log per subscription feeds webhooks, pull cursors, replay and dead letters;
  the be sdk's inline `WebhookPublisher` is not at-least-once, so a durable dispatcher joins the SDK, shared with
  Identity → provisional pick: yes (T7, T8)
- [ ] P17 text search: PostgreSQL has no Uzbek configuration; `simple` with prefix matching over Latin-transliterated
  text, a UTF-8 database locale and a boot self-test → provisional pick: yes (T6, T5)
- [ ] P18 retention travels downstream: deliveries carry `retention_class` and `delete_by`, and `post.purged`
  reaches consumers; derived items, tags and embeddings die with their capture → provisional pick: yes (T5, T6, T2)
- [ ] P19 contact keys: an HMAC with a vault-held pepper, not a plain hash of nine digits → provisional pick: yes
  (T5)

The tracks' own Points (T5-1…22, T6-1…17, T7-P1…P20) hold the children.
