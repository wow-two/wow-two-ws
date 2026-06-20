# Exceptions

*Last updated: 2026-06-17*

> The `<exception>` block — document only the exceptions a method throws itself, not propagated ones.

## Exceptions

- A method documents the exceptions **it itself throws** with `/// <exception cref="…">{trigger}</exception>` — **not** exceptions propagated from callees (inner / nested).
  - ✅ `<exception cref="MigrationDriftException">An applied migration's checksum no longer matches its source.</exception>`
