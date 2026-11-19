# SCFD subscription modes: what exists, and a design sketch

## Settled so far

- Settled by the developer in the `ev-ai` chat (2026-11-17), so points 3, 5, 6 and 12 below are closed:
  - Two AI layers, both in SCFD.
  - Layer 1 (triage, the `post-tags` pass) runs on every post with one small prompt on a cheap model: "one small
    prompt with cheaper model to identify the type is recommended". Its output is this map's two axes, type
    (kind → format) and category → sub-category, from SCFD's operator-owned taxonomy, with the publisher category as
    a hint.
  - Layer 2 (extraction) runs only on posts some subscription's selector matches, with a backfill when a
    subscription is added ("agreed"). There is one extraction prompt per (category, kind), never per source: "we use
    prompt based on use case - for haven it's apartments, for ocharo it's fashion events".
- Layer 1's extra fields, confirmed by the developer in `ev-ai` (2026-11-17: "confirmed extra fields, can also add a
  translated title as well - for english translations"):
  - `about` (what the post describes), `timeframe` (upcoming, ongoing, past or evergreen), `items` (how many events
    or listings the post holds, so a digest splits)
  - `language`, `confidence` (a stronger model re-tags below a bar), `titleEn` (an English title passes through)
  - geography stays a location filter, not a tag
- Proposed in `ev-ai`, not decided: one canonical shape per (kind, category), a base type shape plus a category block.
  It is a child of point 2.
- Points 2-4 settled in `ev-ai` (2026-11-18/19): IAB 3.1 tier-1 domains (minus `Events`, `Genres`, `Sensitive Topics`)
  with subdomains, open English topics, entity types `event` and `listing` only (`opportunity` later); every tag,
  topic and label English only. Layer 1's keys are the selector's keys.
- Point 1 settled (developer, relayed by `ev-ai` 2026-11-19): one selector each subscriber sets — "scfd mustn't have
  any prompts specific for products, it's purpose is to just analyze the type of event"; "client must be able to
  configure what it needs dynamically right ?". Ocharo's selector: `event` AND (`style-fashion` excluding
  `style-fashion/beauty`, or topics `textile`, `ikat`, `garment`); the beauty exclusion waits on the developer's word.
  Built by the `ev-selector` lane with the map's picks for points 8-11 and 14; still the developer's: 7 (prompt-mode
  subscriptions) and 13 (the shadow-to-live switch).
- Entity model (developer in `ev-ai`, 2026-11-18: "we need entity type based architecture and we'll break it down as
  such later"; "basically one entity / one source of truth for events we need"; due end of November): draft in
  [scfd-entity-model.md](../../../../ideas/scfd-entity-model.md). Proposed there, open: posts and entities joined by a
  role relation; a posts feed and an entity-changes feed a subscription can pick; point 2's type axis split into
  entity type and post form. `ev-ai` streams those points and reports each one that settles.


*Written 2026-11-17, read-only, for events-integration #68. Code: harvest `main` `559c7e2` (clean tree), events `73b390e`
plus `ev-build`'s uncommitted E12 edits, ai `fe7d21b` plus `ev-ai`'s paused WIP. Data: the local SCFD stack's
database (`harvest_sources`, read-only `SELECT`s). The deployed `harvest-dev` database was not queried.*

Path roots:

- `{h}` = harvest `engineering/codebase/harvest.backend-services`
- `{e}` = events `engineering/codebase/events.backend-services`
- `{ai}` = ai `engineering/codebase/ai.backend-services`
- `tasks/` = wow-two-ws `system/sessions/events-integration/tasks/`

The developer's words (2026-11-17):

- "subscribers to subscribe with 2 modes - either use those categories and types of posts ( or should I say category
  and sub category ) or subscribe with a prompt so that our own ai in scfd chooses matching tags to that prompt"
- "also another option - should be choosing specific sources as well, and then one between - like choose tags with
  inclusion / exclusion of sources and prompt with inclusion / exclusion as well"
- #58 (2026-11-10): the operator adds sources through adapters, a subscriber chooses from them, and "later we'll add
  tags based on the source classification we do with ai models".

## Overview

- Today a subscription follows exactly one pipeline (one source section), through one filter: a registered regex
  filter or one literal tag.
- No post carries a tag from a shared vocabulary. Only Afisha emits free-form publisher labels (`SourceTags`). No AI
  pass runs anywhere in SCFD.
- Events binds one intake source per SCFD subscription, but keys sourced records by post ID. Moving Ocharo to one
  subscription therefore creates no duplicate events.
- Recommended shape: one **selector** subscription. It combines sources (include and exclude), a post type, and a
  category with sub-categories. A subscriber builds it by picking chips, or by writing a prompt that SCFD's AI compiles
  once into editable chips. Matching runs over tags that SCFD writes once per post. Publisher categories are mapped
  for free, and one AI tagging pass per post fills and corrects them.
- 14 decision points, 7 of which only the developer can decide (#3 below).
- The design supersedes S09, S16, E01 and most of E20. It changes S08, S10, S11, S15, S17, S28, S31, E02, E12, E19, A05
  and A07. E03 and E04 become prerequisites (#4 below).

---

## 1. Today

### 1.1 How a subscription is defined and filtered

| Piece | Fact | Evidence |
|---|---|---|
| Model | `Kind` (`Channel`, `Tag`, `Keyword`), `PipelineId`, `Rules`, `FilterKey`, `WantsAi`, `Schema`, `Context`, `Backfill` | `{h}/packages/Abstractions/Delivery/SubscriptionModel.cs:13-41`, `SubscriptionKind.cs:6-13` |
| Declaration | `PipelineId` is required; `FilterKey` is "a host filter key or `tag:<value>`" | `SubscriptionDeclaration.cs:11`, `:15` |
| Schema | `kind IN ('channel','tag','keyword')`, `(kind = 'channel') = (pipeline_id IS NOT NULL)`; `rules jsonb` and `wants_ai` exist but nothing reads or writes them | `{h}/packages/Module/Migrations/001-baseline/Apply.sql:724-757` (`:749`, `:750`); `005-subscription-filter/Apply.sql:1-2` adds `filter_key` |
| Write path | Module always inserts `kind='channel'`, `mode='pull'` and always reads `Kind = Channel`; `tag`/`keyword` are reserved, not built | `{h}/packages/Module/Delivery/ModuleDeliveryBroker.cs:52-58`, `:151` |
| Access | The pipeline must sit in the pool or the tenant's own container; creation needs `subscriptions:manage`, reads and pulls need `events-read` | `ModuleDeliveryBroker.cs:44-48`; `{h}/packages/Hosting/Delivery/Controllers/SubscriptionsController.cs:19-21`, `:58-60` |
| Filter resolution | null admits everything; a registered key runs its `IDeliveryPostFilter`; anything else is `tag:<literal>`; a throwing filter admits nothing | `{h}/packages/Module/Delivery/DeliveryPostFilters.cs:11-19` |
| Tag filter (`864dc6e`, 11-10) | exact, case-insensitive match on one `Tags[].Tag` or one `SourceTags` value; one tag per subscription | `{h}/packages/Abstractions/Delivery/DeliveryTagFilter.cs:11-21` |
| Registered filters | `ocharo-fashion-v1`: kind `Event`, not an editorial article, then a multilingual subject regex plus an event-context regex; `marketplace-listing-v1`: kind `Listing` | `{h}/sources/Module/Ocharo/OcharoFashionFilter.cs:12-35`; `{h}/sources/Module/Marketplace/MarketplaceListingFilter.cs:18` |
| Delivery-time matching | per post write, picks active subscriptions **in the post's container** whose pipeline ran the capture, or whose source links the post, or that already received it; then `withinSection` (path-scoped section) and the filter; lifecycle events pass for a post the subscription has already seen | `{h}/packages/Module/Delivery/DeliveryEventWriter.cs:17-38` (`withinSection` `:34-35`); `PipelineScope.cs:19-27` |
| Backfill | only at creation: `live` (every live post of the pipeline's source inside the scope and filter), `none`, `since` | `ModuleDeliveryBroker.cs:59-80` |
| No-longer-matching | a seen post that stops matching sends nothing (E03 plans `post.unmatched`) | `DeliveryEventWriter.cs:36-38`; `tasks/tasks-events-path.md` E03 |

Facts that shape the design:

- One subscription is one section. Ocharo setup creates **one subscription per pipeline**: filter
  `ocharo-fashion-v1`, schema `wow2.event.v1`, context `catalog`, `sourceGroup`, `sourceChannel` and `eventFamily`
  (`{h}/sources/Module/Ocharo/OcharoSourceProvisioner.cs:137-157`; `engineering/architecture/contract.md:263-264`).
  Haven's marketplace setup creates one subscription per saved search (`{h}/sources/Module/Marketplace/MarketplaceProvisioner.cs:89-100`).
- Matching never crosses containers (`DeliveryEventWriter.cs:22`, `s.container_id=@container`). A subscription that
  spans the pool and a private container needs a new rule.
- The spec already planned pool subscriptions: "`tag` and `keyword` (read the shared pool, never create a pipeline; a
  keyword may *propose* one)" (wow-two-ws `ideas/harvest-service-spec.md:184-185`). The backlog row "Tag and keyword
  subscriptions" is still `planned` (harvest `engineering/planning/backlog.md:50`).

### 1.2 Tags and categories on posts

| Field | Meant for | Written by | On data |
|---|---|---|---|
| `PostEnvelope.Kind` (`Event`, `Listing`, `Offer`, `News`, `Promo`, `Discussion`, `Other`) | what the post is; dedup never merges two kinds | rules: schema.org Event or Product, else the request's default (`{h}/packages/Module/Extraction/RulesPostExtractor.cs:140`) | local stack: 47 `event`, 43 `unknown` (articles with no event node) |
| `PostEnvelope.SourceTags` | "the publisher's original labels, before mapping" (`PostEnvelope.cs:50`) | Afisha only: `material.tags` from the page data (`{h}/sources/Afisha/AfishaCaptureReader.cs:84-86`) → metadata → `RulesPostExtractor.cs:47-52`, `:142` | local stack: 89 of 90 live posts. The labels are free-form Russian editorial words: `концерт` 18, `выставка` 18, `мода` 6, `фоторепортаж` 4, `tft expo` 4, `отмена` 3 |
| `PostEnvelope.Tags` (`PostTag`: `Tag` such as `real-estate.rent`, `Score`, `Tier`, `Version`) | "tags from the shared vocabulary" (`PostEnvelope.cs:53`, `PostTag.cs:7-16`) | **nothing**: no code path creates a `PostTag` | local stack: 0 posts |
| `PostEnvelope.Classification` (`Classifier`, `Verdict`, `Confidence`, `Reason`, `Kind`) | one relevance verdict; `Kind` is "in the subscriber's taxonomy" (`PostClassification.cs:24-25`) | "no SCFD step writes it yet" (`PostClassification.cs:8`) | local stack: 0 posts |
| Publisher category (`fashion`, `exhibitions`, `concerts`) | Afisha's URL segment | read time only, as the console's "Publisher category" facet (`{h}/sources/Afisha/AfishaSourceAdapter.cs:49-53`); **not** in the envelope (S11 plans `afisha:{category}`) | local stack, by link URL: `concerts` 39, `exhibitions` 27, `fashion` 17, others 7 |
| Section topic | console glyph | guessed from the section name; `SourceSectionDefinition(Label, Url, Locale)` has no topic (`{h}/packages/Abstractions/Sources/ISourceSectionCatalog.cs:11`; S28) | — |

- Dev data: deployed `harvest-dev` was not queried. No code writes `Tags` or `Classification`, so both are empty there
  too. `SourceTags` on dev's Afisha posts is probable, since `v0.2.7` carries the reader, but not verified.
- Publisher labels do not separate subject from format, and they mix editorial labels (`отмена` = cancellation,
  `фоторепортаж` = photo report) with event labels. The console analysis found a concert under Exhibitions and comedy
  under Concerts (`scfd-console/scfd-console-analysis.md` § Event topics and formats).

### 1.3 AI: what classifies today, what is planned

- SCFD runs no AI. The engine hardcodes `Ai = AiMode.Off`, `AiAllowed = false` (`{h}/packages/Module/Engine/HarvestEngine.cs:156-162`).
  Extraction flags `ai_skipped:capability_unavailable` when a pipeline asks for AI (`RulesPostExtractor.cs:146`) and
  stamps tiers `Deterministic` and `Rules` only (`:148`).
- Ocharo's sources are provisioned `AiAllowed = false`, and the pipelines `Ai = AiMode.Off`. A differing existing
  posture is a conflict (`OcharoSourceProvisioner.cs:83`, `:90`, `:129`, `:134`).
- The Process stage (`ICaptureProcessor`, `{h}/packages/Abstractions/Steps/ICaptureProcessor.cs:4-20`) is the seam
  for a per-section AI pass. Its only model user is Haven's `RentalTermsProcessor`, which calls OpenAI directly
  (#65; S03 and S14 move it to the AI layer).
- The AI layer `wow-two-sdk-beta.ai` v0.1 has these pieces:
  - `IAiRunner.RunAsync` resolves a use case's prompt, calls the routed model, checks a strict output schema, falls
    back along the route and logs cost (`{ai}/packages/Abstractions/Runs/IAiRunner.cs:7-15`).
  - Prompts live in tables (rewrite or versioned mode), with an input-hash cache and evals.
  - Prices are seeded: Haiku 5.5 and `gpt-6-luna` at 0.10 / 0.50 USD per 1M input / output tokens
    (`{ai}/packages/Module/Migrations/003-seed-prices/Apply.sql:8-11`).
  - Embeddings: none.
  - Release: no `be-v*` tag, so nothing is published (ai-layer-analysis `#15`, `ideas/ai-layer-analysis.md:176`).
- The only use case defined is `ocharo-relevance`, on the local bench: answer `{ relevance: close|loose|none, kind,
  reason }`. Prompt v1 and v2 exist. Set `afisha-10` holds 10 posts with draft labels and 0 eval runs, and the provider
  keys are unset (ai repo `engineering/planning/version-track/v0.1/v0.1.md:34`; `ideas/ai-layer-analysis.md:177`).
- Planned work:
  - S14 embeds the layer in the source host.
  - S15 and A05 run `ocharo-relevance` in shadow on Afisha.
  - S16 writes the verdict into the **shared post** as `classification` and adds filter `ocharo-relevance-v1`.
  - S17 adds estimated dates.
  - A06 adds budgets. A07 moves Events to `Classifier: payload`.
- The original spec's cascade puts tags in the AI tiers. Tier E (embeddings, nearest-centroid tags, ~0.008 USD per
  1,000) and tier S (small model, zero-shot tags, ~0.12 USD per 1,000) sit behind gates G1-G5 (pipeline `AiMode`,
  source `ai_allowed`, host `ai-input`, data class, budget) (`ideas/harvest-service-spec.md:146-147`, `:157-166`).

### 1.4 How Events, Ocharo and Haven consume subscriptions

- **Events** has one intake source per SCFD subscription. Each source holds `Name`, `Catalog`, `SubscriptionId`,
  `Review` (`manual`, `auto`), `Classifier` (`filter`, `payload`), `Filter` and `MinConfidence`, plus `DefaultCountry`
  and, since `ev-build`'s uncommitted E12, `DefaultKind` (`{e}/packages/Module/Intake/EventsIntakeSourceOptions.cs:19`,
  `:63`, `:67`, `:71`, `:84`).
  - `deploy.yml` binds two subscriptions, `afisha-fashion` and `afisha-exhibitions` (events
    `engineering/deployment/deploy.yml:72-114`).
  - Each new channel costs a deploy entry: E01 adds three, and E19 and E20 aim at discovery.
- The `filter` classifier trusts SCFD: every delivered record counts as relevant (`{e}/packages/Module/Intake/IntakeVerdict.cs:29-36`).
  Under `auto` + `filter`, `Filter` must equal the subscription's `filterKey`, or intake refuses with `filter-mismatch`
  (`{e}/packages/Module/Intake/ScfdSubscription.cs:46-56`; validator `EventsIntakeOptionsValidator.cs:51`).
- The `payload` classifier reads `classification` from the record and takes its `kind` when the catalog taxonomy holds
  it (`IntakeVerdict.cs:38-57`). Events owns per-catalog kinds such as `runway` and `trade-fair`
  (`{e}/packages/Abstractions/Catalogs/CatalogKindModel.cs:3`).
- Records are keyed by `(SourceInstance, CatalogId, PostId)`, not by subscription. A record that arrives on another
  subscription updates the same row, and its `SubscriptionId` is reassigned (events `HEAD` `IntakeProcessor.cs:314`,
  `:331`). A source whose `SubscriptionId` changes restarts its cursor (`:174`).
- **Ocharo** never reads SCFD. Its Events app reads Events' catalog `ocharo-fashion` through the tracking broker
  (`tasks/tasks-events-path.md` intro).
- **Haven** Supply pulls one `wow2.post.v1` subscription per saved search, filtered `marketplace-listing-v1` (harvest
  `v0.2.md:91-94`).
- The live symptom (E00, 2026-11-17): 46 new Afisha posts since 11-13, none passed `ocharo-fashion-v1`. 3 of the 4
  sourced events in Ocharo are off-topic, matched on `шелк`, `украшен`, `аксессуар`/`ткани` (`tasks/tasks-events-path.md` E00).

---

## 2. Design sketch

### 2.1 Shape: one selector, three ways to author it

The developer's three modes all reduce to one predicate over a post: its source, its type and its categories. The
prompt is a way to write that predicate, not a separate matcher. One subscription kind, `selector`, therefore covers
every mode. The mode is how the console builds the selector, kept on the subscription only for display.

| Developer's mode | Selector it produces |
|---|---|
| Categories and types | `types` + `categories` chips; `sources` empty = every source the tenant sees |
| Prompt | the same chips, compiled by SCFD's AI from the prompt and edited by the subscriber; the prompt text kept beside them |
| Specific sources | `sources.include` only; equals today's channel subscription, or S09's many sections |
| Tags + sources, prompt + sources | chips plus `sources.include` / `sources.exclude` |

Match rule, evaluated per post revision:

```text
match = source passes (include empty or post's group/source/section included) and not excluded
    and (types empty or post type in types)
    and (categories.any empty or post has any category at or below one listed, score ≥ minScore)
    and post has no category in categories.none
    and (rule null or registered rule passes)          // transition only (#2.9)
```

- One matcher, one preview, one backfill path, and one cursor per consumer need.
- The schema already reserves the kind slot and an unused `rules jsonb` column (`001-baseline/Apply.sql:731`, `:749`).
  `keyword` is dropped, because the prompt covers it.

### 2.2 Taxonomy: type and category → sub-category

Two axes are written as `PostTag` keys in one shared vocabulary:

| Axis | Levels | Seed (illustrative) | Why |
|---|---|---|---|
| Type | kind → format | `event` → `exhibition`, `trade-fair`, `runway`, `market`, `festival`, `concert`, `performance`, `screening`, `conference`, `workshop`, `competition`; `listing` → `rent`, `sale`; `news` → `report`, `notice`; `promo`, `offer`, `discussion`, `other` | the kind exists (`PostKind`); Events' catalog kinds (`runway`, `trade-fair`, `market`) are formats, which E12 now fakes per subscription |
| Category | category → sub-category | the 14 subject areas of `scfd-console-analysis.md` § Event topics; for example `fashion-craft` → `fashion`, `textile`, `handmade`, `jewelry`, `design`; `music` → …; `business` → `trade`, `careers`; plus `real-estate` → `residential`, `commercial` for Haven | subject is independent of format: a fashion trade expo is `fashion-craft/fashion` + `event/trade-fair` |

- Keys: `type:event/trade-fair`, `category:fashion-craft/textile`. A parent matches its children (`category:fashion-craft/*`).
- Owner: the SCFD operator. It is versioned (`taxonomy@N`), stored in a table, seeded from code, with labels in ru, uz
  and en. Subscribers choose from it and never extend it, per #58's catalog stance.
- Consumers keep their own vocabularies and map from SCFD's. Events maps `type:event/runway` to catalog kind `runway`,
  which replaces `PostClassification.Kind` "in the subscriber's taxonomy" on a shared post.
- Geography (country, city) stays a field filter over `location`, not a tag. It is a later selector field.

### 2.3 How tags get onto posts

Both routes write `PostEnvelope.Tags`, each with its tier and version:

| Route | Tier | When | Owner | Cost | Reliability |
|---|---|---|---|---|---|
| Publisher mapping | `Rules` | at extraction, every post | the adapter: native category or section → taxonomy node (Afisha `fashion` → `category:fashion-craft/fashion`; section default from S28) | free | low to medium: a concert in Exhibitions, editorial labels |
| AI tagging | `SmallModel` | one pass per post revision whose title or text changed, queued on post write (not on the 6-hour Process cadence) | SCFD: one generic use case `post-tags`, output constrained to the taxonomy enum (strict schema), score per tag | ~0.0002 USD per post (#2.4) | high after evals; one pass serves every subscriber |

- Merge: AI tags at or above their score threshold replace mapped tags on the same axis. With AI off or undecided, the
  mapped tags stand. Both stay visible with their tier.
- AI tags need gates G1, G2 and G5 open on the source. That means `AiAllowed = true` on Ocharo's sources and lifting
  the provisioner conflict (`OcharoSourceProvisioner.cs:90`, `:134`). This is a posture change; decision #6.
- The same pass can return S17's `starts`, `ends` and `evidence`, so S17 rides on it instead of on a relevance answer.
- A tag change raises the post's revision. Subscribers that have seen the post get `post.changed`, or `post.unmatched`
  through E03.
- An index table `harvest_post_tags(post_id, container_id, tag, tier, score)` serves matching, previews and counts.

### 2.4 Prompt mode mechanics

| Mechanic | What runs | Visible to the subscriber | AI calls | Cost at 1,000 posts/day | at 8,000 posts/day (~800 sources, #67) |
|---|---|---|---|---|---|
| Compile once | at save: prompt → selector chips plus `uncovered` clauses the taxonomy cannot express ("where a small brand can apply") | yes: editable chips and the uncovered list | 1 per save | ~0.001 USD per save; matching costs 0 beyond the shared tagging pass | same |
| Judge every post | every candidate post (after the source and type prefilter) × every prompt subscription | no chips; a verdict and a reason per post | posts × subscriptions; a prompt edit re-judges the backfill window | 10 subscriptions: ~1.9 USD/day ≈ 57 USD/month; one edit over 30 days ≈ 5.6 USD | ≈ 460 USD/month |
| Hybrid | compile once; an opt-in AI check judges only posts the chips pass, against the prompt text | chips plus a per-post verdict | matches (~5-10% of posts) × subscriptions with the check on | 10 subscriptions at 10% ≈ 6 USD/month | ≈ 46 USD/month |
| Shared tagging pass (all mechanics) | 1 per post revision | tags on every post | 1 per changed post | ≈ 0.19 USD/day ≈ 6 USD/month | ≈ 45 USD/month |

- Assumptions: ~1,200 input tokens per call (title, text cut to ~1,000 tokens, instructions), a ~1,500-token cached
  system prompt holding the taxonomy, ~100 output tokens, at the seeded Haiku 5.5 prices. These are estimates, not
  measurements: no eval run exists yet.
- Recommended: compile once now. It is what the developer described ("our own ai in scfd chooses matching tags"): it is
  previewable and it adds no per-post cost. The hybrid check comes later as an opt-in, reusing S15's
  `ocharo-relevance` work for precision.
- A per-subscription verdict lives on that subscription's delivery event, as `classification`, never in the shared
  post. Events' `payload` classifier reads it unchanged. S16 as written would put one subscriber's verdict and kind
  into every subscriber's copy of the post.

### 2.5 Sources: include and exclude

- Ids at three levels: group (publisher, #30), source (channel), section (pipeline). Exclude wins over include, and an
  empty include means every source the tenant can see (the pool plus its own containers).
- Following never turns harvesting on. The operator sets schedules (#44). The editor marks an included section that
  is not collected, and the operator decides.
- Matching moves from "the subscription's container" to "a container the tenant can see". The writer filters
  subscriptions by tenant visibility and source ids before evaluating tags (`DeliveryEventWriter.cs:17-27` changes).
- Each delivered event carries per-post provenance: group, source, section and the group's country. Consumers then stop
  inferring them from per-subscription context.

### 2.6 Previews and counts before saving

`POST api/subscriptions/preview` takes a selector, or a prompt, which it compiles first. It returns:

- the matched count over the last 30 days of stored live posts (window selectable), with a per-source breakdown
- per chip, how many posts it adds or removes, using the console facet logic: counts ignore the chip being counted
  (contract.md § Stages, discoveries and Posts queries)
- the 20 newest matches, and up to 10 near misses (dropped by exactly one exclude, or matching the category but not
  the type), each with the reason, as the Posts tab's `Matched | All` switch does (#47)
- coverage: the share of the window's posts with AI tags. A low count may mean untagged posts, not few matches.
- for the hybrid check: verdicts on a 20-post sample and the cost of that sample

Tag selectors cost no AI. Previews read `harvest_post_tags` and need no new pipeline.

### 2.7 Backfill when a subscription changes

- A selector edit creates selector version N+1 (with history), on the same subscription and the same cursor.
- SCFD re-evaluates the live posts in the backfill window (default 30 days, or `since`):
  - a newly matching post appends `post.new` with reason `backfill`
  - a delivered post that no longer matches appends `post.unmatched` with reason `resync` (E03)
  - a post that still matches appends nothing
- A taxonomy version change or an AI re-tag changes post revisions, so the normal write path re-evaluates them. A
  pool-wide re-tag runs as a paced bulk job, never one storm.
- Each event records the selector version that admitted it.
- Prerequisites: E03 (`post.unmatched`) and E04 (Events holds an unmatched untracked event).

### 2.8 One subscription replaces the per-pipeline ones Events binds

- Ocharo gets one selector subscription, for example `ocharo-events`:
  - `sources.include`: the Ocharo registry groups
  - `types`: `event/*`
  - categories: `fashion-craft/*`, `business/trade`
  - exclude: `music/*`
  - schema `wow2.event.v1`, context `catalog=ocharo-fashion`
- Events binds it as one intake source. New channels need no deploy entry, which makes E01 unnecessary and E20 largely
  so.
- Per-channel intake settings move into the payload:
  - `DefaultKind` (E12) becomes the `type` format mapped to a catalog kind
  - `DefaultCountry` becomes the group country on the per-post provenance
  - the source name rides the provenance too
- Events' `filter` check changes from `filterKey` equality to the subscription's selector name and version. The review
  actor becomes `selector:{name}@{version}`.
- No duplicates appear on the switch: Events keys records by `PostId` (`IntakeProcessor.cs:314`). Re-pointing
  `Sources:0` to the new subscription restarts its cursor (`:174`) over the backfilled log.

### 2.9 Migration from `ocharo-fashion-v1`

1. Ship the selector kind with a transition field `rule`, which names a registered filter.
   - `ocharo setup` creates `ocharo-events` with `sources` = the Ocharo groups and `rule = ocharo-fashion-v1`, backfilled
     over the live posts.
   - Output equals today's union of the per-pipeline subscriptions. `filterKey` stays `ocharo-fashion-v1`, so Events'
     check passes.
2. Events re-points `afisha-fashion` to `ocharo-events`, disables `afisha-exhibitions`, and drops E01's three extra
   entries.
3. Ship publisher mapping (S11, S28), then the AI tagging pass (S14, then the retargeted S15) on the Ocharo sources.
   - The preview's diff shows rule-only, tags-only and both, as a weekly shadow report.
4. The developer switches: the selector drops `rule` and keeps the tags.
   - Backfill emits `post.unmatched` for off-topic posts (E03, E04 first). The 3 off-topic Ocharo events leave the
     list.
5. Archive the per-pipeline subscriptions and retire `ocharo-fashion-v1` once no subscription names it. E02's regex
   fix serves only as a stopgap before step 4.

### 2.10 Contract and schema sketch

```jsonc
// POST api/subscriptions — kind "selector"; PUT api/subscriptions/{id} makes version N+1
{
  "tenantId": "…", "name": "ocharo-events", "schema": "wow2.event.v1",
  "context": { "catalog": "ocharo-fashion" },
  "selector": {
    "types": ["event/*"],
    "categories": { "any": ["fashion-craft/*", "business/trade"], "none": ["music/*"] },
    "sources": { "include": [{ "group": "…" }], "exclude": [{ "section": "…" }] },
    "minScore": 0.5,
    "prompt": { "text": "…", "compiledVersion": 3, "uncovered": ["…"] },   // prompt mode only
    "rule": "ocharo-fashion-v1"                                             // transition only
  },
  "backfill": { "mode": "since", "sinceUtc": "…" }
}
```

- Routes:
  - `GET api/taxonomy` returns the versioned vocabulary with labels.
  - `POST api/subscriptions/compile` turns a prompt into a selector draft.
  - `POST api/subscriptions/preview`.
  - `GET api/subscriptions` for the tenant's own subscriptions (E19's read).
- Migration `010-subscription-selectors` (the next free ordinal on 17 November; 009 is `step-operations`):
  - the kind check adds `selector`
  - new columns `name`, `selector jsonb`, `selector_version`
  - tables `harvest_subscription_selectors` (history), `harvest_post_tags` and `harvest_taxonomy`
- Event payload, additive:
  - `match { selectorVersion, via: tags|rule|source, tags[] }`
  - `source { group, source, section, country }`
  - `tags[]`, which `wow2.event.v1` already reads from the envelope

---

## 3. Decision points

Parent before child. "Developer" marks a point only the developer can settle. Every other point the orchestrator can
settle on the pick.

| # | Decision | Options | Pick and reason | Who |
|---|---|---|---|---|
| 1 | Subscription model | (a) one `selector` subscription; the modes are ways to author it · (b) a separate kind per mode (tag, prompt, source) | (a): one matcher, preview and backfill, and the "one between" modes come free | Developer (it reframes his modes) |
| 2 | Taxonomy shape (child of 1) | (a) category → sub-category only, kind a fixed filter · (b) type (kind → format) plus category → sub-category · (c) flat tags | (b): Events' catalog kinds are formats, and subject is independent of format | Developer ("categories and types … or category and sub category") |
| 3 | Taxonomy owner (child of 2) | (a) SCFD operator's one shared vocabulary; consumers map · (b) per-tenant taxonomies · (c) shared plus tenant extensions | (a): one tagging pass serves every subscriber; per-tenant taxonomies multiply AI cost | Developer |
| 4 | Seed list v1 (child of 3) | (a) events and listings only: the 14 subject areas, event formats, listing types · (b) a full general taxonomy now | (a): covers Ocharo and Haven; grows by version | Developer reviews the list |
| 5 | How tags reach posts (child of 2) | (a) publisher mapping only · (b) AI only · (c) both: mapping now, AI fills and overrides above its threshold | (c): mapping is free and ships before the AI release; AI fixes mislabelled sections | Orchestrator |
| 6 | AI tagging posture and spend (child of 5) | (a) one pass per post on every AI-allowed source, operator-paid · (b) only on sources a subscriber pays for · (c) only on Ocharo's sources | (a): ~6 USD/month at 1,000 posts/day; it flips Ocharo's sources to `AiAllowed` | Developer (AI posture, #50; spend owner) |
| 7 | Prompt mechanics (child of 1, 5) | (a) compile once into editable chips · (b) judge every post · (c) hybrid: compile plus an opt-in check on matches | (a) now, (c)'s check later: what he described, previewable, no per-post cost | Developer |
| 8 | Where a per-subscription verdict lives (child of 7c) | (a) on the subscription's delivery event · (b) on the shared post (S16 as written) | (a): a shared post cannot hold one subscriber's verdict and kind | Orchestrator |
| 9 | Source scope (child of 1) | (a) group, source and section ids, exclude wins, following never starts harvesting · (b) source ids only · (c) following turns sections on | (a): matches #30's publisher groups; #44 keeps schedules with the operator | Orchestrator |
| 10 | Preview contract (child of 1, 7) | (a) 30-day count, per-chip and per-source counts, samples, near misses, coverage · (b) count only | (a): the near misses and coverage explain a surprising count | Orchestrator |
| 11 | Backfill on change (child of 1) | (a) same cursor; re-evaluate a window; `post.new` / `post.unmatched` · (b) future posts only · (c) a new subscription per edit | (a), default 30 days: consumers keep one cursor; needs E03 and E04 | Orchestrator |
| 12 | Delivery of posts awaiting AI tags (child of 5, 11) | (a) wait for the tagging pass (minutes), deliver on mapped tags after a timeout · (b) deliver on mapped tags at once, correct later | (a): avoids `post.new` → `post.unmatched` churn in Ocharo's list | Orchestrator |
| 13 | Migration from `ocharo-fashion-v1` (child of 1, 5) | (a) a transition selector with `rule`, a weekly shadow diff, then the switch · (b) replace at once | (a): no change in what Ocharo sees until the tags prove better; the developer gives the switch | Developer gives the switch gate |
| 14 | Events binding (child of 1, 13) | (a) one intake source per selector subscription; defaults move to the payload · (b) keep per-channel subscriptions, add discovery (E19, E20) | (a): removes the per-channel deploy entry without a discovery feature | Orchestrator |

---

## 4. Existing tasks this design supersedes or changes

| Task | Planned | Under this design | Verdict |
|---|---|---|---|
| S09 Let one subscription follow many sections | kind `sections`, join table, `PUT …/pipelines {add, remove}` | `selector` with `sources.include`; migration `010` becomes `010-subscription-selectors` | superseded |
| S16 Promote AI relevance into Ocharo's delivery | verdict written into the shared post; filter `ocharo-relevance-v1` | the switch from `rule` to tags (#2.9 step 4); a later opt-in check puts verdicts on events (#8) | superseded |
| E01 Pull all five Ocharo subscriptions into Events | three more `Sources:N` entries | one intake source on `ocharo-events` | superseded |
| E20 Discover intake subscriptions | poll-time discovery for 100 sources | not needed for one subscription per catalog; kept only if a tenant runs several | mostly superseded |
| S08 Golden pages carry the filter key | `filterKey` in `subscription.json` | the golden pages carry the selector subscription (`kind`, `selector`, version, transition `filterKey`) and the `match` and `source` payload fields | changed |
| S10 Ocharo filter regression set | expected verdicts of `ocharo-fashion-v1` per fixture | keep while `rule` lives; its fixtures and E02's negatives become the tagging eval set, with expected type and category per fixture | changed |
| S11 Publisher categories as source tags | `afisha:{category}` source tags; fashion evidence in the regex | keep the source tags; add the adapter's mapping to taxonomy `Tags` (tier `Rules`); drop the regex change | changed, first tag writer |
| S12 Pull lag | depends on S09 | unchanged; depends on the selector kind | dependency moves |
| S14 Embed the AI layer | — | unchanged; prerequisite of the AI tags | unchanged |
| S15 Relevance in shadow | `ocharo-relevance@1` Process stage per Afisha pipeline | the generic `post-tags` pass queued on post write; report = rule against tag selector | changed |
| S17 Estimated dates | from S15's relevance answer | from the tagging pass's answer | changed |
| S28 Section topics | `Topic` enum on sections | a taxonomy node per section: the lowest-precedence mapping and the console glyph | changed |
| S31 Client view, Following | follow and unfollow sections via `PUT …/pipelines` | Following becomes the selector editor: sources, chips, prompt box, preview | changed |
| E02 Tighten `ocharo-fashion-v1` | regex exclusions | a stopgap until the switch; its negatives become eval cases | changed, small |
| E03 Deliver `post.unmatched` | fix | required by backfill on edit and by the switch | prerequisite |
| E04 Hold unmatched events | fix | required by the switch | prerequisite |
| E12 Kind from the subscription | `DefaultKind` per source (uncommitted in events) | kind from the `type` format tag; `DefaultKind` only a fallback | changed |
| E19 List tenant subscriptions | `sourceName` and `country` in subscription context | the list read stays; `sourceName` and `country` move to per-post provenance | changed |
| A05 Relevance shadow (`ev-ai`) | `ocharo-relevance` on one Afisha pipeline | pilots `post-tags` first; `ocharo-relevance` becomes the opt-in check's prompt | changed |
| A07 Events takes AI classification | Events switches to `Classifier: payload` | Events stays on `filter` (the selector is the filter); `payload` only for the opt-in check | changed |
| Backlog "Tag and keyword subscriptions" | planned | becomes this feature; `keyword` dropped | rewritten |
| S18 Run the other Ocharo sources | per-channel subscriptions from setup | pipelines only; the sources join `ocharo-events` by group | changed, small |
