# T7 — Pipelines, subscriptions and delivery

*Last updated: 2026-10-26*

> Harvest's runtime half: how pipelines are identified, scheduled, run, shared and paid for; how tag and keyword
> subscriptions read the pool; how captures and link states reach consumers; and the workers, queues, budgets,
> tenancy and console that carry it. Result: split the spec's "pipeline" into a shared **pipeline** (the unit of
> harvesting) and a per-consumer **subscription** (the unit of consumption, with its own delivery); put one
> PostgreSQL queue of host-keyed **work items** under ListingShelf's runs; give every subscription one durable
> **event log** that serves webhooks, pull cursors, replay and dead letters; and gate every deletion inference on a
> run that proved a complete enumeration. ListingShelf and Haven both assume one process; the run model generalizes,
> the claiming, recovery and delivery do not.

Aliases: `W` = `/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws`.

- `ls` = `W/workbench/maxs-projects/ventures/saas/ventures.listing-shelf/engineering/codebase/listing-shelf.backend-services`
- `hv` = `W/workbench/maxs-projects/ventures/saas/10x-ven-haven/engineering/codebase/haven.backend-services/Haven.Supply`
- `be` = `W/workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src`
- Code read 2026-10-26; nothing built or run. SQL and queue shapes below are design sketches. `(U)` = unverified.
- Codes from earlier tracks: `W1…W18` (T3), `T1-P1…14`, `S1…S12` (T2), `T4-1…13`. P3–P9 are the lead document's.

---

## 1 · Prior art — what generalizes

| Part | ListingShelf | Haven | Verdict |
|---|---|---|---|
| Pipeline | provider + one source URL + `WorkType` (`Capture` · `Discover` · `Refresh`) + `PageLimit` 1–100 + `ItemLimit` 1–2,000 + `KeepPhotos` + `ExportRuns` (`PipelineEntity.cs`) | `Slug` + `ChannelId` + `BatchSize` (min/max) + free `Parameters` JSON that holds a cursor (`PipelineConfigEntity.cs`) | work kinds generalize; identity needs scope and owner; limits per work kind; the cursor idea becomes the durable frontier (T3) |
| Schedule | `IntervalMinutes` ≥ 5 + `ScheduleEnabled` + `NextDueAt`, advanced when the run is queued, so overdue intervals coalesce (`RunRepository.QueueAsync`) | cron string + `IsActive` + `AutoCycle`; a 30 s `PeriodicTimer` asks `GetNextOccurrence(lastCheck, UTC)` and starts what fell between ticks (`PipelineSchedulerBackgroundService.cs`) | keep LS's stored `next_due_at` and coalescing; take Haven's cron through `ICronExpressionParser`; a tick gap during downtime is lost in Haven, so due-ness must come from the stored time |
| Run | `RunEntity`: settings frozen at enqueue, `Trigger` (`Manual` · `Schedule`), `Status` ×7, `Stage`, counts, `Revision`, `CancellationRequested`, `Steps`, ≤ 100 `Errors` of ≤ 1,000 characters | `PipelineExecutionEntity`: `Status` ×5, `Trigger` (+ `Cycle`), node records with input/output counts, one error category | LS's run is the base; Haven's `Cycle` becomes a continuation run |
| Steps | `StepKey` `Discover` · `Capture` · `Archive`, each `Pending` · `Running` · `Completed` · `Skipped` · `Failed` with `Processed` / `Total` / `Message` | nodes declared per pipeline, `StepAsync(key, body)` persists start, counts, failure | step list per work kind, LS's record shape, Haven's wrapper that persists on every change |
| Outcomes | `CompletionReason` ×22; `Completed` only when reachable results ran out; one item's failure never fails the run; a gone page is a finding, not a failure (`RunExecutionService.cs`) | exception → `Failed`; no taxonomy | generalizes; section 2.7 extends it to three levels |
| Queue and claim | the runs table is the queue: `ClaimNextAsync` takes the oldest `Queued` row under SQLite `SerializedWrites`; `QueueAsync` refuses a pipeline that has a queued or running run | none: `PipelineRunner` keeps active runs in a `ConcurrentDictionary` and starts at once in `Task.Run` | the table-as-queue idea generalizes; serialized writes become `FOR UPDATE SKIP LOCKED`; the claim unit changes (section 7) |
| Recovery | `RecoverInterruptedAsync` at boot marks every `Running` run `Interrupted` (`HostRestart`) | `InterruptRunningAsync` at boot, same | valid for one process only; with several workers it kills live runs; needs leases |
| Progress | SignalR `RunChanged` carries the full run after each persisted change; clients merge by monotonic `Revision`, re-read over HTTP on reconnect, poll every 5 s offline | `IPipelineRunNotifier` | generalizes; scale-out needs a backplane without Redis (section 7.7) |
| Pacing | `RequestPacing` 500 ms run-wide; the first `AccessBlocked` or `RateLimited` ends the run; `Retry-After` ignored | none | replaced by per-host state (T3 W13) |
| Budgets, tenancy, delivery | none: no cost field, no auth (loopback only), delivery = `GET /api/runs/{id}/export` polled by Haven every 15 minutes | none | all new |

### Carry over unchanged

- freeze the pipeline's settings into the run at queue time; edits never rewrite history.
- one active run per pipeline and work kind; a second request is refused (`409` in LS) while one is queued or running.
- `Revision` on every persisted change; late writers cannot resurrect a terminal run (`RunRepository.SaveAsync` re-reads the status).
- terminal save retries three times so a slow write cannot leave a run `Running`.
- `Completed` means the source ran out, not that the limit was hit; capped, blocked or failed work ends `partial` or `failed` with a reason.
- an empty page is not proof of an empty source.

### Breaks at more than one worker

- `RecoverInterruptedAsync` / `InterruptRunningAsync` on boot.
- `ClaimNextAsync` picks a run, not a host: two runs on one host would race the politeness delay.
- in-memory "is running" maps (Haven) and `RunQueueTracker` wake-ups (LS) are per process.
- `NextDueAt` advanced at enqueue loses a cycle if the claimed run dies before it starts; fine with coalescing, but the lost cycle must be visible as `interrupted`, not silent.

---

## 2 · Pipeline model

### 2.1 Entities

| Entity | Is | Notes |
|---|---|---|
| tenant | a consuming service: Events, Haven, the ListingShelf view | owns keys, containers, subscriptions, budgets (T4-9: Events is the tenant, Ocharo never calls Harvest) |
| container | the visibility boundary: `public` (the shared pool) or `private:{tenant}/{name}` | one per Events catalog; a post lives in exactly one container (T5 holds the tables) |
| source | one harvestable origin with its adapter family, route ladder, host policy and posture | `permission`, `ai_allowed`, `pool_shareable`, `render` (T1–T3) |
| pipeline | a standing harvest of a source, in a container, with a scope and a work kind set | the shared unit; consumers join it |
| schedule | one cadence row of a pipeline: kind + mode + spec + window + `next_due_at` | a whole-site pipeline has three |
| subscription | one tenant's interest: a channel, a tag set or a keyword set, with its own delivery | the unit of consumption (section 3) |
| run | one execution of one schedule or trigger | section 2.6 |
| work item | one claimable unit: a URL fetch, a page, an API call, a provider job | keyed by host or by (account, method) (section 7) |
| event | one change a subscription must see, with a per-subscription position | the delivery log (section 5) |

- **Identity of a pipeline** = `(container, source, scope_key)`. `scope_key` is the canonical filter (sorted parameters, normalized URL or query) or `*` for whole-site.
- a whole-site pipeline is a **singleton per source and container**; consumers join, never duplicate.
- a filtered pipeline joins on an identical `scope_key` only; a different filter is a different pipeline (section 3.3).
- **state**: `proposed` · `pending-approval` · `active` · `paused` (`operator` · `budget-hard` · `permission` · `account` · `idle`) · `archived`.
- `pinned`: an operator flag; the pipeline runs with zero subscribers (section 3.5).
- **requested vs effective config**: each subscription states what it wants; Harvest derives the effective config; runs freeze the effective one.

### 2.2 Work kinds

| Kind | Does | Scope | Per-run limits | Default schedule |
|---|---|---|---|---|
| `capture` | discover through the source's listing path, then capture each item (LS `Capture`) | filtered | `maxPages`, `maxItems` | interval |
| `discover` | enumerate only; write addresses to the frontier (LS `Discover`) | either | `maxPages` | interval |
| `refresh` | re-capture the known frontier, least recently captured first (LS `Refresh`); event-time revisit per URL (T3) | either | `maxItems` | interval, plus due-driven |
| `sweep` | whole-site: a preset of three schedule rows on one pipeline: `discover` (enumerate), `refresh` (revisit), `check` (verify) | whole-site | request, byte and time budgets, no item cap | provisional hourly · weekly · daily (T3) |
| `check` | existence probe of known posts; emits link state; the method is T5's | either | `maxProbes` | daily |
| `metrics` | snapshot views, forwards and reactions outside the capture hash (T1-P10) | either | `maxPosts` | interval |
| `search` | later: query → candidate posts or sources for review (T4-3, P9) | n/a | `maxResults` | after the first slice |
| `intake` | not scheduled: forwards, guest mentions, uploads, webhooks (T1 route F) | n/a | consent record | event |
| `link` | one submitted URL, on demand; optional watch | n/a | one bounded fetch | on demand |

- `sweep` is not a separate engine: it is `discover` + `refresh` + `check` with a shared frontier and a night window.
- `check` also runs standalone on a filtered pipeline whose items stay in an active stage at a consumer (Haven: daily, a working assumption, T4).

### 2.3 Filtered vs whole-site

| | Filtered | Whole-site |
|---|---|---|
| Example | OLX Tashkent rentals; an Instagram hashtag; a keyword search | afisha.uz, mstar.uz, iticket.uz, a Telegram channel |
| Bounded by | `maxPages`, `maxItems` per run | the enumeration itself; guard = URL-count band (T3: a drop above ~30% marks the enumeration suspect) |
| Completeness claim | never; absence from results is not removal | yes, only after a complete enumeration (T3) |
| Absence inference | forbidden; only per-URL probes | allowed as `suspect`, then a direct fetch decides |
| Join rule | identical `scope_key` | any consumer joins the one pipeline |
| Filtering for consumers | in the pipeline | downstream: tags and keywords over the pool (section 4) |

- Ocharo's evidence: Afisha tags can omit every fashion term (`car-events.md:462`), so harvest whole, then filter.
- ListingShelf's `ItemLimit` 2,000 and `PageLimit` 100 fit filtered pipelines; `sweep` takes budgets instead (T3 limits finding).

### 2.4 Limits

| Limit | Level | Default | Rule |
|---|---|---|---|
| `maxPages`, `maxItems` | pipeline, filtered | LS values (100, 2,000) | cap set by the source adapter; a larger subscriber request is clamped |
| `maxRequests`, `maxBytes`, `maxSeconds` | run, `sweep` | per source | exceeding ends the run `partial` with `request-limit` · `byte-limit` · `time-limit` |
| `maxProbes` | run, `check` | per source | probes are billed on provider routes (T2 S5) |
| concurrency | host | 1 connection, ≥ 2 s (W13) | host policy, not pipeline |
| active runs | pipeline × kind | 1 | LS rule |
| manual runs | pipeline | ≥ 15 min apart per tenant (pick) | stops a tenant hammering a shared source |
| submissions | tenant | per-day quota | section 6 |

### 2.5 Schedules

| Mode | Spec | Use |
|---|---|---|
| `manual` | none | small sites on request ("manual or automatic", developer 2026-10-26); `run now` is a run with trigger `manual` |
| `interval` | minutes, ≥ the source floor | most pipelines (LS) |
| `cron` | cron expression + IANA zone (`Asia/Tashkent` default) via `ICronExpressionParser` | night sweeps, weekly passes (Haven) |
| `adaptive` | `min` · `max` interval + change-rate rule | pipelines whose change rate varies (P2) |
| `revisit` | per-URL `next_due_at` from event time (T3: ≤ 14 days daily, later weekly, stop 7 days after `endDate`) | frontier policy, not a pipeline schedule |

- the **floor** per schedule = max(pipeline minimum, source floor, route floor). Route floors: Telegram preview newest page 5 min (T1 5.4), YouTube units/day, Threads queries/24 h, Instagram hashtags 30/7 days (T2 quota ledger).
- **windows**: `sweep` and bulk `refresh` run inside a night window in `Asia/Tashkent` (W13); `window` is a field of the schedule row, enforced at claim time (items outside the window stay queued).
- **misfire**: coalesce. A pipeline overdue by many intervals gets one run, never a backlog (LS).
- `next_due_at` advances when the run is queued, plus ±10% jitter on `interval` (pick); a run that never starts shows as `interrupted` (lease expired).
- **adaptive rule (sketch)**: after 3 consecutive runs with zero `new` and `changed`, double the interval up to `max`; after a run whose change rate exceeds 10% of captured items, halve it down to `min`. Thresholds are placeholders (T7-P10).
- every schedule row can be `enabled = false`; Haven's `IsActive` and LS's `ScheduleEnabled` collapse into it.
- deletion checks (developer: automatic and configurable) are the `check` row: mode, spec, window and `maxProbes` are configuration; the check method per route is T5's.

### 2.6 Runs and steps

| Field | Meaning |
|---|---|
| `id` · `pipeline_id` · `kind` · `container_id` | identity; `kind` is the schedule row that fired |
| `trigger` | `manual` · `schedule` · `continuation` (Haven `Cycle`: more frontier left) · `join` (new subscriber needs a pass) · `intake` · `link` |
| `frozen` | effective config at queue time: limits, route ladder snapshot, window, flags, budget ids |
| `status` | LS ×7: `queued` · `running` · `completed` · `partial` · `failed` · `cancelled` · `interrupted`; plus `paused` (non-terminal: budget hard stop, awaiting a human, permission pending) |
| `stage` · `steps` | ordered step records, section below |
| counts | `pages` · `discovered` · `captured` · `unchanged` · `failed` · `gone` (LS `Unavailable`) · `skipped` · `requests` · `bytes` |
| cost | `cost_usd_est`, `cost_usd_billed` (section 8) |
| `lease_owner` · `lease_until` · `heartbeat_at` | recovery (section 7.6) |
| `revision` · `cancellation_requested` · `errors` (≤ 100) · `completion_reason` · `message` | LS |

- steps per kind: `enumerate` → `fetch` → `store` → `extract` (optional, T6) → `link` (T5 dedup, state) → `emit` (event rows). Each step carries `processed`, `total?`, `message`, and Haven's `input`/`output` counts.
- `emit` writes the subscription events **in the same transaction** as the capture or state change (transactional outbox); no capture exists without its events, no event without its capture.
- a run that ends `partial` or `failed` must not advance "last verified" or emit absence inferences (section 2.7).
- `paused` is the one addition to LS's statuses; `deferred` is not a status, only a work-item `not_before` (a waiting room or flood wait moves items, not runs).

### 2.7 Outcomes — three levels

ListingShelf's single `CompletionReason` mixes why the run stopped, what happened to an item, and the state of a source. Harvest needs three.

**Run reasons** (why the run stopped)

| Reason | From | Status |
|---|---|---|
| `exhausted` | LS `ReachableResultsExhausted` | `completed` |
| `no-items` | LS `NoListings` | `completed` or `failed` by source rule |
| `page-limit` · `item-limit` · `request-limit` · `byte-limit` · `time-limit` | LS + new | `partial` |
| `repeated-page` · `repeated-items` | LS | `partial` |
| `detail-failures` | LS | `partial` |
| `budget-hard` · `quota-exhausted` · `window-closed` | T2, T3 | `partial` or `paused` |
| `cancelled` · `interrupted` · `lease-expired` | LS `Cancelled`, `Interrupted`, `HostRestart` | terminal |
| `execution-failed` | LS | `failed` |
| the source outcomes below, when they stop the run | T3 | `failed` if nothing captured, else `partial` |

**Source and fetch outcomes** (what the host or platform answered)

| Outcome | Origin | Action |
|---|---|---|
| `robots-disallowed` | T3 | stop that path; no retry until the robots cache expires; link intake falls back to manual entry (W4) |
| `restricted` | T3 `permission` | not scheduled; manual entry only |
| `challenge` · `waiting-room` | T3 | host `paused_until` with backoff 15 min → 1 h → 6 h; alert after 3 |
| `blocked` (401/403) · `rate-limited` (429, 503 + `Retry-After`) | LS `AccessBlocked`, `RateLimited` | pause the host; honour `Retry-After` (cap 15 min per attempt, T3); never end the whole run for one host if other hosts have work |
| `render-required` | T3 | re-queue the item on the render route if the source allows, else report |
| `network-error` · `fetch-timeout` · `http-error` · `unexpected-content` · `response-too-large` · `invalid-redirect` | LS | retry twice (1 s, 2 s), then item failure |
| `unrecognized` | LS `UnrecognizedPage` | report with the sample capture |
| `not-approved` · `provider-failed` · `quota-exhausted` · `budget-exceeded` | T2 ladder | fall to the next enabled route, else `paused` |
| `connection-invalid` | T4-4 | pipeline `paused (account)`; event to the owning tenant |

**Item outcomes** (what happened to one post or URL)

| Outcome | Meaning |
|---|---|
| `new` · `changed` · `unchanged` | LS change tags by content hash |
| `gone` · `moved` · `suspect` · `relisted` | T3/T5 link-state machine; T7 only transports it |
| `source-unavailable` | T1: a private or removed channel never marks its posts gone |
| `extraction-skipped` | `ai_allowed=false`, budget hard stop, or `ai-input=no` (T1, T3 W5); the capture still delivers |
| `media-too-big` | T1 WhatsApp `131052` |

**Account states** (persistent health, not a run result; section 7.4): `active` · `rate_limited` · `session_lost` · `deactivated` · `frozen` · `limited` · `full` · `quarantined`; membership `none` · `peeking` · `join_requested` · `member` · `left` · `banned`.

- **Rule**: only a run that ended `completed` after a complete enumeration may set `last_verified_at`, produce `suspect` from absence, or send a "nothing new" digest. Everything else is "unchecked" (Ocharo: failed access is never "no new events", `car-events.md:364`).
- alerting: `challenge` and `blocked` alert after 3 consecutive runs (T3); `session_lost`, `frozen` and `deactivated` alert at once (T1).

---

## 3 · Shared pipelines and subscriptions

### 3.1 Subscription kinds

| Kind | Subscribes to | Creates a pipeline? | Reads | Delivery unit |
|---|---|---|---|---|
| `channel` | a source, optionally with a scope (a site, a Telegram channel, an Instagram account, a hashtag) | creates or joins | every post of that pipeline | post revision and link-state events |
| `tag` | tag keys from T6's vocabulary | never | the pool: classified posts from many pipelines visible to the tenant | matches |
| `keyword` | keyword sets (word, phrase, language) | never; may *propose* (section 4.3) | the pool | matches |
| `link` | not a subscription: a one-off submission or a single-URL watch | private `link` pipeline | one URL | post events to the submitting tenant |

### 3.2 Create or join

1. Resolve the request to a `source` (registrable domain + adapter; social URL → platform adapter, T3 2.7).
2. Canonicalize the scope → `scope_key`.
3. Look up `(container, source, scope_key)`. The container is `public` when the source is public and the request fits public policy; otherwise the tenant's private container.
4. Hit → **join**: add the subscription, recompute the effective config, backfill (3.6).
5. Miss → **create**. Creation is `active` at once only when the source is `open`, needs no account, uses a free route and is inside the tenant's pipeline quota; otherwise `pending-approval` (T7-P3).
6. Answer with `requested` and `effective` side by side, so a clamped request is never silent.

- private pipelines are never joined by another tenant.
- a public pipeline can be joined by any tenant with `subscriptions:manage`.

### 3.3 Config merge

| Field | Rule | Why |
|---|---|---|
| freshness | each subscriber states a **maximum staleness** (`6h`); the pipeline interval = min over subscribers, clamped to [floor, ceiling] | a cron string cannot be merged; a staleness bound can |
| window | operator or source policy only | a subscriber cannot force a daytime sweep |
| `maxPages`, `maxItems` | max over subscribers, clamped to the adapter cap | captures are shared, so the larger request serves all |
| filter | no merge; a different filter is a different pipeline | the pool query (tags, keywords) covers the narrower view |
| AI extraction | per **subscription** (`wants_ai` + schema); the pipeline extracts when any subscriber wants it and the source allows | extraction is cached per content hash + schema + prompt version (spec), and billed to who asked |
| photos / media | kept when any subscriber wants them | |
| deletion-check cadence | min over subscribers' staleness for link state | |
| delivery target, secret, mode, `context` | never merged; per subscription | |
| posture (`permission`, `ai_allowed`, `pool_shareable`) | source-level, not mergeable | a subscriber cannot widen a terms posture |

- the effective config is a pure function of active subscriptions + source policy + operator overrides; it is recomputed on join, leave and policy change.
- a subscriber that asks for less than the effective config still receives everything the pipeline captures; trimming is the consumer's side.
- containment (a narrow filter inside an existing whole-site pipeline) is the tag/keyword path, not a merge.

### 3.4 Whose budget pays

| Cost | Charged to | Basis |
|---|---|---|
| fetch, render, provider units on a **public** pipeline | WoW2's operator budget (pipeline and provider caps) | the pool is operator-owned; Events is the first consumer |
| the same on a **private** pipeline | the owning tenant's budget | their container |
| AI extraction | the subscription(s) that asked | exact: tokens × price per call, recorded per subscription (T6) |
| a tenant's share of a public pipeline | an equal split among current channel subscribers, shown in the console and counted against the tenant's monthly cap | predictable; a second subscriber lowers the first's share |
| hard stops | always on the pipeline, the provider and the global cap, never on a share | a stop must not depend on who else subscribes |

- per-tenant provider credentials (self-hosted) and a per-consumer budget on the provided instance follow S3 (section 9.2).
- the marginal view ("what this subscriber added to the effective config") is console-only in v1 (T7-P4).

### 3.5 When the last subscriber leaves

| Pipeline | Rule |
|---|---|
| private | `archived` after a grace period; captures follow the tenant's retention; deleting data is explicit |
| public, not pinned | schedules disabled (`paused (idle)`) when the last **channel** subscriber leaves; archived after 30 days idle (pick); data stays in the pool per retention |
| public, `pinned` | keeps running; an operator seeds the pool for tag and keyword readers |

- tag and keyword subscriptions are **weak references**: they read the pool but keep nothing alive. A pipeline whose only readers are weak shows "N readers depend on this" in the console; an operator decides to pin it.
- re-joining an idle pipeline resumes it and runs the backfill gap (a `join` run if the last pass is older than the joiner's staleness).

### 3.6 Backfill on join

- the joiner's event log starts with a **replay of the pipeline's current live posts** (`backfill=live`, default), written as `post.new` events with `reason: backfill`; options `none`, `since:{date}`.
- backfill is delivery only: no fetch cost. It drains at a throttled rate through the same event log, so a webhook endpoint is not flooded (section 5.5).
- a `join` run is queued only when the last complete pass is older than the joiner's staleness.
- AI extraction under the joiner's schema runs for **new and changed captures only**; extracting history is opt-in, with the T6 cost estimate shown first (`backfill_extract=false`).
- a pull-only subscriber can instead start at `now` or at a date through its cursor.

---

## 4 · Tag and keyword subscriptions over the pool

### 4.1 Matching: ingest or query time

| Option | How | Cost | Latency | Fits |
|---|---|---|---|---|
| A · query time | `GET /v1/posts?tags=…&q=…&after=` over indexes (GIN on tag arrays, full-text on normalized text) | nothing at ingest; each read pays | pull only | ad-hoc reads, resync, retroactive views |
| B · ingest-time fan-out | on each post-ready event, evaluate active rules and write a match event per subscription | O(tokens) per post with a compiled term table; no scan per subscription | push-ready | webhooks, cursors |
| C · hybrid | B for the event log, A for reads, one rule definition for both | both | both | **pick** |

- **when**: matching runs on `post.ready` — after classification finishes (T6), not at capture time — because tags appear later and can change.
- **rule changes**: a new or edited rule matches new posts only. History comes from an explicit backfill (a query-time read written as `reason: backfill` events). Silent retroactive pushes would flood.
- **keyword engine**: tokenize the post's normalized text once; look tokens up in a `keyword_rule(term, language, subscription_id)` table; phrases use a PostgreSQL `tsquery`. PostgreSQL ships a `simple` configuration; no Uzbek configuration is known to ship (U: the built-in list was not confirmed; `SELECT cfgname FROM pg_ts_config` on the target server settles it). Script folding (Uzbek Latin ↔ Cyrillic) and stemming belong to T6's `search_text` (T7-P11).
- **tags**: exact match on T6 tag keys, any-of / all-of per subscription.
- **visibility filter**: a match query always restricts to posts the tenant may read — `public` pool (only rows whose route is `pool_shareable`) plus the tenant's own containers.
- **AI posture**: sources with `ai_allowed=false` (Telegram default, T1-P1) get rule-based tags only; a `tag` subscription misses what only an LLM would tag, a `keyword` subscription still sees the raw text. Say so in the console.

### 4.2 What a match delivers

- one event per `(subscription, post, revision)`; several rule hits fold into `matched: [{kind, value}]`.
- a post the subscription has already seen produces `post.changed` and `link.state` events even when it no longer matches (the consumer must be able to update or remove it); a post never delivered produces nothing on state changes.
- the per-subscription **seen set** (`subscription_post(subscription_id, post_id, first_event, last_revision, link_state)`) is what makes `gone` and `relisted` reach exactly the subscribers who hold the post (T4-2).

### 4.3 A keyword proposes, never creates (T4-6)

- a **proposal** is a record `{kind: keyword | link | search, evidence, suggested source + scope, status: proposed | approved | rejected | expired}` shown in the review queue.
- v1 sources of proposals:
  - a link on an unharvested domain (section 6): "harvest this domain publicly?";
  - a coverage gap: a keyword subscription with zero matches over N days flags "no pipeline feeds this" — no automatic source suggestion without a `search` adapter;
  - later, `search` results as candidates (T4-3, P9).
- approval needs `pipelines:manage` (operator or a tenant admin for a private container) and the posture checks of 3.2; approval creates the pipeline, nothing else does.

---

## 5 · Delivery

### 5.1 One log, two doors

- every subscription owns an **event log** (`subscription_event`): rows hold references (`post_id`, `revision`, `link_id`, `capture_id`), not payloads; the payload is rendered at send or read time from the post revision.
- **webhook push** and **pull cursor** read the same log. A subscription has `mode: webhook | pull | both`.
- replay, ordering, idempotency, retry state and dead letters live on the log row, so no second mechanism is needed.
- fan-out at ingest writes one row per matching subscription; with tens of subscriptions this is trivial. Revisit above ~1,000 subscriptions (U).

### 5.2 Event types

| Event | Raised when | Carries | `item_id` |
|---|---|---|---|
| `post.new` | the subscription first sees a post (`reason`: `ingest` · `backfill` · `resync`) | base fields (T4-1), `links[]` with state, media refs, capture ref, container, `matched` for pool subscriptions; `extracted` when AI or a deterministic tier ran | hash(post, revision) |
| `post.changed` | a new revision: content hash changed, a link added or removed | same plus `changes` summary | hash(post, revision) |
| `post.extracted` | extraction finished after the capture was delivered (async or later schema) | `schema`, `schema_version`, `tier` (`deterministic` · `llm`), `model?`, `prompt_version?`, `confidence?`, `fields` | hash(post, revision, schema, versions) |
| `link.state` | a source link moves `live` · `gone` · `relisted` (T4-2) | `link_id`, `state`, `since`, evidence ref; `post_gone: bool` when every link is gone | hash(link, state, since) |
| `pipeline.run` | a run finished, optional per subscription | `pipeline`, `kind`, `status`, `complete: bool`, counts, `checked_at` | run id |
| `pipeline.health` | source blocked, restricted, unavailable; account or connection down; budget soft or hard | `pipeline`, `outcome`, `since` | pipeline + outcome + since |

- Harvest always delivers captures; `extracted` is optional (spec decision 2026-10-26) and its absence is not an error.
- `pipeline.run` exists so a consumer can tell "nothing new" from "unchecked".
- **delivery unit**: the canonical post revision, with `links[]` limited to links the subscriber may see (T7-P7, T5).
- payloads cap at 256 KiB (the SDK's `MaxStoredPayloadBytes`); media and raw HTML travel as File Storage references and `GET /v1/captures/{id}`.

### 5.3 Webhooks

- signing: Standard Webhooks — headers `webhook-id`, `webhook-timestamp`, `webhook-signature`; `v1,` + base64 HMAC-SHA256 over `id.timestamp.body`; several signatures in one header allow key rotation [standard-webhooks]. The SDK ships `StandardWebhookSignatureIssuer` (`be/Messaging/Webhooks/Issuers`).
- `webhook-id` = the event row id, **identical across retries and redeliveries** [standard-webhooks]; consumers deduplicate on it.
- body is sent byte-for-byte as signed.
- retry: durable, from the log row (`attempts`, `next_attempt_at`, `last_status`). Pick, spaced after the previous attempt: 0 s, 5 s, 5 min, 30 min, 2 h, 5 h, 10 h ×4, 24 h — 11 attempts over ~72 h with ±20% jitter. The spec's own example runs from immediate to 75+ hours [standard-webhooks].
- status handling (from the spec): `2xx` success · `3xx` failure, no redirect following · `410` disable the endpoint, stop · `429` / `502` / `504` throttle · other statuses and network errors retry · honour `Retry-After` [standard-webhooks].
- additions: a `4xx` other than `408` / `429` dies after 3 attempts (a permanent rejection should not burn 72 h); per-attempt timeout 15 s (pick; the SDK default is 30 s).
- **dead letter**: after the last attempt the row is `dead`, with `last_status` and `last_error`; the console redrives one or many; a dead row does not block later events.
- **endpoint health**: `healthy` → `degraded` (failures in a row) → `suspended` (all attempts of several events failed, or `410`); a suspended subscription keeps accumulating log rows; resuming replays from the last acknowledged position.
- secrets are stored through Data Protection (`dp1:` prefix, SDK persistence); rotation keeps two active secrets for an overlap window.
- verify on the receiver with the SDK's `AddInboundWebhooks` + `RequireWebhookSignature`, which enforces a replay window.

### 5.4 SDK gap

- `be/Messaging/Webhooks/WebhookPublisher.cs` delivers **inline**: `PublishAsync` loops the matching subscriptions and calls `DeliverAsync` in the same call; retries are in-process (`MaxAttempts` 3, backoff 500 ms → 30 s) and the delivery log records only the terminal `Delivered` / `Dropped`.
- that is not at-least-once over days: a process stop loses pending retries.
- reusable: signing issuers, subscription store with protected secrets, `EfWebhookDeliveryRepository`, `WebhookRedeliveryService` (same id, fresh signature), inbound receiver.
- missing: a durable queue of attempts with `next_attempt_at`, claimed with `FOR UPDATE SKIP LOCKED` (the SDK already has that claim for the outbox: `PostgresSkipLockedOutboxClaimRepository`), per-endpoint health, dead-letter state and redrive.
- Identity's webhooks (M13, "delivery is at least once") need the same thing. Per the SDK doctrine, build the **durable dispatcher in the be SDK**, not in Harvest (T7-P9, T8).

### 5.5 Pull cursor feed

```http
GET /v1/subscriptions/{id}/events?after={cursor}&limit=100
→ { "data": [ …events… ], "next": "{cursor}", "hasMore": true }
```

- the **client holds the cursor**; the server stores `last_read_at` and lag for display only. Replay = pass an older cursor within retention; reset = omit `after`, or `from=now`.
- cursor = opaque `(tx, id)`: `tx` is `pg_current_xact_id()` (an `xid8`, 64-bit, no wraparound [pg-functions]) stamped on the row by default; `id` a bigint identity.
- identities and sequences assign values before commit, so a poller that advances to the highest id can skip a lower id that commits later [cloudscale, dudycz]. The fix from the outbox literature: read only rows with `tx < pg_snapshot_xmin(pg_current_snapshot())`, ordered by `(tx, id)` [dudycz]:

```sql
SELECT * FROM subscription_event
WHERE subscription_id = $1
  AND (tx, id) > ($2, $3)
  AND tx < pg_snapshot_xmin(pg_current_snapshot())
ORDER BY tx, id
LIMIT $4;
```

- cost: a long transaction anywhere holds every feed back. **Rule: no transaction spans network I/O** (fetch, provider call, webhook send). Whether `xid8` has a btree operator class for the row comparison and its index is unverified (U); a counter per subscription is the fallback and serializes writers per subscription.
- long-poll (`wait=25`) is optional; `LISTEN/NOTIFY` can wake it (section 7.7).
- `resync`: `POST /v1/subscriptions/{id}/resync` writes a snapshot of the current visible posts as `post.new` with `reason: resync` after a gap longer than log retention (30 days, pick) or a rule edit.

### 5.6 Ordering and idempotency

- **at least once**; no global order. Per post: events carry a monotonic `revision` (and `link.state` a `since`); a consumer applies the highest revision (the same merge LS's console does with `Revision`).
- push keeps **per-post FIFO**: a row is claimable only when no earlier non-dead row for the same `(subscription, post_key)` is pending, retrying or sending. Other posts proceed, so one failing post cannot stall the stream.
- two ids on every event: `event_id` (= `webhook-id`, per subscription, stable across retries) and `item_id` (content identity, equal across subscriptions and across resyncs). Events' intake is idempotent on `item_id` (events spec § Harvest seam).
- `Idempotency-Key` on every `POST` (links, entries, subscriptions): the key and the response are kept 24 h (pick); a repeat returns the stored response.
- `GET /v1/events/{event_id}` and per-row redrive support audit and replay.

### 5.7 What Events' `POST /harvest/items` needs

| Events needs (spec § Harvest seam + T4) | Harvest sends | Change to the specs |
|---|---|---|
| items idempotent on item id | `item_id`, `event_id`, `revision`, `supersedes` | add `revision`, `supersedes` |
| pipeline, capture URL, captured at, content hash, schema version, model, prompt version, confidence | same fields under `capture` and `extracted` | `extracted` becomes optional; add `tier` |
| route to a catalog without a pipeline→catalog table | the subscription's opaque `context` (`{"catalog":"ocharo-fashion"}`) echoed on every event, plus `subscription_id` | new field; Events sets it at registration |
| dates as published, with precision (T4 § 2) | base `dates[]` with raw string, parsed value, `precision` | T6 fixes the shape |
| a vanished page is a hint, not a cancellation | `link.state` with `since`; `post.changed` with the diff | Events accepts these types |
| failed access is "unchecked", never "no new events" | `pipeline.run{complete, checked_at}` and `pipeline.health` | new types |
| provenance of many sources (`es:71`) | `links[]` with source, URL, state, first seen | new |
| signature check | Standard Webhooks headers, replay window 5 min | add to the spec |
| acknowledgement | `2xx` = stored; duplicates must also answer `2xx`; `400` / `422` = permanent reject | write the rule into the intake contract |
| batch | one event per request in v1 | batching later (T7-P8) |

- Events registers one subscription per source (`kind: channel`, `mode: webhook`, `wants_ai: true`, schema `wow2.event.v1`, `context`), as its spec says; sites with JSON-LD `Event` fill the schema deterministically (T3), so `tier: deterministic` carries no model fields.
- Events is the Harvest tenant; a link or entry for the Ocharo catalog arrives from Events with an `actor` (section 6).

---

## 6 · Link intake and manual entry

### 6.1 Link flow

`POST /v1/links` `{ url, container?, watch?, actor }` with `Idempotency-Key`, scope `links:submit`.

1. **Normalize** (T3 2.7 step 1): http(s) only, no userinfo, IDNA host, drop fragment and tracking parameters.
2. **Route by pattern**: social URLs go to the T1/T2 adapter's single-post lookup; no adapter → a link card from OpenGraph / oEmbed (W16).
3. **Match public pipelines** by registrable domain **and** path scope (T4-11):

| Case | Container | Policy |
|---|---|---|
| URL inside an active public pipeline's scope (whole-site: any included path; filtered: passes the pipeline's own URL claim) | `public` | return the existing post if captured; else a single-URL work item in that pipeline under its host policy, flagged `trigger: link` |
| public source, URL outside every public pipeline's scope (an OLX ad outside the Tashkent-rentals filter) | tenant's private container | capture with that source's adapter and the **shared host limiter**; stays private |
| unknown domain | tenant's private container | `link` pipeline: one bounded fetch, `robots.txt` enforced, SSRF-safe connect (T3) |
| source `restricted` (Afisha before W1) | none | outcome `restricted`; offer manual entry |

4. **Answer**: `200` with the existing post, or `202 { linkId, status: queued }`; completion arrives as `post.new` or `pipeline.health` on the tenant's subscription and `GET /v1/links/{linkId}`.
5. **Failure → manual entry**: `robots-disallowed`, `restricted`, `challenge` after the retry budget, `render-required` on a source that forbids render: the link row ends `needs-manual` with the outcome, and the product shows its typed-entry path (W4).
6. **Watch** (optional): a schedule row on a one-URL private pipeline, interval ≥ 1 day; counts against the tenant's pipeline quota.

- **the container decides visibility, the host decides pacing**: a private capture of an olx.uz URL still waits behind olx.uz's `next_allowed_at`.
- a public in-scope capture is the same post the pipeline would find; it spends public budget, so submissions have a per-tenant daily quota and are `interactive` priority only up to a small cap.
- captures are never promoted from private to public. If the domain later becomes public, the public pipeline captures independently; T5 may link the two canonical posts.
- an unharvested-domain submission files a `link` proposal (section 4.3) for an operator to consider a public pipeline.

### 6.2 Manual entry

`POST /v1/entries` `{ fields, source_url?, reason?, container, actor }`, scope `entries:write`; edits are `PUT /v1/entries/{id}`, each a **new revision**, never an overwrite.

- stored as a capture with `provenance: manual`, `actor_id`, `actor_role`, `entered_at`, `key_id`, optional `reason` (`robots-disallowed` · `restricted` · `challenge` · `no-source`), optional unfetched `source_url`.
- entries live in a private container only. The public pool holds Harvest-fetched content, so its provenance stays clean (T7-P14).
- entries run through the same base-field validation, dedup (T5) and delivery as captures; AI extraction is optional, as for any capture.

### 6.3 What Harvest itself checks

| Check | Harvest | The product |
|---|---|---|
| key valid, tenant resolved | yes | |
| key scope holds `links:submit` / `entries:write` | yes (`RequireApiKeyScope` in the SDK) | |
| container belongs to the key's tenant | yes | |
| `actor.id` present, ≤ 128 characters; `actor.role` is a recorded string | yes (required, stored, audited) | |
| the actor's role may submit or type (Desk `CanEdit`) | no | yes (T4-10, `es:130-131`) |
| `provenance: manual` is set only by the entries endpoint | yes (server-side; never accepted from the body) | |
| submission and entry quotas per key and per tenant | yes | |
| size and shape of fields; URL fields normalized | yes | |
| append-only audit `(key_id, actor, action, target, at)` | yes | |
| consent and deletion of third-party data (T1-P9) | yes, for intake sources | |

- Harvest trusts the product's `actor` as a claim from an authenticated service key; it records it, never verifies the person.
- under Identity (M10 client credentials, audience `harvest`, scopes `harvest.links.submit`), the actor arrives as an `act` claim from token exchange (M11, P2); until then it travels in the body.

---

## 7 · Workers and runtime

### 7.1 Roles

| Role | Does | Scales by |
|---|---|---|
| `api` | HTTP API, console BFF, SignalR | replicas |
| `scheduler` | turns due schedules into runs and plans work items | any number: `UNIQUE (pipeline_id, kind, scheduled_for)` makes the insert idempotent, no leader election |
| `worker` | claims work items by host, fetches, stores, emits | replicas |
| `render` | a separate container with Playwright; claims only `route = render` items (W7) | replicas, memory-bound |
| `account` | holds platform sessions as leases (Telegram `M`) | one holder per account, by lease |
| `deliverer` | claims due event rows, sends webhooks | replicas |
| `maintenance` | retention, pruning, reaper, compliance jobs (T2: X batch compliance, YouTube 30-day verify), budget reconciliation | one at a time by lease |

- one binary, roles by configuration: a Form 2 bundle runs `api + scheduler + worker + deliverer + maintenance` in one process; `render` stays a second container.

### 7.2 Two queue levels

- **run**: bookkeeping and planning — counters, steps, completion, cost, lease. Claimed by the scheduler path, not by fetch workers.
- **work item**: the claimable unit, grouped by `host_key`. For web sources the frontier rows (T3) are the queue; for platform calls the key is `(account_id, method)`; for provider jobs it is `provider_account_id`.
- reason: LS claims a whole run, so two runs on one host would race the delay, and one slow sweep would hold a worker for 30+ minutes (afisha at 1 request / 2 s ≈ 33 min per 1,000 pages, T3). Item-level claiming also makes restart recovery a lease expiry instead of a rerun.

| Work item field | Meaning |
|---|---|
| `run_id` · `pipeline_id` · `container_id` | owner |
| `host_key` / `bucket_key` | `olx.uz`, `t.me`, `acct:42/getHistory` |
| `route` | `static` · `render` · `api` · `provider` · `account` |
| `state` | `queued` · `running` · `done` · `failed` · `gone` · `blocked` |
| `priority` | `interactive` (link awaiting a user) > `fresh` > `sweep` > `check` > `backfill` |
| `not_before` · `attempts` · `lease_owner` · `lease_until` | scheduling and recovery |

### 7.3 Claiming by host (W10) and politeness (W13)

- host policy is **global**, across tenants, containers and pipelines: five pipelines on `olx.uz` share one limiter, and so do private link captures.

| `host_state` field | Meaning |
|---|---|
| `host_key` | registrable domain or API host |
| `max_concurrency` | 1 (W13) |
| `min_delay_ms` · `adaptive_delay_ms` | ≥ 2 s; then `max(base, latency / target concurrency)` (T3, AutoThrottle formula) |
| `crawl_delay_s` | from `robots.txt`, honoured up to 30 s (W13) |
| `retry_after_until` · `paused_until` · `consecutive_failures` | 429/503 and `challenge` / `waiting-room` backoff |
| `next_allowed_at` · `in_flight` | the gate a claim checks and sets |
| `window` · `egress` | night window; static egress id when a source needs one (W8) |
| `robots_cached_at` · `permission` | cache ≤ 24 h (RFC 9309, T3) |

Claim sketch (not run):

```sql
-- 1 pick a host that may be fetched now and has queued work; lock only its state row
SELECT h.host_key FROM host_state h
WHERE h.next_allowed_at <= now() AND h.in_flight < h.max_concurrency
  AND (h.paused_until IS NULL OR h.paused_until <= now())
  AND EXISTS (SELECT 1 FROM work_item w WHERE w.host_key = h.host_key
              AND w.state = 'queued' AND w.not_before <= now())
ORDER BY h.next_allowed_at
FOR UPDATE OF h SKIP LOCKED LIMIT 1;

-- 2 take that host's best item
SELECT id FROM work_item
WHERE host_key = $1 AND state = 'queued' AND not_before <= now()
ORDER BY priority DESC, due_at
FOR UPDATE SKIP LOCKED LIMIT 1;

-- 3 same transaction: set the item running with a lease, bump in_flight,
--   next_allowed_at = now() + delay; commit. The fetch runs outside any transaction.
```

- PostgreSQL documents `SKIP LOCKED` as an inconsistent view, unsuitable for general work but meant for queue-like tables with many consumers [pg-select]; that is this use.
- the lock is held for the claim only; politeness comes from `next_allowed_at`, not from holding a row during I/O.
- the **result write is fenced**: `UPDATE work_item SET state = 'done' … WHERE id = $1 AND lease_owner = $2 AND state = 'running'` in the same transaction as the capture insert; zero rows → roll back (the lease was lost to a reaper; a zombie worker cannot double-write).
- `interactive` items jump the queue but never the pacing.
- `challenge`, `waiting-room`, `blocked`, `rate-limited` set `paused_until` or `retry_after_until` on the **host**, so other hosts keep flowing (LS stops the whole run).
- the SDK's `PostgresSkipLockedOutboxClaimRepository` is the same pattern for the outbox (`SELECT … FOR UPDATE SKIP LOCKED LIMIT`).

### 7.4 Account pool, per-account limits, flood waits (T1)

| Account state | Signal | Effect on work |
|---|---|---|
| `active` | | claims allowed |
| `rate_limited` | `FLOOD_WAIT_X`, `FLOOD_PREMIUM_WAIT_X` | that `(account, method)` bucket gets `not_before = now + X` exactly; items are moved, not failed |
| `session_lost` · `deactivated` | `AUTH_KEY_*`, `USER_DEACTIVATED`, `SESSION_*` | stop; alert; human re-login |
| `frozen` · `limited` | `FROZEN_*`, `PEER_FLOOD`, `@SpamBot` | stop writes; reads (U); appeal is human |
| `full` | joined-chat cap (500 / 1,000) | sources assigned elsewhere up front |
| `quarantined` | operator | no claims |

- **sticky assignment, no failover on flood waits** (T1-P5): a source has one `account_id` for life; a flood wait delays its bucket; it never moves to another account or IP. Failover happens on account death only, and only to an account that already holds the membership. Joining a group on a spare is a human-approved step (T1-P6), so "failover" in practice is an operator action; an unassigned source reports `needs-account`.
- **token bucket per `(account, method)`**; budgets in provisional values tuned on observed waits (T1 5.4). Disable the library's automatic flood retry so every wait lands in the ledger (U: `WTelegramClient` `FloodRetryThreshold`, T1 2.5).
- **session lease**: `account_lease(account_id, owner, lease_until)`; one holder per account because two clients on one auth key give `AUTH_KEY_DUPLICATED` (T1 5.2). Heartbeat every 10–15 s (pick). Scale means more accounts, never more holders per account.
- **provisioning is human**: SIM, login code, 2FA; the console takes the code into the vault; no worker receives it.
- **provider routes** (Apify, Bright Data): the work item is a provider job: `submit → poll → fetch dataset → ingest`; `provider_run_id` is stored, so a restart resumes polling instead of paying again. Apify exposes `status`, `defaultDatasetId` and `usageTotalUsd` ("what you actually pay") on the run [apify-run].
- **official quotas** (YouTube units per day reset at midnight PT, Threads queries per user per 24 h, Instagram hashtags 30 per 7 days, X credits): `quota_ledger(provider_account_id, quota_key, window_start, used, limit)`; a claim checks `used + estimate ≤ limit`, else `not_before = window_end`.

### 7.5 Render tier (W7)

- a separate container and role, no secrets, no route to internal ranges, request routing that blocks images, fonts and analytics, hard per-page timeout (T3 2.4).
- it claims only `route = render` items with the **same claim protocol and the same host gate**, so a rendered page counts against the host's delay; page sub-requests are not paced individually, so the budget is per page.
- hand-off: a static fetch that detects a shell ends `render-required`; if `source.render ≠ never` the item is re-queued with `route = render` and `attempts` kept; otherwise it is the outcome.
- 1–2 contexts per worker, fresh context per page, no persisted cookies; the memory and seconds per page are unmeasured (T3 spike).
- scaled on its own; a browser crash cannot take fetch workers down.

### 7.6 Horizontal scale and recovery

- API and workers are stateless; every coordination fact lives in PostgreSQL.
- **leases** replace boot-time "interrupt everything": a work item and a run hold `lease_until` (2 min default, renewed by heartbeat); a reaper in each worker loop requeues `running` items whose lease expired (`attempts + 1`) and marks a run `interrupted` (`lease-expired`) when its planner also vanished.
- after a restart the **frontier is intact**: queued items stay queued, expired leases requeue, and a `continuation` run resumes the pass. LS restarts a pass from scratch.
- graceful stop: finish or release items (`state = queued`), keep the run `running` until its lease lapses or mark `interrupted` explicitly.
- no transaction spans network I/O; every claim and completion is short.
- duplicate scheduler inserts are harmless (`UNIQUE (pipeline_id, kind, scheduled_for)`).
- connection pool sized for claims plus one `LISTEN` connection per `api` replica.
- throughput limits of one PostgreSQL for this queue are unmeasured (U); the expected load is hundreds of pipelines and thousands of items per hour.

### 7.7 Live progress to the console

- keep LS's contract: events carry the full row and a monotonic `revision`; clients merge by id and ignore lower revisions; after (re)connect they re-read over HTTP; they poll every 5 s while offline (`ls` architecture § Realtime).
- LS's SignalR hub is single-host. Several `api` replicas need a backplane, and Redis is outside "PostgreSQL by convention". Use **`NOTIFY`**: after a persisted change, `NOTIFY run_changed, '{id,revision}'`; each `api` replica `LISTEN`s, loads the row, pushes to its SignalR clients.
- facts [pg-notify]: payload must be under 8000 bytes (send ids, not rows); delivery happens at commit; identical payloads in one transaction fold to one; the page does not say what a dropped listener misses, so every client re-reads on reconnect anyway (U for loss semantics).
- throttle: at most one broadcast per run per second; item-level counters batch.
- event kinds: `RunChanged`, `PipelineChanged`, `HostChanged` (throttled), `AccountChanged`, `SubscriptionChanged`, `QueueDepth`.

---

## 8 · Budgets and cost

### 8.1 What is metered

| Meter | Source | Billed by |
|---|---|---|
| provider results / events | Apify (`usageTotalUsd`), Bright Data, EnsembleData | the run's billed usage; list prices only as estimates (T2: vendor pages contradict) |
| official pay-per-use | X ($0.005 per post read), others | per resource returned |
| LLM tokens | AI gateway (T6) | tokens × price at call time |
| render and fetch | internal | seconds and bytes (informational, not USD in v1) |
| WhatsApp service messages | Cloud API | free up to 1,000 per number per month (T1) |

- `usage(run_id, work_item_id, pipeline_id, tenant_id, subscription_id?, provider_account_id, meter, units, usd_estimated, usd_billed, source)`; `source` = `provider-reported` · `estimate`.
- a price table with `last_checked` backs estimates (T2); billed usage overwrites the estimate when known.

### 8.2 Caps

| Scope | Soft | Hard | On hard stop |
|---|---|---|---|
| run | | `maxUsd` | run ends `partial`, `budget-hard` |
| pipeline, per month | 80% → console flag + `pipeline.health` event (S7) | 100% | pipeline `paused (budget-hard)`; the current unit finishes |
| provider account, per month (global) | 80% | 100% | every pipeline on that route falls down its ladder or pauses |
| tenant, per month (provided form, S3) | 80% | 100% | new paid work for the tenant stops; free routes continue |
| subscription AI, per month | 80% | 100% | `extraction-skipped (budget)`; captures still deliver |
| global | | operator cap | emergency stop |

- **reserve then settle**: before a paid unit, one transaction increments `reserved` on every applicable cap only if `spent + reserved + estimate ≤ hard`; after completion it settles to `usd_billed` or the estimate. Parallel workers cannot overspend; an unsettled reservation expires with the lease.
- period = calendar month UTC; a budget-paused pipeline resumes at the next period unless `stay-paused`.
- soft = warn only (S7); the optional "stretch the interval when soft" degrade is not in v1.
- fallback order on `budget-exceeded`: next enabled route in the ladder that is free or within cap and whose posture allows it; never a route that is `enabled = false`.
- a billed total posted after the run finishes (provider usage lags) is reconciled by `maintenance` daily; the console shows estimate vs billed.
- the AI hard stop degrades to capture-only: "Harvest always delivers captures".

---

## 9 · Tenancy and auth

### 9.1 Tenants, keys, containers

- **tenant** = a consuming service (T4-9: Events, Haven, the ListingShelf view). Ocharo never calls Harvest.
- **API keys** until Identity lands (H3): the SDK's `Identity/ApiKeys` module — keys minted as `{marker}` + 32 characters, stored as SHA-256 hash and prefix, shown once, scopes per key, `RequireApiKeyScope`, last-use touch. `IApiKeyRepository` is product-owned, so Harvest adds `tenant_id`, `expires_at`, `rotated_from`.
- scopes: `pipelines:read` · `pipelines:run` · `pipelines:manage` · `subscriptions:manage` · `events:read` · `links:submit` · `entries:write` · `posts:read`.
- later: OIDC client credentials (M10), audience `harvest`, `client_id` = tenant, `act` = actor (M11, P2). Scope names carry over.
- per-key rate limits through the SDK's `Web/RateLimit` (`PartitionBy` `Tenant` / `User` / `Ip`).
- **isolation**: every tenant-owned table carries `tenant_id`; the SDK's `Tenancy/PerRow` stamps rows (`TenantStampInterceptor`) and `TenantModelBuilderExtensions` adds a global query filter. Public rows have `tenant_id = NULL` and a `public` container; tenants read them, only workers write them.
- defense in depth: an architecture test that every `tenant_id` table has the filter now; PostgreSQL row-level security later (T7-P15).
- **console auth** before Identity: an operator key plus a same-origin guard. ListingShelf's "public hosting needs an authenticated boundary first" holds (`ls` architecture § Boundaries).

| Entity | Public container | Private container |
|---|---|---|
| pipelines, captures, posts | read by all tenants (`pool_shareable` routes only) | owning tenant only |
| subscriptions, events, deliveries | never | owning tenant |
| keys, quotas, budgets | operator | tenant admin sees own |
| accounts, provider accounts (platform-owned) | operator only | tenant-owned ones: that tenant |
| manual entries | never | owning tenant |

### 9.2 Provider credentials by form (S3)

| Form | Whose credentials | Budget |
|---|---|---|
| 3 · provided (WoW2 instance) | WoW2-owned provider accounts; a tenant may bring its own for a private pipeline | per-consumer monthly cap plus the global provider cap |
| 2 · self-hosted | the operator's, which makes the operator the only tenant | the operator's caps |
| 1 · library | the host product's | the host's |

- Meta app review is per app and per owner, so a self-hosted Harvest cannot use WoW2's approved Meta or Threads app (T2): credentials are per tenant there, and the console needs a "bring your own provider account" flow.
- **route resolution**: for a pipeline in container C of tenant T, each ladder entry resolves to a `provider_account`: T's own, else a platform-owned one if `tenant.platform_credentials_allowed` and the route allows sharing, else `not-approved`.
- **`pool_shareable`** is a property of the route: a route using a tenant's Meta token produces posts that stay in that tenant's container; Meta Platform Terms §3.c restrict sharing Platform Data, and T2 asks for a legal read before a provided service serves Meta data to other apps. Route B providers and Meta API routes default to `false`.
- secrets: `provider_account.secret_ref` points to Secrets Vault (envelope encryption, T1 5.2); workers read it at claim, keep it in memory, never in captures, logs, exports or events.

### 9.3 Connection references (T4-4)

- `connection(id, tenant_id, kind, ref, state, verified_at, expires_at)`; a pipeline may carry `connection_ref`.
- `ref` is an opaque id resolved at run time through the **connectors domain's read broker** (T4 § 9, P1): Harvest never stores a token or session.
- rules: private containers only; never pooled; never shared across tenants; a pipeline with a connection is invisible to join lookups.
- states mirror the connectors domain: `valid` · `expired` · `needs-reauth`; a bad state ends runs with `connection-invalid` and sends `pipeline.health` to the owner.
- example: Ocharo Sourcing's signed-in Alibaba RFQ inbox and Gmail (T4 § 3). Whether Harvest performs signed-in browsing at all is a T3/T8 decision; T7 only provides the model (T7-P17).
- platform-owned accounts (the Telegram pool) are a different thing: Harvest-operated, in the `account` table, never exposed to a tenant.

---

## 10 · The console

| Screen | Shows | Actions | Live |
|---|---|---|---|
| Overview | queue depth by host; runs running and failed in 24 h; budget burn; unhealthy accounts; failing endpoints; open review items | jump to the culprit | yes |
| Pipelines | list by container, source, kind, state, schedules, last run, `next_due_at`, subscribers, budget %, posture tag; detail: **requested vs effective** config per subscriber, frontier size, recent runs | run now per kind, pause / resume, pin, archive, edit within policy | yes |
| Runs | list; detail: steps with progress, counts, outcome histogram, ≤ 100 errors, cost, lease holder, timeline | cancel, retry as continuation | yes |
| Captures and posts | browse by pipeline, source, URL; capture history with content-hash diffs; link states; manual entries marked; raw HTML inert and on demand (LS shelf) | open, copy link | no |
| Queue and hosts | per host: queued, running, deferred, `next_allowed_at`, delay, failures, pause reason, robots cache, permission | pause host, clear pause, reprioritize, set egress | yes (throttled) |
| Sources | registry: adapter, route ladder with health, `permission`, `ai_allowed`, `pool_shareable`, `render`, retention class, terms version read | approve `restricted` → `granted`, enable or disable a route | no |
| Accounts and providers | pool: state, `flood_until`, memberships, joined count / cap, lease holder; providers: balance, quota ledger, token expiry, review status | quarantine, take a login code, approve a join | yes |
| Budgets | cap hierarchy with spent / reserved / soft / hard; per pipeline, provider, tenant, subscription AI; price table with `last_checked`; estimate vs billed | edit caps, stay-paused, resume | yes |
| Subscriptions and deliveries | per tenant: kind, rules, mode, endpoint health, lag (position − acked), attempts, dead letters | redrive, resync, rotate secret, send a test event, suspend | yes |
| Review queues | proposals; approvals (restricted source, join, paid route); `needs-manual` links; low-confidence items (T6); `suspect` gone (T5); `unrecognized` pages with sample; consent and deletion requests (T1-P9) | approve, reject, merge, open entry form | yes |
| Tenants and keys | tenants, keys (prefix, scopes, last used), quotas, containers, retention | mint, rotate, revoke | no |
| Settings | host defaults, windows, retention, price table, the identification page text and contact (W14) | edit | no |

- a tenant admin sees only own containers, their subscriptions, and public pipelines they joined; cost internals show as their share.
- built on the fe SDK as ListingShelf's console is (Vue 3, query client, SignalR merge by revision); placement is T8.

---

## 11 · Configuration that waits on lead-document Points

The lead document's open policy Points must not block the design. Each is a configuration value with a conservative default.

| Config | Default | Waits on |
|---|---|---|
| `route.enabled` for Route B providers (Instagram, Facebook, TikTok) | `false`; pipelines created `pending-approval`, outcome `not-approved` | P3 posture, P4 licensed providers (S1, S8) |
| `source.ai_allowed` | `false` for Telegram; `true` elsewhere unless `ai-input=no` (W5) | P3 (T1-P1) |
| `route.pool_shareable` | `false` for Route B and Meta API routes; `true` for open fetch and own feeds | P3, T2 legal read |
| `source.permission` | `open`; Afisha `restricted` | W1 / P7 |
| `telegram.account_pool.enabled`, `max_accounts` | `false`, 0; route `W` (web preview) enabled, route `M` off | P5, P8 (T1-P2, T1-P3) |
| `tenant.platform_credentials_allowed` | `false` | P8 credential owner |
| `whatsapp.intake.enabled` | `false` | P6 (T1-P7, T1-P14) |
| `search` adapter family | not shipped | P9 |
| `render.enabled` | `false` until the W7 spike | W7 |
| `source.egress` | none (direct) | W8 |
| first public pipelines | mstar.uz, voyage.uz `active`; Afisha `pending-approval`; iticket `proposed` | P7 (W1, W2) |

---

## Findings that change the spec

- **Split the spec's "pipeline".** § Concepts defines it as "a consumer's standing request". Developer decisions of 2026-10-26 make it shared, so pipeline (the unit of harvesting) and subscription (the unit of consumption, with its own delivery, schema, AI flag and budget share) are separate; the effective config is derived.
- **Add tenant, container, API key, subscription, event, host state, account lease, quota and usage ledgers** to the spec; none exists today. Key and tenant isolation reuse the SDK's `ApiKeys` and `Tenancy/PerRow`.
- **Claim work by host, not by run.** LS claims whole runs and both prior systems interrupt every `Running` run at boot; neither survives a second worker. The frontier doubles as the queue (`FOR UPDATE SKIP LOCKED`), leases replace boot-time recovery, results are fenced, and a restart resumes instead of rerunning.
- **Politeness and flood waits live in state, not in the run.** LS pauses 500 ms run-wide and ends the run on the first 429; T3 and T1 need `host_state` with `Retry-After`, challenge backoff and per-`(account, method)` buckets, and a block on one host must not stop work on others.
- **One durable event log per subscription serves webhooks, pull cursors, replay and dead letters.** The be SDK's webhook publisher retries inline (3 attempts, 30 s ceiling) and logs terminal outcomes only, which is not at-least-once; a durable dispatcher belongs in the SDK because Identity's webhooks need it too.
- **Delivery contract**: Standard Webhooks signing, 11 attempts over ~72 h, `410` suspends, per-post revision for ordering, `event_id` + `item_id`, `Idempotency-Key` on writes, and an `xid8` horizon cursor so a poller never skips a late-committing row. Events' intake gains `revision`, `supersedes`, `context`, `link.state`, `pipeline.run`, and an optional `extracted`.
- **Run status gates deletion inference.** Only a `completed` run after a complete enumeration may produce `suspect` or a "verified" watermark; `partial` and `failed` runs are "unchecked". `pipeline.run{complete}` lets consumers tell "nothing new" from "unchecked".
- **Outcomes need three levels** (run reason, source or fetch outcome, item outcome) plus persistent account states; LS's single `CompletionReason` mixes them.
- **Tag and keyword readers depend on someone harvesting.** They are weak references that keep no pipeline alive; operator-`pinned` public pipelines seed the pool. A keyword proposes, an approver creates.
- **Link intake**: the container decides visibility, the host decides pacing. A URL outside every public pipeline's scope stays private but uses the shared host limiter; submissions carry per-tenant quotas; captures are never promoted to public.
- **Budgets use reserve-then-settle** against run, pipeline, provider, tenant, subscription-AI and global caps; billed usage replaces estimates; an AI hard stop degrades to capture-only.
- **Live progress without Redis**: `NOTIFY` with ids plus a re-read, so several `api` replicas share one SignalR experience.
- **Credentials**: `pool_shareable` per route, per-tenant provider accounts, connection references resolved through the connectors domain; Harvest holds no token.

---

## Points

- [ ] T7-P1 pipeline identity and join: `(container, source, scope_key)`, whole-site singleton per source, filtered joins on identical `scope_key` only → provisional pick: as stated.
- [ ] T7-P2 subscriber schedule input: max staleness, not cron, on public pipelines; operator owns windows → provisional pick: staleness merged by min and clamped; cron stays on private and operator pipelines.
- [ ] T7-P3 who may create public pipelines → provisional pick: any tenant with `pipelines:manage` may create when the source is `open`, free-route and within quota; anything gated (permission, account, paid route, new source family) is `pending-approval` for the operator.
- [ ] T7-P4 cost attribution → provisional pick: equal split among channel subscribers against tenant caps, AI to the asking subscription, hard stops never on shares; marginal view console-only.
- [ ] T7-P5 idle pipelines → provisional pick: pause when the last channel subscriber leaves unless `pinned`; weak readers keep nothing alive; archive after 30 days idle.
- [ ] T7-P6 backfill on join → provisional pick: replay current live posts through the event log, throttled; `join` run only when stale; no AI on history without opt-in.
- [ ] T7-P7 delivery unit for channel subscriptions: canonical post revision with `links[]` filtered to what the subscriber may see → provisional pick: as stated (T5 confirms the post and link model).
- [ ] T7-P8 event retention and retry horizon, batching → provisional pick: log 30 days, 11 attempts over ~72 h, `410` suspends, one event per request in v1.
- [ ] T7-P9 durable webhook dispatcher placement → provisional pick: in the be SDK (Identity needs it); Harvest consumes it (T8).
- [ ] T7-P10 adaptive schedules → provisional pick: ship `manual`, `interval`, `cron` first; `adaptive` (halve / double between bounds) in the second slice.
- [ ] T7-P11 match engine inputs → provisional pick: match on T6's normalized `search_text` (script folding, language tag); no Uzbek stemming in v1; T6 owns the shape.
- [ ] T7-P12 proposals → provisional pick: sources are link submissions on unharvested domains and keyword coverage gaps; `search` candidates later (T4-3, P9).
- [ ] T7-P13 link scope matching → provisional pick: registrable domain + path scope; in-scope → public; out-of-scope on a public domain → private with the shared host limiter; per-tenant daily quota (T5 for cross-container linking).
- [ ] T7-P14 manual entries → provisional pick: private container only, new revision per edit, `provenance: manual` set server-side; Harvest checks key scope and records the actor, the product checks roles (T4-10).
- [ ] T7-P15 tenant isolation → provisional pick: SDK per-row filter plus an architecture test now; PostgreSQL row-level security later; operator key plus same-origin guard for the console until Identity lands.
- [ ] T7-P16 `NOTIFY` as the console backplane and long-poll wake-up → provisional pick: yes; Redis stays out (T8).
- [ ] T7-P17 signed-in sources (T4-4) → provisional pick: `connection_ref` resolved through the connectors domain, private containers only; whether Harvest drives signed-in sessions at all waits for T3 and T8.
- [ ] T7-P18 flood-wait handling → provisional pick: confirm T1-P5 (sticky, no failover on waits, library auto-retry off); verify the `WTelegramClient` setting in a spike (T1).
- [ ] T7-P19 cursor type → provisional pick: `(xid8, id)` with the `pg_snapshot_xmin` horizon; fall back to a per-subscription counter if `xid8` row comparison does not index (U).
- [ ] T7-P20 deletion-check schedules per route → provisional pick: T7 owns the `check` schedule row, `maxProbes` and the "complete enumeration" gate; T5 owns the probe method; T2 S5 sets provider cadence (weekly newest-30-days re-scrape).

---

## Sources

Read 2026-10-26.

- [pg-select] https://www.postgresql.org/docs/current/sql-select.html — `SKIP LOCKED`: inconsistent view, "queue-like table" use; `LIMIT` locks only returned rows
- [pg-notify] https://www.postgresql.org/docs/current/sql-notify.html — payload under 8000 bytes, delivery at commit, folding of identical payloads, queue full fails commits
- [pg-functions] https://www.postgresql.org/docs/current/functions-info.html — `pg_current_xact_id`, `pg_current_snapshot`, `pg_snapshot_xmin`, `xid8` has no wraparound
- [dudycz] https://event-driven.io/en/ordering_in_postgres_outbox/ — `xid8` column, `pg_snapshot_xmin` bound, order by transaction id then position
- [cloudscale] https://www.cloudscale.ch/en/engineering-blog/2025/10/09/generating-truly-sequential-ids-in-postgresql — sequence values assigned before commit; a poller can skip a late row (search result)
- [standard-webhooks] https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md — headers, signing, retry over days, `410`, `Retry-After`, `webhook-id` idempotency (read through a fetch summary; exact retry numbers U)
- [apify-run] https://docs.apify.com/api/v2/actor-run-get — run object fields `usageTotalUsd`, `defaultDatasetId`, `chargedEventCounts` (first 100,000 of ~216,000 characters read)
- PostgreSQL built-in text search configurations: https://www.postgresql.org/docs/current/textsearch-configuration.html — page lists no configurations; Uzbek absence not confirmed (U)

Workspace

- `ls` `ListingShelf.Domain/Pipelines/Entities/PipelineEntity.cs` · `Runs/Entities/RunEntity.cs` · `Runs/Enums/*` (`CompletionReason`, `RunStatus`, `RunStage`, `RunTrigger`, `StepKey`, `StepStatus`) · `ListingShelf.Infrastructure/Runs/BackgroundServices/RunQueueBackgroundService.cs` · `OrchestrationServices/RunExecutionService.cs` · `Settings/RunExecutionSettings.cs` · `ListingShelf.Persistence/Repositories/RunRepository.cs` · `engineering/architecture/architecture.md` · `pipeline-contract.md`
- `hv` `Haven.Supply.Infrastructure/Pipelines/Engine/*` (`PipelineRunner`, `PipelineRunContext`, `PipelineActiveRun`, `PipelineCatalog`) · `BackgroundServices/PipelineSchedulerBackgroundService.cs`, `PipelineRecoveryService.cs` · `Settings/PipelineSchedulerSettings.cs` · `Haven.Supply.Domain/Pipelines/*` · `Intake/Pipelines/ListingIntakePipeline.cs`
- `be` `Messaging/Webhooks/*` (`WebhookPublisher`, `Issuers/StandardWebhookSignatureIssuer`, `Persistence/*`, `Inbound/*`, `Webhooks.spec.md`) · `Messaging/Reliability/Ef/PostgresSkipLockedOutboxClaimRepository.cs`, `Ef.md` · `Identity/ApiKeys/api-keys.md` · `Tenancy/PerRow/*` · `Web/RateLimit/*` · `Foundation/Time/Parsers/ICronExpressionParser.cs`
- [harvest-service-spec.md](../harvest-service-spec.md) · [events-service-spec.md](../events-service-spec.md) § Harvest seam · [analysis index](harvest-analysis-2026-10.md) · [T1](t1-messaging-sources.md) · [T2](t2-social-sources.md) · [T3](t3-web-sources.md) · [T4](t4-consumers-and-social.md) · [identity T4](../identity-analysis-2026-10/t4-integration-modes.md) (M10, M11, M13)
