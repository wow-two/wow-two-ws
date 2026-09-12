# Backend LLA and MLA construct audit

*Audited: 2026-09-09*

Read-only; no convention or SDK file edited. Existing dirty changes treated as intentional. Findings below are closure groups, not sentence counts. Related task IDs must be reused rather than duplicated. External primary sources were checked live on the audit date. Runtime concerns are not claimed reproduced.

## Findings: 27 groups

### L01 — Client/Broker test reversed

- Mapping: New; related N86/N92.
- Finding: The final provider-swap test gives the opposite answers to the vocabulary rules immediately above it.
- Closure: Mechanical: invert test answers; verify one provider-vocabulary and one house-vocabulary example.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:145` — - must use `Client` when the surface is the provider's own — its types, its call set, nothing of ours.
- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:146` — - must use `Broker` when the surface is ours, whatever it calls underneath.
- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:152` — - the test: would the surface change if the provider were swapped? no → `Client`; yes → `Broker`.

---

### L02 — Static form rules contradict their exceptions

- Mapping: Known N25; completed N6/N92 residue.
- Finding: No fourth static form conflicts with Factory, generic companions and Json; LLA permits only two forms. QuietZoneConstants is incorrectly called nonconforming. IMigrationSource carveout survived N92.
- Closure: Mechanical: consolidate static owner and link exceptions; remove stale Source reference. Resolve Json under N25.

Evidence:

- `conventions/development/backend/dotnet/core/lla/constructs/constructs.md:254` — - must use `static class` only for a `Constants` or `Extensions` role.
- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:204` — `Mapper` for a transform. There is no fourth static form, and a bare noun (`GeohashEncoder`, `QuietZoneConstants`) is none of them.
- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:214` — - must allow `Factory` on a `static class` when both gates below pass — the container-resolved form in
- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:227` — - must give the companion the generic type's exact name, with no suffix — it is the same thing, arity apart.
- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:268` — - must keep `Source` where it names a content origin read from, not a value derived — `IMigrationSource`.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/json.md:37` — - must hold its `JsonSerializerOptions` as a single `static readonly` instance, built once.

---

### L03 — Operation-specific Result records conflict with shared carriers

- Mapping: R7/R8; new convention closure.
- Finding: Result definition mandates per-operation sealed records while response owner specifies shared closed unions.
- Closure: Mechanical: define shared carriers in the construct and link application selection; remove stale per-operation examples.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/data/result.md:37` — - must declare a `sealed record` — a result is its values →
- `conventions/development/backend/dotnet/core/mla/constructs/data/result.md:51` — - must suffix with `Result`, prefixed by the operation — `ChannelGetAllResult`.
- `conventions/development/backend/dotnet/shapes/service/platform/responses/results.md:21` — - both are **closed DUs** — private ctor + sealed nested cases.

---

### L04 — Role-wide Result rules revive refuted blanket wrapping

- Mapping: N69/N81/N82.
- Finding: Service forbids bare values by role; Repository/Client/Broker also mandate Result by role. Mapper both permits failures and calls a non-total mapper a Validator.
- Closure: Mechanical: link failure-mode owner, preserving bridge/guard/framework exceptions; make total Result-valued mapping consistent.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/behavior/service.md:42` — - must return a `Result` carrying a [model](../../../conventions/development/backend/dotnet/core/mla/constructs/data/model.md) — never a `Dto`, never a bare value.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/repository.md:46` — - must return a `Result` — a read can miss and a write can conflict.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/client.md:50` — - must return a `Result` — a provider call fails, and the caller reads that from the type.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/broker.md:44` — - must return a `Result` — a seam over something outside the process always has a failure arm.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/mapper.md:61` — - must stay total: every input shape produces an output, or the type is a `Validator`.
- `conventions/development/backend/dotnet/shapes/service/platform/responses/results.md:37` — - must not read the role as the answer — `Mapper` is not exempt and `Extensions` is not exempt; the

---

### L05 — Validator definition contradicts domain and shipped contract

- Mapping: N10/N81; async seam explicitly deferred.
- Finding: Definition permits lookups, fixes Infrastructure placement and demands Result<ValidationOutcome>; domain forbids persisted reads and consumes ValidationError?. Current SDK agrees with the domain return contract.
- Closure: Mechanical: align active definition; preserve async/ruleset deferrals rather than silently implement them.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/behavior/validator.md:38` — - may take collaborators — a rule needing a lookup is still a rule, and a service must never receive an
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/validator.md:40` — - must live in `Infrastructure`, message validators and domain validators alike, because either may inject
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/validator.md:48` — - must return `Result<ValidationOutcome>` — the outcome carries the rule failures.
- `conventions/development/backend/dotnet/core/mla/domains/validation/validation.md:60` — - must not read persisted state inside an `IValidator<T>` — a validator is pure; phases 1 and 3 own that.
- `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Validation/IValidator.cs:10` — ValidationError? Validate(T instance);

---

### L06 — Options enforcement and defaults conflict

- Mapping: N74/N111; new convention closure.
- Finding: Suffix owner says required is compile-time enforced; definition says Activator bypasses it and requires validation. Defaults allegedly invert when changing to Settings despite the same table saying they match.
- Closure: Mechanical: state enforcement per construction path once; remove false default inversion.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:169` — - `Options` enforces `required` at compile time — `new T()` will not build → [options](../../../conventions/development/backend/dotnet/core/mla/constructs/data/options.md).
- `conventions/development/backend/dotnet/core/mla/constructs/data/options.md:46` — `Activator.CreateInstance`, which bypasses the compile-time guard → [options](../../../conventions/development/backend/dotnet/core/mla/components/options.md).
- `conventions/development/backend/dotnet/core/mla/constructs/data/options.md:68` — - must rename the type when a knob moves from code to configuration — the mutability and the defaults both
- `conventions/development/backend/dotnet/core/mla/constructs/data/options.md:64` — | Defaults | on every omittable member, both alike | same |

---

### L07 — ApiRequest positive sample violates its own naming rule

- Mapping: New.
- Finding: Verb-first rule is illustrated by NamespaceCreateApiRequest.
- Closure: Mechanical: use a verified verb-first positive example.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/data/api-request.md:41` — - must be named `{Verb}{Noun}ApiRequest`, verb-first — it exists for one controller action.
- `conventions/development/backend/dotnet/core/mla/constructs/data/api-request.md:47` — public sealed record NamespaceCreateApiRequest

---

### L08 — Adapter positive sample violates suffix and contract

- Mapping: N86; convention residue.
- Finding: Adapter suffix mandate is illustrated by HybridCacheRepository : ICacheBroker, while pattern sample uses ICacheRepository.
- Closure: Mechanical: use a real Adapter example or explicitly retain a settled capability-role exception.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/behavior/adapter.md:38` — - must suffix with `Adapter`, prefixed by the library — `FluentValidationAdapter<T>`.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/adapter.md:44` — public sealed class HybridCacheRepository : ICacheBroker
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/adapters.md:12` — `FluentValidationAdapter<T> : IValidator<T>` (`src/Foundation/Validation/`), `HybridCacheRepository : ICacheRepository`

---

### L09 — Interceptor definition excludes its observing contract

- Mapping: C8; new convention closure.
- Finding: All interceptors must receive next and choose whether to call it, despite separate read-only contracts. Phase/job ordering example also places Consume rather than job beside suffix.
- Closure: Mechanical: scope next rules to controlling interceptors; retain C8 observation-only power boundary; correct naming example.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/behavior/interceptor.md:46` — - must keep a read-only chain a separate contract from one that can short-circuit, so the power a step has
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/interceptor.md:53` — - must receive the next step and decide whether to call it — that is what makes it a chain rather than a list.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/interceptor.md:40` — `ClaimCheckRehydrateConsumeInterceptor`. The suffix stays last, the job stays beside it.
- `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Messaging/Transport/IConsumeObservingInterceptor.cs:16` — public interface IConsumeObservingInterceptor

---

### L10 — Pattern samples retain removed SDK names and positional records

- Mapping: Completed N34/N92/N112/N113; C8.
- Finding: Pipelines mandates Behavior/IPipelineBehavior; current contract is IRequestInterceptor. Strategies/outbox retain IOutboxClaimStrategy; current contract is IOutboxClaimRepository. Outbox/builder examples still use positional construction.
- Closure: Mechanical: update active samples from settled current source and compile representative examples during SDK sweep.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/patterns/pipelines.md:14` — - must give each step one concern, and suffix it for the framework that runs it — `Behavior` for a mediator step,
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/pipelines.md:21` — public sealed class LoggingBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/strategies.md:22` — public interface IOutboxClaimStrategy
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/outbox.md:18` — - must claim rows through an `IOutboxClaimStrategy`; scale-out takes `PostgresSkipLockedOutboxClaimStrategy`, a single
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/outbox.md:26` — new OutboxRecord(id, typeName, serializer.Serialize(new OrderPlacedEvent(order.Id)), occurredOnUtc, headers), ct);
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/builders.md:24` — public EventSagaDefinition Build() => new(_name, _stepTypes.AsReadOnly(), _destinations.AsReadOnly());
- `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Mediator/IRequestInterceptor.cs:4` — public interface IRequestInterceptor<in TRequest, TResponse> where TRequest : notnull
- `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Messaging/Reliability/Ef/IOutboxClaimRepository.cs:22` — public interface IOutboxClaimRepository

---

### L11 — Positive expression bodies fail global gates

- Mapping: N109 related; new.
- Finding: Mapper constructs over multiple lines; registry branches over three lines. Local permission explicitly still requires global no-construction/no-branch/one-line gates.
- Closure: Mechanical: block bodies or explicit justified override with backlink; check positive samples.

Evidence:

- `conventions/development/backend/dotnet/core/lla/notation/style/style.md:83` — and the first `no` blocks the expression body — a component that grants `=>` still has to pass them.
- `conventions/development/backend/dotnet/core/lla/notation/style/style.md:88` — 4. must not branch — a conditional is a step, and a step wants a name; a fluent chain is one expression.
- `conventions/development/backend/dotnet/core/lla/notation/style/style.md:89` — 5. must not be a construction — `new Foo(a, b)` is a body, however short, because a constructed shape gains members.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/mapper.md:67` — public CodeCreateCommand Map(CreateCodeApiRequest request) =>
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/registry.md:65` — public Type Get(CodeContentType key) => _bindings.TryGetValue(key, out var type)

---

### L12 — Mutable behavior ban excludes Builder/Registry

- Mapping: New.
- Finding: LLA permits mutable state only for Tracker; Builder mutates and Registry accepts registrations. No explicit linked override resolves it.
- Closure: Mechanical: distinguish collaborator immutability from role-owned lifecycle state and link role allowances.

Evidence:

- `conventions/development/backend/dotnet/core/lla/constructs/constructs.md:245` — - must hold no mutable state unless the role is a `Tracker`.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/builder.md:36` — - must declare a `sealed class` — a builder mutates as it accumulates.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/registry.md:58` — - must accept registrations at composition time only, never after the first lookup.

---

### L13 — Doc field admission and inheritance are ambiguous

- Mapping: New; related N108.
- Finding: Omitted fields are banned, but roles rely on lower-layer Member docs; mapper/registry examples use undeclared Params, Registry omits required Returns; Broker demands Remarks without a Remarks heading.
- Closure: Decision: define missing-section inheritance versus field restriction; mechanically propagate the chosen rule and repair samples.

Evidence:

- `conventions/development/backend/dotnet/core/lla/notation/documentation/documentation.md:58` — A component doc names the doc fields its types carry, one sub-heading each. **A field the component does not declare is
- `conventions/development/backend/dotnet/core/lla/notation/documentation/documentation.md:63` — - must not read a missing field as an oversight; a component with no `<remarks>` sub-heading forbids `<remarks>`.
- `conventions/development/backend/dotnet/core/lla/notation/documentation/returns.md:9` — - must carry `<returns>` on every method whose return type is not `void`, `Task`, or `ValueTask`.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/mapper.md:55` — /// <param name="request">The request to map.</param>
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/registry.md:53` — /// <param name="discriminator">The enum member to resolve.</param>
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/broker.md:26` — - must state the degradation in `<remarks>` when a caller has to act on it.

---

### L14 — Remarks requirements overlap bans

- Mapping: New; D6/D3 related.
- Finding: Static readonly Remarks ban overlaps mandatory remarks on fields evaluated through a method. Optional-everywhere conflicts with required exceptions. Positive multiline sample narrates an itinerary its rule says to cut.
- Closure: Mechanical: distinguish initialization from read-time computation; state optional baseline and explicit exceptions; replace positive sample with caller-actionable facts.

Evidence:

- `conventions/development/backend/dotnet/core/lla/notation/documentation/remarks.md:10` — `<remarks>` is **optional on every type-kind** — no component mandates one.
- `conventions/development/backend/dotnet/core/lla/notation/documentation/remarks.md:18` — - must not carry one on a `const` or `static readonly` — a value has no behavior to direct.
- `conventions/development/backend/dotnet/core/lla/notation/documentation/remarks.md:35` — - must carry it on a property or field whose evaluation calls a method or reaches I/O.
- `conventions/development/backend/dotnet/core/lla/notation/documentation/remarks.md:119` — - must cut any step the caller cannot act on — state what a consumer must know, never the itinerary.
- `conventions/development/backend/dotnet/core/lla/notation/documentation/remarks.md:125` — ///   - reads channels from the seed file

---

### L15 — Mixed typeparam rule contradicts omission

- Mapping: New.
- Finding: T plus TAggregate requires both skipping conventional T and documenting all parameters.
- Closure: Mechanical precedence clarification plus mixed-set example.

Evidence:

- `conventions/development/backend/dotnet/core/lla/notation/documentation/typeparams.md:13` — - must skip a **conventional** parameter — `T` · `TKey` · `TValue` · `TResult` · `TRequest` · `TResponse`.
- `conventions/development/backend/dotnet/core/lla/notation/documentation/typeparams.md:16` — - must document **every** parameter once any one is documented ([params](../../../conventions/development/backend/dotnet/core/lla/notation/documentation/params.md) § *Every parameter, every time*).

---

### L16 — One-owner rule duplicated throughout vector

- Mapping: New convention ownership task.
- Finding: File naming, sealed behavior, constructor injection, starters, using-static, var, Adapter/Builder naming appear in multiple layers without distinct overrides. Root says restatement is a defect even when copies agree.
- Closure: Mechanical owner map: replace agreement with section links; retain genuine specializations; merge no-delta pattern/construct duplicates.

Evidence:

- `conventions/development/backend/dotnet/core/lla/constructs/constructs.md:130` — - must give the type its own file, named for the type: `Channel.cs`, `IEntity.cs`, `ChannelGetAllQuery.cs`.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/behavior.md:34` — - must declare a `sealed class` — value equality is wrong on a type whose identity is what it does →
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/service.md:35` — - must declare a `sealed class` with a primary constructor for its collaborators.
- `conventions/development/backend/dotnet/core/lla/notation/naming/naming.md:22` — - **never `using static`** on an extensions class or any other type — it strips the class name off the call site
- `conventions/development/backend/dotnet/core/lla/notation/style/style.md:26` — - **`using static` is banned** — it strips the owning class off the call site.
- `conventions/development/backend/dotnet/core/lla/constructs/statements.md:134` — - must use `var` when the initializer names the type, and write the type when it does not
- `conventions/development/backend/dotnet/core/lla/notation/style/style.md:96` — - must use `var` when the initializer names the type — `var codes = new List<CodeEntity>();` repeats nothing.
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/patterns.md:15` — - must not restate a component's rules — a pattern a component doc already owns is a row below, not a doc

---

### L17 — Definition files leak application and placement rules

- Mapping: New.
- Finding: Constructs forbids technology/registration/flows and non-name facts in Type name; leaves still include Infrastructure, result contracts under Type name, and host scope lifecycle. Repository narrows broad storage vocabulary to rows.
- Closure: Mechanical: route application rules to existing domains/shapes and align Repository definition scope.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:321` — - must not state a technology, a registration, or an end-to-end flow — a [domain](../../../conventions/development/backend/dotnet/core/mla/domains) owns those.
- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:337` — - must state under `Type name` only what governs the **name**: the suffix, the prefix, the ordering, the ban.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/validator.md:40` — - must live in `Infrastructure`, message validators and domain validators alike, because either may inject
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/handler.md:43` — - must return `AppResult<T>` carrying a [model](../../../conventions/development/backend/dotnet/core/mla/constructs/data/model.md), never a `Dto`.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/background-service.md:74` — - must resolve a scoped collaborator from `IServiceScopeFactory` per run — the host holds this
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/repository.md:5` — > The type that reads and persists rows — data in, data out, and nothing else.

---

### L18 — Confirmed suffixes lack required baseline authorities

- Mapping: N100/N101 partly known; additional already-kept gaps.
- Finding: N100 records accepted Capabilities but row is absent. Tracker/Renderer/Generator/Rasterizer/Spec/crypto rows lack authorities despite row-and-doc gate; patterns use StateMachine/Saga absent from keep-list. NodaTime's IClock is a third-party contract and is exempt from house suffix renaming.
- Closure: Separate confirmed baseline completion from unconfirmed N100/N101 coining; do not create one component per construct.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:46` — | `Tracker` | live status many producers push into, persisted nowhere | — |
- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:72` — | `Renderer` | turns a model into a representation of it — text, markup, an image | — |
- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:73` — | `Generator` | derives a value from its inputs — an id, a code, a matrix | — |
- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:74` — | `Rasterizer` | vector → pixels | — |
- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:75` — | `Spec` | a declarative input shape a behavior component consumes — a renderer's style, a mapper's claim bindings; not a wire `Dto` | — |
- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:308` — A confirmed suffix earns a keep-list row and a doc in the same pass.
- `conventions/development/backend/dotnet/core/mla/components/time.md:34` identifies `IClock` as NodaTime; it is not a missing house-role definition.
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/patterns.md:75` — | State | the machine | `StateMachine` | `ProcessingServices/` |

---

### L19 — C# catalogue version/completeness lags SDK

- Mapping: New.
- Finding: Catalogues claim exhaustive C#13/.NET10 while listing C#14 field/extension syntax. No explicit verdicts for partial constructors/events, null-conditional assignment, unbound nameof, simple lambda modifiers, user-defined compound assignment or file-app directives.
- Closure: Mechanical inventory update to actual language baseline; retain house verdicts. Primary: [Microsoft documentation](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14)

Evidence:

- `conventions/development/backend/dotnet/core/lla/constructs/constructs.md:11` — Exhaustive through C# 13 / .NET 10. A form we have never written is still listed, with a verdict.
- `conventions/development/backend/dotnet/core/lla/constructs/statements.md:18` — Exhaustive through C# 13 / .NET 10. A form we have never written is still listed, with a verdict.
- `conventions/development/backend/dotnet/core/lla/constructs/constructs.md:59` — | `field` keyword | the generated backing field, inside an accessor | data | `use with care` |
- `conventions/development/backend/dotnet/core/lla/constructs/constructs.md:76` — | `extension` block | extension members grouped by one receiver | behavior | `use with care` |

---

### L20 — Language descriptions overstate technical facts

- Mapping: New.
- Finding: Event null-check race is avoidable with ?.Invoke; ref readonly call modifier omission is a warning; volatile does not prohibit all reordering. These corrections do not overturn house bans.
- Closure: Mechanical factual fixes. Primary: [Microsoft documentation](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/null-safety/null-operators) ; [Microsoft documentation](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters) ; [Microsoft documentation](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/volatile)

Evidence:

- `conventions/development/backend/dotnet/core/lla/constructs/constructs.md:109` — - the null-invocation race — the last subscriber detaches between check and call, and the call throws.
- `conventions/development/backend/dotnet/core/lla/constructs/constructs.md:52` — | `volatile` field | a field read and written without reordering | data | `use with care` |
- `conventions/development/backend/dotnet/core/lla/constructs/statements.md:122` — | `ref readonly` parameter | the same, modifier required at the call | `use with care` |

---

### L21 — Record Entity compatibility boundary needs verification

- Mapping: Owner decision; preserve deliberate house doctrine.
- Finding: Entity mandates sealed record while Microsoft discourages record entities because EF relies on reference equality. Prototype already forbids with-copies. Do not infer all record tracking is broken. init-blocks-tracker rationale is unverified, not a reproduced fact.
- Closure: Preserve doctrine pending targeted EF verification of navigation reference equality, duplicate tracked instances, mutable equality/hash and detached attach/update; document mitigations or owner-chosen narrowing. Primary: [Microsoft documentation](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/records) and [Microsoft documentation](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/record)

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/data/entity.md:36` — - must declare a `sealed record`.
- `conventions/development/backend/dotnet/core/mla/constructs/data/entity.md:39` — - must declare `{ get; set; }` — a materializer writes after construction, so `init` blocks the tracker.
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/prototype.md:36` — - must not copy an `Entity` with `with` — an entity is identified by its key, and a copy claims the same identity

---

### L22 — Pattern ban citations do not establish absolute bans

- Mapping: Owner decision; keep bans until settled.
- Finding: Node folding does not ban Composite trees, allocation measurement prerequisite does not categorically ban Flyweight, and Result.Match does not ban Visitor on other graphs.
- Closure: Explicitly state house bans at their owner or narrow verdicts to cited conditions; no authorization to introduce patterns.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/patterns/patterns.md:214` — | Composite | `mla/constructs/constructs.md` § *Folds* — `Node` → `PipelineStep` | `Pipeline` with ordered steps |
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/patterns.md:215` — | Flyweight | `constructs.md:94` — allocation must be measured first | a plain reference type |
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/patterns.md:216` — | Visitor | `results.md` § *Carriers* — `.Match` is the consume path | a `switch` over the closed union |

---

### L23 — Scope factory instructions conflict

- Mapping: New; N94 related.
- Finding: Singleton says take scope factory instead of scoped capture; service locator forbids it to dodge lifetime mismatch; BackgroundService legitimately scopes each run.
- Closure: Mechanical: state per-operation scope ownership/disposal versus forbidden retained scoped state.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/patterns/singleton.md:42` — - must not capture a scoped service in a singleton constructor; take `IServiceScopeFactory` instead
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/service-locator.md:44` — - must not use a scope factory to dodge a lifetime mismatch — a singleton holding scoped state is a lifetime error,
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/background-service.md:74` — - must resolve a scoped collaborator from `IServiceScopeFactory` per run — the host holds this

---

### L24 — Template Method contradicts base-call discipline

- Mapping: New.
- Finding: Shape demands base.OnModelCreating ordering docs; Limits forbids subclass obligations at a particular point. Positive EventSagaStep has hooks but no fixed nonvirtual flow.
- Closure: Mechanical: separate framework-required calls from our templates and use a real fixed-flow example.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/patterns/template-method.md:16` — - must state the contract the subclass owes in `<remarks>` on the base — *call `base.OnModelCreating` first*.
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/template-method.md:46` — - must not leave a hook that a subclass **must** call at a particular point — make the base call it instead.
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/template-method.md:21` — public abstract class EventSagaStep : IEventSagaStep

---

### L25 — Proxy pattern misclassifies EF interceptors

- Mapping: New.
- Finding: AuditInterceptor is presented as a generated EF proxy; SaveChangesInterceptor is a registered handwritten callback mechanism.
- Closure: Mechanical: retain Refit proxy example and route EF hook rules to interception/persistence. Primary: [Microsoft documentation](https://learn.microsoft.com/en-gb/ef/core/logging-events-diagnostics/interceptors)

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/patterns/proxies.md:12` — `src/Http/Refit/`), EF Core for a save-time interceptor (`AuditInterceptor`, `src/Data/EntityFrameworkCore/Audit/`).
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/proxies.md:16` — - must keep an interception hook single-purpose: one interceptor stamps audit fields, another applies soft delete

---

### L26 — Lazy Initialization Open note is stale

- Mapping: New.
- Finding: Patterns says LLA does not rule on Lazy, while LLA has a use gate, field starter and deferral requirement.
- Closure: Mechanical: route as owned or name only a remaining unsettled question.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/patterns/patterns.md:227` — - **Lazy Initialization** — `Lazy<T>` is a BCL type we instantiate, not a construct we declare, so
- `conventions/development/backend/dotnet/core/lla/constructs/constructs.md:246` — - must reach for `Lazy<T>` only when the value is expensive and some paths never read it —
- `conventions/development/backend/dotnet/core/lla/constructs/constructs.md:220` — - must name the deferral on a `Lazy<T>` field — the first read pays a cost the signature hides.

---

### L27 — Traceability and authoring closure missing

- Mapping: New.
- Finding: No broken relative file links across 65 files, but nonexistent section citations remain; long tables violate root budget; older narrative/rationale/history is still embedded in rule docs.
- Closure: Mechanical: check anchors and symbols, extract rationale, repair tables and outdated examples; retain decisions.

Evidence:

- `conventions/development/backend/dotnet/core/mla/constructs/data/model.md:36` — - must declare a `sealed record` → [data](../../../conventions/development/backend/dotnet/core/mla/constructs/data/data.md) § *Declaration*.
- `conventions/development/backend/dotnet/core/mla/constructs/data/settings.md:41` — - must declare a `sealed record` → [data](../../../conventions/development/backend/dotnet/core/mla/constructs/data/data.md) § *Declaration*.
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/time.md:36` — - must build on `TimeProvider` → [constructs](../../../conventions/development/backend/dotnet/core/lla/constructs/constructs.md) § *The constructs*.
- `conventions/development/backend/dotnet/core/lla/constructs/constructs.md:127` — - [domain structuring](../../../conventions/development/backend/dotnet/shapes/service/architecture/clean/domain-structuring.md) states which layer it may appear in.

---

## Intentional deferrals / non-findings

- No backend/frontend component-count parity task: be-forwards.md corrects the earlier handoff selection rule. Result/value-object/mapper application docs belong to the separate component audit. Patterns and domain-owned applications do not all need component docs.
- Memento intentionally deferred until undo/draft restore use case.
- Validation async, phase-1 placement, rule sharing, ruleset exposure and Dapper/EF seam remain named deferrals; align contradictory active rules without silently implementing those designs.
- N25 owns Json re-test; N100/N101 own coining decisions.
- House bans and record Entity doctrine remain in force unless owner revises them.
- No SDK build or runtime tests ran; this is a convention audit.

## Full read inventory

All 65 assigned documents were read:

- `conventions/development/backend/dotnet/core/lla/components/indexers.md` (65 lines)
- `conventions/development/backend/dotnet/core/lla/constructs/constructs.md` (262 lines)
- `conventions/development/backend/dotnet/core/lla/constructs/statements.md` (144 lines)
- `conventions/development/backend/dotnet/core/lla/lla.md` (23 lines)
- `conventions/development/backend/dotnet/core/lla/notation/documentation/documentation.md` (251 lines)
- `conventions/development/backend/dotnet/core/lla/notation/documentation/exceptions.md` (15 lines)
- `conventions/development/backend/dotnet/core/lla/notation/documentation/inline.md` (48 lines)
- `conventions/development/backend/dotnet/core/lla/notation/documentation/params.md` (46 lines)
- `conventions/development/backend/dotnet/core/lla/notation/documentation/remarks.md` (129 lines)
- `conventions/development/backend/dotnet/core/lla/notation/documentation/returns.md` (38 lines)
- `conventions/development/backend/dotnet/core/lla/notation/documentation/summary.md` (120 lines)
- `conventions/development/backend/dotnet/core/lla/notation/documentation/typeparams.md` (33 lines)
- `conventions/development/backend/dotnet/core/lla/notation/naming/naming.md` (66 lines)
- `conventions/development/backend/dotnet/core/lla/notation/notation.md` (31 lines)
- `conventions/development/backend/dotnet/core/lla/notation/style/style.md` (209 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/adapter.md` (47 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/background-service.md` (86 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/behavior.md` (49 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/broker.md` (51 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/builder.md` (48 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/client.md` (52 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/controller.md` (52 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/extensions.md` (57 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/handler.md` (50 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/interceptor.md` (66 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/json.md` (50 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/mapper.md` (80 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/policy.md` (49 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/registry.md` (78 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/repository.md` (53 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/service.md` (49 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/time.md` (49 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/validator.md` (58 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md` (387 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/data/api-request.md` (50 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/data/application-request.md` (55 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/data/constants.md` (50 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/data/data.md` (34 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/data/dto.md` (51 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/data/entity.md` (51 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/data/enums.md` (49 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/data/model.md` (52 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/data/options.md` (76 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/data/result.md` (51 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/data/settings.md` (55 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/data/value-object.md` (50 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/adapters.md` (59 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/ambient-context.md` (57 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/builders.md` (52 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/circuit-breaker.md` (55 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/decorators.md` (55 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/factories.md` (68 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/null-object.md` (57 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/outbox.md` (58 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/patterns.md` (229 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/pipelines.md` (62 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/prototype.md` (47 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/proxies.md` (56 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/sagas.md` (60 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/service-locator.md` (56 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/singleton.md` (54 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/state-machines.md` (59 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/strategies.md` (64 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/template-method.md` (57 lines)
- `conventions/development/backend/dotnet/core/mla/constructs/patterns/unit-of-work.md` (52 lines)

Additional full reads:

- `conventions/conventions.md`
- `be-forwards.md`
- `be-components-lane.md`
- `conventions/development/backend/dotnet/dotnet-conventions.md`
- `conventions/development/backend/dotnet/core/mla/mla.md`
- `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/be-convention-sweep.md`
- `conventions/development/backend/dotnet/shapes/service/platform/responses/results.md`
- `conventions/development/backend/dotnet/core/mla/domains/validation/validation.md`
- `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Validation/IValidator.cs`

Targeted reads:

- `.claude/repo-registry.md:81` (SDK identification)
- `conventions/development/backend/dotnet/core/mla/domains/persistence/entities/entity-contracts.md` (identity/member rules)
- `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Mediator/IRequestInterceptor.cs` (contract declaration)
- `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Messaging/Reliability/Ef/IOutboxClaimRepository.cs` (contract declaration)
- `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Messaging/Transport/IConsumeObservingInterceptor.cs` (contract identification)

## Mechanical checks

- Broken relative file links: none across assigned files.
- Section anchors and bare source citations need separate checks.
- Tables with lines over 120 characters:

- `conventions/development/backend/dotnet/core/lla/lla.md`: 14
- `conventions/development/backend/dotnet/core/lla/notation/style/style.md`: 43
- `conventions/development/backend/dotnet/core/mla/constructs/constructs.md`: 40, 49, 65, 75, 187, 190, 192, 193, 194, 195, 198, 249
