# API endpoint documentation

*Last updated: 2026-10-02*

> Pending XML/commenting baseline for MVC APIs; the separate ProblemDetails error-contract decision is adopted.

## Status

- The developer approved controller block bodies separately.
- That rule lives in [controller member content](../conventions/development/backend/dotnet/core/mla/constructs/behavior/controller.md#member-content).
- Documentation scope remains one pending decision; implementation waits for the brainstorming result.
- Existing XML defaults remain authoritative; the developer separately approved typed ProblemDetails error contracts on 2026-10-02.

---

## Source snapshot

Roots relative to `wow-two-ws/`:

- `C` = `workbench/ocharo-hq/ocharo-ws/workbench/ocharo-platform/engineering/codebase/ocharo-catalogue.backend-services/`.
- `A` = `C/OcharoCatalogue.Api/`.

Verified in the checkout:

- `C/Directory.Build.props` targets `net10.0`.
- `C/Directory.Packages.props` pins `Microsoft.AspNetCore.OpenApi` to `10.0.12`.
- `A/Configurations/HostConfigurationExtensions.cs:35` calls `AddOpenApi()`.
- `A/Configurations/HostConfiguration.cs:26` exposes `MapOpenApi()` only in development.
- No `GenerateDocumentationFile` setting exists in the Catalogue project/build files inspected.
- No Swagger UI or Scalar registration exists in those files.
- Catalogue controller actions do not currently declare response metadata.
- `A/Catalogue/Controllers/DesignsController.cs` owns `api/catalogue/designs`; the path is not missing.
- Its create action returns `200` with `CatalogueDesignDetail`; documentation must reflect that current contract.
- Enabling XML generation and adding truthful metadata are distinct implementation steps.

These are source observations, not a generated-document or runtime verification.

---

## Existing owners

- [API action attributes](../conventions/development/backend/dotnet/core/mla/domains/api/api.md#action-attributes) require truthful success payload types and actual ProblemDetails failure schemas.
- [API action naming](../conventions/development/backend/dotnet/core/mla/domains/api/api.md#action-naming) already requires an action summary.
- [XML documentation](../conventions/development/backend/dotnet/core/lla/notation/documentation/documentation.md) supplies inherited defaults.
- [Params](../conventions/development/backend/dotnet/core/lla/notation/documentation/params.md) require complete documented parameter sets.
- [Returns](../conventions/development/backend/dotnet/core/lla/notation/documentation/returns.md) require a value description for `Task<T>`.
- [Remarks](../conventions/development/backend/dotnet/core/lla/notation/documentation/remarks.md) admit consumer constraints conditionally.

A later convention patch should extend these owners rather than create a second documentation policy.

---

## Proposed baseline

A compact contract has machine-readable metadata and consumer-facing text.

### Machine-readable contract

- Preserve explicit HTTP verb, literal route and binding source.
- Declare every supported response status, its actual payload and its media type.
- Use typed `ProducesResponseType<T>` for JSON responses; name the real envelope only when one is returned.
- Use a bodyless response declaration for `204`.
- Propose explicit `ProblemDetails` or `ValidationProblemDetails` error schemas where the runtime emits them.
- Audit automatic validation, authorization and middleware outcomes alongside explicit action returns.
- Add `Consumes` only for intended input formats; it affects request acceptance.
- Declare binary response media types and schemas for PDF/image/ZIP exports.
- Treat attributes as descriptions to verify, not proof that implementation matches.

The framework can infer success schemas from typed returns, but `IActionResult` needs explicit metadata.
ASP.NET Core also distinguishes response schemas, media types, descriptions and bodyless responses.
Web API analyzers are deprecated in .NET 10; propose generated-spec and HTTP contract tests instead.
[Microsoft: endpoint metadata](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/openapi/include-metadata?view=aspnetcore-10.0).

Typed ProblemDetails failure schemas were adopted through the separate error-contract request; the XML-text baseline remains pending.
Shared error metadata can be factored only where the same statuses and schemas truly apply.
Do not blanket-claim `401`, `403`, `404` or `409` on endpoints without those outcomes.

### XML text

- Recommend a concise `<summary>` for each endpoint: purpose plus a behavior the name alone misses.
- Retain current `<param>` and `<returns>` defaults; avoid repeating CLR types.
- Reserve `<remarks>` for client obligations: revision checks, pagination, idempotency or publication boundaries.
- Use `<response code="...">` only when an outcome needs explanation beyond its status.
- Add examples for non-obvious payloads; exclude secrets and sensitive customer data.
- Document DTO field units, null meanings and constraints beside those fields.
- Keep implementation explanations as local `//` comments, not public endpoint descriptions.
- Avoid duplicate XML summaries and `EndpointSummary` strings for the same endpoint.

.NET 10 maps XML text into OpenAPI when XML generation is enabled.
`AddOpenApi()` is a supported source-generator entry point; a nonliteral document-name argument has limitations.
Referenced projects need XML generation too when their DTO comments should appear.
`<response>` adds descriptions to already-declared statuses; it cannot create a missing response entry.
[Microsoft: XML integration](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/openapi/openapi-comments?view=aspnetcore-10.0).

### Return shape

- Retain `Task<IActionResult>` for this documentation pass.
- Discuss `ActionResult<T>` separately if stronger success-type inference is desired.
- Do not change wire envelopes or success statuses merely to improve documentation.

`ActionResult<T>` supports success schema inference; `IActionResult` accommodates differing result types with attributes.
[Microsoft: controller return types](https://learn.microsoft.com/en-us/aspnet/core/web-api/action-return-types?view=aspnetcore-10.0).

---

## Generation and verification proposal

- Enable XML generation for the API and referenced DTO-bearing projects.
- Keep built-in OpenAPI generation; choose a development UI only if useful.
- `Swagger UI` and `Scalar` are viewers, not replacements for accurate response contracts.
- Review generated paths, verbs, success/error schemas, descriptions and file responses.
- Test representative success, validation, missing-resource, conflict and download outcomes.
- Compare those outcomes with generated metadata; source annotations alone cannot establish parity.
- Consider a CI-generated OpenAPI artifact for contract review and client generation.
- Do not require booting production or exposing documentation publicly to verify a build artifact.

ASP.NET Core separates OpenAPI document generation from interactive UIs and supports runtime/build-time generation.
[Microsoft: OpenAPI overview](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/openapi/overview?view=aspnetcore-10.0).

---

## Points

- [ ] Choose the endpoint documentation baseline before adopting or sweeping it.

Options for that single decision:

- Essential, recommended: typed response metadata plus concise XML summary/params/returns; remarks/responses/examples when meaningful.
- Thorough: the same metadata plus per-status response text and a consumer-contract remarks block on every endpoint.

The essential option reduces duplicate prose while preserving generated schemas and inherited XML defaults.
The thorough option makes every action longer and requires more text to stay synchronized.
Neither XML-text option is approved; an application XML documentation sweep remains outside the approved error-contract work.
