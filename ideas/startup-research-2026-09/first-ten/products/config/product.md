# Parity — environment configuration review

W0034 · first-ten order 9 · proposed $39/month · research and clickable prototype, not a configuration service.

## Decision and product philosophy

Test a read-only comparison layer for a small SaaS team whose environment settings are split across several tools. The buyer is the technical lead; the user is the engineer checking a release or onboarding another environment. The job is to find a missing key and distinguish an intentional environment difference from an unexplained one before a deployment depends on it.

The promise is “every difference has an explanation.” The core object is a comparison of two versioned manifests, not a secret or a deployment. A human decides which keys should match, which should differ, and how long an exception remains valid. Automation detects presence, compares fingerprints, and invalidates outdated approvals. It does not copy settings, fetch secrets, edit cloud resources, declare a deployment safe, or approve its own findings. Matching and previously approved pairs stay quiet; only changed or expired decisions need attention.

The narrow initial advantage is reviewable evidence across existing configuration sources without migrating to a new manager. That advantage remains a hypothesis. If customers already maintain one effective source of truth, a separate comparison layer is redundant.

## Market challenge and paid-pilot test

[ConfigCat](https://configcat.com/pricing/) lists a free configuration/feature-flag plan and paid plans; its pricing page describes multiple environments, change audit logs and mandatory reasons. It is an adjacent management product, not proof of demand for independent parity checks. Shell diffs and the team's existing secrets manager are direct substitutes. A $39 review layer cannot win merely by displaying differences more attractively.

Begin with five teams that have a concrete missed-key incident and settings split across at least two sources. Compare five real environment pairs through a customer-run collector. Success requires actionable findings and three paid pilots; each customer must explain the recurring review decision they would pay to preserve. Kill or narrow if 8 of 10 discovery conversations say their current manager solves the problem, teams refuse even sanitized metadata, or approvals become routine blanket suppressions. A local free comparator and incident-focused engineering content are testable channel hypotheses, not validated acquisition channels.

## Core journey and scope

1. Run a local collector with a project-specific customer-held fingerprint key. It reads explicitly selected settings and outputs presence plus keyed fingerprints, never values. Empty onboarding starts with two sample manifests and an explanation of comparison scope.
2. Import a pair with matching schema, project namespace, key version and capture window. Show a freshness warning if one side is stale; incompatible key versions block comparison.
3. Read the side-by-side key roster. Missing keys are separate from differing values. Matching fingerprints indicate equality, not correctness or security.
4. Fix a missing key using the customer's existing tools. A later manifest can show presence; it cannot certify that the value is correct. A new difference still requires review.
5. Approve an intentional difference with a reason and bounded expiry. Approval binds to that exact pair of fingerprints. If a value changes, the previous approval becomes history and the new pair returns to review.
6. Export the comparison and decision history for the release record. No automatic deployment gate is required in the pilot.

MVP: one versioned collector schema, read-only local manifests, two-environment comparison, missing/different/approved/matching states, owner label, expiring approvals and JSON export. Non-goals: secret management, runtime configuration delivery, cloud writes, automatic propagation, value viewers, remote command execution, secret scanning, policy correctness, feature-flag targeting or deployment orchestration.

Failure states: invalid/oversized manifest rejected before persistence; key-version mismatch blocks equality claims; stale/missing collector run remains visible; empty manifest cannot imply everything matches. Conflicts: approval uses an expected comparison version; if a newer manifest arrives concurrently, return `409` with the new pair. Duplicate imports return their original result. Missing keys cannot be approved as intentional differences in the initial product; a distinct optional-key policy would require explicit future design.

## Domain entities and invariants

| Entity     | Required fields                                                   | Invariant                                                                |
| ---------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Project    | Tenant, environment roster, collector namespace                   | Membership and tenant scope are server-derived                           |
| Manifest   | Environment, schema/key versions, collector run, capture time     | Immutable; same logical run cannot contain changed content               |
| KeyEntry   | Canonical key name, presence, keyed fingerprint                   | No raw value; absence differs from an empty value                        |
| Comparison | Two manifest IDs, computed key states                             | Compare only compatible namespaces and key versions                      |
| Approval   | Key, environment pair, exact fingerprints, reason, expiry, author | Change, expiry or revocation returns the difference to review            |
| AuditEvent | Actor, action, comparison version, timestamp                      | Append-only decision history; never a substitute for the source manifest |

Case sensitivity and duplicate-key handling are explicit collector policies, not accidental platform behavior. Preserve “present with empty value” as a state distinct from missing; its acceptability belongs to a policy decision. A matching pair does not mean its value is the right value. An approved difference does not imply production readiness. A new comparison must not silently reuse an approval from another key, environment pair or fingerprint-key version.

## Proposed contracts and jobs

These routes and events are proposed product interfaces, not available SDK APIs:

| Route                                                | Behavior and authorization                                                   |
| ---------------------------------------------------- | ---------------------------------------------------------------------------- |
| `POST /api/projects/{id}/manifests`                  | Collector credential; bounded schema, 256 KB per manifest, no values allowed |
| `POST /api/projects/{id}/comparisons`                | Editor selects two compatible immutable manifests                            |
| `GET /api/projects/{id}/comparisons/{comparisonId}`  | Tenant member reads status and evidence                                      |
| `PUT /api/comparisons/{id}/keys/{keyId}/approval`    | Reviewer supplies reason, expiry and expected version                        |
| `DELETE /api/comparisons/{id}/keys/{keyId}/approval` | Reviewer revokes with expected version and audit reason                      |
| `GET /api/projects/{id}/exports?comparisonId=...`    | Tenant member exports metadata and review decisions                          |

Import idempotency uses `(projectId, environmentId, collectorRunId)` and a canonical digest. Identical replay returns the same manifest; changed content under that identity returns `409`. Approval checks and insertion occur transactionally against the current pair. Proposed events: `ManifestRecorded`, `ComparisonChanged`, `DifferenceApproved`, `ApprovalInvalidated`, `ApprovalExpired`, `ApprovalRevoked`. A persisted worker evaluates expiry/freshness hourly, emits a deduplicated optional digest and prunes old manifests. Historical audits remain linked to manifest identifiers rather than mutating earlier comparisons.

A small ASP.NET Core API with a relational store is sufficient for the narrow control plane. Hosted workers are a supported .NET building block; durable jobs, leases and replay rules are product responsibilities. [Microsoft hosted-service documentation](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/host/hosted-services?view=aspnetcore-10.0). Begin with persisted work in the same database; introduce another queue only when measured throughput warrants it.

## Fingerprint design and security boundary

Proposed collector design: HMAC-SHA-256 with a random customer-held project key over an unambiguous, length-prefixed encoding of namespace, canonical key name and value bytes. Use the same fingerprint-key version across the two compared environments; do not include the environment name in the equality payload. Microsoft documents `HMACSHA256` as a keyed hash primitive. The fingerprint protocol, canonicalization and threat model here are our design proposal and require security review, not a vendor-endorsed protocol. [Microsoft HMACSHA256 documentation](https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.hmacsha256?view=net-10.0).

Plain hashes of low-entropy settings permit dictionary guesses. A customer-held HMAC key reduces that exposure, but fingerprints still reveal equality and changes. Key names, project names and timing can also be sensitive. Keep the HMAC key entirely outside the hosted service; separate it from upload authentication tokens. Rotate with an explicit key version and rebaseline both manifests, invalidating approvals. Compare full fingerprints internally; shortened previews are for display only. Never make a cryptographic security decision from the mock's strings.

Ownership: values and collection stay with the customer; hosted metadata belongs to that customer and is exportable/deletable. Ingest token scope includes project and environment. Rate limits, strict payload allowlists and server-derived tenant checks apply everywhere. Default diagnostic logs contain identifiers and error codes, not incoming payloads. Do not put a general-purpose `.env` upload or secret-value text field in the web UI. Review notes can themselves contain secrets, so labels must warn against pasting them and retention/deletion must cover them. No promise that text fields automatically prevent accidental disclosure.

The mock uses visibly synthetic strings such as `sample-a41c`, has no cryptography or manifest upload, and stores user-entered review notes locally. Its simulated fix changes only local state; it does not touch an environment.

## Vue/.NET and WoW2 SDK boundaries

Vue owns pair selection, state labels, metadata display, approval dialogs and local export. .NET owns canonical comparison, authorization, version checks, expiry and audit records. The collector owns reading values and producing fingerprints. Split the domain comparator from CLI and HTTP transport so protocol fixtures test the same invariants everywhere.

The installed public `@wow-two-beta/ui-vue` 0.0.7 declarations were inspected. `Button`, `DiffViewer`, `Modal` and `DateInput` are exported. Production may use these for bounded display and forms, but no configuration comparator or secret-handling abstraction is claimed to exist. The mock uses a semantic table because the comparison is key-oriented, not a line-by-line text diff. Existing WoW2 backend package exports and the chosen repository's tenant/auth conventions must be verified before implementation; no backend method names are assumed.

## Monetization, budget and expansion

Proposed free: unlimited local comparisons without hosted persistence. Proposed paid: $39/month organization history, expiring approval decisions, owner context and an optional digest, capped at 20 environments, 200 manifest imports/day and 30-day raw manifest history. Retain summarized decision history for a clearly bounded period. Avoid lifetime hosted-history promises; an offline license is a separate later experiment.

Planning estimate: $20–35/month early infrastructure, comprising $12–20 app/database allocation, $4–6 backup/log retention and $4–9 domain/delivery allowance. These are estimates rather than supplier quotes; founder labor, payment fees, taxes and customer compute are excluded. No LLM, cloud polling or hosted secret store is needed. Enforce quota limits before oversized storage accumulates. A ~$300/month budget is available only after products earn and measured capacity or paid requirements justify expansion.

Activation is one missing/unexplained key found and resolved with a fresh manifest. Retention is a second release or environment review that updates meaningful approvals; imported manifests alone are a vanity metric. Three paid pilot commitments are the initial gate. At $39/month, 129 organizations produce $5,031 gross MRR before fees, taxes, refunds or churn. No evidence currently establishes the required acquisition or retention rates.

## Design references and rationale

[ConfigCat's pricing/features page](https://configcat.com/pricing/) describes environments, audit records and mandatory reasons for changes. The extracted conceptual move is “decision plus explanation plus history.” This is source-text evidence, not an inspection of its logged-in interface. The side-by-side columns, selected-key decision card and audit strip are original design proposals focused on comparing two states. [Vue computed properties](https://vuejs.org/guide/essentials/computed.html) support deriving visible totals from underlying keys rather than maintaining separate counters.

Screens: key comparison roster; missing-key detail; unapproved difference detail; approval form; approved difference with revoke control; simulated manifest receipt form; changed-fingerprint review; decision trail. At mobile widths the table scrolls inside its panel and detail stacks below. At 1024 px the detail card stays beside the comparison. Every row includes a text state as well as semantic color. The environment labels remain visible above the data so the direction of comparison is explicit.

| Semantic token               | Light meaning                                      | Dark meaning                           |
| ---------------------------- | -------------------------------------------------- | -------------------------------------- |
| `--surface`, `--surface-alt` | Comparison panel and supporting context            | Separated low-glare panels             |
| `--ink`, `--muted`, `--line` | Key identity, fingerprint context, column boundary | Equivalent readable hierarchy          |
| `--accent`, `--accent-soft`  | Current key and primary decision                   | Same meaning with shell palette values |
| `--danger`, `--warning`      | Missing key / unreviewed difference                | Same meanings with text labels         |
| `--success`                  | Matching state or accepted review panel            | Never a claim of deployment safety     |

Proposed reusable controls: key-presence badge, fingerprint preview, comparison-pair header, reason/expiry approval form and append-only decision trail. Root's light/dark and three palette variants remain proposed, not locked designs.

## Staged delivery and acceptance

1. Test five customer-run manifest pairs using a disposable local comparator. Verify actionable findings and metadata willingness before hosted implementation.
2. Build the collector protocol with canonicalization, absent/empty distinction, namespace/key version handling and known-answer cryptography tests.
3. Build immutable ingest and comparator, then review UI with optimistic concurrency and expiry. Exercise incompatible manifests, duplicate imports, race conditions and tenant isolation.
4. Add history/digests and billing after paid-pilot commitments. Complete deletion, backup restore, key-rotation and audit-integrity verification before customer metadata hosting.

Acceptance: a missing key cannot be approved away; an approval covers only its exact pair; any new fingerprint or key version reopens review; stale manifests are labeled; all displayed counts and exported counts agree; no secret payload enters hosted logs; keyboard operation and dialog focus work at 390/820/1440 px and both themes. This mock verifies interaction logic only; root owns combined build and browser evidence.

## Exact prototype smoke scenario

Start with the shell's reset for this product.

1. Verify 2 missing keys, 1 difference to review, 1 approved difference and 2 matching keys. `PAYMENT_API_KEY` is selected.
2. Click **Record simulated fix**, then **Confirm simulated manifest** while blank. Validation keeps the dialog open.
3. Enter `sample-run-104` and click **Confirm simulated manifest**. Missing becomes 1, differences becomes 2. The new fingerprint is distinct, so the difference needs review.
4. Click **Approve difference**, then **Save approval** with an empty reason. Validation remains visible.
5. Enter `Separate sandbox and production payment credentials`, retain the future expiry, and click **Save approval**. Differences becomes 1, approved becomes 2.
6. Click **Revoke approval**. Differences returns to 2 and approved to 1.
7. Click **Simulate new manifest**. `DATABASE_URL` is selected; its original approval no longer applies. Differences becomes 3 and approved becomes 0.
8. Click **Export comparison**. The JSON summary is missing 1, review 3, approved 0, matching 2; audit includes the fix, approval, revocation and changed manifest.
9. Refresh and verify the four audit events persist; reset returns the initial pair.

Implemented mutations: simulated missing-key resolution, reason/expiry approval, revocation and a changed-manifest simulation. Detail, review filtering, validation, derived counts, local export and persistence work through the shell API. Actual collection, hashing, network ingestion, authentication, cloud changes and billing remain unimplemented.
