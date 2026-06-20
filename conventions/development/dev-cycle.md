# Development cycle

*Last updated: 2026-06-18*

> Two cycles per active app — implement a version in-app, then extract its stable blocks to the SDK + conventions and adopt across the active apps.
> Purpose — mature the apps and the shared SDK in parallel: ship fast in one product, harden once, propagate everywhere — never in isolation.
> Use case — reach for this at a version boundary: opening a version (cycle 1) or closing one that produced a proven, reusable block (cycle 2).

## Cycle = two versions

- a cycle maps to **two version numbers**: the **deliverable version** (cycle 1) then the **extraction version** (cycle 2) — **1 cycle = 2 versions shipped**.
- products start at `v0.1`, minor-increment per version, major only at `.100` or a breaking change — see [version-docs.md](../planning/version-planning/version-docs.md).
- example: smart-qr `v0.1` (product + migrator built inline) → `v0.2` (migrator extracted to the SDK + adopted across apps) → `v0.3` next deliverable.

---

## Cycle 1 — implement (in-app)

- build the version's scope inside the app; iterate in sub-cycles until it ships.
- a product holds **business logic only**; cross-cutting infrastructure (migrations, auth, hosting, result/mediator plumbing) is built **inline** in the app to move fast.
- don't pre-extract — a block earns extraction by proving itself in a real product first.
- track the version in the app's planning per [version-docs.md](../planning/version-planning/version-docs.md).

---

## Cycle 2 — extract & propagate

- when a block is **stable** (below), extract it to the SDK as a four-part deliverable: **SDK code · SDK tests · conventions doc · adoption**.
- write or update the convention(s) the block establishes — cite the SDK symbols, per the [authoring rules](../conventions.md).
- adopt the published package back in the **source app first** (prove parity), then across the **other active apps**.
- the active-app set is named **per chat by the human** — never assume the targets; adopt only the apps the active chat specifies.
- a breaking SDK change = a coordinated consumer update across the named apps; respect lane discipline ([agentic-workflow.md](../agentic-workflow/agentic-workflow.md)).

---

## What "stable" means

- proven in a real product under tests — e.g. the bespoke migrator ran green (`SmartQr.IntegrationTests` + `SmartQr.Migrations.Tests`) in smart-qr before and after extraction.
- API surface settled — no churn expected that would force a second migration across consumers.
- documented — the convention exists, so the next adopter follows one path, not a re-derivation.

---

## Roles — every app is both source and target

- **source** — the app that pioneered a block extracts it (current set: drydock → presentation/controller conventions; smart-qr → the migration layer).
- **target** — every other active app adopts the block once it is stable.
- a target that can't yet adopt (different stack) is **noted, not forced** — e.g. an EF/SQLite app waits for the dialect before taking a Postgres-only block.
