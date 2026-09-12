# State and data

*Last updated: 2026-09-10*

> Request outcomes, server caches and local state across frontend frameworks.

## Transport

- must wire app origins and proxies through [app delivery](../../../../shapes/app/delivery/delivery.md).
- must keep endpoint clients and wire DTOs in the app's `integration/{domain}/` slice.
- must document the method and route at each endpoint function.
- must validate and decode a payload through [type mapping](../api/type-mapping.md).
- must return a [Result](../../constructs/data/result.md) for expected request failures.
- must type a no-content endpoint as `Result<void>`; never cast an empty response into arbitrary `T`.
- must handle malformed JSON, unexpected content types and invalid success payloads as protocol failures.
- must distinguish cancellation, timeout, transport failure and an HTTP failure.
- must pass the caller's cancellation signal to the transport; suppress cancellation notices.
- must set JSON content headers only for JSON bodies; let the browser set multipart boundaries for `FormData`.
- must retain HTTP status and response headers at the integration edge, outside transport-free failure fields.
- must map display-safe failures through the app error catalog, never display an untrusted server body verbatim.
- must consume the backend [success envelope](../../../../../backend/dotnet/core/mla/domains/api/api-messages.md).
- must parse RFC 9457 [ProblemDetails](../../../../../backend/dotnet/shapes/service/platform/responses/problem-details.md).
- must preserve unknown error codes as data without treating them as a known discriminant.

---

## State

- must keep server-owned cached values in the query capability; editing and local UI state stay outside it.
- must define a query key from every variable that selects the response, including tenant/session scope.
- must expose live query state separately from a completed operation's `Result`.
- must fetch through orchestration hooks; presentation consumes their state and actions.
- must map a DTO at integration when the app needs a different representation; a straight read may keep its DTO.
- must dispose session-scoped caches on logout or identity change; late responses cannot repopulate them.
- must persist local state only through [storage](../storage/storage.md).
- must keep framework/engine bindings in provider leaves, including [Vue queries](vue/vue.md).

---

## Mutations

- must reflect only backend-confirmed state; do not pre-write cache entries from mutation input.
- must reconcile success through the returned value or invalidate the affected query keys.
- must leave confirmed cache values intact on failure and expose the failure to the caller.
- must keep mutation retries off by default; retry only an operation with a declared idempotency contract.
- must distinguish a transport cancellation from proof the server did not commit a mutation.
- must retain the latest value for [autosave](../forms/submission.md), rather than equate deduplication with saving it.

---

## Error adaptation

- must translate a failed public `Result` into a vendor rejection inside a query adapter when the engine requires it.
- must translate that rejection back into the public failure/lifecycle state at the adapter boundary.
- must keep vendor errors and result containers out of the app contract.
- must prevent duplicate notices when both a form and a global query error subscriber handle the same failure.
- must test retry, cancellation and cache behavior against each adapter, not only resolved values.
