# Conventions — Development

*Last updated: 2026-09-10*

> The **development** domain: how we structure repos and write code. Lookup table, not auto-loaded.
> Each area has its own `{area}-conventions.md` index.

| Area | Covers |
|---|---|
| [repo/](repo/repo-conventions.md) | Repo shape — layout & naming ([repo-structure](repo/structure/repo-structure.md)) · version control · tech stack |
| [backend/](backend/dotnet/dotnet-conventions.md) | .NET code style — documentation, code-org, entities, enums, services, architecture, db, API, launch-profiles |
| [frontend/](frontend/frontend-conventions.md) | TypeScript, cut twice — `core/` by scope · `shapes/` by shape |

**Cross-area:** [dev-cycle.md](dev-cycle.md) — the 2-cycle app↔SDK maturation rhythm: implement a version in-app → extract stable blocks to the SDK + conventions → adopt across the active apps.

**Cross-area:** [swappable-modules.md](swappable-modules.md) — engine-wrapping SDK modules: contract-first, adapter subpaths with optional peers, one conformance suite, one-line app engine pin.

**Cross-area:** [sdk-extraction.md](sdk-extraction.md) — the extraction **threshold**: what earns a place in either SDK (carries logic + ecosystem-worth) vs stays inline in the product (pure DRY / layout wrappers — duplicate freely); an atom that carries logic is never product-local.

Versioning moved to the sibling **planning** domain → [`../planning/`](../planning/planning-conventions.md).

<a id="the-layers-of-a-thing-required"></a>

## Documentation chain [REQUIRED]

Each thing has a documentation chain: the platform form, our definition, and its application.
These describe the same thing; they do not replace the `lla` / `mla` / `hla` scopes.

| Authority | Is | Present when |
|---|---|---|
| 1 · baseline | what the language or framework already ships — `const`, `BackgroundService`, `TimeProvider`, `useState` | the platform defines the form we build on |
| 2 · construct | **what the thing is** — our definition of a role nothing official defines, its declaration and where it lives | always; no other source defines it |
| 3 · application | **every condition for applying it** — options, attributes, variations, what the SDK ships for it | the thing has conditions worth writing down |

- must keep the construct to the definition — a construct doc says what a thing *is*, never how it behaves in a
  given situation.
- must put every variation in the application — one-to-many versus many-to-many is an application of `Entity`,
  never part of what an entity is.
- must let a thing carry two docs when it has both definition and application — `constructs/{name}.md` defines it and
  `components/{name}.md` applies it, the second linking the first.
- must let the platform form be absent — a role we coined starts at its definition.
- must let the application be absent when a role has no conditions worth adding to its definition.

### Both scopes carry both roles

Constructs and components are **roles**, and each scope holds both — the scope decides whose thing is being
ruled, the role decides whether the doc defines it or applies it.

| | `constructs/` — what it is | `components/` — every condition for using it |
|---|---|---|
| `lla/` | the language form and its verdict — `this[…]`, `record`, `const` | that form used end to end, ours or not — an indexer's accessors, docs and members |
| `mla/` | our role, defined once — `Broker`, `Constants`, `Entity` | our thing applied, when it stands alone |

- must not file a language form's own conventions under `mla/` — a rule that would hold in a project with
  none of our roles present belongs to `lla/components`.
- must not read `lla/` as construct-only — a form we neither wrap nor extend still has conditions of use,
  and those are `lla/components`.

---

### Whose thing earns a doc

A convention doc rules **our** code. The baseline is the platform we build on — C# and .NET on the backend,
the browser and the framework on the frontend — plus our own SDK. Everything else is a dependency we
happen to use today.

- must document only the platform, the framework, and our own SDK — never a third-party library's own
  surface.
- may name a third-party type where our rule needs it — `AbstractValidator<T>`, `IServiceCollection` — and
  a component or domain doc may state the **surface** we touch, never how the library works inside.
- must not restate a third-party naming, documentation or shape rule as ours: the library ships its own,
  our wrapper delegates, and the SDK owns whatever internals we end up keeping.
- may leave a named third-party type outside our own naming and documentation conventions — one day it is
  adopted behind our own type, re-cut to our conventions, or replaced, and none of those needs a doc now.
- must not read "we will replace this one day" as a reason to soften a rule — a rule states what to write
  today, and the replacement rewrites the rule when it lands.

---

<a id="where-layer-3-lives"></a>

### Application ownership

The application splits by **self-sufficiency** — the same register, two possible owners.

| The thing | Application owner | Because |
|---|---|---|
| stands alone with no service, domain or collaborator present | `components/` | its conditions are complete on their own — a `Constants` class and its `Description` attributes |
| needs collaborators to mean anything | `domains/` | its conditions are the domain's — an `Entity` needs a repository, a schema and relations |

- must not file a thing under `components/` to give it a home — a thing needing a collaborator has its
  application in the domain that supplies one.
- must not split the application across both — one home per thing, chosen by the test above.

---

## Using & evolving conventions

- develop **against** the conventions — read the relevant one before / while writing the code, and follow it
- found a gap or a clearly better way? don't silently diverge — implement, then **propose the convention add / update with the reason(s)**, after the implementation
- the convention change rides in with the work that motivated it — so we keep shipping while closing convention gaps
