# Self-serve products after Hijinx and Pose Coach

*Last updated: 2026-10-09*

> Historical first-pass assessment. The user subsequently selected Kids Curiosity. The
> [rebuilt 100-candidate analysis](../self-serve-research-2026-10/self-serve-research-2026-10.md)
> supersedes the preparation ranking below and records the five research priorities. The current
> execution order lives in the [central roadmap](../../system/planning/pln-tasks.md#venture-product-order).

## Decision

**Arcade, narrowed to daily solo puzzles, is the best existing product to assess next.**
It already contains playable implementations and a repeat-play structure. Its current cosmetic-purchase
model is not subscription MRR; a membership would be a proposed product change, not an existing feature.

**Formula Drill Gym is the strongest new product from the existing idea list under the low-dependency
constraint.** It supplies the task, data, rules, feedback and progression. Kids Curiosity is the more
consumer-oriented third choice, with a larger continuing editorial burden.

This is a judgment about fit and the cost of learning, not a probability-of-success estimate. No new
product is added to the execution queue. ForeverPin, Pose Coach, Hijinx and Transcript Forge remain
with their existing chats. The earlier B2B recommendation is superseded for this discussion.

---

## The corrected selection rule

The user's distinction is **who defines the workflow**. A good candidate teaches its own use and gives
one person or a ready-made group a result without importing an organization or adapting to its processes.
Professional tools can qualify too: a spreadsheet practice game is self-serve even when it improves job skills.

The earlier [own-ideas scoring](../own-ideas-review-2026-10/own-ideas-review-2026-10.md) required a persistent
record, three connected stages and two roles. It explicitly penalized consumer products for failing that
business-workflow test. That qualification gate does not answer the user's current question; its numerical
ranking should not be reused as a verdict on Hijinx, Pose Coach or Arcade.

Compare these dimensions instead:

| Dimension | Favor |
|---|---|
| First result | A complete activity before substantial setup or data entry |
| Guided use | The product supplies the sequence, rules and useful feedback |
| Independence | No customer-specific integration, other company approval or network cold start |
| Return value | Fresh play, accumulated skill or recurring practice with visible progress |
| Discovery | A result or short demonstration that explains why somebody would try it |
| Delivery burden | Bounded compute and manageable content production |
| Paid boundary | An understandable upgrade that adds continuing value |

This reduces sales and implementation friction. It does not establish cheaper acquisition or stronger
retention. A share button is only a distribution hypothesis until recipients actually start and finish.
Low compute can still hide substantial design, puzzle construction or curriculum work.

---

## Shortlist

| Priority | Product | Guided experience | Why return | State and principal gap |
|---|---|---|---|---|
| 1 | Arcade: daily solo skill/puzzles | Open today's challenge → learn by playing → result → retry/share | Fresh boards and improving personal performance | 15 game entries implemented; release acceptance and recurring offer unverified |
| 2 | Formula Drill Gym, P037 | Attempt supplied spreadsheet task → receive precise feedback → retry | Adaptive practice of weak skills and harder challenges | Idea only; curriculum and grading engine needed; direct competition exists |
| 3 | Kids Curiosity, P140 | Choose a question → short illustrated explanation/activity → playful check | New questions and connected learning chapters | User-seeded idea; reviewed content and child-appropriate experience need sustained care |
| 4 | Next Set, I04 | Follow program → log completed sets → see next prescribed session | Each workout updates the next step | Idea only; program quality and differentiation from established fitness apps |
| 5 | Hifz revision, P057 | Open today's review → practise → record recall → receive next review | Long-term memorization and revision | Idea only; informed domain review; avoid teacher administration as the initial requirement |
| 6 | PBN Studio | Upload photo → adjust palette → export numbered painting pattern | Another creative project or repeated seller production | Client-side implementation exists; print quality and repeat subscription value remain open |

Additional concepts considered: chess repertoire practice, IELTS writing practice, drawing practice,
speaking rehearsal, art learning and local activity discovery. Their dispositions appear below.

### 1. Arcade: the next existing-product experiment

The [current backlog](../../workbench/maxs-projects/ventures/consumer/ventures.arcade/engineering/planning/backlog.md) and
[game catalog](../../workbench/maxs-projects/ventures/consumer/ventures.arcade/engineering/codebase/arcade.frontend-services/apps/web/src/domain/games/GameCatalog.ts)
contain fifteen implemented games. The [version track](../../workbench/maxs-projects/ventures/consumer/ventures.arcade/engineering/planning/version-track/v0.1/v0.1.md)
still has verification work open. Those are implementation observations, not a live-product acceptance result.

- Lead with one distinctive daily challenge, not a fifteen-game launcher.
- Existing Make-Ten Rush supplies solvable arithmetic puzzles; Echo Grid supplies immediate memory play.
- Keep entry usable in a plain browser; Telegram can be a distribution surface rather than a prerequisite.
- Use personal improvement and asynchronous challenges to distinguish it from Hijinx's hosted social play.
- Hot Take, Decoy and other pass-the-phone games overlap Hijinx; expanding that branch adds little portfolio breadth.

The [current product definition](../../workbench/maxs-projects/ventures/consumer/ventures.arcade/product/product.md) permits cosmetic
Telegram Stars purchases. Those are one-time receipts. A daily-puzzle membership with additional original
challenges and archives is a **proposal** to assess, not a silent replacement of the existing policy.

[Puzzmo's US listing](https://apps.apple.com/us/app/puzzmo-solve-smile-share/id6714482734) shows a comparable
daily-puzzle subscription at $3.99/month. It establishes an available offer, not our ability to sell it.
Puzzle quality, originality and return behavior matter more than increasing the number of modes.

**First evidence milestone:** someone unfamiliar with the game completes it without instruction, chooses
to play another day, and another person starts from the shared result. Test the premium proposition against
that returning cohort. Do not count cosmetics or a paid pack as subscription retention.

### 2. Formula Drill Gym: the cleanest new build

The existing [P037 idea](../../workbench/maxs-projects/ventures/10x-ventures/product-ideas.md) already describes browser
spreadsheet challenges, grading and spaced practice. The first version should own its small datasets and
supported formula subset. Customer spreadsheets, employer integrations and enterprise administration are
unnecessary for this experience. Deterministic tasks do not require an LLM.

One complete session: a short diagnostic → a realistic task → an explained mistake → a retry with changed
data → later recall. The paid reason is improving capability through a useful practice program.

The old claim that this practice category is unserved is false: [ExcelExercises](https://excelexercises.com/premium.html)
offers interactive practice, interview assessments and repeatable lessons at $19.99/month or $59.99/year;
it also lists a $199 lifetime option. [Excel Practice Online](https://excel-practice-online.com/) supplies
free exercises. A tutorial library or cheaper clone is an insufficient proposition.

**Possible distinction to test:** diagnose a particular misunderstanding, make the learner correct it,
and verify transfer to an unfamiliar task. This is a proposed distinction, not a verified competitor gap.
Job-interview preparation can sell but may end quickly; sustained professional practice is a separate
retention hypothesis. Course completion should remain useful even when a subscription ends.

**First evidence milestone:** a learner independently completes the lesson and returns for another
session, then solves a new variant rather than merely remembering the supplied answer.

### 3. Kids Curiosity: the strongest broader consumer alternative

The user-seeded [P140 concept](../../workbench/maxs-projects/ventures/10x-ventures/product-ideas.md) connects a child's
question with a short chapter and understanding check. Start with a bounded, reviewed collection and
parent-led use. Unrestricted live generation, voice pipelines and teacher dashboards are unnecessary to
test whether the experience earns another visit.

The product supplies a question choice, explanation, small activity and satisfying discovery. It must be
better as an experience than reading a chatbot answer. Fresh topics and connected chapters can support
recurrence; the editorial work is part of the product's cost.

[KidCoach](https://www.kidcoach.app/) already offers brief parent-child conversations with fresh monthly
questions and a subscription. That is adjacent evidence of the model, not proof of a gap or of our demand.
Its page does not specify an exact current price, so none is asserted here.

**First evidence milestone:** a parent and child finish one chapter without explanation from the founder,
choose another voluntarily, and later use the product again. Measure that behavior before building a
general-purpose child chatbot or a large content catalog.

---

## Reserves and new adjacent concepts

| Candidate | Assessment |
|---|---|
| Next Set, existing I04 | Strong recurrence and deterministic core. Start with reviewed program rules and manual logging. [Fitbod](https://fitbod.me/faqs/) already offers personalized workout plans, so “tells you the next workout” is not novel. No camera diagnosis or wearables are needed for the proposed initial scope. |
| Hifz revision, existing P057 | Daily individual revision fits well. A guided recall schedule is cheaper than live recitation recognition. [Tarteel](https://tarteel.ai/en/pricing) already sells planning/progress and mistake detection; teacher dashboards would reintroduce coordination. |
| PBN Studio, existing implementation | Immediate creative output with on-device processing. Current [context](../../workbench/maxs-projects/ventures/saas/ventures.pbn-studio/product/context.md) says browser verification and pricing remain open. Its [backlog](../../workbench/maxs-projects/ventures/saas/ventures.pbn-studio/engineering/planning/backlog.md) records thin-region and outline-quality problems. Better fit for per-project sales until repeated seller usage is demonstrated. |
| Drawing practice, new adjacent proposal | Draw → compare proportions/perspective → retry without guidance. Strong visual demonstration and enjoyable progress. [ShadowDraw](https://www.shadowdrawapp.com/faq) already combines free daily entry, artist-authored lessons and subscription access. Original teaching material and actual skill transfer are the hard work. |
| Speaking rehearsal, new adjacent proposal | Prompt → record → inspect pacing/pauses → retry. Basic local analysis is bounded; useful semantic/accent feedback adds processing and calibration. [Speeko](https://www.speeko.co/subscriptions) already sells exercises and feedback. Reserve until the coaching advantage is specific. |
| Chess repertoire, existing P121 | Natural practice loop, but the documented advantage uses imported games to find deviations. Removing those inputs weakens differentiation; importing them raises activation burden. Start with an optional file only if revisited. |
| IELTS writing, existing P036 | Guided self-study fits; reliable feedback calibration is harder than generating advice. Exam-driven churn and inference cost make it less attractive than deterministic practice for this lane. |
| Daily art learning, new proposition | Artwork → story → recognition challenge gives a clear repeatable experience. [DailyArt](https://apps.apple.com/us/app/dailyart/id547982045) already sells this broad category. This would be a new learning product, not the existing Uzbekistan Museums Gallery. |
| Local activity discovery / Museums Gallery | Easy interface, but current venue facts, hours, media rights and payer uncertainty bring external operational dependencies back. Lower fit for the user's clarified constraint. |

Couple question decks and home activities belong with Hijinx; photo missions belong with Pose Coach.
Neither requires another product, brand or customer-acquisition effort merely because it can be packaged separately.

---

## Validation through use

Replace the B2B interview/artifact funnel with a small complete product experience:

1. A public sample or demo explains the activity through use, before requiring account creation where feasible.
2. Observe unaided completion, confusion, abandonment and whether the result satisfies the promise.
3. Measure return on another day or practice occasion; distinguish voluntary return from prompted testing.
4. Follow a shared result through to a recipient's completed session; sharing alone proves little.
5. Present the actual premium boundary, observe purchase, and later measure renewal and support cost.

These are proposed experiments, not actions executed this turn. Customer observation still helps, but it
does not require bespoke integration discovery or sales calls as the entry point. No numeric success rate
or retention threshold is invented from competitor listings.

At a realized $5/month, $5K gross MRR requires 1,000 active subscriptions. At $10/month it requires 500.
Those are scale requirements, not reasons to reject consumer products. Annual plans contribute their
annual price divided by twelve; one-time packs and lifetime purchases do not create subscription MRR.

**Recommended sequence:** assess one Arcade daily experience first; retain Formula Gym as the leading
new subscription concept and Kids Curiosity as the broader consumer alternative. Do not open all three
implementation lanes from this analysis. The existing four release lanes remain unchanged.

## Evidence boundary

Local sources and official competitor pages were reviewed on 2026-10-09. No product runtime, game session,
customer cohort, payment or renewal was tested. Reported implementation states come from source and
repository records. The shortlist does not claim a complete market survey or measured success likelihood.
