# Creator opportunity research notes

Research date: 2026-09-28. Owner: creator lane. Scope: `W0501`–`W0750`.

## Outcome and evidence boundary

`creator.json` contains 250 distinct buyer/job hypotheses, of which 40 have current primary-source desk research and 210 received an analyst screen only. There are 46 primary URLs in the source registry. All were actually opened or returned by live search during this run; unsuccessful pages and pages without substantive content were excluded. None of the 250 is customer-validated. No outreach, test accounts, interviews, pilots, purchases or acquisition experiments were executed.

Paid competitor offers establish that suppliers sell related workflows. They do not establish buyer counts, success probability, unmet demand, willingness to pay our proposed prices, or attainable distribution. `evidence_fit` distinguishes directly overlapping workflow evidence from adjacent category evidence. Proposed prices and scores are hypotheses. Observed prices are recorded separately in `sources` and `competitor_pricing_observed`.

The catalog has correlated job families. Several ideas are alternative wedges into the same buying workflow; they should not all become independent products. For example, sponsorship inventory, delivery packets, ad-read tracking and renewal dossiers belong to `creator-sponsor-operations`. Caption QA and subtitle revision propagation likewise overlap operationally even though their jobs differ. A 250-row inventory is not 250 independent markets.

## Budget gate

The user clarified a default **$20–50 per product per month before revenue**, with **approximately $300 per product per month available after early products earn revenue**. These are product budget ceilings, not measured infrastructure quotes. Founder labor is not priced in this research. Every proposed pilot must fit its ceiling before implementation is approved.

Prefer deterministic text/file validation, metadata ledgers, CSV imports and bring-your-own file links. Do not build video transport, RAW-photo backup, full media libraries, an email sender, an ad marketplace, or uncapped AI generation as the initial wedge. Begin with limited, consented customer records. Capped storage and polling remain necessary even when the expected pilot cost looks small. Paid platform tiers required for API access can exceed the pre-revenue budget, so CSV-based pilots are intentionally part of several MVPs.

The $300 allowance is a later phase gate supported by revenue and observed demand; it is not permission to spend now. No vendor purchase or external action was taken.

## Research iterations

1. Generated concrete recurring jobs across newsletters, podcasts, video/localization, design, publishing, digital products, memberships, online events, marketing and photo workflows.
2. Screened all 250 against buyer clarity, recurrence, low-cost implementation, free substitutes, distribution difficulty and correlated families. Broad commodity clones and unbounded hosting were explicitly rejected.
3. Compared a 75-candidate review pool: the 40 desk-researched candidates plus the 35 strongest remaining screened alternatives listed below. The latter remain unverified; a high score is not equivalent to stronger evidence.
4. Checked 40 candidates against current primary product/pricing pages. Competitive overlap reduced confidence in broad creator platforms and lowered the disposition-ledger candidate because incumbents already resolve comments and compare versions.
5. Flagged budget, acquisition, seasonality, privacy and service-cost failure modes; defined falsifiable future experiments and stop conditions.
6. Falsified the initial strongest three against exact incumbent workflows, downgraded all to reserve, revised two proposed prices and the royalty model, and replaced broad differentiation claims with controlled comparisons.

These are analytical iterations, not empirical validation rounds. Central review can select fewer than 40 creator candidates and should cap shared families. The final 100 should contain experiments, not authorization to build 100 apps.

## Independent falsification update

The strongest three received an additional exact-workflow check. All moved to **reserve**: attractive cost profiles do not overcome feature overlap. These are analyst revisions, not failed customer trials.

| Candidate | Revised score/model | Direct counterevidence | Residual test |
|---|---|---|---|
| W0511 Caption delivery quality gate | 69/100; proposed $39/month freemium | Free [Subtitle Edit](https://subtitleedit.github.io/subtitleedit/) exports error reports and runs headlessly. [CaptionHub QA](https://support.captionhub.com/creating-and-editing-captions/uz47hySTrT5PGcSv3hNgUj/automatic-machine-translation-qa/74r5KxnjMaZE29incW5Gf2) includes language profiles and approval rules; its [usage plan](https://www.captionhub.com/pricing-tiers) includes collaboration at $2.50/minute. | Preserve client acceptance against the exact delivered file version without changing editors. |
| W0516 Creative usage-rights expiry monitor | 69/100; proposed $29/month freemium | [Filecamp expiry](https://filecamp.com/support/expiration/) includes bulk dates, search and impending-expiry markers. [Plans](https://filecamp.com/pricing-plans/) start $29/month; expiration tier entitlement remains unconfirmed. | Detect unresolved placement-specific ownership across differently licensed uses of one asset. |
| W0524 Creator collaboration royalty statements | 61/100; proposed $19/month or $49/period | [Royaltally](https://royaltally.com/) covers imported sales, allocations, bundles and quarterly statements. [Pricing](https://royaltally.com/pricing.php) includes three titles free and $19/$29/$39 monthly tiers. [Gumroad native collaboration](https://gumroad.gumroad.com/p/split-fees-with-collaborators) further reduces simple use cases. | Reconcile actual cross-store, non-book bundle refunds that incumbent mapping cannot handle. |

**Cheapest repeat-use experiment among these three: W0511, conditionally.** Recruit five studios already using local editors through moderator-approved localization communities and a free sample handoff report. This channel is proposed and unvalidated. Compare 40 consented deliveries using Subtitle Edit plus Drive/Sheets against a clickable exception-signoff prototype. Measure coordination minutes, clarification messages and revision-related acceptance errors. The proposed pass threshold is 30% lower median coordination time, three paid $39 pilots and three second-month renewals. Kill if the incumbent baseline is equally convenient. Do not rebuild the free QA engine or require media uploads. Capped text/metadata storage targets the $50/month pre-revenue ceiling; actual hosting quotes and customer evidence are still missing.

W0521 EPUB accessibility review packets and W0537 affiliate destination monitoring remain other low-compute candidates, with strong free/incumbent substitutes already recorded. This extra pass does not validate them by comparison. TranscriptForge should not adopt generic caption QA merely because it is inexpensive: the proposed signoff job needs the same differentiation test.

## Conditional $5,000 MRR arithmetic

MRR here means realized recurring subscription revenue before processing fees, refunds, sales taxes, operating costs and founder labor. It excludes lifetime and per-project receipts. None of these acquisition counts is a forecast.

- At a realized $49/month, 103 active paying accounts produce $5,047 MRR.
- At a realized $39/month, 129 active paying accounts produce $5,031 MRR.
- At a realized $29/month, 173 active paying accounts produce $5,017 MRR.
- At a realized $19/month, 264 active paying accounts produce $5,016 MRR.

These counts assume proposed prices survive testing and customers can be reached economically. Neither assumption is verified. The earlier three-product illustration was removed after direct competition weakened its proposed prices and recurrence. Lower realized prices from annual discounts, refunds and low-volume tiers require more paying accounts. New acquisition must also replace churn; the catalog does not supply measured churn or conversion rates. Landing-page interest alone is insufficient: require repeat use and paid renewal.

## Model choices

- **Freemium** fits a useful single-file or small-record audit whose paid value is reusable profiles, teams, history or recurring checks. A free tier must have firm costs and useful output.
- **Subscription** fits weekly studio work, monthly royalty reconciliation and ongoing rights/link protection. Frequency should be demonstrated before choosing this model.
- **Per-project or hybrid** can fit newsletter migration, conference preparation and beta-reader coordination. These jobs may be too seasonal for dependable MRR.
- **Lifetime** belongs primarily to local deterministic utilities with bounded maintenance promises. Never count lifetime sales as MRR or promise unlimited ongoing storage/compute.
- **Free utility** candidates include a timezone preview, a brand contrast review kit and a color-profile inspector. Their contribution is a channel hypothesis to related paid workflows, not assumed revenue.

## Rejected or weakened traps

- Generic transcript summaries and auto-clippers are bundled by [Descript](https://www.descript.com/pricing), [Kapwing](https://www.kapwing.com/pricing), podcast hosts and general assistants. A different prompt is insufficient differentiation.
- Generic checkout, membership and newsletter platforms meet formidable bundles from [Payhip](https://payhip.com/pricing), [Gumroad](https://gumroad.com/pricing), [Memberful](https://memberful.com/pricing), [Circle](https://circle.so/pricing), [beehiiv](https://www.beehiiv.com/pricing) and [Ghost](https://ghost.org/pricing/).
- Video comment-resolution software was downgraded (`W0513`): [Ziflow](https://www.ziflow.com/pricing) already offers resolution, comparison and workflow stages. Any new tool must beat this for a sharply bounded client segment.
- Broad digital storefronts, community clones and SEO writers need an acquisition advantage that has not been established.
- Lifetime unlimited video/RAW storage and lifetime unlimited AI generation are rejected. They create recurring liabilities with one-time receipts and receive `margin=1`.
- Literary journal software, author beta feedback and low-volume membership cancellation analysis remain reserves because budgets or repeat frequency may be too weak.
- Two-sided marketplaces for clips or events need supply, trust and demand simultaneously. Their cold start is inconsistent with the first low-cost revenue experiments.

## Existing WoW2 overlap supplied by parent

These are competitive comparisons to parent-supplied product descriptions, not a source-code review.

**TranscriptForge:** `CRE08` Descript, `CRE09` Kapwing, `CRE07` Auphonic and `CRE33` Subtitle Edit challenge generic repurposing/transcription. The strongest alternative experiment is a deterministic editorial/QA workflow with preserved source evidence, such as caption batch QA or reusable correction rules. Validate that it is not already convenient in the incumbent before implementing.

**ForeverPin programmable links/QR:** `CRE35` Dub, `CRE36` Short.io and `CRE37` QR Code Generator show that editable destinations, QR design, expiration and targeting are already sold. Short.io's page lists a commercial free tier with custom domains, QR generation and 1,000 branded links; this directly weakens a generic QR subscription. A specific change-approval, destination integrity or migration workflow would need separate evidence. Dub's extracted numeric plans are **Partners** plans, not verified standalone Links entry pricing. QR Code Generator numeric amounts remain unknown.

**Brand Workspace / Ocharo marketing and blog:** `CRE12` Brandfolder, `CRE13` Frontify, `CRE34` Filecamp and `CRE27` Bannerbear provide asset/guideline/template competition. Narrow rights evidence, client handover and campaign-variant QA could be investigated using existing workflows. Internal usefulness in Ocharo would be a dogfood signal, not proof that outside businesses pay.

## Source and global limitations

All sources are supplier-owned product, pricing or documentation pages. No independent customer interviews or representative review sample was conducted. Strong feature evidence is not market-size evidence. Pricing was checked live on 2026-09-28 but can change; dynamic billing selections and missing amounts remain explicitly qualified.

Notable pricing constraints include annual billing on Circle and Ziflow, introductory versus renewal prices on PrettyLinks, and platform plus payment-processing fees on Payhip/Memberful/Luma. A source describing software license keys is only adjacent evidence for creative usage-right licenses. Submittable's current pricing page emphasizes grants and applications; it does not directly verify a literary-journal niche. The initially guessed Filecamp pricing route failed; the correct /pricing-plans/ route was subsequently verified (CRE42). Affordable DAM competition is confirmed; do not infer a gap from enterprise quote pages. Gumroad fee help (CRE46) also clarifies processing fees beyond the headline direct-sale charge.

Global portability means an initial English interface for software-only workflows. Supported payment countries, platform API tiers, languages, RTL rendering, data handling, contract meanings and tax obligations vary. No product here promises universal compliance, legal clearance or platform coverage. Buyers supply rights interpretations and policies. No original large media files are required by most proposed MVPs.

## Comparison pool: 35 additional screened alternatives

The following entries complement the 40 researched rows in the 75-candidate review pool. They received no idea-specific current competitor check; they remain reserves. Equal scores are deliberate coarse judgments, not statistically meaningful precision.

- `W0541` — Editorial source freshness register (69/100).
- `W0543` — Sponsor creative specification checker (69/100).
- `W0544` — Cross-publication content reuse ledger (69/100).
- `W0547` — Subscriber tag hygiene preview (69/100).
- `W0562` — Podcast episode clearance checklist (69/100).
- `W0565` — Podcast show-note link maintainer (69/100).
- `W0577` — Audiobook pronunciation change ledger (69/100).
- `W0583` — Video delivery specification inspector (69/100).
- `W0584` — Screen-recording update dependency map (69/100).
- `W0587` — Video privacy redaction review queue (69/100).
- `W0595` — Multilingual video release parity board (69/100).
- `W0596` — Animation voice pickup coordinator (69/100).
- `W0607` — Digital campaign asset matrix (69/100).
- `W0613` — Design file dependency manifest (69/100).
- `W0614` — Campaign legal-copy version lock (69/100).
- `W0617` — Presentation master quality checker (69/100).
- `W0618` — Accessible document visual handoff (69/100).
- `W0625` — Manuscript style-sheet manager (69/100).
- `W0626` — Author proof correction reconciliation (69/100).
- `W0632` — Editorial sensitivity review issue ledger (69/100).
- `W0636` — Editorial fact verification queue (69/100).
- `W0646` — Digital product update impact notice (69/100).
- `W0647` — Template dependency checker (69/100).
- `W0657` — Creative marketplace earnings variance (69/100).
- `W0667` — Member question commitment tracker (69/100).
- `W0669` — Community moderation appeal ledger (69/100).
- `W0673` — Membership tier migration preview (69/100).
- `W0681` — Cohort peer review allocation (69/100).
- `W0688` — Virtual event timezone conflict inspector (69/100).
- `W0690` — Virtual conference recording permission matrix (69/100).
- `W0694` — Virtual summit sponsor deliverable matrix (69/100).
- `W0698` — Online-event accessibility preparation board (69/100).
- `W0709` — Marketing claim evidence register (69/100).
- `W0710` — Content consolidation decision board (69/100).
- `W0713` — Marketing landing-page promise parity (69/100).

## Verification

Validated exact count (250), contiguous unique IDs (`W0501`–`W0750`), unique names, 40 researched rows, 210 screened rows, required fields, source references, allowed integer score ranges, and null recurring prices for free/lifetime models. Numeric source amounts were not invented where extraction failed. No files outside `creator.json` and `creator-notes.md` were edited by this lane; no staging or commits were performed.
