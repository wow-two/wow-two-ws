# Renewal notice-window tracker

W0261 · first-ten order 8 · proposed $29/month/company · analysis and local prototype, 2026-09-29.

## Decision, user and job

Test a small operations team’s register for making vendor renewal decisions before owner-confirmed notice dates. The core object is a **notice window with an accountable owner and recorded decision**. The promise is visibility into the next decision, its source and responsible person. Recording an intent is never presented as having cancelled or renewed the external subscription.

[ContractSafe’s date tracking](https://www.contractsafe.com/features/contract-tracking-software), [reminder configuration](https://www.contractsafe.com/support/setting-date-reminders) and [upcoming dates view](https://www.contractsafe.com/support/upcoming-contract-dates) were checked 2026-09-29. They explicitly cover notice deadlines, owner/recipient reassignment, renewal-date roll-forward and chronological views. This is extensive direct competition. Cledara, calendars and a vendor spreadsheet also compete. A lightweight manually supplied cross-system decision queue remains only an adoption hypothesis. Strong first-person evidence for the exact wedge and paid intent remain missing.

## Product philosophy

Separate the last day to act from the date the subscription renews. Separate owner acknowledgment from a decision, and a decision from vendor execution. Preserve those facts rather than collapsing them into a green “done” badge. A changed owner must acknowledge responsibility again.

Automate explicit calendar arithmetic, ordering and report assembly. Humans supply/check the contract reference, decide whether to renew, and complete the vendor’s process. Do not infer legal notice rules, business-day conventions or service cancellation from a generic formula. Quiet-by-default means no reminders until an owner enables a schedule; no automatic subscriptions or escalations to unselected recipients.

## Core journey and exceptional states

Register vendor, renewal date, notice period, annual value and source reference. Review the chronological notice agenda. Assign an owner, record acknowledgment and open the decision file. Record renew/cancel intent with a reason and next step. Reopen or revise the intent while preserving history. Export the current register.

An overdue date stays visible as overdue and never promises recoverability. An unacknowledged owner blocks decision recording. Invalid dates, missing source, negative cost and duplicate sample vendors block registration. An empty Needs decision view explains where completed intentions can be inspected. Reassignment clears acknowledgment. A production source/date revision invalidates acknowledgment of the earlier window. Failed reminder delivery does not imply receipt. Conflicting edits return the latest revision instead of silently overwriting another owner’s decision.

## MVP and non-goals

MVP: manual vendor metadata, explicit source reference, renewal/notice dates, named owner, acknowledgment, recorded decision and export. Follow with opt-in reminders only after schedule semantics and delivery outcomes are clear. The mock uses synthetic vendors and a fixed 2026-09-29 date.

No contract upload/OCR, legal interpretation, autonomous cancellation, payment movement, card issuing, procurement platform, vendor login credentials, email inbox scraping or universal jurisdiction support. The prototype’s calendar-day model is deliberately limited; business-day rules and timezone-specific cutoffs require explicit production configuration. Vendor-side confirmation is not implemented and the interface states that no external subscription changes occur.

## Domain objects and invariants

`Organization`, `VendorAgreement`, `AgreementTerm`, `NoticeRule`, `SourceReference`, `OwnershipAssignment`, `Acknowledgment`, `RenewalDecision`, `ExternalConfirmation`, `ReminderPreference`.

- Preserve the supplied renewal date and notice rule separately from their derived deadline.
- For the supported model, `noticeDeadline = renewalDate − calendarNoticeDays` using date-only arithmetic.
- Monetary value includes currency; it is contract exposure, not claimed savings or product revenue.
- Acknowledgment binds owner plus window version; reassigning or changing dates invalidates it.
- A decision binds the acknowledged window, owner, rationale and recorded time.
- `cancel intent` does not equal `cancelled`; external confirmation is a distinct attributable record.
- Overdue windows remain overdue even when an intention is recorded later.
- No recurring term advances automatically without the explicitly configured rule and source review.

## Proposed architecture and API

Vue owns the agenda and decision desk. .NET owns date-rule validation, authorized transitions and derived notice dates. A relational store holds agreements, term revisions and audit events. Initial delivery can be a single low-cost application instance plus a database and bounded job runner, with measurements before operational expansion.

| Proposed endpoint                                         | Boundary                                                     |
| --------------------------------------------------------- | ------------------------------------------------------------ |
| `POST /api/vendor-agreements`                             | Validate source/date/currency; create with idempotency key   |
| `PATCH /api/vendor-agreements/{id}/term`                  | Explicit date/rule revision; invalidate prior acknowledgment |
| `PUT /api/vendor-agreements/{id}/owner`                   | Assign permitted member and create handoff record            |
| `POST /api/vendor-agreements/{id}/acknowledgments`        | Owner acknowledges exact term revision                       |
| `POST /api/vendor-agreements/{id}/decisions`              | Record authorized intent with reason, no external action     |
| `POST /api/vendor-agreements/{id}/external-confirmations` | Owner-supplied evidence of vendor outcome; later phase       |
| `PUT /api/vendor-agreements/{id}/reminder-preference`     | Explicit recipient/schedule opt-in                           |
| `GET /api/vendor-agreements/export`                       | Tenant-scoped current decisions and audit references         |

Commands carry expected versions and idempotency keys. Conflicting payload retries return conflict; matching retries return the original decision. `TermChanged`, `OwnerAssigned`, `WindowAcknowledged`, `RenewalIntentRecorded` and `ExternalOutcomeRecorded` remain separate events. Background jobs calculate due reminders from supported date rules, use an outbox for deduplicated delivery, observe bounces and honor unsubscribed recipients. No job changes a vendor subscription.

## Security and data ownership

Company administrators manage access; assigned owners acknowledge and decide; read-only finance viewers inspect/export permitted agreements. Treat vendor price, renewal terms and source references as sensitive business data. The MVP stores metadata and source labels rather than full legal documents. Validate URLs if added, but do not server-fetch arbitrary references. Scope audit/export to tenant, expire generated downloads, minimize log content and define retention/deletion policy.

The local mock has no real identity, notification delivery, private contract access or server authorization. It saves synthetic plaintext JSON in browser storage and downloads local JSON. It cannot demonstrate that a notification reached an owner or that a recorded vendor action took place.

## Vue/.NET and SDK boundary

Use Vue 3 for timeline filtering, forms and history disclosures; .NET for date-only arithmetic, transitions and permission checks. Product-specific concerns are notice rules and intent-versus-execution semantics. Candidate shared capabilities include owner selection, date inputs, version conflicts, audit history, optional notifications, typed API errors and authentication. Verify real SDK exports before mapping controls/services; no capability is assumed available. This mock depends only on the supplied `PrototypeApi` and native semantic controls.

## Pricing, costs and empirical gate

Propose a free five-vendor register or worksheet and $29/month/company for repeated review, ownership and decision history. Annual buying may fit the low-frequency task better; normalize any annual price when evaluating MRR. The prototype never treats the annual contract-value summary as savings achieved.

Target the $20–50/month total product infrastructure ceiling using metadata, deterministic dates, no AI/OCR, limited records and capped opt-in email. Cost is unquoted. Onboarding inaccurate terms and handling delivery complaints can outweigh hosting. Approximately $300/month is an expansion ceiling only after recurring contribution supports a measured reliability/integration need.

Activation: an owner verifies source terms and makes a consequential decision in time. Retention: a later vendor decision uses the same register with current data. Review 30 contracts across ten firms. Stop if most target firms have fewer than five consequential notice windows annually, calendars/incumbent reminders suffice, or fewer than three accept a paid pilot. A successful reminder delivery alone is not commercial validation.

## Design analysis and references

ContractSafe’s documentation describes a chronological upcoming view and dates with recipient-specific reminder controls. These are documented interaction concepts; no visual inspection of its live product or customer account is claimed. Borrow the chronological ordering and explicit owner relationship as conceptual references. Keep the proposed interface focused on **a notice-date agenda beside a decision file**, with the later renewal date shown separately.

The date stamp answers when to decide; the desk answers who, why and what remains external. Overdue status uses text plus `--danger`, selection uses `--accent`, and the notice date uses `--accent-soft`; `--surface` and `--surface-alt` differentiate files and recorded decisions. All tokens inherit the shell’s light/dark palette, and its three canvas variants remain proposals rather than approved locks. Below 1024px the agenda precedes the desk; below 768px timeline spacing and date cards compact. Radio choices have descriptions; dialogs, selects and errors are labeled and keyboard reachable. Proposed reusable controls are a date-window comparison, owner acknowledgment and intent history.

## Acceptance and staged implementation

Validate manually supplied dates and the decision workflow first. Implement date arithmetic, version-bound acknowledgment and authorization tests next. Add memberships, exports and audit retention before reminder delivery. Enable notification schedules only after recipient consent, delivery observability and date semantics are tested. External confirmation capture comes later; external execution requires a separate product decision.

Acceptance: SlateDesk’s 2026-10-31 renewal minus 30 days yields 2026-10-01; overdue sample remains overdue; owner changes reset acknowledgment; unacknowledged decisions fail; intent never reports external execution; exports match the current dates/history; theme and keyboard checks pass at the supported widths.

## Mock action coverage and smoke scenario

After shell reset:

1. SlateDesk shows decide-by 2026-10-01, renewal 2026-10-31 and two days remaining.
2. Click **Record renewal decision**, enter a reason, then **Save decision**. It is blocked until owner acknowledgment.
3. Close the dialog. Select Jonas Reed in **Decision owner** and click **Assign owner**. Acknowledgment remains required.
4. Click **Simulate acknowledgment**, then **Record renewal decision**. Choose **Plan to cancel**, add a concrete next step, and **Save decision**.
5. The record shows cancel intent, preserves history, and explicitly states that no vendor change occurred.
6. Click **Reopen decision**: the item returns to the open set without deleting the earlier intent.
7. Select SketchPad: its notice date is overdue; the warning makes no cancellation guarantee.
8. **Add vendor** → **Add notice window** rejects incomplete input. Valid unique data creates a manually sourced record.
9. **Export decisions** includes derived deadlines, current intents, history and `externalSubscriptionChanged: false`. Refresh preserves local state.

Working locally: deadline calculations, open/all filters, selection/detail, vendor validation/registration, owner changes, acknowledgment, decision/reopen and export. Mocked/absent: contract interpretation, verified identity, reminders, time progression, external confirmations, vendor execution, backend concurrency and billing. Shell reset restores fixtures.
