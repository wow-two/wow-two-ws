# Kept — customer commitment ledger

Proposal dated 2026-09-29 · W0276 · selected order 7 · proposed $59/month per organization.

## Decision and philosophy

Serve small B2B account teams whose customer commitments escape sales notes and roadmaps. The promise is concrete: every agreed customer outcome has a responsible owner, a due date and an honest, reviewed update. The core object is a **commitment accepted by a named owner**. Feature suggestions, hopes and tentative requests must not silently become commitments.

Humans decide what was promised, whether the owner accepts it, when delivery is credible and what customers should hear. Software remembers the source conversation, highlights missed dates and prepares a reviewable digest. It must not promise roadmap dates, infer agreement from a transcript, or send a customer update without an approved snapshot. Quiet by default means exception-focused views and opted-in internal reminders, not daily activity nags.

## Advantage to falsify

[Canny pricing](https://canny.io/pricing), checked 2026-09-29, lists feedback capture, account-linked workflows and a free tier; Pro starts at $79/month billed annually. [Custify](https://www.custify.com/pricing), checked the same day, offers account tasks, automation and a customer portal with sales-led pricing. These are adjacent category evidence, not evidence that this narrower ledger is underserved.

The residual hypothesis is a lighter sales-to-success agreement workflow with explicit owner acceptance and a human-approved customer snapshot. Compare against CRM notes, ordinary tasks and those incumbents. If a generic task with an account link is sufficient, reject a separate product. A draft digest is useful only if teams maintain accurate commitments.

## Journey, screens and failure states

1. Capture a promise with customer, source conversation, responsible owner and due date.
2. Ask the owner to confirm responsibility. Keep the unconfirmed record internal.
3. Review the due-date timeline and identify overdue or blocked commitments.
4. Record a customer-safe progress update. Preserve previous updates rather than overwrite history.
5. Choose exactly one `Digest account` and preview its confirmed commitments.
6. A person approves its fixed contents; export or an explicit later delivery action follows.

The desktop composition pairs a chronological commitment list with a selected record inspector. Date tiles emphasize time without a misleading numerical health score. Ownership sits above source evidence and updates. A separate digest card contains an explicit `Digest account` selector, defaulting to Northstar Labs. This selector is independent of the ledger filter, including `All accounts`; it has no all-account option. The digest dialog repeats the selector and account identity so the intended recipient remains visible during review. At 820px the list is full width with detail and communication below; at 390px everything stacks. Modals handle capture and digest review.

Empty: an account with no eligible confirmed promises cannot approve or export an empty digest. Validation: title, source and due date are required; duplicates for the same account are rejected. Delivery cannot be marked complete before owner confirmation. Changing `Digest account` clears the draft and disables approval/export until `Refresh digest` prepares that account’s contents. Conflict: production revision conflicts preserve the user’s draft and offer a compare/reload path. The mock checks the account and complete set of confirmed item revisions before approval/export and never mutates already approved snapshots. Save and notification failures are proposed production states, not simulated network calls.

## MVP and non-goals

MVP: manual capture, account filter, ownership confirmation, dated updates, overdue queue, fixed digest approval and local/client export. Use links to existing CRM records before building integrations. Keep dates explicit and customer-safe text separate from private notes.

Exclude CRM replacement, roadmap voting, call recording, automatic AI promise extraction, contract interpretation, task scheduling optimization and automatic customer messaging. The mock has no private-note field, actual users, email or external account connection.

## State model and invariants

`Account` owns `Commitment`; a commitment has `SourceReference`, `OwnerAcceptance`, dated `ProgressUpdate` records and a monotonically increasing revision. Status is Planned, In progress, Blocked or Delivered. Proposed future due-date amendments retain both dates and a reason; they never erase that a promise changed.

A record can exist before acceptance, but cannot appear in a client digest until confirmed. Delivery requires confirmation. Every `DigestSnapshot` owns exactly one account and records its confirmed commitment revisions, public text, reviewer and approval time. The prototype signature binds the account plus the ordered record IDs and revisions; it is a local consistency check, not a cryptographic signature. Editing the ledger never edits a previously approved digest. Changed confirmed records, newly confirmed records, or a changed digest account require regeneration. Client text exports always contain one account and use an account-specific filename. The separate full-ledger JSON export is explicitly marked internal and may include multiple accounts. There is no all-account client digest.

## Proposed implementation

A Vue domain module owns the timeline, inspector, capture form and digest preview. .NET owns tenant permissions, revision checks and append-only updates. Candidate shared `@wow-two-beta/ui-vue` capabilities include dialogs, labeled fields, validation, toasts and date input. Verify public exports in the pinned Vue package before production integration; do not assume legacy `@wow-two-beta/ui` React APIs apply.

Proposed routes: `GET /api/accounts/{id}/commitments`, `POST /api/commitments`, `POST /api/commitments/{id}/acceptance`, `POST /api/commitments/{id}/updates`, `POST /api/accounts/{id}/digest-drafts`, `POST /api/digests/{id}/approval`, and a separately authorized `POST /api/digests/{id}/deliveries`. Create/update commands carry an idempotency key and expected revision. Approval binds a content hash and reviewer role.

Proposed events: `CommitmentCaptured`, `OwnerAccepted`, `CommitmentUpdated`, `DigestApproved`, `DeliveryRequested`. A daily due-date job only creates eligible internal reminder candidates when enabled. Delivery uses an outbox keyed by digest/account/channel, has bounded retries and records provider outcomes. An approved digest is not evidence of a sent message. No job automatically turns notes into commitments.

## Data ownership and security

The organization owns its records and can export them. Limit customer data to account identity, owner, dates, public update and source reference. Apply tenant and account access checks on every route; segregate private information from client snapshots at serialization boundaries. A customer viewer sees only approved snapshots for its account. Escape user text, audit approvals, expire shared links and apply documented retention/deletion. The mock uses synthetic browser storage, not production access control or a confidential-data vault.

## Economics and validation

Test a bounded 14-day trial, then $59/month per organization for recurring owner workflows, updates and approved digests. No permanent free file hosting is required. Proposed pilot limits: 1,000 active commitments, 10 internal users and 1,000 opted-in notifications/month. Links and metadata keep media costs out of scope. Target $20–50/month operating spend before revenue; this is a design ceiling, not a hosting quote. Measure support and onboarding minutes. Approximately $300/month becomes available only after products earn and the next dependency has measured value.

Activation: one real sales-to-success handover captured, accepted and included in a reviewed digest. Retention: the same account team updates commitments in successive weeks and pays through a second month. Proposed experiment: audit ten accounts at five vendors; compare with their existing CRM/tasks. Require three $59 paid pilots, regular owner acceptance and second-month renewal. Kill if the distinction between a promise and a request remains unclear, or teams do not maintain updates. At $59, 85 active organizations produce $5,015 gross MRR; no acquisition or retention rate is established.

## Design references and light/dark system

[Basecamp features](https://basecamp.com/features), checked 2026-09-29, documents project context, to-dos, schedules and client collaboration. The conceptual move is to keep responsibility and time close to the work. Canny and Custify contribute the account/work-item relationship. These are documentation-derived interaction references; visual screenshots were not inspected and their interfaces are not copied.

The timeline plus owner inspector is the recommended original composition. Root’s three canvas variants remain proposals, not approved locks. Light and dark use identical hierarchy: `--canvas` surrounds `--surface` records; `--surface-alt` holds source evidence; `--accent-soft` marks the selected commitment. `--danger` highlights overdue counts alongside the label; status chips carry text. Candidate reusable controls are the dated record row, owner-confirmation card and immutable digest preview. Native dialog behavior and visible form labels preserve keyboard navigation.

## Staged implementation and acceptance

1. Review the local flow with the proposed palette variants.
2. Run a user-authorized historical promise audit before paid integrations.
3. Implement authenticated capture, acceptance, versioned updates and account-scoped exports.
4. Implement fixed digest approval and explicit delivery with replay-safe outbox handling.
5. Add CRM import only after observed repeated manual entry justifies its complexity.

Acceptance requires accurate computed active/overdue/delivered counts, exactly one account per client digest, no unconfirmed record in a client digest, unchanged prior approved snapshots and exports reflecting current state. Changing the ledger filter must not retarget a digest. Changing the digest account must invalidate its draft before approval/export. Production gates include server-enforced cross-account isolation, concurrent-edit rejection, idempotent delivery tests and logs distinguishing approved, queued and delivered.

## Exact prototype smoke steps

1. Reset with the shell control. The sample shows three active, one overdue and one unconfirmed commitment.
2. Select `Deliver the account migration plan`. Click `Confirm owner · simulated`. Unconfirmed decreases to zero.
3. Click `Record update` empty. The inline error appears and history does not change.
4. Enter `The plan is drafted and ready for the migration lead.` Keep `In progress`, then click `Record update`. A dated update appears.
5. Select `Delivered` and enter `The migration plan was reviewed with the account team.` Record it. Active decreases and Delivered increases.
6. Click `Capture a promise`, then `Save commitment` empty. Validation blocks creation.
7. Enter `Deliver the security review summary`, source `Customer call · 29 September`, and a due date. Save. The new record appears unconfirmed.
8. Leave the ledger filter on `All accounts`. Check that `Digest account` defaults to `Northstar Labs`. Click `Preview client digest`: only Northstar’s confirmed records appear; Morrow, Lumen and the new unconfirmed promise are absent.
9. Inside the dialog, change `Digest account` to `Morrow Studio`. The old draft disappears, the refresh notice appears, and `Export digest` / `Approve digest · simulated` are disabled.
10. Click `Refresh digest`. Only Morrow’s compatibility commitment appears. Approve, then export. Inspect `client-digest-morrow-studio.txt`: its account header and every item belong to Morrow; its status says locally approved, not sent.
11. Change the dialog’s account back to `Northstar Labs`. Approval/export disable again. Refresh and approve its Northstar-only snapshot; export `client-digest-northstar-labs.txt`.
12. Close the dialog, change the ledger filter to `Lumen Works`, and preview again. `Digest account` remains Northstar and the prepared snapshot still contains only Northstar records.
13. Close and click `Export commitments`. Its scope explicitly says internal full ledger. Verify it contains all accounts and the separately approved Morrow and Northstar snapshots without changing their contents.
14. Reload to verify ledger and approved snapshot persistence. `Digest account` returns to its default Northstar Labs; no unapproved draft is persisted. Switch light/dark and inspect 390px, 820px and 1440px layouts.

Implemented mutations: capture, confirm owner, append status update, approve immutable digest. Delivery, identity, account authorization, notifications and real client views remain mocked. Root owns integrated verification; the steps are reproducible acceptance criteria, not a claim they were executed.
