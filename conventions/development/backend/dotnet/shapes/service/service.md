# Service

*Last updated: 2026-08-19*

> A hosted .NET process that answers requests, runs background work, or both.
> Purpose — service-specific architecture, platform and deployment rules.
> Use case — building or changing an API, a worker host, or a service's project tree.

## Vectors

| Vector | Lead | Status |
|---|---|---|
| [architecture](architecture/architecture.md) | how the code is arranged inside the service | written — `clean/` |
| [platform](platform/platform.md) | how it is built, started, and how it answers | written |
| [topology](topology/topology.md) | how many processes it deploys as | shell |
| [delivery](delivery/delivery.md) | how it is packaged and shipped | shell |

- must take every naming, construct and component rule from [core](../../core/core.md) unchanged.
- must answer **where a folder is created** here — a construct names `Services/`, this shape says which
  project holds it.
