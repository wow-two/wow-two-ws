# Development cycle

*Last updated: 2026-10-01*

> Two cycles per active app — implement a version in-app, then extract its stable blocks to the SDK + conventions and adopt across the active apps.
> Purpose — mature the apps and the shared SDK in parallel: ship fast in one product, harden once, propagate everywhere — never in isolation.
> Use case — reach for this at a version boundary: opening a version (cycle 1) or closing one that produced a proven, reusable block (cycle 2).

## Cycle = two versions

- a cycle maps to **two version numbers**: the **deliverable version** (cycle 1) then the **extraction version** (cycle 2) — **1 cycle = 2 versions shipped**.
- products start at `v0.1`, minor-increment per version, major only at `.100` or a breaking change — see [version-track.md](../planning/version-track/version-track.md).
- example: forever-pin `v0.1` (product + migrator built inline) → `v0.2` (migrator extracted to the SDK + adopted across apps) → `v0.3` next deliverable.

---

## Cycle 1 — implement (in-app)

- build the version's scope inside the app; iterate in sub-cycles until it ships.
- a product holds **business logic only**; everything cross-cutting belongs to the SDK.
- must adopt the SDK capability where one exists, and fix a missing or wrong API there (§ *SDK change loop*).
- may build a capability the SDK lacks inline to ship the version; its extraction is the next version's scope.
- which piece is generic → [extract / keep / remove](sdk-extraction.md).
- track the version in the app's planning per [version-track.md](../planning/version-track/version-track.md).

---

## Cycle 2 — extract & propagate

- when a block is **stable** (below), extract it to the SDK as a four-part deliverable: **SDK code · SDK tests · conventions doc · adoption**.
- write or update the convention(s) the block establishes — cite the SDK symbols, per the [authoring rules](../conventions.md).
- adopt the published package back in the **source app first** (prove parity), then across the **other active apps**.
- the active-app set is named **per chat by the human** — never assume the targets; adopt only the apps the active chat specifies.
- a breaking SDK change = a coordinated consumer update across the named apps; respect lane discipline ([agentic-workflow.md](../agentic-workflow/agentic-workflow.md)).

---

## Vector completeness — build the whole vector, not the ask

The defining rule of cycle 2. A known domain (forms, validation, auth, tables, storage) is built to completeness, proactively — the cost that kills velocity is **integration** with the rest of the component set, not invention; pay it once, in the SDK, fully.

- must treat the triggering product's need as the **trigger** to build the vector, not its **scope** — ship that product's essential slice, then complete the vector
- must, before building the completion, inventory every capability the vector integrates — an
  `engineering/research/{vector}-completeness.md` map, each capability with a verdict: ship-now /
  defer-with-named-trigger / skip-with-reason
- must complete the vector in a dedicated follow-up pass (its own chat) after the triggering product ships — so the **second** product finds the capability already present, never re-triggers the question
- must not gate a vector **capability** on "a consumer asked" — proactive to completeness is the default
- may gate an alternative **engine adapter** (a 2nd/3rd wrapping of the same capability, e.g. RHF beside TanStack) on preference/trigger once swap-freedom exists (≥2 adapters) — that is the lone exception, not a capability gap
- applies to both the backend and the frontend SDK
- track every vector + its completion iterations in the SDK repository's `engineering/planning/backlog.md` `Vectors` group — a new vector (e.g. i18n) gets a row there the moment it is triggered

---

## What "stable" means

- proven in a real product under tests — e.g. the bespoke migrator ran green (`ForeverPin.Tests.Integration` + `ForeverPin.Tests.Migrations`) in forever-pin before and after extraction.
- API surface settled — no churn expected that would force a second migration across consumers.
- documented — the convention exists, so the next adopter follows one path, not a re-derivation.

---

## A consumer never gates an SDK fix

The SDK is beta for as long as it takes, and its own shape outranks the contract it has with today's consumers.
A mature SDK is what makes every later product fast, so the maturing is the higher-value work — a consumer
re-pins and moves on.

- must fix a wrong shape in the SDK when one is found, whatever it breaks downstream.
- must not weigh "this breaks consumers" as a reason to keep a shape the conventions reject — the cost of
  carrying it compounds across every product built on it afterwards.
- must not soften a fix into an overload, a flag, or a parallel type to spare a consumer a re-pin.
- must name the break in the commit message, so a consumer knows what to change.
- the exception is a shape that is **right** and merely inconvenient; churn for its own sake is not a fix.

---

## SDK change loop — from a product chat

A product chat that needs the SDK changed makes the change, ships it and adopts it in one sitting.

- must add or fix the capability in the SDK repo, with its tests, rather than work around it in the product.
- must pass the SDK repo's own gates, then commit there — one repo, one commit; the product commit is separate.
- must push the SDK repo when its push flag is `ON` — main CI bumps (`0.0.y` npm, `10.y.z-beta` NuGet) and publishes.
- must wait for the published version before adopting — `npm view {package} version` or the NuGet feed.
- must re-pin the product to the published version, never a `file:` / `link:` path or a local build.
- must hand the push to the developer while the SDK push flag is `OFF`, naming the commit and the adoption left.
- must follow the release sync below after every SDK push.

---

## SDK release sync — after every push

Main CI answers every SDK push with a release commit (`chore: release … [skip ci]`); a commit made beside it forks
`main`. The rule applies to any chat that pushes an SDK repo, product chat or SDK lane.

- must wait, after pushing an SDK repo, for main CI's release commit to land on `origin/main`.
- must then `git pull --ff-only` and make the next commit on top of the release commit.
- must not commit in that repo while its release run is in flight — queue the work, or do it in another repo.
- must rebase unpushed commits onto `origin/main` when a release commit landed beside them, then push.
- may hand the wait to a background agent or shell that waits the average release time, then pulls.
- the average release time — UI SDK ≈ 7 min, backend SDK ≈ 10 min; `gh run list --workflow` gives today's figure.
- a failed release run lands no release commit; fix forward, and the next push releases.

---

## Representation choices

- must rank representations that preserve the domain ahead of narrower implementation-driven limits.
- must treat restricted ranges, precision or capacity as the last option in every design decision.
- must account for future values exceeding the limit and the cost of enforcing it across every boundary.
- must prefer a wider type, lossless codec or reusable SDK capability over scattered constraint workarounds.
- must document rejected alternatives and centralized overflow handling when a restricted representation is unavoidable.
- must distinguish genuine domain rules from limits introduced by a chosen implementation.
- must retain explicit resource budgets for untrusted input; exhaustion must fail rather than corrupt values.

---

## Roles — every app is both source and target

- **source** — the app that pioneered a block extracts it (current set: wheelhouse → presentation/controller conventions; forever-pin → the migration layer).
- **target** — every other active app adopts the block once it is stable.
- a target that can't yet adopt (different stack) is **noted, not forced** — e.g. an EF/SQLite app waits for the dialect before taking a Postgres-only block.
