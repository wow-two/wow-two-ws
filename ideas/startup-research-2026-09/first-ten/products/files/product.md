# Arrival — expected partner-file arrivals

W0031 · first-ten order 3 · proposed $39/month · research and clickable prototype, not a live monitor.

## Decision and product philosophy

Test a file-arrival calendar for a small integration team receiving predictable daily files from outside partners. The buyer is the integration or operations lead; the user is the operator answering “which partner file is missing, and was it actually expected today?” The core object is one expected occurrence for one feed and business date. The human decides whether a partner-confirmed exception is legitimate and whether a late file needs escalation.

The promise is an accurate list of expected arrivals. Automation compares schedule, receipt metadata and grace period; it does not infer a holiday, read remote files, contact partners, or repair data. Quiet means no message for on-time receipts, no repeated alert for the same late occurrence, and no alert for an approved exception. A late arrival resolves the incident but retains evidence that the deadline was missed.

## Market challenge and first paid test

[Healthchecks.io](https://healthchecks.io/pricing/) lists 20 monitored jobs free and 100 jobs at $20/month, or $192/year. [Its documentation](https://healthchecks.io/docs/) describes HTTP pings, silence while healthy, and grace periods. A `file-stat` script plus this service is a strong direct substitute. The proposed $39 offer must earn its premium through partner-specific expected dates, exception context and a shared operator handoff. Filename validation alone is insufficient differentiation.

This is supplier evidence, not evidence that a customer wants Arrival. Test with five operators who already maintain file expectations in spreadsheets or tickets. Replay two months of metadata before live alerting; ask for two $39 paid pilots only after the replay demonstrates useful missed-arrival detection and understandable exceptions. Kill or narrow the idea if scripts are sufficient, if partner calendars cannot be obtained reliably, or false alerts exceed one per feed per week after calibration. A published metadata-only collector and an integration-specific calendar template are acquisition hypotheses; no channel is validated.

## Core journey and boundaries

1. Define a feed: friendly partner name, expected filename rule, daily UTC arrival, grace period and responsible operator. Empty onboarding requests one feed and displays its next expected occurrence.
2. Run the collector inside the customer's environment. It checks local filesystem or customer-managed transfer completion, then emits only allowed metadata.
3. Review the day as a timetable. The operator can distinguish expected, within grace, late, received and calendar exception without opening a chart.
4. Inspect a late feed's expected filename, deadline and latest receipt. Record a partner-confirmed exception with a reason, or wait for a genuine receipt.
5. A late receipt changes current state to received while preserving arrival time and lateness. Export the day with exceptions and receipt evidence for a handoff.

MVP: daily UTC schedules, explicit per-date exceptions, one metadata ingestion path, bounded filename and positive row count, grace period, one email digest, history/export. Non-goals: remote SFTP credentials, hosted polling, payload storage, schema validation, orchestration, partner messaging, transfers, compliance guarantees, subminute alert SLA or automatic repair. Time zones, DST and recurring holiday calendars are a paid-pilot extension after the UTC model proves useful, not silently supported in the mock.

Failure states: collector stale must differ from partner late; invalid receipt is rejected with a reason; malformed filenames cannot satisfy an occurrence; a feed with no initial receipt is explicitly unverified. Conflict states: duplicates return the existing receipt; a receipt arriving during exception creation returns a reviewable conflict rather than erasing evidence. An exception cannot be added to an already received occurrence in the narrow UI. Removing an exception immediately restores schedule evaluation.

## Domain model and invariants

| Entity             | Required content                                                            | Invariant                                                                           |
| ------------------ | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Feed               | Project, partner label, filename rule, UTC schedule, grace                  | Rule version is attached to each occurrence                                         |
| ExpectedOccurrence | Feed, expected business date, due instant, grace deadline                   | Unique per feed/date; absence of telemetry is not a successful receipt              |
| Receipt            | Collector event ID, occurrence date, filename metadata, rows, observed time | One accepted receipt version per occurrence in MVP; replays cannot increment counts |
| CalendarException  | Feed/date, reason, author, version                                          | Explicit human decision; removes expectation without fabricating receipt            |
| CollectorHeartbeat | Collector ID and last healthy timestamp                                     | Collector failure is reported independently of partner lateness                     |
| Incident           | Occurrence, opened/resolved times, delivery status                          | At most one active late incident per occurrence                                     |

An on-time receipt remains on time regardless of when the UI is loaded. Late means current time is strictly after `due + grace` for an occurrence with no receipt or exception. Received counts exclude exceptions; expected denominator excludes them too. Zero-row files require a feed policy in production; the narrow prototype explicitly requires a positive whole count. Store both customer-observed and server-received times and flag suspicious clock skew. Never accept an arbitrary client timestamp as proof of timeliness.

## Proposed API, jobs and reliability

These are new product contracts, not existing SDK endpoints:

| Route                                            | Behavior and authorization                             |
| ------------------------------------------------ | ------------------------------------------------------ |
| `POST /api/projects/{id}/feeds`                  | Editor creates a versioned daily UTC schedule          |
| `POST /api/collectors/{id}/receipts`             | Feed-scoped ingest credential submits bounded metadata |
| `POST /api/collectors/{id}/heartbeat`            | Scoped collector health signal, separate from receipt  |
| `GET /api/projects/{id}/calendar?date=...`       | Tenant member reads occurrences and status             |
| `PUT /api/feeds/{id}/exceptions/{date}`          | Editor supplies reason and expected occurrence version |
| `DELETE /api/feeds/{id}/exceptions/{date}`       | Editor removes exception with version guard            |
| `GET /api/projects/{id}/exports?from=...&to=...` | Tenant member exports bounded date range               |

Receipt idempotency uses `(collectorId,eventId)` with a body digest. Identical retry is success; conflicting retry is `409`. The occurrence key is a separate uniqueness constraint so different event IDs cannot inflate a count. Ingestion and incident transition commit together. Proposed events: `ReceiptAccepted`, `OccurrenceBecameLate`, `LateReceiptArrived`, `ExceptionAdded`, `ExceptionRemoved`, `CollectorStale`.

The scheduler materializes upcoming occurrences, evaluates deadlines once per minute and catches up from persisted deadlines after restart. A persisted outbox deduplicates delivery by incident and transition. A separate retention job prunes bounded raw events after 30 days. Using an ASP.NET Core hosted worker is technically supported; application-owned persistence, leases and retries are still required. [Microsoft hosted-service documentation](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/host/hosted-services?view=aspnetcore-10.0). No Redis, Kafka or separate scheduler service is necessary for the pilot.

## Data ownership and security

Files, access credentials and parsing compute stay with the customer. Collect only a feed alias, expected date, safe filename or filename alias, row count, size if necessary and completion timestamps. Filenames can contain customer identifiers: allow local aliasing and forbid raw paths by default. Do not accept file contents, host paths or transfer credentials. Project-scoped tokens can append metadata but cannot read another project's history; rate limits and rotation constrain spoofing. Server-derived tenant filters govern every query. Exception edits require user identity and create an audit entry.

An operator export belongs to the customer. Offer account deletion and documented backup retention; deletion and restore are production acceptance tasks. The prototype has only browser-local synthetic receipts and no file-upload control. No monitoring, alerting or partner contact occurs.

## Vue, .NET and SDK boundaries

Vue handles date/feed selection, derived states, metadata forms and inspection. .NET handles canonical schedule rules, ingestion, tenant authorization, incidents and durable jobs. Keep `Feed`, `ExpectedOccurrence` and evaluator rules in the product domain, separate from transport adapters. The collector is an independent customer-run executable or script with a versioned JSON schema; it must not depend on the frontend SDK.

The inspected public `@wow-two-beta/ui-vue` 0.0.7 declarations export `Button`, `Timeline`, `TimelineItem`, `DateInput` and `Modal`. These are possible production control mappings, not proof that a partner-calendar workflow exists. The prototype intentionally composes native controls and a lightweight timetable. Validate component props and interaction fit in a spike before using these exports. WoW2 backend authentication, persistence and scheduling integration must use verified exports from the selected production repo; none are invented in this document.

## Price, costs and validation gates

Proposed free: two feeds and a local collector. Proposed $39/month organization subscription: 20 feeds, exception history, operator context and 30-day metadata retention; cap ingestion at 50,000 events/month. Do not promise lifetime hosted monitoring. An offline local calendar export could become a separately priced product if customers reject hosted metadata.

Early budget estimate: $20–35/month across app/database allocation ($12–20), backups ($4–6), domain and capped delivery ($4–9). This is a planning allowance, not a quote, and excludes founder labor, taxes, payment fees and customer-side collection. Central payload storage, SFTP polling, SMS and AI are deliberately outside the budget design. Keep UTC evaluation bounded by the paid feed quota. Expand toward $300/month only after earned revenue and measured event volume justify it; additional delivery channels require explicit caps.

Activation means one accurately diagnosed missed occurrence plus one acknowledged calendar exception in the customer's own history. Retention means two subsequent partner cycles with useful operator decisions and tolerable alert precision, not simply a connected collector. At $39/month, 129 organizations yield $5,031 gross MRR before fees, taxes, refunds or churn. Customer acquisition and retention sufficient to reach that count remain unproven.

## Design references and interaction rationale

The [Healthchecks documentation](https://healthchecks.io/docs/) supplies the conceptual separation between schedule, grace period, healthy signal and missed signal. Our “Within grace” terminology avoids calling an allowed delay an incident. This was a textual documentation inspection; no live dashboard visual audit is claimed. The timetable and date strip are original composition choices for the operator's calendar question. [MDN's native dialog guidance](https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement/showModal) supports a focused form with an inert background while an exception is being recorded.

Screens: selected-day timetable; feed receipt/late detail; receipt simulation form; calendar exception form; future day with upcoming expectations. The selected feed stays stable when changing dates, so an operator can inspect one partner across the week. At 390 px the timetable precedes detail; at 768 px detail occupies a second column. Every status has a word label, and all times explicitly use UTC. The five-day strip is deliberately bounded in this research mock; a production range navigator is later work.

| Semantic token              | Light mapping                           | Dark mapping                             |
| --------------------------- | --------------------------------------- | ---------------------------------------- |
| `--canvas`, `--surface`     | Quiet background, calendar surfaces     | Low-glare background, elevated surfaces  |
| `--accent`, `--accent-soft` | Selected date/feed and timetable marker | Same meaning, contrast-adjusted by shell |
| `--warning`                 | Waiting within grace                    | Same state; not an incident              |
| `--danger`, `--success`     | Late / received                         | Same meanings with text labels           |
| `--muted`, `--line`         | Partner context, timetable structure    | Readable secondary text and separators   |

Proposed reusable controls: expected-occurrence badge, day strip, receipt summary, exception form and timezone label. Light/dark and the shell's three palette options remain design proposals.

## Staged build and acceptance

1. Replay metadata from five operators using a local evaluator. Prove whether partner exceptions matter enough to pay for.
2. Build a UTC-only collector protocol and local evaluator with tests for exact grace boundaries, duplicates, exceptions and clock skew.
3. Add tenant-scoped ingestion, durable occurrence jobs, one opt-in notification channel and export. Verify restart catch-up, incident deduplication, stale collectors and unauthorized requests.
4. Add billing after paid-pilot acceptance. Extend to IANA time zones and DST only with explicit skipped/repeated-hour policy tests and real customer need.

Production acceptance: received totals derive from accepted occurrences; exception creation cannot erase a concurrent receipt; a collector outage cannot silently impersonate a partner miss; late receipt preserves lateness evidence; replay cannot duplicate alerts; metadata never contains raw file contents; tab/keyboard navigation works at 390/820/1440 px in both themes. Root owns consolidated build and browser evidence; the following steps specify expected mock behavior.

## Exact prototype smoke scenario

Start with the shell's reset for this product.

1. Verify Sep 29 at 12:30 UTC shows 2/5 received, 1 late, and 2 waiting. Warehouse availability is selected.
2. Click **Simulate file receipt**, then **Record simulated receipt** with blank row count. Validation leaves the dialog open.
3. Keep `inventory_2026-09-29.csv`, enter `1248`, and click **Record simulated receipt**. Counts become 3/5 received, 0 late, 2 waiting. Detail explicitly says it arrived after grace.
4. Select **Regional price book**, click **Add calendar exception**, enter `Partner confirmed no price feed today`, and click **Save calendar exception**. Counts become 3/4 received, 0 late, 1 waiting.
5. Click **Remove exception**. Expected count returns to 5 and waiting becomes 2.
6. Click **Advance 30 minutes** twice. At 13:30 UTC, Wholesale orders is late; late count becomes 1.
7. Select **Thu Oct 01**. The predefined price-book exception makes the expected denominator 4 and late count 0.
8. Click **Export arrival calendar**. The JSON includes the 1,248-row inventory receipt and the current simulation clock.
9. Refresh and reselect Sep 29; receipts and clock persist. Reset restores the initial sample.

Implemented mutations: simulated receipt, exception addition/removal and clock advance. Details, form validation, metadata export, derived counts and persistence are functional locally. Collector execution, network monitoring, timezone rules beyond UTC, notifications and billing remain unimplemented.
