# Platform

*Last updated: 2026-08-16*

> How a service builds, starts, and answers — the floor every endpoint stands on.
> Purpose — a boot decision made per service drifts; made once, it is inherited.
> Use case — adding a host, changing what the pipeline does before a handler runs.

## What lives here

| Folder | Answers | Lead |
|---|---|---|
| [build](build/build.md) | how the solution and its packages are declared | the two solution-root files |
| [startup](startup/startup.md) | how a host is composed, what runs before a request | the boot floor |
| [responses](responses/responses.md) | what the service sends back, success or failure | one success, one error shape |

---

## The boundary

- must hold a rule that is true before any feature exists.
- a feature-shaped rule belongs to its [domain](../../../core/mla/domains/domains.md).
- must apply [host-owned configuration](startup/host-configuration.md#configuration-source).
- must keep a technology choice out — how we talk to a broker or a database is that domain's.
