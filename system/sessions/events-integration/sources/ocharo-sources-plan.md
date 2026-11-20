# Ocharo sources plan

*Written 2026-11-21 for the events-integration orchestrator from a read-only analysis. Lanes build from it; the
orchestrator and the developer own the decisions. Code pins: harvest `527e91b`, ai `1575ea0`, mft-10x-ws `9d060fa`.
Every cost figure says whether it is measured or estimated.*

Developer, 2026-11-21: "plus work on 700+ sources"; "because using that $200 creidt is really important for me, we
can't do it unless we integrate those 700+ resources". The $200 is the monthly API credit of the Claude Console
organization that SCFD's AI layer bills to; it does not roll over. Order and scope: [tasks.md:35-36][t-pull],
[events-integration #74 (`:653-661`)][ei-74] (registering the sources goes to separate chats).

## Status

- ✅ Wave 0: probe ledger and unranked screen (SR01-SR02), 2026-11-21: `source-probes.md` routes all 133 channels
  (generic-site 46, generic-feed 10, generic-structured 1, Telegram 14, Instagram 11, named 6, manual 36, cannot 9);
  `source-screen.md` keeps 32 of 277 unranked hosts; a fresh check found 0 empty routes, 0 contacts, 0 tracking params
- ⬜ Wave 1: generic routes, spend starts (SR03-SR08)
- ⬜ Wave 2: gov.uz and Telegram readers (SR09-SR11)
- ⬜ Wave 3: named event readers (SR12-SR15)
- ⬜ Wave 4: Instagram (SR16)
- ⬜ Wave 5: unranked publishers (SR17)
- ⬜ OQ-1 to OQ-4 answered by the developer

## Verdict

- The "700+" is the event research archive: 911 URLs merged from a 742-URL original and the 724-link export, not
  700 feeds (#1).
- The archive reduces to 100 publishers with 133 pollable channels in the registry, plus about 30 recurring
  publishers (estimate) among 277 unranked hosts (#1).
- Full rollout yields about 480 posts a day (estimate, range ~250-750) (#4).
- At Haiku 5.5, today's route, full rollout spends about $8 a month: 4% of the credit. Volume alone cannot spend it (#5).
- Sonnet 5.5 on `post-tags` turns the same volume into about $130 a month, near Ocharo's 70% share of $140; it is one
  Wheelhouse value (OQ-2).
- Wave 1 routes registry channels with RSS, Atom, ICS, JSON-LD or a sitemap to the generic readers that already exist;
  it needs 3 profiles and a cadence change, no new reader (#6).
- Harvest has one writer at a time: `ev-build` until its selector cutover (~11-24), then lane `src-build`; lane
  `src-probe` writes only this folder meanwhile (#7).

---

## 1. Where the sources are

| List | Where | Count | Role |
|---|---|---|---|
| Link export | mft-10x-ws [`och-event-source-links.md:3`][m-links] | 724 links in 8 topic sections | the list the developer counts as "700+" |
| Event source archive | [`ocharo-event-sources.md:3`][m-archive], [`ocharo-event-source-groups.json:5-11`][m-groups] | 911 URLs: 533 tied to ranked groups, 378 unranked in 277 host buckets | research record; private, it holds personal activity notes |
| Ranked groups | [`ocharo-event-source-priorities.md:5`][m-prio], [`:56`][m-prio-checks] | 100 groups; 89 of 100 primary URLs readable on 2026-11-09 | the shortlist |
| Registry | harvest [`ocharo-event-sources.json`][h-reg-json] | 100 publishers, 188 channels; 6 harvested | what `ocharo setup` reads |

- Most archive URLs are single articles, past editions, forms and PDFs; the registry's rule keeps them out of fetch
  seeds ([`ocharo-source-registry.md:22-24`][h-reg-rule]).
- Unranked hosts: 277 buckets, 220 holding one URL; `.uz` 47, `.ru` 34, `.kz` 13, `.tj` 6, `.kg` 3, `.az` 3, `.tm` 1,
  other 170. Most are one-off citations (news articles, forms, standards pages such as `w3.org`).
- Recurring publishers among them (estimate ~30): design and fashion media (`podium.uz`, `tashkentdesignweek.uz`),
  fairs (`jewelryfair.uz`, `showpro.uz`), Kazakh media and ticketing (`esquire.kz`, `kassir.kz`), Russian fashion weeks
  (`moscowfashion.ru`, `mffrussia.com`). SR02 decides.

**By kind**, registry channels; pollable = every mode except `reference`:

| Kind | Channels | Pollable | Modes today |
|---|---|---|---|
| Website | 157 | 103 | 6 `harvest` · 79 `planned` · 18 `manual` · 54 `reference` |
| Telegram channel | 18 | 17 | 17 `manual` · 1 `reference` |
| Instagram profile | 11 | 11 | 5 `provider` · 6 `manual` |
| Facebook page | 2 | 2 | 2 `manual` |
| Marketplace (OLX and similar) | 0 | 0 | none; OLX, BirBir, Joymee and Domtut readers serve Haven |
| Total | 188 | 133 | |

- Archive URLs by kind: web pages 796, Telegram 50 (25 channel handles, the rest posts and third-party mirrors), PDF 29,
  forms, shared files and chat links 17, Instagram 15 (11 profiles), video 2, Facebook 2.

**By country:**

| Country | Publishers | Pollable channels | Archive URLs by domain |
|---|---|---|---|
| Uzbekistan | 85 | 114 | 416 `.uz` |
| Kazakhstan | 8 | 12 | 56 `.kz` |
| Kyrgyzstan | 3 | 3 | 10 `.kg` |
| Tajikistan | 1 | 2 | 7 `.tj` |
| Several Central Asian countries | 3 | 2 | — |
| Russia and elsewhere | 0 | 0 | 49 `.ru`, 5 `.az`, 1 `.tm`, 367 other (many `.com` publishers are Uzbek) |

**By what they publish:**

| Publishes | Publishers | Source types |
|---|---|---|
| Events, calls and deadlines | 83 | Authority 24, Organizer 23, Media 12, Institution 7, Venue 5, Education 4, Industry body 2, Museum 2, 4 single types |
| Events with ticket or admission offers | 17 | Ticketing 7, Directory 8, Aggregator 2 |
| Listings | 0 | — |

---

## 2. Collectors by kind

- Named readers in harvest `sources/`: Afisha, ANONS, Craftfair, Uzexpocentre, CAEx (events); Instagram Business
  Discovery (official API); OLX, BirBir, Joymee, Domtut (Haven's listings).
- Generic readers in `packages/Module/Readers/` parse sitemaps, RSS, Atom, ICS, JSON-LD `Event` and plain pages, behind
  adapters `generic-site`, `-structured`, `-page`, `-feed`, `-link` ([`readers.md:16-19`][h-readers]).
- The registry routes only to 6 profiles ([`OcharoSourceRegistry.cs:13-21`][h-profiles]), so no registry channel
  reaches a generic reader until S21 ([tasks-scfd.md:439][t-s21]).
- No Telegram reader exists; the `Telegram` family is declared only ([`SourceFamily.cs:30-31`][h-family]).

| Method (registry) | Pollable | Works as-is | Needs building | Cannot within the rules |
|---|---|---|---|---|
| `index-detail` | 20 | 4: Afisha ×2, ANONS, Craftfair | 16: `generic-structured` where JSON-LD `Event` shows, else a named reader (iTicket, Human House, BMCA, CatExpo, CCA, Bukhara Biennial, Idem, EventFlow, EventGo, Sxodim, 10times, KFW, flower festival, Afisha calendar) | ANONS answers a Cloudflare challenge on dev ([events-integration #72, `:638-640`][ei-72]); Craftfair is paused on its passive check ([events-integration #69, `:598-599`][ei-69]) |
| `calendar-rows` | 5 | 2: CAEx, Uzexpocentre | Atakent, Compass Mall | Iteca calendar served a browser challenge; stays manual |
| `news-index` | 46 | 0 | a `gov.uz` reader for 19 (S23 widened, [tasks-scfd.md:465][t-s23]); `generic-feed` for the 27 others where RSS exists; Hunarmand calls (S22) | — |
| `edition-page` | 10 | 0 | `edition-page` reader (S19, [tasks-scfd.md:406][t-s19]) or `generic-structured` | — |
| `ticket-index`, `aggregator-index` | 6 | 0 | S26 iTicket and ShowGo ([tasks-scfd.md:515][t-s26]); GTickets, Olbilet, Idem, VisitUzbek | Ticketon answered 403 (a `manual-review` row) |
| Telegram (`manual-social`) | 17 | 0 | `telegram-preview` over `t.me/s/{username}` (S24, [tasks-scfd.md:480][t-s24]) | — (`t.me/robots.txt` 404, no login) |
| Instagram (`official-instagram` + `manual-social`) | 11 | 5 once the token and Meta grant exist (S25 shipped, [integration-whats-left.md:70][t-s25]) | the 6 manual profiles move to `provider` where Business Discovery answers | a non-business account; scraping |
| Facebook (`manual-social`) | 2 | 0 | — | login wall; no account session |
| `manual-review` | 16 | 0 | re-probe; most read `limited`, `unavailable` or `indexed` | a render-only page while no renderer is bound ([`readers.md:25`][h-render]) |

- Integrations for proxies, CAPTCHA and account sessions stay disabled; S34 drops the first two from the public image.

---

## 3. Registering one source

| Step | What | Where |
|---|---|---|
| 1 Probe | 1 paced GET of `robots.txt` and the channel, identified agent; record the route, feed URL and date in the channel's `note` and `reviewedOn` | by hand, one-time work ([events-integration #52, `:202`][ei-52]) |
| 2 Registry row | `mode: harvest`, `adapterKey`, `setup: default` (bulk) or `selected`; only an `owned` channel with a unique seed passes | [`ocharo-event-sources.json`][h-reg-json]; checks [`OcharoSourceRegistry.cs:95-108`][h-validate] |
| 3 Collector | a `CollectionProfile` for the key; a reader under `sources/{Name}/` when no generic route fits, with trimmed fixtures and synthetic contacts | [`OcharoSourceRegistry.cs:13-21`][h-profiles] |
| 4 Selector | add the publisher to `ocharo-selector.json`, or its matches never reach Ocharo | [`ocharo-selector.json:18-23`][h-selector] |
| 5 Release | push to `main`; CI releases `v0.2.N`; Wheelhouse deploys `harvest-dev` | [tasks-scfd.md:29-30][t-release] |
| 6 Provision | Wheelhouse Run on `harvest-dev`: `ocharo setup --group <id>… --model-processing auto --schedules --selector --selector-reset`; it creates the source (robots obeyed), pipeline, capture (6 h) and check (24 h) schedules and a subscription; reruns reuse ids | [`OcharoSetupVerb.cs:14-34`][h-verb], [`OcharoSourceProvisioner.cs:97-183`][h-prov], dev proof [v0.2.md:389-390][h-v02-setup] |
| 7 AI | an `auto` source queues `post-tags` on each post write; `post-tags backfill --source <id>` covers stored posts | [`tagging.md:15-19`][h-tagging-queue] |
| 8 Read back | `ocharo status --group <id>…`: schedules and each latest run `ok` or `partial/page_limit`; `post-tags report --since <date>`: answers and cost | [`OcharoSetupVerb.cs:31-33`][h-verb] |

Bulk:

- Mark every ready channel `setup: default`; one `ocharo setup` with no `--group` provisions every default channel
  ([`OcharoSourceRegistry.cs:50`][h-routes]).
- `--group` refuses a publisher with no collector ([`OcharoSourceProvisioner.cs:52-57`][h-refuse]), so a bulk list names
  ready publishers only.
- Gaps the waves close:
  - every pipeline gets a fixed 6-hour interval ([`:137`][h-sched]) with `MaxPages` 5 ([`:156`][h-limits]); SR03 adds
    a per-profile cadence
  - setup adds one `ocharo-fashion-v1` subscription per channel ([`:163-183`][h-subs]), redundant after the selector
    cutover; SR03 drops it once SL9 ships
  - the selector names publishers by hand and refuses an empty list ([`OcharoSelector.cs:85-88`][h-sel-validate]); SR04

---

## 4. Throughput and load

- Posts a day now: Afisha gained 88 posts over 2026-11-10 to 11-16 (19, 13, 8, 6, 3, 34, 5), measured by the
  orchestrator's dev diagnosis (`harvest-dev-failures.md:87`, scratchpad, not in git); the Ocharo container held 157
  posts on 2026-11-20 ([v0.2.md:395][h-v02-preview]).
- Posts a day per wave are estimates per channel type: organizer, venue and edition sites 0.2-1; specialist news 2;
  `gov.uz` sections 5; Telegram 5; ticketing and aggregators 15; culture sections of general news 7; Instagram
  profiles 1; unranked publishers 2.

| After | New channels | Posts a day (estimate) |
|---|---|---|
| Today | 6 | ~15 |
| Wave 1 | ~25 | ~105 |
| Wave 2 | +37 | ~290 |
| Wave 3 | +30 | ~410 |
| Wave 4 | +11 | ~420 |
| Wave 5 | +~30 | ~480 |

- Pacing: one connection per host lane; a host without a stored pace waits 2 s between requests, an operator sets
  1-60 s ([`SourceConstants.cs:22-28`][h-pace], [`engine.md:12-16`][h-lanes]).
- A refusal pauses the lane 15 min, doubling per refusal in a row ([`HarvestEngineOptions.cs:20-21`][h-backoff],
  [`engine.md:37-39`][h-refusal]); Telegram reads at 10 s and 3 pages (S24); ANONS is under test at 30 s and 6 pages
  ([v0.2.md:378][h-v02-anons]).
- Run bounds: `MaxPages` 5 (listing and detail together), 150 items, 180 requests, 10 min
  ([`OcharoSourceProvisioner.cs:156`][h-limits]); an index-detail channel admits ~4 new details a run, ~16 a day at 6 h.
- A feed reads its window in one fetch per run ([`GenericSourceAdapter.cs:43-51`][h-generic]), so feeds escape the
  page bound.
- Load at full rollout: ~160 pipelines × (4 captures + 1 check) = ~800 runs and at most ~4,000 fetches a day, about 3 a
  minute; the busiest lane, `gov.uz` with 20 channels, takes ≤ 400 fetches, ~15 min of lane time at 2 s.
- The tagging worker claims 10 posts a pass and polls every 5 s when idle
  ([`PostTagsOptions.cs:22-25`][h-tag-worker]); its capacity is far above 1,000 posts a day.
- Cron cadence exists ([`ScheduleMode.cs:12-13`][h-cron]): captures in 4 daily windows bunch tagging into bursts that
  keep the prompt cache warm (#5).

---

## 5. AI spend

- Provider and model: Anthropic `claude-haiku-5-5` is the default route of `post-tags` and extraction
  ([`tagging.md:25-28`][h-tag-route], [`extraction.md:19`][h-ext-route]); the key on `harvest-dev`
  ([`deploy.yml:72-81`][h-deploy]) bills the Console organization's credit.
- Prices per 1M tokens ([`003-seed-prices/Apply.sql:8-10`][a-prices]): Haiku 5.5 $0.10 in, $0.50 out, $0.125 cache
  write, $0.01 cache read; Sonnet 5.5 $2, $10, $2.50, $0.10. The runner bills each attempt by these ([`PriceMath.cs:25-35`][a-math]).
- The system prompt carries a 5-minute cache mark ([`AiModelCaller.cs:174`][a-cache]); `post-tags` puts the whole
  taxonomy there ([`post-tags.md:33-35`][h-tag-cache]).
- The current cycle ends 2026-11-24 ([ai `context.md:27-28`][a-cycle]: about 70% Ocharo, 30% Haven); this plan spends
  the cycle that starts then. Haven's share also idles while OLX blocks dev fetches ([v0.2.md:334][h-v02-olx]).

| Pass | Tokens per call | Haiku $ per call | Sonnet $ per call | Basis |
|---|---|---|---|---|
| Layer 1 `post-tags` system: instructions + taxonomy | ~12,000 cached | — | — | estimate: 657 nodes render 37,932 chars ([`011-taxonomy`][h-taxonomy], [`PostTagsStore.cs:81-86`][h-tax-render], [`tagging.md:11-14`][h-tax-doc]) ≈ 10,800 tokens + ~1,200 instructions |
| Layer 1 user: title, text ≤ 4,000 chars, fields | ~1,000 in, ~400 out | — | — | estimate ([`PostTagsOptions.cs:12`][h-tag-chars]) |
| Layer 1, warm cache | | $0.00042 | $0.0072 | estimate |
| Layer 1, cold cache (write) | | $0.0018 | $0.036 | estimate |
| Layer 1, paid on dev | — | not measured | — | dev evals answered from the AI store at $0 ([v0.2.md:364-366][h-v02-tags]); SR07 measures |
| Layer 2 `extract-event` | 4.2k | $0.0003 | ~$0.006 | measured on dev, Haiku ([v0.2.md:386][h-v02-ext]); Sonnet ≈ 20× ([`extraction.md:19`][h-ext-route]) |
| `ocharo-relevance` eval, 10 posts | 1,571 in, 166 out | $0.000173 | $0.003473 | measured ([ai v0.3.md:67-74][a-eval]); both 90% |

- Projection rules: Layer 1 calls = posts × 1.15 (changed revisions); Layer 2 on 10% of posts, on Haiku; captures in 4
  cron windows give ~10 cold calls a day.
- Per 100 posts a day: Haiku ≈ $1.5 a month; Sonnet on `post-tags` ≈ $25 a month. Fixed cold-cache cost: Haiku
  ≈ $0.5, Sonnet ≈ $9 a month.

| After | Posts a day | Haiku $ a month | Sonnet `post-tags` $ a month | Sonnet share of $200 |
|---|---|---|---|---|
| Today | ~15 | ~0.6 | ~12 | 6% |
| Wave 1 | ~105 | ~2.0 | ~35 | 18% |
| Wave 2 | ~290 | ~4.9 | ~81 | 41% |
| Wave 3 | ~410 | ~6.7 | ~111 | 56% |
| Wave 4 | ~420 | ~6.9 | ~113 | 57% |
| Wave 5 | ~480 | ~7.8 | ~128 | 64% |
| + whole-site general news (OQ-3 a) | +~350 | +5.4 | +87, total ~216 | 108% |
| Staggered schedules, ~200 cold calls a day | | +8 | +173 | |

- Every row is an estimate; posts a day carry about ±50%, token sizes about ±30%. SR07 replaces them with measured
  rows from `post-tags report` and `extract report`.
- Haiku leaves about 96% of the credit unspent at full rollout; the model route, not the source count, sets the spend.
- Staggered 6-hour intervals cost Sonnet more in cache writes than in tagging; SR03's cron windows guard it.
- The month overshoots $200 only with whole-site news on Sonnet; SR18's weekly line catches it before the bill.

**Spend log (SR18)**, harvest-dev, measured from `post-tags report` and `extract report`:

- 2026-11-21: since 2026-11-13, `post-tags` 405 attempts, 183,770 micro-USD (~$0.18), Haiku 5.5 until SR08; the first
  Sonnet 5.5 call cost 44,851 micro-USD (a cold cache write); `extract-event` 48 attempts, 15,426 micro-USD;
  `extract-listing` 0. Projection not yet meaningful: Wave 1 not provisioned.

---

## 6. Waves

| Wave | Scope | Build | Spend | Done when |
|---|---|---|---|---|
| 0 Probe | 133 pollable channels, 277 unranked hosts | none: hand probes into `source-probes.md` here | none | every channel and host has a route or a `drop`, with a date (SR01-SR02) |
| 1 Generic routes | channels SR01 finds with RSS, Atom, ICS, JSON-LD or a sitemap, est. ~25: specialist media, culture sections, organizer sites | 3 profiles, cron cadence, selector follows every provisioned publisher (S21) | starts, soonest; ~$35 a month on Sonnet | `ocharo status` lists each Wave 1 channel with schedules, latest runs `ok` or `partial/page_limit`, `post-tags report` shows their done answers (SR06) |
| 2 gov.uz and Telegram | 20 `gov.uz` channels, 17 Telegram channels | 2 readers (S23 widened, S24) | ×2.8 | the same read-back for Wave 2, plus a measured 7-day spend row (SR11) |
| 3 Named event readers | 10 edition pages, 6 ticketing and aggregators, Hunarmand calls, index-detail and calendar channels without a generic route | S19, S22, S26 and small readers | +40% | the same read-back for Wave 3 (SR15) |
| 4 Instagram | 11 profiles | none (S25 shipped); the developer's Business account, token and Meta grant | small | Instagram Phase 1 acceptance, 11 sources with capture schedules (SR16) |
| 5 Unranked publishers | ~30 kept by SR02 | registry groups ranked 101+; generic or Telegram routes | +15% | the same read-back over the new groups (SR17) |

- Wave 1 spends soonest with the least build: the readers exist, only routing and cadence change.
- Out of every wave: 55 `reference` channels, 2 Facebook pages, the Iteca calendar, Ticketon, render-only pages and
  one-off archive URLs.

---

## 7. Lanes

| Lane | Model | Writes | Takes | Window |
|---|---|---|---|---|
| `ev-build` (existing) | Opus | harvest, events | the selector cutover; then hands harvest over | until ~2026-11-24 |
| `src-probe` (new) | Sonnet `medium` agent or fork | wow-two-ws `system/sessions/events-integration/sources/` only | Wave 0 (SR01, SR02, SR18) | from 2026-11-21 |
| `src-build` (new) | Opus orchestrates; Sonnet `xhigh` builds readers, Sonnet `medium` runs Wheelhouse steps | `wow-two-sdk-beta.harvest`; `harvest-dev` through Wheelhouse Run | Waves 1-5 code and provisioning, in order | from `ev-build`'s hand-over |

- Two lanes never write harvest at once: `src-build` starts after `ev-build` hands harvest over; if `ev-build` keeps
  harvest past 11-24, it takes SR03-SR06 itself and `src-build` waits.
- No wave writes `ocharo-platform`, events, the AI repo or mft-10x-ws: the selector carries delivery and the model route
  is a Wheelhouse value.
- `wow-two-sdk-beta.harvest-adapters` is retired (events-integration #63); nothing goes there.

---

## 8. Open decisions

**OQ-1 What "the 700+" covers.** The archive is the research list of 911 URLs; a channel is one pollable URL of a
publisher (a page, feed or account) that `ocharo setup` turns into a pipeline with schedules.

- (a) Register the registry's 133 pollable channels and the ~30 recurring publishers SR02 keeps: ~160 channels.
- (b) Register every archive URL: 700-900 seeds, mostly single articles, past editions and forms; they re-read dead
  pages for ever and break the registry's seed rule.
- Pick: (a).

**OQ-2 How the credit gets spent.** Layer 1 (`post-tags`) tags every new or changed post; Layer 2 (extraction) parses
only posts a subscriber's (type, domain) pairs want; the route is the model list a Wheelhouse value sets.

- (a) Haiku 5.5 everywhere: ~$8 a month at full rollout; ~96% of each cycle's credit lapses.
- (b) Sonnet 5.5 on `post-tags` with Haiku as its fallback, extraction on Haiku: ~$35 after Wave 1, ~$130 at full
  rollout; back to Haiku when SR18 projects past $140.
- (c) Haiku tags plus Sonnet extraction widened to every event post: ~$40 a month at full rollout.
- Pick: (b). It is one reversible value, and an Anthropic-only route draws all of it on the credit. Both models
  scored 90% on the first eval, so SR07 measures whether Sonnet's tags earn the spend.

**OQ-3 General news sites.** Seven P3 publishers are whole newsrooms (`gazeta.uz`, `uza.uz`, `uzdaily.uz`,
`kabar.kg`, `yuz.uz`, `dunyo.info`, `namangantoday.uz`), each ~50 articles a day, few about fashion.

- (a) Whole-site feeds: +~350 posts a day; on Sonnet the month passes $200.
- (b) Culture or events sections only; a site without one stays `planned`.
- (c) Leave them out.
- Pick: (b).

**OQ-4 Hosts that challenge the reader.** A challenge is a JavaScript or browser check; the rules never solve or bypass
one, and a challenge pauses the host's lane. ANONS challenges dev, Craftfair's complete pages carry Cloudflare's passive
script that trips the detector, the Iteca calendar served a browser challenge, Ticketon answered 403.

- (a) Keep them paused or manual; their events also arrive through Afisha, organizers and Telegram.
- (b) A dedicated outgoing server per host: allowed; a challenge there still pauses.
- (c) For Craftfair only, read a complete 200 page carrying the passive script as content: the page is served, nothing
  is solved.
- Pick: (a) for ANONS, Iteca and Ticketon; (c) for Craftfair.

---

## 9. Tasks

| Id | Repo | What | Done when (pass/fail) | Depends |
|---|---|---|---|---|
| SR01 | wow-two-ws | Probe the 133 pollable registry channels: `robots.txt` and the channel, 1 paced GET each, identified agent, never past a challenge; per row record route (`generic-feed`, `generic-structured`, `generic-site`, a named key, `telegram-preview`, `instagram-api`, `manual`, `cannot`), feed URL, robots verdict, date in `sources/source-probes.md` | 133 rows, each with a route and a date; every `cannot` row names its rule | — |
| SR02 | wow-two-ws | Screen the 277 unranked host buckets of [`ocharo-event-source-groups.json`][m-groups]: drop one-off citations (forms, PDFs, single articles, standards pages) from the URL alone; probe the rest as SR01; no personal names | 277 rows marked `keep` or `drop` with a reason; every `keep` has a probe row and a proposed group id, tier and country | SR01 |
| SR03 | harvest | S21 profiles: `generic-feed`, `generic-structured`, `generic-site` in `OcharoSourceRegistry.Profiles`; `CollectionProfile` gains a capture cadence (default cron `0 1,7,13,19 * * *`, `Asia/Tashkent`) read by the provisioner instead of the fixed 6 h; once SL9 ships, setup adds no per-channel `ocharo-fashion-v1` subscription | `OcharoRegistryTests` covers a generic route and a profile cadence; `dotnet test be/SCFD.BackendServices.slnx` passes | `ev-build` hand-over |
| SR04 | harvest | Selector follows every provisioned registry publisher: the file lists each publisher with a collector, or takes a registry-wide form that `Resolve` binds to every container group | `OcharoSelectorTests` pass; `--selector-reset` on dev shows the Wave 1 publishers in the preview's per-source counts | SR03 |
| SR05 | harvest | Wave 1 registry: SR01's generic-route channels to `mode: harvest`, a generic `adapterKey`, `setup: default`; 1 trimmed fixture per route family with synthetic contacts | `OcharoRegistryTests` pass; each family's fixture parses ≥ 1 dated item | SR01, SR03 |
| SR06 | harvest-dev | Release; Wheelhouse Run `ocharo setup --model-processing auto --schedules --selector --selector-reset`; then `ocharo status` and `post-tags report --since <release day>` | every Wave 1 channel shows capture and check schedules; each latest run `ok` or `partial/page_limit`; done answers from Wave 1 sources | SR04, SR05 |
| SR07 | harvest-dev | 7 days after SR06: `post-tags report`, `extract report` and posts a day per source; write the measured rows into #5 | #5 holds measured cost per post and posts a day; the estimate rows it replaces say so | SR06 |
| SR08 | harvest-dev | Apply OQ-2: `Harvest:Processing:Tags:Models:0` = `anthropic/claude-sonnet-5-5`, `:1` = `anthropic/claude-haiku-5-5` in Wheelhouse; no OpenAI route | a new processed card's provider mark reads Sonnet 5.5; `post-tags report` lists Sonnet attempts | OQ-2, SR06 |
| SR09 | harvest | `gov.uz` reader (S23 widened): one source, each of the 20 registry `gov.uz` channels a section, one paced lane | fixture tests per index layout pass; a bounded local run captures ≥ 1 article with `postedAt` from 2 sections | SR03 |
| SR10 | harvest | Telegram reader (S24): `telegram-preview` over `t.me/s/{username}`, 10 s pace, 3 pages; registry switches the channels SR01 found dated | unit tests over a synthetic channel read ids, times and an edit as a revision; a bounded local run captures ≥ 1 dated post | SR01, SR03 |
| SR11 | harvest-dev | Wave 2 provisioning and read-back as SR06; 7-day spend row in #5 | as SR06 for Wave 2 channels; the row is in #5 | SR09, SR10 |
| SR12 | harvest | Edition pages (S19) for the 10 `edition-page` channels | S19's checks pass ([tasks-scfd.md:406][t-s19]) | SR03 |
| SR13 | harvest | Ticketing and aggregators: S26 (iTicket, ShowGo); GTickets, Olbilet, Idem, VisitUzbek through `generic-structured` where SR01 found JSON-LD, else a reader | fixture tests per site pass; a bounded local run captures ≥ 1 dated event each; S26's merge test passes | SR01, SR03 |
| SR14 | harvest | Hunarmand calls (S22) and the index-detail and calendar channels SR01 left without a generic route | a fixture test and a bounded local run per reader pass | SR01, SR03 |
| SR15 | harvest-dev | Wave 3 provisioning and read-back as SR06 | as SR06 for Wave 3 channels | SR12, SR13, SR14 |
| SR16 | harvest-dev | Wave 4: Instagram Phase 1 acceptance (harvest `instagram.md`), then the 11 profiles with `--instagram` and schedules on | `ocharo status` lists 11 Instagram sources with capture schedules; one scheduled capture saves posts | the developer's Business account, token and Meta grant |
| SR17 | harvest | Wave 5: SR02's kept publishers as registry groups ranked 101+, routes per SR02; provision as SR06 | `OcharoRegistryTests` pass with the new ranks; SR06's read-back passes over the new groups | SR02, SR03, SR10 |
| SR18 | wow-two-ws | Weekly spend line in #5 from the build lane's `post-tags report`; flag a month projected past $140 | one dated line a week through the cycle | SR06 |

---

<!-- Evidence. wow-two-ws docs are relative; code is pinned. -->

[t-pull]: ../tasks/tasks.md
[t-release]: ../tasks/tasks-scfd.md
[t-s19]: ../tasks/tasks-scfd.md
[t-s21]: ../tasks/tasks-scfd.md
[t-s23]: ../tasks/tasks-scfd.md
[t-s24]: ../tasks/tasks-scfd.md
[t-s26]: ../tasks/tasks-scfd.md
[t-s25]: ../tasks/integration-whats-left.md
[ei-52]: ../events-integration.md
[ei-69]: ../events-integration.md
[ei-72]: ../events-integration.md
[ei-74]: ../events-integration.md

[m-links]: https://github.com/sulton-max/mft-10x-ws/blob/9d060fa67cd0896623d7e796095970bf3ca0176f/output/och-event-source-links.md#L3
[m-archive]: https://github.com/sulton-max/mft-10x-ws/blob/9d060fa67cd0896623d7e796095970bf3ca0176f/output/ocharo-event-sources.md#L3
[m-groups]: https://github.com/sulton-max/mft-10x-ws/blob/9d060fa67cd0896623d7e796095970bf3ca0176f/output/ocharo-event-source-groups.json#L5-L11
[m-prio]: https://github.com/sulton-max/mft-10x-ws/blob/9d060fa67cd0896623d7e796095970bf3ca0176f/output/ocharo-event-source-priorities.md#L5
[m-prio-checks]: https://github.com/sulton-max/mft-10x-ws/blob/9d060fa67cd0896623d7e796095970bf3ca0176f/output/ocharo-event-source-priorities.md#L56

[h-reg-json]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/sources/Module/Ocharo/ocharo-event-sources.json
[h-reg-rule]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/research/ocharo-source-registry.md#L22-L24
[h-profiles]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/sources/Module/Ocharo/OcharoSourceRegistry.cs#L13-L21
[h-routes]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/sources/Module/Ocharo/OcharoSourceRegistry.cs#L50
[h-validate]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/sources/Module/Ocharo/OcharoSourceRegistry.cs#L95-L108
[h-refuse]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/sources/Module/Ocharo/OcharoSourceProvisioner.cs#L52-L57
[h-prov]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/sources/Module/Ocharo/OcharoSourceProvisioner.cs#L97-L183
[h-sched]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/sources/Module/Ocharo/OcharoSourceProvisioner.cs#L135-L140
[h-limits]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/sources/Module/Ocharo/OcharoSourceProvisioner.cs#L156
[h-subs]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/sources/Module/Ocharo/OcharoSourceProvisioner.cs#L163-L183
[h-verb]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/service/HarvestSources.Api/Ocharo/OcharoSetupVerb.cs#L14-L34
[h-selector]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/sources/Module/Ocharo/ocharo-selector.json#L18-L23
[h-sel-validate]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/sources/Module/Ocharo/OcharoSelector.cs#L85-L88
[h-readers]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Module/Readers/readers.md#L16-L19
[h-render]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Module/Readers/readers.md#L25
[h-generic]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Module/Readers/GenericSourceAdapter.cs#L43-L51
[h-family]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Abstractions/Sources/SourceFamily.cs#L30-L31
[h-pace]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Abstractions/Sources/SourceConstants.cs#L22-L28
[h-lanes]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Module/Engine/engine.md#L12-L16
[h-refusal]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Module/Engine/engine.md#L37-L39
[h-backoff]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Module/Engine/HarvestEngineOptions.cs#L20-L21
[h-cron]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Abstractions/Pipelines/ScheduleMode.cs#L12-L13
[h-tag-worker]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Module/Tagging/PostTagsOptions.cs#L22-L25
[h-tag-chars]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Module/Tagging/PostTagsOptions.cs#L12
[h-tax-doc]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Module/Tagging/tagging.md#L11-L14
[h-tagging-queue]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Module/Tagging/tagging.md#L15-L19
[h-tag-route]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Module/Tagging/tagging.md#L25-L28
[h-tax-render]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Module/Tagging/PostTagsStore.cs#L81-L86
[h-taxonomy]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/codebase/harvest.backend-services/packages/Module/Migrations/011-taxonomy/Apply.sql
[h-tag-cache]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/development/post-tags.md#L33-L35
[h-ext-route]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/development/extraction.md#L19
[h-deploy]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/deployment/deploy.yml#L72-L81
[h-v02-olx]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/planning/version-track/v0.2/v0.2.md#L334
[h-v02-tags]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/planning/version-track/v0.2/v0.2.md#L364-L366
[h-v02-anons]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/planning/version-track/v0.2/v0.2.md#L378
[h-v02-ext]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/planning/version-track/v0.2/v0.2.md#L386
[h-v02-setup]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/planning/version-track/v0.2/v0.2.md#L389-L390
[h-v02-preview]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/527e91b2e7b65bb682cbc409c09b3849f65bf661/engineering/planning/version-track/v0.2/v0.2.md#L395

[a-prices]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.ai/blob/1575ea03196bb91a5b65bd21358b5ce38024539f/engineering/codebase/ai.backend-services/packages/Module/Migrations/003-seed-prices/Apply.sql#L8-L10
[a-math]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.ai/blob/1575ea03196bb91a5b65bd21358b5ce38024539f/engineering/codebase/ai.backend-services/packages/Module/Prices/PriceMath.cs#L25-L35
[a-cache]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.ai/blob/1575ea03196bb91a5b65bd21358b5ce38024539f/engineering/codebase/ai.backend-services/packages/Providers/Internal/AiModelCaller.cs#L174
[a-eval]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.ai/blob/1575ea03196bb91a5b65bd21358b5ce38024539f/engineering/planning/version-track/v0.3/v0.3.md#L67-L74
[a-cycle]: https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.ai/blob/1575ea03196bb91a5b65bd21358b5ce38024539f/product/context.md#L27-L28
