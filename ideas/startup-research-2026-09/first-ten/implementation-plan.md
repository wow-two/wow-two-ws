# Implementation and launch sequence

*Proposal · 2026-09-29 · Estimates are planning ranges, not delivery commitments*

## Architecture choice

Use a separately deployable **modular monolith per validated product**: Vue 3/TypeScript frontend, the public `@wow-two-beta/ui-vue` SDK, ASP.NET Core/.NET 10 backend, and existing Clean Architecture/CQRS/EF Core workspace patterns. Serve the compiled UI and API from one origin. Keep paid validation ahead of sophisticated infrastructure.

These prototypes form one research suite for efficient review. They are not a proposed cross-product SaaS super-app. When a product wins a paid pilot, scaffold its own conformant repository using the workspace's `create-repo` workflow. Keep product billing, data ownership, releases and shutdown decisions understandable independently.

SQLite is adequate for a single-instance bounded pilot when backups, concurrency behavior, and restores are verified. Choose PostgreSQL when multi-instance operation or measured write/concurrency needs warrant it. Do not promise transparent migration before testing identifiers, constraints, transaction semantics, and data conversion. No Kubernetes, event bus cluster, vector database, or LLM is required for the first paid outcomes.

## Verified reuse versus proposed work

| Capability | Evidence available in this workspace | Implementation decision |
|---|---|---|
| Vue presentation SDK | Local `@wow-two-beta/ui-vue` 0.0.7 exports public presentation/foundation entrypoints | Prototype imports its `Button` and `useMediaQuery`; production evaluates each needed control against the pinned version |
| Vue, TypeScript, Vite, Tailwind | Installed local versions successfully compile this suite | Reuse the current frontend stack; no React prototype or second design system |
| Product scaffold | Workspace `create-repo` skill and product-template registration exist | Invoke for an actual production repository, not for every mock |
| .NET application shape | Workspace convention specifies Clean Architecture, CQRS/MediatR and EF Core | Follow the template and inspect package APIs at implementation time |
| Auth, tenant membership, billing, jobs, outbox, audit, import preview | Required capabilities, not verified here as complete reusable SDK implementations | Inventory exact SDK contracts before coding; build missing shared vectors in the SDK rather than duplicating product workarounds |
| External connectors and hosted execution | Not implemented or credentials-tested by these mocks | Begin with bounded CSV/JSON imports and customer-owned runners |

An export namespace existing does not prove every needed API exists. Product dossiers list proposed HTTP routes and domain events; those names are designs, not claims about shipped SDK methods.

## Shared production capabilities

1. **Identity and tenant access.** A workspace has members and owner/editor/reviewer roles. Tenant identity comes from authenticated membership, never a freely supplied body field. Every read, command, export and background job checks the scope. Guest links are random, limited to one resource, revocable, expiring, and excluded from analytics/logs.
2. **Imports.** Parse in a bounded job or request, validate into a preview, show row errors, and commit once. Persist an import ID, source identity and content digest where safe. Replaying the same import must not duplicate time, attendance or findings. Quoted CSV and spreadsheet formula injection require deliberate production handling; simple mock parsers are not a production import library.
3. **Optimistic concurrency and evidence.** Mutable resources carry a version. Commands reject stale versions with a conflict response. Record immutable decision events with actor, time, prior version and evidence reference. Reopening creates history rather than removing it.
4. **Jobs and notifications.** Persist schedule, timezone and delivery preference. A database-backed due-job queue plus transactional outbox is sufficient initially. Use unique delivery keys, retry with backoff, dead-letter visibility and cancellation. Changes committed successfully must not be lost if email delivery fails. At-least-once delivery needs duplicate suppression; do not claim exactly-once external effects.
5. **Billing and entitlements.** Select a payment provider only when the founder's business location, entity, payout support and tax obligations are known. Use hosted checkout, verified signed webhooks, idempotent event processing, grace periods and a cancellation path. Do not put card data in product storage. No provider account, legal advice, or pricing quote is implied here.
6. **Export and exit.** Tenant-scoped JSON/CSV export, scoped attachment download, retention/deletion policy and a tested close-account process. Shared hosting must not mean shared access.
7. **Operations.** Health check, request IDs, failure alerts to the operator, quotas, off-host encrypted backups, restore drill, dependency updates and a documented rollback. Logs exclude content, tokens and raw configuration values. Track support burden as a real cost.

Build the first essential slice for the first paid product, then complete the reusable SDK vector in a dedicated pass. Do not build speculative abstractions for all ten before one buyer has used the workflow.

## Risk classes and hard boundaries

| Class | Products | Initial implementation boundary | Required failure check |
|---|---|---|---|
| Decisions and ledgers | Retainer, procedures, training, promises, renewals, podcast | Structured records, explicit roles, evidence and date semantics | Stale approval, duplicate import, cross-tenant read, incorrect totals |
| Customer-run engineering | Docs, config | Local/CI execution; small authenticated metadata/report uploads; customer-held keyed fingerprints only after protocol review | Forged/replayed reports, sensitive data leakage, untrusted pull-request code |
| Scheduled delivery | Files | Customer-run receipt agent; scheduled expected windows | Missing heartbeat mistaken for missing file, timezone edge, delayed/out-of-order receipt |
| Publication review | EPUB | Import checker reports first; no server rendering of untrusted books | Malformed report, oversized archive, stale proof evidence, unsafe HTML |

GitHub's [secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use) supports isolating untrusted workflow input and restricting credentials; customer CI is not automatically safe. Do not run untrusted examples with organization secrets or privileged runners. Use read-only permissions and explicit execution scope.

ASP.NET Core's [authorization guidance](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/secure-data?view=aspnetcore-10.0) supports protecting user-owned data with authorization checks. Authentication alone is not tenant isolation. Write negative tests for other tenants and unauthorized approvers.

Vue's [security guidance](https://vuejs.org/guide/best-practices/security.html) supports keeping untrusted content out of templates and avoiding unsafe HTML/URLs. EPUB content, imported notes, filenames, and CSV cells remain untrusted even when supplied by a paying customer.

The configuration checker can begin with key presence. Its difference-review prototype explores a later customer-held HMAC comparison protocol, described in its dossier. The service must never receive the HMAC key; fingerprints still disclose equality and change patterns. Security review, canonicalization fixtures, rotation, and namespace isolation are prerequisites for shipping that mode. Synthetic strings in the mock do not implement cryptography.

## Build slices and effort

Ranges below estimate focused engineering time for one experienced developer using functioning shared infrastructure. They exclude customer acquisition, external approvals, unplanned SDK gaps, and extended accessibility/security review. Parallel agents can reduce drafting and implementation time; they do not remove integration or buyer-validation time.

| Product | Pilot build estimate | First vertical slice | Follow-up only after pilot evidence |
|---|---:|---|---|
| Retainer | 8–12 developer days | One client/month, import preview, reconciliation, approval receipt, export | Time-tracker connectors and authenticated client portal |
| Docs | 10–15 days | One runner/language, tagged snippets, CI report, owner triage | More languages, repository app, richer annotations |
| Files | 10–15 days | One receipt method, explicit UTC daily schedule, incident state | IANA timezone/DST rules, holiday calendars, multiple receipt agents |
| Procedures | 6–10 days | URL registry, owner/cadence, review evidence, export | Wiki revision connectors and team policies |
| Training | 8–12 days | One cohort, bookings and attendance CSV, substitutions | CRM/LMS adapters and branded sponsor review |
| EPUB | 10–15 days | Ace report import, proof versions, human checks, handoff | Sandboxed EPUB processing and specialist reader integrations |
| Promises | 8–12 days | Accepted commitment, owner confirmation, changes, digest approval | CRM ingestion with explicit acceptance rules |
| Renewals | 6–10 days | Verified notice dates, owner decision, receipt, digest | Contract extraction assistance with mandatory review |
| Config | 10–15 days | Presence-first CLI manifests, keyed comparison, expiring exceptions | Framework adapters, CI gates and schema comparisons |
| Podcast | 6–10 days | Episode checklist, guest form, evidence verification, handoff | Producer templates, branded pages, opted-in reminders |

The range totals **82–126 developer days**, plus roughly **10–20 days** for missing shared production foundations and hardening. These estimates explain why the ten prototypes should not be mistaken for ten near-finished SaaS businesses. Re-estimate the selected build after inspecting its exact template and SDK contracts.

## Budget discipline

The user's constraint is **$20–50 per product per month before revenue**, with about **$300/month allowed when revenue supports it**. These are spending ceilings, not verified hosting quotes.

| Early budget envelope | Monthly planning allowance | Constraint |
|---|---:|---|
| Allocated application/database capacity | $12–25 | Small instance/shared host allocation with explicit isolation |
| Backups/storage | $3–8 | Bounded metadata, exports and retained evidence |
| Transactional delivery | $0–8 | Low volume; no unbounded free sending |
| Monitoring/domain allocation | $3–8 | Basic checks, pooled operation where appropriate |
| Total envelope | $18–49 | Excludes labor, taxes, payment fees and paid acquisition |

No inference of free unlimited service is permitted. Enforce quotas before offering a free tier. Do not store large EPUBs, podcast media, raw scheduled files, source repositories, or secret values in the first version. No LLM calls are needed to deliver the ten core outcomes.

At a full $300 cost, a $39 subscription requires eight accounts merely to cover infrastructure before fees and support. Do not raise the budget merely because the first customer paid. Recommended expansion gate: measurable need, two months of retained revenue, and infrastructure below roughly 20% of that product's recurring revenue unless an explicit short experiment has a stop date. A $300 steady budget would therefore normally wait for about $1,500 MRR. This is a proposed operating rule, not an additional user restriction.

Ten $50 services cost $500/month even when few have customers. Shared hosting reduces some cost but increases operational coupling; keep backup, access and shutdown boundaries independent.

## Validation and launch gates

### Gate 1 — problem evidence

For each product, recruit five target users with the real recurring workflow. Have them show the existing spreadsheet/tool and a recent exception. Capture frequency, consequence, workaround, decision owner and buyer. An enthusiastic interview is not paid demand.

### Gate 2 — paid pilot

Show the clickable prototype using one sanitized real example supplied with permission. Ask for a paid pilot at the proposed price, with the exact bounded outcome and manual work disclosed. A practical gate is three unrelated paying pilot customers or equivalent signed, dated paid commitments. Founder friends, free trials and mailing-list signups do not satisfy this gate.

These are proposed thresholds. If ten qualified demonstrations produce no paid commitment, revise the positioning once and test again; if payment still fails, park the product. If outreach produces no demonstrations, diagnose channel access rather than concluding the problem does not exist.

### Gate 3 — production pilot

Ship one vertical slice. Check authentication/authorization, imports, invariants, recovery, exports, data retention, and backup restoration. Support the first customers manually. Disable unsupported pathways rather than presenting dormant buttons as implemented features.

### Gate 4 — retention and acquisition

Observe the next natural work cycle: monthly allowance, next CI change, next file delivery, procedure deadline, cohort, proof, customer review, notice window, release, or episode. Require a second useful outcome and actual paid renewal. Track qualified leads → demonstration → activation → payment → retained account, and include founder support time per account.

### Gate 5 — expansion

Only expand connectors, compute or infrastructure when retained customers request a recurring paid improvement. Keep a per-product shutdown/export plan. Continue to the next candidate when this product has a repeatable route to customers or a clear stop decision.

## Production acceptance baseline

- One tenant cannot read, mutate, export, or subscribe to another tenant's records.
- Replayed import/webhook/job input has one logical effect.
- Stale changes fail with a conflict and preserve both versions for review.
- No approval can attach to content that changed after the approver inspected it.
- Domain arithmetic and timezone/date boundaries have meaningful tests.
- Failed delivery or worker restart preserves the underlying obligation.
- Export contains enough data to understand the result outside the product.
- A backup is restored into a separate environment and checked before paid general availability.
- Keyboard navigation, focus management, responsive layout, labels and contrast are verified against the actual production UI.
- Public claims match executed capabilities and do not imply certification, contract action, or customer acceptance without evidence.
