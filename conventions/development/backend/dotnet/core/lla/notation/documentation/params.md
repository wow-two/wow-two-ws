# Params

*Last updated: 2026-09-13*

> The `<param>` block — one per parameter, always, describing its role in this method's process.

## Every parameter, every time [REQUIRED]

- must document **every** parameter of a documented method — the set is complete or the doc is wrong.
- **consistency is the reason** — a per-parameter test leaves a reader unable to tell an omission from a decision.
- must not document the parameters of a constructor injecting only collaborators.
- must omit `<summary>` on that collaborator-only constructor; this is an explicit constructor exemption under [documentation](documentation.md#inherited-fields-and-explicit-overrides-required), not an omission-based ban.
- must document every parameter of a constructor taking values, and of a mixed one.
- `<param>` is exempt from *Mandated comment* ([documentation](documentation.md) § *Comment anti-patterns*).

---

## What it carries

A method is one process. A `<param>` says what the parameter **is to that process**.

- must write a compact noun phrase — no filler, no leading type restatement.
- must not restate the type — the signature carries it.
- must name the referent ([documentation](documentation.md) § *Name the referent*).
  - ✅ `the display name of the code` · ❌ `the display name`
- must describe the role in **this** method, never in a method this one calls — a repeat rots when the callee changes.
- should name the constraint the type cannot express — a 1-based index, a required non-empty.

```csharp
// ✅ every parameter, each saying its role here
/// <param name="lines">The document built so far.</param>
/// <param name="prefix">The vCard property prefix to write.</param>
/// <param name="value">The value to escape and append.</param>
private static void AppendProperty(List<string> lines, string prefix, string? value)

// ✅ short names still get their line
/// <param name="id">The code to load.</param>
/// <param name="ct">The cancellation token.</param>
public Task<CodeEntity?> GetByIdAsync(Guid id, CancellationToken ct);

// ❌ restates the type, adds nothing
/// <param name="appliedBy">A string that is the value used for the appliedBy column.</param>

// ✅ says its role in the process
/// <param name="appliedBy">The host stamp recorded on each applied row.</param>
```
