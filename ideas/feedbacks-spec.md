# Feedbacks — Incident Reports & User Feedback for the Fleet

*Last updated: 2026-09-29*

> Proposed `wow-two-platform.feedbacks` (working name) — the central inbox every wow-two app's **Report** button
> lands in: incidents grouped into issues, each with the user's trail, the failed request and its trace id, one
> click from the log lines behind it. One-liner: *a self-hosted Sentry for the fleet, user-facing first.*
>
> **Order:** #3 in [platform apps](../docs/platform-apps.md) — after `wheelhouse` ships and `secrets-vault` is
> hardened. Roadmap brick #7 ([platform roadmap](../docs/platform-roadmap.md)); origin vision
> [UX observability](../docs/ux-observability-system.md).

## Problem

- a user hits an error and the app shows a toast; the report path is "write to support, describe what you did".
- support then asks "what were you doing?", and the answer rarely names the request, its trace id or the steps.
- each app's logs live on its own box; nothing joins what the user saw to what the server logged.
- the same failure reported by ten users arrives as ten unrelated messages.

---

## What already exists (client side, 2026-09-29)

- `@wow-two-beta/ui-vue/reporting` — `createReporter` keeps a trail (requests, navigations, clicks, notices,
  uncaught errors) and `capture(error).send()` delivers an `IncidentReport` (schema 1) through a sink.
- one-click UX — a failed query's danger toast carries a **Report** action (`ReportAction`): Report → Sending… →
  Reported · ref `3E4F5A6B`, or Retry; `feedbackQueryErrors(bus, { reporter })` wires every failed query.
- the payload — error (type, code, status, `traceId`, `requestId`, redacted problem details), the matched request
  (method, URL, status, duration), the frozen trail, page, client, user, tags, note, optional screenshot, and a
  `fingerprint` (app · failure kind · code · templated route) for grouping.
- backend SDK — ProblemDetails already carry `traceId` (`Activity.Id`) and `requestId` (`TraceIdentifier`).
- contract reference: `wow-two-sdk-beta.ui` → `src/reporting/Reporting.spec.md`.

---

## Scope v1 — the triage loop

| # | Capability | Detail |
|---|---|---|
| 1 | Ingest API | `POST /v1/reports`, per-app ingest key (`x-ingest-key`), schema 1 validation, size cap, returns `{ id, url }` |
| 2 | Issue grouping | hash of `fingerprint` → issue; event count, users affected, first/last seen, app versions |
| 3 | Inbox | issues by app and status (new · triaged · resolved · ignored), sorted by last seen or count |
| 4 | Issue detail | latest event: error, request, breadcrumb timeline, page, client, note, screenshot; older events listed |
| 5 | Trace link | copy `traceId` / `requestId`; deep link `logs?traceId=` once the log store (#4) exists |
| 6 | Regression | a new event on a resolved issue from a newer app version reopens it |
| 7 | Alerts | Telegram message on a new issue or a regression, per app, opt-in (reuse the comms Telegram slice) |
| 8 | Reference lookup | search by the short ref the user saw (`3E4F5A6B`) or the full report id |

- auth — operator-only: SDK identity (cookie `Mode=Api`) + allowlist, as `wheelhouse` does.
- deploy — through `wheelhouse`; ingest keys and DB credentials in `secrets-vault`.
- stack — .NET 10 backend on the backend SDK + Vue console on `@wow-two-beta/ui-vue`; Postgres; screenshots in
  S3-compatible storage (the SDK storage block), never in the database row.

---

## Data model (Sentry-shaped)

| Entity | Holds |
|---|---|
| `App` | name, environments, ingest keys (hashed), alert settings |
| `Issue` | app, fingerprint hash, title (error message), status, first/last seen, event and user counts, last version |
| `Event` | one `IncidentReport` as received (JSONB) + indexed columns: issue, occurred/reported at, trace id, request id, user id, version |
| `Attachment` | screenshot blob key, media type, size — one per event |
| `Comment` | operator notes on an issue (triage history) |

---

## Client increment 2 — completing the reporting vector (SDK)

From [UX observability](../docs/ux-observability-system.md), not yet in the SDK:

- **session id** — groups every incident of one visit; journey reconstruction across reports.
- **operation context** — operation type id (`invoice.create`) + operation id per user action, carried from the
  trail to the request headers and into the report; the "operation registry" of the origin doc.
- **help routing** — `operationType × errorCode` → help article link beside Report.
- **"add details"** — an optional note field after a one-click send (the API already takes `note`).
- **active feature flags** — the `/flags` evaluation snapshot on the report.
- **offline outbox** — a failed delivery queued in storage and retried on `online`.
- **client dedupe** — one report per fingerprint per window, so a failing loop cannot flood the ingest.
- **server join** — server-side 5xx exceptions arrive via the log store (#4) under the same trace id.

---

## Build vs. wrap

- Sentry self-hosted — the data model to copy, not the thing to run: 20+ containers (Kafka, ClickHouse, Snuba).
- GlitchTip — a lighter Sentry-protocol server; a fallback only, since the client speaks `IncidentReport`, not
  the Sentry envelope, and the in-app trace/log join is the value.
- verdict — **build thin**: ingest + grouping + inbox is a small CRUD surface; the client already exists.

---

## Phasing

- **P0** — ingest API, `App` + ingest keys, events stored, flat list per app. Point one app's `httpReportSink` at it.
- **P1** — issue grouping, inbox, issue detail with trail timeline and screenshot, reference lookup.
- **P2** — status workflow, regressions, Telegram alerts, retention job.
- **P3** — log-store deep links (#4), client increment 2 (session + operation context, help routing, outbox).

---

## Open questions

1. Name — `Feedbacks` is a working name; nautical siblings to `Wheelhouse`: *Flare* (the distress signal a user
   fires), with *Logbook* for logs and *Lookout* for monitoring.
2. Retention — events and screenshots kept how long per app (proposal: 90 days events, 30 days screenshots)?
3. Screenshot capture — which DOM-to-image library the apps standardize on (`modern-screenshot` vs `html-to-image`).
4. Product feedback (feature requests, praise) — same inbox with a `kind`, or a separate surface later?
