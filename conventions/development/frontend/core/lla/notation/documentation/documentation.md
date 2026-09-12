# Documentation

*Last updated: 2026-09-10*

> What a JSDoc block says and how long it may run — every public export takes one.
> Purpose — a fixed starter vocabulary, so every type's doc opens the same way.

## Format [REQUIRED]

- must write a doc as a one-liner — `/** … */` on a single line.
- may exceed one line only when every condition below holds; failing any one, collapse it.

### The multi-line exception

1. the entity is **exported** — an `@internal` never earns more than one line.
2. every extra line states a caller obligation absent from the signature — precondition, failure, ordering, disposal.
3. no line compares to another implementation, justifies the pattern, or explains *why this shape*.
4. **≤5 lines**; past that it is a doc page, not a comment.
5. no usage example — a snippet goes stale with nothing to catch it; it belongs in a test or a story.

**The test:** strike every line whose removal costs the caller nothing — one survivor earns the block, none
collapses it. Length is not the test; a 200-character restatement fails condition 2 while looking substantial.

```typescript
// ❌ what the code already says, and how it used to say it
/* Chained after the consumer's own click and skipped when they called `preventDefault()`. */

// ✅ one line, the role
/* Runs after the consumer's handler; a prevented default skips it. */

// ✅ earns three lines — each is a caller obligation absent from the signature
/**
 * Opens the channel and returns it. Call `close()` before the page unloads.
 * Throws `DOMException` when the origin is cross-site.
 * Messages sent before `ready` resolves are dropped, not queued.
 */
```

---

## Verb starters

| Target | Verb | Example |
|---|---|---|
| Enum | `Defines` | `/** Defines the QR data-module body shape. */` |
| Enum member | `Refers to` | `/** Refers to a plain square module. */` |
| Displays Record (`{Enum}Displays`) | `Maps` | `/** Maps each barcode format to its display. */` |
| Interface — shape / contract | `Defines` | `/** Defines the editable fields for the edit form. */` |
| Interface — data holder | `Represents` | `/** Represents a domain listing with resolved enums. */` |
| Props interface | `Defines` | `/** Defines props for the author contact strip. */` |
| Prop member — value / input | `The …` | `/** The current foreground gradient, or null. */` |
| Prop member — callback | `Emits …` | `/** Emits the next gradient. */` (pure event → `Fires when …`) |
| Component fn | `Renders` | `/** Renders the author contact strip. */` |
| Utility fn | 3rd-person verb | `/** Resolves a raw API string to a TS enum value. */` |
| Hook | `Manages` | `/** Manages the supply listings fetch lifecycle. */` |
| Context-accessor hook | `Provides access to` | `/** Provides access to auth state from AuthContext. */` |
| Extension object | `Extends` | `/** Extends `Person` for display formatting. */` |
| Extension method | 3rd-person verb | `/** Extracts up to 2 uppercase initials. */` |
| Internal constant | `@internal {desc}` | `/** @internal Whitespace splitter. */` |

- must reserve `Provides` for an object with behaviour of its own — `Provides access to` unwraps a context.
- must not write `Gets or sets` on a prop member — a prop is unidirectional, split across `value` and `onChange`.
- must not write `Holds` / `Provides` on one either — they imply storage the component does not own.

---

## Member docs

- must document a **pure-UI** props interface member by member — no backend contract exists to lean on.
- must omit member docs on a **backend-mirrored** props interface — the backend declares the semantics.
- may leave member docs off a domain interface or DTO, grouping fields with `// ── Section ──` bands.

---

## Name the referent

A doc says *what* a value is, never *whose* — the referent appears only when it is not the type's own subject.

- must name the referent when the value belongs elsewhere — a related entity, author, owner or target.
- must omit it when the value is the type's own — `Channel.slug` takes `/** The kebab-case slug. */`.
- must not add *of the channel* there — the absence of a domain noun is itself the signal.
- must read the **subject**, not the type name — a `CodeDto` *is* the code, a `CodeCreateCommand` is about one.
- must hold in a `@param` and a `@returns` alike.

---

## Scope

A doc identifies the entity and states caller obligations that its signature cannot express.

- must run [the falsifiability test](falsifiability.md) on every doc written or touched.
- must not say why this shape rather than another; pattern choice is a convention's job, not an entity's.
- must not restate a rule from `conventions/` at a use site — the copy drifts the moment the rule changes.
- must retain entity-specific lifetime, ownership, cancellation and failure obligations even when a convention informs them.
- must not point at the convention either (`// see vue-sfc.md § …`) — a reader looks it up once.
- may keep a one-clause because when it changes what the reader does (`// second pass — the ref is unset`).
- **The test:** a line reading identically on every entity following the rule belongs in the rule, not here.

---

## Comments

A `//` block or inline comment states a **role** in one line — never rationale, history, or a design essay.

- must keep a file-top or block comment to one line naming what the code is or does.
- must not narrate migrations, drift risks, version notes or trade-offs in source — those go in the commit.
- must keep an inline comment a short role label (`{/* type picker */}`), not a sentence.
- must check a written doc against [the anti-pattern catalogue](anti-patterns.md) — the eight names are the
  review vocabulary.

---

## Neighbours

- [the C# starter table](../../../../../backend/dotnet/core/lla/notation/documentation/documentation.md) — the peer
- [constructs](../../../mla/constructs/constructs.md) — the component-level additions to these verbs
- [enums](../../components/enums.md) · [extensions](../../components/extensions.md) — the forms these verbs open
- [style](../style/style.md) — the `// ── Section ──` field bands
