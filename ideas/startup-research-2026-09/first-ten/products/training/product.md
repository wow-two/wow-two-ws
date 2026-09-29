# Corporate training seat reconciliation

W0289 · first-ten order 5 · proposed $59/month/provider · analysis and local prototype, 2026-09-29.

## Decision, buyer and job

Test a sponsor-facing entitlement ledger for independent training providers selling repeated online cohorts to organizations. The core object is an **agreement with purchased seats and attributable allocations**. A coordinator must explain who used a seat, who is expected next, and whether a replacement consumed another entitlement.

[Arlo’s customer portal](https://www.arlo.co/features/customer-portal), checked 2026-09-29, already describes registrations, transfers, orders and course history. TalentLMS, TutorCruncher and spreadsheet rosters also overlap. The narrow hypothesis is reconciliation across an existing sales agreement and multiple course systems without migrating course delivery. An incumbent portal may already solve everything. Do not interpret the mock or a lower proposed price as proof of an unmet need.

## Product philosophy

The promise is an explainable seat balance with preserved change history. An invitation, attendance mark and financial entitlement are different facts. The coordinator decides whether an allocation, substitution or release is allowed under the agreement. Automation maintains arithmetic, detects duplicate assignments and assembles a sponsor statement.

Never charge another seat merely because a name changes. Never erase the original learner to make a substitution look clean. Quiet-by-default means no learner invitations, sponsor messages or reminders until explicitly requested. A training provider should use the product when a reconciliation is needed, not to satisfy an engagement metric.

## Journey and failure states

Open the sponsor agreement; inspect purchased, attended, reserved and available seats; filter by cohort; reserve a seat; substitute a learner while preserving the balance; confirm attendance; release an unused seat when allowed; export the sponsor statement including history.

Invalid names/emails block writes. Duplicate active learner email within an agreement blocks a second entitlement. Fully allocated agreements cannot reserve another seat; full cohorts reject assignments even if agreement entitlements remain. Only an enrolled seat can be substituted or released; consumed attendance must first receive an explicit correction. The prototype disables attendance before the cohort date. Released records remain available through the history filter. An empty roster offers a cohort change or reservation, not a fabricated zero-cost purchase.

In production, stale concurrent assignments return a conflict with the latest balance. Failed imports stay in preview, and an unknown learner identifier creates a match task rather than an automatic duplicate or release.

## MVP and exclusions

MVP: organization agreements, purchased entitlements, cohort capacities, CSV preview/import, manual allocations, substitutions, attendance reconciliation and sponsor statements. Keep course content and live teaching in existing systems. The clickable mock uses one 12-seat agreement, two cohorts, local forms and supplied synthetic attendance.

No LMS, course hosting, video transport, checkout, certificates, attendance surveillance, payroll, travel logistics, automatic refunds or payment custody. No production CSV importer exists in the mock. Different cancellation/transfer/expiry rules require explicit policy configuration; the prototype models a single reusable unused-seat rule only.

## Domain and invariants

`ProviderOrganization`, `Sponsor`, `SeatAgreement`, `EntitlementPolicy`, `Cohort`, `LearnerReference`, `Allocation`, `Substitution`, `AttendanceDecision`, `SeatRelease`, `StatementRevision`.

- `available = purchased − attended allocations − reserved allocations`; all quantities are nonnegative integers.
- Cohort capacity and sponsor entitlement are distinct limits and must both pass atomically.
- A substitution releases the old allocation and creates its linked replacement in one transaction; total occupied seats stays unchanged.
- A released learner remains in history and consumes no seat.
- Attendance consumes an already reserved allocation, never a second seat.
- Changes to purchased quantity require an attributable agreement adjustment, not editing a display total.
- Learner matching uses stable source identifiers where available; email is a prototype simplification, not a universal identity key.
- Sponsor exports contain only that sponsor’s learners and agreements.

## Proposed architecture and contracts

Vue shows the seat equation, roster and selected allocation. .NET domain commands enforce both capacities and preserve movement history. Store organizations, agreements, cohorts and allocations relationally, with optimistic concurrency plus transactional seat allocation. Immutable allocation events permit an explainable balance, without assuming a large event-sourcing platform is required.

| Proposed endpoint                           | Critical behavior                                              |
| ------------------------------------------- | -------------------------------------------------------------- |
| `POST /api/agreements/{id}/roster-previews` | Validate bounded CSV and return duplicates/matching conflicts  |
| `POST /api/agreements/{id}/allocations`     | Atomic entitlement and cohort-capacity check                   |
| `POST /api/allocations/{id}/substitutions`  | Replace one active allocation with one linked allocation       |
| `POST /api/allocations/{id}/attendance`     | Record attendance or explicit correction with actor and reason |
| `POST /api/allocations/{id}/releases`       | Apply supported unused-seat release policy                     |
| `POST /api/agreements/{id}/statements`      | Create a reproducible sponsor snapshot                         |
| `GET /api/agreements/{id}/export`           | Export authorized agreement detail                             |

Every mutation takes an idempotency key and expected agreement/allocation version. A replay returns the earlier result; changed payload under the same key returns conflict. `SeatAllocated`, `LearnerSubstituted`, `AttendanceConfirmed`, `AttendanceCorrected` and `SeatReleased` identify the actor and affected agreement. Background jobs only process approved imports, retained export cleanup and explicitly requested statement delivery. No automatic learner outreach.

## Security and data ownership

Providers administer agreements; coordinators work within assigned cohorts; sponsor viewers access only their agreement. Minimize learner data to name and contact/reference needed for the workflow. Avoid storing demographics, assessment scores or sensitive training outcomes. A sponsor report needs a deliberate contact-data policy; public share links are inappropriate defaults.

Enforce tenant/sponsor filtering in queries and downloads, upload row/size limits, safe spreadsheet exports, transactional authorization and revocable access. Define deletion/pseudonymization independently from necessary financial record retention. Production invite links, if added, expire and scope to the learner/action. The mock stores synthetic plaintext browser JSON, provides no verified identities, and sends nothing externally.

## Vue/.NET and SDK integration

Keep the seat policy and transactional allocation logic product-owned. Vue 3 composes roster, detail, substitution form and sponsor projection; .NET handles command validation and data ownership. Shared candidates are accessible dialogs, identity matching previews, grids, filters, timeline history, authentication and typed API errors. Inspect real SDK exports and package versions before reuse; neither backend nor frontend SDK availability is assumed. The current prototype uses the provided `PrototypeApi`, native labeled forms and product-scoped CSS only.

## Pricing, costs and evidence gates

Propose a free single-agreement reconciliation sample, then $59/month/provider for multiple active corporate agreements and repeat sponsor statements. The buyer is the training operator, not the individual learner. Keep transaction/seat fees out of the initial test so the customer can compare a predictable monthly cost with coordinator time saved.

Design for $20–50/month total pre-revenue infrastructure: bounded metadata, no course files or video, CSV/manual input before paid LMS integrations, limited export retention and capped opted-in messages. This is an operating constraint, not a measured hosting quote. Support from ambiguous identity matches and bespoke contract rules is the main cost risk. Expand toward approximately $300/month only after recurring contribution funds a demonstrated limit; do not add expensive connectors to rescue weak demand.

Activation is an existing agreement reconciled without unexplained seat differences. Retention is the next cohort or statement produced using the same policy without bespoke founder work. Test five corporate contracts at two or more providers. Stop if substitutions are rare, existing LMS reports suffice, providers demand course hosting, or no provider pays for repeat reconciliation.

## Design references and rationale

The Arlo source establishes transfers and course history as related operations. This is a documented interaction reference, not a visual inspection or reproduction of Arlo’s application. The proposed visual move is an **entitlement equation plus seat tokens above an operational roster**. It makes a substitution’s unchanged total observable. Cohort cards act as filters rather than navigation to another dashboard. The selected learner desk preserves the earlier name and decision trail.

Design remains a recommended proposal. The shell supplies three canvas variants and theme controls. `--accent` identifies consumed seats, `--accent-soft` reserved seats, and an outlined token available seats; text totals and an accessible map label repeat the distinction. Surfaces and text inherit light/dark semantics. At less than 1024px the detail follows the roster. At less than 768px the seat map becomes two rows, cohort filters stack and the roster scrolls within its panel. All mutations use labeled native dialogs with inline errors. Reusable candidates include an allocation equation, capacity validator and linked-substitution history.

## Acceptance and build sequence

First reconcile real supplied exports manually against sponsor agreements. Next implement seat-policy/domain tests, transaction/idempotency behavior and explicit corrections. Then add tenant/sponsor access and import previews. Only after paid repeated usage add the narrowest verified LMS connector and delivery controls.

Acceptance requires exact unchanged occupied count after substitution; no negative available seats; separate cohort limit; attendance without extra consumption; no release of an attended allocation; duplicates blocked; export reflects current state; local state persists; keyboard paths and responsive themes remain usable.

## Mock action coverage and smoke scenario

After shell reset:

1. Confirm 12 purchased, 1 attended, 4 reserved and 7 available seats.
2. Select **Noah Kim**, then **Substitute learner**. Submit an empty form with **Confirm substitution**: validation blocks it.
3. Enter Alex Morgan, `alex@example.com`, and a substitution reason; keep the September cohort. **Confirm substitution** preserves 7 available seats.
4. Toggle **Show released learners**: Noah remains in the roster as released; Alex references Noah’s original allocation.
5. Select Alex and click **Mark attended**: attended becomes 2, reserved becomes 3, available remains 7.
6. Click **Reserve a seat**, enter a distinct learner/email for the October cohort, then **Confirm reservation**: available becomes 6.
7. Select the new learner, click **Release unused seat**, enter a reason, then **Confirm seat release**: available returns to 7.
8. **Export sponsor statement** downloads the balance and linked history. Refresh preserves it. October attendance stays disabled before 2026-10-14.

Locally working: roster filters, selection/detail, reservation, substitution, attendance/correction, release, invariant-based validation, seat arithmetic and JSON export. Mocked/absent: real attendance ingestion, identity verification, imports, sponsor authentication, notifications, payments and backend concurrency. Shell reset restores the synthetic fixture.
