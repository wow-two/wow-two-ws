# First ten — implementation

Updated: 2026-09-29

The user authorized creating the ten products under `workbench/ventures` and implementing all ten. This supersedes the earlier prototype-only scope. The deliverable is a usable authenticated local v0.1 for each product, with durable domain state, server-side rules, typed Vue integration and verified workflows. External payment, email and production hosting integrations remain launch work.

## Repository map

All repositories use org `ventures`, single-service mode, .NET 10 and Vue 3. Names describe the products; they are not trademark clearance.

| Idea | Repository | Backend namespace | Implementation lane |
|---|---|---|---|
| W0252 | ventures.retainer-balance | RetainerBalance | business |
| W0012 | ventures.documentation-checker | DocumentationChecker | developer |
| W0031 | ventures.file-watch | FileWatch | developer |
| W0263 | ventures.procedure-review | ProcedureReview | business |
| W0289 | ventures.training-seats | TrainingSeats | business |
| W0521 | ventures.epub-review | EpubReview | creator |
| W0276 | ventures.customer-promises | CustomerPromises | creator |
| W0261 | ventures.vendor-renewals | VendorRenewals | business |
| W0034 | ventures.config-checker | ConfigChecker | developer |
| W0507 | ventures.podcast-readiness | PodcastReadiness | creator |

## Track

- [x] Product workflow, market, implementation and clickable design analyses completed.
- [x] User authorized implementation of all ten.
- [x] Audited current template and installed SDK APIs.
- [x] Scaffold and register ten independent repositories.
- [x] Compose common authentication, persistence and frontend foundations.
- [x] Implement business workflows and tests in four repositories.
- [x] Implement developer workflows, customer-local tools and tests in three repositories.
- [x] Implement creator workflows and tests in three repositories.
- [x] Build and verify APIs, persistence, browser workflows and responsive states.
- [x] Save evidence, runtime commands, limitations and deployment gates per repository.

## Acceptance boundary

No generic client-state save endpoint, simulated operational action, or unguarded public mutation qualifies as implementation. Browser storage may hold view preferences only. Database writes must validate domain rules and reject stale revisions. Imports must be bounded and retry-safe. Exports must represent persisted state and retain resource scoping. Core workflows must operate without paid services. Product prices remain validation hypotheses.

SDK versions must match tested package contents. Installed local SDK packages may support local pilots, but production releases require a reproducible feed. Authentication must fail closed; a client-supplied tenant ID is not proof of membership. Billing, email delivery, hosted arbitrary code execution and third-party credentials are not configured by this task.

## Local delivery

[Open the venture app index](../../../workbench/ventures/first-ten.md) for repository links and startup commands. [Verification](implementation-verification.md) records actual tests, browser workflows, export artifacts and launch limitations. All ten are implemented local v0.1 pilots; no paid or production launch is claimed.
