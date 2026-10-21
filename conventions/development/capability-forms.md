# Capability forms

*Last updated: 2026-10-21*

> How a platform capability ships: an SDK library, a self-hosted service image and a provided service, under
> one client contract.
> Use case — identity, file storage, secrets, notifications, audit: a concern several products need that owns
> state or secrets.

## Scope

- must apply this to a capability that owns state, secrets or a hosted surface and serves two or more products.
- must not apply it to stateless code; a helper with no storage is an SDK module only →
  [SDK extraction](sdk-extraction.md) § Extract.

---

## Forms

| Form | Ships | Runs | Consumer owns |
|---|---|---|---|
| 1 · library | an SDK module | inside the consumer's process | config, tables, secrets |
| 2 · self-hosted service | SDK client + Docker image | a container the consumer deploys | the container's config |
| 3 · provided service | the SDK client only | one central deployment we operate | its client config |

- may offer one, two or all three forms; the capability's spec names which.
- must start with the cheapest form a named consumer needs now.
- must add a form when a named consumer needs it: isolation for Form 2, no operations for Form 3.

---

## Contract

- must define the client contract before any form ships.
- must keep one contract across every form; a consumer changes form by configuration, never by code.
- must ship two registrations behind the contract: the in-process module and the HTTP client.
- must keep vendor types out of the contract → [swappable modules](swappable-modules.md) § Contract.
- must run one conformance suite against the in-process module and against the running image.

---

## Layout

| Half | Lives in | Holds |
|---|---|---|
| library | be SDK; an fe SDK subpath for UI | contract, Form 1 module, HTTP client, UI parts |
| service | `wow-two-platform.{capability}` | host, admin UI, Dockerfile, `deploy.yml` |

- must build the service by hosting the Form 1 module, never by implementing the logic a second time.
- must keep the service's HTTP API a mirror of the contract; the service adds hosting, admin and app routing.
- must publish the image per [deployment descriptor](../deployment/descriptor/deploy-descriptor.md) § Rules.
- must keep UI parts form-agnostic; they call the consumer's backend or the service API through the contract.

---

## Ownership

- must let a Form 1 consumer own the tables, migrations and secrets; the module ships the migrations.
- must let a Form 2 or Form 3 service own its database; a consumer never reads its tables.
- must store a running service's secrets per [secrets](../security/secrets/secrets.md) § Storage.
- must list the capability, its forms and their state in the platform app order `docs/platform-apps.md`.
