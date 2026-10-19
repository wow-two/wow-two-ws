# Next product for the MRR roadmap

*Last updated: 2026-10-09*

> Superseded for this chat by the [self-serve product assessment](self-serve-products-2026-10-09.md).
> The user clarified that product-defined experiences, low integration burden and independent adoption
> take priority over the client-specific B2B workflows considered below. The buyer-contact question
> below is no longer the active selection question.

## Recommendation

Progress **S052 — Migration delivery workspace** through a bounded buyer-validation cycle. It is the
strongest additional catalog candidate under the engineering-founder assumption, not a validated business
or an approved fifth implementation lane. Choose **S055 — External client acceptance** instead if access
to software agencies is materially stronger. Choose one of these entry points, not both together.

For an already implemented product, **Retainer Balance** is the strongest fallback for a customer trial.
Its monthly allowance workflow is coherent, but existing code does not establish a reason to subscribe.
The newer research deliberately moved beyond the earlier narrow first-ten pilots; their implementation
head start alone should not reverse that decision.

Buyer access remains unconfirmed. The October 9 question asks whether the founder can already reach
migration consultancies, software agencies, or neither. Until answered, this recommendation assumes no
confirmed pilot customers. No outreach, product implementation, roadmap reorder, or commercial launch
was performed by this assessment.

---

## Current roadmap and ownership

The [central product order](../../system/planning/pln-tasks.md#venture-product-order) is authoritative.
It already assigns four products to release work:

| Product | Current ownership | Revenue issue still distinct from local implementation |
|---|---|---|
| ForeverPin | Separate chat, per user | Reliable paid release and actual payment acceptance |
| Pose Coach | Separate chat, per user | Paid device release and repeat use that supports renewal |
| Hijinx | Active `w2 - hijinx` chat | Paid-release model, recurring host value and release acceptance |
| Transcript Forge | Also owned by `w2 - hijinx` | Local Release 1 precedes hosted customer isolation, quotas and billing |

Transcript Forge ownership was checked in the current chat history, not inferred from its absence in
the user's three-product exclusion. Its [release assessment](../../workbench/maxs-projects/ventures/saas/10x-ventures-transcript-forge/engineering/research/release-readiness-2026-10.md)
and [product context](../../workbench/maxs-projects/ventures/saas/10x-ventures-transcript-forge/product/context.md) separate
local workflow reliability from the unvalidated repeat-publisher subscription.

The October 31 target applies to the existing Transcript Forge/Hijinx lane. It is not a deadline or
paid-launch forecast for a new catalog product.

The roadmap is currently stronger on building and release verification than on customer evidence.
The reviewed sources do not establish acquired, paying, renewing cohorts. Additional development can
increase the number of working products without resolving that missing evidence. The useful additional
lane therefore owns buyer access, a concrete recurring workflow, and paid-cycle evidence.

---

## Ranked additional options

All prices are existing hypotheses. Account counts are arithmetic for at least $5,000 gross MRR,
before discounts, churn, fees, taxes and operating costs; they are not acquisition forecasts.

| Priority | Product | Recurring payer and job | Proposed monthly price | Accounts for $5K |
|---|---|---|---:|---:|
| 1 | S052 — Migration delivery | Consultancy managing successive migration engagements | $149 | 34 |
| 2 | S055 — External client acceptance | Agency obtaining client acceptance across successive releases | $99 | 51 |
| 3 | Retainer Balance | Agency reconciling allowances and overages every billing period | $39 | 129 |

### 1. Migration delivery

- Buyer: owner or delivery lead at a small CRM/ERP migration consultancy.
- Paid job: resolve mapping disagreements and exceptions, reconcile a dry run, preserve client acceptance.
- Renewal hypothesis: the consultancy brings its next engagement into the same operating record.
- Initial scope: mapping versions → exception ownership → reconciliation evidence → client cutover decision.
- Boundary: customers keep transformation code and full datasets; the product manages bounded evidence.
- Existing estimate: 8–12 full-time builder-weeks, excluding discovery, sales and external procurement.

This fits the founder's engineering experience and avoids mandatory model-inference costs. Domain fit
does not establish access to budget owners. The [existing dossier](catalog-100.md#s052) ranks it first
under both acquisition-heavy and feasibility-heavy sensitivity weights; those rankings remain judgments.

**Strongest objection:** [Flatfile Projects](https://flatfile.com/pricing) already markets migration
mapping, collaborative review, multi-step approvals and audit trails. Its project-volume pricing is
quote-based. “Migration collaboration” alone is not differentiation. The proposed opening is a smaller,
customer-run migration process whose reconciliation and client decisions remain costly in existing tools.
That opening needs observation, not another feature list.

**Next milestone:** replay a redacted completed migration with a consultancy, identify one unpaid
reconciliation failure, and show how a versioned decision record prevents it. The existing validation
target is ten interviews, five artifact walkthroughs and three $149/month pilots across two engagements.
Observe actual subscription renewal separately from repeated project use. Stop if buyers require bespoke
transformations or will not pay for the shared workflow. These are internal gates, not market benchmarks.

### 2. External client acceptance

- Buyer: delivery director at a software agency with repeated external-client releases.
- Paid job: turn scenarios, defects and retests into an explicit approval of a particular release.
- Renewal hypothesis: the next client release needs another acceptance cycle.
- Initial scope: scenario import → guest results → linked defects → retest → version-bound approval.
- Boundary: issue links before synchronization; bounded screenshots; no full test-management platform.
- Existing estimate: 6–10 full-time builder-weeks; shortest estimated new build among the ten finalists.

The [dossier](catalog-100.md#s055) supports a bounded delivery product, but **faster implementation does
not mean faster revenue**. [Marker.io](https://marker.io/pricing) already sells agency feedback/UAT
workflows, including accountless reporters. Its agency offer displays $129 monthly or $99/month with
annual billing, subject to eligibility. [Testmo](https://www.testmo.com/pricing/) lists $59/month for five
users. The case must concern unresolved business acceptance and disputed releases, not screenshot capture.

**Next milestone:** replay one disputed release and one subsequent retest with an agency and its client.
Require the client to participate and the agency to pay through a second cycle. Prefer this candidate
over migration delivery when those buyers are actually reachable. Stop if approval stays in email or
incumbent configuration already solves the costly part. Do not assume approvals constitute legal signatures.

### 3. Retainer Balance

The [current product](../../workbench/maxs-projects/ventures/saas/ventures.retainer-balance/product/product.md) implements
CSV time import, allowance reconciliation, recorded external approval evidence and frozen statements.
It is an authenticated personal workspace. It has no verified client consent, team membership or billing.
The [backlog](../../workbench/maxs-projects/ventures/saas/ventures.retainer-balance/engineering/planning/backlog.md) still
lists published dependency pins, hosting/restore acceptance, account recovery and commercial launch gates.

**Why third:** a monthly money-related workflow is more naturally recurring than a one-off generator,
and there is already a demonstrable pilot. However, [Harvest](https://www.getharvest.com/blog/2018/06/more-powerful-budgeting-to-keep-your-monthly-retainers-on-track)
already supports monthly retainer budgeting. [ManyRequests](https://manyrequests.com/blog/client-request-management-software)
describes a request-to-billing workflow. An extra allowance ledger must save work those tools leave behind.

**Next milestone:** use the pilot to replay two real agency billing periods, comparing the statements
with the agency's existing reports. Investigate authenticated client participation only if that missing
interaction explains willingness to pay. The existing stop rule is four of five agencies accepting their
current reports as sufficient, or fewer than three accepting a paid pilot. Do not build more integrations
merely to make the prototype look complete.

---

## Why other products wait

| Product or group | Disposition | Reason |
|---|---|---|
| S094 — Receivables/disputes | Conditional reserve | Strong recurring pain; finance-buyer access could promote it, but correctness, integrations and collection-service expectations add scope |
| [File Watch](../../workbench/maxs-projects/ventures/saas/ventures.file-watch/product/product.md) | Existing-pilot reserve | Repeated delivery accountability is plausible; buyer adoption and notification/operational readiness remain open |
| [Documentation Checker](../../workbench/maxs-projects/ventures/saas/ventures.documentation-checker/engineering/research/research.md) | Existing-pilot reserve | Engineering access may help; current checker breadth and paid differentiation need evidence |
| [Training Seats](../../workbench/maxs-projects/ventures/saas/ventures.training-seats/product/product.md) | Buyer-access reserve | Promote only with a reachable course/training provider and repeated cohort administration |
| [ListingShelf](../../workbench/maxs-projects/ventures/saas/ventures.listing-shelf/product/product.md) | Hold for MRR priority | Personal listing-research use is established; recurring commercial buyer and paid boundary are not |
| [Prism](../../workbench/maxs-projects/ventures/saas/10x-ventures-prism/product/context.md) / Whiteout | Hold for MRR priority | Current engineering scope is substantial; a near-term recurring commercial path is not established |
| [Whiteout Presets](../../workbench/maxs-projects/ventures/consumer/10x-venture-whiteout-presets/README.md) | Support asset | Companion game assets are not a separate validated subscription business |
| [Craft generators](../../workbench/maxs-projects/ventures/10x-ventures/ideation/runs/2026-09-26-thirty-day-revenue/pool-speed.md) | Revalidate before promotion | July rankings are stale; later research challenged free substitutes, distribution and physical-kit demand |
| Haven | Preserve explicit gate | User placed it after stable $2K venture MRR |
| TNIS / Mintrans | Preserve existing deferral | Existing roadmap defers them behind the current release priorities |

The July [portfolio registry](../../workbench/maxs-projects/ventures/10x-ventures/README.md) and
[judged pipeline](../../workbench/maxs-projects/ventures/10x-ventures/products-final.md) are historical context, not
reliable current release states. The [October decision report](decision-report.md) and current repository
contexts supersede their technical-readiness claims. This assessment revisits the relevant shortlist and
existing products; it does not claim a fresh 100-product market study.

---

## Shared revenue dependency

The roadmap already tracks the parent-company/payment setup as `ven-t-012`. Resolve that existing lane
alongside product validation. [Stripe's supported-country list](https://stripe.com/global), checked
October 9, does not list Uzbekistan. Actual seller eligibility and payout acceptance must be established
for the selected route; a new product or existing checkout integration cannot establish them.

This assessment makes no new entity, tax or provider recommendation. It does not extend that Stripe
observation into a claim about every possible payment provider.

---

## Evidence boundary

- Local evidence: current central roadmap, product contexts/backlogs, October catalog and active Hijinx chat.
- Official web refresh: Flatfile, Marker.io, Testmo, Harvest, ManyRequests and Stripe, accessed 2026-10-09.
- No product tests were rerun; repository test records were not treated as deployment or payment evidence.
- Buyer access, comparative time savings, paid demand, renewals and support economics remain unverified.
- This file records a recommendation; the central execution order remains unchanged by this assessment.
