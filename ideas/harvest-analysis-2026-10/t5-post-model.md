# T5 — Post model

*Last updated: 2026-10-26*

> One `harvest` PostgreSQL schema of 28 tables stores five layers: sources, immutable captures, one reading per link
> (what extraction made of the link's latest capture), links (one post as seen at one source URL or id, with its own
> `live` · `suspect` · `gone` · `relisted` state) and the canonical post. The canonical post is derived from its
> links' readings by field precedence and never patched in place, so a merge, an unmerge, a purge and a revoked AI
> permission all recompute it deterministically. Dedup is a deterministic ladder whose merges are `move_link` calls,
> so every merge undoes; a post is gone only when every verifiable link is. Containers isolate consumers, and a private
> post keeps its id when its content later comes from the pool. Policy stays configuration (`ai_allowed`,
> `permission`, `posture`, retention class sit on the source), so open Points change defaults, never tables.

- `(U)` = unverified. Track refs T1–T4 are the wave 1 files in this folder; S, W and T4-n are their Points.
- Aliases (from the workspace root `W`): `lb` = `workbench/maxs-projects/ventures/saas/ventures.listing-shelf/engineering/codebase/listing-shelf.backend-services`;
  `hb` = `workbench/maxs-projects/ventures/saas/10x-ven-haven/engineering/codebase/haven.backend-services`.
- Facts come from reads on 2026-10-26 of `lb` `Persistence/Migrations/001…007`, `ListingSnapshotRepository.cs`,
  `RunExecutionService.cs`; `hb` `Migrations/002-external-listings`, `008-listing-phones`, `ExternalListingRepository.cs`;
  the Harvest and Events specs; T1–T4. PostgreSQL facts cite § Sources. Nothing was built or run; volumes are
  assumptions, stated as such.
- Scope: storage model only. T6 owns extraction and field content, T7 pipelines, schedules, workers and delivery,
  T8 placement; cross-track questions sit under Points with the track tag.

---

## Verdict

- **Five layers, one direction:** `sources` → `captures` → `link_readings` → `post_links` → `posts`. Captures are
  facts, readings are the latest interpretation, the post is a pure function of its links' readings.
- **Link, not observation:** the table of "one post at one source URL" is `post_links`. Events already uses
  `observation` for a delivered item awaiting a match; Harvest avoids the word.
- **Capture on change:** a capture row exists only when the normalized content hash changed. An unchanged poll
  updates one narrow hot row (`link_schedule`). ListingShelf writes a capture per run and listing, changed or not.
- **Merge is `move_link`:** dedup re-points links between posts and recomputes. Nothing is destroyed, so undo is a
  logged inverse move; a rejected pair becomes a `non_match` that nothing re-suggests or auto-merges.
- **Deterministic first, AI last:** exact keys, normalized-text hash and `pg_trgm` on Latin-transliterated text carry
  v1. Embeddings (pgvector) are an optional tier, off by default, and never read text of a source with
  `ai_allowed = false` (Telegram's AI clause covers them under the conservative reading, T1-P1).
- **Gone is a rollup:** link states move on authoritative negatives from an available source only; a post is gone
  when all its verifiable, non-retired links are gone. Sources that cannot be checked abstain.
- **Containers:** the pool and each consumer's private container share the tables, keyed by `container_id` with
  composite foreign keys. The one cross-container edge is `posts.alias_of` (private → pool). Private never merges
  into the pool.
- **Retention is a role:** captures are immutable by grants (the app role cannot update or delete them); a purge role
  scrubs by `expires_at` and by compliance events, and purge propagates through provenance to the post.
- **Size:** about 7 GB a year in PostgreSQL and about 190 GB in File Storage at the Haven-plus-Ocharo design point
  (§ 9, assumptions); captures and metrics are partitioned monthly from the first migration because retrofitting is
  a rewrite.

---

## 1 · Prior art read

### ListingShelf (SQLite)

| Part | What the code does | T5 decision |
|---|---|---|
| capture | `listing_snapshots`: one row per `(RunId, ProviderId, ExternalId)` whether or not anything changed; `ContentHash` = SHA-256 of the normalized `Data` JSON; raw HTML Brotli-compressed in the row (`RawHtmlCompressed`) | keep the hash of normalized content; write a capture only on change; bytes go to File Storage |
| change tag | computed at query time with window functions over all snapshots (`GetRunListingsAsync`: `New` · `Changed` · `Unchanged` · `Gone`) | store state and `last_changed_at` on write; tags become events |
| absence | `listing_absences`: one row per run and listing; any "provider reports gone" is final; no `suspect`, no threshold; OLX removal itself unconfirmed (T4 § 5) | link state machine with `suspect`, confirmation and preconditions (§ 5) |
| relisting | implicit: `UnavailableSince` counts only absences after the last capture, so a new capture clears it | explicit `relisted` state and event |
| identity | `(ProviderId, ExternalId)`; membership `(PipelineId, ProviderId, ExternalId, SourceUrl)` in `discovered_listings` | `(source_id, external_key)` for a link; pipeline membership is T7's join |
| photos | `photos(Hash)` content-addressed, `snapshot_photos(SnapshotId, Position, SourceUrl, PhotoHash)`, 90-day prune of older captures' copies | `media_assets` + `link_media` + `post_media` (§ 2.7) |
| search | FTS5 over title, description, location, seller, attributes, external id; `unicode61 remove_diacritics 2` | `pg_trgm` + optional `to_tsvector('simple', …)` on `match_text` (T7 keyword reads) |
| view state | `listing_notes` (stars, notes) keyed `(ProviderId, ExternalId)`; stays in the view | view chooses per post or per link (T5-17) |
| limits | `pageLimit` 1–100, `itemLimit` 1–2,000; one run at a time | T7 |

### Haven (`external_listings`, PostgreSQL)

| Part | What the code does | T5 decision |
|---|---|---|
| upsert | `ON CONFLICT (provider, external_id) DO UPDATE … WHERE external_listings.captured_at <= EXCLUDED.captured_at` | keep the stale-write guard, per field (§ 4) |
| improvement | `price = COALESCE(NULLIF(EXCLUDED.price,''), external_listings.price)` and the same for description, author, region: blank never overwrites | keep as a rule: a null reading is no claim; the last value stays, flagged stale |
| churn | rewrites every row each 15-minute run even when nothing changed | hash-compare skip; hot columns split off (`link_schedule`) |
| insert detection | `RETURNING (xmax = 0)` | usable for upserts of `post_links` (U: relies on an implementation detail) |
| traceability | `collector_snapshot_id` + `snapshot jsonb` (the normalized snapshot as received) | `link_readings.capture_id` + `field_prov` |
| phones | `listing_phones(listing_id, phone_key varchar(9))`, key = last nine digits, trigger-synced; ≥ 3 listings flags a realtor (T4) | `contact_keys` with a keyed hash instead of the raw nine digits (§ 3.5, § 7) |
| status | `external_status` (`active` / `deleted`) + `external_status_checked_at`; nothing writes `deleted` (T4) | link and post state with a scheduler (§ 5) |
| dedup | none across sources | § 3 |

---

## 2 · Entities and tables

### 2.1 Rules for every table

- Schema `harvest`; PostgreSQL only, so no table prefix (Identity keeps `identity_` for SQLite).
- Ids are UUID v7 made in code; PostgreSQL 18 has a built-in `uuidv7()` as fallback [pg-uuid]. Time columns are `timestamptz`.
- Migrations are SQL sets, `Apply.sql` + `Rollback.sql`, as in ListingShelf and Haven; baseline `001`.
- **Tenancy key:** every table except `containers` and the global config tables (`retention_policies`,
  `check_policies`, `host_policies`) carries `container_id uuid NOT NULL`. Parents expose `UNIQUE (container_id, id)`; children
  reference `(container_id, parent_id)`, so a link cannot point at a post in another container.
- No foreign key points into a partitioned table: a primary key there must contain the partition key [pg-part].
  `capture_id` references are paired with `captured_at` and checked in code.
- The app database role has `INSERT` and `SELECT` on `captures`; a separate `harvest_purge` role holds `DELETE` and
  `UPDATE (scrubbed_at, body_ref, expires_at)`. Immutability is a grant, not a trigger.
- Policy is configuration under `Harvest:Dedup`, `Harvest:Retention`, `Harvest:Checks`; policy tables hold seeded rows.

### 2.2 The five layers

| Layer | Table | Mutable | Holds |
|---|---|---|---|
| source | `sources` | config | a channel, site, account or feed, with posture, `permission`, `ai_allowed`, retention class |
| capture | `captures` | no, inside its window | bytes as fetched (File Storage), content hash, legal metadata |
| reading | `link_readings` | replaced on change | the latest extraction of one link: text, base fields, tier per field |
| link | `post_links` + `link_schedule` | state and schedule only | one post at one source URL or id, with state |
| post | `posts` + `post_texts` | derived | the improved record with provenance per field |

### 2.3 Inventory (28 tables)

| Group | Table | Purpose | Partition |
|---|---|---|---|
| containers | `containers` | the pool and each consumer's private container | no |
| | `publishers` | one brand across a site, a Telegram channel and an Instagram account | no |
| sources | `sources` | where posts come from | no |
| | `source_scopes` | host and path patterns a `coverage = whole` source owns (link routing, § 6) | no |
| | `source_aliases` | handles a source used over time (Telegram renames, T1) | no |
| | `host_policies` | per registrable host: `permission`, robots state, content signals | no |
| | `retention_policies` | retention classes (§ 7) | no |
| | `check_policies` | deletion-check policies (§ 5) | no |
| | `intake_consents` | consent record per intake submitter (T1-P9) | no |
| captures | `enumerations` | one pass over a sitemap, feed or channel list: complete or window, count, guard | no |
| | `captures` | immutable, dated snapshot of one link | monthly on `captured_at` |
| links | `post_links` | one post as seen at one source URL or id | no |
| | `link_schedule` | hot columns: next check, last seen, counters | no |
| | `link_readings` | latest extraction per link | no |
| | `link_parts` | album members, thread parts | no |
| | `link_events` | link state history, append-only | no |
| | `link_check_log` | every check with its evidence, 30 days | weekly (U) |
| | `link_metrics` | views, forwards, reactions series | monthly on `observed_at` |
| posts | `posts` | the canonical post | no |
| | `post_texts` | text per locale, normalized match text | no |
| | `post_edits` | edit history of resolved fields | no |
| | `contact_keys` | keyed hashes of phones and handles | no |
| | `post_media` | the post's gallery | no |
| media | `media_assets` | one stored file per distinct image or file per container | no |
| | `link_media` | media a link referenced, stored or link-only | no |
| dedup | `merge_candidates` | pairs waiting for review | no |
| | `merge_log` | every merge, auto or manual, with the links moved | no |
| | `non_matches` | pairs that must never merge | no |

- T7 adds pipelines, runs, deliveries and subscriptions; T3 and T7 own `source_routes` (ordered routes with health).
- At the design point only `captures` (~1.1M rows a year) and `link_metrics` (~3.7M) pass 1M rows a year (§ 9).

### 2.4 Core columns

**`containers`**

| Column | Type | Rule |
|---|---|---|
| `id` | uuid v7 | |
| `kind` | `pool` · `private` | one `pool` per instance (partial unique index) |
| `consumer_id` | uuid null | null for the pool; T7 owns consumers |
| `external_ref` | text null | the consumer's name for it, such as the Events catalog slug `ocharo-fashion` (T4-9) |
| `residency` | text null | where its data may live; unset until the personal-data read (T5-12) |
| `embeddings_enabled` | bool | default `false` |
| `state`, `created_at` | | |

**`sources`**

| Column | Type | Rule |
|---|---|---|
| `id`, `container_id` | uuid | |
| `family` | text | `page` · `structured` · `site` · `render` · `api` · `feed` · `link` · `telegram` · `whatsapp` · `instagram` · `facebook` · `youtube` · `threads` · `x` · `intake` · `manual` (T1–T3 families) |
| `handle` | text | canonical identity: host, or `tg:{username}`; `UNIQUE (container_id, family, handle)` |
| `external_ref` | text null | numeric platform id (Telegram peer id); wins over the handle when they disagree |
| `publisher_id` | uuid null | brand linking (§ 3.7) |
| `coverage` | enum | `whole` (every post: sitemap, full channel) · `filtered` (only what pipelines discover) · `single` (submitted URL) |
| `completeness` | enum | `complete` (an enumeration lists every live post) · `window` (feed, newest page, search results) · `none` |
| `posture` | enum | `official` · `licensed_provider` · `own_fetch` · `consented_intake` (P3); required |
| `permission` | enum | `open` · `restricted` · `granted` · `denied` (W1); stricter of source and host policy wins |
| `ai_allowed` | bool | gates LLM extraction and embeddings (§ 2.5) |
| `consent_basis` | enum | `owner` · `submitter` · `none` (T1) |
| `authority` | smallint | 0–100: how close the source is to the thing (organizer 80, aggregator 50, repost 20); feeds precedence (§ 4) |
| `retention_class` | text | → `retention_policies.key` |
| `check_policy_id` | uuid | → `check_policies` |
| `state`, `state_since` | | `active` · `paused` · `unavailable` · `preview_unavailable` · `quota_exhausted` · `retired` (T1 § 5.3) |
| `created_by`, `created_at` | | actor from the service key (T4-10) |

**`captures`** (monthly partitions; primary key `(captured_at, id)`)

| Column | Type | Rule |
|---|---|---|
| `id` | uuid v7 | |
| `container_id`, `source_id`, `link_id` | uuid | `link_id` soft-checked |
| `run_id` | uuid | T7 |
| `captured_at` | timestamptz | partition key |
| `request_url`, `final_url` | text | after redirects |
| `outcome` | enum | `ok` for a stored capture; refusals and blocks are not captures (`link_events`, `link_check_log`) |
| `http_status` | smallint null | |
| `route`, `posture`, `provider`, `logged_out`, `terms_version` | | per-capture legal metadata (T2 § 6) |
| `raw_hash` | bytea(32) | SHA-256 of the body as received: "was the fetch identical" (T3) |
| `content_hash` | bytea(32) | SHA-256 of the normalized content projection: "did the post change" |
| `body_ref` | uuid null | File Storage file, Brotli; null after a scrub |
| `body_bytes` | int | |
| `retention_class`, `expires_at` | | copied from the source at capture time |
| `scrubbed_at`, `scrub_reason` | | purge role only |
| `warnings` | jsonb | |

- The content projection excludes metrics, ads, session tokens and CDN URL tokens (Telegram video `token`, T1); it
  includes text, structured nodes, media descriptors by stable URL and the `edited` marker.
- A capture exists only when `content_hash` differs from the link's latest, or when a pipeline asks for a heartbeat
  capture every N days (default off).

**`post_links`** (narrow, written on state or identity change)

| Column | Type | Rule |
|---|---|---|
| `id`, `container_id` | uuid | |
| `source_id`, `post_id` | uuid | composite FK `(container_id, post_id)` |
| `external_key` | text | web: normalized URL; Telegram: `{peer_id or username}/{message_id}` (album: lowest id); Instagram: shortcode; YouTube: video id; X: post id; OLX: ad id; manual: uuid. `UNIQUE (source_id, external_key)` |
| `url`, `url_key` | text, bytea(16) | canonical URL (T3 § 2.7 normalization) and its hash |
| `origin_key` | text null | forward origin `tg:{peer}/{id}`, declared `rel=canonical`, `sameAs`: exact-match keys (§ 3.2) |
| `role` | enum | `primary` · `alternate` (locale) · `copy` (repost, forward) · `part` · `reply` |
| `parent_link_id` | uuid null | thread root for `part` and `reply` |
| `locale` | text null | BCP 47, with script for `uz-Latn` · `uz-Cyrl` |
| `state`, `state_since` | enum, timestamptz | `live` · `suspect` · `gone` · `relisted` |
| `retired_at`, `retired_reason` | | `moved` · `merged_duplicate` · `covered_by_pool` · `source_removed`; retired links leave every rollup |
| `check_capability` | enum | `full` · `weak` · `none` (§ 5.3); `none` abstains from the post rollup |
| `consent_id` | uuid null | → `intake_consents` |
| `first_seen_at`, `last_changed_at`, `gone_at`, `relist_count` | | |
| `latest_capture_id`, `latest_captured_at`, `latest_content_hash` | | soft reference |

**`link_schedule`** (hot: `fillfactor` 70; updated on every poll and check)

| Column | Type | Rule |
|---|---|---|
| `link_id` | uuid PK | |
| `container_id` | uuid | |
| `next_check_at`, `last_checked_at`, `last_seen_at`, `last_enumerated_at` | timestamptz | |
| `check_level` | smallint | raised by a consumer watch (T7), never lowered below the policy |
| `check_count`, `fail_count`, `consecutive_missing` | int | |
| `last_outcome` | text | `ok` · `absent` · `gone_signal` · `blocked` · `rate_limited` · `error` … |
| `due` | bool | true while `state` is checkable; the partial index `(next_check_at) WHERE due` feeds the scheduler |

- Splitting this off keeps wide rows still: every poll rewrites 80 bytes, not a link row, and `next_check_at` being
  indexed makes those updates non-HOT, so the table needs its own `autovacuum` settings (§ 9).

**`link_readings`** (one row per link; T6 writes `fields` and `tier_map`)

| Column | Type | Rule |
|---|---|---|
| `link_id` | uuid PK | |
| `container_id`, `capture_id`, `captured_at` | | the capture this reading came from |
| `extractor_version` | text | |
| `locale`, `title`, `body` | text | the link's own text, before resolution |
| `fields` | jsonb | T6's base fields (dates with precision, price, location text, tags, author…) |
| `tier_map` | jsonb | per field: `manual` · `api` · `jsonld` · `microdata` · `selector` · `opengraph` · `regex` · `llm` |
| `ai` | jsonb null | `{model, prompt_version, confidence}` when any field came from an LLM |
| `contacts` | jsonb null | raw phones, emails, handles; excluded from default selects and from pool reads (§ 7.3) |
| `updated_at` | timestamptz | |

**`posts`**

| Column | Type | Rule |
|---|---|---|
| `id`, `container_id` | uuid | `UNIQUE (container_id, id)` |
| `kind` | text | from T6; dedup never merges across kinds |
| `state`, `state_since` | enum, timestamptz | `live` · `suspect` · `gone` (rollup, § 5.4) |
| `verifiable` | bool | false when no link can be checked |
| `relisted_at`, `relist_count` | | an event plus a stamp; the state returns to `live` |
| `alias_of` | uuid null | pool post whose content this private post shows (§ 6.3) |
| `merged_into` | uuid null | set on a loser; reads redirect |
| `purged_at` | timestamptz null | shell kept for referential integrity |
| `primary_locale`, `published_at` | | earliest source publish time |
| `base` | jsonb | resolved base fields (T6) |
| `field_prov` | jsonb | per field: `{link, capture, tier, authority, at, stale?}` (§ 4.2) |
| `dedup_state` | enum | `pending` · `settled` (T7 holds first delivery until `settled` or the settle timeout) |
| `revision`, `first_seen_at`, `last_changed_at` | | |

**`post_texts`** (PK `(post_id, locale)`)

| Column | Type | Rule |
|---|---|---|
| `title`, `body` | text | resolved per locale |
| `match_text` | text | normalized for matching (§ 3.3), capped at 1,000 characters |
| `text_norm_hash` | bytea(16) | hash of the full normalized text |
| `num_sig` | bytea(16) | hash of the sorted digit tokens: the merge guard (§ 3.6) |
| `link_id`, `updated_at` | | the winning link |

### 2.5 Policy fields and what each default waits on

| Field | Lives on | Default | Waits on |
|---|---|---|---|
| `ai_allowed` | source | `false` for `telegram`, `whatsapp`, and wherever `consent_basis = none`; `true` elsewhere unless the host sends `ai-input=no` (W5) | T1-P1 |
| `permission` | source, `host_policies` | `open` where robots allow; `restricted` for Afisha | W1, P3 |
| `posture` | source, copied onto each capture | none: a source cannot be created without one | P3 |
| licensed-provider route | `source_routes.enabled` | `false` until a developer sign-off | P4, S1 |
| `retention_class` | source | by family: `youtube`, `x`, `meta` forced on their official routes; else `standard` | S4, T5-9 |
| `embeddings_enabled` | container | `false`; text of a source with `ai_allowed = false` is never embedded | T1-P1, T6 |
| `residency` | container | unset | T5-12 |

- Every default is a value in a row, so the answer to a Point is an `UPDATE` and a seed change, not a migration.

### 2.6 Index set

| Table | Indexes | Why |
|---|---|---|
| `sources` | `UNIQUE (container_id, family, handle)` | identity |
| `source_scopes` | `(host, path_prefix text_pattern_ops)` | link routing lookup |
| `captures` | PK `(captured_at, id)`; `(link_id, captured_at DESC)`; `(expires_at) WHERE scrubbed_at IS NULL` | history; purge job |
| `post_links` | `UNIQUE (source_id, external_key)`; `(container_id, post_id)`; `(container_id, url_key)`; `(container_id, origin_key) WHERE origin_key IS NOT NULL` | upsert; post fan-in; URL and origin exact match |
| `link_schedule` | PK; `(next_check_at) WHERE due` | scheduler claim with `FOR UPDATE SKIP LOCKED` |
| `link_events` | `(link_id, at)`; `(container_id, at)` | history; T7 event feed |
| `link_metrics` | PK `(observed_at, link_id)`; `(link_id, observed_at DESC)` | series reads |
| `posts` | PK; `UNIQUE (container_id, id)`; `(container_id, kind, first_seen_at DESC)`; `(container_id, state, state_since)`; partial on `alias_of`, `merged_into` | lists; rollups; redirects |
| `post_texts` | PK; GIN `match_text gin_trgm_ops`; `(container_id, text_norm_hash)` | near-dup; exact text |
| `contact_keys` | PK `(link_id, kind, key)`; `(container_id, kind, key)` | contact match |
| `media_assets` | `UNIQUE (container_id, sha256)`; optional HNSW on `phash` with `bit_hamming_ops` | file dedup; image match |
| `merge_candidates` | `(container_id, status, score DESC)` | review queue |
| `non_matches` | PK `(post_lo, post_hi)` with `CHECK (post_lo < post_hi)` | veto lookup |

- Hot-write budget: at most six indexes on `posts` (two are tiny partials), four on `post_links`; the trigram GIN is the heaviest write
  cost, so `match_text` is rewritten only when the resolved text changes.
- Keyword subscriptions (T7) add one `to_tsvector('simple', match_text)` GIN; PostgreSQL ships no Uzbek dictionary
  (U), and transliterated text makes `simple` consistent across scripts.

### 2.7 Media

| Table | Key | Rule |
|---|---|---|
| `media_assets` | `UNIQUE (container_id, sha256)` | `file_id` in File Storage, `content_type`, `bytes`, `width`, `height`, `phash bit(64)`, `generic bool`, `state` `stored` · `purged`; File Storage dedups per organization and never across, so the container is the organization |
| `link_media` | PK `(link_id, position)` | `role` `image` · `video` · `doc` · `thumb`, `source_url`, `url_state` `ok` · `dead` · `unchecked`, `asset_id` null for link-only, `capture_id` |
| `post_media` | PK `(post_id, position)` | the resolved gallery: best resolution per perceptual-hash cluster, ordered by source authority |

- Store thumbnails and the first image; link the rest; never download YouTube video (S9). Telegram `file_reference`
  and preview video tokens expire and WhatsApp media URLs live five minutes (T1), so storing happens at capture time.
- A store-vs-link decision is a pipeline flag; `link_media.asset_id IS NULL` is a valid permanent state.

### 2.8 Metrics and link history

**`link_metrics`** (monthly partitions; PK `(observed_at, link_id)`)

| Column | Type | Rule |
|---|---|---|
| `link_id`, `container_id`, `observed_at` | | |
| `views`, `likes`, `comments`, `shares`, `forwards` | bigint null | the common counters; null = not offered by the route (Bot API has none, T1) |
| `reactions` | jsonb null | per-emoji counts (Telegram preview) |
| `extra` | jsonb null | route-specific (`impressions`, `bookmarks` on X) |

- Outside the capture hash (T1-P10): a counter change never makes a capture or a `changed` event.
- Written only when a counter moved or the series is due: every poll for the first 24 hours, then at most every 6
  hours to day 7, then one row a day; `youtube` rows expire in 30 days. The latest values also sit in
  `link_readings.fields.metrics` for cheap lists.
- Never summed into the post: the same audience seen on two platforms is not additive; reads sum or list per link.

**`link_events`** (append-only): `id`, `container_id`, `link_id`, `at`, `from_state`, `to_state`, `reason`
(`direct_410` · `direct_404` · `named_redirect` · `soft_404` · `node_vanished` · `absent_from_enumeration` ·
`embed_not_found` · `mtproto_empty` · `delete_update` · `provider_error_item` · `compliance_delete` · `api_missing` ·
`seen_again` · `manual`), `evidence jsonb` (check method, HTTP status, `capture_id`, enumeration id), `run_id`, `actor`.

---

## 3 · Dedup

### 3.1 Three levels

| Level | Question | Owner | Mechanism |
|---|---|---|---|
| link identity | is this the same page or post I saw before? | Harvest | `(source_id, external_key)`; an upsert, not a merge |
| post | do two links show the same thing? | Harvest | the ladder below; `move_link` |
| entity | are two posts the same event, flat or supplier machine? | the consumer | Events' external id → key → fuzzy title, dates, city (`events-service-spec` § Harvest seam); Sourcing's "same machine" |

- T4 § 2 and § 3: Harvest dedups the same page across crawls, locale twins and the same offer under several URLs; the
  consumer dedups many posts into one entity. Harvest never merges two events that differ in date (§ 3.6).

### 3.2 The ladder

| # | Tier | Evidence | Cost | Decision |
|---|---|---|---|---|
| 0 | link identity | `(source_id, external_key)`; platform ids; normalized URL | one unique index | upsert |
| 1 | exact cross-link keys | Telegram forward origin `(chat, message_id)`; declared `rel=canonical`, JSON-LD `url` / `@id`, `og:url`; `hreflang` alternates; path-locale swap (`/ru/x` ↔ `/uz/x`) | indexed equality on `origin_key` and `url_key` | auto-merge, confidence 1.0 |
| 2 | normalized text | equal `text_norm_hash` (≥ 80 characters), no veto | indexed equality | auto when same publisher, or ≥ 1 corroboration; else review |
| 3 | near-duplicate text | `pg_trgm` similarity on `match_text` (§ 3.4) | GIN probe, bounded by kind and time window | auto only with corroboration and no veto; else review |
| 4 | media | perceptual hash within 6 bits (Desk's rule, T4 § 3), `generic = false` | `bit_count(a # b)` over candidates | corroboration, or review alone |
| 5 | contacts | keyed phone hash, author handle | indexed equality | corroboration, or review alone |
| 6 | embeddings (optional) | pgvector cosine on `halfvec` | embed per post, HNSW | review suggestion only, never auto |

- Corroboration = another independent tier agreeing: shared contact key, shared non-generic image, same author handle
  or publisher. A contact key on more than three posts counts half (Haven flags such numbers as realtors, T4 § 5).
- References are not identity: voyage.uz lists iticket offers by URL, and `sameAs` or ticket links create `related`
  hints that seed candidate searches, never merges.
- Tiers 0–2 run in the ingest transaction. Tiers 3–6 run in a job within minutes; the post is `dedup_state = pending`
  until then, and T7 holds the first delivery for a settle window (default 2 minutes) so most merges precede it.

### 3.3 Normalization for matching (`match_text`)

1. Unicode NFKC, lowercase, strip HTML, URLs, emoji, hashtags' `#`, markup.
2. Fold Uzbek apostrophe variants (`ʻ` `‘` `’` `` ` `` `'` after o, g) to one character.
3. Transliterate Cyrillic to a Latin key: Russian by a fixed table; Uzbek Cyrillic with `ў → o'`, `ғ → g'`, `қ → q`, `ҳ → h`.
4. Collapse whitespace and punctuation; keep digits; cap at 1,000 characters.

- Output is ASCII, so trigram behaviour no longer depends on the database locale: `pg_trgm` extracts trigrams from
  alphanumerics only, and old reports say a `C` locale skips non-ASCII letters (current behaviour (U)) [pg-trgm] [pg-trgm-c].
- Uzbek Latin and Cyrillic then match lexically (same language, two scripts); Russian ↔ Uzbek ↔ English never does.
- Suffix-heavy Uzbek (`kvartira`, `kvartirani`, `kvartirada`) breaks word shingles; character trigrams tolerate it.

### 3.4 Near-duplicate methods compared

Reasoned, not measured. Columns are text classes in uz, ru and en, in both scripts.

| Method | verbatim | light edit | script variant | reworded | translation | short text (< 80) | Cost |
|---|---|---|---|---|---|---|---|
| exact hash of `match_text` | ✓ | ✗ | ✓ after step 3 | ✗ | ✗ | ✓, but templates collide | O(1), btree |
| simhash 64 on word 3-grams | ✓ | ✓ up to ~20% edits (U) | ✓ | ✗ | ✗ | ✗ unstable | one `bit(64)`; probes via four 16-bit band indexes (pigeonhole at distance ≤ 3) |
| minhash + LSH | ✓ | ✓ | ✓ | ~ at Jaccard ≥ 0.5 | ✗ | ✗ | ~512 B a post, GIN on bands |
| `pg_trgm` `%` on `match_text` | ✓ | ✓ | ✓ | ~ | ✗ | ✓ best on titles | no column; GIN ≈ text size or more (U); default threshold 0.3 [pg-trgm] |
| embeddings, pgvector | ✓ | ✓ | ✓ | ✓ | ✓ if the model covers `uz` (U) | ~ | 4 KB a post at 1,024 dims in `vector`, 2 KB in `halfvec`; HNSW up to 2,000 / 4,000 dims [pgvector]; embed cost per post |

- **v1 pick:** `pg_trgm` on `match_text`, with titles and the first 300 characters as probe text for long posts; the
  threshold is calibrated on labelled pairs, not the 0.3 default.
- simhash stays in reserve if trigram latency fails at scale; minhash adds nothing over trigram at this size.
- Embeddings are the only tier that could link translations, and the only one inside the AI clause. They run only
  when `embeddings_enabled` and the source's `ai_allowed` are both true, and only suggest.
- With pgvector installed, a 64-bit perceptual hash can use `bit(64)` with an HNSW `bit_hamming_ops` index [pgvector];
  without it, image match verifies candidates the other tiers found (pHash is a verifier, not a retriever).

### 3.5 Contact keys

- Key = `HMAC-SHA256(pepper, kind || ':' || normalized value)` truncated to 16 bytes; phone normalized to the last
  nine digits (Haven's rule). `contact_keys(link_id, kind, key)` holds no raw value.
- **A plain hash of nine digits is not anonymous:** the space is about 10⁹ values, so it falls to brute force in
  minutes (U, arithmetic). The pepper lives in Secrets Vault; rotating it re-keys the table.
- Raw values stay in `link_readings.contacts`, outside the default column set and outside pool reads (§ 7.3).
- Keys on more than three posts get `high_frequency = true` and weigh half in corroboration.

### 3.6 Merge guards (vetoes)

| Guard | Rule |
|---|---|
| kind | different `kind` never merges |
| numbers | `num_sig` token sets (price, floor, area, phone fragments) with Jaccard < 0.8 block a tier 2–3 merge |
| dates | events: `starts_at` differing beyond precision tolerance blocks, so *Fashion Week 2025* never absorbs *2026* |
| contacts | disjoint non-empty contact-key sets block a text-only match (one realtor's template text, two flats) |
| container | never across containers (§ 6) |
| `non_matches` | a rejected pair never auto-merges or re-queues |
| locale | a cross-locale match is review-only unless tier 1 declared it |

### 3.7 Brand linking

- `publishers` group sources of one brand: `afisha.uz` + `t.me/afishauz`, `uybor.uz` + `t.me/Uybor`, a site and the
  invite link that hides its public channel (Domtut, T1 § 1).
- Edge accepted automatically when the site links the channel from header or footer *and* names match; otherwise a
  review row. Resolving an invite to a public username is a heuristic by title and size (T1).
- A shared publisher lowers the bar: same text or trigram ≥ 0.7 within 30 days auto-merges; cross-publisher needs
  ≥ 0.85 plus corroboration.
- Telegram handles change and get reused: `external_ref` (numeric id) identifies, `source_aliases(handle, valid_from,
  valid_to)` keeps old handles and refuses a reused one for a different peer.

### 3.8 Auto-merge or review

| Evidence | Outcome |
|---|---|
| tier 1 exact key | auto |
| tier 2 equal text, same publisher | auto |
| tier 2 equal text + ≥ 1 corroboration, no veto | auto |
| tier 3 trigram ≥ 0.85 + ≥ 1 corroboration, no veto | auto |
| trigram 0.6–0.85, or a single weak tier (image only, contact only) | review (`merge_candidates`, score and evidence kept) |
| embeddings similarity, any score | review |
| any veto | no merge; `non_matches` row if a reviewer confirmed |

- Defaults are conservative and set per kind in `Harvest:Dedup:Profiles:{kind}`; 5% of auto-merges are sampled into
  review to measure precision. Thresholds stay provisional until calibrated on a labelled set (T5-3).
- Reviewers: Harvest operators for the pool; the consumer's reviewers for a private container.

### 3.9 Merge and undo

- `Merge(survivor, loser)` = in one transaction: `move_link` for each of the loser's links, `loser.merged_into =
  survivor`, `merge_log` row with the links moved and both revisions, then `ResolvePost` on the survivor.
- Ids stay resolvable: reads of the loser answer with a redirect, and T7 emits `post.merged {from, into}`.
- `Unmerge(merge_id)` = move exactly `links_moved` back, restore the loser's state, resolve both, insert a
  `non_matches` pair, emit `post.unmerged`. It needs no stored copy of the old canonical fields because they derive
  from the links.
- A link that has moved again since is skipped and listed as partial; after the undo window (default 90 days) the
  tool is `SplitLinks(post, link_ids)`, the same primitive without the log.
- Manual pins are readings from the editor's `manual` source (§ 4); they travel with the links they sit on.

---

## 4 · Improving a post

### 4.1 Precedence

A reading is a claim for each field it holds. The winner is the first by the sort key of the field's class.

| Field class | Examples | Sort key (first wins) |
|---|---|---|
| manual | any pinned field | a `manual` reading always wins |
| facts about the thing | dates, price, status, location, contacts | source `authority`, then tier, then newest `observed_at` |
| presentation text | title, body | tier, then completeness (not truncated), then `authority`, then newest |
| sets | tags, images, links | union, deduplicated, ordered by authority |
| precision-bearing | dates | higher precision wins unless a same-authority claim disagrees: then both are kept, `conflict = true`, review |

- Tier order: `manual` > `api` > `jsonld` · `microdata` > `selector` > `opengraph` > `regex` > `llm` (low confidence ranks lower).
- A null or blank reading is no claim (Haven's `COALESCE(NULLIF())` rule). When a field's last claim disappears the
  last value stays, flagged `stale`, until a purge or a manual edit clears it.
- Truncation guard: a reading whose text is a prefix of the current one and under 60% of its length does not replace it.
- Date traps from T3 are inputs, not rules here: Afisha's bucket date is a publish date, date-only events can arrive as
  midnight UTC, `eventStatus` changes are status not deletion. T6 types them; T5 only ranks claims.

### 4.2 Provenance per field

`posts.field_prov[field] = { link, capture, tier, authority, at, mode, stale? }`; `mode` is `auto` · `manual` · `ai`
with `ai` carrying model and prompt version through `link_readings.ai`.

- Provenance answers "why this value", drives purge propagation (§ 7.2) and lets a revoked `ai_allowed` strip every
  `mode = ai` field by recomputing without those claims.

### 4.3 What a later observation does

1. A fetch yields `content_hash`. Equal → `link_schedule` only. Different → store the capture, replace the link's
   `link_readings`, set `last_changed_at`.
2. `ResolvePost(post)` locks the post row, loads the readings of its non-retired participating links plus manual
   readings, and recomputes only the fields the new reading touched.
3. A reading older than the current winner's `at` from the same link, or arriving from a backfill, cannot displace
   it (Haven's `captured_at <=` guard, per field).
4. Each changed field appends a `post_edits` row; `revision` and `last_changed_at` rise only if a winner changed.
   A worse-ranked source editing its copy changes nothing visible.
5. T7 emits `post.changed {fields}` and, for a new link joining, `post.link_added`.

`post_edits`: `(id, container_id, post_id, at, field, old jsonb, new jsonb, cause, link_id, capture_id, actor,
revision)`; `cause` = `source_changed` · `better_source` · `manual` · `merge` · `unmerge` · `purge`.

- Two histories: the capture chain per link is the source's own history (what Telegram's `edited` marker or a price
  change looked like then); `post_edits` is the history of the resolved record.

---

## 5 · Link state and deletion checks

### 5.1 State machine

| From | Event | To | Rule |
|---|---|---|---|
| `live` | strong negative, confirmed `confirm_checks` times | `gone` | 410; 404 on a direct fetch; named not-found redirect (Domtut `/404`); `messageEmpty`; compliance `delete` |
| `live` | weak negative | `suspect` | absent from a *complete* enumeration; soft-404 marker; structured node vanished |
| `suspect` | direct fetch ok | `live` | |
| `suspect` | strong negative | `gone` | |
| `suspect` | still ambiguous after `suspect_resolve_within` | stays `suspect` | back-off; a human sees it; never auto-`gone` |
| `gone` | seen again (fetch ok or enumerated) | `relisted` | event with `gone_at` and gap |
| `relisted` | `relist_stable_checks` ok checks, or a content change | `live` | `relist_count++`; three relists in 30 days sets `flapping` |
| any | result is not an authoritative negative | unchanged | § 5.2 |

- Not a deletion, so no `gone`: event ended, cancelled, postponed (T3 § 2.3), feed window drop, album id gap, source
  `unavailable`, redirect without a rule (`moved`: the old link retires with reason `moved`, the new URL joins the post).
- Evidence for each transition is stored on `link_events.evidence`; routine results go to `link_check_log` (30 days).

### 5.2 Preconditions: what counts as an authoritative negative

| Rule | Reason |
|---|---|
| the source is `active` and its last availability check passed | an unavailable channel answers "not found" for every id (T1 § 5.3) |
| the check itself ran: not `blocked`, `challenge`, `waiting-room`, `rate-limited`, `render-required`, auth error, quota or network error | those are outcomes, never absence (spec: blocks are outcomes) |
| absence from an enumeration counts only if `sources.completeness = complete` and the pass was complete | an OLX search page or a feed window lists newest items, so absence there proves nothing |
| enumeration is complete only if every child was fetched and the count is within the guard of the last pass | a drop above ~30% marks the pass suspect (W15) |
| the same negative twice for MTProto / embed probes | T1 § 5.6 |

### 5.3 Method per source family

`check_capability`: `full` = a direct existence answer; `weak` = only enumeration or re-scrape; `none` = cannot tell.

| Family and route | Method | Strong signal | Weak signal | Default cadence (first band wins) | Capability |
|---|---|---|---|---|---|
| web page, structured | conditional GET of the URL | 410; 404; named redirect | soft-404 marker; node vanished | ≤ 14 days to event: daily; further: weekly; stop 7 days after end (T3) | full |
| whole site | sitemap enumeration + direct fetch | 410; 404 on direct fetch | absent from a complete enumeration (`suspect` after 1 run) | enumerate hourly, sweep weekly, verify daily (T3) | full |
| listing site (OLX, Domtut) | direct fetch of the detail page | `ListingUnavailable` (404/410, `/404`) | none; OLX removal shape unconfirmed, so `suspect` first (U) | age < 2 d: 6 h; < 14 d: daily; else weekly; daily for a consumer-watched post | full |
| Telegram, web preview `W` | `t.me/{ch}/{id}?embed=1&mode=tme` after `/s/{ch}` answers | "Post not found" twice | id gap in a listing: never | < 7 d: daily; < 90 d: weekly; then monthly | full |
| Telegram, MTProto `M` | `channels.getMessages(ids)` batch; `updateDeleteChannelMessages` push | `messageEmpty` twice with membership verified; a push is one | – | as `W`; push is immediate | full |
| Telegram, Bot API `B` (owner channel) | none: no delete updates | – | – | never | none |
| Telegram forward intake `F` | probe the public origin like `W` | as `W` | – | monthly; private origin: none | full or none |
| WhatsApp intake, channel snapshot | none (sender deletes unseen; page keeps ~4 updates) | – | – | never | none |
| RSS / Atom / ICS | none: a window drops old items; `STATUS:CANCELLED` is status | – | – | never | none |
| Instagram, official `A` | re-list the account's media and diff | absent from a fully paged re-list | – | weekly (U) | weak |
| Instagram / Facebook / TikTok, provider `B` | re-scrape the post URL | provider error item twice | – | weekly, newest 30 days only (billed, S5) | weak |
| X official | Batch Compliance with post ids | `delete` event; `protected` · `deactivated` · `suspended` also delete | `rehydrate` → re-fetch; `scrub_geo` → drop geo | daily, mandatory | full |
| YouTube | `videos.list` by id, 50 per unit | id absent from `items` | – | at most every 30 days, mandatory; user request within 7 days | full |
| Threads | `GET /{media-id}` | request fails (U) | – | weekly | weak |

- A post whose only links are `none` is `live` with `verifiable = false`; mixed posts roll up over the checkable links.
- A source `unavailable` pauses its links' checks. After 30 days a human decides (retire source, keep last state);
  nothing auto-marks posts gone (T1 § 5.3).

### 5.4 Post rollup

| Verifiable, non-retired, participating links | Post state |
|---|---|
| ≥ 1 `live` or `relisted` | `live` |
| none live, ≥ 1 `suspect` | `suspect` |
| ≥ 1 link, all `gone` | `gone` |
| none verifiable | `live`, `verifiable = false` |

- `reply` links and retired links never count. A post going `gone` → `live` stamps `relisted_at`, bumps
  `relist_count` and emits `post.relisted`; a repost under a new id or URL arrives as a new link that dedup joins,
  and the event reason says `reposted`, not `relisted`.
- Rollup runs in the transaction of the link change, under the post-row lock.

### 5.5 What the schedule config carries (T7 runs it)

```txt
checkPolicy: web-listing-daily
methods:         [direct_fetch]                 # ordered; enumeration_absence, mtproto_by_id, embed_probe,
                                                # provider_rescrape, compliance_batch, api_exists
cadence:                                        # age = now - first_seen_at; first band wins
  - { ageUnder: 2d,  every: 6h }
  - { ageUnder: 14d, every: 1d }
  - { otherwise,     every: 7d }
byEventTime:     { within: 14d, every: 1d, stopAfterEnd: 7d }
interest:        { watched: 1d }                # a consumer watch tightens, never loosens
confirmChecks:   1                              # 2 for embed_probe and mtproto_by_id
suspectResolveWithin: 3d
enumeration:     { completeOnly: true, dropGuardPct: 30 }
relistStableChecks: 2
budget:          { requestsPerHostPerDay: 20000, usdPerMonth: null }
stopAfter:       { age: 365d }
```

- The budget is real. At one request per 2 seconds per host (W13) a host has 43,200 requests a day. With ~60,000 live
  links and the bands above, checks need ~45,000 requests a day, ~33,000 of them on OLX if it holds three quarters of
  the live set (arithmetic on § 9.1 assumptions, U). Cadence must be adaptive and prioritised (watched posts first), not fixed.
- `enumeration_absence` is free where a sitemap exists and useless where only search pages exist.

---

## 6 · Containers and visibility

### 6.1 Rules

- Two kinds: the **pool** (everything harvested publicly under WoW2's own pipelines) and a **private container** per
  consumer (T4-9: the Events service is the tenant with one container per catalog; Ocharo never calls Harvest).
- Private contents: submitted links on unharvested domains, hand-typed entries, intake submissions, and credentialed
  sources (Sourcing's signed-in RFQ inbox never enters the pool, T4-4).
- A private container **reads** the pool through subscriptions and aliases; the pool never reads a private container.
  Reads are scoped `container_id IN (own, pool)` in the service layer; row-level security as a second guard on the read
  role is possible, with a cost I have not measured (U).
- Dedup runs inside a container. For a private container only tiers 0–1 may look into the pool, and only to create an
  alias; fuzzy matches against the pool become private review suggestions.
- Private content is never merged into a pool post: that would leak consumer-only fields, signed-in captures and the
  fact of the consumer's interest. Contribution to the pool is an explicit operator act, not built in v1 (T5-14).

### 6.2 Where a submitted link goes

| Step | Test | Result |
|---|---|---|
| 1 | normalize (T3 § 2.7) and route social URLs to their adapters | |
| 2 | `source_scopes` host + path match an `active` pool source with `coverage = whole` and `permission` ∈ `open` · `granted` | the link is *covered* |
| 3 | not covered, but the URL is already a link of a pool source | covered (a `filtered` source covers only URLs it already found) |
| 4 | covered and already captured | an alias post in the consumer's container pointing at the pool post |
| 5 | covered, not captured | queue a single-URL capture in the pool source (its policy and pacing, T3 step 3); create the alias now |
| 6 | not covered | private source `coverage = single` for that host in the consumer's container; fetch there |
| 7 | host's pool source is `restricted` or `denied` | not covered; the private fetch obeys the same `host_policies.permission` |

- Intake works the same way: a forwarded public post resolves to its origin `(chat, id)`; if the origin channel is a
  covered pool source the forward becomes an alias, else it is a private `single` link with `consent_basis = submitter`.
- OLX's filtered Tashkent real-estate pipeline covers no unseen OLX URL; an Ocharo machine listing goes private (T4 § 5).

### 6.3 Alias posts

- A private post may carry `alias_of = pool post`. Its fields read through to the pool post, overlaid by readings from
  the container's own `manual` source. The consumer's reference is the private id, which never changes.
- Aliases follow `merged_into` on the pool side and show `purged` if the pool post is purged.
- If the pool source is retired, alias posts keep their last content and the consumer can adopt a private link.

### 6.4 When a private domain becomes public

1. A pool source with `coverage = whole` is created or its scope widens: the job `adopt_private_links` finds private
   links of every container whose URL falls in the scope.
2. For each, ensure the pool link exists (queue a capture if not), turn the private post into an alias, retire its
   private links with `retired_reason = covered_by_pool`, and emit `post.rebased` to the consumer.
3. The private captures stay, immutable, until their retention ends; nothing of them enters the pool.
4. If the pool cannot obtain the URL (restricted, blocked), the link stays private.

- The consumer's post id and delivery history stay valid throughout; only the content source changes.

### 6.5 Self-hosted and library forms

- Form 2 instance: one pool and its own consumers' containers, same schema. Form 1 library: one private container, no
  pool, no alias. Form 3: WoW2's pool plus a container per consumer. `containers.kind` is the only difference.
- Credentials (Meta, X, Google, Telegram sessions) are per-container or per-instance references held in the vault and
  never in these tables (S3, T4-4).

---

## 7 · Retention and personal data

### 7.1 Retention classes

| Class | Applies to | Raw body | Readings and fields | Media | Metrics | Duties |
|---|---|---|---|---|---|---|
| `standard` | web, listings, feeds, Telegram preview | 365 days after the link's last capture (U) | while the post lives | thumbnail + first image while the post lives; originals 90 days after `gone` (ListingShelf's number) | 400 days, daily after day 7 | operator takedown |
| `youtube` | YouTube Data API | none | ≤ 30 days, then refresh or delete (T2) | none: embed only | ≤ 30 days | existence check ≤ 30 days; user deletion ≤ 7 days |
| `meta` | Meta API and providers on Instagram, Facebook | 30 days, refreshed while a pipeline subscribes (provisional) | same | thumbnail only | 30 days | delete when unneeded and on request (Platform Terms §3.d, T2) |
| `x` | X API | ≤ the compliance window | apply events daily | by X policy (U) | by X policy (U) | `delete` → purge; `rehydrate` → re-fetch; `scrub_geo` → null geo |
| `telegram` | public Telegram, any route | as `standard` | as `standard`; AI off by default | fetched at capture | as `standard` | Bot Terms §4.2 on intake |
| `intake` | consented submissions | until withdrawal | until withdrawal | as `standard` | – | delete on request |

- A class is data: `retention_policies(key, raw_ttl, reading_ttl, media_ttl, metric_ttl, refresh_every,
  mandatory, delete_request_sla)`. Official routes force their class on; an operator cannot loosen it.
- `captures.expires_at` is computed at insert from the source's class, so a later policy edit never lengthens a
  platform duty for rows already stored.

### 7.2 Purge versus immutable captures

- Inside its window a capture is immutable: no role but `harvest_purge` can `DELETE` it or `UPDATE` the three purge
  columns.
- The purge job selects `expires_at <= now() AND scrubbed_at IS NULL`, deletes the File Storage file, sets
  `scrubbed_at`, `body_ref = NULL`, keeps the row (id, hashes, metadata) as a stub unless the reason is a data-subject
  request, in which case it deletes the row (T5-10).
- **Propagation:** purging a link's capture also drops its `link_readings`, `link_media` and `link_metrics` for that
  class, then runs `ResolvePost` without it. A field whose winner came from the purged link falls to the next claim,
  or clears if none remains; a post left with no claim becomes a shell (`purged_at`) and T7 emits `post.purged`.
- **Refresh instead of purge:** `youtube` (and `meta` while subscribed) re-fetch before `expires_at`, writing a new
  capture with a renewed date; a failed refresh purges.
- Deliveries carry `retention_class` and `delete_by`; a consumer that stored a delivered item must honour `post.purged`
  (the platform duty binds data received, not only data held; T7 puts it in the delivery contract).

### 7.3 Personal data

| Item | Where | Rule |
|---|---|---|
| author name and handle | `link_readings.fields` | handle kept, profile data not (S12) |
| phones, emails | `link_readings.contacts` raw; `contact_keys` keyed hash | raw excluded from pool reads and from default selects; visible to the pipeline's subscribers only (T4-7) |
| intake submitter | `intake_consents` | HMAC of the sender id, text version, timestamp, `withdrawn_at`; no profile data |
| media of people | `media_assets` | as the post |
| captured bodies | File Storage | contain everything on the page; purge removes them whole |

- `intake_consents(id, container_id, subject_kind, subject_key bytea, text_version, given_at, withdrawn_at, channel,
  evidence jsonb)`; every link from that submitter carries `consent_id`.
- **Deletion on request** (submitter, platform user, or data subject): find links by `consent_id`, or by
  `contact_keys.key = HMAC(value)` for a named person; purge their captures and readings; recompute posts; log the
  request. Internal service level: 7 days, matching YouTube's.
- Uzbek personal-data law (database registration, localization of citizens' data) was deferred to this track by S12 and
  is **not read here** (U). The schema is ready for either answer: `containers.residency` and subject keys make
  localization a placement choice (T8) and erasure a query.

---

## 8 · Locale alternates and multi-part posts

### 8.1 Locale alternates (W11)

- One post, many links: each URL in each locale is a `post_links` row with `locale`, role `alternate` except the
  primary-locale link.
- Alternates are declared by structure, never inferred by language: `hreflang`, `<link rel=alternate>`, a path locale
  swap on a known pattern, shared JSON-LD `@id`. These are tier 1.
- `post_texts` holds one row per locale; trigram and text-hash dedup run within a locale (and across `uz-Latn` /
  `uz-Cyrl`, which are one language in two scripts after transliteration).
- The default locale is `primary_locale` (site default, else the majority of links); consumers read any locale or fall
  back to the primary (`Accept-Language`, Events' contract).
- Undeclared translations (a Telegram channel posting ru then uz) are found only by embeddings or a human; review-only.

### 8.2 Multi-part posts

| Shape | Model |
|---|---|
| Telegram album | one link, `external_key` = lowest message id; `link_parts` rows per member (`part_key` = message id, `position`, `grouped_id`, `state`); text from the captioned member; link `gone` only when all parts are (album id gaps are not deletions, T1 § 2.2) |
| thread by one author (X, Telegram sequence) | parts as `link_parts` of the root link; text concatenated in order |
| replies and comments by others | links with `role = reply`, `parent_link_id`; stored only when a pipeline asks; excluded from resolution, dedup and state; terms exposure is higher (T1 § 7) |
| forum topics | `parent_link_id` = topic root; same as threads |

---

## 9 · Volume and growth

### 9.1 Assumptions (design point: Haven plus Ocharo, year 1)

| Input | Value | Basis |
|---|---|---|
| new links a day | ~2,000: Haven OLX + Domtut ~1,500, Telegram groups and Instagram ~400, Ocharo Events ~100–200 | 1,416 OLX listings in one dataset, ~1,100 classified on one day (T4 § 5); 151 event families, 17 Instagram and 11 Telegram channels, Afisha's ~3 changed child sitemaps a day (T3, T4) (all U as rates) |
| links per post | 1.3 | dedup rate guess (U) |
| changed captures per new link | 0.5 | price and text edits (U) |
| live links | ~60,000 | listings live for weeks (U) |
| one-off backfill | 10⁵–2·10⁵ links | Telegram history is random-access by `?before=`; `@afishauz` ids reach ~34,000 (T1) |
| headroom | 10× | |

### 9.2 Rows and size

| Table | Rows a year | Row | Heap | Indexes | Notes |
|---|---|---|---|---|---|
| `captures` | ~1.1M | ~350 B | 0.4 GB | 0.3 GB | bodies in File Storage |
| `post_links` | ~0.75M | ~300 B | 0.25 GB | 0.2 GB | |
| `link_schedule` | ~0.75M | ~80 B | 0.06 GB | 0.06 GB | ~65,000 updates a day: needs aggressive `autovacuum` |
| `link_readings` | ~0.75M | ~2.5 KB | 1.9 GB | – | TOAST-compressed text |
| `posts` + `post_texts` | ~0.55M | 0.5 + 2.5 KB | 1.65 GB | ~1 GB trigram (U) | |
| `post_edits`, `link_events` | ~0.8M, ~1M | ~150 B | 0.27 GB | 0.1 GB | |
| `link_metrics` | ~3.7M | ~70 B | 0.26 GB | 0.15 GB | ~500 social links a day × ~20 rows in the first week |
| `link_check_log` | ~2M held | ~80 B | 0.16 GB | – | 30-day window |
| media tables | ~0.8M, ~2M | ~150 B | 0.4 GB | 0.1 GB | |
| **PostgreSQL** | | | | | **~7 GB a year (U)**; ~70 GB at 10× |
| File Storage, bodies | ~1.1M | ~25 KB Brotli | ~27 GB | | ListingShelf compresses HTML with Brotli level 5 |
| File Storage, media | ~0.8M | ~200 KB | ~160 GB | | thumbnail + first image (S9); links for the rest |

- File Storage cost on the recommended Contabo object store is a few euros a month at this size (File Storage spec §
  Backing store); storage is not the constraint, request budget and review load are.
- Metrics are written only on change; after seven days they roll up to one row a day; `youtube` rows expire in 30 days.

### 9.3 Partitioning

- `captures` and `link_metrics`: monthly range partitions, created three months ahead by a job; a default partition
  catches strays. Partition counts stay far under the "few thousand" the planner handles [pg-part].
- At the design point (~100,000 capture rows a month) partitioning is operational, not required. It is chosen at birth
  because moving a populated table into a partitioned one is a rewrite, and `DETACH PARTITION CONCURRENTLY` gives
  cheap cold-storage moves [pg-part].
- Cost accepted: primary keys carry the partition key, and no foreign key points at these tables.
- Not partitioned: `post_links`, `posts` (the working set is hot and key-addressed), `post_edits`, `link_events`.
- `link_check_log`: weekly partitions dropped after 30 days (or a delete job; U at this volume).
- Per-row purge is the main retention tool for short classes; partition drops only retire months in which every row
  expired.

---

## 10 · ER diagram

```txt
containers 1─* sources *─1 publishers          sources 1─* source_scopes · source_aliases · (source_routes: T3/T7)
    │1             │1                           sources 1─* enumerations            host_policies, retention_policies,
    │*             │*                                                               check_policies: global config
    │         post_links *────1 posts ──── alias_of ⇢ posts (pool)      posts ──── merged_into ⇢ posts
    │              │1             │1                                    
    │              ├─1 link_schedule          ├─* post_texts            merge_candidates *─2 posts
    │              ├─1 link_readings          ├─* post_edits            merge_log        *─2 posts
    │              ├─* captures (monthly)     ├─* post_media *─1 media_assets 1─* link_media *─1 post_links
    │              ├─* link_events            ├─* contact_keys *─1 post_links
    │              ├─* link_check_log (30 d)  └─* non_matches (pair)
    │              ├─* link_metrics (monthly)
    │              ├─* link_parts             intake_consents 1─* post_links
    └─ every table carries container_id; children reference (container_id, parent_id)
```

---

## Findings that change the spec

- **Concepts (spec § Concepts):** the spec stops at `capture` → `item`. The model needs `source`, `link`, `reading`,
  `post` and `container`; the unit consumers care about is the post and its events (`created` · `changed` · `gone` ·
  `relisted` · `merged` · `purged`), with the item as one link's reading. Events' `observation` is Harvest's delivered
  reading; the two words must not collide.
- **Capture (spec § Concepts, § Storage):** "immutable capture" becomes immutable inside a retention window, written
  on content change only. ListingShelf's one-snapshot-per-run grows linearly with polling; a pipeline capturing 2,000 items
  every 15 minutes writes up to ~190,000 snapshots a day, ~70 million a year, most identical.
- **Dedup (spec has none):** a deterministic ladder with guards and a review queue; merges are `move_link` and undo;
  near-duplicate matching is `pg_trgm` over Latin-transliterated text. Embeddings are optional, gated by `ai_allowed`
  and container flag, review-only.
- **Canonical fields are derived (spec § Extraction):** per-link readings with tier and authority, resolved by rule,
  with provenance per field. That one choice makes unmerge, purge propagation and AI revocation recomputations
  instead of data repairs, and makes `ai_allowed` enforceable after the fact.
- **Deletion (spec § From ListingShelf):** `gone` needs a `suspect` state, preconditions (source available, check
  authoritative, enumeration complete), unverifiable sources that abstain, and a rollup. Check volume is a budget
  problem: one host allows 43,200 requests a day at one per two seconds.
- **Retention duties travel (spec § Storage, T7 delivery):** platform terms bind data received, so deliveries need
  `retention_class`, `delete_by` and a `post.purged` event, and the schema needs a purge role and propagation.
- **Hashed phone keys (T4-7 amended):** a plain hash of nine digits is brute-forceable in minutes; the key must be an
  HMAC with a vault-held pepper, and it remains personal data.
- **Containers (spec has none):** private post ids are stable aliases to pool posts; "already harvested publicly"
  means a `coverage = whole` source with open or granted permission, or an already-found URL; private content never
  merges into the pool.
- **Partitioned tables break foreign keys:** captures and metrics are referenced softly by `(id, timestamp)`.
- **Telegram identity:** usernames change and get reused, so the numeric peer id and an alias history identify a
  source; `(username, message_id)` alone mis-attributes after a rename.

---

## Points

Open questions; each ends in a provisional pick.

- [ ] T5-1 vocabulary in the spec: add `source`, `link`, `reading`, `post`, `container`; keep `item` as a link's reading; avoid `observation` → provisional pick: yes (T8 edits the spec)
- [ ] T5-2 capture on change versus per run → provisional pick: on change; unchanged polls touch `link_schedule`; an optional heartbeat capture per pipeline, off by default (T7)
- [ ] T5-3 auto-merge thresholds → provisional pick: tiers 1–2 plus trigram ≥ 0.85 with corroboration; same-publisher ≥ 0.7; 5% of auto-merges sampled; calibrate on ~200 labelled Haven and Ocharo pairs before widening (T6 for kinds)
- [ ] T5-4 near-dup retriever → provisional pick: `pg_trgm` on transliterated `match_text`; simhash only if latency fails; embeddings stay off until T1-P1 and T6 settle AI use
- [ ] T5-5 extensions on the host → provisional pick: require `pg_trgm` (contrib); pgvector optional behind `embeddings_enabled` (T8, Wheelhouse database image)
- [ ] T5-6 cross-language matching → provisional pick: declared alternates only; embedding suggestions are review-only
- [ ] T5-7 contact keys → provisional pick: HMAC with a Secrets Vault pepper, rotation job, raw values only in `link_readings.contacts`, never in pool reads (amends T4-7) (T6, T7)
- [ ] T5-8 unverifiable sources → provisional pick: abstain from the rollup; the post carries `verifiable = false` (T7)
- [ ] T5-9 retention defaults → provisional pick: `standard` raw bodies 365 days, originals of media 90 days after `gone`, metrics 400 days; `meta` shaped like `youtube` until counsel reads (S4, P3)
- [ ] T5-10 purge result → provisional pick: a scrubbed stub (hashes, no body) for expiry; full row delete for data-subject requests; legal read before relying on it (U)
- [ ] T5-11 check defaults and budgets → provisional pick: the bands in § 5.5, `confirmChecks` 2 for embed and MTProto probes, `suspect` after one absent complete enumeration, 30% drop guard (W15); per-host request budgets in config (T7)
- [ ] T5-12 Uzbek personal-data law (S12): registration, localization, contact storage → provisional pick: not read in this track; `containers.residency` and subject keys exist; no raw contact storage goes live before the read (counsel with P3)
- [ ] T5-13 intake consent and withdrawal → provisional pick: `intake_consents` as in § 7.3; withdrawal purges within 7 days (T1-P9)
- [ ] T5-14 contributing private content to the pool → provisional pick: not in v1; an operator act when it comes
- [ ] T5-15 alias post versus pin → provisional pick: alias post with a stable private id (§ 6.3) (T7, T8)
- [ ] T5-16 partition at birth → provisional pick: `captures` and `link_metrics` monthly, no foreign keys into them; a Harvest job creates partitions unless the be sdk migrator gains `pg_partman` support (T8)
- [ ] T5-17 ListingShelf view row (T4): per post or per link → provisional pick: per post, links expanded in the detail (T4, T8)
- [ ] T5-18 brand linking acceptance (T1-P11) → provisional pick: auto for a header or footer link with matching name, else review (T3)
- [ ] T5-19 dedup settle window before first delivery → provisional pick: 2 minutes, 0 for latency-critical pipelines (T7)
- [ ] T5-20 delivery contract for retention → provisional pick: every delivery carries `retention_class`, `delete_by`; consumers must honour `post.purged` (T7)
- [ ] T5-21 field base for guards: `starts_at` with precision, price amount and currency, contact keys, location text must be in T6's base so § 3.6 guards work → provisional pick: yes (T6)
- [ ] T5-22 source unavailable for 30 days → provisional pick: a human retires the source; posts are never auto-`gone` (T7)

---

## Sources

PostgreSQL and extensions (read 2026-10-26):
- [pg-trgm] https://www.postgresql.org/docs/current/pgtrgm.html — non-alphanumerics ignored, case-insensitive, `similarity_threshold` 0.3, GIN `gin_trgm_ops` for `%` and `LIKE`, GiST for distance ordering
- [pg-trgm-c] https://postgrespro.com/list/thread-id/1757572 — "Thread: pg_trgm", 2008–2010 reports that non-ASCII letters are skipped in the `C` locale; a 2013 commit changed trigram construction; current behaviour not confirmed (U)
- [pgvector] https://github.com/pgvector/pgvector — v0.8.7; HNSW and IVFFlat limits 2,000 (`vector`), 4,000 (`halfvec`), 64,000 (`bit`); `bit` with `<~>` and `bit_hamming_ops` on HNSW; iterative scans since 0.8.0; post-index filtering caveat
- [pg-part] https://www.postgresql.org/docs/current/ddl-partitioning.html — unique and primary keys must include all partition key columns; pruning; "up to a few thousand partitions"; `DETACH PARTITION … CONCURRENTLY`
- [pg-bit] https://www.postgresql.org/docs/current/functions-bitstring.html — `bit_count(bit)`, `bit # bit` for equal lengths, integer casts to `bit(n)`
- [pg-bin] https://www.postgresql.org/docs/current/functions-binarystring.html — `bit_count(bytea)`; introduced in PostgreSQL 14 per the docs back-patch thread (search result; release notes not read, U)
- [pg-uuid] https://www.postgresql.org/docs/current/functions-uuid.html — `uuidv7()` built in on PostgreSQL 18; no monotonicity guarantee documented
- multilingual embeddings: searches on 2026-10-26 did not confirm Uzbek support for BGE-M3 or multilingual-e5 (U); XLM-RoBERTa's 100 training languages include Uzbek from background knowledge, not from a page read

Workspace:
- ListingShelf: `Persistence/Migrations/001-baseline`, `003-absences`, `006-photos`, `007-exports`; `Persistence/Repositories/ListingSnapshotRepository.cs`; `Infrastructure/Runs/OrchestrationServices/RunExecutionService.cs` (all under `lb`)
- Haven: `Haven.Database/Haven.Database.Persistence/Migrations/002-external-listings`, `008-listing-phones`; `Haven.Supply/Haven.Supply.Persistence/Intake/Repositories/ExternalListingRepository.cs` (under `hb`)
- [harvest-service-spec.md](../harvest-service-spec.md) · [events-service-spec.md](../events-service-spec.md) § Harvest seam · [file-storage-service-spec.md](../file-storage-service-spec.md) § Instances per owner · [analysis index](harvest-analysis-2026-10.md)
- [t1-messaging-sources.md](t1-messaging-sources.md) · [t2-social-sources.md](t2-social-sources.md) · [t3-web-sources.md](t3-web-sources.md) · [t4-consumers-and-social.md](t4-consumers-and-social.md)
- format: [identity T10](../identity-analysis-2026-10/t10-schema-migrations.md)
