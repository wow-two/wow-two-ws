# WoW 2.0 — Concepts

*Last updated: 2026-10-28*

> The words wow2 uses for what it builds, runs and owns, defined once so analyses, conventions and Wheelhouse mean
> one thing by each. A definition marked *proposed* waits for the developer. The forms a platform capability ships in:
> [capability forms](../conventions/development/capability-forms.md); the build order: [platform apps](platform-apps.md).

## Builds

| Term | Means | Examples | Status |
|---|---|---|---|
| product | what its users or its owner use, under a brand: one or more repositories, services and frontends released together, which Wheelhouse deploys as one product with its environments | ForeverPin, Haven, Ocharo (4 repositories, 9 services) | proposed |
| product service | "a service designed to serve a product only — whether or not it will be integrated to other products" | ForeverPin's `redirect`, Ocharo's `desk`, Haven's `database` | developer, 2026-10-27 |
| platform service | "a wow2 service — for example Wheelhouse, whether it's meant to integrate to others (file server, identity server, events harvester etc) or not" | Wheelhouse, Identity, Files, Harvest, Events | developer, 2026-10-27 |
| platform app | one row of the [platform app order](platform-apps.md): a platform service, or a platform tool that runs no service | Wheelhouse (#1), Identity (#2); the shared workflows (#8), the `wow` CLI (#9) | proposed |
| domain library | the library half of a [domain repo](../conventions/development/repo/structure/domain-structure.md): be packages and the fe package, holding the contract, the Form 1 module and the HTTP client | `WoW2.Sdk.Beta.Be.Identity.*`, `@wow-two-beta/fe-files` | proposed |
| module | a domain library's Form 1 part, which a product registers in its own process; it brings its own migration set | `Identity.Module` inside a product host | proposed |

- must classify a service by whom it was designed to serve, not by who calls it: a product service that another
  product integrates with stays a product service, and a platform service nothing calls stays a platform service
  (developer, 2026-10-27).
- a product holds product services; a platform service runs as one or more instances (proposed).
- a platform service that owns state and serves two or more products ships in the capability forms: its module is
  Form 1, its instances are Forms 2 and 3 (proposed).

---

## Runs and owns

| Term | Means | Examples | Status |
|---|---|---|---|
| instance | one running deployment of a platform service with its own settings, domain and release pace; where its migration sets live follows whom it serves: one product (a per-product instance) or several (a shared instance) ([migrations analysis](../ideas/migrations-analysis-2026-10/migrations-analysis-2026-10.md) M6) | Ocharo's Identity; the Files host | developer, 2026-10-27 |
| per-product instance | an instance that serves one product, its published image pulled beside the product or its libraries built into the product's image as a module (Form 1): its sets are named schemas in that product's database — "the same pgsql container and same database inside it, just separate schemas" — migrated in the product's step and restored with its snapshot; product tables may key into its published tables | Ocharo's Identity | developer, 2026-10-27 |
| shared instance | an instance that serves several products: its own database, "hosted separately, in a completely separate server" apart from every product's host, its own rollout as a Wheelhouse product of its own ([identity instances](../ideas/identity-instances-2026-10/identity-instances-2026-10.md) § Two owners' instances of one image, Q5 · B); products hold its ids, never a foreign key | the Files host serving many products as tenants; wow2's Identity for the platform apps | developer, 2026-10-27 |
| owner | the party a product or an instance belongs to, who decides its releases | wow2, Max's ventures, Ocharo, a client | proposed |
| migration set | ordered SQL migrations with one history table, one advisory lock and optionally one owned schema; the unit of schema ownership ([migrations](../conventions/development/backend/dotnet/core/mla/domains/persistence/migrations/migrations.md#model)) | a product's default set; the `identity` set | developer, 2026-10-27 (M3) |
| set owner | the one repository and assembly that embeds a migration set and decides its changes: a product, a module, a package or an instance's service; databases and services host sets and own none | `ForeverPin.Persistence`, `Identity.Module` | developer, 2026-10-27 (M3) |

- a per-product instance belongs to its product's owner; a shared instance serves several products, of one owner or
  many, as tenants (developer, 2026-10-27).
- a platform service reaches a product in one of two consumption modes: its published image pulled beside the product,
  or its libraries built into the product's image (a module, Form 1). The service's named set is the same in both, with
  its own history, so switching modes is a `claim`, not a migration (developer, 2026-10-27; M3, M76).
- a per-product instance turning shared is a move: its schema leaves for the shared server, and every foreign key into
  it becomes an id with loose cleanup (developer, 2026-10-27; M6, M33).
- an owner and a set owner differ: Ocharo owns its Identity instance, while the Identity repository owns the sets that
  instance runs (developer, 2026-10-27; M3).
