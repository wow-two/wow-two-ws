# Host configuration rationale

*Last updated: 2026-09-10*

> Reasons for host-owned wiring and asynchronous startup; rules live in host configuration.

## Ownership

Explicit product registrations keep every wire visible from the host's configuration chain.
The SDK provides reusable registration contracts; product glue remains in each host.
Small repeated glue blocks across hosts are accepted until they earn an SDK seam.

---

## Async startup

Blocking a startup task hides its asynchronous contract and encourages copying the blocking form into request code.
Awaiting startup work preserves its completion and failure path without occupying a blocked thread.
A host may fail before accepting traffic when required initialization cannot complete.

The normative rules live in [host configuration](host-configuration.md#async-startup).
