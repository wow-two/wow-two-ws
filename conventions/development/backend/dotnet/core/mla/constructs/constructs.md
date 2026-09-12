# Constructs

*Last updated: 2026-09-10*

> The canonical suffix→role vocabulary for backend types — one name per role,
> the suffix declaring the responsibility.
> Purpose — when `Store`, `Repository` and `Provider` all mean data access, a reader cannot infer role from a name.
> Use case — naming any backend type; check the keep-list before coining, run the gate before adding.

## How to use

- must pick the suffix whose **role** matches what the type does — a suffix is a contract, not decoration.
- must rename to the canonical when the name you reached for appears in § *Folds*.
- must run § *Adding a new suffix* when no existing suffix fits.
- must leave *how* a role behaves to the cited authority — this doc is the vocabulary.
- framework-named types and contracts (`Middleware`, `Filter`, `TimeProvider`, `IClock`, and an `Interceptor` deriving from a base such as
  `SaveChangesInterceptor`) are exempt; the framework owns the name.

---

## Rename cost [REQUIRED]

- must not weigh rename cost when deciding a name — decide what is correct, rename everything carrying the old one.
- must not keep a wrong name because it is established, shipped, or used in another repo.
- must treat the vocabulary as iterable — a name settled last month gets re-settled the moment a better one is argued.
- must refuse a name for duplicating a role, never for the work of renaming; **saturation** is the real cost.

A rename that builds and passes is done — the compiler and the tests are the whole safety argument.

---

## Keep-list

One suffix per role. Where another doc owns the role, that doc is the **authority** and this row is the index.
Split by what the type is for — [data](data/data.md) holds, [behavior](behavior/behavior.md) does.

- `Service`
  - role: business logic, orchestration, compute — the default role
  - authority: [service](behavior/service.md)
- `BackgroundService`
  - role: work the host runs off the request path, for as long as it lives
  - authority: [background service](behavior/background-service.md)
- `Client`
  - role: one external provider's call surface, out-of-proc
  - authority: [client](behavior/client.md)
- `Broker`
  - role: the app-side seam over an external dependency
  - authority: [broker](behavior/broker.md)
- `Repository`
  - role: any seam reaching data — rows, documents, blobs, keys, files
  - authority: § *`Repository`*
- `Factory`
  - role: runtime instance creation, per key or per request
  - authority: [factories](patterns/factories.md)
- `Registry`
  - role: key → type or capability bindings, registered at composition
  - authority: [registry](behavior/registry.md)
- `Tracker`
  - role: live status many producers push into, persisted nowhere
  - authority: [tracker](behavior/tracker.md)
- `Extensions`
  - role: static logic over a domain — no injection, no state
  - authority: [extensions](behavior/extensions.md)
- `Handler`
  - role: the receiver of one dispatched message
  - authority: [handler](behavior/handler.md)
- `Command` · `Query` · `Event`
  - role: a dispatched use case — write, read, fan-out
  - authority: [application request](data/application-request.md)
- `Validator`
  - role: input validation for one request
  - authority: [validator](behavior/validator.md)
- `Controller`
  - role: the HTTP delivery surface — a thin dispatcher
  - authority: [controller](behavior/controller.md)
- `ApiRequest`
  - role: the API edge body one controller action binds
  - authority: [api request](data/api-request.md)
- `ApiResponse`
  - role: the success envelope a client reads `.data` from
  - authority: [api messages](../domains/api/api-messages.md)
- `Dto`
  - role: a projection onto the wire — data, never behavior
  - authority: [dto](data/dto.md)
- `Entity`
  - role: a table-mapped row, owning its identity
  - authority: [entity](data/entity.md)
- `ValueObject`
  - role: values stored inside a row; identity is the values
  - authority: [value object](data/value-object.md)
- `Result`
  - role: the carrier — a typed success or an `AppError`
  - authority: [result](data/result.md)
- `Model`
  - role: the application's own shape of a thing, inside the carrier
  - authority: [model](data/model.md)
- `Adapter`
  - role: a third-party type fitted to an interface we declared
  - authority: [adapter](behavior/adapter.md)
- `Builder`
  - role: stepwise construction, ending in `Build()`
  - authority: [builder](behavior/builder.md)
- `Policy`
  - role: decides whether, when, or how often another operation runs
  - authority: [policy](behavior/policy.md)
- `Settings`
  - role: a config section bound through `IOptions<T>`
  - authority: [settings](data/settings.md)
- `Options`
  - role: behavior knobs passed in code, bound from nothing
  - authority: [options](data/options.md)
- `DbContext`
  - role: the EF unit of work
  - authority: [database](../domains/persistence/database/database.md)
- `Configuration`
  - role: an EF `IEntityTypeConfiguration<T>`
  - authority: [entity configuration](../domains/persistence/access/ef/entity-configuration.md)
- `Constants`
  - role: a holder of `const` and `static readonly` values
  - authority: [constants](data/constants.md)
- `Mapper`
  - role: any deterministic in→out transform, owning no data
  - authority: [mapper](behavior/mapper.md)
- `Pipeline` · `PipelineStep`
  - role: an ordered multi-step flow, and one step of it
  - authority: [pipelines](patterns/pipelines.md)
- `Interceptor`
  - role: a step a message passes through on its way to its handler
  - authority: [interceptor](behavior/interceptor.md)
- `Middleware` · `Filter`
  - role: a framework hook — exempt from the gate, because the framework owns the name
- `Cipher`
  - role: encryption and decryption
  - authority: [cipher](behavior/cipher.md)
- `Hasher`
  - role: input to digest
  - authority: [hasher](behavior/hasher.md)
- `Issuer`
  - role: an issued authentication artifact
  - authority: [issuer](behavior/issuer.md)
- `Authenticator`
  - role: evidence to authenticated identity
  - authority: [authenticator](behavior/authenticator.md)
- `Renderer`
  - role: turns a model into a representation of it — text, markup, an image
  - authority: [renderer](behavior/renderer.md)
- `Generator`
  - role: derives a value from its inputs — an id, a code, a matrix
  - authority: [generator](behavior/generator.md)
- `Rasterizer`
  - role: vector → pixels
  - authority: [rasterizer](behavior/rasterizer.md)
- `Spec`
  - role: a declarative input shape consumed by behavior
  - authority: [spec](data/spec.md)
- `Capabilities`
  - role: supported operations, a kind of model
  - authority: [capabilities](data/capabilities.md)
- `Json`
  - role: one type's persisted JSON seam — `Options`, `Serialize`, `Deserialize`
  - authority: [json](behavior/json.md)

**Scope.** Every suffix here names a type in an owned backend codebase: service, library, SDK or CLI.
A browser-side type is a wire projection of one, so it carries none of them.
What the frontend calls its own types is [the frontend's](../../../../../frontend/frontend-conventions.md).

---

## `Mapper` vs `Registry`

Both answer "given X, give me Y". The line is who owns the mapping data.

- must use `Mapper` when the data arrives as an argument — pure, no injection, no I/O, nothing stored.
- must use `Registry` when callers register into it and it owns whether the set is whole.
- must use `Service` or `Broker` instead when the lookup needs injected collaborators or I/O.
- must not call it a `Registry` when nothing registers — a table read from config is a `Mapper` handed its data.

`Registry` holds **types and capabilities**; `Repository` holds **instances**. An in-memory `Repository` is still one.

| | `Registry` | `Repository` |
|---|---|---|
| Holds | key → type or capability | instances of an entity |
| Entries appear | at composition, in code | at runtime, from user or system action |
| A lookup gives you | something to dispatch to | something to read or write |

---

## `Repository`

One role for every seam that reaches something holding data — a table, a document, a blob, a cache, a
key with a TTL, a file on disk.

- must name the contract `Repository` whatever holds the data, because the contract has to survive a
  swap: moving a domain from Postgres to Redis is a host-configuration change, and a use case never
  learns that it happened.
- must not encode the engine, the permanence or the access shape in the role — each of those is an
  implementation fact, and a role that carries one renames when the implementation changes.
- must carry the implementation in the **prefix** — `EfUserRepository`, `RedisOtpRepository`,
  `LocalFileBlobRepository`, `InMemoryTenantRepository`. Swapping one never touches the contract.
- must keep an entity's **persistence knowledge** in its repository — relations, key shape, hashing,
  encoding, the projection a row needs. A service never sees how a thing is stored.
- may compose a repository from a more abstract one — the entity's repository states what this entity
  needs, and the generic one underneath does the reaching. Both are repositories.
- must use `Service` only when the logic is about **what to fetch and why**, which is a business decision;
  *how this entity is stored* never is.

---

## Role and shape

A capability contract carries the **role**; the type implementing it carries the **shape** it takes.

- must suffix the contract with its role — `ICacheRepository`, `IBlobRepository`, `IUserRepository`.
- must carry the shape as a **prefix** and the role as the suffix — `InMemoryDeadLetterRepository`,
  `SystemTextJsonMessageSerializer`, `HybridCacheRepository`. The suffix answers *what is this*, the prefix
  answers *which implementation*.
- must not stack two role words — `CacheStorageAdapter` names a kind, a role and a shape at once, where
  `HybridCacheRepository` says the same thing in the order the tree already uses.
- must leave a lone implementation the role's own name — a shape prefix earns its place by telling one
  implementation from another.
- `Adapter` · `Broker` · `Client` stay suffixes where the shape **is** the role — a type whose whole job is
  fitting a library, reaching a system, or speaking a provider's surface.

---

## `Client` vs `Broker`

Both reach an external system. The line is whose vocabulary the type exposes.

- must use `Client` when the surface is the provider's own — its types, its call set, nothing of ours.
- must use `Broker` when the surface is ours, whatever it calls underneath.
- must use `Adapter` when the type fits a **library** to a contract we declared, and `Broker` when it
  reaches a **system** — `HybridCacheRepository` delegates to a library type, while a hand-written Redis
  seam would cross the wire in our vocabulary and be a `Broker`.
- both may implement one capability contract — `ICacheRepository` names the capability, and the adapter or the
  broker behind it is an implementation detail the caller never sees.
- must test whether a provider swap changes the surface: yes → `Client`; no → `Broker`.
- either may exist alone; a `Broker` may sit over a `Client`, a vendor SDK, or a raw `HttpClient`.

---

## `Settings` vs `Options`

- must use `Settings` when the config binder populates it from `appsettings.json`.
- must use `Options` when a caller supplies it in code — a delegate, or `new`.

Both carry their defaults the same way, and the origin only changes what enforces the rule.

- must give every omittable member a default on the type — the caller states what differs, nothing else.
- must declare a member that has to be supplied as `required`, with no default — a placeholder value that
  never runs is worse than an absent one, because it runs.
- must not ban defaults to keep configuration honest — `required` is what marks a value the caller owns,
  and a full `appsettings.json` of unchanged values hides the few lines that matter.
- must validate required members when reflection constructs the value — the binder and `Activator` bypass `required`.
- must let object initializers enforce `required` at compile time when the caller writes `new T { … }`.
- registration and validation → [options](../components/options.md) · [settings](../components/settings.md).

---

## Folds

Each left-hand suffix names a role an existing suffix already owns.
Rename to the canonical; never introduce the synonym.

- `Store`
  - canonical: `Repository`
  - why: both are rows in, rows out against a backing store
- `Gateway`
  - canonical: `Broker`
  - why: a gateway to an external system is the app-side seam
- `Provider`
  - canonical: `Service`
  - why: every service provides something; the word adds nothing
- `Node`
  - canonical: `PipelineStep`
  - why: a node means nothing outside the pipeline it steps through
- `Encryptor`
  - canonical: `Cipher`
  - why: `Cipher` is the established crypto-primitive suffix
- `Mapping` · `Profile`
  - canonical: `Mapper` · `Spec`
  - why: the type maps → `Mapper`; a `Profile` that only declares a mapping's inputs → `Spec`. `Profile` is AutoMapper's
    base type, not a role
- `Normalizer`
  - canonical: `Mapper`
  - why: `T → T` is a transform; idempotence is a property, not a role
- `Map`
  - canonical: `Mapper`
  - why: the type is a function, and `Map` reads as data
- `Resolver`
  - canonical: `Mapper` · `Broker` · `Service`
  - why: pure → `Mapper`; out-of-process → `Broker`; injected collaborators → `Service`
- `Emitter`
  - canonical: `Renderer`
  - why: emitting a representation of a model is rendering it
- `Source`
  - canonical: `Generator` · `Broker`
  - why: derives a value → `Generator`; reads one from an external store → `Broker`, the seam a provider swap stops at
- `Observer`
  - canonical: `Handler` · `BackgroundService` · `Service`
  - why: the word names a position and a permission, never a verb — a bound receiver is a `Handler`, a timer poller a
    `BackgroundService`, and a notified hook whose work is its own verb is a `Service` named for that work
- `Scheduler`
  - canonical: `BackgroundService` · `Service`
  - why: runs itself on a timer → `BackgroundService`, because a poller schedules nothing; takes a request to deliver
    later → `Service`, which is a capability a caller reaches for
- `HostedService`
  - canonical: `BackgroundService`
  - why: both are host-run work; the name should say how it executes, not that it is hosted
- `Keeper`
  - canonical: `Service`
  - why: a synonym for a stateful service
- `Behavior`
  - canonical: `Interceptor`
  - why: the word names a category, not a job — a pipeline step intercepts
- `Filter` · `Observer`
  - canonical: `Interceptor`
  - why: both sit in the chain; what each does goes in the middle word, `FilteringInterceptor` · `ObservingInterceptor`

- must keep a **third-party** name as it ships — a fold governs only names we choose.
- must fold a name in our own SDK like any other — the SDK is ours, so a convention change reaches it as a
  row in that repo's sweep file, never as an exemption.
- must name a pure `static class` by its role — `Constants`, `Extensions` or `Mapper`.
- may use the `Factory`, non-generic companion and `Json` forms declared below and in their role docs.
- must not leave a static transform named `GeohashEncoder`; its role is `Mapper`.

### `Factory` vs `Mapper`

Both take arguments and hand back an object. The line is which end the caller cares about.

- must use `Factory` when the **output type is the point** and the arguments are ingredients —
  `AppErrorFactory.NotFound(resource, id)` builds an `AppError` out of parts that were never one.
- must use `Mapper` when **one shape becomes another** — `ConfigurationMapper.Map<T>(configuration)`
  hands back the same information wearing a different type.
- must allow `Factory` on a `static class` when both gates below pass — the container-resolved form in
  [factories](patterns/factories.md) is the same role with a variant to choose.
- must name it singular — `DbUpProviderFactory`, never `…Factories`; the type is one factory with many
  methods, not a bag of them.

---

### The non-generic companion

A generic type often needs a same-named non-generic `static class` beside it, so a caller can state both type
arguments explicitly — `Result` beside `Result<T>`, `SagaTestHarness` beside `SagaTestHarness<TState>`. The
companion is a language idiom, not a role.

- must give the companion the generic type's exact name, with no suffix — it is the same thing, arity apart.
- must keep it to entry points that return the generic type; anything else belongs on its own type.
- must not read it as a bare noun failing the three static forms — the generic type's name already carries
  the role, and a suffix here would name the companion something the generic type is not.

---

### `static readonly` is a value

- must file a `static readonly` object built once at type load under `Constants` — being configured does
  not make it behavior, and `JsonOptionsConstants` owns those options the way a literal is owned.
- must split values from operations unless the role explicitly owns both, as the [Json seam](behavior/json.md) does.

---

### Static or instance

Two independent gates, and a `static class` needs **both**.

- **Simple**
  - passes when: the logic is arrangement — combining strings, ordering fields, a format's layout
  - fails when: it is a real algorithm — hashing, compression, key derivation, cipher work
- **Single**
  - passes when: exactly one variant of the operation exists
  - fails when: the operation names a family a caller could pick from

- must declare a `static class` only when both gates pass — base32 encoding, snake-casing, a geohash.
- must declare an instance type when either gate fails, so the choice is made at registration.
- must not treat statelessness as the test — a stateless type still goes instance when a gate fails.

Worked examples:

- an RFC payload encoded by combining strings — simple ✓, single ✓ → `static class`
- the same string work where the spec admits several encodings — simple ✓, single ✗ → instance
- hashing a string — simple ✗, single ✗ → instance
- a geohash — simple ✓, single ✓ → `static class`, and `GeohashEncoder` still needs one of the three forms

- must read an algorithm-selecting argument on a static method as the signal both gates failed —
  `Hash(value, HashAlgorithm.Sha256)` is a registration decision leaking into every caller.
- must not count a `static readonly` options field as state — a value built once at type load is a constant.
- a single-variant operation that grows a second implementation becomes a service then, and the rename is
  the record that it grew one.

---

## Banned

Each names *nothing* — it describes "a class that does stuff". The gate points at the real role.

| Banned | Why | Reach for |
|---|---|---|
| `Manager` | "manages" = unspecified work | `Service` · `Registry` · `Tracker` |
| `Helper` · `Common` | an unspecified role | `Extensions`, or fold into its owner |
| `Util` · `Utils` | `Helper`, vaguer | `Extensions` |
| `Accessor` | "accesses" = reads — say what | `Repository` · `Client` · `Service` |
| `Engine` | an important-sounding `Service` | `Service`, or `Pipeline` for a flow |
| `Strategy` | names swappability, which is a shape rather than a responsibility | `Policy` · `Mapper` · `Service` |

---

## Adding a new suffix [REQUIRED]

Answer in order; the first **yes** picks the suffix, and coining requires four `no`s.

1. does it call out-of-process? → `Client` or `Broker`.
2. does it persist or read rows? → `Repository`.
3. does it only supply configuration? → `Settings` or `Options`.
4. is it pure compute or orchestration with no narrower role? → `Service`.

- must coin only for a role no existing suffix covers — a distinct verb, never a synonym.
- must not coin inline; a name that misses is copied forward by every later scaffold.
- must state the role's verb in one line — no verb to state means it is a `Service`.
- must name the nearest two suffixes and why each fails — failing against none means it folds.
- must bring both to the developer and wait; only a confirmed suffix is implemented.

Rapid scaffolding raises this bar rather than lowering it — scaffolding replicates an unconfirmed name fastest.

---

## Adding a component [REQUIRED]

A confirmed suffix earns a keep-list row and a doc in the same pass.
The doc states the **baseline** — what the type is, wherever it is used.
Whatever varies by technology or by flow belongs to the domain that uses it.

- must give each component one file, named for the suffix it defines — `mapper.md` for `Mapper`.
- must carry the `##` sections in order — `Location` · `Declaration` · `Content`.
  - omit a section rather than rename it.
- must name a **role folder** as the plural of the suffix — `Mapper` → `Mappers/`, `Entity` → `Entities/`.
- must name a **subject folder** for the domain or capability it holds, never for a role — `Integrations/`,
  `Integrations/{Provider}/`, `Codes/`. The plural rule governs role folders only, and a subject folder's
  children answer to their own roles.
- must state only the folder **name**, never its layer
  ([domain structuring](../../../shapes/service/architecture/clean/domain-structuring.md)).
- must not state a technology, a registration, or an end-to-end flow — a [domain](../domains/) owns those.
- must cite [one type, one file](../mla.md) rather than restate it — state a deviation only.
- must land before the first implementation — an unwritten baseline is what lets `Normalizer` ship beside `Mapper`.
- must follow [writing a doc in this scope](../mla.md) for the shared doc rules.

| Section | Sub-headings | States |
|---|---|---|
| Location | Folder · File | the folder name that wraps it, and the file's name |
| Declaration | Type doc · Construct · Type name | the doc fields, the form declared, and the name |
| Content | Member docs · Members | the members, when this doc is what fixes them |

- must omit `Content` when the shape belongs elsewhere — the SDK for a type it declares, the domain for the rest.
- must carry `Content` when the members **are** the contract, as a [component](../components/components.md) does.
- must give the construct its own `### Construct` sub-heading — `sealed record`, `sealed class`, `static class`.
- must keep a member fact out of `Type name` — `init`-only and `required` are the construct's, ruled at
  [lla constructs](../../lla/constructs/constructs.md) § *Data components*.
- must state under `Type name` only what governs the **name**: the suffix, the prefix, the ordering, the ban.

````markdown
# {Components}

*Last updated: {YYYY-MM-DD}*

> {One line saying what the role is.}
> Purpose — {what having it buys}.
> Use case — {when to reach for it}.

---

## Location

### Folder
- must {rule}

### File
- must {rule}

---

## Declaration

### Type doc

#### [Summary](../../lla/notation/documentation/summary.md)
- must {rule}

```csharp
// ✅
{good}
// ❌ {why it fails}
{bad}
```

### Type name
- must {rule}
````

[The component template](../components/components.md) § *Adding a component* keeps a third `Content` section, because a
component is self-sufficient: its members are the whole contract, and no domain exists to own them.

---

## Authoring this doc

- must stay vocabulary and role, never prose — cite the authority instead of restating its rules.
- must list what we **recognize**, not what has shipped — a role earns a row before any type carries it.
- must cite a real symbol in an example, and carry no example at all for a recognized-but-unbuilt role.
