# T4 — Consumer needs and social integrations

*Last updated: 2026-10-26*

> What Ocharo (Events, Sourcing, Marketing), Haven, ListingShelf and the other ventures need from Harvest, then every
> place code or specs touch a social or messaging platform, with the evidence for P1. Three results: Haven's 48-field
> output holds 6 source-agnostic fields and 37 real-estate ones, so Harvest's own fields stay thin; ListingShelf
> already records deletions but Haven never receives them; Ocharo's automations discover unknown sources by search
> rather than monitor known ones. Credentials and sessions have no home in the Harvest spec or in any code, and
> the Telegram Bot API is called from five separate code paths.

Path aliases (`W` = `/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws`):

- `oc` = `W/workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws`
- `op` = `oc/workbench/ocharo-platform` · `om` = `oc/workbench/ocharo-marketing`
- `dk` = `op/engineering/codebase/brand-workspace.backend-services` (Desk backend)
- `mk` = `om/engineering/codebase/ocharo-marketing.backend-services` · `mkp` = `mk/OcharoMarketing.Infrastructure/Providers`
- `mft` = `/Users/max/Projects/10x-ws/workbench/fam/mft-10x-ws/context/domains/external/work` (Maftuna's private workspace, outside `W`)
- `hv` = `W/workbench/maxs-projects/ventures/saas/10x-ven-haven` · `hb` = `hv/engineering/codebase/haven.backend-services`
- `shelf` = `W/workbench/maxs-projects/ventures/saas/ventures.listing-shelf` · `lb` = `shelf/engineering/codebase/listing-shelf.backend-services`
- `be` = `W/workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src`
- `v` = `W/workbench/maxs-projects/ventures` · `st` = `/Users/max/.claude/scheduled-tasks`
- `hs` = `W/ideas/harvest-service-spec.md` · `es` = `W/ideas/events-service-spec.md`

Scope: what each product needs from Harvest. How or when Ocharo or Haven change is outside this track.

---

## 1 · Needs at a glance

| Need | Ocharo Events | Ocharo Sourcing | Haven | ListingShelf view |
|---|---|---|---|---|
| sources | Afisha, iticket, 9 reviewed links, organizer sites, Instagram + Telegram announcements, submitted links, typed entries | supplier catalogue pages, marketplaces (Made-in-China, Alibaba, OLX, AliExpress), signed-in RFQ inbox + Gmail | OLX, Domtut now; BirBir, Telegram groups, Instagram planned | whatever pipelines harvest; OLX + Domtut today |
| Harvest holds | title, text, URLs, dates as published with precision, place text, organizer, images, language, tags | title, price + currency, MOQ text, seller, URLs, images | 6 of 48 output fields, captures, source attributes verbatim | captures, content hash, page HTML, photos, absences |
| product breaks down | deadlines, offers, series/edition, certainty, scope, participation route | model, bed type, gauge, inclusions, delivered price, lead time, terms | 37 real-estate fields | stars, notes, views stay local |
| volume | tens a week after filters; whole-site raw volume not measured | tens of listings per query (36 in one ledger) | not measured; ~1,100 classified on one day (2026-03-04) | ≤ 2,000 per run |
| freshness | weekly discovery, daily register pass, daily near a deadline | weekly opportunities, monthly catalogues, RFQ inbox about daily | 15-minute intake per site | follows the pipeline |
| deletion / change | changed date, cancelled, closed call; a vanished page is only a hint | listing sold or removed, price change | listing gone from the source; none reaches Haven today | absence reports, "no longer listed since" |
| dedup | same event across Afisha, organizer, Instagram (entity level, Events' job); `/ru/` and `/uz/` path variants (post level, twins unverified) | same offer under several listing URLs (post level) | same flat on OLX + Telegram; none exists today | one row per listing |
| media | event posters by reference into File Storage | supplier photos, PDFs, videos; private | photos posted to Telegram; provider URLs rot | photo copies by hash, 90-day retention |
| visibility | public pool for harvested sites; private container for submitted links; catalog private (EV1) | private: contacts, quotes, inbox | public sources; corrections and stages are Haven's | personal archive, no auth today |
| who submits | Desk owner + editor (`CanEdit`); viewer reads | same | agent / admin / service | single user |
| subscription | channels for sites; tags for organizer posts | keywords on marketplaces; channels for 2 catalogues | channels per site; tags for mixed Telegram groups | channels |

- Ocharo Marketing has no harvest need in its docs (§ 4).
- Cells quote evidence in §§ 2–6; "not measured" means no figure found in docs or code.

---

## 2 · Ocharo Desk Events

### Sources and forms

The register = `mft/career/car-events*.md` (five files, 1,848 lines); link counts below are occurrences of the host name in them.

| Source | Evidence | Form |
|---|---|---|
| Afisha (`afisha.uz`) | 35 links in the five-file register; first on the spec's list (`es:171`) | whole site |
| ANONS (`anons.uz`) | 32 links; fairs and markets (`mft/career/car-events-markets.md`) | whole site |
| iticket (`iticket.uz`) | 0 links in the register; one venue page in `mft/ventures/ocharo/och-shoot-2026-09.md:62`; named by the developer, no Ocharo requirement text found | whole site |
| nine reviewed links | `op/engineering/codebase/brand-workspace.frontend-services/apps/web/src/domain/workspace/SourceDirectory.ts:3-19`: 3 events, 4 both, 2 sourcing | page captures |
| organizer sites and channels | 151 event families (`mft/career/car-events.md:374`); 17 Instagram and 11 `t.me` links in the register | page, Instagram, Telegram |
| submitted link | not built; Desk research plans "reviewed link and evidence upload" → bounded fetcher (`op/engineering/research/desk/2026-10-09-sourcing-events-integrations.md:120`) | any |
| typed entry | built: `POST …/events`, writes need `CanEdit` (`op/engineering/architecture/events-contract.md:47`) | manual |

- Afisha URLs carry `/{ru|uz}/{fashion|exhibitions|gorod}/YYYY/MM/DD/slug` (`car-events-fashion.md:22,100`, `car-events-markets.md:67`).
- Dated Afisha pages loaded while category snapshots could be stale (`car-events.md:461`).
- Afisha tags can omit every fashion term: the ICHKARI exhibition carried only `ichkari` and `выставка` and keyword discovery missed it (`car-events.md:462`). Whole-site harvest then filter fits.
- Instagram and Telegram: `@fwtashkent` is the only channel of Visa Fashion Week Tashkent (`mft/ventures/ocharo/och-channels.md:181`).
- Direct Instagram or Telegram retrieval failed in four monitoring passes (`car-events.md:393,450,461,482`); indexed copies served instead.
- `t.me/s/{name}` renders a public channel without login (`och-channels.md:87`) and the register already links it (`car-events-markets.md:191`).
- Desk research rules arbitrary Telegram channel monitoring "unsupported" for a bot (`…integrations.md:116`); organizer channels give the bot no admin rights, so a bot-only path misses them.

### Today's automations that Harvest replaces

- Weekly task `st/ocharo-weekly-events-scan/SKILL.md`: WebSearch + WebFetch, bundle, validator, import as `candidate`; enabled, Mondays 09:11 (task list 2026-10-26).
- Its output on disk (`mft/ventures/ocharo/research/assets/och-events/desk-import/`): `2026-10-08` seed of 41 events; `2026-10-13` seven candidates from seven different hosts, six international, none from Afisha; no folder for 10-20 or 10-26 (cause not checked).
- Its path `P` points at `W/workbench/ocharo-hq/…`, which does not exist; the real root is `W/workbench/mfts-projects/ventures/ocharo-hq/…`.
- A second automation, `morning-fashion-and-craft-event-check`, runs daily 09:00 Asia/Samarkand and edits the register (`car-events.md:362`). Each pass runs "two searches": changes to known families, plus broad discovery for new names in Uzbek, Russian and English (`:358`).
- New families per pass: 7 on 16 Oct (`:447`), 6 on 15 Oct (`:456`), 3 on 26 Oct (`:374`).
- Both automations are search-driven discovery. Harvest as scoped monitors known sources.

### Needs

- **Fields.** Harvest holds title, text, URLs, publish date, event dates **as published with precision**, place text, organizer, images, language, tags. Ocharo's rule is "September is not 1 September" (`car-events.md:340`); a base field that defaults a month to the 1st forces every consumer to repeat the lie (Desk stores month → 1st plus `datePrecision`, `events-contract.md:32`).
- **Product-side breakdown.** Deadlines, offers, series and edition, `certainty: estimated` (predicted from earlier editions), derived `scope`, participation route (`es:61-109`).
- **Freshness.** Weekly for opportunities, daily near a known deadline (`…integrations.md:82`); reminders at 30/14/7/2 days (`car-events.md:364`). A pipeline's cadence must tighten as a date nears.
- **Failed access is "unchecked", never "no new events"** (`car-events.md:364`); matches `hs:65-69` (blocks are outcomes).
- **Change, not only new.** Desk's import skips an existing key and never updates it (`dk/BrandWorkspace.Infrastructure/Events/Services/EventImportService.cs:31-35`); a moved or cancelled event reaches Ocharo only as a delivered change. The record holds one `sourceUrl` (`dk/BrandWorkspace.Domain/Events/Models/EventModels.cs:21`), so provenance of many sources lives in Events (`es:71`).
- **Deletion.** A page that disappears is not a cancellation; cancellation is text (`es:61`). Harvest reports `gone` as a hint and `changed` with the diff.
- **Dedup.** Two levels: post (same page across crawls, `/ru/` and `/uz/` path variants; whether one post has twins in both languages is not verified) belongs to Harvest; entity (many posts, one event) belongs to Events' ladder (external id, key, fuzzy title + dates + city, `es:157`) with a human merge (`…integrations.md:70`). Register rule: never merge distinct platforms that share a name (`car-events.md:344`).
- **Media.** Poster by reference into the shared File Storage instance; the reference keeps the file after pruning (`es:190-199`).
- **Visibility.** Two layers: Harvest container (public pool vs Ocharo's private container) and Events catalog visibility (`private` until EV1, `es:165`). A product-submitted link on an unharvested domain goes private; the developer's rule needs a domain check against public pipelines.
- **Who is the Harvest tenant.** Events registers pipelines and receives deliveries (`es:151-155`, `es:126`); Ocharo calls Events, not Harvest. The "Ocharo private container" is therefore the Events catalog `ocharo-fashion` (`es:165`), not an Ocharo tenant.
- **Roles.** Desk roles `owner` · `editor` · `viewer` ([Identity accounts](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.identity/blob/main/product/features/accounts.md)); the app enforces membership before calling the service (`es:130-131`). Harvest sees a service key plus an actor id.

---

## 3 · Ocharo Desk Sourcing

- Scope: supplier discovery and quote monitoring (E2 in `oc/docs/app-boundaries.md` is open; Sourcing stays in Desk until decided).
- **Discovery sources.** Two catalogue pages (`SourceDirectory.ts`, area `sourcing`: P L Industries / KRITI, Lucky Enterprises); marketplace searches in one ledger `oc/tasks/waistband-machine-sourcing/waistband-machine-sourcing.md`: 36 listings across Made-in-China (8), Alibaba (16), AliExpress (6), OLX + Prom.uz (5), shop (1); supplier Instagram posts (`oc/tasks/shawl-sourcing/shawl-sourcing.md:106`).
- **Search terms**: five per query across English, Russian and Uzbek (ledger "Search terms"). OLX is both a Haven source and an Ocharo Sourcing source with a different category, so keyword subscriptions read only what some pipeline harvests (§ 5 note).
- **Quote monitoring is a signed-in source.** `st/ocharo-waistband-rfq-check/SKILL.md` steps 1–2 read the Alibaba RFQ comparison page and message center in a signed-in browser, then Gmail with `(from:alibaba.com OR from:made-in-china.com) newer_than:2d …`. The task file exists; it is not in the scheduled-task list of 2026-10-26.
- The spec has no credential or session concept (grep of `hs`: none); this source family needs a consumer-owned login that never enters the shared pool.
- **Fields.** Harvest holds title, price + currency, MOQ text, seller, URL, images, capture dates. Sourcing breaks down model, bed type, gauge, inclusions, delivered-Tashkent price, lead time, payment terms (`SKILL.md` step 3). Offer rules (unit, quantity break, FX snapshot, validity) are Sourcing's (`…integrations.md` "An offer needs").
- **Prices arrive in mixed currencies** (Alibaba UZS with USD tiers; OLX UZS; Made-in-China USD ranges); conversion at a dated CBU rate is Sourcing's job (ledger header).
- **Dedup, post level.** One factory lists the same machine under several URLs: `M3` and `M4` duplicate `M1` (ledger rows). Harvest dedup of the same offer inside a source is useful; cross-supplier "same machine" is Sourcing's.
- **Deletion and change.** A sold or removed listing, a price change (`O1` $730 benchmark). Checks: monthly for catalogues (`…integrations.md:82`).
- **Media.** Photos, PDFs, videos stay content-addressed in Desk: SHA-256 plus a 64-bit perceptual hash, near-duplicates at ≤ 6 bits (`op/engineering/architecture/sourcing-contract.md:38-40`). Reusable for post-level image dedup (T5).
- **Visibility.** Private. "Bundles contain private contact data" (`sourcing-contract.md:145`); the RFQ inbox, supplier replies and WhatsApp screenshots never enter a pool. Public catalogue pages could.
- **Roles.** Same as Events (`CanEdit`).
- **Subscription.** Keywords over marketplaces; channels for the two catalogue pages; the inbox is a private credentialed source.

---

## 4 · Ocharo Marketing

- No watch or listening need found. The research states the "scanning" feature "does not promise social-account scraping or competitor monitoring" (`om/engineering/research/operator-experience.md:102`) and the product never shows invented reach or trends (`om/product/product.md:33`).
- It needs publishing and own-post metrics, which are write-side (Part B): Telegram, Instagram, X, WhatsApp brokers (`om/product/product.md:29`).
- It reads Events by reference for campaigns (`events-contract.md` Increment), not Harvest.
- Harvest relevance is indirect: Marketing's brokers are the nearest working code for Harvest's social adapters (§ 9).

---

## 5 · Haven

### Intake today

- Sources: channels `olx-uz` and `domtut-uz` (`hb/Haven.Database/Haven.Database.Persistence/Seeds/001-channels.json`), mapped from ListingShelf providers (`hb/Haven.Supply/Haven.Supply.Api/appsettings.json:19-25`).
- Cadence: `sup-intake-olx` and `sup-intake-domtut`, cron `*/15 * * * *`, batch 200 (`hb/…/Seeds/002-pipelines.json:10-17,23-30`); classification `*/5`, batch 20 (`:36-43`).
- Volume: not measured in docs. Data points: 1,416 OLX listings in the February 2026 dataset (`hv/engineering/research/classification/olx-listing-data-report.md:3`); about 1,100 classified on 2026-03-04, before the rebuild (`…/ai-cost-analysis.md:63-66`). Batch sizes above are configuration, not measurements.
- Mechanism: reads the 200 newest ListingShelf runs, takes finished ones per provider, remembers the last 1,000 run ids (`hb/Haven.Supply/Haven.Supply.Infrastructure/Intake/Settings/ListingShelfSettings.cs:17,21`; `Intake/Pipelines/ListingIntakePipeline.cs:43-52`). It reads `GET api/runs/{id}/export` only (`Intake/Brokers/ListingShelfBroker.cs:30`).
- Snapshot fields consumed, all text: `sourceUrl`, `title`, `description`, `priceText`, `location`, `postedAtText`, `sellerName`, `imageUrls`, `attributes` (`ListingShelfBroker.cs:63-76`). Location splits at the first comma into region and subregion (`hb/Haven.Supply/Haven.Supply.Persistence/Intake/Repositories/ExternalListingRepository.cs:81-91`).
- Identity: `(provider, external_id)` unique (`hb/…/Migrations/002-external-listings/Apply.sql:58`); newest snapshot per listing wins (`ExternalListingRepository.cs:17-21`).
- Planned: BirBir, Telegram groups, Instagram "through ListingShelf" (`hv/engineering/planning/backlog.md:46,71`; `hv/product/product.md:199`).
- ListingShelf's charter excludes social media (`shelf/CLAUDE.md:3`, `shelf/product/product.md:13`); the planned sources only fit a widened service, which is Harvest.

### The 48-field output

`hb/Haven.Supply/Haven.Supply.Infrastructure/Classification/Models/ClassificationOutputSchema.cs:10-151`.

| Group | Fields | Count | Owner |
|---|---|---|---|
| source-agnostic | `ExternalListingId` (post ref), `AuthorName`, `PhoneNumbers`, `PostedAt`, `PriceAmount`, `PriceCurrency` | 6 | Harvest can hold |
| borderline | `PricePeriod`, `PriceIsNegotiable`, `IsUrgent`, `InvalidReason` (relevance verdict), `LocationSignals` (raw mention text is generic; landmark and district resolution is Haven's Location service) | 5 | Harvest holds a generic form (`per` unit, negotiable flag, in/out of scope, location text) |
| property | `PropertyType`, `BuildingType`, `YearBuilt`, `YearBuiltEnd`, `Floor`, `TotalFloors`, `Rooms`, `Layout`, three areas, `CeilingHeightM`, `BathroomsCount`, `BathroomType`, `Renovation`, `IsFurnished`, two amenity lists | 18 | Haven |
| rent terms | `CommissionType/Amount/Currency`, `DepositType/Amount/Currency`, `PrepaidMonths`, `UtilitiesIncluded`, `AcceptedTenants`, `ExcludedTenants` | 10 | Haven |
| seller reading | `ContactType` + confidence + signals, `IsRealtorsNotAllowed`, `AuthorRegisteredAt` | 5 | Haven |
| deal reading | `ListingType` + confidence + signals | 3 | Haven |
| quality | `DataQualityFlags` | 1 | Haven |

- 6 + 5 + 37 = 48. Harvest's base set stays small; Haven's vertical schema sits above it (`wow2.listing.v1` in `hs:44` is a consumer schema, not the base).
- Price is deterministic in most cases: 97% of 1,416 OLX listings read `NUMBER у.е.` (`hv/engineering/research/classification/olx-listing-data-report.md:3,480`). A deterministic base parse removes tokens from Haven's prompt.
- Haven's LLM cost ~$0.022 per listing (March 2026 audit, `…/ai-cost-analysis.md:53`; Anthropic first, OpenAI fallback, `hv/engineering/architecture/architecture.md:43`). A second Harvest LLM pass over the same text would add cost; Haven's pipelines want captures + deterministic fields, AI off.

### Phones

- ListingShelf's listing schema 1.0 has no phone field (`shelf/engineering/architecture/pipeline-contract.md:15`); Haven inserts an empty phone array (`ExternalListingRepository.cs:50`). Numbers come only from description text via the model (`ClassificationOutputSchema.cs:85`).
- Haven uses the last nine digits as the comparison key (`hb/…/Migrations/008-listing-phones/Apply.sql:6-9,24-26`) and flags a number on ≥ 3 listings as a realtor (`hb/…/Classification/Settings/ClassificationSettings.cs:45`; `SharedPhoneFlagger.cs:36`).
- Phone coverage is not measured. The same key is the natural cross-source dedup signal (OLX vs Telegram).

### Deletion

- ListingShelf records absences (`shelf/engineering/architecture/architecture.md:28,47,55`) and exposes them (`pipeline-contract.md:18,37`). The run export Haven reads carries snapshots only (`lb/ListingShelf.Api/Runs/Extensions/RunExportModelExtensions.cs:30`; `hb/…/Intake/Contracts/ListingShelfRunExportContract.cs:3-5`).
- Haven sets `external_status = 'active'` on every upsert (`ExternalListingRepository.cs:68`); nothing in the code writes `'deleted'` (grep of `*.cs`, `*.sql`; enum at `001-baseline/Apply.sql:12`). The old status check is retired (`hv/engineering/planning/backlog.md:69`).
- OLX removal detection is itself unconfirmed: a made-up ID answers 404/410, a real removed ad was not seen (`shelf/engineering/planning/backlog.md:49`).
- Need: per source link a state (`live` · `gone` · `relisted`, with "since"), delivered as events; a canonical post is gone only when every linked source is. Rentals go stale fast; at least daily for listings still in an active stage is the working assumption, not a measured figure.

### Dedup

- None across sources. Cross-posting and owner-plus-realtor duplicates are deferred in Haven's backlog (`hv/engineering/research/classification/standard-listings-optimization.md:314-318`).
- Signals on hand: phone key, price, rooms, area, floor, location signals, photo perceptual hash.
- "One improved post with every source linked": Haven would show all links, classify once per canonical post, and mark the flat gone only when all links are gone.

### Media, visibility, roles, subscription

- Photos are provider URLs handed to Telegram (`hb/Haven.Supply/Haven.Supply.Infrastructure/Notifications/Brokers/TelegramGroupBroker.cs:26,57`); ListingShelf's photo copies are opt-in per pipeline (`architecture.md:64`). Harvest media in File Storage gives stable URLs.
- Visibility: OLX, Domtut, BirBir, public Telegram groups are public. Corrections, stages and notes are Haven's. Phones and names from public posts raise a pool-exposure question (Points).
- Roles: `agent`, `admin`, `service` (`hv/engineering/architecture/architecture.md:11`). Owner self-submission is a Google Form on Haven's side (`hv/engineering/planning/backlog.md:144`), not a Harvest need.
- Subscription: channels per site now; dedicated housing groups fit a channel, mixed groups fit a tag subscription (`real-estate`, `rent`, Tashkent).
- Pool note: Haven's OLX pipeline is a filtered Tashkent real-estate pipeline. A keyword subscription for an OLX machine would read nothing from it (§ 3).

---

## 6 · ListingShelf as a consumer view

- Today: a personal archive; no authentication, loopback only (`shelf/engineering/architecture/architecture.md:81`); social feeds out of scope (`shelf/product/product.md:13`); no AI in the capture path (`product.md:12`).
- The view reads: latest capture per listing within a filter; capture history with content-hash diffs; per-run change tags `new` · `changed` · `unchanged` · `gone`; "no longer listed since" from absences (`architecture.md:51,55`); photo copies by hash, up to 12 per capture, older captures drop theirs after 90 days (`:64`); JSON schema 2.0 and CSV exports, ≤ 5,000 (`pipeline-contract.md` Exports).
- It keeps locally, never in Harvest: stars and notes (`listing_notes`), saved shelf views, compare.
- Limits per run: 1–100 pages, 1–2,000 listings (`architecture.md:75`).
- Needs from Harvest: immutable dated captures with hash, absences as immutable reports, per-capture photo references, change tags per run, API with authentication (the view becomes a client with a key).
- One decision: the view's row is `(provider, externalId)` today; Harvest's canonical post may hold several source links, so the view chooses a row per link or per post.
- Run exports saved beside the archive after each run already serve as a delivery (`architecture.md:46`).

---

## 7 · Other products

| Product | Would subscribe to | Form | Evidence | Fit |
|---|---|---|---|---|
| Events service | every Ocharo and shared catalog source | channel pipelines; deliveries to `POST /harvest/items` | `es:126,145-159` | first consumer |
| ActivityMatcher | iticket theatres (v2 booking link); Afisha as event listing | channel | `W/ideas/activity-matcher-spec.md:68,165,167`; spec dated 2026-04-20, data is a static catalogue | weak, unbuilt |
| fin-nt (NT auction tracker) | e-auksion.uz lots: provider API, 30-minute scrape, 6-hour status updater | channel + deletion/status check | `v/labs/10x-fin-nt/platform/planning/platform-planning.md:89-108,203` (541 lots scraped) | strong; plans its own `BackgroundService`s |
| Sift | YouTube channels it curates | channel; ingest on user action, never on a timer | `v/saas/sift/product/context.md:25`; Data API behind `IYouTubeClient` (`engineering/engineering.md:13`) | fits T2; timing rule conflicts with a scheduled harvester |
| TranscriptForge | new uploads per channel ("auto-process new uploads") | channel | `v/saas/10x-ventures-transcript-forge/product/product.md:32`; legality (OAuth vs scraping) open, `product/context.md:56` | fits T2; channel automation sits in a separate app (`product/research/app-family.md:15,37`) |
| PoseCoach | TikTok/Reels pose trends by hashtag | tag | `v/consumer/ventures.pose-coach/engineering/research/pose-coach-spec.md:53,64`; scraping deferred, rights concern (`ai-photo-director-market-analysis.md:256,394`) | deferred |
| Trademark Watcher | USPTO ODP and EUIPO filings by keyword | provider API + keyword | `v/saas/trademark-watcher-poc/README.md` "Data sources" | weak: filings, not posts |

- Skipped, no plausible need found: Matinee (no scraper by decision, `v/consumer/ventures.matinee/CLAUDE.md:37`), Museums Gallery, TNIS (ingests static datasets), Unpause, Fun Vault and Hijinx (hand-curated), Arcade, ForeverPin, Whiteout, PRISM, Surface Pattern, City Vision, first-ten pilots.

---

## 8 · Social-integration inventory

Direction: **read** · **write** · **auth** · **notify**. State: built · built, no live use found · fixtures · decided · spec · planned.

### Ocharo

| # | Platform | Direction | Credential | Product | Path | State |
|---|---|---|---|---|---|---|
| O1 | Telegram | write: channel text or photo | bot token + destination chat id | Marketing | `mkp/Brokers/TelegramSocialPublishingBroker.cs:44-45`; `mkp/TelegramProviderOptions.cs:6-9` | built; no live use found: delivery "manual in this pilot" (`mk/OcharoMarketing.Infrastructure/Marketing/Services/ExternalMarketingService.cs:19-22`), research states no live calls (`om/engineering/research/providers.md:3`) |
| O2 | Telegram | read: verify bot, chat, membership | bot token | Marketing | `mkp/Brokers/TelegramAccountVerificationBroker.cs:25-26,38,54` | built |
| O3 | Instagram | write: image container → publish | OAuth user token (Instagram Login) or page-linked token (Facebook Login) | Marketing | `mkp/Brokers/InstagramSocialPublishingBroker.cs:29,34,64`; `mkp/InstagramProviderOptions.cs:6-9` | built; no live use found |
| O4 | X | write: media upload + post | OAuth 2.0 user token | Marketing | `mkp/Brokers/XSocialPublishingBroker.cs:55,94` | built; no live use found |
| O5 | X | read: public post counters, billable | same token + `EnableMetricReads` | Marketing | `mkp/Brokers/XSocialMetricsBroker.cs:37-38`; `mkp/XProviderOptions.cs:3-9` | built; no live use found |
| O6 | X | read: account check, receipt lookup | same token | Marketing | `mkp/Brokers/XAccountVerificationBroker.cs:20`; `mkp/Brokers/XReceiptReconciliationBroker.cs:28-29` | built; no live use found |
| O7 | WhatsApp Cloud API | write: template or service-window message | system-user token + phone-number id | Marketing | `mkp/Brokers/WhatsAppSocialPublishingBroker.cs:61-62`; `mkp/WhatsAppProviderOptions.cs:5-9` | built; no live use found |
| O8 | Telegram | auth + notify: link, sign-in code, webhook, polling | bot token + webhook secret | Desk | `dk/BrandWorkspace.Api/Identity/Telegram/TelegramAuthSettings.cs:9`, `TelegramPollingService.cs:15`, `TelegramAuthEndpoints.cs:140` | built |
| O9 | Gmail, Alibaba, Made-in-China, WhatsApp, OLX chats | read: supplier replies and quotes | Gmail connector (OAuth user); signed-in browser session | Sourcing | `st/ocharo-waistband-rfq-check/SKILL.md` steps 1–2; planned connector `op/engineering/research/desk/2026-10-09-sourcing-events-integrations.md:115` | manual / task file |
| O10 | Telegram channels, Instagram | read: organizer announcements | bot in permitted channels; Instagram professional-account API | Events | `…integrations.md:116-117` | planned |

### Haven

| # | Platform | Direction | Credential | Product | Path | State |
|---|---|---|---|---|---|---|
| H1 | Telegram | write: forum-group topic posts, albums, topic create | bot token + chat id | Supply | `hb/Haven.Supply/Haven.Supply.Infrastructure/Notifications/Brokers/TelegramGroupBroker.cs:17,26,57`; host `Haven.Supply.Api/Configurations/HostConfiguration.Extensions.cs:76-77,167,175` | built |
| H2 | Telegram | auth + notify: sign-in code, webhook | bot token + webhook secret | Auth | `hb/Haven.Auth/Haven.Auth.Api/Telegram/Controllers/TelegramController.cs:15-17`; `HostConfiguration.Extensions.cs:39-42` | built |
| H3 | BirBir, Telegram groups, Instagram | read | not chosen | Supply | `hv/engineering/planning/backlog.md:71` | planned |

- H1 and H2 read the same env name `TELEGRAM_BOT_TOKEN` in two services (`HostConfiguration.Extensions.cs:39` in Auth, `:76` in Supply).
- The backlog lists daily posts to `@Ijara_tashkent_kvartira`, OLX cross-posts and Telegram-group posts as product tasks (`hv/engineering/planning/backlog.md:179-181`); no OLX or Instagram code exists.

### Other products and the SDK

| # | Platform | Direction | Credential | Product | Path | State |
|---|---|---|---|---|---|---|
| X1 | Telegram Mini App | auth: `initData` HMAC | bot token as HMAC key | Arcade | `v/consumer/ventures.arcade/engineering/codebase/arcade.backend-services/Arcade.Infrastructure/Telegram/Services/TelegramInitDataValidator.cs:13-14,62` | built |
| X2 | YouTube Data API v3 | read: channel uploads | API key | Sift | `v/saas/sift/engineering/codebase/sift.backend-services/Sift.Infrastructure/Videos/Ingesting/YouTube/YouTubeOptions.cs:11-20` | fixtures; live check waits on a key (`sift/product/context.md:9-10`) |
| X3 | YouTube | read: captions, audio, metadata | none (`yt-dlp`) | TranscriptForge | `v/saas/10x-ventures-transcript-forge/engineering/codebase/transcript-forge.backend-services/TranscriptForge.Infrastructure/Videos/Core/Brokers/YtDlpVideoMetadataBroker.cs` | built |
| X4 | GitHub | auth | OAuth client | Wheelhouse | `W/workbench/wow-two-platform/wow-two-platform.wheelhouse/engineering/codebase/wheelhouse.backend-services/Wheelhouse.Api/Auth/AuthConfigurationExtensions.cs:66` | built |
| X5 | Google | auth: ID token | client id, no secret | ForeverPin | `v/saas/10x-venture-forever-pin/engineering/codebase/forever-pin.backend-services/ForeverPin.Api/Configurations/HostConfiguration.Extensions.cs:166` | built |
| X6 | Telegram | notify: alerts and deploy outcomes | bot token | Wheelhouse | `W/workbench/wow-two-platform/wow-two-platform.wheelhouse/engineering/research/feature-completeness.md:261`; SDK sender missing, `:219,269` | decided; no Telegram code found in the repo (grep of `*.py`, `*.cs`, `*.yml`) |
| X7 | Telegram | notify: issue alerts | bot token | Feedbacks | `W/ideas/feedbacks-spec.md:46` "reuse the comms Telegram slice" | spec; slice does not exist (`feature-completeness.md:219`) |
| S1 | Telegram | notify: OTP | bot token via a consumer-registered `ITelegramBotClient` | be sdk | `be/Identity/Otp/Telegram/TelegramOtpDeliveryHandler.cs:9-25` | built |
| S2 | Telegram Gateway | notify: OTP | Gateway API token | be sdk | `be/Identity/Otp/TelegramGateway/TelegramGatewayOtpOptions.cs:11` | built; paid in TON, deferred ([identity T1](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.identity/blob/main/engineering/research/identity-analysis-2026-10/t1-integrations.md) § 3) |
| S3 | Telegram | read: webhook validation | secret token | be sdk | `be/Messaging/Webhooks/Inbound/Validators/TelegramWebhookSignatureValidator.cs:12-25` | built |
| S4 | WhatsApp Cloud API | notify: OTP and messages | system-user token + phone-number id | be sdk | `be/Comms/WhatsApp/Meta/MetaWhatsAppOptions.cs:6-16`; `be/Identity/Otp/WhatsApp/` | built |
| S5 | 17 OAuth providers | auth | client id + secret; user tokens kept in cookie auth properties (`SaveTokens`) | be sdk | `be/Identity/OAuth/oauth.md:30-36` | built; only X4 and X5 have consumers |
| S6 | Log in with Telegram (OIDC), 17 providers via Identity | auth | bot client id + secret | Identity | [Identity sign-in methods](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.identity/blob/main/product/features/sign-in-methods.md) | planned (I20, P2) |
| S7 | Platform link parsing | read helper | none | be sdk | `be/Media/YouTube/YouTubeUrlMapper.cs`, `YouTubeLinkExtractor.cs` | built, YouTube only |
| M1 | Telegram user account | read: channels and groups | MTProto session | Harvest (T1 decides) | none: no MTProto client, library or spec in `W` (grep `mtproto`, `WTelegram`, `TdLib`, `Telethon`, `Pyrogram`) | not found |

- The be sdk `Comms/` holds Email, Sms, Push and WhatsApp; no Telegram sender (`feature-completeness.md:219`; `be/Comms/` listing).
- The Telegram Bot API is called from five C# code paths: O1 (raw HTTP), H1, H2, O8 and S1 (the last four on `Telegram.Bot`). X6 and X7 plan two more consumers of a sender that does not exist.
- Account verification exists only as Marketing's O2 and O6; Identity's contact-sharing check is I20, unbuilt ([identity T1](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.identity/blob/main/engineering/research/identity-analysis-2026-10/t1-integrations.md) § 3).
- No platform has a durable per-account token store: Marketing reads one account per provider from configuration (`mk/OcharoMarketing.Api/Configurations/HostConfiguration.Extensions.cs:214,229,248,259`; `ExternalMarketingService.cs:19-22`); the SDK keeps OAuth tokens in the cookie.

---

## 9 · P1 evidence: connectors beside Harvest, or one repo

### Genuinely shared across read and write

| Shared | Why | Evidence |
|---|---|---|
| connected accounts | tokens, ids, verification state, revision; Harvest reads need the same record for any platform that wants a token or session (Telegram user session, Instagram Graph, X, Reddit) | Marketing keeps verification evidence apart from secrets and binds it to a config stamp (`mk/OcharoMarketing.Domain/Marketing/Entities/DeliveryConnectionRecord.cs:3-4`; `mk/OcharoMarketing.Persistence/Marketing/Repositories/DeliveryRepository.cs:69`); no store exists elsewhere |
| token lifecycle | refresh, expiry, revocation | X needs `offline.access` (`om/engineering/research/providers.md:112`); Instagram access gated (`providers.md` Instagram section) |
| rate limits and budgets | one quota per app or account across publish, metrics and harvest reads | X pay-per-use credits cover posting and billable metric reads (`providers.md:112`; `mkp/XProviderOptions.cs:3`); Telegram ~30 msg/s overall, ~1 msg/s per chat ([identity T1](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.identity/blob/main/engineering/research/identity-analysis-2026-10/t1-integrations.md) § 3); Harvest requires per-source limits and backoff (`hs:67-68`) |
| platform clients | typed calls, id handling, bounded bodies, error → outcome | `mkp/ProviderHttpTransport.cs:34-36` maps outcomes; X metrics maps 401/403/429/404 (`mkp/Brokers/XSocialMetricsBroker.cs:41-45`) |
| media in and out | Instagram needs a public image URL; Telegram takes file, URL or `file_id`; Harvest stores media in File Storage | `providers.md` Instagram and Telegram sections; `hs:58-61`; `TelegramGroupBroker.cs:57` |
| inbound webhooks | Telegram updates with `secret_token` | `be/Messaging/Webhooks/Inbound/Validators/TelegramWebhookSignatureValidator.cs`; Auth bots (H2, O8) |
| URL parsing | submitted links and receipt links need canonical forms (`t.me`, `instagram.com/p/`, `x.com/…/status/`) | `be/Media/YouTube/YouTubeUrlMapper.cs`; Telegram receipts give stable links (`providers.md` Telegram section) |
| account verification | "is the bot still an admin, is the session alive" before a run | O2, O6 |

### Not shared

- Web pages, browser capture, provider APIs (e-auksion, USPTO), RSS/ICS feeds and manual entry have no social account.
- Many social reads need no account: public `t.me/s/{name}` (`och-channels.md:87`), a YouTube API key (X2).
- Policy differs by direction. Marketing forbids automatic side-effect retries and returns `Ambiguous` for reconcile (`ProviderHttpTransport.cs:34-36`); Haven waits out one rate limit and recreates a deleted topic once (`TelegramGroupBroker.cs:16`); ListingShelf retries twice paced 500 ms (`shelf/engineering/architecture/architecture.md:75`). A shared client exposes calls and outcomes; the caller picks the policy.
- Publishing-only: approvals, scheduling, receipts, reconciliation, own-post metrics. Harvest-only: captures, dedup, deletion checks, extraction, pipelines, schedules, deliveries, containers.
- Identity's OAuth identifies a person; a connected account acts for an organization's account. Keep sign-in separate.

### Weighing

| Option | For | Against |
|---|---|---|
| one social-media repo holds Harvest | one release line; social adapters beside their clients | Harvest has non-social consumers and sources (Afisha, e-auksion, feeds); a "social" repo owns them wrongly; connectors wait on Harvest's cadence |
| connectors domain beside Harvest | fits [capability forms](../../conventions/development/capability-forms.md): it owns secrets and state and serves two or more products (Marketing, Haven, Wheelhouse, Feedbacks, Harvest); Harvest stays platform-neutral; five Telegram paths collapse to one client | two repos and one more contract to version; the second consumer of connected accounts is Harvest, not yet built |
| clients only in core, accounts in Harvest | cheapest | publishing would need Harvest to hold its tokens |

- Provisional pick: **two domains**. A social connectors domain holds platform clients (read and write brokers per platform), connected accounts and sessions, limits, verification, publishing and metrics brokers; Harvest's social adapters call its read brokers and never hold a token. Connectors never depend on Harvest. Approvals and scheduling stay in the products.
- Notifications (#10 in `W/docs/platform-apps.md`) needs the same Telegram sender; it should consume the connectors' client, not add a sixth.
- Public-read adapters (`t.me/s`, API-key reads) need no connected account, so the split does not block them; T1 and T2 confirm per platform. T8 decides placement.

---

## 10 · Not found

- iticket as an Ocharo requirement (only the developer's naming and ActivityMatcher's v2 note).
- Afisha, iticket or ANONS posts per day. T3 profiles Afisha's sitemap index (5,358 child files, 18 changed since 2026-10-19, `t3-web-sources.md:124`); that counts files, not posts.
- Haven listings per day; phone coverage after the move to ListingShelf snapshots.
- Any Marketing watch or listening requirement.
- A Telegram sender in the be sdk; a durable per-account token store anywhere.
- Credentials, sessions, containers, roles or subscriptions in `hs` (grep: only the word "subscribes", `hs:17`).
- Code that writes `external_status = 'deleted'` in Haven.

---

## Findings that change the spec

1. **A base post schema must exist beside consumer schemas.** `hs:5-6,49-52` extracts into "a schema the consumer names"; the 2026-10-26 decisions have Harvest hold high-level fields and run AI optionally. Haven's output is 6 generic / 5 borderline / 37 vertical fields. Harvest needs its own small base (title, text, URLs, publish date, event or offer dates with precision, price amount + currency + per-unit, author, contact points, location text, language, tags, media, source attributes verbatim) filled deterministically where possible; consumer schemas (`wow2.listing.v1`, `wow2.event.v1`) are an optional second pass.
2. **Source state is a delivery event.** ListingShelf records absences, Haven never receives them, and `external_status` is `active` forever. The spec lists `gone` as change detection (`hs:39`) but not as something a consumer receives. Add per source link `live` · `gone` · `relisted` with "since", and a canonical post gone only when all links are.
3. **Search-driven discovery is a source family the spec lacks.** Both Ocharo automations discover by search (seven candidates from seven hosts, none Afisha). Known-source monitoring replaces the register pass; discovery needs a `search` adapter or stays outside Harvest.
4. **Consumer-owned credentials and sessions are missing from the spec.** Quote monitoring is a signed-in browser plus Gmail; social reads may need a token or session. A pipeline needs a reference to a connection the consumer owns, valid only in that consumer's private container. This is the same record P1's connectors domain would hold.
5. **The tenant and the container need defining.** Ocharo's events container is the Events catalog `ocharo-fashion`; Events is the Harvest consumer. Link intake needs a domain check against public pipelines, and keyword subscriptions read only what pipelines harvest (Haven's filtered OLX pipeline holds no machines).
6. Post-level dedup (same page, language twins, same offer under several URLs) is Harvest's; entity-level dedup (many posts, one event; one flat across phone and price) stays with the consumer's matching. Reusable: Haven's phone key, Desk's SHA-256 + 64-bit perceptual hash.
7. Phones are text-only today. Harvest must say whether it extracts contact points, and whether they enter the shared pool.
8. Haven's planned Telegram, Instagram and BirBir sources contradict ListingShelf's social-media exclusion; the charter changes with the widening.
9. Correction to the analysis input: `harvest-analysis-2026-10.md:15-16` says ListingShelf has no consumer API beyond its console and run exports. It has listing, change, absence and photo endpoints (`shelf/engineering/architecture/pipeline-contract.md:37-46`); they are unauthenticated and loopback-bound (`architecture.md:81`).

---

## Points

- [x] **P1** one social repo or connectors beside Harvest → confirmed 2026-10-27: two domains, Harvest's social adapters call the connectors' read brokers (T8 decides placement; § 9)
- [x] **T4-1** base post schema vs consumer schemas → confirmed 2026-10-27: Harvest owns a small base filled deterministically; consumer schemas are an optional per-pipeline pass (T6)
- [x] **T4-2** source state in deliveries → confirmed 2026-10-27: `live` · `gone` · `relisted` per link, canonical post gone when all links are (T5, T7)
- [x] **T4-3** search-driven discovery → confirmed 2026-10-27: a `search` adapter family after the first slice; query results land as candidate posts or sources for review (T3)
- [x] **T4-4** consumer-owned credentials and signed-in sessions → confirmed 2026-10-27: a connection reference per pipeline, private container only, never pooled (T1, T3, T7)
- [x] **T4-5** Telegram read path for organizer channels with no admin rights → confirmed 2026-10-27: public `t.me/s` first; T1 chooses between bot, user session and web view (T1)
- [x] **T4-6** keyword subscription semantics → confirmed 2026-10-27: v1 reads the pool only; a keyword may propose a pipeline, never create one (T7)
- [x] **T4-7** contact points (phones, names) from public posts → confirmed 2026-10-27: store a hashed last-9-digit key for dedup in the pool; raw values visible to subscribers of that pipeline only (T5, T6)
- [x] **T4-8** Harvest AI on Haven's pipelines → confirmed 2026-10-27: off; captures plus deterministic fields, Haven's own classification continues (T6)
- [x] **T4-9** container owner → confirmed 2026-10-27: the Events service is the Harvest tenant with a container per catalog; Ocharo never calls Harvest (T7, T8)
- [x] **T4-10** submissions and roles → confirmed 2026-10-27: products enforce their own roles; Harvest records `manual` plus an actor id from a service key (T7)
- [x] **T4-11** link intake routing → confirmed 2026-10-27: match the registrable domain and path scope of public pipelines, else the product's private container (T3, T5)
- [x] **T4-12** iticket → confirmed 2026-10-27: defer until a consumer names fields; it is a client-rendered shell (`t3-web-sources.md:78`), so it needs the `render` form (T3)
- [x] **T4-13** phone reveal where a source hides numbers → confirmed 2026-10-27: not in v1; measure phone coverage from text first (T3)
