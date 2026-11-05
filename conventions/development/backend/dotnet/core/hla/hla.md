# HLA — between our own services

*Last updated: 2026-11-05*

> High-level architecture: rules that only exist once there is more than one of our services.
> Purpose — keep fleet-shaped decisions out of `mla/`, where a single service would silently adopt them as defaults.
> Use case — reach here when a rule needs both ends to obey it, and we own both ends.

## The boundary

- **`hla/` when we own both ends** — gRPC contracts, cross-service event schemas, shared quotas, gateway routing.
- **`mla/` when we own one end** — a third party is *adapted*, never contracted.
- its client, broker and observed limits live in `mla/domains/`.

---

## Contents

- [API communication](api-communication.md) — service tokens, long-running work and revocation.

The folder was named ahead of its contents on purpose. Without it, the first gateway or gRPC rule lands in
`shapes/service/platform/` and becomes a single-service default that every later service inherits by accident.

Candidates, as they arrive:

- API gateway routing
- gRPC contract and versioning
- cross-service event schema and delivery guarantees
- rate limiting and quota allocation across services
- distributed tracing correlation
