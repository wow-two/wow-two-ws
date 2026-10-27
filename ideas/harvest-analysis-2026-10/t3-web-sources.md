# T3 — Web sources

*Last updated: 2026-10-26*

> The web half of Harvest's source families: what ListingShelf's page client and brokers give the family, the seven
> shapes a web source takes (static page, structured data, whole-site harvest, browser render, provider API, feed,
> link intake), the behaviour Harvest keeps at every site, build against wrap for the crawler stack, and a profile of
> the Uzbekistan event sites plus the nine links Ocharo reviewed. Result: build the family in .NET on ListingShelf's
> bounded client with AngleSharp and a separate Playwright worker, wrap nothing in P1, read structured data before
> any LLM, and treat Afisha's terms and iticket's client-rendered shell as the two gates on the first Events
> sources.

Legend: **(U)** = could not verify. All sites and docs read 2026-10-26. Route codes — **R1** structured data, AI-free
· **R2** static HTML, selectors or LLM · **R3** sitemap-driven whole-site · **R4** browser render · **R5** API or JSON
· **R6** feed · **R7** gated (challenge, terms, permission). Sizes are bytes as received without `Accept-Encoding`
(uncompressed). Paths are from the 10x-ws workspace root.

Site requests: plain GETs from the developer's Mac with the UA `Mozilla/5.0 (compatible; WoW2-Harvest-research/0.1; +https://github.com/wow-two)`,
no sign-in, no forms, no crawling. Per site: home, `robots.txt`, `sitemap.xml`, one content page. Exceptions:
`afisha.uz` took ~12 GETs because its sitemap is an index (I read 5 child files); the first `iticket.uz` home
request followed 50 redirects in a loop (no cookie support) before curl stopped it. No undocumented API endpoint was
called.

---

## 1. Reuse from ListingShelf

Code read: `IListingBroker.cs`, `HtmlListingBroker.cs`, `ListingPageClient.cs`, `RunExecutionService.cs`,
`OlxListingBroker.cs`, `DomtutListingBroker.cs`, `HostConfiguration.Extensions.cs:81-99`,
`ListingSnapshotRepository.cs:29`, `architecture/pipeline-contract.md` (all under
`workbench/maxs-projects/ventures/saas/ventures.listing-shelf/engineering/`).

| Part | Today | Verdict | What changes for the web family |
|---|---|---|---|
| Bounded page client | `ListingPageClient`: 50 s deadline `:16`, 8 MiB cap `:19`, ≤5 manual redirects `:66`, 2 retries at 1 s and 2 s `:39`, streamed read; handler has no auto-redirect and no cookies (`HostConfiguration.Extensions.cs:92-99`) | generalizes; this is the core | returns status, headers, bytes and final URL; media-type allow-list per family (today only `text/html`, `application/xhtml+xml` `:96`); charset-aware decode (today `Encoding.UTF8` `:111`); conditional GET; `Retry-After`; per-host limiter; optional run-scoped cookie jar; UA with a contact (today `ListingShelf/1.0` `:69`) |
| Redirect re-validation | a `validate` callback runs on the start URL and every hop; `ValidateDetailUri` + `IsMissingPage` (`HtmlListingBroker.cs:167-175`) | generalizes | the callback becomes a URL policy: a known-host set for adapters, a public-internet check at connect time for link intake; `IsMissingPage` becomes a per-source gone rule (Domtut: redirect to `/404`) |
| Block outcomes | `ProviderAccessException` + `CompletionReason`: `AccessBlocked` (401/403), `RateLimited` (429), `FetchTimeout`, `NetworkError`, `HttpError`, `UnexpectedContent`, `ResponseTooLarge`, `InvalidRedirect`, `ListingUnavailable`, `UnrecognizedPage` | generalizes | rename `ListingUnavailable` to gone; add `challenge`, `waiting-room`, `robots-disallowed`, `render-required`, `policy-denied`; carry `Retry-After` on `RateLimited` |
| Challenge detection | `IsChallenge` `:323`: title contains "access denied", "just a moment", "captcha", "attention required", or 3 selectors | generalizes as a pluggable detector | misses `<title>One moment, please...</title>` (textileexpo.uz) and a redirect to a queue host (iticket.uz); test the detector against recorded samples |
| JSON-LD reader | `ReadStructuredListing` `:356`, `Flatten` `:377` walk arrays and `@graph`; first node typed Product, Apartment, House, RealEstateListing or Offer | generalizes | return every node by `@type`, with a subtype map (`MusicEvent`, `TheaterEvent` ⊂ `Event`); resolve `@id` references; keep nested `location` and `offers` arrays |
| Fallback chain | title: selector, then JSON-LD `name`, then `og:title` (`:116`); same for description | generalizes | order per source, structured first when present; record which tier supplied each field (provenance for T6) |
| Pagination discovery | `FindNextPage` `:213`, `PreserveFilters` `:290`, `NextSelector`; stop reasons `RepeatedPage`, `RepeatedListings`, `PageLimit`, `ItemLimit` | generalizes | a `ListingPagination` discovery strategy with selectors in source config; keep the guards |
| Run loop | `RunExecutionService`: discover then capture; one item's failure never fails the run; a gone item is a finding (`:198`); `refresh` re-walks the known set (`:215`); stops on block or rate limit | generalizes | needs a durable frontier, resume, and per-host scheduling across runs; today one run at a time with a run-wide 500 ms pause (`RunExecutionSettings.cs`) |
| Change hash | SHA-256 of the normalized `Data` JSON (`ListingSnapshotRepository.cs:29`), not the raw HTML | generalizes | keep two hashes: raw body (was the response identical) and normalized content (did the post change) |
| Listing-specific | `SourcePathPattern`, `ListingPattern`, host-bound `ValidateSourceUri`, title/price/description/seller selectors, `ReadAttributes`, `ImageKey`/`PreferImage`/`ThumbnailUrl`, `PhotoClient`, `ListingData`, `ListingOf` | stays in the listing adapter | OLX and Domtut become one adapter set emitting `wow2.listing.v1` |
| Gaps | no `robots.txt`, no sitemap reader, no feed/ICS/JSON reader, no per-host state, no cookies, no conditional GET; API limits `pageLimit` 1–100 and `itemLimit` 1–2,000 | new work | sections 2 and 3 |

### Seam sketch

```text
UrlPolicy    known hosts | public internet (connect-time IP check)
Fetcher      bounded GET → { status, headers, bytes, finalUrl, outcome }
Discovery    Sitemap | ListingPagination | Feed | SeedList | LinkFollow → discovered URLs
Extractor    JsonLd | Microdata | OpenGraph | Selectors | Feed | Ics | JsonPath | Llm
GoneRule     status | redirect pattern | soft-404 marker | absent from a complete enumeration
```

- an adapter = policy + discovery + extractors + gone rule; OLX and Domtut are two such sets.
- the extractor order is data, per source: `[JsonLd, Selectors, OpenGraph, Llm]`.

---

## 2. Families

| Family | Reads | AI needed | Discovery | Change signal | Gone signal | Seen on |
|---|---|---|---|---|---|---|
| `page` static HTML | server-rendered HTML; CSS selectors, else text for the LLM | selectors none; free text yes | seed URLs, listing pagination | content hash; conditional GET when offered | 404/410, redirect to a not-found page, soft-404 marker | uzexpocentre.uz, kfw.kz, fashionexpo.kz, Tilda sites |
| `structured` | JSON-LD, microdata, OpenGraph inside the page | no; gaps only | as `page` | hash of the normalized node | as `page` | afisha.uz, mstar.uz, voyage.uz |
| `site` (a discovery mode) | every post of a small site | per extractor | sitemap, then pagination, then link-follow | sitemap `lastmod` where trustworthy, else hash | absent from a complete enumeration, then confirmed by a fetch | afisha.uz, iticket.uz, mstar.uz |
| `render` | DOM after JavaScript, or the JSON the page fetched | per extractor | as `site` | hash of rendered DOM or captured JSON | as `page` | iticket.uz (client-rendered shell) |
| `api` | documented or public JSON | no | paging, cursor, `modified_after` | API cursor or `updated` field | tombstone or absence | WordPress REST, Events Calendar REST |
| `feed` | RSS, Atom, ICS | no | the feed URL | item `guid`/`UID` + `updated`; ETag | none; a feed window drops old items | spot.uz RSS (news, not events) |
| `link` | one URL a product submits | optional | none | on demand, optional watch | as `page` | Ocharo's links |

### 2.1 Static HTML pages

- extraction ladder: structured nodes, then CSS selectors in the adapter, then main-content text for the LLM (T6).
- shell check before extraction: body text under ~400 characters inside `#__nuxt`, `#root`, `#app` or `#__next` →
  `render-required`; iticket.uz returns the same 7,024-byte shell for the home page and an event URL.
- free-text tables are better parsed by a selector than the LLM: uzexpocentre.uz's schedule page is one HTML table
  (topic, organizer, date as `01-31.07`, pavilion) with the year only in the heading "JULY–DECEMBER 2026".
- pages are kept as captured bytes plus the decoded text; the decoded form follows the declared charset (all 12
  homes checked declare UTF-8, so the gap is latent).

### 2.2 Structured data

- shapes: JSON-LD (`<script type="application/ld+json">`), microdata (`itemscope`/`itemprop`), OpenGraph/Twitter meta.
  Google documents JSON-LD examples and accepts microdata and RDFa.
- coverage: 51.25% of 2.4 billion crawled pages carry structured data; JSON-LD on ~11.5 M sites, microdata on ~7.6 M
  (Web Data Commons, Common Crawl 2024). In this sample: `Event` nodes on 3 of the 16 sites profiled (afisha.uz,
  mstar.uz, voyage.uz); none on the nine Ocharo links.
- what the three sites give:

| Site | Node | Fields present | Missing |
|---|---|---|---|
| afisha.uz event page | `Event` | `name`, `description`, `image`, `url`, `startDate` (`+05:00`), `location` (`Place` + address + `geo`) | `offers`, `endDate`, `eventStatus`; price only in title/description text ("от 50 000 сумов") |
| mstar.uz event page | `MusicEvent` | `eventStatus`, `eventAttendanceMode`, `performer`, `organizer`, `offers` as `AggregateOffer` (`lowPrice` 200000, `highPrice` 2000000, UZS, `availability`), `startDate` | none that Events needs; the page also carries `FAQPage` |
| voyage.uz `/events` | `ItemList` of 4 `Event` | `startDate`, `endDate`, `eventStatus`, `eventAttendanceMode`, `location`, `offers` (URL points to iticket.uz) | `startDate` of an apparently date-only event is `…T00:00:00.000Z` (U) |

- traps for the extractor (T6) and Events' `When` precision:
  - a date-only event can arrive as midnight UTC (voyage.uz, apparently, U); keep the raw string and infer precision, never trust the time part.
  - Google's status rules: postponed keeps the old `startDate` with `EventPostponed`; rescheduled changes
    `startDate` and may add `previousStartDate` with `EventRescheduled`; cancelled keeps all values with
    `EventCancelled`. Map them to the Events `status` field, never to a gone state.
  - a listing page can embed full nodes (voyage.uz) or only links (mstar.uz home lists 5 events under
    `Organization.event` with only `name`, `url`, `startDate`, `eventStatus`); the detail page is the source of record.
- libraries: AngleSharp + `System.Text.Json` cover JSON-LD and OpenGraph. No maintained .NET extractor for JSON-LD or
  microdata turned up on NuGet (microdata packages found write markup, not read it); microdata is ~100 lines over the
  HTML spec's algorithm. Pick: write both readers in the family.

### 2.3 Whole-site harvest

For small sites such as afisha.uz, iticket.uz, mstar.uz: every available post, on manual or automatic schedules.

**Scope, discovery, change, gone**

- source config: hosts, include/exclude URL patterns, locale policy, discovery strategies in order, revisit policy, gone rules.
- discovery order: `Sitemap:` lines from `robots.txt`, then `/sitemap.xml`, then listing pagination, then seed URLs, then
  link-follow (same host, pattern-bound, depth-capped) as the last resort.
- sitemap limits: 50,000 URLs and 50 MB uncompressed per file, 50,000 children per index; `lastmod` is meant to be the
  page's modification time, not the generation time. Sites break that rule per URL class:

| Site | Sitemap `lastmod` | Trust |
|---|---|---|
| afisha.uz index | 5,358 children, 3,279 distinct values; the 18 children changed since 2026-10-19 are the delta | trust per child |
| afisha.uz `standard-ru.xml` | 61 URLs, 1 distinct value (generation time) | ignore |
| mstar.uz | 10 distinct values over 24 URLs: 15 static URLs carry the fetch time, 9 event URLs carry real dates | trust on `/event/*` only |
| plshawlstoles.com, shawlsandcarpets.com | 1 distinct value for 64 and 57 URLs | ignore |
| iticket.uz, uzexpocentre.uz, fashionexpo.kz | none | hash only |

- rule: store a `lastmod_trust` per source and URL pattern; downgrade it when `lastmod` equals the fetch time or all values are equal.
- conditional GET is not offered by any event page read: afisha.uz event page sends `Cache-Control: private, no-cache, no-store`, no `ETag`; mstar.uz
  sends `public, max-age=60, s-maxage=300`, no `ETag`; iticket.uz's `Last-Modified` matched the fetch minute. Plan on
  sitemap `lastmod` plus normalized-content hash; send validators when a site offers them.
- delta enumeration of afisha.uz: 1 request for the 752 KB index plus the children whose `lastmod` moved (18 in the
  last 7 days, about 3 a day), never the 5,358 files; each moved child then names the pages to fetch.
- afisha.uz's bucket dates are the material's publish date, not the event date (`/ru/theatres/2026/10/26/clowns` has
  `startDate` 2026-11-15). A lookback window therefore reads recent weekly buckets plus the event pages still upcoming.

**Frontier (shape for T5 and T7 to finish)**

- one row per URL: `url_key` (normalized), `source_id`, `state` (`discovered` · `queued` · `fetched` · `gone` ·
  `blocked` · `excluded`), `discovered_via`, `first_seen_at`, `last_enumerated_at`, `sitemap_lastmod`, `etag`,
  `last_modified`, `raw_hash`, `content_hash`, `next_due_at`, `fail_count`, `gone_since`.
- three cadences per source, set separately: `enumerate` (cheap, frequent: sitemap index or listing pages), `fetch`
  (new and changed URLs), `verify` (gone checks). Provisional for events: enumerate hourly, full sweep weekly, verify daily.
- revisit by event time: upcoming within 14 days daily, further out weekly, stop 7 days after `endDate` (provisional).

**Gone detection**

| Signal | Strength | Rule |
|---|---|---|
| 410, or 404 on a direct fetch | strong | `gone` |
| redirect to the site's not-found page or home | strong when a source rule names it (Domtut `/404`) | off-pattern redirect without a rule = `moved`, not gone |
| 200 with a soft-404 marker, or the structured node vanished | medium | `suspect`; confirm on the next fetch |
| absent from a complete enumeration | weak | `suspect` after 1 run, then a direct fetch decides |
| event ended, or `eventStatus` cancelled/postponed | not a deletion | `ended` or a status change; T5 owns the state machine |

- complete enumeration = every child sitemap fetched without error and the URL count within a sane band of the last run
  (guard: a drop above ~30% marks the enumeration suspect and skips absence inference; threshold provisional).

**What a pass costs**

| Site | URLs | Bytes per page | One full pass | At 1 request / 2 s |
|---|---|---|---|---|
| afisha.uz | per 1,000 pages | 159,218 (event page); home 486,194 | ~159 MB | ~33 min |
| iticket.uz | 131 events (shell only; data not in it) | 7,024 | ~0.9 MB | ~4.4 min |
| mstar.uz | 9 events | 30,974 | ~0.28 MB | ~18 s |

### 2.4 Browser-rendered pages

- needed when the static GET returns a shell and the data arrives by script. First case: iticket.uz (Nuxt by markup, v2 by `data-n-head`, U:
  `<div id="__nuxt">`, axios from cdnjs, `window.__NUXT__` holding only `config` with `currency` and `frontUrl`, no JSON-LD).
- order of attempts: (1) JSON the page fetches, found once while authoring the adapter and then called directly when
  `robots.txt` and the terms allow; (2) Playwright render. The endpoints are undocumented, so each adapter gets a
  contract test.
- Playwright .NET `Microsoft.Playwright` 1.64.1 (2026-10-22, MIT); the official image `mcr.microsoft.com/playwright/dotnet`
  is tagged by version and Ubuntu base (`v1.63.0-noble` in the docs) and must match the package version.
- the image ships the browsers, not the package; Microsoft documents it as a testing and development image and does
  not recommend it for untrusted sites. For crawling the docs advise a non-root `pwuser` with a seccomp profile
  (`--security-opt seccomp=…`), plus `--init` and `--ipc=host` (Chromium can otherwise run out of memory).
- cost (U, measure in a spike): several hundred MB per browser process and ~50–150 MB per page; 3–10 s per page against
  ~0.3 s for a static GET. Plan 1–2 concurrent contexts per worker, a fresh context per page, no persisted cookies.
- guardrails: separate worker container with no secrets and no route to internal ranges; block images, fonts, media and
  analytics via request routing; hard per-page timeout; no stealth plugins, no challenge solving.
- output: the rendered DOM plus the JSON responses it fetched; the JSON is the stabler extraction input.
- opt-in per source: `render: never | fallback | required`.

### 2.5 Provider APIs and public JSON

- no documented API found for afisha.uz or iticket.uz (searches 2026-10-26: nothing from either; afisha.uz's
  footer points to the editorial office for reuse).
- documented patterns to look for before page capture:
  - WordPress REST `/wp-json/wp/v2/posts`: `modified_after`, `after`, `orderby=modified`, `per_page` documented. Seen
    sites disallow it (uniticket.uz robots: `Disallow: /wp-json/`).
  - The Events Calendar REST `/wp-json/tribe/events/v1/events`: `start_date`, `end_date`, `page`, `per_page` in the
    plugin's source docs; whether a given site exposes it is per site (U).
  - partner programmes (Ticketmaster Partner API is restricted to distribution agreements) — none apply to UZ today.
- undocumented endpoints the site's own frontend calls (Next.js `/_next/data/…`, Nuxt payloads, XHR JSON): not a
  default route. afisha.uz disallows `/api/` and `/_next`; the adapter would reach them only if `robots.txt` allows
  and the terms do not forbid, and it carries a contract test.
- auth: none for public JSON; provider keys live in the secret store; a quota hit is a `rate-limited` outcome.

### 2.6 RSS, Atom and ICS feeds

- libraries: `System.ServiceModel.Syndication` 10.0.14 (RSS 2.0, Atom), `Ical.Net` 5.2.3 (2026-06-23, MIT).
- discovery: `<link rel="alternate" type="application/rss+xml|atom+xml">` and `.ics`/`webcal://` links. Found on 1 of
  16 sites (spot.uz, a business-news feed, not events).
- item identity: RSS `guid`, Atom `id`, ICS `UID`; ICS `SEQUENCE`, `LAST-MODIFIED` and `STATUS:CANCELLED` carry
  change and cancellation (RFC 5545 §3.8.4.7 UID, §3.8.7 change management, §3.8.1.11 STATUS; property text not re-read, U).
- recurring ICS events: expand `RRULE` into occurrences within a horizon; Events has an occurrence concept for them.
- a feed window drops old items, so absence is never a gone signal; a feed carries `new`/`changed` only.
- prefer a feed over page capture when it carries the fields the schema needs (spec § Behaviour at sources).

### 2.7 Link intake

Any URL a product submits (Ocharo's links, manual entries with a source link).

| Step | Rule |
|---|---|
| 1 normalize | http and https only; no userinfo; IDNA host; drop fragment and tracking parameters (`utm_*`, `fbclid`, …; spot.uz's own `Clean-param` lists them); keep the rest of the query |
| 2 route by pattern | an adapter registry, first match wins; social URLs (`t.me`, `instagram.com`, `x.com`, `facebook.com`, `reddit.com`, `tiktok.com`, `youtube.com`/`youtu.be`, `threads.net`, `linkedin.com`, `vk.com`) go to the T1/T2 adapters; if the adapter is missing or unconfigured, fall back to a link card |
| 3 known public domain? | look up the registrable domain in the public source registry. Hit and URL already captured → return that post. Hit and not captured → queue a single-URL capture inside that public pipeline under its policy and pacing. Miss → step 4 (developer decision 2026-10-26: private container unless the domain is harvested publicly) |
| 4 unknown domain | capture into the product's private container with the `link` pipeline: one bounded fetch, `robots.txt` enforced, outcome codes as in section 3 |
| 5 extraction ladder | JSON-LD/microdata nodes (`Event`, `Product`, `Article`, `Offer`, `LocalBusiness`), then oEmbed, then OpenGraph, then `<title>` and meta description, then the LLM if the pipeline flag is on, then `render` only if a shell was detected and the source policy allows it |
| 6 output | a `linkCard` (title, description, image, canonical URL, site name, type, published time) plus the raw structured nodes; Harvest always delivers the capture |
| 7 watch | optional: schedule a `refresh` of the one URL; conditional GET plus hash; gone rules as for pages |

- oEmbed: discovery by `<link rel="alternate" type="application/json+oembed">` (or XML) or an HTTP `Link` header;
  response types `photo`, `video`, `link`, `rich`; the provider registry is `https://oembed.com/providers.json`.
- OpenGraph: `og:title`, `og:type`, `og:image`, `og:url` are the four required properties; `og:description`,
  `og:site_name`, `og:locale`, `article:published_time` are optional; no event properties exist.
- SSRF (OWASP): an allow-list does not work for unknown domains; resolve A and AAAA, reject loopback, private,
  link-local and metadata addresses (`169.254.169.254`), connect to the validated IP, re-validate every redirect hop,
  allow http/https only. In .NET the connect-time check is `SocketsHttpHandler.ConnectCallback` (net5.0 to net11.0);
  ListingShelf's per-provider host allow-list is not enough for intake.
- `robots.txt` applies to a submitted URL too (pick, W4); a refusal returns `robots-disallowed`, and the product shows
  its hand-typed entry path (T7 roles).

---

## 3. Behaviour at sources

| Topic | Rule | Basis |
|---|---|---|
| Identify | UA `WoW2-Harvest/{version} (+https://{host}/bots/harvest; {contact})`; the same product token is the `robots.txt` token; the page says what Harvest is and how to block it | spec § Behaviour at sources; today `ListingShelf/1.0` has no contact (`ListingPageClient.cs:69`) |
| `robots.txt` fetch | 2xx: parse (support ≥500 KiB); 4xx: unavailable, crawling allowed; 5xx or network error: assume complete disallow; cache ≤24 h; follow ≥5 redirects | RFC 9309 |
| `robots.txt` that is not robots | an HTML body at `/robots.txt` is unreadable: treat as disallow and record `challenge` | textileexpo.uz serves its 12 KB challenge page there (pick, W3) |
| Crawl-delay | not defined by RFC 9309; honour it when ≤30 s | pick (W13) |
| Parser | `Meziantou.Framework.RobotsTxt` 2.0.6 (MIT, RFC 9309 plus Google wildcards, net10.0, 2026-10-21) | NuGet |
| Content signals | parse `Content-Signal: search=…, ai-input=…, ai-train=…`; `ai-input=no` → capture only, no LLM extraction for that host; `ai-train=no` needs no action (Harvest trains nothing) | craftfair.uz serves `search=yes,ai-train=no,use=reference`; the file frames its restrictions as reservations of rights under EU Directive 2019/790 Art. 4; Cloudflare says a blank signal is not "no preference" (W5) |
| Terms | a per-source `permission`: `open` · `restricted` · `granted` · `denied`. `restricted` blocks scheduled and whole-site capture until `granted` | afisha.uz § terms: copying, reproduction and other use of site information only with prior written permission (W1) |
| Politeness | per host: 1 connection, ≥2 s between requests, then adaptive: `delay = max(base, latency / target concurrency)` | pick (W13); formula as Scrapy AutoThrottle (target delay = latency / `AUTOTHROTTLE_TARGET_CONCURRENCY`) |
| Backoff | 429 or 503 with `Retry-After`: wait it, capped at 15 min per attempt, else defer to the next slot; 5xx and network errors: 2 retries at 1 s and 2 s (as today) | today a 429 stops the whole run and ignores `Retry-After` (`RunExecutionService.cs`, capture loop) |
| Off-peak | whole-site sweeps run at night, UZ time | pick (W13) |
| Conditional requests | send `If-None-Match` / `If-Modified-Since` whenever a validator is stored | RFC 9110 §13.1 headings; none of the event pages read offers one |
| Cookies | run-scoped jar per host, discarded after the run; no login cookies; never sign in | iticket.uz needs cookie support to pass its waiting room (W6) |
| Limits | page 8 MiB, deadline 50 s; sitemap files up to 50 MB streamed; images separate | `ListingPageClient.cs:16-19`; sitemaps.org |
| Proxies | none: direct egress from Harvest's own IPs; no pools, no residential proxies, no rotation. A single static egress per source only for a geo reason, declared in the source policy and shown in the console | spec: blocks are outcomes, never bypassed (W8) |

### Outcomes (extends `CompletionReason`)

| Outcome | Trigger | Action |
|---|---|---|
| `robots-disallowed` | path denied, or `robots.txt` unreadable | stop for that path; no retry until the cache expires |
| `restricted` | source `permission` is not `open`/`granted` | not scheduled; manual entry only |
| `challenge` | JS interstitial, CAPTCHA, "access denied" page | stop the host's run; retry next slot; alert after 3 |
| `waiting-room` | the site queues the client (page, not an admitting redirect) | defer; never open parallel sessions to skip the queue |
| `blocked` | 401/403 on a public page | stop the host's run; alert |
| `rate-limited` | 429, or 503 with `Retry-After` | wait or defer as above |
| `render-required` | shell detected | route to `render` when the source allows, else report |
| `gone` · `moved` | table in section 2.3 | to T5's state machine |
| `unrecognized` | markup matches no extractor | report with the sample capture |

### Signatures seen on 2026-10-26

- iticket.uz: `https://iticket.uz/` → 302 `https://queue.iticket.uz/waiting?room=main&continue=…` → 302 back with
  `wr_room_main` and `wr_session_id` cookies. A client without cookies loops (50 hops). With a cookie jar the queue
  admitted the request on the first pass (2 redirects). ListingShelf's client (no cookies, host check on each hop)
  would stop at the first hop as `InvalidRedirect`.
- textileexpo.uz: `/`, `/robots.txt` and `/sitemap.xml` all return a 12 KB page titled "One moment, please..." with
  `setTimeout(reload, 5000)` (verified on all three): a JS interstitial. The outcome is `challenge`; passing it with a browser would be bypass.
- texworld-apparel.uz and tftexpo.com send `server: ddos-guard`; plain GETs got 200.
- iticket.uz, mstar.uz, voyage.uz, craftfair.uz, uniticket.uz, tickets.uz sit behind Cloudflare; plain GETs got 200.
- reachability from a datacenter IP is untested (U); the profiles above come from one home connection.

---

## 4. Build vs wrap

| Tool | Licence | Language | Self-host | Library or sidecar | Fit | Pick |
|---|---|---|---|---|---|---|
| Crawlee 3.18.2 (2026-09-29) | Apache-2.0 | TypeScript (a Python port exists) | yes, a Node process | library; for .NET only a sidecar | queue and storage live in the Node process (files by default, purged at start unless configured); `respectRobotsTxtFile` defaults to false; browser crawlers enable fingerprint spoofing by default | skip; borrow `sameDomainDelaySecs`, `maxRequestsPerMinute` ideas |
| Firecrawl (`v2.11.0`, 2026-06-19) | AGPL-3.0; SDKs and some UI MIT | TypeScript | yes: API + workers + Redis + RabbitMQ + PostgreSQL + Playwright; API unauthenticated by default; no fire-engine | sidecar | markdown-for-LLM output equals what Harvest's own text prep does; a modified, network-exposed fork would owe source | skip |
| changedetection.io 0.60.9 (2026-10-12) | Apache-2.0 | Python | yes, Docker; REST API; Apprise notifications | sidecar | single-URL watcher with CSS/XPath/JSONPath filters and Playwright; it would own scheduling and storage that Harvest owns | skip; borrow the filter vocabulary (ignore text, trigger text) |
| RSSHub (build `v2026.10.25`) | AGPL-3.0 | TypeScript | yes, Docker; Redis cache; `PROXY_URI` | sidecar over HTTP, RSS/Atom/JSON Feed out | `telegram/channel/:username` reads `t.me/s/:username`, falls back to MTProto with `TELEGRAM_SESSION`; Instagram routes need `INSTAGRAM_COOKIE` and are flagged anti-crawler; Twitter routes need `TWITTER_AUTH_TOKEN` or account credentials; `rsshub/transform/html\|json\|sitemap` turns CSS rules into a feed; ≥1,000 route folders | optional sidecar adapter behind a flag; unauthenticated routes only; off in P1 |
| Scrapy 2.19.0 (2026-09-10) | BSD-3-Clause | Python | yes | sidecar only | AutoThrottle, per-domain limits, duplicate filter; wrong runtime for the platform | skip; adopt the throttle formula |
| Abot 2.0.70 (NuGet 2021-08-09; GitHub pushed 2026-07-17) | Apache-2.0 | C#, .NET Standard 2.0 | library | library | AngleSharp parser, `MinCrawlDelayPerDomainMilliSeconds`, `IRobotsDotTextFinder`; in-memory scheduler; JS rendering and multi-site parallelism are in AbotX | skip; its crawl loop wants to own scheduling, Harvest's frontier is durable in PostgreSQL |
| AngleSharp 1.8.6 (2026-10-25) | MIT | C# | library | library | already in `ListingShelf.Infrastructure.csproj`; CSS selectors, DOM | **use** |
| HtmlAgilityPack 1.13.1 | MIT | C# | library | library | XPath, lenient parser; a second parser only if a source needs XPath | skip |
| Playwright .NET 1.64.1 (2026-10-22) | MIT binding; Playwright core Apache-2.0 | C# | library | library inside a separate worker container | render tier (section 2.4) | **use** for `render` |
| `Meziantou.Framework.RobotsTxt` 2.0.6 | MIT | C# | library | library | RFC 9309 parser | **use** |
| `Ical.Net` 5.2.3 · `System.ServiceModel.Syndication` 10.0.14 | MIT | C# | library | library | ICS; RSS/Atom | **use** |
| Sitemap parsers (`Toimik.SitemapsProtocol` 0.7.0, `Louw.SitemapParser` 0.0.2) | (U) | C# | library | library | immature (3.5k and 20k downloads) | write a streaming `XmlReader` reader |

- pick: build the family in .NET on ListingShelf's client; no crawler framework; no sidecar in P1.
- reasons: the frontier, schedule, quotas and deliveries are Harvest's own and live in PostgreSQL; every wrapped
  framework would duplicate one of them, and the Node and Python options add a second runtime to the platform.
- RSSHub is the one wrapper with distinct value: long-tail platforms where T2 finds no official API. Its Instagram and
  Twitter routes rely on a real account's cookie or token, which conflicts with "no sign-in"; T2 decides per platform.
- AGPL: running RSSHub or Firecrawl unmodified on the internal network, never exposed to users, keeps WoW2's code free
  of the licence; a fork changes that.

---

## 5. Uzbekistan event sources

Structure only; page counts are from sitemaps (URLs include locale variants unless stated).

### 5.1 Ticketing and event sites

| Site | robots.txt | Sitemap | JSON-LD Event | Feed | JSON API visible | Browser | Size | Route pick |
|---|---|---|---|---|---|---|---|---|
| afisha.uz (Afisha Media) | `*`: Disallow `/adm/`, `/api/`, `/*/search`, `/_next`; no Crawl-delay. Terms: reuse needs prior written permission | `/sitemap.xml` index, 5,358 children (movies, places, performances, materials by week since 2006; ru, uz), per-child `lastmod` | yes on event pages: `Event` with `startDate`, `location` + `geo`; no offers | none (Google News sitemap only) | not used: `/api/` and `/_next` disallowed | no (SSR Next.js) | ≥10⁴ URLs (U); event page 159 KB | R1 + R3; R7 until permission |
| iticket.uz | `*`: Disallow `/profile`, `/ru/profile`, `/en/profile`, `/users`; sitemap declared | flat, 684 URLs = 230 per locale (131 events, 83 venues, 16 static) × 3 locales; no `lastmod` | no: Nuxt 2 client-rendered shell (7,024 B), generic OpenGraph | none found | yes by inference (SPA with axios); host and endpoints not read (U) | yes, or its API | ~130 events | defer; R4 or R5 after an API and terms check |
| mstar.uz (MSTAR CO, concert promoter) | `Allow: /`; Disallow login, register, profile, dev, `offerta.pdf`, panel, admin, `/api/`, check, ws, accounts | flat, 24 URLs: 9 events + static × 3 locales; real `lastmod` on events | yes: `MusicEvent` + `AggregateOffer` + `eventStatus` + performer | none | not used: `/api/` disallowed | no | 9 events, 31 KB each | R1 + R3; P1 candidate |
| voyage.uz (travel guide, 5 locales) | `Allow: /`; Disallow `/go/`, `/search/`, legal and guide pages, any URL with a query (`/*?*`) | index of 5 locale sitemaps; ~150 `lastmod` entries in the first | yes: `ItemList` of 4 `Event` on `/events`; offers link to iticket.uz | none | no | no | ~150 URLs per locale; 4 events listed | R1; secondary, derived from iticket offers; low volume |

- checked and set aside: uniticket.uz (air tickets, WordPress, Disallow `/wp-json/` and `/*?`), tickets.uz (air and
  travel; its robots names tickets.kz), spot.uz (business news; RSS at `/ru/rss/` is general news; `/ru/events/`
  carries `WebPage` JSON-LD only), OY Tickets (cinema; site and Telegram bot since July 2023; not probed).
- afisha.uz, spot.uz share sitemap naming (`standard-ru`, `materials-ru-DATE`, `google-news-ru`) and the `/adm/`
  disallow; both are listed among Afisha Media's properties (search snippet of `/ru/about`). One adapter may cover
  both (U).

### 5.2 The nine links Ocharo reviewed

Source: `SourceDirectory.ts` (area and kind in parentheses).

| # | Site | robots.txt | Sitemap | JSON-LD Event | Feed | JSON API | Browser | Size | Route pick |
|---|---|---|---|---|---|---|---|---|---|
| 1 | texworld-apparel.uz (both; Tilda, DDoS-Guard) | Tilda defaults: a few `/page…html`, `/tilda/form*`, `/tilda/cart*`…, then an open `Disallow:` | `sitemap.xml` 43 URLs, 43 distinct `lastmod`; also `sitemap-feeds.xml` declared (content not read, U) | no | none | no | no | 43 URLs | R2 + LLM, monthly |
| 2 | craftfair.uz Hunarmand (events) | Cloudflare managed: `Allow: /`, `Content-Signal: search=yes,ai-train=no,use=reference`; named AI crawlers (ClaudeBot, GPTBot, anthropic-ai, …) `Disallow: /` | `/sitemap.xml` returns 404 | no | none | no | no | one page, 50 KB | R2; capture only until W5 sets the signal rule |
| 3 | uzexpocentre.uz (events; venue calendar) | `User-agent: *`, no rules | `/sitemap.xml` (undeclared), 201 URLs in ru/uz/en, no `lastmod` | no | none | no | no | ~65 pages per locale (U) | R2 with a table parser for the schedule page; best of the nine |
| 4 | kfw.kz Kazakhstan Fashion Week (events) | `Disallow:` empty (allow all) | `/sitemap.xml` returns 404 | no | none | no | no | small; the page read is 20 KB | R2 + LLM, manual refresh |
| 5 | tftexpo.com (both; Tilda, DDoS-Guard) | Tilda defaults; sitemap declared | `sitemap.xml` 42 URLs, 26 distinct `lastmod` | no | none | no | no | 42 URLs | R2 + LLM, monthly |
| 6 | fashionexpo.kz (both; Joomla) | Joomla defaults (admin, libraries, `/shop/`); sitemap declared as `/Sitemap.xml` | 57 URLs, no `lastmod` | no (`Organization` only) | none | no | no | 57 URLs | R2 + LLM, monthly |
| 7 | textileexpo.uz (both) | `/robots.txt` returns the challenge page (`text/html`, 12,079 B) | `/sitemap.xml` returns the same page | unknown | unknown | unknown | challenge page | unknown | R7 `challenge`; hand-typed entry; no bypass |
| 8 | plshawlstoles.com (sourcing) | Disallow `/cgi/`, `/temp/`, `/stats/`, `/glpcat/`, `/GATRACK/` | 64 URLs, 1 shared `lastmod` | no (`LocalBusiness`, `AggregateRating`) | none | no | no | 64 pages; the catalogue page is 1.3 MB | R2: capture and hash for change; LLM on demand |
| 9 | shawlsandcarpets.com (sourcing) | same pattern | 57 URLs, 1 shared `lastmod` | no (`LocalBusiness`, `AggregateRating`) | none | no | no | 57 pages; page read 205 KB | R2: as 8 |

- these are brochure sites: one fair or one supplier per site, so the `site` mode matters little; weekly or monthly
  `page` captures plus change hash fit, and the LLM does the extraction (T6).
- links 8 and 9 are supplier catalogues (sourcing), not events; they ride the same `page` family and a different schema.
- `texworld` and `tftexpo` are Tilda exports with near-identical robots files; one Tilda selector set may serve both (U).

---

## Findings that change the spec

- Source adapters: replace "web page, provider API, RSS or ICS feed, Telegram channel" with the family set `page`, `structured`, `site` (mode), `render`, `api`, `feed`, `link`.
- Extraction: add a deterministic tier before the LLM. `Event` JSON-LD exists on 3 of the 16 sites profiled and fills most of `wow2.event.v1`; the LLM covers gaps such as afisha.uz's price text.
- Whole-site harvest is sitemap-driven for the sites in scope: afisha.uz publishes an index of 5,358 child sitemaps with per-child `lastmod`, so enumeration costs 1 index request plus ~3 changed children a day.
- Change detection: no event page read offers `ETag`; use sitemap `lastmod` where trusted (afisha.uz children, mstar.uz events) plus a normalized-content hash, as ListingShelf already hashes.
- `lastmod` trust is per URL class: afisha.uz `standard-*` and mstar.uz static URLs carry the fetch time; store a trust flag per source and pattern.
- Outcomes: add `challenge`, `waiting-room`, `robots-disallowed`, `restricted`, `render-required`, `gone`, `moved`; ListingShelf's `IsChallenge` misses textileexpo.uz's "One moment, please...".
- Cookies: a client without cookies loops on iticket.uz's waiting room; allow a run-scoped cookie jar, and keep "no sign-in".
- Afisha's terms (prior written permission to copy or use material) make EV2 a legal gate before any scheduled or whole-site harvest; add a per-source `permission` field.
- iticket.uz is client-rendered (7,024 B shell, no JSON-LD): its data needs the browser tier or an API; mstar.uz, afisha.uz and voyage.uz do not.
- Browser tier: a separate worker container, per-source opt-in; Microsoft's Playwright image is documented as a testing image, not for untrusted sites, so harden it (non-root, seccomp, no internal routes).
- Link intake: ListingShelf's host allow-list does not cover unknown domains; add connect-time IP checks (`SocketsHttpHandler.ConnectCallback`) and per-hop re-validation.
- Politeness: ListingShelf pauses 500 ms run-wide, stops on the first 429 and ignores `Retry-After`; Harvest needs per-host limits and `Retry-After` handling.
- `robots.txt` edge: RFC 9309 treats 5xx as complete disallow; a challenge page served at `/robots.txt` (textileexpo.uz) needs the same treatment.
- Content signals: craftfair.uz publishes `ai-train=no`; add a per-host `aiUse` flag so LLM extraction can be skipped where `ai-input=no`.
- Limits: API caps `pageLimit` 100 and `itemLimit` 2,000 fit listings, not whole sites; raise or exempt `site` pipelines.
- Build vs wrap: build on ListingShelf's client with AngleSharp, `Meziantou.Framework.RobotsTxt`, `Ical.Net`, `System.ServiceModel.Syndication` and Playwright .NET; wrap nothing in P1; RSSHub stays an optional T2 sidecar.
- Date traps for T6 and Events: afisha.uz bucket dates are publish dates, uzexpocentre.uz dates omit the year, voyage.uz sends date-only events as midnight UTC.
- Hash both raw body and normalized content: the first answers "was the fetch identical", the second "did the post change".

---

## Points

- [x] W1 — Afisha permission: ask Afisha Media (info@afisha.uz) for written permission before scheduled or whole-site capture, or build the Afisha source later. Afisha's terms require prior written permission for copying and other use; this gates EV2 and Events' first source (T4, T7) → confirmed 2026-10-27: ask now; until `granted`, Afisha events come in by hand-typed entry.
- [x] W2 — iticket.uz: defer, spike the browser tier, or find its API and ask for partner access. The shell carries no data (T7) → confirmed 2026-10-27: defer; start with mstar.uz and voyage.uz (R1), add Afisha on W1, revisit iticket after an API and terms check.
- [x] W3 — a challenge page served at `/robots.txt` or `/sitemap.xml` (textileexpo.uz): treat as unreadable, therefore disallow, and record `challenge` → confirmed 2026-10-27: yes, same as an RFC 9309 5xx.
- [x] W4 — does `robots.txt` bind a single URL a product submits? → confirmed 2026-10-27: yes, and a refusal falls back to hand-typed entry (T7 roles).
- [x] W5 — content signals: map `ai-input=no` to "capture only, no LLM extraction" and ignore `ai-train=no`; craftfair.uz sets `ai-train=no,use=reference` with `ai-input` blank (T6) → confirmed 2026-10-27: as stated; revisit when T6 fixes which providers see captured text.
- [x] W6 — run-scoped cookie jar per host (waiting rooms, consent cookies), never persisted, never a login → confirmed 2026-10-27: yes.
- [x] W7 — render tier placement: a separate container in the Harvest bundle, 1–2 contexts per worker, per-source opt-in (T7, T8) → confirmed 2026-10-27: yes; spike measures memory and seconds per page first (the figures in 2.4 are U).
- [x] W8 — proxies: direct egress only; one static egress per source for geo reasons if a source needs it. Reachability of afisha.uz, iticket.uz, mstar.uz from the production host is untested (U) → confirmed 2026-10-27: none until a source needs it; test reachability from the host that will run Harvest.
- [x] W9 — RSSHub sidecar: allowed as an adapter for platforms without an official API, unauthenticated routes only (T2) → confirmed 2026-10-27: off in P1; T2 decides per platform, and any route needing a real account's cookie stays out.
- [x] W10 — frontier storage and claiming: PostgreSQL rows per URL with a per-host lock; the worker claims `fetch` jobs by host (T5 identity, T7 workers) → confirmed 2026-10-27: PostgreSQL, no Redis or external queue.
- [x] W11 — multi-locale sites (iticket ×3, afisha ru/uz, mstar ×3): one post with locale alternates, or one post per locale (T5) → confirmed 2026-10-27: one post, default locale as canonical, alternates linked.
- [x] W12 — lookback for Afisha-style archives: upcoming events plus the last 8 weekly buckets, not the 5,358-file history (T7) → confirmed 2026-10-27: as stated.
- [x] W13 — politeness defaults: 1 connection, ≥2 s, adaptive by latency, `Crawl-delay` honoured up to 30 s, whole-site sweeps at night UZ time → confirmed 2026-10-27: as stated.
- [x] W14 — identification: the bot page URL and contact in the UA need a WoW2 domain the developer owns → confirmed 2026-10-27: `https://{wow-two domain}/bots/harvest`; developer names the domain.
- [x] W15 — gone thresholds: `suspect` after one run absent from a complete enumeration, a direct fetch decides; enumeration suspect above ~30% URL drop (T5) → confirmed 2026-10-27: as stated.
- [x] W16 — social URL with no adapter yet: return a link card from OpenGraph/oEmbed rather than fail (T1, T2) → confirmed 2026-10-27: link card.
- [x] W17 — Ocharo's nine links: weekly or monthly `page` captures, LLM extraction, change hash; textileexpo.uz stays manual until the owner allows access (T4) → confirmed 2026-10-27: as stated; uzexpocentre.uz gets a table parser first.
- [x] W18 — the web family as be SDK code (Form 1) or inside Harvest only (T8) → confirmed 2026-10-27: fetcher, URL policy, robots and sitemap readers and structured readers in the be SDK; adapters and frontier in Harvest.

---

## Sources

Sites (read 2026-10-26):

- https://www.afisha.uz/robots.txt · https://www.afisha.uz/sitemap.xml · https://www.afisha.uz/sitemaps/standard-ru.xml · https://www.afisha.uz/sitemaps/materials-ru-2026-10-26.xml · https://www.afisha.uz/sitemaps/performances-ru-2026-10-19.xml · https://www.afisha.uz/sitemaps/google-news-ru.xml — robots rules, index of 5,358 children, `lastmod` behaviour
- https://www.afisha.uz/ru/theatres/2026/10/26/clowns — `Event` JSON-LD, headers (`no-store`, no ETag), 159,218 B
- https://www.afisha.uz/ru/terms — prior written permission for copying and other use; no clause on bots
- https://www.afisha.uz/ru/about — related properties (search snippet); https://www.afisha.uz/ru/cinema/2023/07/20/oy-tickets — OY Tickets launch
- https://iticket.uz/ · https://iticket.uz/robots.txt · https://iticket.uz/sitemap.xml · https://iticket.uz/events/concerts/tashkent-city-park2 — waiting room, shell, 684 URLs
- https://mstar.uz/ · https://mstar.uz/robots.txt · https://mstar.uz/sitemap.xml · https://mstar.uz/event/valeriia-2026/ — `MusicEvent` + `AggregateOffer`, `lastmod` pattern
- https://voyage.uz/events · https://voyage.uz/robots.txt · https://voyage.uz/sitemap-index.xml · https://voyage.uz/sitemap.xml — `ItemList` of `Event`
- https://www.spot.uz/ru/events/ · https://uniticket.uz/ · https://tickets.uz/ — set aside (news, air tickets)
- https://texworld-apparel.uz/eng · https://craftfair.uz/?lang=en · https://www.uzexpocentre.uz/en/menu/krgazmalar-rezhasi · https://kfw.kz/page/o-nedele · https://tftexpo.com/en · https://fashionexpo.kz/en/ · https://textileexpo.uz/ · https://www.plshawlstoles.com/ladies-stole.html · https://www.shawlsandcarpets.com/cashmilon-kashmiri-shawls-and-stoles.html — the nine links, each with its `/robots.txt` and sitemap
- web searches 2026-10-26: UZ ticketing platforms (uniticket.uz, mstar.uz, tickets.uz, OY Tickets), no public API for iticket.uz or afisha.uz, Visa Fashion Week Tashkent coverage on afisha.uz/fashion (https://www.afisha.uz/ru/fashion)

Standards and docs:

- https://www.rfc-editor.org/rfc/rfc9309.html — robots.txt: 4xx unavailable, 5xx disallow, 500 KiB, 24 h cache, ≥5 redirects, no Crawl-delay
- https://www.rfc-editor.org/rfc/rfc9110.html — `Retry-After` §10.2.3, conditional requests §13.1, 404/410 §15.5 (section headings only; body text not read)
- https://www.sitemaps.org/protocol.html — 50,000 URLs, 50 MB, 50,000 children, `lastmod` meaning
- https://www.rfc-editor.org/rfc/rfc5545.html — iCalendar; VEVENT §3.6.1, STATUS §3.8.1.11, UID §3.8.4.7, change management §3.8.7 (headings only)
- https://developers.google.com/search/docs/appearance/structured-data/event — required and recommended `Event` properties, status handling
- https://www.uni-mannheim.de/dws/news/wdc-json-ld-microdata-rdfa-data-corpus-2024-published — structured-data coverage, Common Crawl 2024 (search summary)
- https://blog.cloudflare.com/content-signals-policy/ · https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/ — content signals (search summary)
- https://oembed.com/ · https://oembed.com/providers.json · https://ogp.me/ — oEmbed discovery and types; OpenGraph required properties
- https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html — SSRF defences for arbitrary URLs
- https://learn.microsoft.com/en-us/dotnet/api/system.net.http.socketshttphandler.connectcallback — connect-time hook, net5.0–net11.0
- https://developer.wordpress.org/rest-api/reference/posts/ — `modified_after`, `orderby=modified`
- https://docs.theeventscalendar.com/reference/classes/tribe__events__rest__v1__endpoints__archive_event/ — Events Calendar REST parameters
- https://developer.ticketmaster.com/products-and-docs/apis/partner/ — Partner API restricted to distribution agreements (search summary)
- https://playwright.dev/dotnet/docs/docker — image tags, `--init`, `--ipc=host`, seccomp, "testing and development"
- https://docs.scrapy.org/en/latest/topics/autothrottle.html — AutoThrottle formula and defaults

Build vs wrap:

- https://github.com/apify/crawlee · https://crawlee.dev/js/docs/guides/avoid-blocking · https://crawlee.dev/js/docs/guides/request-storage — Apache-2.0, 3.18.2, fingerprints default on, queue storage; `respectRobotsTxtFile`, `sameDomainDelaySecs`, `maxRequestsPerMinute` read from `packages/basic-crawler/src/internals/basic-crawler.ts`
- https://github.com/firecrawl/firecrawl · https://raw.githubusercontent.com/firecrawl/firecrawl/main/SELF_HOST.md — AGPL-3.0 (SDKs MIT), compose services, unauthenticated API, fire-engine not bundled
- https://github.com/dgtlmoon/changedetection.io · https://raw.githubusercontent.com/dgtlmoon/changedetection.io/master/README.md — Apache-2.0, filters, Playwright, API
- https://github.com/DIYgod/RSSHub · https://docs.rsshub.app/deploy/config — AGPL-3.0; config keys; route sources `lib/routes/telegram/channel.ts`, `instagram/index.ts`, `twitter/user.ts`, `rsshub/transform/html.ts`
- https://github.com/scrapy/scrapy — BSD-3-Clause, 2.19.0
- https://github.com/sjdirect/abot · https://www.nuget.org/packages/Abot — Apache-2.0, 2.0.70 (2021-08-09), AbotX split
- https://github.com/AngleSharp/AngleSharp · https://www.nuget.org/packages/AngleSharp — MIT, 1.8.6
- https://github.com/zzzprojects/html-agility-pack · https://www.nuget.org/packages/HtmlAgilityPack — MIT, 1.13.1
- https://github.com/microsoft/playwright-dotnet · https://github.com/microsoft/playwright · https://www.nuget.org/packages/Microsoft.Playwright — MIT binding, Apache-2.0 core, 1.64.1 (2026-10-22)
- https://www.nuget.org/packages/Meziantou.Framework.RobotsTxt · https://www.nuget.org/packages/Ical.Net · https://www.nuget.org/packages/System.ServiceModel.Syndication — robots parser, ICS, RSS/Atom
- https://www.nuget.org/packages/Toimik.SitemapsProtocol · https://www.nuget.org/packages/Louw.SitemapParser — sitemap parsers (NuGet search)
