# Core

*Last updated: 2026-09-10*

> What holds in every .NET deliverable we build — the language, the roles we define, the things complete on
> their own, and the capabilities a codebase reaches for.
> Purpose — a rule that does not change when the deliverable changes belongs here, once.
> Use case — naming a type, writing a doc comment, picking a role, or reaching for a capability.

## The three scopes

| Scope | Answers | Lead |
|---|---|---|
| [lla](lla/lla.md) | one symbol | the C# form, and how that form is written end to end |
| [mla](mla/mla.md) | one codebase | roles, self-contained components, capabilities |
| [hla](hla/hla.md) | between our own services | contracts requiring both ends to comply |

- must place a rule here when it holds whatever is being built — a service, a library, the SDK, a CLI.
- must place it under [shapes](../shapes/shapes.md) when it changes with the deliverable.
- must leave project placement, build and host composition to the owning shape.

---

## Routing a rule

**Routing.** A kind of type you declare → `mla/constructs/{kind}.md`. A thing complete on its own →
`mla/components/`. How any symbol is written → `lla/`. A concrete technology or capability →
`mla/domains/{domain}/`. A rule spanning services we both own → `hla/`.
Where a folder is **created in the project tree**, how a service builds, starts and answers →
[shapes](../shapes/shapes.md), never `core/`.

**The test between `mla/` and `hla/`:** do we own both ends? A third party is adapted in `mla/`, never contracted in `hla/`.
**Definition and application.** The C# form is in [constructs](lla/constructs/constructs.md).
Our role's definition is in `mla/constructs/`, including roles that stand alone.
Its application is in `mla/components/` when self-contained, or `mla/domains/` when it needs collaborators.
A ban stays with the obligation it qualifies.

**The test between baseline and a domain:** would the rule survive if the feature were deleted? Yes → baseline. No → the domain that owns it.

---

## What each scope owns

### `lla/` — one symbol
Every rule that holds for **any** symbol, whatever kind it is: its name, its doc blocks, its member bodies, its file layout,
and the language constructs banned outright. A rule naming a *kind* of type is not `lla/`; a rule naming a technology is not `lla/`.

### `mla/` — one codebase

- must place role definitions in `constructs/`, self-contained application rules in `components/`,
  and capability-specific application rules in `domains/`.
- must file a third-party integration under the domain that consumes it.
- must keep SDK usage obligations here and instance API surfaces beside the SDK source.
- must leave architectural placement to [shapes](../shapes/shapes.md).

### `hla/` — between our own services
Named ahead of its contents on purpose: without it, the first gateway or gRPC rule lands in `shapes/service/platform/` and becomes a
single-service default every later service inherits by accident.

---
