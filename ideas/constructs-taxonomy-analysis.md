# Constructs taxonomy — analysis

*Last updated: 2026-08-21*

> Why the keep-list cannot answer "what exactly is a `Renderer`", and the axes that would let it.
> Purpose — the list grew to 37 rows carrying 3 discriminators; every new role widens it further.
> Use case — read before adding a suffix, folding one, or renaming a type into an existing role.

## The defect

Measured against `conventions/development/backend/dotnet/core/mla/constructs/constructs.md`:

| | Count |
|---|---|
| keep-list rows | 37 |
| rows carrying a discriminator section | 3 |
| rows defined by a one-line gloss only | 34 |

The three that work are `Mapper` vs `Registry`, `Client` vs `Broker`, `Settings` vs `Options`. Each states a
**question** whose answer picks the side — who owns the mapping data, whose vocabulary the surface exposes,
where the value comes from. The other 34 rows state what the role *is* and never what separates it from its
neighbour, so two readers place the same type differently and both cite the doc.

The symptom is already in the SDK: one suffix sits on both sides of the collaborator line.

| Type | Injects | Suffix |
|---|---|---|
| `SvgRenderer` | nothing | `Renderer` |
| `QrCodeRenderer` | `IQrMatrixGenerator` · `ISvgRasterizer` | `Renderer` |
| leaf caption parsers (4) | nothing | `Parser` |
| `CompositeCaptionParser` | 4 parsers | `Parser` |

A reader cannot tell from the name whether the type is a pure function or a composition.

---

## The axes

Five questions, asked in order. The first that fires places the type, and each has a mechanical answer.

| # | Question | Fires → |
|---|---|---|
| 1 | does it hold values rather than do work? | the data roles |
| 2 | does it leave the process? | `Client` (their vocabulary) · `Broker` (ours) |
| 3 | does it read or write rows? | `Repository` |
| 4 | does it stitch several output kinds together? | `Service`, or a named composed role |
| 5 | otherwise — what does it output? | a pure role, named for the output |

Axis 4 is what the current doc is missing, and it is what answers *"can it be a rendering service then?"*

- must keep the output suffix when every collaborator **feeds one output** — `CodeRenderer` over two
  renderers is still a renderer, and `CompositeCaptionParser` over four parsers is still a parser.
- must name it a `Service` when the type **stitches different output kinds** — `QrCodeRenderer` takes a
  matrix from a `Generator` and pixels from a `Rasterizer`, which is orchestration wearing a transform's name.

---

## Settled — operation · step · flow

Agreed 2026-08-21. Three words, and a type is exactly one of them.

| Word | Contract | Injected by | Named |
|---|---|---|---|
| **operation** | names no domain type | any flow | a role suffix — `Mapper` · `Validator` · `Serializer` · `Hasher` |
| **step** | names a domain type | one flow | for its stage, internal to that flow |
| **flow** | composes steps and operations | — | `Service` |

- must extract a step into an operation on the **second** consumer, never the first — a contract with one
  caller is decoration, and genericity only makes a step eligible.
- must read the vocabulary as recursive — a flow whose steps are themselves flows is one level up, and
  that level is the only thing an orchestrator names.
- the same verb can be both: a generic `Hasher` over `byte[]` is an operation, a hash over one payload
  shape is a step. The contract decides, and both existing is not a conflict.

Measured on the SDK when the words were agreed: `IMessageSerializer` is injected by 10 flows,
`ISvgRasterizer` · `IQrMatrixGenerator` · `SvgRenderer` by exactly 1, and `ICodeRenderer` ·
`ITabularExporter` · `ICaptionParser` by 0, being their flow's entry point.

---

## Settled — invertibility names the wire band

Agreed 2026-08-21. A transform is placed by whether its output can rebuild its input.

- **invertible**, correctness fixed by an external spec → the wire band: `Serializer` · `Parser` ·
  `Encoder` · `Decoder`. Each ships its inverse and is tested round-trip.
- **one-way**, correctness decided by taste or a culture → presentation. No inverse exists to test, and
  information is dropped on purpose.

---

## Settled — the domain shape

Agreed 2026-08-21, product-side. The role vocabulary does not need closing if it never reaches the
domain root; nesting caps the root instead.

```
{Domain}/
  Commands/ · Queries/ · Events/     intake — carriers of what arrives from outside
  Models/                            the shapes the domain passes around
  Constants/                         the values the domain already knows
  FoundationServices/                Mappers/ · Validators/ · Serializers/ · Encoders/ ·
                                     Publishers/ · Extensions/
  ProcessingServices/                one flow each
  OrchestrationServices/             a flow of flows
```

**Why `Constants/` is not an app message.** `Models/` and `Constants/` are kin — both are data the domain
holds and passes. A command, query or event is a *carrier of what arrives from outside*; a constant is never
input, it is what the domain already knows. That is the line, and it keeps constants beside models rather
than beside messages.

**Why the three service folders sit at the root.** A parent folder over them has no honest name: `Services/`
repeats what each child already says, `Behavior/` and `Logic/` describe nothing, and `Operations/` collides
with the word *operation* this doc has already spent. A folder that cannot be named is not a folder, so the
three stand at the root and `Extensions/` files inside `FoundationServices/` with no parent problem left.

- the root holds 7 entries in every domain, known before a single file exists
- a new role kind adds a folder under `FoundationServices/`, never at the root
- `Services/` holds only folders — no loose file beside them, matching
  [conventions](../conventions/conventions.md) § *Authoring a convention*
- aliases name both the component and its folder: `Mappers/OrderMapper.cs`

A command validator names a domain type, so by the operation test it is a step rather than an operation —
but that test governs whether a thing earns a **role name**, not which layer it belongs to. A validator is
a stateless single act, registered and swapped as a group, so it is foundation and files under
`FoundationServices/Validators/`.

---

## Settled — the product shape, both layers

Agreed 2026-08-21. One rule throughout: **a component sits in its role folder under its subdomain, in the
layer that owns its kind.** No use-case folders, no thresholds, no exceptions.

```
Application/{Domain}/{Subdomain}/
  UseCases/                          Commands/ · Queries/ · Events/
  Models/ · Constants/               the shapes and the values
  Services/ · Repositories/          interfaces only

Infrastructure/{Domain}/{Subdomain}/
  UseCases/                          CommandHandlers/ · QueryHandlers/ · EventHandlers/
  FoundationServices/                Validators/ · Mappers/ · Serializers/ · Parsers/ ·
                                     Encoders/ · Decoders/ · Renderers/ · Formatters/ ·
                                     Exporters/ · Publishers/ · Generators/ · Extensions/
  ProcessingServices/                one flow each
  OrchestrationServices/             a flow of flows
  Settings/                          bound configuration is not contract
  Brokers/ · Adapters/ · Integrations/{Provider}/

Persistence/{Domain}/
  Repositories/                      the implementations
  DataContexts/ · Configurations/ · Migrations/
```

- a use case's files scatter across folders on purpose — the folder answers *what kind is this*, and the
  name answers *which use case*, so neither has to answer both.
- the shape is known before a single file exists, which is what a scaffold and an agent both need.

---

## Pure roles, by output

Axis 5. Every row here is a total function of its arguments — no collaborators, no I/O, no state.

| Output | Role | Discriminator |
|---|---|---|
| another shape of ours | `Mapper` | the output is consumed by our code, not shipped |
| a representation to display or ship | `Renderer` | a caller writes the result somewhere, unchanged |
| pixels from vectors | `Rasterizer` | `Renderer`'s one named special case |
| a shape from untrusted text | `Parser` | the input can be malformed, so the call can fail |
| both directions on one format | `Serializer` | it owns the format's options and its version |
| a file a user downloads | `Exporter` | the output carries a content type and a filename |
| human-readable text | `Formatter` | culture decides the result |
| a value derived from nothing but inputs | `Generator` | no input shape is transformed, one is produced |
| a cryptographic result | `Cipher` · `Hasher` · `Issuer` · `Authenticator` | correctness is fixed by a spec, not by us |

`Parser` and `Renderer` are inverses; that is why folding them into one suffix loses information.

---

## Composed roles

Axis 4. Each holds collaborators, configuration, or both.

| Role | Discriminator against `Service` |
|---|---|
| `Service` | the default — stitches output kinds, and nothing narrower applies |
| `Handler` | bound to exactly one dispatched message |
| `Controller` | the HTTP surface; it dispatches and returns, never decides |
| `BackgroundService` | the host runs it, not a request |
| `Validator` | returns rule failures as its success payload |
| `Policy` | decides whether, when, or how often another operation runs |
| `Factory` | produces instances, per key or per request |
| `Registry` | callers register into it, and it owns whether the set is whole |
| `Tracker` | live status pushed in by many producers, persisted nowhere |
| `Adapter` | a foreign type fitted to a contract we declared |
| `Builder` | stepwise construction, closing on `Build()` |
| `Pipeline` · `PipelineStep` | an ordered flow, and one step of it |

---

## Data roles

Axis 1. None of these carry behavior.

| Role | Discriminator |
|---|---|
| `Entity` | owns a row's identity |
| `ValueObject` | identity is the values, stored inside a row |
| `Dto` | a projection onto the wire |
| `Model` | our own shape of a thing, inside a carrier |
| `ApiRequest` · `ApiResponse` | the edge body, and the success envelope |
| `Result` | the carrier — a typed success or an `AppError` |
| `Settings` · `Options` | configuration, split by origin |
| `Constants` | `const` and `static readonly` values |
| `Spec` | a declarative input a renderer consumes |

---

## Against the pattern buckets

`patterns/patterns.md` already does what the keep-list does not: four buckets (Creational · Structural ·
Behavioral · Enterprise), every row carrying a verdict from a closed set (`use` · `folded` · `owned` ·
`banned` · `open`), and a link to the doc that owns it.

- must give the keep-list the same shape — a bucket per axis, and a discriminator per row.
- the patterns table already contradicts the code in one place: Composite is `banned`
  ("a `Pipeline` and its ordered steps, never a uniform tree"), and `CompositeCaptionParser` is one.

---

## Open

- **iteration 17 needs a re-read.** Per-use-case grouping was agreed before the layer split moved handlers
  to `Infrastructure`. Measured in forever-pin, only 2 of 20 validators pair with a message; the other 18 are
  domain validators, so the grouping would move two files and split the validator population in two.
- the SDK has no layer split, so it files the same role folders by domain with no `Application` /
  `Infrastructure` pair above them.

- **where the three service folders live.** `FoundationServices/` · `ProcessingServices/` ·
  `OrchestrationServices/` are implementation folders, so they belong in `Infrastructure`, with their
  interfaces under `Application/{Domain}/Services/`. The SDK has no layer split and files them by domain.
- **`Mappers/` sits in two places.** `architecture.md:84` files it under `Infrastructure`, while this doc
  files it under a domain's `FoundationServices/`.
- `Json` names a format rather than a role; `Serializer` covers what it did.
- `Middleware` · `Filter` · `Interceptor` are exempt from the gate, which is a fourth verdict the keep-list
  has no vocabulary for — the patterns table would call it `owned`.
- `Spec` and `Model` both name "our own shape"; the discriminator between them is unwritten.
- `Configuration` (an EF `IEntityTypeConfiguration<T>`) collides with the configuration domain by name.

---

## Iterations

Every turn that moved the design, newest last. A row is what changed and what made it change.

| # | Date | Moved | Because |
|---|---|---|---|
| 1 | 2026-08-21 | keep-list audited — 31 roles, 3 discriminators | `Renderer` vs `Service` had no test a reader could apply |
| 2 | 2026-08-21 | five ordered axes drafted | a role needs a question, not a gloss |
| 3 | 2026-08-21 | `Renderer` refuted as a sibling of `Service` | one suffix already sat on both sides of the collaborator line |
| 4 | 2026-08-21 | **operation · step · flow** settled | injection counts split the vocabulary cleanly — 10 vs 1 vs 0 |
| 5 | 2026-08-21 | invertibility named the wire band | it is what separates encoder from formatter |
| 6 | 2026-08-21 | subject-counting refuted for orchestration | sign-in touches three subjects and is still one flow |
| 7 | 2026-08-21 | orchestration redefined recursively | a flow's parts are steps; an orchestrator's parts are flows |
| 8 | 2026-08-21 | `Mapper` purity refuted | any mapping can fail, so `Result` applies — opens `N69` |
| 9 | 2026-08-21 | alias model rejected as a separate idea | a name always used is the name, not an alias |
| 10 | 2026-08-21 | folder threshold refuted | a role folder is a slot declaration, so it exists from file one |
| 11 | 2026-08-21 | nesting caps the root, not the vocabulary | a new role kind adds a folder below, never at the root |
| 12 | 2026-08-21 | three service layers + three folders settled | foundation varies, processing injects, orchestration composes |
| 13 | 2026-08-21 | `Extensions/` moved into `FoundationServices/` | an extension is a foundation operation in extension syntax |
| 14 | 2026-08-21 | `Validators/` returned to `FoundationServices/` | the operation test governs naming, not layering |
| 15 | 2026-08-21 | parent `Services/` folder dropped | no honest name exists for it, and each child already says it |
| 16 | 2026-08-21 | handler refuted as a processing service | a handler dispatches, the way a controller does for HTTP |
| 17 | 2026-08-21 | message + validator + handler grouped per use case | they change together, and the message is the domain's door |
| 18 | 2026-08-21 | two validator kinds separated | a message validator is 1:1 with its message; a domain validator is reused |
| 19 | 2026-08-21 | `*Handlers/` moved to `Infrastructure` in `architecture.md` | forever-pin keeps 11 of 11 handlers there; the doc said `Application` |
| 20 | 2026-08-21 | the layer split is interface vs implementation | `Application/*/Services/` holds 6 interfaces and 0 classes |
| 21 | 2026-08-21 | validators stay in `Application` | 20 of 20 sit there, and a validator states a message's contract |
| 22 | 2026-08-21 | validator purity written into `validator.md` | 20 of 20 inject nothing, and a state-reading check in the pipeline is a race |
| 23 | 2026-08-21 | three service folders placed in `Infrastructure` | they are implementations; their interfaces stay in `Application/{Domain}/Services/` |
| 24 | 2026-08-21 | a subdomain level found between domain and role folders | forever-pin files `Codes/Core/`, `Codes/Content/`, `Codes/Rules/` |
| 25 | 2026-08-21 | iterations 21-22 reversed — validators move to `Infrastructure` | either kind may inject a service, and a service must never take an input it has to reject |
| 26 | 2026-08-21 | validators keep their place under `FoundationServices/` | no carve-out needed once the layer is settled |
| 27 | 2026-08-21 | per-use-case wrapping refuted (iteration 17 closed) | one location rule beats a second shape; the same argument that killed the folder threshold |
| 28 | 2026-08-21 | one location rule written | a component sits in its role folder under its subdomain, in the layer that owns its kind |
| 29 | 2026-08-21 | `Settings/` moved to `Infrastructure` | bound configuration is not contract, so it does not belong to the contract layer |
| 30 | 2026-08-21 | `UseCases/` wraps the dispatched path on both sides | it names the contents rather than the mediator, so a mediator swap leaves it standing |
| 31 | 2026-08-21 | repositories move to `Persistence/{Domain}/Repositories/` | row access belongs with the EF model and the schema, not with the rest of infrastructure |
| 32 | 2026-08-21 | foundation vocabulary ratified at 12 role folders | `Renderer` · `Formatter` · `Exporter` are foundation roles, not `Service` content |
| 33 | 2026-08-21 | a foundation service may inject another | `CodeRenderer` over 2 renderers and `QrCodeRenderer` over a generator + rasterizer both stand |
