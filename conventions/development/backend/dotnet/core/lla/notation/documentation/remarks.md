# Remarks

*Last updated: 2026-09-10*

> The `<remarks>` block — the detail a one-sentence `<summary>` cannot carry.
> Optional by default; required only for the explicit consumer-contract cases below.

<a id="never-required-required"></a>

## Admission

- must omit `<remarks>` by default; the explicit contract cases below may require one.
- must not require one merely because of the type's role.

- must not add one because the component-kind seems to warrant it.
  - a `Service` or `Repository` with a sufficient summary carries none.
- must omit it when the summary already says enough.
- must not carry one on a test method — the name states the case.
  - a test has no consumer to direct.
- must not carry one on a `const` or `static readonly` — a value has no behavior to direct.
- must leave a value's whole doc to its `<summary>`.
  - not how a caller uses it, not what it means downstream.
- must not carry one where no `<summary>` exists.
  - a `<remarks>` adds to a description, it never replaces one.
- may sit beside `<inheritdoc/>`, which supplies the description from the base.

### Overrides

- must omit it on a purely declarative override — `<inheritdoc />` is the whole doc.
  - `Configure` on an EF configuration, a validator's rule constructor, a mapper's transform.
  - `ExecuteAsync` on a hosted service — the work it starts lives in the services it calls.
- must carry it beside `<inheritdoc />` when the override adds a fact the caller relies on.
  - a narrowed contract, a side effect, or a failure mode the base does not have.

### Computed members

- must carry it on a computed property whose read invokes nontrivial work or I/O.
- must not treat a field initializer as read-time evaluation; reading a stored value runs no initializer again.
- must omit it on a pure expression over the type's own fields.

---

## What it carries

Three things, and nothing else:

- **a directive** — what a consumer must do; open with an imperative.
  - `Use with …` · `Wire via …` · `For X, prefer …`
  - ✅ `For Postgres, prefer <see cref="IHasXmin"/> instead.`
- **a specification reference** — the RFC, spec, or vendor doc the shape answers to.
  - name it, don't restate it.
  - ✅ `Follows RFC 5322 for the header set.`
- **genuine complexity** — an interaction, constraint, or ordering a reader cannot infer and would get wrong.
  - ✅ `Attach before mutating — attaching after snapshots the mutation as the original.`

Everything else is cut:

- ❌ rationale for how the code is written — that is a `//` beside the code
- ❌ provider or framework behavior stated as trivia — `Maps to SqlServer's 8-byte rowversion column; EF Core
  throws DbUpdateConcurrencyException when the stored value drifts.`
- ❌ who sets the value, when, or how
- ❌ anything the `<summary>` already carries

`<remarks>` is exempt from the falsifiability test ([summary](summary.md) § *The falsifiability test*)
— a directive may describe the present.

---

## Frames — the shapes that recur

Ten frames, each answering a question the signature leaves open. `n` counts occurrences across the workspace.

- must reach for the frame whose question the reader is actually asking.
- must treat a `<remarks>` fitting none of them as rationale, which § *What it carries* removes.

| Frame | Opener | Answers | Carrier | n |
|---|---|---|---|---|
| Read-as | `Read … as` · `Treat … as` | how to interpret the value | directive | 69 |
| Invariant | `Every …` | what always holds | complexity | 36 |
| Default state | `Defaults to …` · `Off by default.` | what happens when nothing is set | complexity | 21 |
| Empty / null | `Returns … when …` · `Nothing …` | the boundary case | complexity | 20 |
| Display | `Render …` | how a UI must present it | directive | 17 |
| Wiring | `Register …` · `Call … before …` | what must be configured, and in what order | directive | 16 |
| Prohibition | `Never …` | the one thing that breaks it | directive | 12 |
| Selection | `Use … only for …` | which of several to reach for | directive | 10 |
| Re-run safety | `Idempotent — …` · `Re-run freely — …` | whether repeating is safe | complexity | 7 |
| Spec | `Follows {SPEC} …` | which standard binds the shape | spec reference | — |

**The corrective is a modifier, not a frame.** `…, never Y` / `…, not Y` attaches to *any* frame above,
naming the wrong reading the sentence displaces.

- ✅ `Read free-flow off the observed speed_90, never off the maxspeed tag.` — a Read-as carrying one.

- must open a **Prohibition** with `Never …` at the start of the sentence.
  - a mid-sentence `, never …` is the corrective — it corrects a reading, never forbids a call.
- must keep `only` in a **Selection** — `Use for idempotent calls only` selects; `Use AddResilientClient` wires.
- must not aim a `<remarks>` at the next editor — IntelliSense ships it to every consumer.
  - a maintainer fact goes in a `//` ([documentation](documentation.md) § *Where a fact belongs*).

---

## Multi-line — the same three gates [REQUIRED]

A `<remarks>` earns extra lines the way a `<summary>` does: it clears
**convention → compaction → length** (§ *What it carries*).

- must not wrap a block that has not cleared gates 1 and 2 — a multi-line `<remarks>` is evidence they were skipped.
  - readability is not a ground, and a multi-step flow is not a licence.
- must not open a line with a severity glyph — `⚠`, `❗`, `NOTE:`.
  - a `<remarks>` is already the consumer directive.
- must state a known defect the caller works around in `<remarks>`.
- must state a defect only the maintainer acts on in a `//`.
- must cap at **5 lines, tags included** — no exception, flow or otherwise.
- must carry a multi-line block as **bullets**, one claim per line.
  - never numbered steps, never running sentences.
- must compact each bullet the way a convention bullet is.
  - drop the linker, drop a subject already given.
- must not use `<list>` markup — three tags per item leaves no room under a 5-line cap.
- may use `<para>` only when the block is genuinely two paragraphs of sentences, each as compact as a bullet.
- must move a flow needing more to the module's `.standard.md` and reference it.
- must cut any step the caller cannot act on — state what a consumer must know, never the itinerary.

```csharp
/// <summary>Provides an in-memory event-saga itinerary.</summary>
/// <remarks>
/// - use a persisted state machine when execution must survive a crash
/// - declare every destination with SendsTo before building the itinerary
/// </remarks>
```
