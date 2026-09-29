# Product philosophy for the first ten

*Proposal · 2026-09-29 · No product or design approval is inferred from this analysis*

## The promise

**Get The Work Done & Never Bother Me.** For these ten products, this means the user can recognize the outcome, understand the evidence behind it, and leave the application until another meaningful decision is required.

A product should remove a recurring uncertainty: how many hours remain, which example failed, whether a delivery arrived, who reviewed a procedure, which training seats count, what changed between proofs, which promise is owned, when notice is due, whether drift is intentional, or whether a guest is ready.

Each product owns one small record of truth. It should not acquire every adjacent feature simply because the same customer could use it.

## Principles translated into behavior

| Principle | Behavior required | Failure to avoid |
|---|---|---|
| Start with the decision | First screen shows the work needing attention and a concrete next action | Decorative metrics without a useful task |
| Preserve the source | Show the imported ID, version, timestamp, or evidence reference | An unexplained green badge |
| Make completion honest | Name exactly what was recorded, tested, approved, or received | “Done” implying an external action that never happened |
| Keep judgment human | Approval, contractual meaning, accessibility judgment and acceptance stay explicit | A checkbox silently creating an obligation |
| Automate repetition | Recalculate, group, compare, deduplicate, and prepare drafts | Autonomous decisions exceeding the user's instructions |
| Be quiet by default | Opted-in channels, batching, timezone-aware deadlines, pause and digest controls | Repeated reminders, upsells, streaks, or engagement nags |
| Be reversible | Reopen with history, restore samples, preview imports, retain source evidence | Destructive edits that erase the previous decision |
| Leave cleanly | Export understandable records without locking the user into our UI | Proprietary lock-in for a simple ledger |
| Charge for recurring work | Paid tier covers repeat teams/workflows and dependable delivery | Artificially withholding the one useful result |
| Know when to stop | A completed period, reviewed proof, resolved incident, or ready episode has a clear endpoint | Endless inbox work caused by the tool itself |

## Ten interpretations

| Product | Core object | User's decisive act | Safe automation | Completion evidence |
|---|---|---|---|---|
| Retainer | Client period allowance ledger | Reconcile an entry; accept extra scope | Sum integer minutes and prepare the client statement | Approved extension plus reconciled source entries |
| Docs test | Example run tied to a commit | Assign/fix a failure; review a fresh run | Compare customer-run reports and group recurring failures | New run ID, commit, runner result and resolved failure |
| File watch | Expected delivery window | Acknowledge, excuse, or resolve an incident | Match receipts to windows; deduplicate alerts | Receipt identity and delivery timestamp |
| Procedure review | Procedure review obligation | Review the source and attest with evidence | Calculate due dates and assemble owner queues | Reviewer, source revision, method and review time |
| Training seats | Booking allocation within a cohort | Resolve unmatched attendance or substitution | Reconcile purchased/reserved/attended seats | Closed cohort export with preserved substitutions |
| EPUB review | Proof-specific finding | Judge and document the correction | Import tool findings and compare proof versions | Finding evidence and separate human review record |
| Promises | Accepted customer commitment | Accept scope; approve a customer update | Surface overdue owners and draft a digest | Immutable digest snapshot of commitment revisions reviewed at approval time |
| Renewals | Verified notice deadline | Choose and execute renewal/cancellation elsewhere | Calculate reminder windows around confirmed terms | Decision record plus external receipt reference |
| Config check | Release manifest comparison | Approve an intentional difference with expiry | Compare names/types and existing exception scopes | Customer-run manifest plus scoped exception history |
| Guest ready | Episode readiness checklist | Verify assets and permission evidence | Group missing items and prepare a handoff | Completed checklist with producer verification |

## The common interaction grammar

**Capture → inspect → decide → record → leave.** The steps look different in each product. A balance ledger needs arithmetic close to line items; a configuration checker needs a comparison matrix; EPUB review needs document structure and version context. Shared controls do not justify forcing all ten into the same dashboard.

Every action has a truthful verb. “Prepare statement” creates a draft. “Record approval” stores a human event. “Import sample report” does not execute a test. “Mark recovered” does not retrieve a file. A production interface should expose the source and time of external evidence whenever that evidence changes the user's decision.

The mock suite uses a fixed September 29, 2026 reference date to make deadlines reproducible. Real services need persisted UTC timestamps, explicit IANA timezones, date-only concepts where appropriate, and tested daylight-saving transitions. Those semantics belong to the domain, not to a formatting helper.

## Where each product must resist expansion

- Retainer is not a complete accounting, time-tracking, or payments suite.
- Docs test is not hosted arbitrary-code execution or a replacement documentation CMS.
- File watch is not a file-transfer service or customer credential vault.
- Procedure review is not a wiki editor or a compliance certification system.
- Training seats is not an LMS, examination platform, or learning surveillance product.
- EPUB review is not an authoring platform or an accessibility certification service.
- Promises is not a general CRM, feedback board, or autonomous sales agent.
- Renewals is not contract interpretation, purchasing, or automated cancellation.
- Config check is not a secrets manager or deployment controller.
- Guest ready is not audio recording, hosting, or automatic consent generation.

These exclusions are the cost strategy as well as the product philosophy. The first paid version handles structured records and bounded imports, not expensive compute, media custody, or dozens of fragile integrations.

## Monetization principles

Prefer a useful free result and a paid recurring workflow. Examples: a local docs runner, a single reconciled retainer period, one proof review, or one guest pack. The paid tier adds recurring projects, collaboration, history, dependable opted-in notifications, and external review links where needed.

Subscriptions fit ongoing obligations. Lifetime purchases fit a bounded local utility or a supported major version; they do not fund unlimited server work and future notifications forever. Any lifetime offer needs explicit limits and a reserve for support. Avoid launching all three payment models per product before one has evidence.

Use plan limits that follow value: active client retainers, repositories, monitors, procedures, cohorts, concurrent proofs, customer accounts, vendors, environments, or active shows. Do not meter basic safety, export, cancellation, or access to a user's own records.

## Evidence that would change the philosophy

If buyers only need a one-time cleanup, sell a fixed-scope utility or service rather than forcing a subscription. If the existing spreadsheet already produces a reliable result in minutes, stop that product. If users demand hosted compute, large-file processing, or constant integrations before paying, move the candidate behind a product with cheaper validation.

Success is a repeated outcome the user values enough to pay for—not daily active use. Renewal and procedure products may be valuable with infrequent logins. Measure acted-on deadlines and current review coverage, not engagement manufactured by notifications.
