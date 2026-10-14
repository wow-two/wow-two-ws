# Self-serve product research protocol

*Last updated: 2026-10-09*

## Decision

Rebuild the 100-product candidate pool for the user's clarified preference: products define their own
experience, deliver value without customer-specific process discovery or integrations, and give users
a reason to return. Kids Curiosity is selected by the user. Identify four additional priorities around
it, preserving ForeverPin, Pose Coach, Hijinx and Transcript Forge in their current execution lanes.
Research and roadmap selection are authorized; product implementation and publication are outside this turn.

## Why rebuild

The October 5 SaaS protocol explicitly required a persistent system of record, three connected stages
and collaboration between distinct roles. Its 100 records all have at least two roles. This shaped the
candidate pool before ranking; selecting another five from it cannot repair the missing consumer and
independently adopted product families. The old research remains useful for its original B2B question.

## Qualifying unit

- A complete, independently understandable experience with a named user, first useful result and repeat occasion.
- A product may serve an individual professional without importing a customer's business workflow.
- A proposed product must differ in the outcome, interaction and purchase decision, not merely a theme or language.
- No hardware manufacturing, inventory, shipping, two-sided marketplace, or required customer-specific integrations.
- Standard distribution, identity and billing integrations are allowed; they are not evidence of bespoke adoption.
- Prefer local computation or reviewed reusable content. Meter variable processing and state required content expertise.
- No automatic rejection for one user, low price, entertainment, or absence of organizational records.
- No automatic subscription claim: packs, lifetime and one-time products have zero subscription MRR.
- Existing apps receive no demand bonus. Their implementation can improve the speed of an experiment separately.
- If an idea is really a feature of another entry or an active app, replace it or explicitly consolidate it.

## Evidence

Each of 100 records needs at least one freshly opened primary source for a real alternative, with access
date, supported facts, relation (direct or adjacent), and exact URL. Reusing a source across genuinely
different outcomes is allowed but disclosed; 100 records do not imply 100 independently verified markets.
Search snippets alone do not verify prices. Unknown prices remain unknown. No invented revenue, market
size, conversion, retention, traffic, customers or success probability. Proposed prices are our hypotheses.
The final top five need at least two relevant alternatives and a concrete argument against building.

## Record contract

Save a JSON array of exactly 25 records to the assigned lane file. All fields below are required:

```json
{
  "id": "E001",
  "name": "Distinct proposed product",
  "family": "learning",
  "origin": "existing idea P140 / existing repository / new research proposal",
  "user": "Who uses and pays",
  "first_result": "Concrete first-session outcome",
  "loop": ["start", "do", "feedback", "return"],
  "return_trigger": "Natural repeat occasion; distinguish habit hypothesis from evidence",
  "paid_value": "Continuing benefit worth testing",
  "pricing": {"model":"subscription", "monthly_usd":8, "annual_usd":null, "basis":"hypothesis; no observed willingness to pay", "free":"bounded first result", "paid":"clear ongoing boundary"},
  "dependencies": ["Mandatory input, service, data or specialist review; none if none"],
  "compute": "local / curated / metered; explicit main driver and cap",
  "content_burden": "What must be authored and maintained",
  "first_scope": ["minimum complete experience", "second capability", "third capability"],
  "acquisition": "Specific demonstration or distribution experiment; unverified",
  "competitors": [{"name":"Real alternative", "url":"https://...", "accessed":"2026-10-09", "relation":"direct / adjacent", "facts":"paraphrased observed facts", "price":"verified exact billing/unit/currency or not verified"}],
  "difference": "Specific proposed distinction, unvalidated; not an assertion incumbent lacks it",
  "risk": "Strongest counterargument",
  "experiment": "Unaided first value -> independent return -> actual purchase test",
  "stop_rule": "Observable result that defeats the proposition; no fake industry benchmark",
  "overlap": "Other candidate / active product boundary",
  "scores": {"activation":4,"recurrence":4,"independence":4,"demonstrability":4,"paid_value":3,"differentiation":3,"feasibility":4},
  "rationale": "Why scores fit evidence and uncertainty",
  "disposition": "shortlist / reserve / defer",
  "confidence": "low; competitor evidence only"
}
```

Use null monthly pricing for a one-time product; record the purchase hypothesis in basis. Record known
annual pricing separately rather than pretending an annualized price is the monthly checkout price.
Avoid arbitrary precise engineering or revenue forecasts. $20–50/month before revenue remains a bounded
pilot cash target, not a measured total cost; editorial, support, acquisition and founder labor are separate.

## Ranking and challenge

Seven 1–5 judgment dimensions: activation 15, recurrence 20, independence 15, demonstrability 10,
paid value 15, differentiation 15, feasibility 10. Base = sum(weight * score / 5).
Do not call scores success probabilities. Differences under five points form one broad tier.

Every record receives a separate challenge pass checking evidence sufficiency, overlap, actual repeat
value, acquisition, operating burden and honest monetization. Reviewers can recommend a score change,
merge/replacement or disposition change with a reason; no opaque penalty is automatically subtracted.
Root resolves global duplicates and runs alternative recurrence-heavy and discovery-heavy rankings.
User selection of Kids Curiosity is recorded separately from its score, not manufactured by scoring.

### Interpretation and selection

Activation measures the path to a real first useful result, not merely account creation or a preview.
Independence measures freedom from individual customer discovery, integrations and live help. Standard
device permissions and reusable expert-authored content do not automatically reduce independence;
content expertise and maintenance belong primarily in feasibility. Recurrence measures a plausible
return occasion, not observed retention. Paid value and differentiation remain judgments about a
specific proposed offer, never inherited from the incumbent's price or popularity.

The five-product research recommendation combines the selected Kids Curiosity with four candidates
whose paid continuing job can be tested independently. Aggregate scores include one-time products and
therefore cannot directly define an MRR roadmap. High-scoring commodity timers, products with no
subscription, and concepts consolidated into another candidate do not become build priorities.
Keep reviewer downgrades visible; do not increase scores to make the recommendation look stronger.

One hundred means one hundred assessed candidate concepts. A challenge may reject a candidate as a
separate business and consolidate it into another product; disclose these cases rather than counting
them as extra roadmap slots. This is a fresh pool for the clarified brief, not proof that the older
1,000-to-100 research programme was completed.

## Ownership

Root owns protocol, E076–E100, integration, final evidence checks and the roadmap.
Learning/family lane owns E001–E025. Creative lane owns E026–E050. Play/hobby lane owns E051–E075.
Each agent writes only its assigned lane JSON. Cross-review artifacts have separately assigned filenames.
No outreach, account change, purchase, publication, app implementation or unrelated repository edit.
