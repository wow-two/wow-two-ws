# Fresh analysis of 100 SaaS products

Research date: 2026-10-05. Decision: which complete software business should receive customer validation before further implementation?

## Execution decision

The user has since selected the existing venture work sequence, including consumer and entertainment products. The [canonical venture product order](../../system/planning/pln-tasks.md#venture-product-order) owns that sequence and its current product. This report's B2B ranking remains research; it is not the active build queue. The follow-up [subscription-speed comparison](subscription-speed.md) compares the ten finalists with the existing ventures.

## Recommendation

Validate **S052 — Migration delivery workspace** first under an engineering-led founder assumption. Compare **S094 — B2B receivables and dispute operations** as a second, commercially different path. Both can plausibly support a $149/month workspace hypothesis; neither has demonstrated demand for our version. Keep a third product slot uncommitted until buyer access and paid repeated use are known.

Migration delivery combines a coherent client-facing operating record with bounded hosting and repeat consultancy customers. It ranks first under both acquisition-heavy and implementation-heavy scoring. Receivables has the highest base-weighted final score because an identifiable finance owner repeatedly deals with unpaid invoices; its main uncertainty is whether buyers want software or collection labor. The founder’s access to either buyer group is unverified, so actual access can reverse the order.

The completed desk-research funnel is **100 candidate products → 100 independent challenges → 12 discovery candidates → 10 focused finalists**. The remaining 42 are Reserve and 46 are Defer. These statuses are decisions under the stated constraints, not success probabilities. No interviews, outreach, paid pilots, demand tests or new implementations were performed.

## Read the work

- [All 100 products, ranked](ranked-100.md): comparison with prices, account targets, cost envelopes and alternative ranks.
- [All 100 detailed dossiers](catalog-100.md): buyer, value, full workflow, competition, distribution, risks, pricing, MVP and kill gate.
- [Official evidence register](evidence-register.md): links and observed price qualifications.
- [Research protocol](research-protocol.md): weights, evidence rules and financial definitions.
- [Structured dataset](products.json): all records and review history.
- [Review and scope audit](review-log.md): removed overlaps, limitations and unproven boundaries.

## What changed from the earlier micro-SaaS approach

Existing prototypes received no bonus. The unit is an ongoing business process with a persistent record, connected stages, multiple roles and a recurring budget owner. A narrow first release remains sensible, but it must complete a valuable cycle. A checker, standalone generator, reminder or dashboard does not qualify merely because additional screens can be imagined.

The pool deliberately emphasizes B2B and professional organizations because the objective is $5,000 MRR with a small number of products and modest cash spending. It covers service businesses; education and digital publishing; technical/data operations; and finance, customer operations and governance. It is not an exhaustive search of consumer, gaming, collector or social opportunities. Five duplicate or overly similar entries were replaced during review. Adjacent products still share channels and infrastructure; 100 hypotheses are not 100 independent bets.

## Ten finalists for validation

Ordered by final score among candidates that passed the qualitative discovery gate. This deliberately skips higher-scoring Reserve entries whose specific switching advantage remains too weak. “Validate” means compare real workflows and seek paid repeated use; it does not mean build ten products.

| Priority | Product and payer | Score | Proposed USD/mo | Accounts for $5K MRR |
|---:|---|---:|---:|---:|
| 1 | [S094 — B2B receivables and dispute operations](catalog-100.md#s094) | 76 | $149 | 34 |
| 2 | [S052 — Migration delivery workspace](catalog-100.md#s052) | 74 | $149 | 34 |
| 3 | [S080 — Policy and control operations for small B2B firms](catalog-100.md#s080) | 72 | $129 | 39 |
| 4 | [S090 — RFP and bid response operations](catalog-100.md#s090) | 72 | $199 | 26 |
| 5 | [S055 — External UAT acceptance workspace](catalog-100.md#s055) | 71 | $99 | 51 |
| 6 | [S039 — Newsletter sponsorship revenue operations](catalog-100.md#s039) | 71 | $149 | 34 |
| 7 | [S040 — Editorial commissioning for content agencies](catalog-100.md#s040) | 71 | $129 | 39 |
| 8 | [S029 — B2B course-license account operations](catalog-100.md#s029) | 70 | $199 | 26 |
| 9 | [S009 — Localization agency production operations](catalog-100.md#s009) | 68 | $149 | 34 |
| 10 | [S013 — Remote back-office service operations](catalog-100.md#s013) | 68 | $199 | 26 |

### 1. S094 — B2B receivables and dispute operations

**Buyer:** Finance manager at a 10–100-person B2B agency or consultancy **Payment hypothesis:** Finance teams could pay to resolve invoice disputes, assign the missing action and reconcile settlement.

**SaaS scope:** Payment reminders are already bundled elsewhere. The distinct record must connect the unpaid invoice to the actual disputed deliverable, agreed action and accepted settlement.

**Competitive check:** [Chaser](https://www.chaserhq.com/chaser-pricing) — Compact supports receivables workflows and four users; Care adds human collection services separately. [Upflow](https://upflow.io/pricing) — Starter includes collections communication, analytics, accounting integrations and unlimited seats. Discover provides free AR dashboards; paid plans scale by gross invoice value and invoice volume.

**Argument against building:** Strong discovery candidate with identifiable finance ownership, but concierge resolution can confound software value with collection labor. Require enough recurring disputed invoices and measure owner follow-through and reconciliation, not recovered cash alone. Upflow also provides AR collaboration, integrations and free insights, further narrowing the entry. The distribution score four is ahead of evidence: accountants are a proposed channel with no demonstrated referrals. No automated outreach should occur in this research.

**Decisive test:** During discovery, separate three buyer groups: firms with frequent disputed service invoices, firms with late-but-undisputed invoices, and firms wanting outsourced collection labor. Only the first tests this proposition.

**Delivery envelope:** 10–16 full-time builder-weeks; estimated pilot cash $20–50/month with stated quotas. These are unmeasured estimates, excluding acquisition, support labor and assurance work. **Stop:** Stop if reminder automation alone is valued or mandatory integrations exceed first-cohort demand

### 2. S052 — Migration delivery workspace

**Buyer:** Owner of a small CRM/ERP migration consultancy **Payment hypothesis:** Migration consultancies could pay to reduce unpaid rework and obtain clear client acceptance.

**SaaS scope:** A complete engagement joins source inventory, mapping revisions, exceptions, dry-run control totals and cutover acceptance. A spreadsheet importer alone does not own this business process.

**Competitive check:** [Flatfile Projects](https://flatfile.com/pricing) — Independently reopened: project-volume pricing, unlimited invited users, mapping, correction and approval in collaborative workspaces. It explicitly serves NetSuite and Workday partners. [Dromo](https://dromo.io/pricing) — Independently reopened: embedded/headless import, validation, mapping and private mode; adjacent to full migration engagement management.

**Argument against building:** Best developer-lane test: repeat consultancy delivery supplies a budget owner and client acceptance record. Flatfile already combines correction and collaborative approval, while Dromo is an importer rather than proof of demand for a separate workspace. Require two paid engagements per firm and a measurable reduction in unpaid reconciliation; reject bespoke transformation services.

**Decisive test:** Test consultancies that repeatedly deliver migrations, not companies performing one migration. Require a customer data owner to approve real reconciliations and a second engagement to reuse the record.

**Delivery envelope:** 8–12 full-time builder-weeks; estimated pilot cash $20–50/month with stated quotas. These are unmeasured estimates, excluding acquisition, support labor and assurance work. **Stop:** Stop if fewer than three pay or buyers demand bespoke transformations rather than repeatable software.

### 3. S080 — Policy and control operations for small B2B firms

**Buyer:** Operations director at a 30–150-person client-audited service firm **Payment hypothesis:** Operations teams could pay to connect approved policies to recurring control work and evidence.

**SaaS scope:** The core is policy version → assigned control run → exception → review → evidence export. Certification badges or a document wiki alone do not satisfy the proposition.

**Competitive check:** [SweetProcess](https://www.sweetprocess.com/) — Platform connects policies, procedures, tasks, manager approval and version history. [Process Street](https://www.process.st/pricing/) — Lists document/policy control and workflow operations, with approvals, enforced task order, role assignments, scheduled workflows and workflow revisions.

**Argument against building:** A worthwhile validation candidate, but Process Street already combines policy/document control with workflow execution, approvals and permissions. This new comparison weakens the claimed policy-to-execution distinction. Test three concrete recurring controls and evidence lineage against configured incumbents, not a static wiki. Consultant introductions remain unverified; consultant setup labor must be separated from software value. Validate means discovery and paid-pilot testing, not build approval.

**Decisive test:** Require customers to show recurring work that stays unowned or cannot be tied to a policy version in their current tools. Human reviewers retain framework interpretation.

**Delivery envelope:** 8–14 full-time builder-weeks; estimated pilot cash $20–50/month with stated quotas. These are unmeasured estimates, excluding acquisition, support labor and assurance work. **Stop:** Stop if teams only need a static policy library or cannot distinguish this from their wiki

### 4. S090 — RFP and bid response operations

**Buyer:** Bid lead at a B2B service company submitting 5–20 complex bids per quarter **Payment hypothesis:** Bid teams could pay to complete concurrent proposals with approved, current evidence.

**SaaS scope:** Own qualification, requirement responsibility, controlled answer reuse, exception review and submission readiness. AI text generation is an optional capability, not the business.

**Competitive check:** [Loopio](https://loopio.com/pricing/) — Foundations lists 10 seats, unlimited projects and library entries, review workflows and role controls. [Responsive](https://www.responsive.io/pricing) — Emerging edition lists unlimited response projects, content/collaboration, integrations and access controls. Platform subscription is annual; user licenses and add-ons are separate components.

**Argument against building:** A reasonable discovery candidate because recurring bids create a clear owner, reusable evidence and expensive coordination. The second source confirms formidable direct competition: Responsive sells centralized content and collaboration even to emerging proposal teams. No extra penalty beyond the existing wedge/feasibility discount. A pilot must include document roundtrip, exception approval and final submission assembly, and quantify reduced review work rather than AI draft volume.

**Decisive test:** Replay an actual redacted bid in the current tool and the proposed workflow. Measure late expert responses, outdated answers and assembly rework; do not promise win-rate improvements from a tiny pilot.

**Delivery envelope:** 10–16 full-time builder-weeks; estimated pilot cash $20–50/month with stated quotas. These are unmeasured estimates, excluding acquisition, support labor and assurance work. **Stop:** Stop if buyers value draft generation only or require bespoke document parsing per bid

### 5. S055 — External UAT acceptance workspace

**Buyer:** Delivery director at a 5–30-person software agency **Payment hypothesis:** Software agencies could pay to turn client testing into version-bound release acceptance.

**SaaS scope:** Agree business scenarios, collect guest results, track defects and retests, and preserve the final release decision. A bug-report form alone fails the SaaS scope test.

**Competitive check:** [Testmo](https://www.testmo.com/pricing/) — Test cases, runs, milestones, results and issue-tracker integrations. [Qase](https://www.qase.io/pricing/) — Test reviews, requirements traceability and history; free tier targets learning/nonprofit uses.

**Argument against building:** Occasional client testing is a plausible buyer-specific workflow, but closer competitor Marker.io already provides free accountless reporters and UAT/approval features. Testmo is also inexpensive. Validate version-bound business acceptance, not generic screenshot collection: require repeat client participation and three second-cycle payments.

**Decisive test:** Buyers must release to external clients repeatedly and obtain a second-cycle payment. Treat this as an alternative entry to the delivery family, not an automatic second app beside migration delivery.

**Delivery envelope:** 6–10 full-time builder-weeks; estimated pilot cash $20–50/month with stated quotas. These are unmeasured estimates, excluding acquisition, support labor and assurance work. **Stop:** Stop if participation stays in email or fewer than three agencies pay for the second cycle.

### 6. S039 — Newsletter sponsorship revenue operations

**Buyer:** Publisher revenue lead running 3–10 newsletters with direct sponsor relationships. **Payment hypothesis:** Multi-newsletter publishers could pay to reconcile sponsor packages, delivery exceptions and billing.

**SaaS scope:** Own the sponsor campaign record across reserved placements, approved creative, proof, make-goods and the billing adjustment. Selling advertisers is explicitly outside the product.

**Competitive check:** [Passionfroot](https://www.passionfroot.me/creator-pricing) — Direct creator-sponsorship alternative provides a booking and collaboration workflow; marketplace sourcing is optional to the competitor model. [Letterhead Studio Revenue](https://www.tryletterhead.com/revenue.html) — Direct competitor already supplies sponsorship inventory, scheduled placements, per-send revenue and proof-of-publication reports over existing email providers.

**Argument against building:** Letterhead already spans inventory through proof, and Passionfroot offers a zero-subscription entry. Test only documented multi-publication make-good and billing exceptions; ordinary sponsor administration is insufficient differentiation.

**Decisive test:** Start with publishers already closing direct sponsor deals across several publications. If standard Letterhead or Passionfroot configuration handles the real exceptions, reject the idea.

**Delivery envelope:** 8–14 full-time builder-weeks; estimated pilot cash $25–45/month with stated quotas. These are unmeasured estimates, excluding acquisition, support labor and assurance work. **Stop:** Stop if existing vendors handle exceptions adequately or prospects need us to source advertisers.

### 7. S040 — Editorial commissioning for content agencies

**Buyer:** Managing editor of a 5–20-person content agency using freelance contributors. **Payment hypothesis:** Content agencies could pay to control editorial revisions, contributor cost and client acceptance.

**SaaS scope:** The commission joins brief version, contributor commitment, review rounds, approved scope, delivery acceptance and margin. This is an operating product only if those decisions change economics.

**Competitive check:** [Bynder Content Workflow](https://support.bynder.com/hc/en-us/articles/14788733803922-Get-Started-with-Content-Workflow) — Direct editorial alternative structures projects, content items, templates, roles and configurable draft-to-publication workflows; supports content exports. [ManyRequests](https://www.manyrequests.com/pricing) — Includes client portal, requests, time tracking, billing and reporting; Pro adds workload management.

**Argument against building:** ManyRequests bundles requests, billing, time and a client portal. Editorial commissioning merits a distinct product only if versioned brief, contributor cost and acceptance materially change margins beyond configurable project tools.

**Decisive test:** Replay one profitable and one overrun commission. Identify exactly which approval or scope change caused extra cost; a prettier board is not a paid advantage.

**Delivery envelope:** 8–14 full-time builder-weeks; estimated pilot cash $25–45/month with stated quotas. These are unmeasured estimates, excluding acquisition, support labor and assurance work. **Stop:** Stop if agencies cannot link approval/scope failures to margin loss.

### 8. S029 — B2B course-license account operations

**Buyer:** Owner or account director of an established course publisher selling to employers. **Payment hypothesis:** Course publishers could pay to reconcile corporate licenses and renewals across learning systems.

**SaaS scope:** Own the corporate agreement, seat allocation, entitlement changes, completion evidence and renewal. The course player remains in the customer LMS.

**Competitive check:** [Thinkific](https://www.thinkific.com/pricing/) — Direct B2B course-selling competitor: Grow includes group orders, bulk seat purchases, invoicing, API/webhooks and engagement tools. [LearnWorlds](https://www.learnworlds.com/pricing/) — Direct competitor: Learning Center supports ten client groups, scheduled reports and white labeling; Corporate offers larger groups and flexible invoicing.

**Argument against building:** Cross-LMS contract reconciliation is unproven, while Thinkific and LearnWorlds already monetize B2B groups. Validate only publishers running multiple systems and repeated corporate renewals; single-LMS buyers do not establish this market.

**Decisive test:** This depends on a narrower segment than all course creators: established publishers with multiple actual systems and employer contracts. Five single-LMS customers cannot validate it.

**Delivery envelope:** 8–14 full-time builder-weeks; estimated pilot cash $25–45/month with stated quotas. These are unmeasured estimates, excluding acquisition, support labor and assurance work. **Stop:** Stop if fewer than three prospects actually use multiple systems or incumbents already reconcile their contract terms.

### 9. S009 — Localization agency production operations

**Buyer:** Operations owner, 2–8-manager translation agencies **Payment hypothesis:** Localization agencies could pay to reconcile job versions, supplier rates, review acceptance and payables.

**SaaS scope:** Own the localization order through language-pair allocation, approved counts/rates, review and delivery. Translation generation and a new translator marketplace are unnecessary.

**Competitive check:** [Protemos](https://protemos.com/prices.html) — Agency pricing is per concurrent manager; unlimited manager, client and vendor accounts can be created. [Plunet](https://www.plunet.com/en/pricing/) — AgencyStart starts with two full users and 50 concurrent freelancer/client licenses; higher plans offer CAT interfaces.

**Argument against building:** Suitable for comparative discovery because order, vendor job, rate and acceptance form a coherent financial workflow. However Protemos, Plunet and XTM already cover the proposed lifecycle, including portals and vendor management. Rate-version transparency must beat an incumbent configuration, not merely spreadsheets. Test analysis-file portability before promising a CAT-neutral system.

**Decisive test:** Use actual CAT analysis files and a rate-change exception. Protemos, Plunet and XTM are direct comparisons; neutrality across tools must save work instead of adding another import.

**Delivery envelope:** 14–22 full-time builder-weeks; estimated pilot cash $20–50/month with stated quotas. These are unmeasured estimates, excluding acquisition, support labor and assurance work. **Stop:** Stop if Protemos configuration resolves the issue or buyers require several live CAT connectors first.

### 10. S013 — Remote back-office service operations

**Buyer:** Operations director, 5–30-person remote data-processing service firms **Payment hypothesis:** Remote back-office providers could pay to connect accepted work units and rework to billing.

**SaaS scope:** A service order governs inputs, processing, quality review, exceptions, accepted-unit counts and closeout. The customer supplies the workers and processing systems.

**Competitive check:** [Moxo](https://www.moxo.com/pricing) — Offers workflow builder, milestones, approvals, forms, decisions and file requests; adjacent configurable workflow substitute. [Process Street](https://www.process.st/pricing/) — Offers workflow runs, forms, approvals, enforced task order and role assignments; configurable substitute.

**Argument against building:** The strongest business-lane discovery candidate: accepted units and rework connect operational decisions to billing. Enterprise process products already support portals, approvals and routing, so they are substitutes rather than proof of a gap. The catalog-maintenance niche must share a stable unit and exception model across three providers; reject any need for customer-specific processing engines.

**Decisive test:** Choose one unit model such as catalog-data maintenance. Require three providers to use the same basic exception and acceptance model without a bespoke execution engine.

**Delivery envelope:** 14–22 full-time builder-weeks; estimated pilot cash $20–50/month with stated quotas. These are unmeasured estimates, excluding acquisition, support labor and assurance work. **Stop:** Stop if each buyer requires a different processing engine or the team must perform the outsourced work.

## Why apparently attractive products moved down

- **Generic onboarding:** Rocketlane already covers customer portals and approvals, while [Dock](https://www.dock.us/pricing) also offers customer workspaces. S083 needs a specific repeated failure those tools leave unresolved.
- **Grant administration:** [Grantseeker](https://grantseeker.io/pricing?lg_redirect=1) supplies a low-cost alternative; comparing only with Instrumentl would overstate room for a $129 product. S086 remains Reserve.
- **Engineering escalation:** [Linear’s Zendesk integration](https://linear.app/docs/zendesk) already connects support and engineering work. S070 needs more than ticket synchronization.
- **Paid newsletters and storefronts:** incumbent platforms already combine publishing, payments and customer access at accessible entry prices. No convincing switching reason emerged for S038/S044.
- **Security enforcement, confidential investigations, regulated cases and billing:** some have strong pain and budget, but assurance, correctness, support and integration requirements defeat a first $20–50 pilot business. Higher revenue can fund reconsideration; $300 hosting alone cannot fund every obligation.

## Paths to $5,000 MRR

These are arithmetic scenarios, not forecasts. Prices are our hypotheses; there are no acquired customers. Counts assume full-price active subscriptions with no discounts or failed payments.

| Portfolio scenario | Calculation | Gross MRR |
|---|---:|---:|
| One $149 product | 34 organizations × $149 | $5,066 |
| Two $149 products | 18 + 18 organizations × $149 | $5,364 |
| Three products at $149, $149 and $129 | 12 × $149 + 12 × $149 + 12 × $129 | $5,124 |
| One $199 product | 26 organizations × $199 | $5,174 |
| One $99 product | 51 organizations × $99 | $5,049 |

MRR is not profit. Payment fees, refunds, acquisition, support, taxes and infrastructure reduce what remains. At an illustrative 3% monthly logo churn, 34 accounts require roughly one replacement customer each month merely to hold the account base; this is a stress scenario, not a churn benchmark. Lifetime and setup payments add cash but contribute no MRR.

Launching 100 paid-hosted products at $20–50 each already implies $2,000–5,000 monthly infrastructure spending before labor or acquisition. The better path under this target is one complete workflow, repeated paid use, then a second product only when its distribution and support burden can be funded. Keep the 100-product catalog as options, not a simultaneous build queue.

## Pricing and product boundaries

| Model | Recommendation | Conditions |
|---|---|---|
| Monthly subscription | Default for shared operational records | Start with organization/workspace pricing, bounded active cases and storage; charge for recurring workflow completion. |
| Annual subscription | Offer after repeated use is demonstrated | Show the full annual commitment; any discount must leave room for support and costs. |
| Freemium | Selective, capped acquisition product | One sample workflow, small record quota or solo tier; measure support and activation. Free users alone are not validation. |
| Lifetime | Finite/offline capabilities only initially | Templates, local utilities or bounded prepaid usage; never assume a one-time payment funds unlimited hosted collaboration. |
| Setup/migration fee | Separate where real onboarding work exists | Charge and measure services separately; do not count service revenue as subscription MRR. |
| AI/paid APIs | Optional metered add-on after revenue | Keep deterministic core workflows usable; observe unit cost before allowing usage above the initial budget. |

A lower price is not a durable entry strategy by itself. The initial claim must be a workflow outcome the buyer cannot achieve economically with its existing tools. Price testing should compare that outcome and support burden, not merely undercut a published incumbent package.

## Budget interpretation

78 candidates have a stated pilot cash envelope at or below $50/month. That count means **an engineering hypothesis for capped test usage**, not verified production feasibility. The other 22 exceed the envelope before considering excluded costs. Individual dossiers define users/organizations, records, files, communication or execution boundaries; root operations candidates now have explicit aggregate quotas.

At $20–50, assume simple structured records, tightly bounded attachments and transactional email, customer-owned heavy compute, and no expensive data licenses or always-on AI. After paid usage, up to approximately $300 can fund measured database, backup, observability and integration growth. Independent security review, specialist legal work, custom migration and substantial human support are separate costs. A product requiring those before its first customer remains gated even if its database bill is small.

Global means remotely distributable software, not immediate legal or commercial readiness in every country. Begin with an English-language, clearly defined buyer segment. Entity/payment-provider eligibility, tax treatment, contractual data handling, residency requirements and localization need a separate launch check for the chosen product and selling entity; this research does not establish those arrangements.

## Three analysis iterations and uncertainty

1. **Product and evidence qualification:** four lanes generated 25 candidates each. Every final record has an identifiable buyer, a persistent record, at least three workflow stages, roles, a price hypothesis, a channel test and a kill gate. 136 distinct official source URLs were opened across candidate research and review. Numeric prices keep billing, currency or selector uncertainty explicit.
2. **Independent challenge:** a researcher other than the author challenged every record. Five overlapping concepts were replaced and reviewed; incomplete value loops and weak pilot quotas were corrected. Penalized risks and rejected wedges remain in the dataset.
3. **Shortlist and sensitivity:** the 10 finalists each have at least two competitor vendors represented. Alternate weights emphasize acquisition or delivery feasibility. Qualitative gates override a high numerical score; a high Reserve score is not a hidden build recommendation.

| Candidate | Base-weighted rank | Acquisition-heavy rank | Feasibility-heavy rank |
|---|---:|---:|---:|
| S052 — Migration delivery workspace | 3 | 1 | 1 |
| S094 — B2B receivables and dispute operations | 1 | 2 | 7 |
| S055 — External UAT acceptance workspace | 10 | 3 | 2 |
| S080 — Policy and control operations for small B2B firms | 6 | 11 | 8 |
| S039 — Newsletter sponsorship revenue operations | 11 | 6 | 4 |
| S009 — Localization agency production operations | 16 | 18 | 26 |
| S013 — Remote back-office service operations | 18 | 34 | 31 |

The ranking is ordinal judgment. Differences of a few points should be treated as the same broad tier. Reviewer penalties are not statistically calibrated and some risks overlap the base dimensions; this is a limitation of the screening, not quantified confidence. The strongest directional result is migration delivery remaining first under both alternate priorities. BPO and localization drop when acquisition or feasibility receives more weight, so they should not displace an accessible candidate solely on workflow appeal.

We verified competitor offers and observed pricing, not category market size, competitor revenue, buyer search volume, our conversion, CAC, retention or an underserved market. No TAM or success probability is invented. Existing-source accuracy is bounded by the opened pages; quote-based and conflicting dynamic prices remain unconfirmed. All channels are hypotheses until buyers are actually reached.

## First validation cycle

1. **Confirm buyer access.** Start with migration consultancies unless finance/accounting access is materially stronger. Build a list of qualified budget owners using authorized public or existing contacts; any outreach is a separate execution step.
2. **Observe ten qualified buyers.** Ask for the last completed workflow, the cost of its failures and the current tools. Count organizations with an actual repeat process, not developers expressing interest.
3. **Replay five customer artifacts.** Use redacted or permissioned data. Reproduce the workflow in both the current incumbent and a lightweight proposed flow; demonstrate where the latter removes work. Avoid importing live sensitive datasets before appropriate controls exist.
4. **Seek three paid pilots.** Present a concrete $149/month offer and full manual/software boundaries. A letter of intent is weaker than payment, and a paid concierge service is not automatically SaaS MRR.
5. **Require repeated use.** The buyer and external participant should complete another cycle without the founder doing the core work. Record support time, active usage, renewal/payment and correctness.
6. **Choose one build.** Proceed only if the same product solves all three pilots without bespoke processing. Stop or revise when the listed kill gate appears. The numerical targets here are internal decision rules, not industry benchmarks.

## Completed scope and pending decisions

- Completed: fresh 100-product research, official category/pricing evidence, economics, independent challenge, scoring sensitivity and a ten-product shortlist.
- Completed: all research outputs saved locally; previous product prototypes and runtime state were not changed.
- Pending: founder buyer access, actual paid-demand evidence, measured operating costs, legal/payment launch details for the selected product and the decision to build.
- Separate earlier objective: this turn completes a fresh 100-product exercise; it does not claim the earlier requested 1,000-to-100 funnel was completed.
