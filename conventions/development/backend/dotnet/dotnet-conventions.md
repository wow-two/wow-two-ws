# Conventions — Development — Backend (.NET)

*Last updated: 2026-09-10*

> .NET convention lookup for services, libraries, SDKs and CLIs. The scope and deliverable shape are independent cuts.

## The two cuts [REQUIRED]

| Cut | Answers | Owner |
|---|---|---|
| Scope | one symbol, one codebase, between owned services | [core](core/core.md) |
| Shape | how a service, library, SDK or CLI is arranged, built and shipped | [shapes](shapes/shapes.md) |

- must put deliverable-independent rules in core.
- must put project placement, build, host composition and release rules in the applicable shape.
- must name only a role's folder in a construct or component doc; its project belongs to the shape.

## The scopes and the layers

Scope definitions and routing live in [core](core/core.md).
LLA owns platform forms and notation; MLA owns roles and their application within one codebase;
HLA owns contracts between independently deployed services we control.

<a id="the-layers-of-a-thing-required"></a>

## Definition and application [REQUIRED]

The authority model is the shared [documentation chain](../../development-conventions.md#documentation-chain-required).

| Authority | Home | Example |
|---|---|---|
| Baseline | [LLA constructs](core/lla/constructs/constructs.md) and [notation](core/lla/notation/notation.md) | record syntax, file layout, XML fields |
| Definition | [MLA constructs](core/mla/constructs/constructs.md) | what an Entity, Broker or Settings record is |
| Application | [components](core/mla/components/components.md), [domains](core/mla/domains/domains.md), or the applicable shape | settings registration, entity mapping, hosted work |

- must give our role one definition before documenting its application.
- must put a self-contained role's application in components.
- must put an application needing collaborators in its domain, or in a shape when deliverable-specific.
- must not treat a missing platform form or component page as proof of a missing role.
- must reference third-party APIs where our rule uses them; do not create a definition of a third party's surface.
- must keep variations in the application owner rather than duplicating the role definition.

## Layer direction [REQUIRED]

- must state a higher-scope override or extension at that higher scope.
- must link the exact lower-scope rule it overrides or extends.
- must cite the lower owner without restating it when adding no rule.
- must resolve a scope conflict in favour of the explicit higher-scope override.

## Files

The lead documents below own their leaf inventories. Descriptions here locate rules rather than restate them.

| Area | Owner | Coverage |
|---|---|---|
| Language forms | [constructs](core/lla/constructs/constructs.md) | C# forms, file rules and construct-level restrictions |
| Statements | [statements](core/lla/constructs/statements.md) | Statement and expression verdicts |
| Notation | [notation](core/lla/notation/notation.md) | Naming, documentation and style |
| Role vocabulary | [constructs](core/mla/constructs/constructs.md) | Suffix authorities, static gates, folds and coining |
| Data roles | [data](core/mla/constructs/data/data.md) | Entity, model, result, settings, options, spec and capabilities |
| Behavior roles | [behavior](core/mla/constructs/behavior/behavior.md) | Services, boundaries, transforms, tracking and generation |
| Patterns | [patterns](core/mla/constructs/patterns/patterns.md) | Applicability and house verdicts |
| Components | [components](core/mla/components/components.md) | Self-contained application contracts |
| Domains | [domains](core/mla/domains/domains.md) | Capability contracts and provider rules |
| Cross-service scope | [HLA](core/hla/hla.md) | Contracts between owned services |

### Domains

| Domain | Coverage |
|---|---|
| [persistence](core/mla/domains/persistence/persistence.md) | Entities, access, databases, migrations and test databases |
| [messaging](core/mla/domains/messaging/messaging.md) | Dispatch, delivery and provider seams |
| [identity](core/mla/domains/identity/identity.md) | Trusted claims, account context and authorization |
| [api](core/mla/domains/api/api.md) | HTTP requests, edge mapping and envelopes |
| [integrations](core/mla/domains/integrations/integrations.md) | Client/broker contracts and provider boundaries |
| [validation](core/mla/domains/validation/validation.md) | Validation phases and failure mapping |
| [observability](core/mla/domains/observability/observability.md) | Logging, tracing, metrics and startup failure capture |

### Deliverable shapes

| Shape | Coverage |
|---|---|
| [service](shapes/service/service.md) | Architecture, platform, topology and delivery |
| [architecture](shapes/service/architecture/architecture.md) | Project placement and architecture selection |
| [build](shapes/service/platform/build/build.md) | Central build properties, packages and SDK selection |
| [startup](shapes/service/platform/startup/startup.md) | Host registration, configuration and middleware |
| [responses](shapes/service/platform/responses/responses.md) | HTTP results, ProblemDetails, serialization and fixed endpoints |
| [SDK](shapes/sdk/sdk.md) | Package architecture, testing and release verification |
| [library](shapes/library/library.md) | Product-local package shape and adoption trigger |
| [CLI](shapes/cli/cli.md) | Command-line shape and adoption trigger |
