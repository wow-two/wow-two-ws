# Startup

*Last updated: 2026-08-17*

> How a host is composed, and what it has running before the first request arrives.
> Purpose — a boot decision made per service drifts; made once, every later service inherits it.
> Use case — adding a host, registering a dependency, changing what the pipeline does before a handler.

## What lives here

- [host configuration](host-configuration.md) — the `Configure` / Extensions split, settings, env overrides
- [startup defaults](startup-defaults.md) — the `AddApiDefaults()` / `UseApiDefaults()` boot floor
- [launch profiles](launch-profiles.md) — `launchSettings.json`, one `https` profile, the even/odd port pair

---

## Boundary

- must keep a rule that is true before any feature exists here.
- a feature-shaped rule belongs to its domain.
- must apply [host-owned configuration](host-configuration.md#configuration-source).
