# Shapes

*Last updated: 2026-08-19*

> What differs by **deliverable** — the kind of thing being built, not how far a rule reaches.
> Purpose — a service, a library and the SDK share every naming and construct rule and almost no structure.
> Use case — starting a repo, placing a folder in the project tree, or choosing an architecture.

## The shapes

| Shape | Is | Status |
|---|---|---|
| [service](service/service.md) | a hosted process answering requests — an API, a worker, or both | written |
| [library](library/library.md) | a package consumed inside one product, never published alone | shell |
| [sdk](sdk/sdk.md) | a reusable package family consumed by products | written |
| [cli](cli/cli.md) | a command-line tool | shell |

### The test

Not *does the rule change between deliverables* — a rule can be fixed forever and still belong here.
**Does the rule have a subject when this shape is absent?**

| Rule | Subject without a service | Home |
|---|---|---|
| middleware order — auth before authorization, static files first | none; only a host has a pipeline | shape |
| a registration method names a subject, never a layer | none; only a host has `Add*` seams | shape |
| a `Repository` is named `{Noun}Repository` | a library ships repositories too | core |
| `Directory.Packages.props` centralises package versions | none; `core/` rules the logic, not how it packs | shape |

- must file a rule by that test, not by whether it is stable.
- must not read a constant rule as a core rule — middleware order never changes and still has no meaning in
  a CLI or a package.

---

- must read [core](../core/core.md) first — every rule there holds here too, unchanged.
- must not restate a core rule in a shape; a shape states only what its deliverable changes.

---

## The vectors inside a shape

A shape is cut by vector, the same way a domain is. Each answers one question about the deliverable.

| Vector | Answers |
|---|---|
| `architecture/` | how the code is arranged inside it — clean, onion, hexagonal, vertical slice |
| `topology/` | how many processes it deploys as — monolith, modular monolith, microservices |
| `platform/` | how it is built, started, and how it answers |
| `delivery/` | how it is packaged and shipped — a container, a NuGet package, a binary |
| `testing/` | the test shape the deliverable earns |

- must give a vector its own folder, even when it holds one doc.
- must leave a vector absent rather than empty — a shape with no topology choice has no `topology/`.
- must not put a placement rule in `core/` — which project a `Services/` folder is created in is a shape's
  answer, and the construct doc names only the folder.
