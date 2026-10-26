# T9 — Steps and capabilities

*Last updated: 2026-10-26*

> How a pipeline reaches a source that resists it. A pipeline is a declared sequence of steps; each step is a broker
> call that states the capabilities it needs — egress, session, render, profile, challenge handling, pacing, an
> account lease, a provider run, AI — as a floor, a ladder and a ceiling. The runner resolves them at claim time and
> learns, per host and per lane, the cheapest rung that works. Social holds every capability provider and its
> secrets, and all platform clients; Harvest holds the engine and the non-social site adapters. Source terms are no
> longer honoured (developer, 2026-10-26), so 24 earlier picks change, while the posture fields stay as switches.

- Aliases: `W` = `/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws` · `ls` = `W/workbench/maxs-projects/ventures/saas/ventures.listing-shelf/engineering/codebase/listing-shelf.backend-services` · `hv` = `W/workbench/maxs-projects/ventures/saas/10x-ven-haven` · `hvb` = `hv/engineering/codebase/haven.backend-services` read at `65a355ad^` (the tree before the 2026-09-26 rebuild deleted it) · `rce` = `hvb/Haven.Channels.RenderedContentExtractor` · `be` = `W/workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src` (at `6f55cfe`, `10.0.81-beta`).
- Codes from the lead document and T1–T8 (P1–P20, S, W, T4-n, T5-n, T6-n, T7-Pn, T8-n); `(U)` = unverified.
- Facts come from code reads, `git show` of Haven's history, the earlier tracks and public vendor pricing pages, all on 2026-10-26. No target site was probed; nothing was built, bought or signed in to.

---

## Verdict

- **A pipeline is a declared list of steps.** An adapter declares step brokers (`enumerate` · `detail` · `contact` · `media` · `thread` · `check` · `metrics` · `provider-job` · `account-op`), each with its capability requirements. T7's work kinds become named step plans, and render is a capability a step requires, not a step.
- **Capabilities resolve at claim, and ladders learn per host lane.** A step states a floor, a ladder and a ceiling. The resolver picks the rung from `host_lane` state, reserves budget and leases egress and sessions. Three challenges in a row promote one rung; a daily probe demotes; a rate limit paces and never promotes.
- **One exact step gets its own lane.** OLX's phone reveal ran through the friction challenge API over rotating residential proxies in Haven (March 2026) and returned `captcha_triggered` when the challenge was not blank. It becomes a `contact` step in lane `olx.uz#contact` with a residential floor, while detail pages start direct. A block in one lane never pauses another.
- **The cut under answer 1.** Social holds the platform clients (read, post, trends, own-account monitoring) and every capability provider with its secrets: egress pools and IP servers, sessions and account pools (the Telegram MTProto pool moves out of Harvest), the browser, solvers and provider runners. Harvest holds the engine (steps, resolver policy, ladders, runs, posts, dedup, extraction, subscriptions, trends learning, mass actions) and the non-social site adapters.
- **The chain holds, and slice 1 does not wait.** core → Identity → Files → Social → Harvest → Events still sorts; `Harvest.Module` gains one edge, to `Social.Abstractions`. Slice 1 needs only direct egress, anonymous cookie jars, profiles, challenge detection and pacing. These are built inline behind Social-shaped contracts and move to Social at the +0.1 after Harvest's first paid capability.
- **Posture.** 24 earlier picks change (§ 5.1). `permission`, `ai_allowed`, `pool_shareable`, `posture` and the new `robots_policy` stay as fields with permissive defaults, so a ban or a takedown is a one-row `UPDATE`. Afisha joins slice 1, and Telegram gets AI extraction.
- **Wrap IPs and solvers; build the plumbing.** Residential egress lists at $2–8/GB, though GeoNode lists $0.30–0.88. Bright Data and Oxylabs publish Uzbekistan pools. Solvers cost $0.30–3 per 1,000. A Tashkent VPS as an "IP server" runs about $25–30 a month for egress tied to one identity. Harvest builds the leases, health, ladders and budgets.
- **Telegram and WhatsApp send stay in core `Comms`.** Identity sits left of Social and sends OTPs; posting to channels is Social's.

---

## 1 · Step model

### 1.1 What exists

| Prior art | Steps | Capability choice | Evidence |
|---|---|---|---|
| ListingShelf | two broker calls: `DiscoverAsync` (list page → links + next page) and `CaptureAsync` (detail), plus helpers `ListingOf`, `IsPhotoUrl`, `ThumbnailUrl`; run steps fixed at `Discover` · `Capture` · `Archive`; work types `Capture` · `Discover` · `Refresh` | none: one client, no proxy, no cookies, one 500 ms run-wide pause | `ls/ListingShelf.Application/Providers/Brokers/IListingBroker.cs:15-39` · `Domain/Runs/Enums/StepKey.cs:7-13` · `Domain/Pipelines/Enums/WorkType.cs:7-13` · `Infrastructure/Runs/Settings/RunExecutionSettings.cs:7` |
| ListingShelf blocks | a challenge page during discovery returns `Unrecognized`; during capture it throws `AccessBlocked`; the capture loop stops on `AccessBlocked` or `RateLimited` | stop and report | `Infrastructure/Providers/Brokers/HtmlListingBroker.cs:65-66,110-111` · `Infrastructure/Runs/OrchestrationServices/RunExecutionService.cs:359-365`; charter "no proxy, CAPTCHA bypass or private endpoint" (`ventures.listing-shelf/engineering/architecture/architecture.md:75`) |
| Haven, removed 2026-09-26 | a per-target extraction service: `ListingDataTarget` `Phones` · `ImageUrls`, plus a detail-fetch node | per target: phones over a static client through rotating residential proxies; images in a browser (`PuppeteerSharp` 20.0.0) without a proxy; detail pages through residential "to avoid OLX CloudFront 403s" from a Hetzner VPS | `rce.Abstractions/Settings/Proxy/ProxyProvider.cs:3-13` (Decodo, GeoNode) · `ProxyServerProviderSettings.cs:6` ("Images use no proxy") · `hvb/Haven.Channels.Supply/Infrastructure/Listings/Capturing/Scraping/ScrapeListings/Nodes/FetchDetailsNode.cs:12-13,112-113` · commit `4cd49e62` (2026-03-11) |
| T7 | work item with `route` `static` · `render` · `api` · `provider` · `account` and a `host_key` or `bucket_key` | `route` is a coarse capability tag fixed per item | T7 § 7.2 |

- Haven is the prior art for a capability per step: the same listing took three transports, one per target.
- What Haven lacked: a model. The proxy was a host setting, the captcha outcome meant "skip, retry later" (`rce.Abstractions/Enums/ExternalListingDataExtractionFailureType.cs:12-13`), and nothing learned which transport a host needed.
- Haven's three OLX calls sent three different Chrome identities: UA Chrome 120 (`rce/appsettings.json:14`), UA Chrome 131 (`FetchDetailsNode.cs:22`), client hints Chromium 145 (`rce/…/OlxUzStaticContentPhoneExtractionHandler.cs:40`). A profile catalog (§ 2) exists to stop that.

### 1.2 Step roles

| Role | Does | Emits | Examples |
|---|---|---|---|
| `enumerate` | lists what exists | `detail` targets, the next `enumerate` item, an enumeration-complete flag | OLX list page; Afisha sitemap child; `t.me/s/{ch}?before=` |
| `detail` | fetches one post: a page or an API object | a capture; `contact`, `media` and `thread` targets | OLX ad page; Afisha event page; `channels.getMessages` |
| `contact` | reveals a hidden contact point | contacts on the reading (T5 `link_readings.contacts`) | OLX friction → `limited-phones` |
| `media` | copies images and video into Files | media refs | `olxcdn.com`; Telegram CDN; Instagram CDN |
| `thread` | reads comments and replies | child links (`role = reply`) | Telegram discussion groups |
| `check` | probes whether a post still exists | link state (T5 § 5.3 methods) | `?embed=1` "Post not found"; a 404 |
| `metrics` | snapshots counters outside the content hash | a metric series (T1-P10) | views, reactions |
| `provider-job` | `submit` → `poll` → `collect` a licensed run | captures from dataset items | Apify actor run |
| `account-op` | acts with an account: resolve, join, leave | membership state | Telegram `importChatInvite` |
| `extract` | the T6 cascade | a reading | D, R, E, S, L |

- **Render is a capability, not a step.** The same `detail` step runs static or rendered depending on its rung, so a separate render step would break the ladder (§ 3.3). The caller's "render" example maps to `render: fallback | required` on `enumerate` or `detail`.
- **Fan-out is the frontier.** A step's result enqueues work items for later steps of the same run (a list page yields detail items, a detail yields contact and media items). This is T7's frontier, generalized from URLs to step items.

### 1.3 Work kinds as step plans

| Work kind (T7 § 2.2) | ListingShelf | Steps it runs |
|---|---|---|
| `capture` | `Capture` | `enumerate` → `detail` → (`contact`) → (`media`) → `extract` |
| `discover` | `Discover` | `enumerate` |
| `refresh` | `Refresh` | `detail` → (`contact` once per link) → (`media` when changed) → `extract`, over the known frontier |
| `sweep` | — | `enumerate` (complete) + `refresh` + `check`, three schedule rows |
| `check` | — | `check` |
| `metrics` | — | `metrics` |
| `link` | — | `detail` (single URL) → `extract` |
| `intake` | — | none scheduled: forwards and uploads write captures directly |

- A step in parentheses is optional per pipeline (`steps.contact.enabled`). Across subscribers it merges by OR, as photos do (T7 § 3.3), and its cost is charged to the pipeline.
- `RunExecutionService.cs:73-75` branches on `WorkType`; that branch becomes a lookup of the step plan.

### 1.4 Declaring and overriding

Requirements merge in four layers. The first three are frozen into `runs.frozen` at queue time (T7 § 2.6); the learned rung is state, read at claim, never frozen.

| Layer | Owner | Holds |
|---|---|---|
| adapter default | code | steps, roles, default ladder and ceiling per step, lanes, challenge detectors |
| source policy | operator (`sources` row) | ceiling per step, egress pool and geo, profile, solver allowance, monthly cap |
| pipeline override | `pipelines:manage` (operator, or a tenant admin on a private pipeline) | optional steps on or off; a lower ceiling; a stricter cap |
| step override | the same, inside the pipeline | one step's ladder or lane |
| learned rung | the engine (`host_lane`) | the rung in use, inside floor and ceiling |

- A subscriber cannot widen capabilities, as it cannot widen posture (T7 § 3.3). Raising a ceiling or enabling a paid rung needs `pipelines:manage` and budget headroom.

```yaml
# source policy, olx.uz (placeholder values)
capabilities:
  defaults: { profile: browser:chromium-desktop, session: anonymous/run, ladder: [R0, R3, R4, R5], ceiling: R5 }
  steps:
    contact: { lane: contact, floor: R3, ladder: [R3, R4, R7], ceiling: R4, solver: { maxUsdPer1k: 3 } }
    media:   { ladder: [R0, R3], ceiling: R3 }
budget: { monthUsd: 30, maxUsdPerSuccess: { R3: 0.005, R5: 0.02 } }

# pipeline override, Haven "Tashkent rentals"
steps: { contact: { enabled: true } }
```

### 1.5 Fit with T7: work items, leases, `host_state`

| T7 piece | Change |
|---|---|
| `work_item` | adds `step`, `lane`, `plan_ref` (frozen requirements), `rung` (set at claim), `egress_lease_id?`, `session_lease_id?`; `route` becomes derived from the rung |
| `host_state` (§ 7.3) | stays the global gate per host: concurrency, delay, `Retry-After`, robots, window |
| `host_lane` (new) | `(host_key, lane)`: `rung`, `rung_since`, `consecutive_failures`, `last_challenge_kind`, `paused_until`, `probe_due_at`, `success_ewma`, `cost_per_success_usd`, `max_concurrency` (≤ the host's) |
| claim (§ 7.3 step 1) | picks a `(host, lane)` where both rows pass their gates and items are queued; step 2 is unchanged |
| claim (§ 7.3 step 3) | also reserves budget for the rung's estimate (T7 § 8.2 reserve-then-settle) in the same transaction |
| capability leases | acquired after the claim commits, before I/O: egress, session or account, render slot. If none is free, the item returns to `queued` with `not_before` and outcome `capability-unavailable` |
| fenced result write (§ 7.3) | also writes the `host_lane` update and settles usage |
| account pool (§ 7.4) | rows move to Social (§ 4); the `(account, method)` bucket key stays on the item, and the claim asks Social's lease contract |
| provider jobs (§ 7.4) | unchanged mechanics; the runner moves to Social |
| outcomes (§ 2.7) | `challenge` gains a `kind` (`js-interstitial` · `captcha:{recaptcha,hcaptcha,turnstile,geetest,friction,other}` · `waiting-room` · `login-wall`); new `capability-unavailable`, `login-required`, `session-expired`, `solver-failed`, `rung-ceiling`, `human-pending` |
| run steps (§ 2.6) | `runs.steps` lists the plan's steps with counts and a histogram of rungs used |

- ListingShelf's `AccessBlocked` merges a challenge with a 403 (`HtmlListingBroker.cs:110-111`, `CompletionReason.cs:27-28`). The ladder needs them apart: a challenge may yield to render, a 403 from CloudFront to another egress.

---

## 2 · Capability catalog

Prices were read on vendor pages on 2026-10-26 (§ 7). Home "Social" means a `wow-two-sdk-beta.social` package; until that repo exists, the code is built inline in Harvest (§ 4.4).

| Capability | Contract | State · secrets | Cost | Home | Failure outcomes |
|---|---|---|---|---|---|
| `egress.direct` | the host's own IP through core `Http/Safety` | none | $0 | core transport; policy in Harvest | `blocked`, `rate-limited`, `challenge` |
| `egress.datacenter` | `LeaseEgress(pool, geo, stickiness)` → endpoint, session key, credentials | vendor credentials (sealed); lease rows; health per `(IP, host)` | ~$0.90–1.80 per IP-month (Bright Data per-IP tables, mapping U) | Social `Social.Egress` | `egress-unavailable`, `proxy-auth-failed`, `blocked` (IP-scoped) |
| `egress.residential` | same; `rotating` (new IP per request) or `sticky` (session key; vendor time-to-live 30 min to 7 days) | as above, plus bytes per lease | $2–8/GB list; GeoNode $0.30–0.88/GB | Social | as above, plus `quota-exhausted` |
| `egress.mobile` | same, on mobile networks | as above | per GB, above residential (U: not priced on the pages read) | Social | as above |
| `egress.static` ("IP server") | a fixed proxy on a VPS we run, in Uzbekistan when geo matters | the VPS, its proxy ACL and credentials | ~$25–30 per IP-month in Tashkent (U: exchange rate) | Social (config, health); the VPS is operations | `egress-down`, `blocked` (the whole IP) |
| `egress.unlocker` | one request through a vendor that adds egress, fingerprint, render and solving | vendor key | $1.30–1.50 per 1,000 (Bright Data); $0.13–16 per 1,000 by site tier (Zyte) | Social | `provider-failed`, `budget-exceeded` |
| `session.anonymous` | a cookie jar per run (W6), or a warm jar per host reused for hours | cookies, sealed at rest with a short time-to-live | $0 | Social `Social.Sessions` | `waiting-room`, `session-expired` |
| `session.account` | `LeaseAccount(pool, purpose)` → credentials or a session blob, its pinned egress, per-method buckets | accounts, sealed sessions, leases, the T7 § 7.4 state machine | one SIM or one site sign-up per account; human provisioning | Social `Social.Accounts` | `login-required`, `session_lost`, `limited`, `frozen`, `full`, `capability-unavailable` |
| `session.connection` | resolves a consumer-owned connection ref (T4-4) | the consumer's tokens and cookies, in Social custody | $0 | Social | `connection-invalid` |
| `render` | `Render(url, egress, sessionState, profile, budget)` → DOM, fetched JSON, new session state | nothing at rest; secrets per call, in transit only | 3–10 s and 50–150 MB per page (U, T3 § 2.4) | Social `Social.Browser` and its image | `render-timeout`, `render-crashed`, `challenge` |
| `profile` | a named, coherent header set: `bot` (identifying UA and bot page, W14) or `browser:{name}` (UA, client hints, `Accept-Language`, header order) | data only | $0 | Social catalog; the adapter picks | `challenge` (profile rejected) |
| `challenge.detect` | `IChallengeDetector` per adapter over a generic one → `challenge{kind}` | detector version, recorded samples | $0 | Harvest (grown from `HtmlListingBroker.cs:323-329`) | produces outcomes |
| `challenge.solve` | `Solve(kind, siteKey, pageUrl, egress?, profile)` → token | vendor key (sealed), solve ledger | $0.30–3 per 1,000 solves | Social `Social.Solvers` | `solver-failed`, `solver-timeout`, `token-rejected` |
| `challenge.human` | a review task: an operator signs in or passes the check, then imports cookies or a storage state, or types a code | task row; the imported session, sealed | operator minutes | Harvest console + Social session store | `human-pending` (item parked), `human-expired` |
| `pacing` | gates on `host_state`, `host_lane`, `(account, method)` buckets, the quota ledger, windows | rows | $0 | Harvest (host, lane, window); Social (account buckets, provider-account quotas) | `rate-limited`, `window-closed`, `quota-exhausted` |
| `provider.run` | `Submit` → `Poll` → `Collect`, with `provider_run_id` stored so a restart resumes (T7 § 7.4) | vendor tokens, run ledger | $1–13 per 1,000 results (T2 § 3.2) | Social `Social.Providers` | `provider-failed`, `quota-exhausted`, `budget-exceeded` |
| `ai` | the T6 cascade behind gates G1–G5 | as T6 | $0.008–11.3 per 1,000 posts (T6 § 5) | Harvest, over core `Ai` | `extraction-skipped` |

### 2.1 Egress

- **Geo** is an attribute of every egress lease (`UZ` · `any` · country list), not a capability of its own.
- **Sticky vs rotating.** Rotating spreads load and suits single-request steps (OLX `contact`). Sticky keeps one identity across a session: a warm cookie jar, a login, an account. Sticky keys bind to a run, a host or an account (`bound_to`).
- **IP-scoped blocks.** A `blocked` on one sticky IP marks that `(IP, host)` pair bad in Social's health ledger and retries on a fresh session before it counts toward a lane promotion; one bad exit is not a verdict on the host.
- **The "IP server".** A static exit we own, for egress tied to an identity (each Telegram account pinned to one IP) or to geo (a Uzbek address with Tas-IX peering). It runs outside any private network, and its proxy ACL denies private ranges (§ 3.5).

### 2.2 Sessions

- `anonymous`: a run-scoped jar (iticket's waiting room, T3 § 3) or a warm jar per host that survives across runs for a few hours; reuse is the cheapest captcha avoidance.
- `account`: an account Harvest operates — a site login, a Telegram MTProto session, a platform token. Pools, leases and states are Social's. Login runs in `render` with the account's pinned egress. A 2FA or OTP code goes through the console, as T1 § 5.2 already requires for SIMs.
- `connection`: an account a consumer owns, valid only in that consumer's private container, never pooled (T4-4, T7 § 9.3). Ocharo Sourcing's signed-in RFQ inbox fits here.
- This reverses T7-P17 and T8-15 (no signed-in browsing in v1): the developer names sign-in as a capability a source may need.

### 2.3 Render and profiles

- Render binds egress, session and profile inside one browser context. That binding is why it sits beside them in Social (§ 4.3).
- `profile` covers headers only. TLS and HTTP/2 fingerprints of .NET's `HttpClient` differ from Chrome's whatever the headers say (U, not measured). A host that fingerprints TLS needs the render rung.
- One profile per egress session. A coherent identity — UA, client hints and language that agree, kept stable for a session — is the point; Haven's three Chrome versions on one host (§ 1.1) were the opposite.

### 2.4 Captcha: avoid, detect, hand over, solve

| Order | Mechanism | Lives in |
|---|---|---|
| 1 avoid | pacing (adaptive delay, `Retry-After`), warm session reuse, sticky egress, a coherent profile, night windows | Harvest policy over Social providers |
| 2 detect | a challenge is an outcome with a kind, never a parse failure; adapters add their own detectors (OLX friction `challenge.type ≠ "blank"`, `OlxUzStaticContentPhoneExtractionHandler.cs:177-181`) | Harvest |
| 3 escalate | the lane climbs the ladder: new egress, render, unlocker (§ 3.3) | Harvest |
| 4 solve | a third-party solver when the step allows it and the cap holds; tokens are often bound to the exit IP and UA, so the solve passes the lease's egress (U per vendor) | Social `Social.Solvers` |
| 5 human | a review task; the operator's session is imported and reused (§ 2.2) | Harvest console |

- The be sdk's `Web/Captcha` verifies tokens on our own forms (Turnstile, hCaptcha, reCAPTCHA; `be/Web/Captcha/captcha.md`). It is inbound and unrelated; the outbound package is named `Solvers` to avoid the clash.

### 2.5 Account-pool leases

- T1 § 5 and T7 § 7.4 rules stay: one holder per auth key (`AUTH_KEY_DUPLICATED`), heartbeat every 10–15 s, sticky source assignment, a `(account, method)` token bucket, `FLOOD_WAIT_X` moves items rather than failing them, provisioning by a human.
- New: each account is pinned to one egress (`egress.static`, or residential UZ with a multi-day sticky session). More accounts is the scale path; rotating an account's IP is not (T1-P5).
- Account steps have no rung ladder. Their escalation is "another account that already holds the membership", or an operator.

---

## 3 · Broker contract and resolution

### 3.1 How an adapter declares steps

```csharp
// Harvest.Module — adapter side
public interface ISourceAdapter
{
    string Family { get; }                                  // "listing", "structured", "telegram", …
    AdapterDescriptor Describe(SourceConfig source);        // steps, plans, defaults
}

public sealed record AdapterDescriptor(
    IReadOnlyList<StepDescriptor> Steps,
    IReadOnlyDictionary<string, string[]> Plans);           // "capture" → ["enumerate","detail","contact","media","extract"]

public sealed record StepDescriptor(
    string Key, StepRole Role, Requirements Requires,
    string Lane = "default", bool Optional = false);

public interface IStepBroker
{
    string StepKey { get; }
    Task<StepResult> ExecuteAsync(StepItem item, IStepContext context, CancellationToken ct);
}

public interface IStepContext
{
    ResolvedPlan Plan { get; }              // rung, egress lease, session lease, profile
    HttpClient Http { get; }                // bound to the plan's egress, jar and profile
    IBrowserRenderer? Browser { get; }      // when the rung renders
    ISessionHandle? Session { get; }        // account or connection lease
    ISolverHandle? Solver { get; }          // when the rung may solve; each call reserves budget
    IProviderRunHandle? Provider { get; }
    void Observe(Signal signal);            // challenge kind, status, bytes, latency → ladder and usage
}

// Social.Abstractions — the shared vocabulary
public sealed record Requirements(
    EgressNeed Egress, SessionNeed Session, RenderNeed Render, string Profile,
    ChallengePolicy Challenge, IReadOnlyList<string> Ladder, string Floor, string Ceiling);
```

- `StepResult` carries the T7 three-level outcome, captures, next items (step key and target), and usage (requests, bytes, solves, estimated USD).
- ListingShelf maps one-to-one: `DiscoverAsync` → the `enumerate` broker, `CaptureAsync` → `detail`, `IsPhotoUrl`/`ThumbnailUrl` → `media` helpers, `ValidateSourceUri` → the source's scope policy, `ListingPageClient` → `IStepContext.Http` on rung `R0`.

### 3.2 The resolver at claim

1. **Plan** — frozen at queue time from adapter, source, pipeline and step layers (§ 1.4).
2. **Rung** — `host_lane.rung`, clamped to `[floor, ceiling]`. When `probe_due_at` has passed, one item tries the next lower rung (§ 3.3).
3. **Budget** — the rung's estimate is reserved against every cap (T7 § 8.2 plus the step cap). If it does not fit, the cheapest ladder rung at or above the floor that fits is used; failing that, outcome `budget-exceeded` and the item goes `blocked`.
4. **Leases** — through Social's `ICapabilityLeases`: egress (sticky key = run, host or account), session or account, render slot. In-process with `Social.Module`, or over HTTP with `Social.Client` (§ 4.4).
5. **Execute** — the broker runs; `Observe` records signals.
6. **Settle** — usage settles, leases release or stay bound to the run; `host_lane` updates in the fenced result write.

### 3.3 The escalation ladder

| Rung | Egress | Session | Render | Profile | Solve | Cost unit |
|---|---|---|---|---|---|---|
| `R0` direct | direct | per step | no | `bot` | no | $0 |
| `R1` direct-browser | direct | per step | no | `browser` | no | $0 |
| `R2` datacenter | datacenter, rotating | per step | no | `browser` | no | IP-month |
| `R3` residential | residential, rotating | per step | no | `browser` | no | $/GB |
| `R4` residential-sticky | residential, sticky | warm jar | no | `browser` | no | $/GB |
| `R5` render | residential, sticky | warm jar | yes | the browser's own | no | $/GB + seconds |
| `R6` unlocker | vendor | vendor | vendor | vendor | vendor | $/1,000 requests |
| `R7` solver | as `R4` or `R5` | warm jar | as `R5` | as `R5` | yes | $/1,000 solves |
| `R8` human | as `R5` | operator's | as `R5` | as `R5` | operator | minutes |

- An adapter declares its subset (Afisha `[R0, R2, R3]`; OLX contact `[R3, R4, R7]`). Geo is an attribute of `R2`–`R5`.
- **Promote** one rung after 3 consecutive `challenge` or `blocked` results at the current rung (T3's "alert after 3" count), or straight to the first render rung on `render-required`.
- **Never promote on `rate-limited`.** Rate limits pace (`Retry-After`, cap 15 min, T3); promoting on throttles is how proxy budgets burn.
- **IP-scoped first.** A `blocked` on a sticky exit retries on a fresh egress session before it counts (§ 2.1).
- **Demote** with a probe: after 24 h at a rung, one item runs one rung lower; 3 probe successes in a row step down. Cost falls back when a block lifts.
- **Ceiling.** A lane that fails at its ceiling pauses with T7's backoff (15 min → 1 h → 6 h), alerts, and reports `rung-ceiling`; links stay "unchecked" (T7 § 2.7 rule).
- **Cost caps.** Each rung keeps a moving `cost_per_success_usd`; a rung above its `maxUsdPerSuccess` is skipped. The step has a monthly `maxUsd`, and the solver has `maxUsdPer1k` and `maxSolvesPerDay`. The console shows rung, history and cost per success per lane.
- Thresholds (3, 24 h, 3) are placeholders, to be tuned on observed outcomes (T9-7).

### 3.4 Budgets

- T7 § 8's ledger gains meters: `egress_bytes` (priced per pool), `egress_ip_months`, `solves`, `unlocker_requests`, `render_seconds` (informational in v1).
- Social reports usage per lease; Harvest attributes it to run, item, pipeline, tenant and subscription.
- Caps per provider account (one proxy or solver account shared by every Social caller) live in Social; caps per pipeline, tenant, step and subscription live in Harvest. A hard stop on either side stops the paid rung, and the free rungs keep running.

### 3.5 Core and transport

- `be/Http/Safety` disables proxies and cookies (`SafeOutboundHttpClientBuilderExtensions.cs:46-48`) and validates the destination at connect time (`:51-54`, `:64-80`). Behind a proxy the socket connects to the proxy, so that check would see the proxy's address, not the target's.
- **Core ask:** an egress option on `AddSafeOutboundHttp` that pre-resolves and validates the target before sending it to a third-party proxy. The vendor's exit cannot reach our private ranges, so the DNS-rebinding window is accepted there. Direct egress keeps the connect-time check, and a self-hosted IP server must deny private ranges in its own ACL.
- `SocketsHttpHandler` takes one proxy per handler, so the client factory keeps one handler per egress lease, keyed by endpoint and session key, disposed when the lease ends. A `CookieContainer` per session lease extends T8's cookie option (W6).
- `be/Http/Resilience` (3 retries, 2 s, circuit breaker; `HttpResilienceOptions.cs:9-24`) stays off fetch clients. Retries and breaking belong to the ladder and `host_state`; generic retries replay a blocked request from the same IP.
- Sealing: `be/Foundation/Security` (`SealService`, `EnvironmentMasterKeyBroker`) seals proxy credentials, session blobs and imported cookies, as T8 § 5.2 does for Telegram sessions.

---

## 4 · The cut under answer 1

### 4.1 Reading the answer

- Social is platform-facing: one integration per platform for read, post, trends and monitoring of the organization's own accounts, plus the shared integration libraries ("for example ip servers").
- Harvest is the mass engine "on top of those libs": pipelines and steps at volume, posts, dedup, extraction, subscriptions, trends learned from harvested posts, mass actions.
- Two splits follow. Trends: platform trend endpoints and own-account monitoring are Social's; trends learned over the pool are Harvest's. Monitoring: watching our own accounts and mentions is Social's; watching third-party sources at volume is a Harvest pipeline.

### 4.2 T8 § 1.4 redrawn

| Capability | T8 home | T9 home | Why |
|---|---|---|---|
| Telegram readers: `t.me/s` parser, MTProto client | Harvest | Social `Social.Telegram` (read side, beside the bot edge) | a social platform integration; Harvest's Telegram adapter declares steps over it |
| Telegram MTProto account pool: sessions, leases, flood buckets, joins | Harvest | Social `Social.Accounts` | accounts are custody; one pool can later serve mass actions (joins, posting); `IAccountLeases` in the contract |
| intake bots (Telegram bot, WhatsApp number) | Harvest | Harvest (`intake` family) over Social's edges | consent, `forward_origin` and container attribution stay Harvest's; the transport moves under Social's edges |
| RSS and ICS readers, link cards, sitemaps, JSON-LD, robots | Harvest | Harvest `Module/Web/` | not social; one consumer (T8-7) |
| non-social site adapters: OLX, Domtut, Afisha, iticket, mstar, voyage | Harvest | Harvest | § 4.3 |
| licensed-provider runners (Apify, Bright Data) and their accounts | Harvest | Social `Social.Providers` | a shared integration library: Social's trends use the same actors (PoseCoach's TikTok and Reels hashtag trends, T4 § 7); one vendor account, one quota |
| egress: proxy pools, IP servers, geo, sticky sessions | none (T3 W8: direct only) | Social `Social.Egress` | answer 1's own example |
| sessions: anonymous jars, site accounts, consumer connections | nowhere in v1; an `IConnectionResolver` port | Social `Social.Sessions` / `Social.Accounts` | custody; answer 2 names sign-in |
| browser render and profiles | Harvest (`Harvest.Render`, image `harvest-render`) | Social `Social.Browser`, image `social-browser` | § 4.4 |
| captcha solvers, unlockers | forbidden | Social `Social.Solvers`, `Social.Egress` (unlocker) | vendor integrations with secrets |
| capability vocabulary: requirement types, rung names, lease and usage records | none | `Social.Abstractions` | one vocabulary for every caller |
| step model, resolver policy, ladder learning (`host_lane`), budgets per pipeline and tenant | none | Harvest | engine decisions |
| publish with receipts, own metrics, verification, connected accounts, token lifecycle | Social | Social | unchanged |
| platform trend endpoints, own-account monitoring | none | Social | answer 1 |
| trends learning over harvested posts; mass actions | none | Harvest | answer 1 |
| platform API transport (Graph, X v2, Google) | Social edges | Social edges | unchanged |
| authenticated reads (IG business discovery, PPCA, Threads, X, YouTube) | Harvest adapters over Social edges | same | unchanged |
| Telegram and WhatsApp send (notify, OTP) | core `Comms` | core `Comms` | § 4.6 |
| sign-in (OAuth, Telegram login, `initData`) | Identity | Identity | unchanged |
| approvals, scheduling, campaigns | the product | the product | unchanged |

- T8's rule "a client lives in Social only if a second domain calls it" gives way to answer 1. Every platform client lives in Social; Harvest keeps only what is not about a platform.

### 4.3 Where the non-social site brokers live

| Option | For | Against |
|---|---|---|
| a · Harvest adapters | the only consumer; their steps carry Harvest's semantics (frontier, gone rules, `lastmod_trust`, JSON-LD readers, `wow2.post.v1`); they consume Social's capability providers | none found |
| b · Social integrations | sits beside the egress and session code they use | Social's charter is social media; OLX, Afisha and mstar have no social account, post nothing and serve no Social feature |
| c · a third repo (`sites`) | isolates fragile scrapers | duplicates Harvest's step contract; a third release line; one consumer |

**Pick: a.** Exceptions:

- a write client for a marketplace (Haven's planned OLX cross-posts, `hv/engineering/planning/backlog.md:179-181`) goes to Social when it is built, as posting; the read adapter stays in Harvest.
- a site adapter a second product uses without Harvest's store becomes a Harvest edge (`Harvest.Web`, T8-7).

### 4.4 Render, the chain and the first slice

**Render** goes to Social as the extension `Social.Browser` (Playwright host and its RPC client) with image `social-browser`. It binds egress, session and profile in one context, and posting without an API may need it.

- Each call receives the lease's egress credentials and the session's storage state, and returns the new state. It persists nothing and holds no database credential (T8 § 5.3, amended: no secret at rest instead of no secret).
- A Harvest bundle that renders includes the `social-browser` container.

**Chain.** Added edges, all pointing left:

```text
social    Social.Abstractions  → Be.Abstractions, Identity.Abstractions   + capability vocabulary, lease contracts
          Social.Egress        → Social.Abstractions, Be                  edge: handler pool per lease, vendor dialects
          Social.Solvers       → Social.Abstractions, Be                  edge
          Social.Providers     → Social.Abstractions, Be                  edge: Apify, Bright Data runners
          Social.Telegram      → Social.Abstractions, Be                  + WTelegramClient, t.me/s reader
          Social.Browser       → Social.Abstractions, Be                  extension: Playwright
          Social.Module        → Social.Abstractions, the edges, Be       accounts, sessions, leases, egress health, quotas
harvest   Harvest.Module       → Harvest.Abstractions, Social.Abstractions, Be        (new edge)
          Harvest.Telegram     → removed: the adapter needs only Social's contract and joins Module
          Harvest.Render       → removed: Social.Browser
          service Harvest.Api  → Harvest.Module, .Files, .Social, Social.Module | Social.Client, Identity.Auth, Files.Client
```

- `Harvest.Abstractions` stays free of Social; capability types appear only in `Harvest.Module`, where adapters live.
- Social references nothing to its right. When Social's monitoring wants third-party volume, a product subscribes to Harvest; Social never calls Harvest.
- Forms: `Harvest.Api` hosts `Social.Module` in-process by default (schema `social` in Harvest's database, `Social:Mode = InProcess | Remote`). A Form 3 instance may point at a shared Social service when another product shares the same accounts. One account lives in one store only.

**First slice (T8 § 7).** Social's packages do not precede it. Answer 1's libraries are built inline in Harvest and extracted at the +0.1, per the standing rule.

| T8 § 7 step | Change |
|---|---|
| 2 · SQL `001` | adds `host_lane`, `sources.capability_policy`, `pipelines.step_overrides`, usage meters |
| 3 · fetch lane | becomes the inline capability layer `Module/Capabilities/`: direct egress over `Http/Safety`, anonymous jars, `bot` and `browser` profiles, the generic challenge detector, the ladder engine with `R0`–`R1` live and later rungs declared but `unavailable` |
| 4 · engine lane | work items carry `step` and `lane`; claims are by `(host, lane)` |
| 5 · adapter lane | adapters declare steps; OLX and Domtut port `enumerate`, `detail` and `media`, with `contact` declared and disabled |
| gate | adds a ladder fixture test: a fake host challenges 3 times, the lane climbs to a fake proxy rung from `Harvest.Testing`, and the probe brings it back. Afisha joins mstar.uz and voyage.uz (§ 5.1) |
| out of the slice | real proxies, accounts, render, solvers and provider runners: slice 2 (OLX `contact` on residential, the Telegram pool, Apify) |

- Social is created at the first of T8 § 1.6's triggers or Harvest's first paid capability, whichever comes first. The inline `Capabilities/` code moves into Social at the next +0.1. Its interfaces carry Social's shape from day one; the namespace changes once, inside Harvest only.

### 4.5 Mass actions

- v1 reads, plus bulk operations over posts: checks, re-extraction, re-delivery, export.
- Mass writes (bulk posting, joins, messages) would use Social's publish brokers and account pools. They are a later scope, and they strengthen the case for the pool living in Social (T9-20).

### 4.6 Telegram and WhatsApp send

- **Unchanged: core `Comms`.** Identity (left of Social) sends Telegram OTPs (`be/Identity/Otp/Telegram/TelegramOtpDeliveryHandler.cs`), and Wheelhouse and Feedbacks alerts must not restore Social (T8-3).
- Answer 1's "posting stuff" is channel and group posting (Marketing O1, Haven H1, WhatsApp templates O7). That is Social's, over the same `Telegram.Bot` client and the existing `be/Comms/WhatsApp/Meta` sender.

### 4.7 Recipes in public repos

- Domain repos are created public (`conventions/development/repo/structure/domain-structure.md:191`). Generic providers (a proxy pool client, a solver client, a browser host) are fine in public.
- A per-site recipe is not: the OLX friction flow (`OlxUzStaticContentPhoneExtractionHandler.cs:19-25`), header sets or private endpoints in a public repo under WoW2's name invite the site to patch them and document the bypass.
- Pick: recipes in a private package or an operator-supplied config bound by name; T8-5's strip pass covers research text, not code (T9-19).

---

## 5 · The posture change

### 5.1 Picks that change

| # | Point or section | Was | Now |
|---|---|---|---|
| 1 | P3 | honour each source's terms | not honoured (answered 2026-10-26) |
| 2 | P4 · S1 | Route B behind counsel; providers attest no accounts and no bypass | enabled; attestation dropped; `posture` still recorded per capture |
| 3 | T1-P1 · T6-6 · T6-7 · P15 | Telegram `ai_allowed = no`; Meta-route, X, YouTube `unreviewed` | `yes` on every route, embeddings included |
| 4 | T1-P5 · T7-P18 | sticky, no failover, no IP rotation, because a limit is never bypassed | sticky stays, for account health; each account pinned to one egress; more accounts is the scale path |
| 5 | T1-P6 · P5 | a human approves every join | public groups joined automatically within a per-account daily budget; a human for `request_needed` invites |
| 6 | T1-P7 · P6 | no linked-device WhatsApp sidecar | allowed later as a `session.account` route; v1 unchanged, on build cost |
| 7 | T1-P13 | check API Terms §3.3 (sponsored messages) | dropped |
| 8 | W1 · P7 | ask Afisha; `restricted` until granted | `open`; Afisha joins slice 1 |
| 9 | W2 · T4-12 | iticket deferred to render after a terms check | its own JSON endpoints first, found while authoring and contract-tested; render as fallback |
| 10 | W3 · W4 | `robots.txt` binds every fetch, submitted URLs included | `robots_policy` per source (T9-17) |
| 11 | W5 · G3 | `ai-input=no` blocks E, S, L | recorded, not enforced by default |
| 12 | W8 | direct egress only; no pools, no rotation | the egress capability (§ 2.1) |
| 13 | W9 | RSSHub on unauthenticated routes only | cookie routes allowed through sessions; still off in P1 |
| 14 | W14 | an identifying UA on every request | a profile per source (T9-16) |
| 15 | T3 § 2.4 | render: no stealth plugins, no challenge solving | browser profiles and the ladder's solve rungs allowed |
| 16 | T3 § 3 | `challenge` stops the host; textileexpo.uz stays hand-typed | the ladder applies (render clears JS interstitials); hand entry is the last fallback |
| 17 | T2 § 3.3 | "clearly prohibited": logged-in scraping, bypassing CAPTCHA, bot walls or IP blocks | capabilities behind switches; residual exposure in § 5.3 |
| 18 | T2 § 4 | Harvest never runs Route C on Instagram, Facebook, TikTok, X | allowed as a last route; Route B stays first on maintenance cost |
| 19 | T7 § 11 · T5 § 2.5 | `route.enabled = false` for Route B; `ai_allowed = false` for Telegram, WhatsApp, `consent_basis = none`; Afisha `restricted` | `true`; `true`; `open` |
| 20 | T7 § 9.2 · T8 § 5.2 | `pool_shareable = false` for Route B and Meta API until counsel | `true` for Route B and own fetch; Meta official routes per T9-5 |
| 21 | T7-P17 · T8-15 | no signed-in browsing in v1 | sessions capability (§ 2.2) |
| 22 | T8 § 5.3 · T8-10 | render holds no secret and no cookie jar | per-call session and egress credentials in transit, nothing at rest, no database credential; moves to Social |
| 23 | T8 § 5.5 | a self-hoster brings "a posture decision"; counsel reads are the operator's | the operator sets switches; permissive defaults ship |
| 24 | T4-13 | no phone reveal in v1 | the OLX `contact` step (T9-15) |

- Unchanged: T1-P9 (intake consent: personal-data law and deletion requests, not platform terms), S11 (separate Meta apps, now for ban isolation), S12 and T6-15 (personal data), S5 (check cadence), W13 (politeness, now an avoidance capability).

### 5.2 The switches stay

**Pick: keep every posture field, with permissive defaults.** The columns already exist in T5's `001`. A reversal — a takedown letter, a ban wave, a consumer contract, the jurisdiction P8 picks — becomes an `UPDATE`, not a migration (T5 § 2.5 rule).

| Field | Lives on | New default | Flipped when |
|---|---|---|---|
| `permission` | source, `host_policies` | `open` everywhere | a takedown: `denied` stops scheduling; `purge_on_deny` scrubs per retention |
| `ai_allowed` | source | `true` | a platform action or a consumer's contract |
| `pool_shareable` | route | `true`, except Meta official routes (T9-5) | a platform claim over pooled data |
| `route.enabled` | route | `true` | a ban or a provider failure |
| `posture` | source, capture | required; records the route class, gates nothing | evidence when someone asks how a post was read |
| `robots_policy` | source | `obey` for link intake and the long tail; an operator may set `ignore` | per source |
| `content_signals` | host | `record` | `enforce` on request |
| `platform.enabled` (new) | platform | `true` | one field stops every route of a platform (all Meta, all Telegram) |
| `capabilities.ceiling` | source, step | per adapter | a cost spike or a ban lowers it |

### 5.3 What still binds

- **Official API keys we hold.** YouTube's 30-day refresh, X's compliance events and Meta Platform Terms §3.c on sharing are enforced by revoking the key or the app, which the platform does on its own. Keeping `retention_class` and `pool_shareable = false` on official routes costs one purge job and one flag. Scraped and provider routes ignore them (T9-5, a developer fork).
- **Personal data.** Uzbekistan's personal-data law (T2 S12, T5-12, unread) is law, not terms; T9 changes nothing there.
- **Residual legal exposure, recorded once.** In Reddit v. Perplexity (S.D.N.Y., 2026-07-31), a DMCA anti-circumvention claim over bypassing bot detection survived a motion to dismiss (T2 § 3.3; pleadings stage, US). The switches keep a stop to one field.
- **Platform enforcement is the working constraint**: account bans, IP blocks, app revocation. Ladders, account health, separate apps (S11) and the kill switch handle it.

---

## 6 · Worked mappings

### 6.1 Haven's OLX (filtered pipeline "Tashkent rentals", captcha)

Evidence: ListingShelf reads OLX direct from the developer's Mac today. Haven's Hetzner VPS needed residential proxies against CloudFront 403s on detail pages (`FetchDetailsNode.cs:12-13`). Its phone step posted to `friction.olxgroup.com/challenge`, then `/exchange`, then `www.olx.uz/api/v1/offers/{id}/limited-phones/` with the friction token, using a fresh device id per call (`OlxUzStaticContentPhoneExtractionHandler.cs:19-21,150-151,210-217`). Any challenge type but `blank` was a captcha (`:177-181`).

| Step | Calls | Floor | Ladder → ceiling | Lane | Outcomes it learns from |
|---|---|---|---|---|---|
| `enumerate` | list pages (`DiscoverAsync`); search pages render-only (`HtmlListingBroker.cs:80-81`) | `R0`, anonymous jar, `browser` profile | `R0` → `R3` → `R5` | `olx.uz` | `repeated-page`, `unrecognized` spikes, `blocked` |
| `detail` | ad page (`CaptureAsync`) | `R0` | `R0` → `R3` → `R4` → `R5` | `olx.uz` | CloudFront 403 promotes; `gone` per T5 |
| `contact` | friction challenge → exchange → `limited-phones` | `R3` rotating (Haven never ran it direct), one `browser` profile matching the client hints | `R3` (fresh IP and device id each call) → `R4` → `R7` solver, off by default (friction's widget kind unknown, U) → ceiling `R4` | `olx.uz#contact` | `challenge{friction}` retries later on a new exit, as Haven did; `phone_not_in_response` = none listed |
| `media` | `olxcdn.com` photos, ≤ 12, ≤ 5 MiB (`IsPhotoUrl`) | `R0` (Haven ran images without a proxy) | `R0` → `R3` | `olxcdn.com` | |
| `extract` | D and R: price `у.е.` (97%), phones from text | — | — | — | AI off for Haven (T4-8) |
| `check` | detail fetch, gone rules | as `detail` | as `detail` | `olx.uz` | OLX removal signal unconfirmed (T4 § 5) |

- Plans: `capture` every 15 minutes (Haven's `*/15`) runs `enumerate` → `detail` → `contact` → `media` → `extract`; `check` runs daily. `contact` runs once per link, not on every refresh.
- Concurrency: the `contact` lane may run several in flight because each call leaves from a different exit (Haven ran 10 per batch of 50 with 2 s between batches, `hvb/Haven.Channels.Supply/appsettings.json:174-178`). The host row still caps total load on `olx.uz`.
- Cost, an estimate with assumptions marked: three JSON calls of ≤ 20 KB per listing (U) cost ≤ $0.06 per 1,000 at $3/GB. Detail pages through residential at 0.5 MB each (U) cost ~$1.50 per 1,000. At ~1,100 listings a day (Haven, 2026-03-04, T4 § 5): about $2 a month for `contact`, against ~$50 for `detail` if it ever needs residential, and $0 while direct holds. That gap is why `contact` gets its own lane and floor.

### 6.2 Telegram channels and groups

Channels, route W (`t.me/s`, no account):

| Step | Calls | Floor | Ladder → ceiling | Lane |
|---|---|---|---|---|
| `enumerate` | `/s/{ch}` newest page every ≥ 5 min; `?before={id}` backfill, 20 per page | `R0`, no session | `R0` → `R2` → `R3` | `t.me` |
| `media` | CDN photo URLs; short mp4 with a `token` (fetch at capture, T1 § 5.7) | `R0` | `R0` → `R3` | the CDN host (U) |
| `metrics` | views and reactions from the same page | as `enumerate` | — | `t.me` |
| `check` | `/s/{ch}` availability first, then `/{ch}/{id}?embed=1` "Post not found" | `R0` | `R0` → `R2` | `t.me#check` |
| `extract` | D and R; E, S, L allowed now (`ai_allowed = yes`) | — | — | — |

- `preview_unavailable` switches the source to route M. That is a route ladder over alternative step plans (T1 § 5.1), separate from the capability ladder.

Groups, comments and private chats, route M (MTProto, an account):

| Step | Calls | Requires | Bucket |
|---|---|---|---|
| `account-op` resolve | `contacts.resolveUsername`, `messages.checkChatInvite` | `session.account(pool = tg-uz)`, the account's pinned egress | `acct:{id}/resolve` |
| `account-op` join | `channels.joinChannel`, `messages.importChatInvite` | as above, plus a join budget per account per day | `acct:{id}/join` |
| `enumerate` / `detail` | `messages.getHistory` (≤ 100 per call), `channels.getMessages` | as above | `acct:{id}/getHistory` |
| `thread` | `messages.getDiscussionMessage` + replies | as above | `acct:{id}/getReplies` |
| `media` | `upload.getFile` | as above | `acct:{id}/getFile` (`FLOOD_PREMIUM_WAIT`) |
| `check` | `channels.getMessages(ids)` → `messageEmpty` | as above, membership first | `acct:{id}/getMessages` |

- No rung ladder: `FLOOD_WAIT_X` sets the bucket's `not_before` exactly; `INVITE_REQUEST_SENT` parks the join for an admin or a human; `CHANNELS_TOO_MUCH` marks the account `full`.
- Egress: one static UZ IP server per 1–2 accounts, or residential UZ with a multi-day sticky session (IPRoyal lists up to 7 days). How sensitive Telegram is to session IP changes or shared exits is untested (U).
- Cost: SIMs and an IP server at ~$25–30 a month; no API fee.

### 6.3 Instagram public profiles (Ocharo brands, Haven realtors)

Route B, the provider runner:

| Step | Calls | Requires | Notes |
|---|---|---|---|
| `provider-job` submit | `apify/instagram-post-scraper` with `usernames[]`, `onlyPostsNewerThan` | `provider.run(apify)` from `Social.Providers` | bucket `prov:apify` |
| `provider-job` poll | run status by stored `provider_run_id` | as above | a restart resumes polling and never pays twice |
| `provider-job` collect | dataset items → one capture per post | as above | `usageTotalUsd` settles billed cost |
| `media` | Instagram CDN URLs (signed, expiring, U) | `R0` → `R3` | an expired URL re-collects |
| `extract` | D from dataset fields, then R | — | AI allowed |
| `check` | weekly re-scrape of the newest 30 days (S5) | provider | billed per result |

- Route ladder of the source: A (business discovery over `Social.Meta`, a Harvest-owned professional account, $0, business accounts only) → B (above) → C (own render + residential UZ sticky + a signed-in account from a pool; allowed now, highest upkeep and the account's ban risk).
- Cost: $1.00–2.70 per 1,000 results (T2 § 3.2): ~$10–27 for 10k posts a month, plus the Apify plan.

### 6.4 Afisha whole-site (`sweep`)

| Step | Calls | Floor | Ladder → ceiling | Lane |
|---|---|---|---|---|
| `enumerate` | `robots.txt` per `robots_policy` → `/sitemap.xml` index (752 KB) → children whose `lastmod` moved (~3 a day) | `R0`, anonymous jar, `bot` profile | `R0` → `R2` → `R3` | `afisha.uz` |
| `detail` | event pages (SSR, 159 KB, JSON-LD `Event`) | `R0` | as above | `afisha.uz` |
| `media` | posters | `R0` | `R0` → `R3` | the image host (U) |
| `extract` | D: JSON-LD → `wow2.event.v1` mapping; R: price text ("от 50 000 сумов") | — | — | — |
| `check` | absence from a complete enumeration → `suspect` → a direct fetch decides | `R0` | as `detail` | `afisha.uz#check` |

- Schedules from T3: enumerate hourly, sweep weekly, verify daily, inside the night window. One pass is ~159 MB per 1,000 pages and ~33 min at 1 request per 2 s. Cost ~$0.
- Robots disallows `/api/` and `/_next`, which this server-rendered route does not need. With `permission = open`, Afisha moves into slice 1 beside mstar.uz and voyage.uz (P7).

---

## 7 · Build vs wrap

### 7.1 Proxies and IP servers

| Vendor | Types | Price as listed | Sticky | Uzbekistan |
|---|---|---|---|---|
| Bright Data | residential, mobile, ISP, datacenter | residential $4/GB pay-as-you-go (promo; $8 list) → $2.50/GB at 798 GB ($1,999/month); per-IP tables $0.90–1.80 (datacenter or ISP, mapping U) | "extended session control" | yes: 41,130 residential and 1,024 datacenter IPs listed; the header says 10,538 (conflict) |
| Oxylabs | residential, datacenter | $6/GB to 5 GB, $5 to 20 GB, $4 to 125 GB, $2.50 at 1,000+ GB; plans $30–500/month | yes, length not stated | yes: 81,764 IPs on the Uzbekistan page; title "from $8/GB" |
| Decodo (Haven used it) | residential | $4/GB pay-as-you-go; $3.75–2.75/GB (3–100 GB); $2.50–2.00/GB (250–1,000 GB) | ≤ 30 min | not named; the country page answered 404 (U) |
| IPRoyal | residential | $7.35/GB at 1 GB → $1.84/GB at 10 TB+ pay-as-you-go; traffic never expires | ≤ 7 days | not listed; the country page answered 404 (U) |
| GeoNode (Haven's active provider) | residential | $0.88/GB pay-as-you-go at 10 GB → $0.30 at 100 TB; unmetered $1,800–3,800/month | yes, length not stated | not named; "150+ countries" (U) |
| a Tashkent VPS as the IP server (pro-data.tech, ahost.uz) | static datacenter, Tas-IX | pro-data.tech 358,800 UZS/month (2 vCPU, 2 GB, one dedicated IPv4); ahost.uz 395,000 UZS/month (IP not stated) | static | yes, by location |

- Shifter claims 98,708 Uzbek residential IPs (vendor page, not priced here). Uzbek mobile egress (a modem farm on our own UZ SIMs) is possible and untested (U; SIM rules in T1 § 6).
- **Pick: wrap the IPs, build the plumbing.** A residential pool cannot be built. Harvest and Social build the lease client, the handler pool, the health ledger per `(IP, host)`, the usage meters and the ladder.
- Start with one vendor that lists a Uzbek pool (Bright Data or Oxylabs) for `geo = UZ`, keep GeoNode as the cheap rotating pool behind the same `IEgressPool`, and run one Tashkent VPS for egress tied to an identity (T9-13).

### 7.2 Captcha solvers and unlockers

| Service | Method | reCAPTCHA v2 | reCAPTCHA v3 | Turnstile | GeeTest | Image |
|---|---|---|---|---|---|---|
| 2Captcha | humans and AI (the page names both) | $1–2.99 | $1.45 (score ≤ 0.3) – $2.99 | $1.45 | $2.99 | $0.50–1 |
| CapSolver | AI | $0.80 | $1.00 | $1.20 (Cloudflare Challenge $1.20) | $1.20 | $0.40 |
| Anti-Captcha | human workers | $0.95–2 | $1–2 | $2 | $1.80 | $0.50–0.70 |
| CapMonster Cloud | AI, cloud only | $0.60 | $0.90 | $1.30 | $1.20 | $0.30 |

All prices are per 1,000 solves. 2Captcha's page lists no hCaptcha price.

| Unlocker | Price | Billing | Includes |
|---|---|---|---|
| Bright Data Web Unlocker | $1.50 per 1,000 pay-as-you-go; Scale $499/month for 383k, then $1.30 | successful requests only; 5k free a month | egress, fingerprinting, JavaScript rendering, captcha solving |
| Zyte API | $0.13–1.27 per 1,000 HTTP, $1.01–16.08 per 1,000 rendered, pay-as-you-go, by five site tiers | successful responses only | geolocation; the rest by tier |

- Solvers are priced per widget kind; none lists OLX's friction challenge, whose kind is unknown (U). Geo does not apply to solvers, but a token may be bound to the exit IP, so the solve should pass the lease's egress (U per vendor).
- **Pick: never build a solver.** Avoid first (§ 2.4). Put `ICaptchaSolver` in front of two vendors — CapMonster Cloud or CapSolver for common widgets, 2Captcha for odd kinds — off by default, allowed per step under a cap. For HTML pages where render on residential fails, prefer the unlocker rung (`R6`), which bundles the rest. Human hand-over is the last rung (T9-14).

---

## Findings that change the spec

- **§ Concepts gains step, capability, lane and rung.** A pipeline's adapter declares steps; each step states requirements; the runner resolves them per claim. "Source adapter" means an adapter with step brokers, not a single read call.
- **§ Behaviour at sources** already names the capabilities (spec lines 67–71). It gains the ladder rules: avoidance before escalation, rate limits never escalate, a lane's rung is learned and decays, and a block no rung clears within its ceiling and budget stays an outcome.
- **§ Placement.** Capability providers and every platform client live in `wow-two-sdk-beta.social`; Harvest's Form 1 module references `Social.Abstractions` and the host binds `Social.Module` or `Social.Client`. T8's `Harvest.Telegram` and `Harvest.Render` packages and the `harvest-render` image leave Harvest.
- **The Telegram MTProto pool moves to Social** (T8 § 1.4, § 5.4, T8-12 amended). Harvest leases accounts through `IAccountLeases`; custody, sessions and buckets are Social's.
- **Signed-in sources are in scope** (T7-P17, T8-15 reversed): site accounts from pools, consumer connections, logins in the browser, codes through the console.
- **Render carries per-call secrets** (T8 § 5.3 amended): egress credentials and session state travel with each call and nothing persists; the no-database-credential rule stands.
- **`host_state` needs a lane table.** One step can need different egress from the rest of its host (OLX `contact`); a block in that lane must not pause detail pages.
- **Core `Http/Safety` needs an egress option.** It disables proxies today, and its connect-time check cannot see the target behind one; pre-resolving the target for third-party egress is the core ask, beside T8's cookie option.
- **OLX phone reveal returns** (T4-13 reversed). Haven had it working through friction plus residential rotation until the 2026-09-26 rebuild dropped it; phones are text-only today.
- **Posture fields stay, with permissive defaults**, plus a `platform.enabled` kill switch and `robots_policy`; Afisha's `permission` becomes `open`, Telegram's `ai_allowed` `true`, Route B `enabled`.
- **Afisha joins Events' first sources** (P7, W1): the permission gate is gone, and its sitemap delta and JSON-LD need nothing beyond `R0`.
- **Per-site recipes stay out of public repos.** Domain repos are public; generic providers are fine, site bypass recipes go to a private package or operator config.
- **Costs are small where the ladder is narrow.** OLX `contact` on residential is ~$2 a month at Haven's volume; residential detail pages would be ~$50; solvers run $0.30–3 per 1,000. The cap that matters is per lane and rung, not per pipeline only.

---

## Points

- [ ] T9-1 (P20) the capability framework → provisional pick: pipelines as declared step plans; each step a broker with requirements (floor, ladder, ceiling); the resolver picks the rung at claim from learned `host_lane` state, reserves budget and leases capabilities; render is a capability, not a step (§ 1, § 3)
- [ ] T9-2 (P1, T8-1, T8-2) the cut under answer 1 → provisional pick: Social holds every platform client (read, post, trends, own-account monitoring), every capability provider with its secrets (egress, sessions, account pools including Telegram MTProto, browser, solvers, provider runners) and the capability vocabulary; Harvest holds the engine, resolver policy, ladders, budgets and the non-social site adapters (§ 4.2)
- [ ] T9-3 (T8-18) timing → provisional pick: slice 1 builds direct egress, anonymous jars, profiles, the detector and the ladder engine inline behind Social-shaped contracts; Social is created at the first of T8 § 1.6's triggers or Harvest's first paid capability; inline code moves at the next +0.1; the slice gate gains the ladder fixture test and Afisha (§ 4.4)
- [ ] T9-4 (P3) posture switches → provisional pick: keep `permission`, `ai_allowed`, `pool_shareable`, `route.enabled`, `posture`, add `robots_policy`, `content_signals` and `platform.enabled`; permissive defaults; a ban or takedown is one `UPDATE` (§ 5.2)
- [ ] T9-5 official-route obligations (YouTube 30-day refresh, X compliance events, Meta §3.c pool sharing) → provisional pick: honour them on official API routes only, because the platform revokes keys on its own; scraped and provider routes ignore them (§ 5.3)
- [ ] T9-6 step vocabulary → provisional pick: roles `enumerate` · `detail` · `contact` · `media` · `thread` · `check` · `metrics` · `provider-job` · `account-op` · `extract`; T7 work kinds become step plans; optional steps OR-merge across subscribers and bill the pipeline (§ 1.2, § 1.3)
- [ ] T9-7 ladder rules → provisional pick: rungs `R0`–`R8`; promote after 3 consecutive challenges or blocks; rate limits never promote; IP-scoped blocks retry a fresh exit first; demote by a probe after 24 h and 3 successes; ceiling → backoff, alert, `rung-ceiling`; per-rung `maxUsdPerSuccess`; thresholds tuned on observed outcomes (§ 3.3)
- [ ] T9-8 lanes → provisional pick: `host_lane(host_key, lane)` beside `host_state`; a step may declare a lane; the claim checks both rows; the host row still caps total load (§ 1.5)
- [ ] T9-9 non-social site adapters (OLX, Domtut, Afisha, iticket, mstar, voyage) → provisional pick: Harvest; a marketplace write client goes to Social when built; a site adapter a second product needs without the store becomes a Harvest edge (§ 4.3)
- [ ] T9-10 (T8-10, W7) render → provisional pick: `Social.Browser` and image `social-browser`; per-call egress and session state, nothing at rest, no database credential; built inline in Harvest first; still gated on the W7 spike (§ 4.4)
- [ ] T9-11 (T7-P17, T8-15, T4-4) sessions → provisional pick: `anonymous` (run jar or warm host jar, sealed, short time-to-live), `account` (site logins and Telegram from Social's pools), `connection` (consumer-owned, private containers only); login in render; codes and imported cookies through the console (§ 2.2)
- [ ] T9-12 (T8-12, T1-P5, T1-P6, P5) Telegram pool → provisional pick: `Social.Accounts` and `Social.Telegram`; Harvest's adapter over `IAccountLeases`; each account pinned to one egress; public groups joined automatically within a daily budget, a human for `request_needed` invites; `ai_allowed = yes` (§ 2.5, § 6.2)
- [ ] T9-13 (W8) egress vendors → provisional pick: one vendor with a listed Uzbek pool (Bright Data or Oxylabs) plus GeoNode behind one `IEgressPool`; one Tashkent VPS IP server for egress tied to an identity; build leases, the handler pool, health and meters (§ 7.1)
- [ ] T9-14 captcha → provisional pick: avoid, detect as an outcome with a kind, escalate, then solve through `ICaptchaSolver` (CapMonster Cloud or CapSolver plus 2Captcha), off by default and capped per step; the unlocker rung for HTML pages; human hand-over last (§ 2.4, § 7.2)
- [ ] T9-15 (T4-13) OLX `contact` step → provisional pick: back in scope as its own step in lane `olx.uz#contact`, residential floor, solver off; off per pipeline by default, Haven's pipeline turns it on; slice 2 (§ 6.1)
- [ ] T9-16 (W14) identification → provisional pick: a profile per source: `bot` with the bot page for hosts that do not block; coherent `browser` profiles elsewhere; one profile per egress session (§ 2.3)
- [ ] T9-17 (W3, W4, W5) robots and content signals → provisional pick: `robots_policy = obey` for link intake and unknown domains, `ignore` per source by an operator; `ai-input` recorded, not enforced (§ 5.2)
- [ ] T9-18 (T8-8) core asks → provisional pick: an egress option on `Http/Safety` that pre-resolves the target for third-party proxies; one handler per egress lease; a cookie container per session; generic resilience off on fetch clients (§ 3.5)
- [ ] T9-19 per-site recipes in public repos → provisional pick: generic providers public; recipes (OLX friction flow, header sets, private endpoints) in a private package or operator config bound by name (§ 4.7)
- [ ] T9-20 mass actions → provisional pick: v1 is reads plus bulk operations over posts (check, re-extract, re-deliver, export); mass writes (posting, joins, messages) go through Social's publish brokers and pools later (§ 4.5)
- [ ] T9-21 (P8) credential owner widens → provisional pick: proxy, solver, unlocker and provider vendor accounts join P8's owner question; all sealed in Social's store; caps per provider account in Social (§ 3.4)
- [ ] T9-22 (T1-P7, P6) WhatsApp linked-device route → provisional pick: allowed later as a `session.account` route (a whatsmeow sidecar); v1 stays intake plus channel snapshots, since no consumer needs WhatsApp channels yet (§ 5.1)
- [ ] T9-23 (P7, W1, W2) first web sources → provisional pick: mstar.uz, voyage.uz and Afisha in slice 1; iticket through its own JSON endpoints with a contract test, render as fallback, after the slice (§ 5.1, § 6.4)

---

## Sources

Read 2026-10-26.

Vendors:

- https://brightdata.com/pricing/proxy-network/residential-proxies · https://brightdata.com/pricing/proxy-network — residential per-GB tiers (50% promo), per-IP tables (type mapping inferred)
- https://brightdata.com/locations/uz — Uzbekistan: 41,130 residential, 1,024 datacenter IPs; header 10,538 (conflict); city targeting
- https://brightdata.com/pricing/web-unlocker — $1.50/1k pay-as-you-go, Scale $499 for 383k then $1.30/1k, success-only, captcha, fingerprint, rendering
- https://oxylabs.io/pricing/residential-proxy-pool · https://oxylabs.io/location-proxy/uzbekistan — per-GB tiers, plans; 81,764 Uzbek IPs, "from $8/GB"
- https://decodo.com/proxies/residential-proxies/pricing — $4/GB pay-as-you-go to $2/GB; sticky ≤ 30 min; the Uzbekistan page returned 404
- https://iproyal.com/pricing/residential-proxies/ — $7.35 → $1.84/GB; non-expiring traffic; sticky ≤ 7 days; the Uzbekistan page returned 404
- https://geonode.com/pricing — $0.30–0.88/GB; unmetered $1,800–3,800/month; 150+ countries
- https://shifter.io/location/uzbekistan — 98,708 Uzbek residential IPs (vendor claim; search result)
- https://www.pro-data.tech/en/virtual-server and whtop.com listings for pro-data.tech and ahost.uz — Tashkent VPS prices in UZS (search results)
- https://2captcha.com/pricing · https://www.capsolver.com/ · https://anti-captcha.com/ · https://capmonster.cloud/en/ — prices per 1,000 by widget kind; human vs AI
- https://www.zyte.com/pricing/ — per-1,000 prices by commitment and five site tiers, success-only

Workspace:

- `ls`: `ListingShelf.Application/Providers/Brokers/IListingBroker.cs` · `ListingShelf.Infrastructure/Providers/Brokers/HtmlListingBroker.cs` · `OlxListingBroker.cs` · `ListingShelf.Infrastructure/Providers/Clients/ListingPageClient.cs` · `ListingShelf.Infrastructure/Runs/OrchestrationServices/RunExecutionService.cs` · `Runs/Settings/RunExecutionSettings.cs` · `ListingShelf.Domain/Runs/Enums/CompletionReason.cs`, `StepKey.cs` · `ListingShelf.Domain/Pipelines/Enums/WorkType.cs` · `ventures.listing-shelf/engineering/architecture/architecture.md`
- `hv` at `65a355ad^` (deleted by `65a355ad`, 2026-09-26): `rce.Abstractions/Settings/Proxy/{ProxyProvider,ProxyServerProviderSettings,ProxySettings}.cs` · `rce.Abstractions/Enums/ExternalListingDataExtractionFailureType.cs` · `rce/Infrastructure/Extraction/Channels/OlxUz/Handlers/OlxUzStaticContentPhoneExtractionHandler.cs` · `…/OlxUz/Constants/{Errors,HeaderNameConstants}.cs` · `…/OlxUz/Models/FrictionApiResponse.cs` · `rce/Infrastructure/Extraction/Services/ExternalListingDataExtractionService.cs` · `rce/appsettings.json` · `hvb/Haven.Channels.Supply/Infrastructure/Listings/Capturing/Scraping/ScrapeListings/Nodes/FetchDetailsNode.cs` · `hvb/Haven.Channels.Supply/appsettings.json` · `engineering/deployment/domain-setup.md`; commits `4cd49e62` (proxy for detail pages), `e8f19be7` (friction handler)
- `hv` today: `engineering/planning/backlog.md` · `engineering/architecture/architecture.md`
- `be`: `Http/Safety/SafeOutboundHttpClientBuilderExtensions.cs`, `safety.spec.md` · `Http/Resilience/HttpResilienceOptions.cs` · `Web/Captcha/captcha.md` · `Web/RateLimit/` · `Web/Quotas/` · `Foundation/Security/` · `Integrations/integrations.md` · `Identity/Otp/Telegram/TelegramOtpDeliveryHandler.cs` · `Comms/WhatsApp/`
- [lead document](harvest-analysis-2026-10.md) · [spec](../harvest-service-spec.md) · [T1](t1-messaging-sources.md) · [T2](t2-social-sources.md) · [T3](t3-web-sources.md) · [T4](t4-consumers-and-social.md) · [T5](t5-post-model.md) · [T6](t6-extraction.md) · [T7](t7-pipelines-delivery.md) · [T8](t8-placement.md) · `conventions/development/repo/structure/domain-structure.md` · `conventions/development/capability-forms.md` · `conventions/development/dev-cycle.md`
