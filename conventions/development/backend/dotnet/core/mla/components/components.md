# Components

*Last updated: 2026-08-18*

> The things that are complete on their own — declared, and immediately doing their whole job.
> Purpose — a component needs no service, no domain and no collaborator present to mean something.
> Use case — a constants holder, an enum, a settings record, a clock seam, a result, a mapper.

## The registers [REQUIRED]

Every thing here has a doc in [`mla/constructs/`](../constructs/constructs.md) too. The two split by what
they own, not by what they cover.

| Register | Owns | Lives in |
|---|---|---|
| definition | what the role is, its declaration, its suffix, where it sits | [`mla/constructs/`](../constructs/constructs.md) |
| application | which one to reach for, and with what values — members, attributes, how a host or store reads it | `mla/components/` — here |
| surface | every prop, slot, emit, option and state one thing exposes | the SDK repo's own spec, where it ships one |

- must open each doc here with a link to its construct — a reader landing on the condition still reaches
  the definition ([development conventions](../../../../../development-conventions.md) § *The layers of a thing*).
- must leave the surface register empty until the backend SDK specs its own types; a rule about an
  SDK type's options belongs to that SDK's doc, never here.
- must move a rule to `mla/constructs/` when it says **what the thing is** rather than how one is used.
- must not carry a variation in the construct — a variation is an application, so it belongs here.

`lla` / `mla` / `hla` name the **scope** a rule reaches. A register is the other cut: which half of one
thing a doc owns.

---

## The gate [REQUIRED]

- must be **self-sufficient** — declared, and doing its whole job with nothing else present.
- must run the test by demonstration — declare it in a program with nothing else, and use it.
- must fail the gate when it stays inert until a collaborator exists.
  - an `Entity` needs a store, a `Handler` a dispatcher.
- must not read simplicity as self-sufficiency — the test is whether it delivers its contract alone.
- must move to [constructs](../constructs/constructs.md) when it names a role rather than a whole thing.

| Component | Self-sufficient because |
|---|---|
| [constants](constants.md) | the value is readable the moment the class exists |
| [enums](enums.md) | the member names an option, and naming it is the whole contract |
| [extensions](extensions.md) | the method runs on the receiver, with no collaborator to inject |
| [json](json.md) | the seam holds its options and serializes with nothing else present |
| [settings](settings.md) | the record binds and validates without another type existing |
| [options](options.md) | the delegate fills the class, and its defaults hold when none runs |
| [time](time.md) | the seam answers the clock question on its own |
| [result](result.md) | the value carries its own success or failure, with nothing else present |
| [value-object](value-object.md) | the type is valid on its values alone, needing no store |
| [mapper](mapper.md) | the transform runs on its arguments, with no collaborator to inject |

---

## Adding a component [REQUIRED]

- must give each component one file, named for the role — `constants.md`, `enums.md`.
- must open with the three `##` sections in order: `Location` · `Declaration` · `Content`.
- may add further `##` sections after those three — registration, tests, a domain-specific concern — each
  answering a question the three do not.
- must give `Declaration` the sub-heads `### Type doc` · `### Construct` · `### Type name`.
  - skip any it has no rule for.
- must state the folder **name** only, never its layer
  ([domain structuring](../../../shapes/service/architecture/clean/domain-structuring.md)).
- must cite [one type, one file](../mla.md) rather than restate it — state a deviation only.
- must follow [writing a doc in this scope](../mla.md) for the shared doc rules.

A component keeps `## Content` because its members **are** its contract.
A [construct](../constructs/constructs.md) drops it — the shape of a role belongs to the domain using it.
