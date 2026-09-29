# Business workflow opportunity research

*Last updated: 2026-09-28*

## Status

- Completed 250 manually specified business hypotheses, `W0251`–`W0500`.
- Completed a 75-candidate comparison and 40 desk-research cards using 40 current primary sources.
- All market fit, distribution, willingness to pay, retention and margins remain unvalidated.
- Research and proposed prices are hypotheses; no purchase, outreach or account change occurred.
- Workspace ownership: `wow-two-ws` meta-repository; only `business.json` and `business-notes.md` changed in this lane.

---

## Recommendation

Prioritize recurring B2B coordination errors that have a named owner and visible economic consequences.
The strongest lane hypothesis is an evidence-linked decision workflow around an existing business system:
get a scope change approved, obtain missing invoice evidence, act before a renewal notice deadline,
or prevent a customer escalation from becoming unowned.

A paid incumbent proves an offer exists; it does not prove our smaller product deserves a separate subscription.
The dangerous assumption is that removing features automatically produces a better or cheaper product.
Most of these buyers already have forms, spreadsheets, email, project tools, an ATS or a helpdesk.
A test must compare against a competently configured existing workflow, not an artificially weak manual baseline.

Provisional alternatives after the focused incumbent stress test:

| ID | Candidate | Proposed price | Incumbent boundary to test | Stop condition |
|---|---|---:|---|---|
| W0261 | Renewal notice-window tracker | $29/month | User-entered deadlines across software and service vendors while leaving cards/contracts in existing systems | Existing calendar or contract tool handles the review in under 30 minutes monthly |
| W0276 | Customer commitment ledger | $59/month | Human-acknowledged customer promises across existing CRM/helpdesk links; no roadmap, AI extraction or system migration | Existing CRM tasks consistently capture the same promises and owners |
| W0263 | Procedure recertification queue | $29/month | Review campaign over links in existing wikis rather than document hosting or workflow replacement | Native wiki reminders or Process Street provide sufficient reviews with less setup |

These are low-infrastructure experiment designs, not verified feature gaps. The $20–50 budget refers to
monthly operating spend per product, not the customer's subscription price. Founder access to buyers,
conversion and support cost remain unknown for all three.

`W0251`, `W0284` and `W0286` moved to reserve after direct documentation exposed strong core-feature
overlap. Their detailed stress test appears below. `W0251`, `W0252` and `W0284` share agency distribution
and source data, so they are correlated bets. `W0261` and `W0262` remain one renewal family.


---

## Evidence and price interpretation

`business.json` is the canonical row-level record. `sources` contains exact live URLs, access date,
observed pricing and caveats. Each researched row cites the source IDs and identifies whether the
source supports the direct workflow or only an adjacent category. Screened rows carry no fabricated
source association: `source_ids=[]`, `evidence_fit=none`.

Examples that materially constrain the proposed products:

- [Ignition](https://www.ignitionapp.com/pricing) already offers scope adjustments, billing and proposal renewals.
- [Content Snare](https://contentsnare.com/pricing/) already covers document requests, reminders and answer approval.
- [Help Scout](https://www.helpscout.com/pricing/) has a free plan and native workflows; generic ticketing is a weak wedge.
- [Canny](https://canny.io/pricing) already connects feedback to accounts; customer promises must mean something different.
- [Workable](https://www.workable.com/pricing) combines hiring scorecards, scheduling and HR administration.
- [Dovetail](https://dovetail.com/pricing/) has a free research entry point; a small repository clone has little rationale.
- [Arlo](https://www.arlo.co/pricing) includes organization portals and registration administration.

Price extraction has specific limitations. Several pages expose both billing toggles without identifying
which is active in text. Those prices are labeled ambiguous, not silently annualized. Teamwork's returned
number lacks an explicit currency symbol. Arlo's currency selector was unresolved: the registry preserves
raw dollar-sign values instead of claiming USD. Cledara's page contains inconsistent qualifying-card-use
counts; the conditional free offer is not a dependable zero-cost comparison. ContractSafe, ChartHop,
Teamtailor and other quote-led/selector-led pages do not yield reliable numeric entry prices.

Some narrow hypotheses deliberately remain weakly evidenced despite desk research. `W0285` used adjacent
expense/receivables tools rather than a direct duplicate-payables competitor. `W0274` has adjacent recruiting
workflow evidence, not an accessibility practitioner review. The focused follow-up on `W0286` found direct Scoro and Track & Bill PO tracking; its score and decision were reduced accordingly.
Weak adjacent-source candidates should lose to otherwise comparable direct-evidence candidates in central selection.

No source establishes our addressable market size, actual buyer conversion, revenue, profitability or
retention. Vendor testimonials were not treated as independent measurements. No source access required
creating accounts, sending messages or purchasing subscriptions.

---

## Pricing and operating-budget gates

User budget: $20–50/month per product before revenue, with roughly $300/month per product available
once the first products earn. These are budget ceilings, not measured hosting quotes.

For the first wave, use a deterministic workflow, manual entry or limited CSV import, link-based evidence,
email caps and a small shared hosting deployment. A product requiring enterprise APIs, video transcription,
paid prospect databases, identity verification, organization-wide integrations or large private document
storage before demonstrating value should be deferred.

A $49 subscription needs 103 paying organizations to exceed $5,000 gross MRR. Three $49 products with
35 paying organizations each produce $5,145 gross MRR. This arithmetic excludes payment fees, taxes,
refunds, acquisition, support and infrastructure. It is not a forecast or evidence that these customer
counts are reachable. A $29 product needs 173 paying organizations for $5,000 MRR; a $79 product needs 64.

Subscription is plausible where ownership, expiry, reminders or repeated evidence cycles persist.
Bounded freemium is proposed for handoff exports, procedure review, decision journals and help-article
review. Free users must not receive unlimited files, notifications or human setup help.

Lifetime prices apply only to local or export-oriented tools with bounded obligations, such as a
facilitator timing console or a scenario worksheet. Lifetime cash is not MRR. A hosted product with
indefinite reminders, file retention and support should not use lifetime pricing merely to generate
initial cash. `W0334`, the timezone fairness planner, is a free utility candidate with no assumed direct MRR.

Initial paid pilot requirements:

1. A buyer supplies redacted real workflow examples and names the accountable budget owner.
2. A manual or clickable prototype solves the actual case using the existing baseline for comparison.
3. At least three qualified organizations agree to a priced pilot before a broad build.
4. The same organization uses a second real work cycle; positive interview comments do not qualify.
5. Setup, support, notification and storage costs are measured before projecting margin.

The numerical gates are proposed stop/go criteria, not observed results or statistical significance.
No cold outreach or pilot offers have been sent during this research.

---

## Iteration record

### Pass 1: 250 distinct workflows

Each row has a concrete buyer, recurring job, proposed wedge, model, price, eight integer scores,
plausible acquisition action, strongest failure reason, MVP boundary and falsifiable validation step.
The rows were individually specified; category/buyer noun cross-products were not used.
Related variants retain a shared family when they compete for the same workflow or budget.

### Pass 2: 75-candidate comparison

The comparison contains the 40 purposively chosen research candidates plus the strongest 35 remaining
screened alternatives. This is a broad comparison set, not a claim that the original research choices
were the top 40 by final arithmetic. Some researched candidates fall outside the mechanically highest
75 after scoring; they remain to expose evidence and boundary weaknesses across the lane.
Every compared record carries `iteration2_review` with physical-dependency, family and differentiation checks.

Scores are explicit analyst judgments. No candidate receives reach=5 or wedge=5. Family overlap,
privacy burden, expensive integration requirements and weak source fit can override an attractive total.
Do not change scores merely to make the research subset appear mathematically optimal.

| ID | Candidate | Score /100 | Evidence | Review outcome |
|---|---|---:|---|---|
| W0252 | Retainer allowance evidence | 76 | desk_researched | Central comparison; paid workflow test still required |
| W0254 | Milestone acceptance packet | 76 | desk_researched | Central comparison; paid workflow test still required |
| W0261 | Renewal notice-window tracker | 76 | desk_researched | Central comparison; paid workflow test still required |
| W0276 | Customer commitment ledger | 75 | desk_researched | Central comparison; paid workflow test still required |
| W0277 | Escalation ownership handoff | 75 | desk_researched | Central comparison; paid workflow test still required |
| W0251 | Scope change approval ledger | 74 | desk_researched | Reserve: direct incumbent overlap |
| W0253 | Client evidence collection board | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0256 | Project margin leakage review | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0259 | Client decision delay register | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0262 | Vendor renewal evidence room | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0263 | Procedure recertification queue | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0265 | Follow-the-sun service handover | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0268 | Recurring control evidence inbox | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0273 | Recruiter shortlist review room | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0275 | External-worker onboarding expiry | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0278 | Repeat-contact root cause review | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0279 | Customer onboarding dependency map | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0280 | Renewal outcome evidence packet | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0281 | Help-center answer expiry review | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0283 | Receivables dispute evidence packet | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0284 | Unbilled milestone monitor | 73 | desk_researched | Reserve: direct incumbent overlap |
| W0285 | Duplicate vendor invoice review | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0289 | Corporate training seat reconciliation | 73 | desk_researched | Central comparison; paid workflow test still required |
| W0375 | Support macro policy comparison | 73 | screened | Reserve; direct source and demand gaps |
| W0377 | Customer promised-update calendar | 73 | screened | Reserve; direct source and demand gaps |
| W0418 | Software owner attestation registry | 73 | screened | Reserve; direct source and demand gaps |
| W0257 | Subcontractor delivery signoff | 72 | desk_researched | Central comparison; paid workflow test still required |
| W0264 | Temporary policy exception expiry | 72 | desk_researched | Central comparison; paid workflow test still required |
| W0270 | Candidate promise clock | 72 | desk_researched | Central comparison; paid workflow test still required |
| W0282 | Refund exception approval log | 72 | desk_researched | Central comparison; paid workflow test still required |
| W0287 | Research participant cooldown ledger | 72 | desk_researched | Central comparison; paid workflow test still required |
| W0290 | Association credential renewal desk | 72 | desk_researched | Central comparison; paid workflow test still required |
| W0380 | VIP entitlement lookup | 72 | screened | Reserve; direct source and demand gaps |
| W0381 | Known issue customer roster | 72 | screened | Reserve; direct source and demand gaps |
| W0403 | Invoice approval missing-evidence queue | 72 | screened | Reserve; direct source and demand gaps |
| W0405 | Subscription invoice receipt organizer | 72 | screened | Reserve; direct source and demand gaps |
| W0410 | Retainer prepaid-credit reconciliation | 72 | screened | Reserve; direct source and demand gaps |
| W0459 | Online cohort substitution desk | 72 | screened | Reserve; direct source and demand gaps |
| W0462 | Tutor lesson-credit expiry | 72 | screened | Reserve; direct source and demand gaps |
| W0469 | Corporate learner nomination portal | 72 | screened | Reserve; direct source and demand gaps |
| W0476 | Group membership seat allocation | 72 | screened | Reserve; direct source and demand gaps |
| W0490 | Fractional executive decision inbox | 72 | screened | Reserve; direct source and demand gaps |
| W0258 | Bid capacity stress test | 71 | desk_researched | Central comparison; paid workflow test still required |
| W0431 | Customer questionnaire answer expiry | 71 | screened | Reserve; direct source and demand gaps |
| W0449 | Participant incentive reconciliation | 71 | screened | Reserve; direct source and demand gaps |
| W0461 | Corporate training completion evidence | 71 | screened | Reserve; direct source and demand gaps |
| W0481 | Continuing-education event attendance reconciliation | 71 | screened | Reserve; direct source and demand gaps |
| W0487 | Translation agency terminology approval | 71 | screened | Reserve; direct source and demand gaps |
| W0495 | Professional translator availability commitments | 71 | screened | Reserve; direct source and demand gaps |
| W0260 | Fixed-fee estimate calibration | 70 | desk_researched | Central comparison; paid workflow test still required |
| W0267 | Departure knowledge handover | 70 | desk_researched | Central comparison; paid workflow test still required |
| W0269 | Interview rubric calibration | 70 | desk_researched | Central comparison; paid workflow test still required |
| W0286 | Client purchase-order runway | 70 | desk_researched | Reserve: direct incumbent overlap |
| W0294 | Negotiated rate exception register | 70 | screened | Reserve; direct source and demand gaps |
| W0295 | Sales handoff completeness check | 70 | screened | Reserve; direct source and demand gaps |
| W0305 | Dependency owner escalation map | 70 | screened | Reserve; direct source and demand gaps |
| W0307 | Delivery assumption drift board | 70 | screened | Reserve; direct source and demand gaps |
| W0338 | Company operating manual dependency map | 70 | screened | Reserve; direct source and demand gaps |
| W0384 | Escalation postmortem action tracker | 70 | screened | Reserve; direct source and demand gaps |
| W0446 | Research screener logic preflight | 70 | screened | Reserve; direct source and demand gaps |
| W0271 | Evidence-first hiring packet | 69 | desk_researched | Central comparison; paid workflow test still required |
| W0393 | Expansion request qualification | 69 | screened | Reserve; direct source and demand gaps |
| W0419 | Unused license review organizer | 69 | screened | Reserve; direct source and demand gaps |
| W0421 | Service vendor delivery scorecard | 69 | screened | Reserve; direct source and demand gaps |
| W0422 | Procurement approval route finder | 69 | screened | Reserve; direct source and demand gaps |
| W0426 | Vendor account exit checklist | 69 | screened | Reserve; direct source and demand gaps |
| W0432 | Business continuity rehearsal log | 69 | screened | Reserve; direct source and demand gaps |
| W0439 | Operational incident action evidence | 69 | screened | Reserve; direct source and demand gaps |
| W0466 | Training program version retirement | 69 | screened | Reserve; direct source and demand gaps |
| W0482 | Association sponsorship fulfillment proof | 69 | screened | Reserve; direct source and demand gaps |
| W0272 | Reference consent coordinator | 67 | desk_researched | Central comparison; paid workflow test still required |
| W0255 | Client handoff passport | 66 | desk_researched | Central comparison; paid workflow test still required |
| W0288 | Research contradiction register | 65 | desk_researched | Central comparison; paid workflow test still required |
| W0266 | Business decision review dates | 63 | desk_researched | Central comparison; paid workflow test still required |
| W0274 | Accessible interview logistics | 62 | desk_researched | Central comparison; paid workflow test still required |

### Pass 3: 40 desk-research cards

The researched cards are `W0251`–`W0290`; each has competitors including a manual/free substitute,
observed source references, pricing-test boundary, operating-cost gate, global limitations,
a concrete kill test and a source-specific research note. The 37 `advance` cards are eligible for central comparison; three researched cards moved to `reserve`.
Neither label authorizes a build or claims customer validation.

### Pass 4: central portfolio comparison

The parent review selects across all lanes without a fixed business quota. This lane recommends reducing
correlated agency variants, retaining credible B2B price tests, and demoting weak direct evidence even when
score arithmetic looks attractive. Existing WoW2 product overlaps are a parent-level comparison because
this lane did not inspect or claim ownership of product repositories.

---

## Rejected traps and uncertainty

- Generic agency suites, project management clones, helpdesks, LMSs and community platforms require migration and breadth.
- Generic AI note-taking, chatbot and resume-ranking products face bundled incumbents and recurring compute/support exposure.
- Marketplace ideas need both sides of distribution; the existence of professionals does not create buyer liquidity.
- Tax filing, financing, legal verdicts, employment ranking and disciplinary decisions exceed this administrative-software scope.
- Compliance badges, professional accreditation and synthetic customer interviews must not be represented as verified outcomes.
- Highly confidential case administration may fit software-only scope but exceed the user's pre-revenue operating budget.
- Shared spreadsheets can be the rational customer choice; a narrowly worded product is not automatically differentiated.
- Global English workflows still require payment access, privacy controls, time zones and localized customer policies.
- Acquisition channels are hypotheses. No community access, audience, partner relationship or conversion advantage was verified.

---

## Cross-lane overlap guidance

Keep business ownership where the payer runs an organization and the product administers a service:
corporate training seats, online tutoring billing, research participant operations, association credentials,
and client delivery evidence. Personal learning tools, generic creator publishing tools, developer incident
or security systems and consumer collection catalogs belong to the other research lanes.

Potential consolidation during central review:

| Business family | Merge or distinguish by |
|---|---|
| Agency scope, acceptance, retainer and billing | One cohesive customer decision-to-invoice workflow; avoid counting feature slices as independent products |
| Vendor renewal and ownership | Same buyer and data; select one initial product wedge |
| Customer promises and onboarding dependencies | Customer-success buyer with different trigger; check whether one product should cover both |
| Operational evidence and procedure review | Independent consultant buyer versus internal administrator; distinguish security/compliance tooling |
| Research evidence and participant consent | Repository versus recruiting operations; do not merge merely because both mention research |
| Training administration and credentials | Provider workflow versus learner experience; issuer authority remains external |

---

## Machine-checkable totals

- Ideas: 250; unique IDs: 250; range: `W0251`–`W0500`.
- Evidence: {'desk_researched': 40, 'screened': 210}.
- Decisions: {'reserve': 181, 'advance': 37, 'reject': 32}.
- Models: {'subscription': 239, 'freemium': 4, 'lifetime': 6, 'free': 1}.
- Sources: 40 distinct primary URLs, all returned by live browsing on 2026-09-28.
- Compared candidates: 75; every researched row resolves all source references.
- No customer-validated record, invented demand metric or inferred market revenue.

---

## Focused first-revenue stress test

The following is a falsification pass against concrete incumbent documentation, not an implementation recommendation.

| Candidate | Revised score | Decision | Material observation |
|---|---:|---|---|
| W0251 Scope change approval | 74 | Reserve | [Ignition change orders](https://support.ignitionapp.com/en/articles/15198048-create-and-send-change-orders) already connect original scope, pricing and client approval |
| W0284 Unbilled milestone monitor | 73 | Reserve | [Ignition milestone billing](https://support.ignitionapp.com/en/articles/16698484-set-up-milestone-billing-in-a-proposal) supports scheduled or manually triggered invoices |
| W0286 Client purchase-order runway | 70 | Reserve | [Scoro](https://support.scoro.com/hc/en-us/articles/48823995667341-Client-Purchase-Orders-quote-based-app) and [Track & Bill](https://trackandbill.app/help) already track client-PO balances and overspend |

### W0251: scope approval

The proposed core flow overlaps directly with Ignition. The surviving experiment is whether agencies
committed to other agreement and billing systems want a standalone change receipt enough to pay $49/month.
Do not imply legal enforceability or replace the client's contract. Keep an original-scope link, proposed
change, price, authorized recipient and human acceptance record. No payment execution or legal drafting.

Acquisition hypothesis: a moderator-permitted agency-operations post provides a useful change-control
worksheet and invites opt-in walkthroughs. A fractional operations consultant might refer their own willing
clients, but no such relationship is established. Avoid scraping agency directories or unsolicited messages.

Operating-cost boundary: text, links and capped email should plausibly fit the user's $20–50 target with
shared hosting, subject to a real hosting/security quote. The larger risk is support around identity,
disputed acceptance and custom approvals. Weekly change volume across several projects supports recurrence;
a solo freelancer with one quarterly change probably belongs on a free document template.

Strongest kill: show ten qualified non-Ignition agencies both the standalone prototype and incumbent/manual
alternatives. Stop if three can configure their existing solution within one hour, or fewer than three agree
to a priced pilot. A claim that the tool looks useful is insufficient; require a second real change cycle.

### W0284: unbilled milestones

Generic milestone billing is already implemented. The possible add-on monitors completion evidence in one
system against invoices in another, with an explicit source row for each mismatch. Export-based analysis
keeps the first experiment cheap, but source matching becomes a support business if every buyer uses a
different definition of accepted, invoiced, credited or voided.

Acquisition hypothesis: willing fractional bookkeepers or agency operators volunteer redacted quarter-end
exports through their communities. Begin with a read-only reconciliation, never a promise to recover money.
Finding an uninvoiced milestone is not the same as collecting revenue; it may be intentionally deferred.

Recurrence is the primary risk: the first audit may clean up a one-time mess. The ongoing product must
change a monthly billing decision. Stop if five qualifying firms produce no confirmed missed trigger,
or if fewer than three want to repeat the review at $49/month after their first cleanup. Reject a connector
roadmap unless a paying customer proves the same source format recurs. Free spreadsheet comparisons count.

### W0286: PO runway

The earlier hypothesis of a simple underserved PO layer did not survive direct competitor inspection.
Scoro explicitly accounts for open estimates, confirmed quotes and invoiced work. Track & Bill documents
remaining balances and overbilling warnings, with public [solo pricing of $19.99/month](https://trackandbill.app/).
Scoro's minimum five users and paid extras create a different package, but this is not a universal premium-price gap.
The possible remaining experiment is cross-system commitment review for firms unwilling to change their billing stack.

Acquisition hypothesis: opt-in agency finance workshops via willing fractional finance practitioners;
qualify only firms with several simultaneous client POs and a recent blocked invoice. No channel access or
conversion is verified. Small consultants with one PO and a reliable workbook are poor targets.

The deterministic balance calculation is cheap; keeping commitments current is not. Manual inputs must
show last-updated time and unknown balances. Currency, tax treatment and line-level authorizations remain
customer-defined. Do not claim invoice prevention if the tool cannot control the invoicing system.
Stop if customers need live ERP integration before any useful review, or if no three of ten qualified
agencies pay $59 for repeated cross-system review after comparing incumbent and spreadsheet alternatives.

### Why the three alternatives remain provisional

`W0261` can start with customer-entered dates and acknowledgment, but ContractSafe already reminds owners
and Cledara already manages renewals. Its only initial boundary is smaller setup across existing systems.
A paid pilot must prove this boundary matters; annual deadline anxiety alone does not prove monthly retention.

`W0276` can start with manually entered promises and links. Canny already manages account-linked feedback;
Custify already manages account actions. Distinguish an accepted customer obligation from a product request,
and reject the idea if ordinary CRM tasks capture it adequately. Test with one success manager handling
multiple accounts, not an enterprise organization requiring immediate integration across every system.

`W0263` can attach owner review dates to existing wiki links without storing documents. Process Street
and Notion remain credible substitutes. Require a review cycle that finds and corrects stale instructions;
clicking acknowledge without reading is a failed outcome. Repeated reviews and affordable setup, not
an assertion of missing incumbent features, are what must justify $29/month.
