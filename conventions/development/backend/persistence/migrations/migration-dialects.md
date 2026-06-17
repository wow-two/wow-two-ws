# SQL Authoring

*Last updated: 2026-06-16*

> Author-facing Apply/Rollback SQL dialect idioms for the bespoke migrator — Postgres today, SQLite/SqlServer later.
> Purpose — the engine runs `.sql` **verbatim** (no auto-quote, rewrite, or portability check), so per-provider correctness is the author's job.
> Use case — reach here when hand-writing a migration's `Apply.sql` / `Rollback.sql` and needing the dialect-correct form.

---

## Scope

- Engine lifecycle + file layout → [bespoke-migrations.md](bespoke-migrations.md); this doc is dialect idioms only.
- Distinct from the engine's internal `IMigrationDialect` seam (SDK `Bespoke/bespoke.md`) — that owns the migrator's *own* SQL (advisory lock,
  `migration_history` DDL), not your migration SQL.

---

## Postgres

> The only shipping dialect. SQLite / SqlServer get sibling `##` sections when those tracks land — until then, every rule below is
> Postgres-specific.

### Reserved-word quoting

- The engine does **not** auto-quote (EF does; raw SQL does not). Hand-quote any reserved word with double quotes: `"order"`, `"user"`, `"group"`.
- Quote it **everywhere** the column appears — `CREATE TABLE`, every index, every constraint, every `Rollback.sql` reference.
- Canonical example — `routing_rules."order"` in `001-baseline/Apply.sql`:

```sql
CREATE TABLE routing_rules (
    id       uuid    NOT NULL,
    "order"  integer NOT NULL,
    ...
);
CREATE INDEX ix_routing_rules_code_id_order ON routing_rules (code_id, "order");
```

- Prefer renaming around reserved words when the schema is still fluid; quote only when the column name is load-bearing (a domain term like `order`).

---

### Rollback idioms

- Every `Apply.sql` ships a paired `Rollback.sql` that **inverts** it — mandatory to author (a missing one fails the scan); at run time it's a
  guarded recovery op (gated by `MigrationOptions.AllowRollback`) — roll forward by default, prod-allowed for recovery. Mandate + gating →
  [bespoke-migrations.md](bespoke-migrations.md).
- **Reverse dependency order** — drop children before parents (the inverse of Apply's create order). A child holding an FK to a parent can't be
  dropped after the parent is gone.
- **`IF EXISTS` + `CASCADE`** on every drop — the script must be safe on partial state (a half-applied `@no-transaction` Apply, or a re-run).
- `001-baseline` is the reference — Apply creates `codes` → `routing_rules` → `scan_events`; Rollback drops the reverse:

```sql
DROP TABLE IF EXISTS scan_events CASCADE;
DROP TABLE IF EXISTS routing_rules CASCADE;
DROP TABLE IF EXISTS codes CASCADE;
```

- `CASCADE` also clears dependent objects the Apply created implicitly (FKs, indexes) without listing each — drop the table, not its parts.
- Inverting an `ALTER TABLE ... ADD COLUMN` → `ALTER TABLE ... DROP COLUMN IF EXISTS`. Inverting `CREATE INDEX` → `DROP INDEX IF EXISTS`.
- A native-enum `ADD VALUE` is **not** reversibly rollback-able (PG can't drop an enum label) — leave a no-op `Rollback.sql` with a comment saying
  so; roll forward instead.

---

### `@no-transaction` idempotency

- Default: the engine wraps each file in a per-file transaction (PG transactional DDL) — a failed Apply leaves zero partial schema, so plain
  non-idempotent DDL is fine.
- A file led by `-- @no-transaction` runs **outside** a transaction and records **separately** — a crash mid-file leaves it partially applied **and
  unrecorded**, so the next run **re-executes** it. The directive + recording semantics are the engine's
  ([bespoke-migrations.md](bespoke-migrations.md)); the **idempotency idioms** below are the author's.
- Therefore: a `@no-transaction` Apply **MUST be idempotent** — re-running it on a partially-applied state must succeed. Non-negotiable.

Idempotency idioms:

| Idiom | Use |
|---|---|
| `CREATE INDEX CONCURRENTLY IF NOT EXISTS …` | the common case — concurrent index build |
| `IF NOT EXISTS` / `IF EXISTS` on every `CREATE`/`DROP`/`ALTER` | guards re-execution |
| guarded `DO $$ … $$` block | conditional logic a bare `IF NOT EXISTS` can't express |

```sql
-- @no-transaction
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_codes_user_id ON codes (user_id);
```

```sql
-- @no-transaction
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'code_status') THEN
        CREATE TYPE code_status AS ENUM ('active', 'paused');
    END IF;
END $$;
```

**Statements that forbid a transaction** (must carry `-- @no-transaction`):

| Statement | Why |
|---|---|
| `CREATE INDEX CONCURRENTLY` | concurrent build can't run inside a tx block |
| `ALTER TYPE … ADD VALUE` | new enum label not usable in the same tx that adds it (PG) |
| `VACUUM` / `VACUUM FULL` | maintenance commands forbid a tx block |
| `REINDEX … CONCURRENTLY` | same concurrent-build constraint |

- Keep `@no-transaction` files **single-statement** where possible — each statement autocommits independently, so a multi-statement file has
  multiple partial-failure points to make idempotent.

---

### Native enum changes

- Adding a value to a native PG enum **is** a migration — `ALTER TYPE foo_status ADD VALUE 'archived'`.
- `ADD VALUE` cannot run in a transaction → the file **must** be `-- @no-transaction`:

```sql
-- @no-transaction
ALTER TYPE code_status ADD VALUE IF NOT EXISTS 'archived';
```

- `IF NOT EXISTS` on `ADD VALUE` makes it idempotent (required per the `@no-transaction` rule above).
- Creating a brand-new enum type (`CREATE TYPE … AS ENUM (…)`) inside `CREATE TABLE`-adjacent DDL **can** run in a normal transactional migration —
  only `ADD VALUE` against an existing type forces `@no-transaction`.
- The C#/EF side (mapping the enum, `NpgsqlDataSourceBuilder.MapEnums(CaseStyle.Snake, …)` via `PostgresServiceCollectionExtensions`, snake_case
  labels) → [../enums.md](../enums.md). PascalCase C# `Archived` ↔ PG label `'archived'` — author the SQL label in snake_case to match.

---

### Schema-mirror discipline

- Apply SQL **is** the schema-first source of truth — EF maps over it, never generates it ([bespoke-migrations.md](bespoke-migrations.md),
  `database.md`).
- Write columns to mirror the EF model the product already uses — snake_case names, enums-as-native-type (or text on non-PG), `jsonb` for JSON,
  `timestamptz` for instants. `001-baseline/Apply.sql` is the worked example (see its header comment).
- Name constraints explicitly — `CONSTRAINT pk_codes PRIMARY KEY (id)`, `CONSTRAINT fk_routing_rules_codes_code_id FOREIGN KEY (code_id)
  REFERENCES codes (id) ON DELETE CASCADE` — so `Rollback.sql` and later `ALTER`s can reference them by name.
