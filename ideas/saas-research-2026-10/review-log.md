# Research review and scope audit

Research date: 2026-10-05. This is an audit of the research deliverable, not evidence that any proposed business has customers.

## Ownership and review

| Author lane | Final IDs | Independent reviewer | Review artifact |
|---|---|---|---|
| Business research agent | S001–S025 | Developer research agent; root reviewed replacement S018/S020 | [Business review](artifacts/review-business.json) |
| Creator research agent | S026–S050 | Root | [Creator review](artifacts/review-creator.json) |
| Developer research agent | S051–S075 | Creator research agent | [Developer review](artifacts/review-developer.json) |
| Root operations research | S076–S100 | Business research agent | [Operations review](artifacts/review-operations.json) |

The root integrated all records and reviewed cross-lane overlap, the shortlist, revenue arithmetic and evidence boundaries. The developer research agent performed an additional whole-catalog schema and overlap audit. Reviews are independent passes by collaborating models, not independent customer or domain-expert validation.

## Replacements

Five entries were replaced rather than counted twice under different buyer labels. Each replacement received fresh official-source evidence and a completed record.

| ID | Removed overlap | Final candidate | Distinct ownership |
|---|---|---|---|
| S018 | Association-management company versus S045 member administration | Private professional community operations | Discussions, moderation cases and curated knowledge; not dues accounting |
| S020 | ISO consultancy controls versus S080 internal policy/control operations | Brand asset lifecycle operations | Approved asset versions, use constraints, distribution and retirement |
| S047 | Association board governance versus S098 board governance | Professional credential lifecycle registry | Applicant evidence, human award, verification status, development evidence and renewal |
| S091 | In-house research evidence versus S010 research consultancy delivery | B2B customer support operations | Customer conversations, support commitments, resolution and reusable knowledge |
| S095 | Cash-planning scenarios versus S014 virtual-CFO planning cycles | Usage-based billing operations | Metered-usage and contract ledger, invoice approval, adjustments and billing close |

S018/S020 are deliberately low-priority candidates after replacement: removing a duplicate is not evidence of finding a better opportunity. S047 is Reserve; S091/S095 are Defer.

## Remaining related families

These are alternative business hypotheses with different records or decisions. They should not be presented as independent market validation or launched together merely because they occupy separate rows.

| Family | IDs | Boundary that must survive discovery |
|---|---|---|
| Customer delivery | S052, S055, S083 | Migration mappings/reconciliation; external release acceptance; general customer implementation dependencies. Choose one entry first. |
| Software support | S051, S070, S091 | Integration recovery; engineering escalation across affected versions; frontline customer support. Buying one does not establish budget for all three. |
| Software access and spend | S059, S060 | Permission fulfillment/revocation versus license-pool invoice and reclamation decisions. Merge if the same workflow and budget solve both. |
| Contract evolution | S064, S067 | External API versions and consumer migrations versus internal datasets, producer ownership and batch-data commitments. Generic version approvals alone do not distinguish them. |
| Recruitment and staffing | S007, S008, S022 | Placement/guarantee; retained research mandate/client calibration; ongoing assignment/time/settlement. Different operating models must be observed. |
| Professional learning governance | S027, S028, S047 | Candidate assessment moderation; provider accreditation; a person’s credential award/renewal record. No statutory authority is assumed. |
| Publishing assets | S020, S041 | Internal brand-asset distribution versus commercial rights availability, licensing terms and usage declarations. |
| Grant operations | S086, S087 | Applicant/award recipient obligations versus funder adjudication and grant portfolio administration. |

No exact repeated name or ID remains. That mechanical result does not establish that customers regard every pair as a separate purchase. The listed boundaries are falsifiable conditions, not reasons to inflate the addressable market.

## Corrections during review

- Operations MVPs originally listed early stages without every closing decision. They now include the complete proposed workflow, including post-award reporting, invoice settlement and experiment outcomes.
- S063 now explicitly coordinates customer-executed maintenance and imports result receipts. It does not promise a hosted remote execution engine or independently guaranteed rollback.
- S072’s MVP explicitly includes a bounded customer-run launcher, preflight checks and versioned receipts for one supported container runtime. Customer-funded compute does not remove compatibility or support risks; the candidate remains Defer.
- Operations pilot assumptions now cap organizations, active cases, child records, aggregate storage, individual file size and monthly transactional email. Limits are hypotheses to measure, not tested system capacity.
- Direct alternatives changed the interpretation of grants, sponsorships and engineering escalation. An expensive competitor alone was insufficient evidence of room for a new product.
- Every numerical top-ten record and every focused shortlist record has at least two competitor vendors represented. Multiple URLs from one vendor are not treated as multiple competitors.
- Final independent report QA checked shortlist order, every account target, portfolio arithmetic, count claims and source links. Categorical payment wording was replaced with explicit hypotheses, particularly for unverified cross-LMS demand.

## Scoring limits

Base weights total 100: pain 20, recurrence 15, budget 15, distribution 15, wedge 15, feasibility 10, global 5 and cost 5. Each score is an ordinal 1–5 judgment. Final score subtracts the recorded review penalty. Ties use distribution, wedge and stable ID.

The acquisition-heavy alternative uses 15/10/10/30/15/10/5/5 in that same dimension order. The feasibility-heavy alternative uses 15/10/10/15/10/25/5/10. Both reuse the same review penalty so the effect of changing weights is visible.

Review penalties reflect different judgments and are not statistically calibrated. Some objections overlap dimensions already discounted in the base score; differences of a few points therefore cannot support a precise ranking claim. Status gates and paid customer evidence should dominate a small numerical difference. Two additional discovery candidates outside the focused ten are S057 accessibility remediation and S008 retained executive search.

## Verified deliverable checks

- Exactly 100 final records: S001–S100, 25 per source lane.
- Required fields present; each record has at least three workflow stages, at least two roles and an opened official source.
- Source observation dates are 2026-10-05; quote-only, conflicting and currency-ambiguous amounts remain qualified.
- Every record has a cross-review decision, a 0–20 penalty with reason, eight 1–5 scores and a positive proposed monthly price.
- Cash-envelope flags match the upper end of their stated ranges. This verifies consistency, not actual hosting cost.
- All $5,000 account counts use the ceiling of 5000 divided by the proposed monthly price.
- [Compiler](artifacts/compile_catalog.py) regenerates the ranked list, dossiers, evidence register and dataset; [report compiler](artifacts/compile_report.py) regenerates the recommendation and focused shortlist.

Final counts and source totals are recorded in [catalog-checks.json](artifacts/catalog-checks.json). No product code, runtime, external account, outreach, purchase, deployment or publication changed during this research.
