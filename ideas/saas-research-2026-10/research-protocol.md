# Research protocol for one hundred SaaS products

Research date: 2026-10-05. This is a fresh product selection exercise, superseding the earlier micro-SaaS ranking for this decision. Existing code receives no scoring bonus. The previous 1,000-to-100 funnel is not represented as completed.

## Decision and constraints

Identify 100 distinct software businesses that can own an ongoing customer workflow, rank them, and recommend a small validation portfolio capable in principle of reaching $5,000 total monthly recurring revenue across one to three products. This is desk research, not customer validation or an instruction to build 100 applications.

Global software delivery, English-first acquisition, and no physical fulfillment are required. Software may serve service providers, but candidate success must not require us to own goods, employ physical operators, or establish a two-sided marketplace. Favor customers reachable from a small remote team.

The user permits $20–50 monthly operating cost per product before revenue, potentially about $300 after revenue. These are pilot cash-cost envelopes, not all-in business costs or promises at scale. Engineering time, customer support, payment fees, taxes, acquisition and third-party usage are separate. Each idea must identify usage limits and any dependency preventing the initial envelope.

## Qualification

A qualifying SaaS owns a persistent system of record, at least three connected workflow stages, recurring decisions, and collaboration between distinct roles. A narrow first release is acceptable when the expansion path stays within the same buyer and workflow. A checker, calculator, isolated generator, reminder or dashboard without this path is a feature, not a qualifying product here. More features alone do not establish a viable business.

Each record names the initial customer segment, budget owner, current workaround, costly recurring job, proposed entry point, persistent record, full workflow, why payment is plausible, distribution, defensibility hypothesis, competition, launch risks and a falsifiable validation test. Similar candidates must differ in their core record or operating workflow; superficial industry reskins do not count twice.

## Evidence

Every candidate requires at least one live-opened official competitor/product/pricing source. Capture URL, observation date, supported facts and an observed price with currency, billing basis, unit and minimum commitments where explicit. If no price can be confirmed, write “not verified” or “contact sales”; never guess. Search snippets identify sources but are insufficient for a confirmed price when full pages are available. Vendor claims are attributed to the vendor and do not establish independent customer outcomes.

Paid competitors establish a commercial category, not an unmet need or willingness to buy our product. Proposed pricing, demand, wedge, acquisition, score, effort and operating estimates are analyst hypotheses. Top candidates get a second relevant competitor source plus an explicit argument against building. Do not fabricate market size, search volumes, user counts, conversion, CAC or competitor revenue.

## Scoring

Eight dimensions, integers 1–5, where 5 is most favorable. Weighted base score is sum(weight × dimension / 5), rounded to one decimal. Scores are prioritization judgments, not success probabilities.

| Dimension | Weight | Meaning of a high score |
|---|---:|---|
| pain | 20 | Recurring loss or delay with an identifiable budget owner |
| recurrence | 15 | Repeated use and persistent operational records |
| budget | 15 | Plausible recurring budget relative to saved work |
| distribution | 15 | Specific reachable initial buyers and credible acquisition route |
| wedge | 15 | Defensible focus against current alternatives |
| feasibility | 10 | Small team can implement and support the first useful workflow |
| global | 5 | Low localization, regulatory and regional dependence |
| cost | 5 | Bounded variable costs fit the bootstrap cash envelope |

Round one screens product shape and evidence. Round two independently challenges duplicates, broad claims, switching cost, distribution, security and cost; recorded penalties of 0–20 points produce a final score. Round three deepens a small shortlist and compares ranks under distribution-first and feasibility-first weights. Rank ties are broken by distribution, wedge and stable ID, not by invented decimal certainty.

Statuses are Validate, Reserve and Defer. None means “build approved.” Each final record keeps its base score, challenge penalty and reason, final score, evidence confidence and fatal gate. Official source observed = category evidence; pilot willingness to pay = unvalidated unless actual customer evidence is collected.

## Economics and validation

Proposed prices are USD monthly workspace/account hypotheses unless explicitly stated otherwise. Accounts required for $5,000 MRR = ceiling(5000 / proposed monthly price), before churn, discounts, fees, support and taxes. Lifetime sales and setup fees never count as MRR. Freemium requires a capped, inexpensive solo or preview tier; sustained hosted collaboration defaults to subscription. A lifetime license is only considered for finite/offline capabilities or clearly capped prepaid use.

Before committing to a build, each candidate receives a concierge test with a proposed pilot price and rejection condition. Suggested internal gates are ten qualified interviews, five workflow demonstrations using real customer artifacts, and three paid pilot commitments; these are decision thresholds, not market benchmarks. No outreach, purchase, account creation or publication is authorized by this research task.

## Output

Four disjoint 25-product lanes produce JSON records, then a consolidated 100-product catalog, evidence register, rank table, shortlist and validation recommendation. Root owns integration and independent challenges. Existing applications and other sessions remain untouched.

Lane ownership: business agent S001–S025, creator agent S026–S050, developer agent S051–S075, root S076–S100. The attached schema is the integration contract.
