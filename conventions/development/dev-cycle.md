# Development cycle

*Last updated: 2026-06-18*

> Two cycles per active app — implement a version in-app, then extract its stable blocks to the SDK + conventions and adopt across the active apps.
> Purpose — mature the apps and the shared SDK in parallel: ship fast in one product, harden once, propagate everywhere — never in isolation.
> Use case — reach for this at a version boundary: opening a version (cycle 1) or closing one that produced a proven, reusable block (cycle 2).

## Cycle = two versions

- a cycle maps to **two version numbers**: the **deliverable version** (cycle 1) then the **extraction version** (cycle 2) — **1 cycle = 2 versions shipped**.
- products start at `v0.1`, minor-increment per version, major only at `.100` or a breaking change — see [version-track.md](../planning/version-track/version-track.md).
- example: smart-qr `v0.1` (product + migrator built inline) → `v0.2` (migrator extracted to the SDK + adopted across apps) → `v0.3` next deliverable.

---

## Cycle 1 — implement (in-app)

- build the version's scope inside the app; iterate in sub-cycles until it ships.
- a product holds **business logic only**; cross-cutting infrastructure (migrations, auth, hosting, result/mediator plumbing) is built **inline** in the app to move fast.
- don't pre-extract — a block earns extraction by proving itself in a real product first.
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
- must, before building the completion, inventory every capability the vector integrates — a `docs/analysis/{vector}-*.md` completeness map enumerating all, each with a verdict: ship-now / defer-with-named-trigger / skip-with-reason
- must complete the vector in a dedicated follow-up pass (its own chat) after the triggering product ships — so the **second** product finds the capability already present, never re-triggers the question
- must not gate a vector **capability** on "a consumer asked" — proactive to completeness is the default
- may gate an alternative **engine adapter** (a 2nd/3rd wrapping of the same capability, e.g. RHF beside TanStack) on preference/trigger once swap-freedom exists (≥2 adapters) — that is the lone exception, not a capability gap
- applies to both the backend and the frontend SDK
- track every vector + its completion iterations in the SDK's `docs/planning.md` Vectors table — a new vector (e.g. i18n) gets a row there the moment it is triggered

---

## What "stable" means

- proven in a real product under tests — e.g. the bespoke migrator ran green (`SmartQr.IntegrationTests` + `SmartQr.Migrations.Tests`) in smart-qr before and after extraction.
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

## Roles — every app is both source and target

- **source** — the app that pioneered a block extracts it (current set: drydock → presentation/controller conventions; smart-qr → the migration layer).
- **target** — every other active app adopts the block once it is stable.
- a target that can't yet adopt (different stack) is **noted, not forced** — e.g. an EF/SQLite app waits for the dialect before taking a Postgres-only block.
