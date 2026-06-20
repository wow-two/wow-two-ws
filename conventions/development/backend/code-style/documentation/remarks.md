# Remarks

*Last updated: 2026-06-17*

> The `<remarks>` block — directive, telling the consumer what to do, plus the multi-line exception for numbered flows.

## Remarks — directive, not explanatory

`<remarks>` tells the consumer **what to do**, not how the SDK works internally.

- Open with an imperative: `Use with …`, `Wire via …`, `For X, prefer …`, `Populate … at construction.`
- Cut tech-facts and rationale — performance reasoning, compiler-quirk explanations, provider/EF behavior, "throws X on drift", who-reads-the-value.
  - ✅ `For Postgres, prefer <see cref="IHasXmin"/> instead.`
  - ❌ `Maps to SqlServer's 8-byte rowversion column; EF Core throws DbUpdateConcurrencyException when the stored value drifts from the original.`
- Omit `<remarks>` entirely when the summary already says enough.

## Multi-line for numbered flow

- **Exception** — `<remarks>` with numbered flow steps (3+ steps) may use multi-line for readability.

```csharp
// ✅ OK — multi-line remarks for numbered flow (exception)
/// <summary>Provides channel and pipeline seeding on application startup.</summary>
/// <remarks>
/// Seed flow:
///   1. Read channels from seed file
///   2. Upsert channels + sources via EF Core
///   3. Insert missing pipeline rows with code defaults
/// </remarks>
```
