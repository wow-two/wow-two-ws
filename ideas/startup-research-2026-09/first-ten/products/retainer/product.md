# Retainer allowance evidence

W0252 · first-ten order 1 · proposed $39/month/company · analysis and local prototype, 2026-09-29.

## Decision, user and job

Test a client-facing reconciliation layer for a small agency that already records time but repeatedly explains allowance consumption and overages. The core object is an **allowance period with attributable work and decisions**. The promise is that an account owner can explain the balance and agree the next request before a billing surprise. The product neither invents billable time nor judges the fairness of a contract.

The narrow advantage is a reviewable bridge between existing time records, the work a client recognizes, and explicitly approved additions. This is a hypothesis. [Harvest budgets](https://support.getharvest.com/hc/en-us/articles/360048686811-How-to-Use-Budgets) already support recurring budgets, remaining amounts and alerts. [Harvest reports](https://support.getharvest.com/hc/en-us/articles/360048181592-Members-Reports) already drill into client/project/task time and export details. Both primary references were checked 2026-09-29. Bonsai, Harvest and a shared spreadsheet remain substantial substitutes. The earlier public problem reports support retainer-accounting friction, not willingness to pay for this specific layer.

## Product philosophy

- A timer entry is evidence to review, not automatic authorization to charge.
- Preserve the original allowance. Additions are separate decisions with an approver and scope.
- Show unreviewed work separately; a reassuring balance must not hide pending consumption.
- Automate arithmetic, duplicate detection and statement assembly. Humans reconcile work and authorize additions.
- Stay quiet by default. External digests and threshold notifications require explicit opt-in, recipient selection and frequency limits.
- An exported explanation belongs to the agency and client. No lock-in through opaque balances.

## Journey and states

1. Open one client period and see confirmed hours, authorized hours and work awaiting review.
2. Paste a time export. Preview validates source IDs and numeric durations before a batch is committed.
3. Inspect a work item, reconcile it into the period, or return it to review. Balances recompute.
4. When more work is needed, prepare a scoped extra-allowance request. Requested hours do not increase the authorized allowance.
5. Record client approval against the requested hours and price, then produce a current statement.

Empty periods invite import. Duplicate source IDs block the whole batch. Invalid hours identify the failing row. Over-consumption stays visible as unapproved overage. Changing underlying work invalidates the previously prepared statement. Production conflict handling returns the newer period revision before accepting a stale approval or reconciliation.

## MVP boundary

One hourly allowance model; one currency per agreement; monthly periods; bounded CSV import; review decisions; overage requests; client-readable statement; downloadable audit. The mock uses one synthetic company and September period. It deliberately keeps request creation and approval separate.

No timer, invoicing, payment collection, accounting integrations, automated client email, legal interpretation, rollover rules, multi-currency conversion or automatic approval. Production client access requires scoped identity; clicking the mock approval is explicitly a simulation.

## Domain and invariants

`Organization`, `Client`, `Agreement`, `AllowancePeriod`, `ImportBatch`, `TimeEntry`, `Reconciliation`, `OverageRequest`, `Approval`, `StatementRevision`.

- Durations use integer minutes; money uses integer minor units and currency, not binary floating-point billing.
- `confirmedMinutes = sum(reviewed entries)`; `authorizedMinutes = base + approved additions`.
- `balance = authorized − confirmed` may be negative; the UI must expose that state.
- Pending entries and pending requests never silently alter authorized consumption or allowance.
- Imported identity is unique within organization/source/period. Retrying an import cannot add time twice.
- Approval binds the exact request revision, minutes, rate, approver and period; editing invalidates approval.
- Published statements are immutable snapshots. Corrections create another revision with provenance.

## Proposed implementation

Vue owns the import-review view, entry detail and client-statement projection. A .NET application service owns import validation, minute arithmetic, transitions and authorization. A relational database stores typed records and append-only decision events. Keep original uploads optional and short-lived; a normalized row plus source hash is usually sufficient.

| Proposed endpoint                           | Boundary                                                           |
| ------------------------------------------- | ------------------------------------------------------------------ |
| `POST /api/periods/{id}/import-previews`    | Validate a bounded file; return row errors and content fingerprint |
| `POST /api/periods/{id}/imports`            | Commit reviewed fingerprint with an idempotency key                |
| `PATCH /api/entries/{id}/reconciliation`    | Period-owner authorization and expected version                    |
| `POST /api/periods/{id}/overage-requests`   | Store scope, minutes and price snapshot                            |
| `POST /api/overage-requests/{id}/decisions` | Client approver grants/declines the exact revision                 |
| `POST /api/periods/{id}/statements`         | Create an immutable statement revision                             |
| `GET /api/periods/{id}/export`              | Authorized tenant-scoped export                                    |

Use ETags/expected versions for changes. Reused idempotency keys with different payloads return conflict. Events include `ImportCommitted`, `EntryReconciled`, `OverageDecided`, `StatementPublished`. Background work is limited to opted-in digest delivery and retention cleanup; an outbox prevents duplicate deliveries. No integration is implicitly wired.

## Ownership and security

Agency administrators control membership; account owners manage assigned periods; client approvers see only their own statements and pending decisions. Import limits include byte, row and field lengths, supported encodings and malformed-file rejection. Neutralize spreadsheet formulas if CSV export is introduced. Do not store card data or time-provider credentials. Apply tenant filtering before queries, signed scoped sharing with revocation, audit retention and account deletion/export policy.

The prototype saves synthetic JSON in browser storage and exports local JSON. It provides no encryption-at-rest assurance, server identity, cross-user permission enforcement or durable audit guarantee. Use no real client records in it.

## Vue/.NET and SDK boundary

Production proposes Vue 3 and .NET, with product-owned minute arithmetic, approval state and statement projections. Shared candidates are validated forms, dialog behavior, semantic status, data tables, tenant auth, audit events and download handling. Verify actual workspace SDK exports before adopting them; this document declares no existing SDK API. The mock consumes only the provided `PrototypeApi` and native controls, with per-product CSS and semantic theme tokens.

## Economics and validation

A useful free single-period worksheet can demonstrate the job; $39/month/company tests recurring periods, approval history and client views. It is a proposed price, not a measured willingness-to-pay result. Before revenue, design for $20–50/month total product infrastructure: shared hosting/database, local CSV parsing, metadata retention, 1,000 active records per pilot organization and capped opted-in notifications. No AI or paid provider integration is required. These are design limits, not vendor quotes; support minutes may dominate hosting.

Expand toward approximately $300/month only after positive recurring contribution and a measured storage, reliability or integration bottleneck. Activation is a reconciled real period that answers a client question; retention is the next period reconciled without founder data-cleaning help. Run two billing cycles at five agencies. Stop if four accept existing reports as sufficient, or fewer than three accept a paid pilot after a concrete demonstration.

## Design analysis and reference rationale

The Harvest references establish interaction concepts—client-to-entry drilldown, budget-versus-consumption, and exported reports. These are text/documentation observations; no claim is made to have visually inspected or copied the full Harvest UI. The proposed move is a **reconciliation desk beside a statement-shaped client view**: evidence on the left, consequence and approval on the right. This avoids making activity metrics the primary task.

The shared shell supplies three canvas proposals; none is an approved brand lock. `--surface` carries evidence and statements, `--surface-alt` the prepared digest, `--accent-soft` the selected entry, and `--danger` negative balance. Status always includes text. Light/dark use the same semantic roles; no literal color encodes approval alone. On widths below 1024px, the statement follows the ledger; below 768px, the allowance strip compacts while the table remains locally scrollable. Buttons, labels, native dialogs and error alerts provide keyboard routes. Proposed reusable controls: import preview, minute balance, revision-bound approval and statement preview.

## Acceptance and staged build

1. Validate the imported evidence and approval workflow with a manually prepared statement.
2. Implement domain arithmetic and import/idempotency tests before external sharing.
3. Add tenant membership, read-only client statements and revision-bound approval.
4. Add delivery only after consent/recipient controls and paid repeated usage.

Acceptance requires duplicate rejection, exact minutes after review/reopen, no allowance change for pending requests, correct approved fee totals, stale statement invalidation, exported data matching visible balances, keyboard completion, responsive layout and theme parity.

## Mock action coverage and smoke scenario

After shell reset:

1. Confirm 19 hours reviewed, 24 authorized, 5 available and 4 awaiting review.
2. Select **New partner page — confirm allowance** and click **Reconcile entry**: 23 confirmed, 1 available.
3. Click **Import time**, then **Review import**, then **Import 1 entry**. The 3.5-hour entry remains unreviewed.
4. Click **Reconcile entry**: 26.5 confirmed; 2.5 hours need approval.
5. Click **Request extra allowance**, retain 3 hours, then **Prepare approval request**. Authorized hours remain 24.
6. Click **Simulate client approval** with Avery Chen: authorized hours become 27, available becomes 0.5, extra fee $285.
7. Click **Prepare client statement**, then **Export ledger**. Both reflect the current decisions.
8. Re-import source `T-105`: **Review import** rejects the duplicate. Refresh preserves committed local state.

Local working capabilities: import validation/preview, reconciliation/reopen, request/approval simulation, computed balance, statement invalidation/preparation and JSON export. Not implemented: production CSV quoting/encoding, authentication, real approvals, email, backend, immutable server audit, billing and integrations. Shared-shell reset handles sample restoration.
