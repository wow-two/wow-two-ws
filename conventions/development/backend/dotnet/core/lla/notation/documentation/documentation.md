# Documentation

*Last updated: 2026-09-10*

> XML-doc index — the cross-cutting format and the per-block table; each block's rules live in `documentation/`.

## XML doc format

- **One-liner by default** — `<summary>`, `<remarks>` content is a compact single line
- **Inline tags** — opening and closing tags on the same line as the content
- **`and`, not `+`** — in prose (summaries, remarks, `//`) `+` reads as a code operator: `PG and SQLite`

```csharp
// ✅ Correct — compact one-liner, tags inline
/// <summary>Defines a handler for extracting phone numbers from a listing via HTTP.</summary>
/// <remarks>Single responsibility — no image extraction, no browser dependency.</remarks>

// ❌ Wrong — multi-line summary for content that fits on one line
/// <summary>
/// Defines an extraction handler for browser-based data.
/// Each channel implements its own logic.
/// </summary>
```

---

## Per-block conventions

Each XML doc block has its own rules — start here:

- `<summary>` → [summary](summary.md) — **canonical**: starters, falsifiability test, tone, properties, constants
- `<remarks>` → [remarks](remarks.md) — optional by default, required only for explicit consumer-contract cases
- `<param>` → [params](params.md) — compact noun-phrase per parameter
- `<typeparam>` → [type params](typeparams.md) — skipped for a conventional name, carried for a domain-meaningful
- `<returns>` → [returns](returns.md) — required unless the return is `void` / `Task` / `ValueTask`
- `//` inline → [inline](inline.md) — the maintainer-facing comment inside a body
- `<exception>` → [exceptions](exceptions.md) — only exceptions the method throws itself

---

## Where a fact belongs [REQUIRED]

Most bad doc comments are true sentences filed in the wrong place. Route by **audience**, and the tag follows.

- what the member guarantees to a caller → consumer → `<summary>`
- what a caller must do to use it correctly → consumer → `<remarks>`, imperative
- why the code is written this way; a format's or a literal's provenance → maintainer → `//` beside the code
- a policy binding many types (naming, layering) → team → a convention doc in `conventions/`, never a member's doc

- **`<summary>` / `<remarks>` ship** — to the XML doc and IntelliSense; a maintainer note there hits every consumer.
- **A member cannot know how it is used** — claims of caller count, uniqueness or authority go in a convention.

---

## Declared fields only [REQUIRED]

A component doc names the doc fields its types carry, one sub-heading each. **A field the component does not declare is
forbidden on that component** — the omission is the ban, so no doc has to list what it excludes.

- must add a field only by declaring it in the component doc, with the rule it obeys there.
- must justify the addition in that sub-heading's first line — what the field carries that the declared ones cannot.
- must not read a missing field as an oversight; a component with no `<remarks>` sub-heading forbids `<remarks>`.

---

## Name the referent [REQUIRED]

A member name says *what* a value is, never *whose* it is: `Name` on a `CodeCreateCommand` could be the code's,
its author's, or its owner's. The referent is named exactly when it is **not** the enclosing type's own subject, so a
domain noun is a signal and its absence says *this belongs to the type you are reading*.

- must name the referent when the value is not the enclosing type's own — a related entity, author, owner or target:
  `Gets the order of the rule that matched the scan.`
- must **omit** it when the value is the type's own — `ChannelEntity.Slug` takes `Gets or sets the kebab-case slug.`
- must not add *of the channel* there — it restates the declaration and drains the signal where the noun matters.
- must read the **subject**, not the type name — a `CodeDto` *is* the code, so `Name` omits;
  a `CodeCreateCommand` is a command *about* a code, so `Name` names the code.
- must apply in a `<summary>`, a `<param>`, and a `<returns>` alike.
- must not stretch it into who sets the value, when, or how — that is § *Where a fact belongs*.

The failure it names is an **unanchored value**: a doc that describes a value and leaves its owner to inference.

---

## Comment anti-patterns [REQUIRED]

Named failure modes, checked at **gate 1**. The name is the review vocabulary — say "nonlocal information",
not "this feels off". Names marked *(Clean Code)* are Robert C. Martin's, ch. 4.

### Nonlocal information *(Clean Code)*

A local comment asserting a system-wide fact — the claim rots the moment a second caller appears.

```csharp
// ❌ the member cannot know how many places read it
/// <summary>Gets the storage table name — the single source of truth for hand-written SQL.</summary>

// ✅ states what it offers; the "only place" policy lives in a convention
/// <summary>Gets the storage table name for the code entity.</summary>
```

Same failure: a **delivery channel** a value object does not own. It states what it *holds*, never how it travels.

```csharp
// ❌ binds the type to one channel — a click-to-copy or share path makes it false
/// <summary>Represents a phone number dialed on scan.</summary>

// ✅ the value, and the capability it carries
/// <summary>Represents a telephone number to dial.</summary>
```

**Serialization is the same failure.** A value object's summary states what it holds, never how it encodes —
a second encoder makes the claim false. The fact is local on `Encode()` or its extensions class, nonlocal on the type.

```csharp
// ❌ nonlocal information — the encoder decides the scheme, not the value
/// <summary>Represents free-form text belonging to no scheme.</summary>

// ✅ the value
/// <summary>Represents free-form text.</summary>
```

### Too much information *(Clean Code)*

Spec provenance, standards history, format archaeology — irrelevant to whoever calls it.

```csharp
// ❌ archaeology — what the spec says, restated
/// <remarks>The <c>mailto:</c> scheme is registered (RFC 6068), and what follows the <c>?</c> is not an HTTP query.</remarks>

// ✅ name the spec, do not restate it
/// <remarks>Follows RFC 6068.</remarks>

// ✅ provenance is a maintainer fact — move it to a `//` beside the literal it explains, or drop it
```

**Conformance is not provenance.** *"Conforms to RFC 6068"* is a contract, so it ships — as a **spec reference in
`<remarks>`** ([remarks](remarks.md) § *What it carries*), naming the spec and restating none of it. The `<summary>`
keeps its purpose shape and never absorbs the citation; provenance (*why the literals look this way*) goes in a `//`.

```csharp
// ❌ restates the spec, and repeats the scheme RFC 6068 already names
/// <summary>Extends <see cref="EmailContentValueObject"/> to the RFC 6068 <c>mailto:</c> payload.</summary>

// ✅ purpose in the summary, the spec named once in <remarks>
/// <summary>Extends <see cref="EmailContentValueObject"/> for payload encoding.</summary>
/// <remarks>Follows RFC 6068.</remarks>
```

### Over-specification

Documenting internals the contract does not guarantee — changing what the method wires breaks its documentation.

```csharp
// ❌ enumerates what the call happens to register today
/// <summary>Adds persistence — registers the DbContext, the interceptors, the migrator, and the health check.</summary>

// ✅ the guarantee, not the wiring
/// <summary>Adds Postgres persistence to the container.</summary>
```

**Cutting a failing block is not relocating its sentence.** A fact that fails gate 1 in `<remarks>` usually fails in
`<summary>` too — re-check it here after the move, or the defect only changes tag.

### Redundant comment *(Clean Code)*

Restates the member name, so it costs a line and pays nothing.

```csharp
// ❌ the predicate is empty — the name already said "slug"
/// <summary>Gets or sets the slug.</summary>
public required string Slug { get; set; }

// ✅ the starter stays; the predicate carries the entity and the shape
/// <summary>Gets or sets the kebab-case slug.</summary>
```

The defect is the empty predicate, never the starter — a property summary keeps its `Gets` / `Gets or sets`
([summary](summary.md) § *Properties on entities + DTOs*).
Say what the name cannot — units, range, what null means; name a related owner under § *Name the referent*.
Not who sets it, when, or how.

### Mandated comment *(Clean Code)*

A doc written because a rule demands one, carrying nothing the declaration lacks — an empty `<summary>` on a
self-evident private method, a `<returns>` restating the return type. **`<param>` is exempt**: [params](params.md)
requires one per parameter, because a partial set reads as an omission.

### Inobvious connection *(Clean Code)*

A comment referring to something the reader cannot locate — "the sentinel", "as described above", "the usual flow".
Name the identifier with `<see cref="..."/>` or cut the sentence.

### Circumstance as definition

A `<summary>` describing today's arrangement rather than what the type is — it fails the **falsifiability test** in
[summary](summary.md), which names the shapes it takes.

### Wrapped instead of cut

Hitting the 120-char limit and wrapping to satisfy it, without running gates 1 and 2. A multi-line block is
evidence the earlier gates were skipped until proven otherwise.

---

## Cross-references [REQUIRED]

A `<see cref>` is a **navigation aid**, not decoration — it earns its place when the reader must read the referenced
type to use this one correctly. It costs 20–60 chars of the 120-char budget, so a decorative one displaces a fact.

**Use a cref when the type is off-screen and load-bearing:**

- a sibling to prefer or a replacement — `For Postgres, prefer <see cref="IHasXmin"/>.`
- a registry, options bag, or contract the reader must keep in lockstep —
  `Keep <see cref="Subtypes"/> in lockstep with the frontend union.`
- the type a member delegates to, when the delegation is the point

**Do not use a cref when it links to something already in view:**

- a type in this member's own signature — `Serialize(IReadOnlyList<CodeRuleValueObject>)` already shows it
- the declaring type, inside its own members — the file is the context
- a type named only as a noun in prose — drop the tag, keep the word
- every type mentioned, out of completeness — the mandated-comment anti-pattern wearing a link

**Pick the right tag:**

- `<see cref="X"/>` — a type or member that exists; the compiler checks it (`CS1574`), so it is rename-safe.
- `<c>x</c>` — a literal that is **not** a type: a wire token, column name, header, JSON key, shell value
  — `<c>content_json</c>`, `<c>Stripe-Signature</c>`, `<c>"vCard"</c>`.
- `<paramref name="x"/>` / `<typeparamref name="T"/>` — always correct; they bind to the signature, not away from it.

Never write a type name as bare prose when a cref would link it **and** the link earns its place above. Otherwise use
the plain noun — *"the rule set"*, not `<see cref="CodeRuleSet"/>`.

---

## Terminology

- **Collection** — say "collection" in `<summary>` for any grouping type (`List<T>`, `T[]`, `Dictionary<K,V>`)
- **The {entity}** — name the owning entity in prose (`the channel`); the type name goes in `<see cref>`.

---

## Neighbours

- [models.md](../../constructs/constructs.md) — record style + general property rules
- [entities.md](../../../mla/constructs/data/entity.md) — entity-specific doc rules
- [enums](../../../mla/components/enums.md) — enum value documentation
- [services.md](../../../mla/constructs/behavior/service.md) — service / client / factory naming
- [mediator](../../../mla/domains/messaging/mediator/mediator.md) — query/command/handler naming + docs
