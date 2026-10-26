# T8 — Placement

*Last updated: 2026-10-26*

> Where Harvest's code lives. Harvest becomes its own domain repo, `wow-two-sdk-beta.harvest`, seeded by copying
> ListingShelf's generic core; ListingShelf stays alive as the consumer view. Social media is not Harvest's home: a
> second domain, `wow-two-sdk-beta.social`, holds what acts as an organization's account (publish, own metrics,
> authorised reads, account custody), while Harvest keeps the public readers, the Telegram account pool and the
> intake bots, and calls Social only on authenticated routes. Events is a third repo and a Harvest tenant. The chain
> core → Identity → Files → Social → Harvest → Events has no cycle. Three pieces go to core, the web family does not,
> and Harvest's first slice needs nothing but core and PostgreSQL.

- Aliases: `W` = `/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws` · `be` = `W/workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src` · `ls` = `W/workbench/maxs-projects/ventures/saas/ventures.listing-shelf` · `mkp` = `W/workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/ocharo-marketing/engineering/codebase/ocharo-marketing.backend-services/OcharoMarketing.Infrastructure/Providers`.
- Codes from the lead document and T1–T7 (P1–P19, S, W, T4-n, T5-n, T6-n, T7-Pn); `(U)` = unverified.
- Facts come from reads and greps on 2026-10-26 and one throwaway container probe (§ 3.4). Nothing was built or edited.

---

## Verdict

- **P1: two domains.** `wow-two-sdk-beta.social` beside `wow-two-sdk-beta.harvest`; Harvest never holds a social token, and Social never references Harvest.
- **Direction splits the code:** Social acts as an organization's account (write and authorised read); Harvest observes (public read, platform-owned readers, consented intake).
- **Harvest keeps:** every public reader, the licensed-provider runners and their accounts, the Telegram MTProto pool, and both intake bots. No second domain calls any of these today.
- **Social is not on Harvest's first slice.** It is created on the first of: Marketing's first live publish needing stored tokens, Harvest's first authenticated Meta, X or Threads route, a second product that publishes.
- **H1 / P2: a new repo.** `wow-two-sdk-beta.harvest` stamped from the domain template; ListingShelf's client, broker base, two brokers, run vocabulary and fixtures are copied with the source commit cited; ListingShelf stays the shelf view.
- **Org:** `wow-two-sdk-beta` for Harvest, Social and Events, as Identity (Q1a) and Files chose; catalog, platform-apps and both specs still say `wow-two-platform.*`.
- **Chain:** core → Identity → Files → Social → Harvest → Events. Events sits right of Harvest because it imports Harvest's delivery contract. Checked by topological sort of 33 package nodes: no cycle, no edge points right.
- **Core gets three things:** the durable webhook dispatcher (P16), a cookie option on `Http/Safety` (W6), tier routing and metering on `Ai`. The web family (fetcher, robots, sitemap, structured readers) stays in Harvest: one consumer, and the Files Q6 rule puts a pipeline's stateless library with its domain.
- **Render tier:** a stateless HTTP service and a second image, not a role that claims work from PostgreSQL; T7 § 7.5 contradicts T3's no-secrets guardrail.
- **Forms:** one image, `Harvest:Tenancy:Mode = Single | Shared` (Form 2 · Form 3), as Files does for A and B. The Telegram pool is platform-owned and Harvest-operated; a self-hoster brings its own SIMs.
- **First slice:** adapters for public sources, the 001 tables, claim-by-host workers, extraction D+R, pull-cursor delivery. Gate: `mstar.uz` and `voyage.uz` reach a fake Events intake once each, and a killed worker resumes.
- **No blocker.** Two hand steps stay the developer's when the build starts: the GitHub repo and the NuGet trusted-publishing policy.

---

## 1 · Social media and Harvest (P1)

Developer, 2026-10-26: "since this includes a lot of social media logic, should the repo target social media and harvester be part of it?" Ocharo and other products need social integration for other logic too.

### 1.1 Who reads, writes and authenticates (T4 § 8, 28 rows)

| Bucket | Rows | State | Consumers | Account needed |
|---|---|---|---|---|
| act as an organization's account: publish, own metrics, verify | O1 O2 O3 O4 O5 O6 O7 H1 (8) | all built; Marketing's 7 have no live use found, delivery is manual in the pilot | Marketing, Haven | yes: bot token, OAuth user token, system-user token |
| sign in, notify, validate inbound | O8 H2 X1 X4 X5 S1 S2 S3 S4 S5 S6 X6 X7 (13) | 10 built · X6 decided · X7 spec · S6 planned | Desk, Haven, Arcade, Wheelhouse, Feedbacks, Identity, be sdk | bot token or client id and secret; `initData` and webhook checks use a secret only |
| read others' content | O9 O10 H3 X2 X3 S7 M1 (7) | X3 (`yt-dlp`) and S7 (link parser) built · X2 fixtures · O9 a manual task · O10, H3 planned · M1 not found | Sift, TranscriptForge, Sourcing; Harvest planned | only M1 (a Telegram user session) and O10 |

- Third-party reads are 7 of 28 rows. One (M1) needs an account session, and it is not built.
- The products that act as accounts today are Marketing and Haven. Harvest would be a second consumer of account custody, not its owner.
- Five C# paths call the Telegram Bot API (O1 raw HTTP; H1, H2, O8, S1 on `Telegram.Bot`); X6 and X7 plan two more. What repeats is wiring, token config and error mapping, not an HTTP client.
- No platform has a durable per-account token store (T4 § 10).

### 1.2 Which half of Harvest has no social account

`sources.family` has 16 values (T5 § 2.4). Eight are social: `telegram` · `whatsapp` · `instagram` · `facebook` · `youtube` · `threads` · `x` · `intake`. Eight are not: `page` · `structured` · `site` · `render` · `api` · `feed` · `link` · `manual`.

- Events' first sources (`mstar.uz`, `voyage.uz`, Afisha, the nine reviewed links) and Haven's current sources (OLX, Domtut) are all in the non-social eight.
- Inside the social eight most routes need no account: `t.me/s`, a YouTube API key, Route B providers (Apify), forwards into an intake bot.
- Accounts appear only on: Telegram MTProto (T1 route M), Instagram business discovery (a Harvest-owned professional account), Facebook Page Public Content, Threads search, X pay-per-use, and a consumer-owned connection (T4-4).
- Events, fin-nt (e-auksion lots) and the ListingShelf view need no social account at all (T4 § 7).

### 1.3 Options

| Option | For | Against | Domain-structure rule |
|---|---|---|---|
| a · one social repo holds Harvest | one release line; adapters beside clients | half of Harvest has no social account; Events, the first consumer, is non-social; Marketing and Haven would restore Harvest's workers, Playwright and provider runners to publish; S11's separate apps need separate failure domains, one repo couples their releases | a domain is one capability; this is two audiences |
| b · Social domain beside Harvest | Social owns secrets and state, has broker contracts, and serves Marketing, Haven and Harvest; Harvest stays platform-neutral | two repos, one more contract to version; Harvest is Social's second consumer, not yet built | earns a repo: capability forms scope (state and secrets, 2+ products) and a broker contract |
| c1 · connectors as be sdk companions, no service | no new repo; stateless clients are exactly what companions are | custody is state: token refresh, per-owner accounts, S3's per-tenant credentials, T4-4's connection refs, Marketing's receipts and evidence; core is shedding domains (Identity, Files), not gaining | right for stateless clients, wrong for the store |
| c2 · one `channels` domain, intake bots included | one place for every bot | intake semantics (consent, `forward_origin`, container attribution) are Harvest's; transport is core inbound validators plus `Telegram.Bot`; the name collides with core `Comms` channels | joins inbound observing with outbound acting |
| c3 · Harvest builds its social adapters inline, extract Social at +0.1 | no dependency on an unbuilt repo; matches the developer's rule to build infra inline and extract it to the SDK in the +0.1 | one more move later | not an alternative to b: it is b's timing |

**Pick: b, timed as c3.**

### 1.4 The cut

| Capability | Home | Why |
|---|---|---|
| public readers: `t.me/s`, link cards (OpenGraph, oEmbed), RSS and ICS | Harvest | no account; no other reader |
| licensed-provider runners (Apify, Bright Data) and `ProviderAccount` | Harvest | only Harvest buys data; vendor tokens are Harvest's (T2 § 6) |
| Telegram MTProto pool: sessions, joins, flood buckets, leases | Harvest | only reader; leases and `(account, method)` buckets bind to work items (T7 § 7.4); platform-owned, never a tenant's |
| intake bots: Telegram bot and WhatsApp number | Harvest (`intake` family) | transport = core inbound webhook validators + `Telegram.Bot` / `Comms/WhatsApp`; consent, `forward_origin`, attribution = Harvest (T1-P8, T5 § 7.3) |
| Telegram and WhatsApp send (notify) | core `Comms` | `Comms/` already holds Email, Sms, Push, WhatsApp; D12 recommends building Notifications thin on it; Wheelhouse and Feedbacks must not restore Social to send an alert |
| publish with receipts and reconcile, own-post metrics, account verification | Social | Marketing's `mkp` brokers: 9 of its 12 are social (`Providers/` is about 1.1k lines in all) with outcomes such as `Ambiguous` |
| connected accounts, tokens, refresh, revocation, per-account call quota | Social | custody and state |
| platform API transport shared by publish and read (Graph, X v2, Google) | Social edges (`Social.Meta`, `.X`, `.Google`, `.Telegram`) | one place for version churn (Graph removed the Groups API in v19) |
| authenticated reads: IG business discovery, Page Public Content, Threads search, X search, YouTube | Harvest adapters over Social's edges | Harvest-owned read-only app credential (S11); Harvest holds the token |
| consumer-owned connection for a pipeline | Social broker, resolved through Harvest's `IConnectionResolver` | T4-4: private containers only, never pooled |
| sign-in: OAuth providers, Telegram login, Mini App `initData` | Identity | a person is not an account that acts for an organization (T4 § 9) |
| approvals, scheduling, campaigns, receipts policy | the product | Marketing's business logic |
| signed-in browser sessions (RFQ inbox) | nowhere in v1 | T7-P17: the render tier holds no secrets or cookies |

- Refines T4 § 9: Notifications consumes core `Comms`, not Social's client, because Identity (left of Social in the chain) and the M0 products need the sender too. Social's Telegram edge sits above the same sender.
- A client lives in Social only if a second domain calls the same API with an account. Harvest-only clients (MTProto wrapper, `t.me/s` parser, provider runners) stay in Harvest.

### 1.5 Meta review, Telegram pool, intake bots

- Meta app review is per app and per owner (S3, S11). Separate apps per function: Harvest's reading app, an owner's publishing app, Identity's sign-in app. Each has its own failure domain.
- Social runs per owner, as Identity does (D2): Ocharo's instance holds Ocharo's apps; WoW2's holds WoW2's. Harvest Form 3 holds WoW2's reading apps; Form 2 brings its own.
- Telegram pool: platform-owned SIM accounts, operated by Harvest (§ 5.4). Not a connected account, so not Social's.
- Intake bots: one Harvest intake bot and one WhatsApp number, separate from any notification or publishing bot (T1-P8). D5 recommends the same rule: one bot, one webhook owner; Harvest owns the intake webhook.

### 1.6 Pick and timing

- Two domains; Social scope in Points T8-2.
- Social starts on the first of: Marketing's first live publish with stored tokens, Harvest's first authenticated Meta, X or Threads adapter, a second publishing product. Seed code: Marketing's `mkp` brokers.
- Until then Harvest's authenticated adapters, if built first, use a thin inline transport; the second consumer moves it to `Social.Meta` / `.X`.
- Harvest declares `IConnectionResolver` in its contract and leaves it unbound in slice 1.

---

## 2 · ListingShelf (H1 / P2)

### 2.1 What ListingShelf is

`ls` is a venture repo (`sulton-max/ventures.listing-shelf`, 68 commits): a personal listing archive. Charter: personal utility hypothesis, no AI in the capture path, social out of scope, no authentication, loopback only.

| Part | Today | Harvest needs | Fate |
|---|---|---|---|
| Store | SQLite, 11 tables, FTS5, Unix-ms timestamps, migrator sets `001`–`007` | PostgreSQL `harvest` schema, 28 tables plus T7's engine tables (T5, T7) | rewrite; `Apply.sql` + `Rollback.sql` carries |
| Run engine | one serial worker; claims whole runs; interrupts every `Running` run at boot | claim by host, leases, resume (T7 § 7) | replaced; statuses, steps and the 22 `CompletionReason` values carry as vocabulary |
| Fetch | `ListingPageClient` 115 lines, `HtmlListingBroker` 404 | bounded fetcher, discovery, outcomes (T3 § 1) | copy, then generalise |
| Adapters | OLX 69 + Domtut 65 lines; fixtures in `FixturePages.cs` and E2E `ProviderPages.cs` | the `listing` adapter set | copy |
| API | unauthenticated, loopback, same-origin guard | keyed tenants, scopes (T7 § 9) | rewrite |
| Console | about 10.6k lines Vue/TS: shelf, stars and notes, saved views, compare, run canvas, pipelines | operator console: pipelines, runs, canvas, captures | canvas, pipelines and runs → `apps/web`; shelf pages stay |
| Tests | 3.3k lines (unit, integration, E2E) | conformance suite, per-family fixtures | fixtures copy; suites rewrite |

- Backend is 7.8k lines (Api 2.1k, Application 1.2k, Domain 0.6k, Infrastructure 2.4k, Persistence 1.5k). About 1.2–1.5k lines carry over as code or vocabulary (U: estimate from file sizes).
- Two live dependencies exist today: Haven reads finished run exports every 15 minutes (T4 § 5), and the developer's own `listingshelf.db` holds live captures that tests must never open. Neither changes by this decision; how and when Haven changes is outside this track.

### 2.2 Options

| | A · widen and rename in place | B · new domain repo, copy the core | C · greenfield, no copy |
|---|---|---|---|
| History | 68 commits under one name | cites the source commit (Identity T5 § 6 precedent); `git filter-repo` is developer-only object surgery | none |
| Product identity | the personal archive disappears into a platform | ListingShelf keeps its name and charter as the view | as B |
| Rewrite | SQLite → PostgreSQL, T5 schema, T7 engine, auth and Clean-Architecture → domain shape, all inside the live repo | the same rewrite in a clean repo | the same, plus re-deriving the client, brokers and fixtures |
| Live dependants | Haven's intake and the live archive freeze or break during the rewrite | untouched until the view cuts over | as B |
| Archetype | venture → domain by restructuring: five Clean-Architecture projects become packages + service | born as a domain from `wow-two-sdk-beta.domain-template` (CI, conformance, tag-derived releases come stamped) | as B |
| Org and account | `sulton-max` personal repo moves to `wow-two-sdk-beta` | born in `wow-two-sdk-beta` | as B |

**Pick: B.** Widening in place means converting a live repo to a different archetype while two things read from it. T5's schema replaces its tables, and T7 replaces its run model; what survives is vocabulary and fetch code.

### 2.3 Copy, keep, retire

| Copy into Harvest (source commit cited) | Stays in ListingShelf | Retires |
|---|---|---|
| `ListingPageClient` → bounded fetcher; `HtmlListingBroker` pagination, JSON-LD and fallback chain → `listing` adapter base; OLX and Domtut brokers; status, step and `CompletionReason` vocabulary; fixtures; run canvas, pipelines and runs pages | shelf pages, stars and notes (`listing_notes`), saved views, compare, CSV export | SQLite capture store, FTS5 index, serial worker, loopback origin guard, Unix-ms timestamps |

- The shelf survives as a consumer view: a tenant of Harvest with a key, reading `wow2.listing.v1` items (or the base envelope plus `extras.listing`). Its backend shrinks to a notes and views store plus a BFF; SQLite stays acceptable for a local tool (D11).
- View row: per post, links expanded in the detail (T5-17).
- The live archive imports once into the view's private container. The importer belongs to the view's cutover, not to Harvest's first slice.
- Retire the product name `ListingShelf` for the harvester: Harvest is the capability; ListingShelf is one view on it.

---

## 3 · Package graph

### 3.1 Harvest repo

`wow-two-sdk-beta.harvest`, from the domain template (`packages/` · `service/` · `tests/`; `apps/web`; `engineering/research/harvest-analysis-2026-10/` after sanitising, § 4).

| Package | Layer | Holds | Heavy dependencies | Slice |
|---|---|---|---|---|
| `WoW2.Sdk.Beta.Be.Harvest.Abstractions` | contract | brokers (`IHarvestSubscriptions`, `IHarvestPipelines`, `IHarvestPosts`, `IHarvestDeliveries` pull cursor, `IHarvestLinks`, `IHarvestEntries`, `IHarvestSchemas`); `wow2.post.v1`; post and link events (`post.new` … `link.state`, `pipeline.run`, `pipeline.health`); three-level outcomes; scopes; `ActorRef`; ports `ICaptureStore`, `IAlertSink`, `IConnectionResolver` | none | 1 |
| `…Harvest.Module` | forms · Form 1 | SQL set, scheduler, claim-by-host workers, leases, frontier, `Web/` (fetcher, robots, sitemap, structured and feed readers), `Extraction/` (D and R tiers), adapters for `page` · `structured` · `site` · `feed` · `link` · `listing` · Telegram preview · provider runner · `intake`, post resolve and dedup tiers 0–3, link state machine, delivery log and pull cursor, retention purge, `maintenance` jobs | AngleSharp, Meziantou.Framework.RobotsTxt, Ical.Net, System.ServiceModel.Syndication; fastText wrapper (native) in P2 | 1 |
| `…Harvest.Client` | forms · Forms 2/3 | HTTP client over the same brokers; Standard Webhooks receiver helper | core | 1 |
| `…Harvest.Files` | extension | `ICaptureStore` and media over `Files.Abstractions` | none beyond the contract | when Files P1 lands |
| `…Harvest.Social` | extension | authenticated adapters over Social's edges and read brokers | Social edges | after Social |
| `…Harvest.Telegram` | extension | MTProto pool client (route M), session store | `WTelegramClient` | P5 (T1-P2) |
| `…Harvest.Render` | extension | Playwright worker and the render RPC contract | `Microsoft.Playwright` | after the W7 spike |
| `…Harvest.Testing` | test kit | fake host server, recorded pages, fake clock, fake Events intake, conformance base | `…Be.Testing` | 1 |
| `@wow-two-beta/fe-harvest` | fe | `./contracts` (TS mirror), `./console` (pipelines, runs and canvas, captures, queue and hosts, subscriptions and deliveries, review), `./intake` (submit-link and manual-entry widgets that call the host's routes) | peers `@wow-two-beta/fe` | 1 (console minimum) |
| `service/Harvest.Api` · `apps/web` | service | one host: `api` · `scheduler` · `worker` · `deliverer` · `maintenance` roles, SignalR, console served single-host; image `harvest` | — | 1 |
| `service/Harvest.Render` | service | the render host; image `harvest-render` | Playwright base image | after W7 |

- `Module` references core only. Each cross-domain adapter is its own extension package (`Harvest.Files`, `Harvest.Social`), so slice 1 restores no other domain and a Form 1 host takes only what it uses.
- No edge in v0.1. `Harvest.Web` (fetcher, robots, sitemap, structured readers) and `Harvest.Extraction` (D and R) split out the day a second product uses them without Harvest's store. Namespaces stay, so the split costs no `using`.
- Tests: `Harvest.Tests.{Unit,Integration,E2E,Migrations,Conformance}`; the conformance suite runs in-process against `Module` and against the released image.
- Release lines: NuGet `10.y.z-beta` on `be-v*`, npm `0.0.z` on `fe-v*`, image `X.Y.Z` on `vX.Y.Z`, per domain structure.

### 3.2 Social and Events, outline

| Repo | Packages | Service and image | fe |
|---|---|---|---|
| `wow-two-sdk-beta.social` | `…Social.Abstractions` (`IConnectedAccounts`, `ISocialPublisher`, `ISocialMetrics`, `IAccountVerifier`, `ISocialReader`, `IPlatformEvents`; `Receipt`, outcomes incl. `Ambiguous`) · edges `…Social.Telegram`, `.Meta`, `.X`, `.Google` · `.Module` (store, token lifecycle, quota ledger) · `.Client` · `.Testing` | `Social.Api` (OAuth connect callbacks, refresh worker, platform webhook hosts); image `social` | `@wow-two-beta/fe-social` (connect-account widgets, accounts table) |
| `wow-two-sdk-beta.events` | `…Events.Abstractions` (`IEventsClient`, models, `IEvent` records) · `.Module` (catalog, tracking, intake handler, ICS) · `.Client` · `.Testing` | `Events.Api` (review console, `POST /harvest/items`); image `events` | `@wow-two-beta/fe-events` (feed components) |

- Social's edges are store-less: a product that publishes with a configured token uses `Social.Meta` without the store (the edge rule).
- Social's contract references the kernel and `Identity.Abstractions` (organization claims) only.

### 3.3 What moves into core, and what does not

| Item | Verdict | Why |
|---|---|---|
| Durable webhook dispatcher (P16, T7-P9) | **core**, `Messaging/Webhooks` (new `Durable/`) | four domains need at-least-once outbound: Identity (M13), Harvest, Events, Files. Messaging stays in core (Identity T5 § 7). Harvest cannot own it: Identity sits left of Harvest |
| URL policy, address half | already **core**: `Http/Safety` (`AddSafeOutboundHttp`) | connect-time address validation through `SocketsHttpHandler.ConnectCallback`, redirects, proxies and shared cookies off. T3 § 2.7 listed it as new work |
| `Http/Safety` cookie option | **core**, small | W6 needs a run-scoped cookie jar (iticket's waiting room); the handler disables cookies today |
| URL policy, scope half (known hosts, path scope, registrable-domain routing) | Harvest | `source_scopes` is Harvest's table |
| Fetcher, robots, sitemap, structured and feed readers (W18) | **Harvest** (`Module/Web/`) | one consumer: no HTML-parser or browser package (`AngleSharp`, `HtmlAgilityPack`, `Microsoft.Playwright`, `RobotsTxt`, `PuppeteerSharp`) appears in any csproj or props file under `workbench/` outside ListingShelf (grep, 2026-10-26). Files Q6 puts a pipeline's stateless library with its domain. "Form 1 in the be SDK" (spec) means the Harvest package family `WoW2.Sdk.Beta.Be.Harvest.*` |
| `Ai` seam | **core** `Ai` (exists) + `Ai/Routing`: tier map (`embed` · `lite` · `core` · `pro`), fallback order, usage tagged by `{consumer, pipeline, tier, promptVersion}` | three consumers: Haven (`Haven.Platform.Ai` is the source), Marketing (OpenAI, Gemini), Harvest (D16). Anthropic and OpenAI registrations are still pending. Not slice 1: AI is off |
| Telegram sender | **core** `Comms/Telegram` | § 1.4; unrelated to Harvest's slice |
| `NOTIFY` backplane for SignalR (T7-P16) | Harvest first | lift to core `Realtime` when a second service runs several replicas |
| Partition job (T5-16) | Harvest `maintenance` job behind `IPartitionMaintainer` | lift to core `Data` when Logs (#6) needs time partitions |
| Keyed work queue: claim by host, leases, fenced results | Harvest | one consumer; Files runs on `Jobs/` |
| AI gateway service (#15) | not needed | T6: Harvest builds on the `Ai` seam |

- Core asks follow the SDK change loop: change core, push, wait for the release commit, `git pull --ff-only`, re-pin. Order for slice 1: the cookie option before the fetcher lane; the dispatcher in parallel, before webhook push. Pull-cursor delivery needs neither.

### 3.4 Dependencies on other domains

| Harvest needs | From | Slice 1 | Later |
|---|---|---|---|
| auth for consumers | Identity | core `Identity/ApiKeys` (spec H3); namespace unchanged across the Identity cut | `Identity.Auth` for token validation (M8); client credentials (M10); actor by token exchange (M11) |
| capture bodies and media | Files | `ICaptureStore` over core `Storage/` byte adapters (local disk, S3); `body_ref` becomes an opaque text | `Harvest.Files` over `Files.Abstractions`; Files Q13 and Q18 are sized for Harvest |
| operator alerts (`session_lost`, `frozen`, budget) | Notifications (#10) | `IAlertSink`: log + console; no reference | bind Notifications, or core `Comms/Telegram`, by host config |
| authenticated social routes | Social | none | `Harvest.Social` over Social's edges |
| consumer-owned connections | Social | `IConnectionResolver` unbound | bound to Social's broker |
| tier routing, embeddings, LLM | core `Ai` | none: D and R only (T6-17) | `Ai/Routing` |
| Events | none | none | none: Harvest never references Events |

- Files is not built (spec ready, empty solution, repo waits for the template). Binding the capture store to a port keeps slice 1 off it.
- The platform database image is `postgres:16-alpine` (Wheelhouse `products.compose.yml`). Probe on 2026-10-26, a throwaway container per image: `pg_trgm` and `unaccent` available, `vector` absent; database locale `en_US.utf8`; `show_trgm('привет')` returns seven trigrams, `lower('КВАРТИРА')` folds, `similarity('КВАРТИРА','квартира')` = 1. Same on `postgres:16` (Debian). T6's boot self-test passes on the platform image. `uuidv7()` needs PostgreSQL 18, so ids stay code-made (T5). Embeddings (pgvector) need a custom image (T5-5).

### 3.5 Dependency graph

```text
repo chain, left → right. "A → B" = A references B. A package references only repos to its left,
and every repo also references core. Services and the consumer view may reference any implementation.

core ──► identity ──► files ──► social ──► harvest ──► events        (+ ListingShelf view, a consumer)

kernel    Be.Abstractions                    → (none)
core      Be                                 → Be.Abstractions
identity  Identity.Abstractions              → Be.Abstractions
          Identity.Auth                      → Identity.Abstractions, Be
          Identity.Module · .Client          → Identity.Auth            (.Server → .Module; Providers → Be)
files     Files.Abstractions                 → Be.Abstractions
          Files.Module                       → Files.Abstractions, Identity.Abstractions, Be
          Files.Client                       → Files.Abstractions, Be
social    Social.Abstractions                → Be.Abstractions, Identity.Abstractions
          Social.{Telegram,Meta,X,Google}    → Social.Abstractions, Be
          Social.Module                      → Social.Abstractions, Social.{Telegram,Meta,X,Google}, Be
          Social.Client                      → Social.Abstractions, Be
          service Social.Api                 → Social.Module, Identity.Auth
harvest   Harvest.Abstractions               → Be.Abstractions
          Harvest.Module                     → Harvest.Abstractions, Be
          Harvest.Client                     → Harvest.Abstractions, Be
          Harvest.Files                      → Harvest.Module, Files.Abstractions
          Harvest.Social                     → Harvest.Module, Social.Abstractions, Social.{Telegram,Meta,X,Google}
          Harvest.Telegram                   → Harvest.Module
          Harvest.Render                     → Harvest.Abstractions, Be
          service Harvest.Api                → Harvest.Module, .Files, .Social, .Telegram, Identity.Auth, Files.Client
          service Harvest.Render             → Harvest.Render
events    Events.Abstractions                → Be.Abstractions, Identity.Abstractions, Harvest.Abstractions
          Events.Module                      → Events.Abstractions, Harvest.Abstractions, Files.Abstractions, Be
          Events.Client                      → Events.Abstractions, Be
          service Events.Api                 → Events.Module, Harvest.Client, Identity.Auth, Files.Client
consumer  ListingShelf view                  → Harvest.Client, Harvest.Abstractions, Be

ports (no package edge): Harvest.IAlertSink → host binds core Comms or Notifications · Harvest.ICaptureStore →
core Storage or Harvest.Files · Harvest.IConnectionResolver → Social broker

Social → Harvest: none. Harvest → Events: none. Anything → a repo to its right: none.
```

- Check: a topological sort over 33 package and service nodes (script run 2026-10-26) found no cycle, and no edge points from a left repo to a right one.
- Why Harvest sits left of Events: Events imports Harvest's delivery payload types and its subscription broker. T7 § 5 of the Identity analysis drew Events and Harvest as siblings; siblings cannot share the contract.
- Notifications (#10) is not a node: Harvest reaches it through `IAlertSink`, so Notifications can land on either side.

---

## 4 · Org and naming

| Option | For | Against |
|---|---|---|
| `wow-two-sdk-beta.{harvest,social,events}` | Identity Q1a and Files Q3 confirmed the org; domain structure § Open leads with it; Harvest and Events are free to self-host, so public by design; packages are first-class artifacts; every domain gets one home | catalog, platform-apps and both specs say `wow-two-platform.*`; the repos are public, so research needs sanitising (identity Q39) |
| `wow-two-platform.{…}` | already in the catalog and platform-apps; Wheelhouse knows the org | the org is internal infra, "not for external consumers"; splits domains across two orgs; Identity chose against it |

**Pick: `wow-two-sdk-beta`.** Closes domain structure § Open for these three.

| Part | Harvest | Social | Events |
|---|---|---|---|
| repo | `wow-two-sdk-beta.harvest` | `wow-two-sdk-beta.social` | `wow-two-sdk-beta.events` |
| code dirs | `harvest.backend-services/` · `harvest.frontend-services/` | `social.…` | `events.…` |
| NuGet | `WoW2.Sdk.Beta.Be.Harvest.{Layer}` | `…Be.Social.{Layer}` | `…Be.Events.{Layer}` |
| namespace root | `WoW.Two.Sdk.Beta.Be.Harvest` | `…Be.Social` | `…Be.Events` |
| npm | `@wow-two-beta/fe-harvest` | `fe-social` | `fe-events` |
| image | `harvest`, `harvest-render` | `social` | `events` |
| descriptor product slug | `harvest` | `social` | `events` |

- Slug `social` is a provisional name. `connectors` is the alternative (T4's word); it would also cover a future Gmail connector (T4 O9). `social` matches the developer's question and keeps Gmail out.
- Catalog: three entries keep `kind: platform`, `workspace: wow2-platform`; `repositories` point at the new repos; `local:` moves from `workbench/wow-two-platform/…` to `workbench/wow-two-sdk-beta/…`. Social is a new entry.
- Platform apps: row 16 and 17 repo columns change; row 17 "Needs" drops `15` (AI Gateway) for `3` (T6-11); a Social row is added when its trigger fires.
- Public repos: T1 § 6 (SIMs, entity, Uzbek access risk), T2 § 3.3 (legal posture) and the sources' terms readings move into `engineering/research/` only after a strip pass, as Identity Q39 does for T6.

---

## 5 · The three forms for Harvest

| | Form 1 · library | Form 2 · self-hosted | Form 3 · provided |
|---|---|---|---|
| Ships | `Harvest.Module` + adapters in the host's process | image `harvest` (+ `harvest-render` if enabled), bundle with its own File Storage instance | the `Harvest.Client` only |
| Runs | `scheduler`, `worker`, `deliverer`, `maintenance` as hosted services | one process, five roles; `render` a second container | WoW2's instance, `Tenancy:Mode = Shared`, off the control host |
| Database | the host's PostgreSQL, schema `harvest`, SQL set shipped by the module | its own PostgreSQL | its own |
| Containers | one private, no pool, no alias (T5 § 6.5) | one pool + its consumers' containers | WoW2's pool + a container per consumer |
| Captures | `ICaptureStore` over core `Storage/` or `Files.Client` | the bundled Files instance | WoW2's own Files instance (instances per owner) |
| Tenant | the host product | the operator, the only tenant (`Mode = Single`) | many; Events first |
| Credentials | the host's | the operator's own, per tenant (S3) | WoW2-owned, with a per-consumer cap; a tenant may bring its own for a private pipeline |
| Telegram pool | the host's accounts, if it enables it | the operator's own SIMs | WoW2's pool |
| Consumer owns | config, tables, secrets | the container's config | its client config and key |

### 5.1 One image, two modes

- `Harvest:Tenancy:Mode = Single | Shared` on one image, as Files runs A and B (Files Q8). `Single` caps `tenants` at one row and resolves it without asking.
- Tenant resolution: API key prefix, later token `iss` + `aud` (T7 § 9.1).
- Form 3 is not the control host: Identity Q4 keeps products off it, and Harvest's egress and Playwright load do not belong beside Wheelhouse.

### 5.2 Credentials by form (S3, refines T7 § 9.2)

- Static provider keys (Apify, Bright Data, Meta and Threads app secrets, X, YouTube) are host files rendered from Wheelhouse's vault (D10).
- Mutable secrets (Telegram session blobs, OAuth refresh tokens) live in Harvest's database, sealed with core `Foundation/Security` (`ValueCipher`, `SealService`) under a master key from the environment (`EnvironmentMasterKeyBroker`), set from a host file. T1 § 5.2 names Secrets Vault, which is inactive in the catalog (merging into Wheelhouse); the sealed column replaces it.
- Meta app review is per app and per owner, so Form 2 cannot use WoW2's approved apps. The console needs the "bring your own provider account" flow (T2).
- `tenant.platform_credentials_allowed` stays `false` until P8 settles the owner.
- `pool_shareable` stays `false` for Meta API and Route B routes until counsel reads Meta Platform Terms § 3.c (T2).

### 5.3 Render tier (W7)

- **Change to T7 § 7.5:** the render container is a stateless HTTP service, not a role that claims work items. T3 § 2.4 requires "no secrets and no route to internal ranges"; claiming from PostgreSQL needs both.
- Shape: the `worker` claims a `route = render` item under the normal host gate, calls `POST /render { url, policy }` on `harvest-render`, receives the rendered DOM and the JSON responses the page fetched, and writes the capture. The lease covers the call (3–10 s, U).
- `harvest-render` holds no database credential, no secret and no cookie jar between pages; egress only to the public internet; non-root, seccomp profile, `--init`, `--ipc=host` (Playwright docs).
- A second image and a second `services:` entry in `deploy.yml` (the descriptor supports several; `needs` stays empty for it). Domain structure § Backend names one host, `service/{Domain}.Api`; this adds `service/Harvest.Render` as a convention delta.
- Form 1: render is off, or points at an endpoint URL; the Playwright dependency stays out of the host unless `Harvest.Render` is referenced. Form 2: in the bundle only when `render.enabled`.
- Off until the W7 spike measures memory and seconds per page.

### 5.4 The Telegram account pool (P8, T1-P3)

- **Legal owner, Form 3:** the parent company of `ven-t-012` (P8); SIMs registered to it. UZ SIM rules for a foreign owner are unread (U, T1 § 6).
- **Code custodian:** Harvest. `account` rows hold lease, flood buckets, memberships and a sealed session; platform-owned, never exposed to a tenant (T7 § 9.3).
- **Why not Social:** the pool has one reader, and its state is work-item scheduling (sticky assignment, `(account, method)` buckets). A custody record in Social would add a round trip per call for no second user.
- **Per form:** Form 1 host supplies its own accounts; Form 2 operator brings SIMs and their own `api_id` and `api_hash` (one `api_id` per number, T1 § 5.2); Form 3 is WoW2's. Default `telegram.account_pool.enabled = false`.
- Provisioning stays human: SIM, login code, 2FA go through the console into the sealed store; no worker receives a code (T1 § 5.2).

### 5.5 What a self-hoster brings

| Needs | Required | Note |
|---|---|---|
| Docker host and egress IP | yes | reachability from a datacenter IP is untested (U, W8); probe before choosing the host |
| PostgreSQL ≥ 16, UTF-8 locale, `pg_trgm` | yes | the boot self-test fails closed (T6-14); pgvector only for embeddings |
| File Storage | bundled | its own instance in the bundle (spec § Storage) |
| identification page and contact | yes | the image serves `/bots/harvest`; the UA names the operator, not WoW2 (W14) |
| an operator API key for the console, plus host files for secrets | yes | console auth is the operator key and a same-origin guard until Identity (T7 § 9.1); secrets per D10 |
| provider accounts: Apify or Bright Data, Meta or Threads apps with their own review, X credits, YouTube key | optional | each unlocks its routes; none needed for web sources |
| SIMs, `api_id`, `api_hash` | optional | Telegram routes beyond `t.me/s`; their own terms exposure |
| LLM keys | optional | AI is off by default; `Ai` seam, tier map by configuration |
| a posture decision | yes | `permission`, `ai_allowed`, route posture per source (P3); counsel reads are the operator's |

---

## 6 · Events and Harvest

### 6.1 One repo or two

**Two.** Events is a catalog with private tracking, a review console and ICS; Harvest is a 24/7 capture engine.

| | Events | Harvest |
|---|---|---|
| Owns | events, series, places, tracking, review | sources, captures, posts, links, deliveries |
| Consumers | Ocharo Desk now; any product that tracks events | Events, Haven, fin-nt, Sift, TranscriptForge, the ListingShelf view |
| Heavy dependencies | an ICS writer (U: `Ical.Net`) | AngleSharp, Playwright, `WTelegramClient`, fastText |
| Runtime | a service plus an embeddable Form 1 module | workers with egress, leases and a render tier |
| Cadence | follows Desk's needs | follows source changes |

- A merged repo would give Harvest an event vocabulary (T4 § 2: Harvest holds title, text and dates with precision, nothing event-specific) and make Haven restore the catalog.
- The seam is the contract: Events imports `Harvest.Abstractions` (`IHarvestSubscriptions`, delivery payloads); the Events service takes `Harvest.Client`.

### 6.2 Events as a Harvest tenant (T4-9)

- The tenant is whoever holds the Harvest key. For the Events service that is the service; Ocharo Desk never calls Harvest.
- One container per catalog: `containers.external_ref = 'ocharo-fashion'` (T5 § 2.4). Subscriptions carry `context = {"catalog":"ocharo-fashion"}`, echoed on every event (T7 § 5.7).
- Scopes: `subscriptions:manage` · `pipelines:manage` · `events:read` · `posts:read`; `links:submit` and `entries:write` only if Events proxies Desk's submissions (T7 § 6.3).
- Events registers `wow2.event.v1` and its mapping at start-up from embedded resources in `Events.Module`; the mapping reads Harvest's envelope paths (`extras.schemaOrg.event…`), which is the one place Events depends on Harvest's shape (T6 § 3).
- Form 1 Events (the module inside a product) makes the host product the tenant. The registration code is the same.
- Events' own source kinds shrink to `Harvest subscription · manual · import`: feeds are a Harvest family (T3 § 2.6), so Events keeps ICS export only.

### 6.3 Vocabulary: four collisions and two mappings (T5 flagged one)

| Word | Events spec | Harvest (T5, T7) | Rule |
|---|---|---|---|
| `observation` | one extracted record from a source, awaiting match | not used | stays Events-only. An observation = one delivered post revision plus its `post.extracted` item |
| `pipeline` | the stages and custom fields an organization tracks events with | a standing harvest of a source | Events renames its tracking `pipeline` to `workflow`; Desk's built contract does not use the word |
| `source` | where events come from: a Harvest pipeline, feed, manual entry, import | an origin site, channel or account with family and posture | Events' `source` references a Harvest subscription id; it never holds a Harvest source |
| `subscription` | a token URL serving ICS for a saved filter | one tenant's channel, tag or keyword interest | Events renames its own to `feed link` |
| `provenance` | every source that reported it | `field_prov` per field and `links[]` | Events' `provenance` is derived from `links[]`; it keeps no copy of raw captures |
| `catalog` / `container` | catalog = curated namespace | container = visibility boundary | one-to-one; `external_ref` ties them |

### 6.4 Who owns matching

| Level | Question | Owner | Mechanism |
|---|---|---|---|
| link identity | the same page or post seen again? | Harvest | `(source_id, external_key)` upsert |
| post | two links show one thing? (locale twins, a forward and its origin, one offer under several URLs) | Harvest | T5 ladder; `move_link`; vetoed across kinds and across dates beyond precision |
| entity | do several posts describe one event? | **Events** | external id, then key, then fuzzy title, dates and city within series or place (events spec § Harvest seam); human merge |

- No matching logic moves to Harvest. Harvest supplies the inputs: `post_id`, `revision`, `links[]` (source handle, `external_key`, state), `origin_key`, dates with precision, place text, `publisher` id.
- Events' "external id" tier reads Harvest's `links[].external_key`; Events' `externalIds` map (source → id) is that list.
- Events must handle `post.merged {from, into}`, `post.unmerged` and `post.purged` (T5 § 3.9, § 7.2): re-point or restore observations, and drop purged text from catalogs. Add them to the intake contract.
- Harvest merges posts only within a container, so the Events catalog sees its own container's merges (T5 § 6.1).
- Alias posts (T5-15): a catalog container shows pool posts through aliases with stable private ids; Events stores the private id, which never changes when a pool post merges.

### 6.5 Edits to the Events spec

- Repo `wow-two-sdk-beta.events`; Placement names the Harvest dependency (`Events.Module` → `Harvest.Abstractions`).
- Rename tracking `pipeline` → `workflow` and ICS `subscription` → `feed link`.
- Intake: accept `link.state`, `pipeline.run{complete}`, `pipeline.health`, `post.merged`, `post.unmerged`, `post.purged`; `extracted` optional (T7 § 5.7).
- Sources: feeds go through Harvest; EV2 (Afisha) stays W1.

---

## 7 · First slice

**Scope: only what the Harvest build needs first.** Product changes (Ocharo, Haven, the ListingShelf view) are outside it.

**Gate:** from the dev host, Events' two JSON-LD sources (`mstar.uz`, `voyage.uz`) are harvested on schedule; a fake Events intake receives each event once with source, dates and precision; a removed page becomes `suspect`, then `gone`, with `link.state`; a worker killed mid-sweep resumes with an intact frontier; the conformance suite passes in-process and against the image; one `listing` run (OLX or Domtut fixtures) proves the second family.

| # | Step | Where | Exit check |
|---|---|---|---|
| 0 | developer: GitHub repo, NuGet trusted-publishing policy for `publish-packages.yml`, git flags; confirm org (T8-5) | hand steps | repo exists |
| 1 | stamp `wow-two-sdk-beta.harvest` (`create-repo`, `SHAPE=domain`, slug `harvest`); add `Harvest.Api`, `apps/web`; spec → `product/product.md`; analysis → `engineering/research/` after the strip pass | repo | template CI green |
| 2 | SQL set `001`: `containers` · `sources` · `source_scopes` · `host_policies` · `retention_policies` · `check_policies` · `enumerations` · `captures` (monthly partitions, a default partition, a `maintenance` job creating three months ahead) · `post_links` · `link_schedule` · `link_readings` · `link_events` · `link_check_log` · `posts` · `post_texts`; engine tables: `tenants` · `api_keys` · `pipelines` · `schedules` · `runs` · `work_item` · `host_state` · `subscriptions` · `subscription_event`; boot self-test `show_trgm('привет')` | `Module` | migrations suite on `postgres:16-alpine` |
| 3 | fetch lane: copy ListingShelf's client onto `Http/Safety`; robots (RFC 9309), `host_state`, outcomes, conditional GET, `Retry-After`, run-scoped cookies | `Module/Web/` | contract tests against a fake host server |
| 4 | engine lane: scheduler (stored `next_due_at`, coalescing), run model, claim-by-host with `SKIP LOCKED`, leases, fenced writes, frontier, work kinds `capture` · `discover` · `refresh` · `sweep` · `check` | `Module/Engine/` | kill -9 mid-sweep resumes |
| 5 | adapter lane: `structured` (JSON-LD `Event`), `site` (sitemap, `lastmod_trust`), `page`, `feed` (RSS, ICS), Telegram preview (route W), `listing` (OLX, Domtut ported) | `Module/Adapters/` | recorded-page fixtures per family |
| 6 | extraction D and R: `wow2.post.v1`, normalisation `norm@1`, dates with precision, prices, phones (HMAC key), script and language by rules, schema.org `Event` → `wow2.event.v1` mapper | `Module/Extraction/` | fixture evaluation set per family (T6 § 6.3, subset) |
| 7 | post layer: link upsert, dedup tiers 0–2, `ResolvePost`, link state machine and rollup | `Module/Posts/` | suspect and gone scenarios on the fixture server |
| 8 | delivery: transactional event log, pull cursor with the `xid8` horizon (T7-P19), tenants and API keys through core `ApiKeys`; webhook push once the core dispatcher releases | `Module` + `Api` | a fake Events intake receives mstar items idempotently |
| 9 | console: pipelines, runs with the copied canvas, queue and hosts, subscriptions and deliveries; `fe-harvest` minimum | `apps/web` | one operator walk-through |
| 10 | image, `deploy.yml`, dev rollout through Wheelhouse on the Form 3 dev host; reachability probe for the four event sites (W8) | `deployment/` | dev verify passes |

- Lanes 3, 4, 5, 6 touch disjoint folders and can run as parallel chats (agentic workflow: disjoint file sets).
- Core asks (§ 3.3) ride beside: cookie option before step 3; dispatcher before the push half of step 8.
- Afisha stays `pending-approval` until W1; iticket waits for the render tier (T4-12).

**Out of the slice:** Social; the Telegram pool and `Harvest.Telegram`; Instagram, Facebook, X, Threads, YouTube, TikTok adapters; WhatsApp; the render tier and `Harvest.Render`; link intake and manual entries (slice 2, when a product submits); tag and keyword subscriptions; containers' alias and adoption jobs; E, S and L tiers; adaptive schedules; merge review UI; `Harvest.Files` (until Files P1); retention purge beyond a stub; the ListingShelf importer.

---

## Findings that change the spec

- **Placement section of the Harvest spec.** Form 1 is the Harvest package family `WoW2.Sdk.Beta.Be.Harvest.*` in `wow-two-sdk-beta.harvest`, not code "in the be SDK". Form 3 becomes `Tenancy:Mode = Shared` of the same image. H1 closes: a new repo, not a renamed ListingShelf.
- **Social is a second domain, and Harvest keeps more of the social code than T4 assumed.** Public readers, provider runners, the MTProto pool and the intake bots stay in Harvest; Social takes publish, metrics, verification, custody and the shared platform transport. T4 § 9's "shared state" list shrinks once S11 gives each function its own app.
- **Telegram send belongs in core `Comms`, not in Social.** It refines T4 § 9: Notifications builds on `Comms/` (D12), and Identity and the M0 products need the sender with no Social restore.
- **The org is `wow-two-sdk-beta`** for Harvest, Social and Events. Catalog `local:` paths and `repositories`, platform-apps rows 16 and 17, and both specs' repo names change; row 17 "Needs" drops `15`.
- **Render tier correction.** T7 § 7.5 has `render` claim work from PostgreSQL; T3 § 2.4 forbids secrets and internal routes on that container. The render container becomes a stateless RPC service with its own image and `services:` entry.
- **W18 resolved the other way.** The web family ships inside Harvest. Core gets only the durable webhook dispatcher, a cookie option on `Http/Safety`, and `Ai/Routing`.
- **`Http/Safety` already ships connect-time address validation.** T3 § 2.7 asked for it as new work; Harvest's URL policy is the scope half on top.
- **The chain order puts Events right of Harvest.** Identity T7 § 5 drew them as siblings; Events imports Harvest's contract. Notifications is reached through `IAlertSink`, not a reference.
- **Capture storage is a port.** T5's `body_ref uuid` → opaque text; slice 1 runs on core `Storage/` because Files is unbuilt. `Harvest.Files` binds Files later.
- **Secrets custody changed.** T1 § 5.2 assumes Secrets Vault, which is inactive; static keys come from host files (D10), mutable sessions and tokens sit sealed in Harvest's database.
- **Events vocabulary.** Four collisions, not one: `observation` stays Events-only; `pipeline` and `subscription` rename on the Events side. Events' feed sources collapse into Harvest subscriptions.
- **The platform database image passes T6's self-test.** `postgres:16-alpine` folds Cyrillic and builds Cyrillic trigrams; it has no `vector` and no `uuidv7()`.
- **Harvest has two deployables.** Domain structure § Backend and the template assume one `service/{Domain}.Api`; `service/Harvest.Render` is a convention delta.
- **Public-repo hygiene.** The analysis moves into a public repo only after a strip pass (identity Q39).

---

## Points

- [ ] T8-1 (P1) social media and Harvest: one repo, or two domains → provisional pick: two domains, `wow-two-sdk-beta.social` beside `wow-two-sdk-beta.harvest`; Social never depends on Harvest; Harvest's authenticated social adapters use Social's edges, its public readers stay in Harvest; Social is created on its first trigger, not on the first slice
- [ ] T8-2 Social's scope and slug → provisional pick: in: connected accounts and tokens, publish with receipts, own metrics, verification, authorised-read transport, inbound platform events, per-account call quota; out: sign-in (Identity), approvals and scheduling (products), the MTProto pool, intake bots, public readers (Harvest), Telegram and WhatsApp send (core `Comms`); slug `social`, alternative `connectors`
- [ ] T8-3 Telegram sender → provisional pick: core `Comms/Telegram` over `Telegram.Bot`, extracted from the five paths; Notifications builds on `Comms/` (D12); Social's Telegram edge sits above it (T4 § 9 amended)
- [ ] T8-4 (P2 / H1) Harvest's repo → provisional pick: new `wow-two-sdk-beta.harvest` from the domain template; ListingShelf's client, broker base, OLX and Domtut brokers, run vocabulary, fixtures, canvas and pipelines pages copied with the source commit cited; ListingShelf stays the shelf view and keeps serving its live dependants until it cuts over
- [ ] T8-5 org, names, catalog → provisional pick: `wow-two-sdk-beta` for Harvest, Social, Events; names per § 4; catalog entries repointed, platform-apps rows 16 and 17 edited (row 17 Needs `3`), a Social row on its trigger; research stripped before it moves into the public repo
- [ ] T8-6 chain and ports → provisional pick: core → Identity → Files → Social → Harvest → Events; `Module` references core only; `Harvest.Files` and `Harvest.Social` are extension packages; `IAlertSink`, `ICaptureStore`, `IConnectionResolver` are ports bound by the host
- [ ] T8-7 (W18) web family → provisional pick: inside `Harvest.Module`; split into edges `Harvest.Web` and `Harvest.Extraction` when a second product uses them without the store
- [ ] T8-8 (P16, T7-P9) core asks → provisional pick: durable dispatcher in core `Messaging/Webhooks/Durable` (Identity, Harvest, Events, Files); `Http/Safety` cookie option (W6); `Ai/Routing` from `Haven.Platform.Ai` before AI turns on; pull-cursor delivery ships first, webhook push after the dispatcher releases
- [ ] T8-9 capture and media store → provisional pick: `ICaptureStore` port, `body_ref` opaque text; core `Storage/` in slice 1; `Harvest.Files` when Files P1 lands (T5 amended)
- [ ] T8-10 (W7) render tier → provisional pick: stateless HTTP service, image `harvest-render`, no DB, no secrets, second `services:` entry; domain structure § Backend gains a second-host exception; off until the spike measures it
- [ ] T8-11 (S3) forms and tenancy → provisional pick: one image, `Harvest:Tenancy:Mode = Single | Shared`; Form 3 on its own host off the control host; reachability probed before the host is chosen (W8)
- [ ] T8-12 (P8, T1-P3, S3) credentials and pool → provisional pick: static keys from host files (D10), mutable sessions sealed in Harvest's database with core `ValueCipher`; pool platform-owned, Harvest-operated, legally owned by the `ven-t-012` company in Form 3; a self-hoster brings its own SIMs, `api_id`, `api_hash`, provider accounts and Meta apps; pool and platform credentials off by default
- [ ] T8-13 (T4-9) Events as a tenant → provisional pick: Events is its own repo and a Harvest tenant, one container per catalog, `context` echoed; Events renames tracking `pipeline` → `workflow` and ICS `subscription` → `feed link`; its feed sources move into Harvest subscriptions
- [ ] T8-14 matching → provisional pick: Events owns entity-level matching; Harvest owns post-level dedup and supplies `links[]` keys, dates with precision and `post.merged` · `post.unmerged` · `post.purged`; the Events intake contract accepts them
- [ ] T8-15 (T7-P17) signed-in sources → provisional pick: no signed-in browsing in Harvest v1; `IConnectionResolver` is reserved for API-token connections in private containers; the RFQ inbox stays with its consumer
- [ ] T8-16 (T5-16, T7-P16) partitions and console backplane → provisional pick: Harvest `maintenance` job behind `IPartitionMaintainer` and `NOTIFY` in Harvest first; lift to core `Data` / `Realtime` when Logs (#6) or a second multi-replica service needs them
- [ ] T8-17 (T5-5, T6-14) database image → provisional pick: `postgres:16-alpine` with `pg_trgm` and the boot self-test; code-made UUIDv7; embeddings wait on a custom image with pgvector (T6-8)
- [ ] T8-18 first slice → provisional pick: § 7 steps 0–10 with its gate; link intake and manual entries are slice 2; Social, the pool, render and AI are out
