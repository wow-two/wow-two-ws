# Inline comments

*Last updated: 2026-08-16*

> The `//` comment inside a method body — the only doc a maintainer reads and a consumer never sees.
> Purpose — carry the fact a shipped block must not, so `<summary>` and `<remarks>` stay consumer-facing.
> Use case — reach here when the reason lives in the code, not in the contract.

## What it carries

- must explain a non-trivial step in one imperative line — present-tense verb, essentials only.
- must skip the comment when the code is self-evident.
- must not run a `//` or `/* */` past one line — the earned-multi-line clause covers `<summary>` / `<remarks>` only.
- must move a note needing a second line to the commit, the tracking issue, or the module's `.standard.md`.
- must not draw a section banner in `//` — `// ── Columns ──` groups members, and grouping is `#region`'s
  job → [constructs](../../constructs/constructs.md) § *Behavior components*.

```csharp
// Acquire the advisory lock so only one host migrates at a time.
await dialect.AcquireLockAsync(connection, ct);

// Fetch the applied set, then diff against the source.
var applied = await history.GetAppliedAsync(connection, ct);
```

- ❌ `// This loop iterates over the directories and for each one it checks whether…` (multi-line / restates code)

---

## Exclusions

- Internal types and members — warnings are suppressed; a brief one-liner only when context isn't obvious
- Auto-generated code — skip
- Test classes / methods — name carries the meaning
- **`<example>` tags** — don't use them; they restate the obvious and go stale.
- **Change / refactor narration** — `// moved from X`, `// renamed` — comment intent, never edit history.
- **Defence against a shape that was rejected** — `// not a factory the SDK calls`, `// an instance rather than a
  static because…`. A shape that did not fit leaves no trace: the reader meets what is, not the argument that got
  here. State the behaviour positively, or say nothing.
- **Rationale / justification essays** — `// stays in the handler because it's a business rule`.
  - a genuinely non-obvious *why* is **one** terse line, never a note re-explaining the code.

---

## Neighbours

- [documentation](documentation.md) — the routing table that sends a fact here
- [style](../style/style.md) — how the line the comment sits above is laid out
