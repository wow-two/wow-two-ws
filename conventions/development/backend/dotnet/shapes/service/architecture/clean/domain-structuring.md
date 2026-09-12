# Domain structuring

*Last updated: 2026-09-10*

> Domain and subdomain grouping inside each Clean project.

## Domains

- must group source by domain before grouping by type role.
- must name a domain folder with its plural subject, such as `Listings/`.
- must give a domain with multiple subdomains a `Core/` for its shared model and reads.
- must name operation subdomains for their concern, such as `Capturing/`, `Processing/` or `Publishing/`.
- must not repeat the parent domain name in a subdomain name.
- must keep read queries, shared projections and common contracts in `Core/`.
- must keep operation-specific inputs, processing and external integrations with that operation.

---

## Alignment

- must use the same domain/subdomain names across projects where the concern exists.
- may omit a subdomain from a project that declares nothing for it.
- must not create empty mirror folders merely to make project trees identical.
- must place type-role folders beneath their owning domain or subdomain.
- must read role-folder names from their construct/component owner.
- must read project ownership from [Clean placement](clean.md#placement).

```text
Brand.Domain/                         Brand.Infrastructure/
  Listings/                             Listings/
    Core/                                 Core/
      Entities/                             FoundationServices/
      Enums/                              Capturing/
    Capturing/                              Brokers/
      Models/                             Processing/
                                            ProcessingServices/
                                          Publishing/
                                            Publishers/
```

- must put read orchestration in Infrastructure when row access is delegated to Persistence.
