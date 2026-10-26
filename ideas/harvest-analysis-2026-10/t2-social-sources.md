# T2 — Social platform sources

*Last updated: 2026-10-26*

> One tailored Harvest adapter per social platform, reading public content posted by others. For each platform: the official read route and its real limits, the licensed-provider route (Apify, Bright Data and others), the logged-out public-page route, the fields each returns, whether deletion is detectable, and a pick with the monthly cost at 10k posts. The result is narrow: only YouTube, Threads, X (paid) and Facebook Pages offer a general official read for third-party public content; Instagram, Facebook Events and Groups, TikTok and Reddit reduce to licensed providers, and LinkedIn to nothing. Money is not the constraint (about $0–50 per platform at 10k posts a month); legal posture, access gates and per-platform retention duties are.

Legend: **Route A** = official API or feed · **Route B** = licensed third-party provider reading logged-out public pages · **Route C** = Harvest's own logged-out page fetch, oEmbed, OpenGraph. **(U)** = unverified or secondary source only. All pages read 2026-10-26; sources older than 2025 are marked `stale`. Prices are USD per 1,000 items (`/1k`) from vendor pages read the same day; vendor pages contradict each other, so ranges are shown.

---

## 1. Platforms and Uzbekistan relevance

Reach = platform ad-tool audience, not active users (DataReportal Digital 2026, Kepios data of Oct 2025). Total social identities: 14.1M, 37.9% of population.

| Platform | UZ reach | Matters for UZ audiences? | Priority |
|---|---|---|---|
| Instagram | 14.1M (53.7% of adults) | yes — the main public social network; fashion brands, realtors, event promoters | P0 |
| Facebook | 2.30M (DataReportal) vs 17.1M (NapoleonCat, Sep 2026) — sources conflict (U) | yes for public groups (rentals) and events; page reach uncertain | P1 |
| YouTube | not in DataReportal's page; large in UZ (U) | yes — shows, venues, brands; official API is cheap | P1 |
| Telegram | not in DataReportal; website-share proxy 81.5% (WMTips, U) | dominant — [T1](t1-messaging-sources.md), not here | — |
| TikTok | 2.59M (adults 18+) | partly — younger audience, trend and brand content | P2 |
| Threads | 834K | little — but the only platform with an official keyword search for third parties | P3 |
| Odnoklassniki (ok.ru) | ok.ru has 649K monthly search visits from UZ, second among social sites (Ahrefs, Jul 2025, U) | older and regional audiences; no official route found | P3 watch |
| VK | sixth among social sites by UZ search traffic (Ahrefs, Jul 2025, U) | small Russian-speaking niche; official API has monthly caps (section 2) | P3 watch |
| LinkedIn | 1.10M registered members | hiring and B2B only; no route exists (section 2) | skip |
| X | 148K, down 60% in a year | marginal | P4 |
| Reddit | 262K | marginal | skip |

---

## 2. Official read routes (Route A)

| Platform | Official route for third-party public content | Gate | Real limits | Fits Harvest? |
|---|---|---|---|---|
| Instagram | **Business discovery**: `business_discovery.username(x){media{…}}` run on Harvest's own Instagram professional account | token of a Business or Creator account; permissions `instagram_basic`, `instagram_manage_insights`, `pages_read_engagement`; the target must be a Business or Creator account (not personal) and not age-gated; App Review for live use beyond app roles (U) | returns public media fields and `followers_count`/`media_count`; a `GET` on a returned media object fails by design; call-rate numbers not published (U) | yes for a known list of business accounts (brands); no discovery |
| Instagram | **Hashtag search** (`recent_media`, `top_media`) | App Review: `Instagram Public Content Access` + `instagram_basic`; business verification | 30 unique hashtags per account per rolling 7 days; `recent_media` only media from the last 24 hours; ads excluded; 50 per page; no `username` field. Allowed use is narrow: own campaigns, brand sentiment, contest entrants, customer support | no — Meta's allowed use is not general harvesting |
| Instagram | oEmbed (`/instagram_oembed`) | token requirements not stated on the page (U) | 1,000 requests/hour; returns embed HTML only; **using the data for anything but a front-end view — analytics, extraction, persisting — is prohibited** | display of a pasted link only, never a harvest route |
| Instagram, Facebook | **Meta Content Library + API** | academic or not-for-profit research institutions only; vetted by CASD, 2–3 weeks; annual recertification | export from the Secure Research Environment is not permitted | no — researchers only |
| Facebook Pages | **Page Public Content Access** (`/page/feed`, `/page-post`, `/page-post/comments`, Pages Search API) | business verification + App Review; possibly extra contracts; allowed use: "analyze and/or display posts and engagement on Pages"; in live mode no Page public content is visible without it | per-app call budget `4,800 × engaged users` per 24h (third-party, U) — a new app with no users may get little headroom (U) | yes for public Pages, if business verification works from UZ (U) |
| Facebook Events | Graph `Event` node | Meta's reference: "Access to Events on Users and Pages is only available to Facebook Marketing Partners"; group events needed the Groups API | — | no |
| Facebook Groups | none | Groups API deprecated in Graph v19.0, removed 2024-04-22 (`publish_to_groups`, `groups_access_member_info`); group admins can no longer install apps | — | no |
| X | **X API pay-per-use**: `/2/tweets/search/recent`, user timelines, post lookup | credits bought in the Developer Console; no subscription or minimum; legacy Basic ($200) and Pro ($5,000) reported closed to new sign-ups (U) | posts $0.005 each, users $0.010, billed per resource returned; 24-hour UTC dedup of re-requested resources; cap 3M post reads per month; recent search = last 7 days, 100 per request; full-archive 500 per request, pay-per-use and Enterprise only | yes, as a priced option |
| Reddit | **Data API** | commercial use needs a separate agreement (Data API Terms §3.1, revised 2026-07-20); Responsible Builder Policy (Nov 2025) requires approval for new tokens; **requests for new public API access stop 2026-10-31, unregistered apps lose access 2027-01-12, public API access closes March 2027, RSS ends 2026-11-13** (Decrypt, 2026-10-01; Reddit's own post not fetched, U) | commercial price unpublished; "$0.24 per 1,000 calls" is third-party and unconfirmed (U); free tier 100 queries/minute per OAuth client dates from 2023 (`stale`) | no — closing to new third parties |
| TikTok | **Research API** | non-profit academic institutions in the US, EEA, UK, Switzerland, or not-for-profit research bodies in the EU; commercial users ineligible (secondary, U) | ~1,000 requests/day, commercial use prohibited (secondary, U); approvals reported to take weeks to many months | no |
| TikTok | **Display API** | OAuth by the account owner; scopes `user.info.basic`, `video.list`; app audit | the authorizing user's own profile and videos only (third-party reading of the docs, U); official docs timed out on 2026-10-26 | no — own content only |
| TikTok | Commercial Content API | research account; ads delivered to EEA, UK, Switzerland (secondary, U) | ads library only | no |
| YouTube | **Data API v3** `playlistItems.list`, `videos.list`, `channels.list`, `commentThreads.list` | Google Cloud project + API key; no review for default quota; quota extension by form | 10,000 units/day for all endpoints except `search.list`, which has **its own bucket of 100 calls/day**; each call 1 unit incl. `search.list`; invalid requests still cost 1; resets midnight PT (page updated 2026-10-15) | yes — the best-supported route |
| YouTube | per-channel RSS `feeds/videos.xml?channel_id=` | none; unofficial, 15 latest uploads (U) | a Google forum thread reports intermittent 404s in Jan 2026 | optional cheap poller |
| Threads | **Keyword and topic-tag search** (`/keyword_search`), **profile posts** (`/profile_posts?username=`), media lookup | `threads_keyword_search` and `threads_profile_discovery` need approval (advanced access); with standard access only Meta's own accounts (`@meta`, `@threads`, `@instagram`, `@facebook`) are readable | keyword: 2,200 queries per user per rolling 24h, 100 results per query, `RECENT` or `TOP`; profile posts: public profiles with ≥100 followers only, 1,000 requests per user per 24h; app budget `4,800 × impressions` (min 10) per app-user pair | yes — free, real third-party search |
| LinkedIn | none for third-party members; organization posts via Community Management API | vetted two-step approval (Development, then Standard with screencast); `r_member_social` is closed; an admin sees only posts their organization created or reshared | — | no |
| VK | VK API (`dev.vk.ru`), service key for public reads (U) | VK ID business account; **from 2026-09-07 unverified partners get 10,000 calls/month, verified 100M** | `wall.get` limits not found (U); methods outside public docs "will be phased out" | maybe later |
| Odnoklassniki | OK REST API | app registration; methods need permissions such as `VALUABLE_ACCESS` | current approval path not found (U); only third-party mirrors and Habr threads of unknown age | no |

- Meta Platform Terms (changed 2026-02-03) §3.a.iv forbid selling, buying or licensing Platform Data, §3.c limits sharing it with third parties, §3.d requires deleting or updating it on a request from Meta or the user, and when no longer needed.
- A Meta app that also publishes, measures or signs users in carries its own permission reviews on top of these features; see Point S11.

---

## 3. Licensed third-party providers (Route B)

### 3.1 Providers

| Provider | Covers | Price | Model and freshness | Notes |
|---|---|---|---|---|
| Apify (store actors) | Instagram, Facebook posts, groups, events, TikTok, X, Reddit, YouTube, VK, LinkedIn, Threads | per-actor, pay-per-event; plans Free $0 ($5 credit), Starter $19, Scale $199, Business $999, each with matching usage credit | on-demand runs, minutes; scheduled runs inside Apify; no dataset snapshots | actor prices differ between the store header and the README; store them as config |
| Bright Data Web Scraper API | Instagram profiles, posts, reels; Facebook page posts; X posts, profiles; TikTok; LinkedIn; Reddit posts; YouTube | $1.50/1k pay-as-you-go, pay only for success; Scale $499/month incl. 384k records then $1.30/1k; free tier 5k records/month | on-demand, API | Phyllo's table shows $0.75–1.00/1k at volume; the pages show three prices (U) |
| Bright Data Datasets | the same platforms, no Facebook groups or events | from $2.50/1k, smallest tier 100k records $250 one-time | pre-collected snapshots; refresh one-time, quarterly, monthly; "refreshed monthly" | bulk backfill, not 24/7 harvesting |
| EnsembleData | TikTok, Instagram, YouTube, Threads, Reddit, Twitch, Twitter, Snapchat (no Facebook) | $100/month (1,500 units/day), $200 (5,000), $400 (11,000); 50 units/day free | daily units, reset every 24h; TikTok user posts = 1 unit per 10 posts, Reddit subreddit posts = 2 units per 30, Instagram user posts billed per post | unused units expire daily |
| Data365 | Facebook, Instagram, X, TikTok, Reddit, Pinterest, Threads | €300/month (1 network, 500k credits), €850 (3 networks, 1M); post = 1 credit, search = 7, profile = 9 | credit-based API; real-time claim is marketing copy | only the larger Facebook-capable option besides Apify and Bright Data |
| ScrapeCreators | Instagram, TikTok, YouTube, X, Facebook, Reddit and others | packs: $47 for 25k credits (~$1.88/1k), $497 for 500k (~$0.99/1k) (secondary, U) | one credit per request, not per post | `/pricing` page returns 404; figures from the homepage and comparison sites |
| X-only: twitterapi.io, SocialData | X | ~$0.18–0.20/1k profiles (Phyllo table, Jul 2026) | per-item balance | cheaper than official reads |

### 3.2 Actors and prices that matter

| Platform | Actor | Price | Inputs and limits |
|---|---|---|---|
| Instagram | `apify/instagram-scraper` | $1.50 (Business) – $2.70 (Free)/1k results | profile, hashtag, place, post URLs; keyword search by hashtag, place or user; public data only, "as a logged-out visitor"; private profiles not returned; `likesCount = -1` when hidden |
| Instagram | `apify/instagram-post-scraper` | from $1.00/1k; README $2.30 Starter | usernames, profile or post URLs; `onlyPostsNewerThan`; reposts not included |
| Facebook | `apify/facebook-posts-scraper` | header $2.00/1k; README $5 ($4 on Starter), date filter +$2 | page URLs; header and README conflict |
| Facebook | `apify/facebook-groups-scraper` | header $2.60/1k; README ~$5 | public groups only; no login or cookies |
| Facebook | `apify/facebook-events-scraper` | header $7.00/1k events; README $13 base, $10 Starter, $8.50 Scale | event search by keyword and location, event, page (`upcoming_hosted_events`), group URLs; filter URLs must be copied logged-out; pages and groups return only the recent events visible without scrolling, so schedule runs; some keywords are hidden from logged-out users and return 10–30 events |
| TikTok | `clockworks/tiktok-scraper` | from $1.70/1k; video downloads, transcription, AI summary billed extra | profiles, hashtags, search, post URLs; "Popular" sort returns only ~400–500 videos per profile |
| X | `apidojo/tweet-scraper` | $0.40/1k tweets; other actors $0.15–0.30/1k | min 50 tweets per query; no single-tweet or reply scraping; 1 concurrent run |
| Reddit | `trudax/reddit-scraper-lite` | from $3.40/1k results | lists stop near 1,000 items; no login |
| YouTube | `streamers/youtube-scraper` | from $2.40/1k videos | not needed — the official API is free |

### 3.3 Legal posture

| Case | Date | Holding | Reading for Harvest |
|---|---|---|---|
| Meta v. Bright Data, N.D. Cal. 3:23-cv-00077 (Chen) | 2024-01-23; Meta later dropped the case and waived appeal (MediaPost, early 2024) | Facebook and Instagram terms govern a user's own use of the products and do not reach logged-off collection of public data, so no breach of contract | logged-out public reading is not a contract breach by the scraper; the ruling is district-level, not appellate |
| X Corp. v. Bright Data (Alsup) | 2024-05-09 dismissal; 2024-11-26 leave to amend | contract and tort claims about selling public posts preempted by copyright; claims on server impairment (trespass to chattels) allowed to proceed; Bloomberg Law reported a settlement on 2025-06-23, terms confidential (U) | copyright preemption helps, but heavy load on a platform's servers is a live theory |
| Meta v. Voyager Labs | motion to dismiss denied; settlement approved later (date not found, U) | 38,000 fake Facebook accounts used to scrape 600,000 users; settlement bars scraping and requires deletion | logged-in scraping with fake accounts is the clear line |
| LinkedIn v. Proxycurl | resolved 2025-07-28 (LinkedIn); Proxycurl shut down | injunction and data deletion reported (secondary, U) | LinkedIn litigates aggressively |
| LinkedIn v. ProAPIs, Netswift | filed Oct 2025; court-approved settlement later (date not found, U) | stop mass scraping, stop selling the data, no fake accounts, delete data | same |
| Reddit v. Perplexity, SerpApi, Oxylabs, AWMProxy (S.D.N.Y., Engelmayer) | filed 2025-10-22; motions to dismiss largely denied 2026-07-31 | DMCA anti-circumvention claim survives where scrapers bypass a bot-detection control (Google SearchGuard); unjust enrichment and unfair competition dismissed; a pleadings ruling, not liability | bypassing CAPTCHA or bot walls creates exposure beyond contract |
| Google v. SerpApi (N.D. Cal.) | 2026-07-20 | dismissed in part: no circumvention claim over material Google does not own | ownership of the underlying copyright matters; courts are split |

- Meta's **Automated Data Collection Terms** (effective 2024-10-07, after the Chen ruling) bar automated collection of Meta products without Meta's express written permission, bar selling or transferring collected data, and bar collecting non-public personal data. Whether they bind a logged-out, non-user scraper is untested (U).
- Instagram's terms bar collecting information "in an automated way" without permission (Nov 2021 change); LinkedIn's User Agreement §8.2 bars scraping and copying content "directly or through third parties (such as … data aggregators or brokers)".
- Reddit Data API Terms: user content may be copied and displayed only as necessary to run the app; no training of ML or AI models without rightsholders' permission; delete data beyond the approved use and delete cached content on termination.
- Apify states that scraping public data is generally legal, that logged-in data needs extra care, and that the user carries the legal responsibility (blog, Feb 2026). Bright Data's position, per the Meta case reporting, is that it collects only publicly available data. Neither vendor shifts liability from the buyer.
- **Clearly prohibited, whatever the route:** logged-in scraping or fake accounts; bypassing CAPTCHA, bot detection or IP blocks; private accounts, private groups and non-public personal data; selling or licensing Meta Platform Data; AI training on Reddit content; downloading or caching YouTube audiovisual content; scraping YouTube from an API client.

---

## 4. Public page route (Route C)

| Platform | Logged-out web in 2026 | oEmbed | Feed | Verdict |
|---|---|---|---|---|
| Instagram | profile picture, bio, counts and a grid of ~6–12 recent posts, then a login wall; followers, full comments, stories hidden; post permalinks unreliable (blogs, U) | Graph oEmbed, display only | none | not a Harvest route; providers do this work |
| Facebook | public Pages, public groups and event pages load logged-out; Apify actors rely on it; some searches hidden from logged-out users | Graph oEmbed (same terms as Instagram, U) | none | provider only |
| X | single posts load logged-out (30/30 in one vendor test); Replies, Media tabs and search redirect to login (10/10) — vendor test, date unknown (U) | `publish.x.com/oembed`, no auth, not rate limited, returns HTML | none | no |
| Reddit | `.json` access for logged-out clients reported blocked since late May 2026; RSS ends 2026-11-13; Old Reddit being limited to logged-in users | — | RSS closing | closed |
| TikTok | public video pages load logged-out (providers depend on it, U) | `tiktok.com/oembed` (not read, U) | none | provider only |
| YouTube | public pages and per-channel RSS | `youtube.com/oembed` (not read, U) | RSS, 15 latest | RSS is a cheap poller; the API is the route |
| Threads | public posts on the web (U) | tokenless `oembed` since ~2026-03 (WordPress core ticket, U); display only, persisting and analytics prohibited | none | API is the route |
| LinkedIn | partial public profiles | none | none | prohibited by the User Agreement |
| VK, OK | public communities visible logged-out (U) | — | — | later |

- OpenGraph on social URLs yields a caption snippet and one image at best (U); a pasted social link goes to the platform adapter (single-post lookup), not a generic page fetch ([T3](t3-web-sources.md) owns generic link intake).
- Harvest should not run Route C itself against Instagram, Facebook, TikTok, X or LinkedIn: it is the same act as Route B without the provider's proxy and breakage handling, and it makes Harvest the party exposed to the access-control theories in section 3.3.

---

## 5. Fields, deletion, media and rate limits

### 5.1 Fields by pick route

Cells say what the route returns; `–` = not returned; (U) = inferred, not read in docs.

| Platform (route) | Text | Author | Posted at | Media | Location | Engagement | Edit signal |
|---|---|---|---|---|---|---|---|
| Instagram (A, business discovery) | caption | the queried account | `timestamp` | `media_url` (omitted for videos with licensed audio and reels with downloads off), `thumbnail_url`, `children` | – (U) | `like_count`, `comments_count`, `view_count` | none |
| Instagram (B, Apify) | caption, hashtags, mentions | owner details | timestamp | image and video URLs, carousel children | place scraper returns coordinates and address; per-post location (U) | likes (`-1` if hidden), comments, first and latest comments, views | none seen |
| Facebook Pages (A, PPCA) | post message | Page | `created_time` (U) | attachments (U) | – | reactions, comments, shares (U) | `updated_time` (U) |
| Facebook posts, groups (B) | text, links | author name and ID | timestamp | media URLs, video URLs, transcripts | – | reactions by type, comments (top), shares | none seen |
| Facebook events (B) | name, description | organizer name, URL, verified flag | start, end, UTC start, duration, canceled flag | image | venue, address, coordinates, country code | going, interested, responded | canceled flag; no edit time |
| X (A) | `text`, `entities` (hashtags, URLs, mentions) | `author_id` (+ user expansion) | `created_at` | `attachments` → media expansion | `geo.place_id` when tagged | `public_metrics` (retweets, replies, likes, quotes, impressions, bookmarks) | `edit_history_tweet_ids`, `edit_controls` |
| Reddit (B) | title, body | `username` | `createdAt` | image and video URLs with `includeMediaLinks` | – | upvotes, ratio, comment count with `includeMediaLinks` | none seen |
| TikTok (B) | `text`, hashtags, mentions | `authorMeta` (name, id, fans, verified) | `createTime` | video, cover, slideshow, subtitle links | `locationCreated` | play, digg, share, comment, collect counts | none |
| YouTube (A) | title, description, tags (`snippet`) | channel | `publishedAt` | thumbnails, `player` embed; no download | `recordingDetails` when set | `statistics`: views, likes, comments | none; compare `snippet` between polls |
| Threads (A) | `text`, `link_attachment_url`, `topic_tag` | `username`, `is_verified`, `profile_picture_url` | `timestamp` | `media_url`, `thumbnail_url`, `children`, `gif_url` | – | none on others' posts | none |
| LinkedIn, VK, OK | no adapter | | | | | | |

### 5.2 Deletion, media and rate limits

| Platform (route) | Deletion detectable for scheduled checks | Media download rule | Binding limits |
|---|---|---|---|
| Instagram (A) | re-list the account's media and diff; direct fetch of others' media fails by design; hashtag media vanish after 24h | `media_url` returned except licensed-audio videos and no-download reels; Meta Platform Terms §3.d: delete when no longer needed or on request (CDN URL lifetime not checked, U) | 30 hashtags per 7 days; business-use-case rate limits (numbers not found, U) |
| Instagram (B) | re-scrape the post URL; provider returns an error item (U) | media URLs point to Instagram's CDN; copying is a copyright act per photo owner | provider run limits |
| Facebook Pages (A) | `GET` on a deleted post returns an error (U) | as Instagram (A) | `4,800 × engaged users` per 24h (U) |
| Facebook groups, events (B) | re-scrape; event pages carry a canceled flag | as above | events actor shows only recent events |
| X (A) | **Batch Compliance** (upload post IDs, async): events `delete` (reasons `deleted`, `protected`, `deactivated`, `suspended`), `rehydrate` (`tweet_edited`), `scrub_geo` (delete stored geo); developers must use reasonable efforts to honour deletions and edits | media via expansions; X Developer Policy applies (not read, U) | credits; 24h dedup; 3M reads/month |
| Reddit (B) | re-fetch; removed and deleted markers (U) | Data API Terms §2.4 if ever on Route A | — |
| TikTok (B) | re-scrape; error item `errorCode` | video download is a separately billed provider event | provider limits |
| YouTube (A) | `videos.list` by ID: removed videos drop from `items` (U, docs show `videoNotFound` on some calls); **policy: verify every 30 days that stored videos still exist; delete user-requested data within 7 days** | no download, offline use or caching of audiovisual content; public API data may be kept ≤30 days, then refresh or delete | 10,000 units/day, `search.list` 100/day |
| Threads (A) | `GET /{media-id}` fails when removed (U); ghost posts carry `ghost_post_status` | `media_url` in fields; oEmbed forbids persisting | keyword 2,200/24h per user; profile posts 1,000/24h per user |

---

## 6. Route ladder, pick and cost at 10k posts/month

Provider prices are the cheapest listed Starter-to-Business rates; add the Apify plan fee ($19 Starter, whose credit counts against usage) once for all Apify actors.

| Platform | Ladder | Pick | Cost per month at 10k posts | Notes |
|---|---|---|---|---|
| Instagram | A business discovery (known business accounts) → B provider (everything else) → C never | A for the brand list; B for hashtags, locations, personal accounts | A: $0 · B: $10–27 | A needs a Harvest-owned professional account and token upkeep |
| Facebook Pages | A PPCA → B Apify posts | B first, A when business verification passes | A: $0 · B: $20–50 | A gives engagement fields and a stable contract |
| Facebook public groups | B only | `apify/facebook-groups-scraper` | $26–50 | public groups only |
| Facebook events | B only | `apify/facebook-events-scraper`, scheduled | $70–130 per 10k events; 500–2,000 events/month realistic = $4–26 | recent-events-only behaviour needs frequent runs |
| YouTube | A API → A RSS poller | API: `playlistItems.list` per channel's uploads playlist, then `videos.list` in batches of 50 | $0; ~400 of 10,000 daily units for 10k posts | `search.list` is capped at 100/day |
| Threads | A keyword search and profile posts | A; apply for `threads_keyword_search` and `threads_profile_discovery` | $0 | review time not found (U) |
| X | A pay-per-use → B provider | A if a source needs X; hard budget cap | A: $50 · B: $1.5–4 | $0.005 per post read; owned reads $0.001 |
| TikTok | B → none | `clockworks/tiktok-scraper` | $17+ | Research and Display APIs do not apply |
| Reddit | A closing → B | skip until a consumer asks | B: $15–34 | official route closes to new apps 2026-10-31 |
| LinkedIn | none | no adapter | — | Bright Data lists LinkedIn at $1.50/1k, but the User Agreement and the lawsuits make it a no |
| VK | A | defer | $0 within 10,000 calls/month (U) | each `wall.get` call returns up to 100 posts (U) |
| Odnoklassniki | none found | no adapter | — | |

Modest basket for the two known consumers (Instagram 10k, Facebook groups 5k, Facebook events 1k, YouTube, Threads): about $55/month on Apify Starter.

### What Harvest must model

- **`ProviderAccount`** — kind (`meta-app`, `threads-app`, `x-api`, `google-api-key`, `apify`, `brightdata`, `ensembledata`, `vk-app`), owner (WoW2 or tenant), credential reference in the vault, granted features (`Instagram Public Content Access`, `threads_keyword_search`), review status and date, token expiry with a refresh job, balance for prepaid providers (X credits, Apify, ScrapeCreators).
- **Route ladder per platform** — ordered A/B/C entries with an enabled flag and a legal-posture tag per route; fallback on outcomes `not_approved`, `quota_exhausted`, `blocked`, `provider_failed`, `budget_exceeded`.
- **Per-platform adapter config** on a source: Instagram `accounts[]`, `hashtags[]`, post types, `resultsLimit`, `onlyPostsNewerThan`; Facebook `pageUrls[]`, `groupUrls[]`, event search (keywords, location, `maxEvents`); YouTube `channelIds[]`, `publishedAfter`; Threads keyword or tag or username; X query and `since_id`.
- **Quota ledger** for official routes — YouTube units per day (reset midnight PT), Threads queries per user per 24h, Instagram hashtags per 7 days, X credits and dedup window.
- **Cost ledger and budget** — provider usage and USD per run, a monthly budget per pipeline (soft warning, hard stop) and a global cap per provider; store each provider's price with a last-checked date, since vendor pages contradict each other.
- **Compliance jobs** — X Batch Compliance, YouTube 30-day verify, Meta delete-on-request handling, Reddit purge on termination.
- **Per-capture legal metadata** — route class, provider, `loggedOut = true`, retention class (YouTube 30 days, Meta delete-when-unneeded, X compliance events), terms version read.

---

## 7. Consumer lens

- **Ocharo** — fashion events and brands in Central Asia: Instagram matters most (brand accounts through business discovery, hashtags and competitors through a provider), Facebook events through a provider, YouTube channels for shows through the official API; about $25–60/month.
- **Haven** — rental listings in Tashkent: Instagram realtor accounts through a provider (personal accounts cannot use business discovery) and public Facebook groups through a provider; Telegram sits in [T1](t1-messaging-sources.md); about $20–50/month.

---

## Findings that change the spec

- The spec's "must honour each source's terms … prefers a provider API" cannot hold for Instagram, Facebook, TikTok, X and Reddit through licensed providers: Meta's Automated Data Collection Terms (2024-10-07) forbid automated collection without written permission, while Meta v. Bright Data (2024-01-23) held contract terms do not reach logged-out public scraping. The spec needs route classes A/B/C with a posture tag and a developer sign-off on Route B.
- "Provider API" is two things — an official platform API and a licensed third-party data provider; the spec and the adapter model should name both and let a platform hold a ladder of routes.
- Official routes are narrow: Instagram business discovery reads known business accounts only, and hashtag search sees 24 hours, 30 hashtags per week, for own-campaign uses; Facebook Events need Marketing Partner status and the Groups API is gone; TikTok and LinkedIn offer nothing; Reddit closes to new apps on 2026-10-31.
- Reddit: RSS ends 2026-11-13, new public API access requests stop 2026-10-31 and public access closes March 2027 (secondary reports, U); a Reddit adapter would be provider-only, and Reddit barely matters in UZ (262K).
- YouTube `search.list` moved to its own 100 calls/day bucket (quota page updated 2026-10-15); discovery by search is capped, while channel monitoring through `playlistItems.list` costs 1 unit per 50 posts.
- Platform retention duties contradict "immutable capture": YouTube data ≤30 days then refresh or delete, existence check every 30 days, user deletion within 7 days; Meta deletion on request or when unneeded; X `delete`, `rehydrate` and `scrub_geo` events; Reddit deletion on termination. Capture retention and deletion checks must be per-source policy, and mandatory on official routes ([T5](t5-post-model.md)).
- Meta Platform Terms §3.a.iv and §3.c (sell, license, share) and Instagram Public Content Access's allowed uses conflict with a shared harvest pool served to many apps; a provided service (form 3) delivering Meta API data to other apps needs a legal read before it ships.
- Meta app review is per app and per owner: a self-hosted Harvest (form 2) cannot use WoW2's approved Meta or Threads app, so credentials must be per tenant, and the console needs a guided "bring your own provider account" flow.
- oEmbed for Instagram and Threads forbids persisting or analytics, so it serves link-intake display only; a pasted social URL needs a per-platform single-post lookup (Threads media, YouTube `videos.list`, X lookup at $0.005, provider for Instagram, Facebook and TikTok).
- Cost is small: 10k posts/month costs $0 (YouTube, Threads), $10–50 (Instagram, Facebook, TikTok, Reddit) and $50 on X official; per-pipeline budgets matter mainly for X's per-resource billing and the Facebook events actor (~$7–13/1k).
- Vendor price pages contradict themselves (Apify store header vs README, Bright Data three prices, ScrapeCreators `/pricing` 404); Harvest should read billed usage from each run instead of trusting listed prices.
- Facebook public events are available only through a logged-out provider that returns the events visible without scrolling and hides some keywords from logged-out users, so event pipelines need frequent runs and an explicit "partial" outcome.
- Instagram reach in UZ (14.1M) dwarfs every other platform tracked here, X is at 148K and falling, and Threads is the only platform with a free official keyword search; build order Instagram, Facebook, YouTube, Threads, with X, Reddit, TikTok, LinkedIn, VK and OK deferred.

---

## Points

Open questions; each ends in a provisional pick.

- [ ] S1 may Harvest use Route B (licensed providers on logged-out public pages) for Instagram, Facebook and TikTok despite platform terms → provisional pick: yes, public logged-out data only, providers must attest no accounts and no bypass, each capture tagged with its route; counsel reads Meta's 2024 Automated Data Collection Terms first (T8)
- [ ] S2 which entity owns the Meta, Threads, X and Google credentials, and can it pass Meta business verification from Uzbekistan → provisional pick: the parent company chosen in `ven-t-012`; try verification early, run Route B until it passes (T8)
- [ ] S3 self-hosted and provided forms: credentials per tenant or shared → provisional pick: per tenant for self-hosted, WoW2-owned for the provided instance with a per-consumer budget (T7, T8)
- [ ] S4 retention class per source (YouTube ≤30 days, Meta delete-when-unneeded, X compliance events) → provisional pick: a `retentionPolicy` on each source route, applied by a purge job; captured text stays immutable inside its window (T5)
- [ ] S5 deletion-check cadence per platform → provisional pick: X Batch Compliance daily, YouTube every 30 days at most, provider-routed posts weekly re-scrape of the newest 30 days only, because each re-scrape is billed (T5, T7)
- [ ] S6 first social adapters → provisional pick: Instagram (business discovery plus Apify), Facebook groups and events (Apify), YouTube (API), Threads (API, App Review in parallel); X, Reddit, TikTok, LinkedIn, VK, OK wait for a named consumer (T4)
- [ ] S7 budget enforcement → provisional pick: a monthly USD cap per pipeline with a soft warning at 80% and a hard stop, plus a global cap per provider (T7)
- [ ] S8 first provider → provisional pick: Apify (actors for Facebook groups and events, pay-per-event, no minimum); Bright Data Scraper API as the second implementation behind one provider-runner interface (T3)
- [ ] S9 media: store or link → provisional pick: store only thumbnails and the first image for event and listing items; link the rest; never download YouTube video; CDN URL lifetimes tested before relying on them (T5)
- [ ] S10 are Haven's Instagram sources business or personal accounts → provisional pick: assume personal, so Route B; confirm with a sample of 10 realtor accounts (T4)
- [ ] S11 one Meta app for Harvest reads and the social connectors' publishing, metrics and sign-in, or separate apps → provisional pick: separate apps, so a review rejection or a ban on the reading app leaves publishing alive (T4, T8)
- [ ] S12 personal data in captured posts (realtors, private group members) → provisional pick: store only fields a pipeline's schema needs, keep author handle but not profile data, defer the Uzbek personal-data-law read (database registration, localization; see [identity T1](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.identity/blob/main/engineering/research/identity-analysis-2026-10/t1-integrations.md) finding, U) to the T5 pass (T5)

---

## Sources

Instagram and Meta
- https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/business_discovery — business discovery permissions, field expansion, age-gated exclusion
- https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-facebook-login/business-discovery — public fields, media GET fails, `media_url` omissions
- https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-facebook-login/hashtag-search — 30 hashtags per 7 days, App Review
- https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-hashtag/recent-media — 24-hour window, ads excluded, 50 per page
- https://developers.facebook.com/documentation/development/features-reference/instagram-public-content-access — allowed usage, business verification
- https://developers.facebook.com/documentation/development/features-reference/page-public-content-access — Page Public Content Access, endpoints, review
- https://developers.facebook.com/docs/graph-api/reference/event/ — Events limited to Marketing Partners
- https://developers.facebook.com/docs/graph-api/changelog/version19.0 — Groups API deprecation, 2024-04-22
- https://www.gigazine.net/gsc_news/en/20240206-meta-cuts-third-party-access-facebook-groups — Meta statement of 2024-01-23 (secondary)
- https://developers.facebook.com/docs/instagram-platform/oembed — Instagram oEmbed limits and no-persist rule
- https://developers.facebook.com/documentation/threads/tools-and-resources/embed-a-threads-post — Threads oEmbed, 1,000/hour, display only
- https://core.trac.wordpress.org/ticket/64858 — Threads tokenless oEmbed, March 2026 (secondary, U)
- https://developers.facebook.com/docs/content-library-api/get-access and https://developers.facebook.com/docs/content-library-and-api/support/faqs — Meta Content Library eligibility, no export
- https://developers.facebook.com/terms/dfc_platform_terms/ — Meta Platform Terms, last changed 2026-02-03 (read in a Russian render): §3.a.iv, §3.c, §3.d
- https://www.facebook.com/legal/automated_data_collection_terms — Automated Data Collection Terms, effective 2024-10-07
- https://opentermsarchive.org/en/memos/instagram-blocks-data-retrieval-and-clarifies-what-information-it-retrieves/ — Instagram terms change, Nov 2021
- https://data365.co/facebook-search-api — Graph search restriction timeline (vendor, secondary)
- https://www.getphyllo.com/post/instagram-api-rate-limits-explained-and-how-to-scale-beyond-them-2026 — rate-limit claims (vendor, U)

Threads
- https://developers.facebook.com/documentation/threads/keyword-search — keyword search, 2,200/24h, permissions
- https://developers.facebook.com/documentation/threads/retrieve-and-discover-posts/retrieve-posts — `profile_posts`, ≥100 followers, 1,000/24h, field list
- https://developers.facebook.com/documentation/threads/overview — `4,800 × impressions` rate formula

X
- https://docs.x.com/x-api/getting-started/pricing — pay-per-use prices, 24h dedup, 3M cap
- https://docs.x.com/x-api/posts/search/introduction — recent and full-archive search
- https://docs.x.com/x-api/fundamentals/data-dictionary — Post fields, edit fields, geo
- https://docs.x.com/x-api/compliance/batch-compliance/introduction — `delete`, `rehydrate`, `scrub_geo`
- https://docs.x.com/x-for-websites/oembed-api — oEmbed, no authentication (search snippet)
- https://developer.x.com/en/docs/x-api/compliance/streams/integrate/honoring-user-intent — duty to honour deletions (search snippet)
- https://www.medianama.com/2026/02/223-x-developer-api-pricing-pay-per-use-model/ — launch of pay-per-use (secondary; dates differ, Jan 21 or Feb 6)
- https://twitterapi.io/blog/twitter-web-viewer — logged-out X test (vendor, undated, U)

Reddit
- https://www.redditinc.com/policies/data-api-terms — Data API Terms, last revised 2026-07-20 (read via curl; the page body)
- https://decrypt.co/379892/reddit-killing-rss-feeds-public-api-access-ai-scrapers — RSS end 2026-11-13, API access dates (2026-10-01, secondary)
- https://openrss.org/blog/go-easy-on-the-feeds-reddit — Reddit post of 2026-05-28 on scraping and RSS (secondary)
- https://dev.to/tonywangca/why-reddit-blocked-unauthenticated-json-in-2026-and-how-to-still-get-reddit-data-58b9 — unauthenticated `.json` blocked (vendor-authored, U)
- https://r.datuan.dev/r/redditdev/comments/1oug31u/introducing_the_responsible_builder_policy_new/ — Responsible Builder Policy announcement mirror, Nov 2025 (Reddit's support page returned 403)
- https://octolens.com/blog/reddit-api-pricing — "$0.24 per 1,000 calls" (third-party, U)
- https://reddit.rtrace.io/r/redditdev/comments/13wsiks/api_update_enterprise_level_tier_for_large_scale/jnhaz5f — 100 queries/minute (2023, `stale`)

TikTok
- https://developers.tiktok.com/products/research-api — Research API eligibility (search snippet; the developer site timed out on 2026-10-26)
- https://www.getphyllo.com/post/tiktok-api-integration-guide-2026-setup-endpoints-common-pitfalls — Display API scope and audit (vendor, U)
- https://scrapebadger.com/blog/tiktok-scraping-apis-in-2026-the-complete-deep-guide — Research API limits and commercial exclusion (vendor, U)
- https://kinit.sk/when-research-apis-close-the-door/ — approval took 21 months in one case (U)

YouTube
- https://developers.google.com/youtube/v3/determine_quota_cost — quota costs, `search.list` 100/day bucket (page updated 2026-10-15, read raw)
- https://developers.google.com/youtube/v3/getting-started — default quota, extension form
- https://developers.google.com/youtube/terms/developer-policies — 30-day refresh, 7-day deletion, no download, no scraping
- https://developers.google.com/youtube/v3/docs/videos/list — parts, `videoNotFound`
- https://discuss.ai.google.dev/t/youtube-rss-feed-endpoint-returns-404-errors/113379 — RSS 404s, Jan 2026 (U)

LinkedIn, VK, OK
- https://www.linkedin.com/help/linkedin/answer/a1341387 and https://www.linkedin.com/legal/user-agreement — scraping prohibition incl. via data brokers
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api — Posts API, organization scope (search snippet)
- https://bundle.social/blog/linkedin-api-permissions — `r_member_social` closed, approval tiers (vendor, U)
- https://news.linkedin.com/2025/LinkedInWinsLegalBattleToProtectMemberData — Proxycurl, 2025-07-28
- https://therecord.media/linkedin-wins-court-order-blocking-mass-scraping — ProAPIs, Netswift settlement (search snippet)
- https://dev.vk.ru/en/api/overview — monthly call limits from 2026-09-07
- https://www1.ru/en/news/2026/09/09/vxod-zakryt-vkontakte-zablokirovala-dostup-kate-mobile.html — VK limits enforcement (secondary)
- https://qna.habr.com/q/303145 and https://jentic.com/apis/ok.ru/ok.md — OK API permissions (old, third-party, U)

Uzbekistan audiences
- https://datareportal.com/reports/digital-2026-uzbekistan — platform ad reach, Kepios data of Oct 2025
- https://napoleoncat.com/stats/social-media-users-in-uzbekistan/ — Facebook and Instagram audiences (2026 snapshots via search results)
- https://www.wmtips.com/technologies/social-media/country/uz — website-share proxy (weak)
- https://ahrefs.com/websites/uzbekistan/social-networks — search traffic by social site, Jul 2025

Providers
- https://apify.com/pricing — plans, compute units, pay-per-event
- https://apify.com/apify/instagram-scraper · https://apify.com/apify/instagram-post-scraper · https://apify.com/apify/facebook-posts-scraper · https://apify.com/apify/facebook-groups-scraper · https://apify.com/apify/facebook-events-scraper · https://apify.com/clockworks/tiktok-scraper · https://apify.com/apidojo/tweet-scraper · https://apify.com/trudax/reddit-scraper-lite · https://apify.com/streamers/youtube-scraper — actor prices, inputs, limits
- https://brightdata.com/pricing/web-scraper-api and https://brightdata.com/pricing/datasets — records pricing and platform coverage
- https://ensembledata.com/pricing — daily-unit plans and endpoint costs
- https://data365.co/pricing — euro plans and credit weights
- https://www.getphyllo.com/post/social-data-api-pricing — vendor comparison and price contradictions (Phyllo sells a consent-based product)
- https://scrapecreators.com/blog/best-social-media-scraping-apis — ScrapeCreators packs (vendor, U)
- https://peekstories.com/blog/instagram-web-vs-app-what-you-can-see-2026 — logged-out Instagram view (blog, U)

Court rulings and legal posture
- https://www.fbm.com/post/102kqw7/ — Meta v. Bright Data summary judgment, 2024-01-23
- https://www.mediapost.com/publications/article/393996/meta-abandons-lawsuit-against-bright-data-over-scr.html — Meta dropped the case
- https://www.mediapost.com/publications/article/395944/judge-throws-out-xs-claims-against-data-scraper.html — X v. Bright Data dismissal, 2024-05-09
- https://www.mediapost.com/publications/article/401510/x-corp-can-revive-scraping-battle-with-bright-dat.html — leave to amend, server impairment, 2024-11-29
- https://blog.ericgoldman.org/archives/2025/01/catching-up-on-the-heavyweight-scraping-battle-between-x-and-bright-data-guest-blog-post.htm — amended claims allowed, counterclaims
- https://news.bloomberglaw.com/ip-law/musks-x-settles-data-scraping-dispute-against-israeli-data-firm — settlement report, June 2025 (search snippet, U)
- https://www.mediapost.com/publications/article/401661/analytics-company-voyager-labs-settles-scraping-ba.html — Meta v. Voyager Labs settlement (search snippet)
- https://www.mediapost.com/publications/article/416950/reddit-can-proceed-with-scraping-claims-against-pe.html — Reddit v. Perplexity, SerpApi, 2026-07-31
- https://dataimpulse.com/blog/2026-data-court-cases-what-the-reddit-vs-perplexity-lawsuit-means-for-data-teams/ — 2026 cases, Google v. SerpApi (vendor, secondary)
- https://blog.apify.com/is-web-scraping-legal/ — Apify's legal posture, Feb 2026
