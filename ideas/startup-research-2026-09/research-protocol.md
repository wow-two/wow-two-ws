# Global software opportunity research

Research date: 2026-09-28. This document defines the shared research contract.

## Objective and boundaries

Screen 1,000 distinct software business hypotheses, compare existing WoW2 ideas,
and distill 100 candidates for experiments. Model a combined $5,000 MRR target
from one to three products. The 100 are an opportunity backlog, not 100 approved builds.

Software for collectors of physical objects is allowed. Manufacturing, inventory,
shipping, hardware purchases, field services, and fulfillment operated by us are excluded.
Global means a portable initial English-language workflow with explicit expansion constraints,
not universal payment, language, legal, or data coverage.

Assume bootstrap economics, founder-led distribution, no existing large audience, and low
variable cost. User clarified: default $20–50 monthly per product before revenue;
allow roughly $300 monthly per product once early revenue can support expansion.
Prioritize testing revenue channels for the initial products. Higher-cost candidates
remain eligible for a later revenue-funded phase; no channel is empirically validated yet.
No outreach, purchases, deployments, product scaffolds, or account changes are authorized by this research.

## Evidence discipline

- Browse current primary product/pricing/documentation pages; record exact URLs and access date.
- A paid competitor establishes a commercial offer, not customer count, revenue, retention, or demand for our wedge.
- Never claim a niche is empty, underserved, or profitable merely because search found few results.
- Scores, proposed prices, costs, channels, and conversion rates are analyst hypotheses unless directly sourced.
- Distinguish direct feature evidence from adjacent-category evidence; free substitutes count as competition.
- Missing prices stay unknown. Annual prices retain annual billing labels; normalize explicitly.
- Source excerpts/paraphrases stay brief; do not copy pages or reviews wholesale.
- No invented TAM, search volumes, reviews, interviews, willingness-to-pay measurements, or success probabilities.
- Classify `screened` versus `desk_researched`; no idea is `customer_validated` in this exercise.

## Parallel lanes

All work belongs to the `wow-two-ws` meta-repository, under this directory only.
Existing changes and staged files belong to other lanes. Agents do not stage or commit.

| Lane | IDs | Scope | Owned files |
|---|---|---|---|
| developer | W0001–W0250 | developer tools, data, engineering operations | developer.json, developer-notes.md |
| business | W0251–W0500 | professional services, business administration, remote operations | business.json, business-notes.md |
| creator | W0501–W0750 | creators, publishing, digital commerce, marketing | creator.json, creator-notes.md |
| personal | W0751–W1000 | collectors, hobbies, personal workflows, learning, research | personal.json, personal-notes.md |

Avoid mere noun substitutions and feature-only splits. Each idea needs a distinct buyer,
recurring job, or value proposition. Closely related ideas get one `family` identifier
so the final shortlist can avoid pretending correlated variants are independent businesses.

## Scoring

Eight dimensions, each integer 1–5; higher is better. These are explicit analyst judgments,
not estimated probabilities. `score = sum(weight * dimension / 5)` out of 100.

| Key | Weight | 1 | 3 | 5 |
|---|---|---|---|---|
| pain | 20 | optional amusement | repeat inconvenience | urgent costly recurring job |
| pay | 15 | mostly free substitutes | adjacent paid offers | direct paid workflow and identifiable budget owner |
| reach | 20 | broad ads/network needed | specific channel hypothesis | existing accessible distribution advantage |
| repeat | 15 | one-off | monthly/seasonal | weekly/daily or continuous protection |
| wedge | 10 | commodity clone | testable narrow distinction | compelling underserved workflow with evidence |
| build | 10 | large platform/research | focused multiweek MVP | small deterministic MVP |
| margin | 5 | heavy uncapped compute/data | bounded paid dependencies | cheap deterministic workload |
| portability | 5 | local law/data dependency | adaptation needed | software-only and geography-light |

Do not award reach=5 without real founder access; do not award wedge=5 on intuition.
Evidence confidence remains a separate field; arithmetic must not disguise uncertainty.

## Lane deliverable schema

Each lane JSON is an object with `lane`, `sources`, and exactly 250 `ideas`.
Each source: `id` (lane-prefixed), `url`, `title`, `checked` (2026-09-28),
`supports`, `price_observed` (string, preserve currency/billing), and `caveat`.
Only sources actually opened or returned by live web search belong in this registry.

Each idea:

```json
{
  "id": "W0001", "name": "Specific workflow", "family": "buyer-job-family",
  "buyer": "Specific paying user", "job": "Concrete problem and software outcome",
  "wedge": "A testable distinction, not a claim of an empty market",
  "model": "subscription|freemium|lifetime|usage|hybrid|free",
  "price_monthly_usd": 29, "price_once_usd": null,
  "scores": {"pain": 3, "pay": 3, "reach": 2, "repeat": 3, "wedge": 2, "build": 4, "margin": 5, "portability": 5},
  "channel": "Specific plausible channel and first acquisition action",
  "risk": "Strongest reason this fails",
  "evidence": "screened|desk_researched",
  "source_ids": ["DEV01"],
  "evidence_fit": "direct|adjacent|none",
  "decision": "advance|reserve|reject",
  "reason": "Idea-specific explanation of the decision",
  "mvp": "Narrow product boundary",
  "validation": "Falsifiable next experiment; no fabricated results"
}
```

`price_monthly_usd` is a proposed realized recurring price before fees, never competitor revenue.
Annual consumer subscriptions are monthly equivalents. Lifetime-only/free ideas have null recurring price.
For screened rows, mvp/validation may be short; all other fields remain substantive.
For the best 40 per lane, mark `desk_researched` and add:

```json
{
  "competitors": "Named direct/adjacent products and the free/manual substitute",
  "pricing_test": "Proposed free limit, paid feature boundary, subscription or lifetime rationale",
  "cost_risk": "Storage/API/support exposure with a limit; estimates labelled",
  "global_note": "Geographic/language/payment/platform limitation",
  "kill_test": "Concrete result that would stop this idea",
  "research_note": "What live sources establish and what remains unverified"
}
```

Aim for at least 25 distinct primary sources per lane; each researched idea gets named
competitive evidence and a defensible source link. Adjacent evidence is acceptable when
explicitly labelled, but is weaker. Do not silently reuse one category source as verification
of many unrelated markets. Write notes on the strongest picks, rejected traps, uncertainties,
and source limitations. Keep research depth ahead of spurious precision.

## Iterations and ownership

1. Generate and screen 1,000 with explicit buyers, jobs, prices, risks, and scores.
2. During generation, desk-research 40 promising leads per lane (160), including competitive pricing and distribution hypotheses. The leads were deliberately chosen, not a random or exhaustive sample.
3. Construct a reproducible 300-row comparison cohort: the 40 researched leads plus the 35 highest raw-scoring other rows per lane. Lane notes may also retain their own earlier top-75 comparisons; those are separate views, not an identical cohort.
4. Compare 160 researched leads centrally, including direct-substitute falsification, source confidence, operational risk and cross-lane family overlap. Screened rows with attractive raw scores remain visible but do not outrank source-backed rows without further research.
5. Retain 90 by evidence-adjusted priority and 10 explicit exploratory positions for collector/personal and local one-time purchase models. Apply one selected candidate per conservative family; exclude lane rejects. Keep central operational risks qualitative to avoid counting the same risks twice. This is a portfolio judgment, not a statistically optimal allocation or 100 independent markets.
6. Stress-test the leading experiments against acquisition, churn, support, and $5,000 MRR arithmetic. Describe paid-test gates before product development.

These are analytical passes with evidence gathered concurrently, not claims that all 1,000 ideas passed sequential live market validation. The 300 is a documented comparison cohort, not 300 individually sourced markets. `build_research.py` records the exact cohort, deductions and selection so later evidence can change the result.

One explicit family preference retains W0511's narrowed, supplied-file client-signoff experiment over W0512 subtitle revision propagation, despite the sibling's higher raw score. The choice reflects a cheaper test boundary and deeper falsification, not stronger demand evidence. Lane reserve decisions remain visible and block automatic build advancement.

Selection records must retain exclusions and uncertainty. Customer interviews, paid pilots,
actual acquisition tests, and retention observation remain future empirical validation.
