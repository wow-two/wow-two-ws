# Api messages

*Last updated: 2026-09-13*

> HTTP bodies and payloads, with explicit mapping between wire and application models.

## Requests

- must use the [api request declaration](../../constructs/data/api-request.md#declaration) for a dedicated body.
- must share a `CreateUpdate{Noun}ApiRequest` only while create and update accept the same body.
- must split into `Create{Noun}ApiRequest` and `Update{Noun}ApiRequest` when the bodies diverge.
- must leave route ids, caller identity, source IP and server timestamps off the body.
- must mark non-nullable body properties `required`.
- must leave authored field validation to the application boundary, not attributes on the HTTP body.
- may bind the application request directly only when its complete input equals the body:
  no route value or server-authoritative field is omitted from that comparison.
- must use a separate api request when mapping merges body and server-authoritative inputs.

---

## Sub-blocks

- must name a nested wire block `{Noun}Dto`, whether a request, response or both contain it.
- must reserve `ApiRequest` for a top-level action body.
- must map a sub-block at the same edge as its parent.
- must keep request-specific wire blocks at the delivery boundary; share a wire shape only when its contract is shared.

---

## Response

- must apply [service response rules](../../../../shapes/service/platform/responses/responses.md).
- must project an application [model](../../constructs/data/model.md) to a [dto](../../constructs/data/dto.md) at the edge.
- must keep `Dto` out of layers below that edge.
- must keep the success envelope to its payload; extra fields belong in the payload.

---

## Mapping

- must pass route ids and [caller context](api-context-building.md) as explicit mapping arguments.
- must name the mapping for its target role — `ToCommand(...)` or `ToQuery(...)`.
- must keep mapping independent of `HttpContext` and injected caller-context services.
- must use a block body for edge mapping.
- must keep the API request and its mapping extension class together in `{RequestType}.cs`, in the request's folder and namespace.
- must name that companion `{RequestType}Extensions`; it extends only that request and maps it through `ToCommand(...)` or `ToQuery(...)`.
- must apply [extension declaration rules](../../constructs/behavior/extensions.md) except this explicit folder, file, receiver-name and type-summary scope; the companion summary names the request mapping capability.
- must keep mapping a simple, deterministic projection of body values and explicit route/caller arguments; no persistence I/O, service calls, business decisions or workflow orchestration.
- must leave validation and business rules at the application boundary; a nested HTTP payload does not authorize complex mapping logic.
- must keep unrelated extensions outside the request file; this exception does not combine arbitrary types or response mappings.

---

## Placement rationale

The wire shape and its small boundary translation form one reviewable unit, so their declarations stay
together. WoW2 requires simple request mapping by design; HTTP itself does not limit payload complexity.
This is the scoped API request exception to [one type, one file](../../mla.md#one-type-one-file-required).

Example layout: `Requests/CreateCodeApiRequest.cs` contains `CreateCodeApiRequest` followed by
`CreateCodeApiRequestExtensions`; the extension's `ToCommand(...)` copies authored fields and accepts
server-authoritative values explicitly.
