# Procedure recertification queue

W0263 · first-ten order 4 · proposed $29/month/team · analysis and local prototype, 2026-09-29.

## Decision, user and job

Test a review register for operations teams whose procedures live across existing documents. The core object is a **review of an identified procedure version**, assigned to a person and ending in a dated attestation or revision. The promise is to make ownership and review evidence visible without migrating the company’s wiki.

[Notion’s wiki and verified-page documentation](https://www.notion.com/help/wikis-and-verified-pages), checked 2026-09-29, explicitly describes page owners, expiring verification and owner notifications. This is direct incumbent overlap, not an uncovered market. Process Street and ordinary calendar/task reminders also compete. A possible narrow advantage is one review campaign across disparate document systems, with a reason for each attestation. That advantage and buyer budget remain unverified.

## Product philosophy

The product should earn trust through an accountable review, never through a decorative verification badge. An owner states which steps still work, what changed, and which version they examined. Automation sorts due records, invalidates outdated attestations, and preserves history. It cannot determine whether a policy is correct, safe or legally sufficient.

Quiet-by-default means no automatic subscriptions, broadcast reminders or guilt-driven activity prompts. Owners explicitly opt into due digests. Completed reviews disappear from the active queue until the next agreed cycle. Never turn a procedure review into a forced daily habit.

## Core journey and edge states

Register a title, source and owner; triage due procedures; open the local excerpt and source reference; start a review; revise if necessary; record concrete evidence and attest the version; inspect history or export the register.

The board distinguishes due, in-review and current records. An empty lane explains that no work is waiting there. New records contain no implied verified excerpt. Invalid or duplicate sources block registration. Attestation requires both source comparison and workflow checks plus a useful note. Revision clears the pending checks and requires renewed attestation. In production, a document hash/version change during review creates a conflict rather than approving the older content. Missing source permission pauses the review without storing a fabricated copy.

## MVP and non-goals

MVP: URL register, named owners, explicit review cadence, review/revision history, version-bound attestation, digest opt-in and export. Links remain external to the register. The prototype uses local synthetic excerpts so the task is inspectable without accessing a private wiki.

No wiki authoring platform, crawler, document ingestion, AI policy writer, compliance certification, employee surveillance or unrequested messages. Mock excerpt revision changes only the prototype, never its displayed source URL.

## Domain and invariants

`Organization`, `ProcedureReference`, `SourceRevision`, `ReviewCycle`, `ReviewAssignment`, `RevisionNote`, `Attestation`, `NotificationPreference`.

- A current attestation identifies reviewer, source version, evidence note, timestamp and expiry.
- A title or badge never establishes source correctness.
- Source revision changes invalidate any in-progress verification checks and prior current status.
- Review history is append-only; reopening does not erase an earlier decision.
- Reassignment requires the new owner to acknowledge responsibility.
- A scheduled review date uses the organization’s defined calendar/timezone; production supports configurable cadence.
- Duplicate canonical source references are detected within a tenant, not across tenants.

## Proposed architecture and API

Vue presents the work queue and focused review desk. .NET application services authorize transitions and calculate the next review. A relational database stores metadata, review evidence and immutable decision events. Source content is optional and explicitly supplied; private document fetching is a later independently authorized connector.

| Proposed endpoint                     | Behavior                                                   |
| ------------------------------------- | ---------------------------------------------------------- |
| `POST /api/procedures`                | Register URL, owner and cadence with idempotency key       |
| `GET /api/reviews?state=due`          | Tenant/assignment-scoped work queue                        |
| `POST /api/procedures/{id}/reviews`   | Start one active cycle for the expected source revision    |
| `POST /api/reviews/{id}/revisions`    | Record changed version and rationale                       |
| `POST /api/reviews/{id}/attestations` | Require reviewed version, evidence and reviewer permission |
| `PATCH /api/procedures/{id}/owner`    | Record ownership change and acknowledgment requirement     |
| `GET /api/procedures/export`          | Owner-authorized register export                           |

Commands use expected versions; stale changes return conflict with the newer record. Idempotency keys scope to organization and command; retries cannot create duplicate cycles or attestations. Events are `ReviewOpened`, `SourceRevisionChanged`, `ProcedureAttested`, `OwnerChanged`. Background jobs open due cycles once and deliver only opted-in digests through an outbox. Failed delivery never marks a review acknowledged.

## Security and ownership

Owners edit assigned reviews; administrators manage registrations and membership; viewers read only permitted procedures. Enforce tenant scope and document-level access on every query and export. URLs can contain sensitive identifiers: validate HTTPS and avoid logging full query strings. Never server-fetch arbitrary registered URLs without SSRF protections and explicit connector scope. Strip unsafe URL schemes, limit excerpts/notes and keep user content escaped. Separate private review notes from exports to broader audiences.

Production retention is configurable, with export/deletion policy and minimal source copies. The browser prototype stores synthetic plaintext JSON locally; it does not enforce identities or actual source permissions. No real internal policies should be pasted into the mock.

## Vue/.NET and shared boundaries

Use Vue 3 for queue filtering, revision editing and review forms; use .NET for authorization, review state and scheduling. Product-owned behavior is the source-version/attestation relationship. Candidate shared components include review board, accessible dialog, owner picker, audit timeline, version-conflict panel and validated form controls. Existing SDK exports must be inspected before implementation; no SDK availability is asserted here. The mock only imports `PrototypeApi` and semantic CSS.

## Pricing, operating cost and paid gate

Propose a free register of five procedures and a $29/month team plan for repeated campaigns, history and ownership. The free boundary should demonstrate the task without requiring a large document migration. It must not encourage unbounded free storage.

Target $20–50/month total pre-revenue infrastructure through metadata-only storage, local excerpts, bounded records and capped explicitly requested digests. No AI/API spend is required. The ceiling is a design constraint, not a quote or operating result. Track onboarding/review support separately. Consider approximately $300/month only when paying teams demonstrate repeat value and contribution finances a measured bottleneck.

Activation: an owner identifies one meaningful discrepancy and completes a versioned review. Retention: another review cycle occurs without founder chasing. Pilot 30 procedures across five teams. Stop if reviews become blind checkbox acknowledgments, existing Notion/Process Street workflows suffice, or fewer than two teams pay for a second cycle.

## Design analysis

The Notion help page supplies documented interaction references: “pages I own,” explicit verification expiry, and ownership. These are conceptual/documentation observations rather than a visual teardown of its current app. Extract ownership and dated verification; do not copy the badge as a claim of truth.

The recommended composition is a small review board beside a reading desk. Cards answer what needs review; the desk shows the version and evidence needed for a decision. A three-state board is a workflow view, not a productivity scorecard. Shared canvas variants remain proposals, not approved design locks.

Use `--surface` for cards, `--surface-alt` for the excerpt, `--accent` for the selected record and `--accent-soft` where contextual selection is needed. Warning/success badges retain explicit state labels in both themes. The board and detail stack below 1024px; lanes become a vertical list below 768px. Native checkboxes, labeled fields, focusable cards and dialogs support keyboard completion. Candidate reusable patterns are a version-bound review form and a history disclosure.

## Acceptance and staged build

First validate review quality using existing links and a manual register. Next implement versioned transitions and conflict tests, then tenant permissions and source access boundaries. Add scheduling and opted-in notification only after a recurring review habit is observed. Source connectors are a later separate investment.

Acceptance requires failed attestation without evidence, revision invalidation, preserved prior history, correct next date, duplicate-source handling, scoped exports, no source mutation and readable states at 390/820/1440px in both themes.

## Mock coverage and ordered smoke test

After shell reset:

1. **Client launch handoff** starts due, version 3. Click **Start review**: its card moves to In review.
2. Click **Attest current version** without checks or evidence: inline validation blocks it.
3. Click **Revise excerpt**, add an explicit access-expiry check, explain the change, then **Save revision**: version becomes 4; status stays In review.
4. Check both review statements and enter a concrete evidence note. Click **Attest current version**: it becomes Current until 2026-10-29.
5. Expand **Review history**: earlier review, revision and attestation remain visible.
6. Click **Register procedure**, submit invalid source data, then supply a unique HTTPS URL and title. **Add to review queue** creates a due record without fetching its URL.
7. **Export register** downloads current JSON. Reload preserves committed state; shell reset restores the samples.

Implemented locally: filter/select, register/validate, review start/reopen, revision, attestation, history and export. Mocked or absent: private wiki access, concurrent editors, real owner identity, notifications, scheduled expiry processing, server audit and billing.
