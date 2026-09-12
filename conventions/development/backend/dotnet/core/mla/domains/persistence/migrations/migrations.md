# Migrations

*Last updated: 2026-09-10*

> Selecting one schema-evolution owner for a product database.

## Strategy

- must choose one strategy per owned database; do not apply competing journals to the same schema.
- must use [bespoke SQL](sql/bespoke-migrations.md) by default for owned Apply/Rollback scripts.
- may use [EF migrations](ef/ef-migrations.md) when the EF model owns schema evolution.
- may use [DbUp](dbup/dbup-migrations.md) for forward-only embedded script sets.
- must retain explicit schema ownership when changing strategy.

---

## Lifecycle

- must express schema changes as versioned migrations, not ad-hoc edits to a live database.
- must preserve applied migration content and identity; corrections normally roll forward.
- must apply development migrations before accepting work that depends on the new schema.
- must apply production migrations through an explicit deployment action, not silently on application startup.
- must guard rollback and repair against the resolved target when recovery requires them.
- must not infer production safety from an environment name alone.
- target guard → [migration tooling](sql/migration-tooling.md#destructive-operations).

---

## Coordination

- must serialize migration application against one database.
- must verify the chosen runner and provider supply a database-level migration lock before allowing concurrent applicants.
- must use one deployment applicant when that lock is absent or unverified.
- must not treat journal idempotency as mutual exclusion.
- must verify both repeat application and simultaneous application for a runner claiming concurrent safety.

---

## Delivery

- must embed SQL used by a runtime host in its deployment artifact.
- may use filesystem sources for CLI/development workflows.
- source and journal differences → [bespoke](sql/bespoke-migrations.md), [DbUp](dbup/dbup-migrations.md),
  [EF](ef/ef-migrations.md).
