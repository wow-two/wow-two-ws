# WoW 2.0 — Platform Model & Build Strategy

*Last updated: 2026-06-20*

> How every wow-two platform capability is **shaped, shipped, and promoted**: the three distribution forms · the build-now-promote-later lifecycle · the parallel-bricks delivery rule. Read this before designing any new platform component.

## North Star

Build the **best platform to build apps fast — with reliable, battle-tested code**. A radical-engineering substrate that serves three audiences at once:

- **wow-two apps** — the micro-SaaS portfolio (ship many, fast).
- **myself** — personal products.
- **other devs** — eventual **non-profit OSS**, free to use.

Not commercial. The product is *leverage*: a new app should need near-zero infra work and inherit production-grade reliability for free.

## The Three Distribution Forms

Every platform capability (secrets, identity, comms, jobs, …) is delivered in **one or more of three forms**. A consumer picks the form that fits its stage and **migrates up on demand** — same logic, heavier isolation, less consumer effort.

| # | Form | What ships | Runs where | Consumer effort | Isolation | Analogy |
|---|------|-----------|-----------|----------------|-----------|---------|
| 1 | **Wireable infra** | SDK component (library) | In-process, inside the consumer API | Wire it + own its config/storage | none (shared process) | embedded lib |
| 2 | **Self-hosted service** | API-client lib **+ Docker image** | Sidecar/container the consumer spins up | Wire client + run container | process/container | sidecar |
| 3 | **Provided service** | API-client lib only | **We host it centrally**; consumer just calls | Wire client only | full (managed) | managed SaaS |

**Form 1 → 2 → 3 = increasing isolation, decreasing consumer effort.** The logic is identical; only the deployment boundary moves.

### How a component offers forms

- A component may offer **1, 2, or all 3** forms depending on the logic.
- Start with whichever form is **cheapest to ship**; add forms as demand appears.
- The **client contract stays stable across forms** — consumers migrate by *config, not rewrite*.

### Worked examples

- **secrets-vault** — today **Form 2** (Docker image + client). Next: add **Form 1** (wireable kit) so a brand-new micro-SaaS embeds it in-process, then **shifts to Form 2** when it needs isolation. (Form 3 later if one central vault makes sense.)
- **identity** — needs **all 3**. Wire it in-process first (**Form 1**, already ~there via the `backend.beta` identity slice) → split to a self-hosted identity container (**Form 2**) → finally run **one central wow-two identity provider** (**Form 3**) so apps stop minting their own OAuth clients across every provider.

## Build-Now, Promote-Later

We don't gate building on "is it ready." Build into **beta**, harden over months, then promote.

```
Build in beta  →  battle-harden   →  migrate beta→stable  →  shake repos    →  OSS promote
(sdk-beta,        (tests cover all   (beta SDK → real        (clean-commit     (non-profit,
 platform.*,       angles; survive    wow-two-sdk; full       rebuild of the    public, free)
 drydock)          real product use)  checks + semver)        promoted set)
```

1. **Build in beta** — everything starts in `wow-two-sdk-beta` / `wow-two-platform` (private, fast-moving, beta-forever, `0.x`, auto-bump on push).
2. **Battle-harden** — real wow-two apps consume it; tests grow to cover all angles; APIs *survive the battles*.
3. **Migrate beta → stable** — graduate proven libs from `wow-two-sdk-beta` into the public `wow-two-sdk`; add full checks (semver, docs, CI gates).
4. **Shake the repos** — rebuild the promoted set with **clean commit history**; git history is disposable until promotion.
5. **OSS promote** — release as non-profit OSS products.

**Implication:** the empty `wow-two-sdk.language.*` repos are *intentional* — the real code lives in beta until it earns promotion. Don't "fix" them.

## Parallel Bricks — No Hard Ordering

We do **not** sequence "finish A, then start B." Platforms grow together.

- Build **A**; if **B** needs a piece of A, build that piece and consume it mid-flight.
- "**2 bricks in A, 3 bricks in B**" — interleave; no platform blocks on another being "done."
- Consume-while-building is the norm: `drydock` reuses `secrets-vault` patterns before secrets-vault is finished; apps use `backend.beta` while it's still beta.
- The dependency map is a **pull graph**, not a waterfall: a consumer pulls the API it needs → the producer bumps it → the consumer re-pulls.

So **"what to build first" is the wrong frame**. The right frame: *which brick unblocks the most consumers per unit effort?* The roadmap ranks **bricks**, not whole platforms.

## Designing a New Platform Component — Checklist

1. **Capability** — what single concern does it own? (one bounded context)
2. **Forms** — which of the 3 does it need *now*? Default to the cheapest; plan the migrate-up path.
3. **Client contract** — define the stable client API **first**; it must not change across forms.
4. **Config & storage ownership** — Form 1: consumer owns it. Form 2/3: the component owns it.
5. **Promotion path** — where it lives in beta + the bar to graduate to stable SDK.
6. **Consumers** — who pulls it? (drives bump cadence; see `conventions/agentic-workflow/`).

## See also

- `docs/wow-two-refinement.md` — master vision & layer model (KB → Platform → SDK → Apps)
- `docs/beta-launch.md` — beta-forever strategy, naming, `0.x` auto-bump
- `docs/versioning-strategy.md` · `docs/branching-strategy.md`
- `conventions/development/backend/service-architecture.md` — once the forms stabilize, graduate the rules here
- `docs/platform-roadmap.md` *(coming)* — ranked brick backlog from the platform-apps deep-research
