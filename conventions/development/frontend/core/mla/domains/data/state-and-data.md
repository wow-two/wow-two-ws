# State and data

*Last updated: 2026-10-02*

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

## Loading

A data region answers three loading moments differently: the first load, a refresh the user asked for, and a
background refetch. The user must always be able to tell that an asked-for refresh ran.

- must render a first load as a skeleton shaped like the loaded region; use a generic structural skeleton when that shape is unknown.
- must not show a visible `Loading…` paragraph instead of loading content; a single screen-reader announcement remains appropriate.
- must replace existing values with their matched skeletons during a user-requested refresh.
- must retain a known empty region during refresh; must not invent populated grid geometry.
- must hold that skeleton for a minimum duration, 400 ms by default, through the SDK `useRefresh`.
- must keep labels, headings and actions visible during a refresh; only values turn into placeholders
  (`SkeletonStateSlot`).
- must keep identities (names, ids, paths) through a refresh; they turn into placeholders on a first load only.
- must keep content on screen during background refetches and polling; show freshness with a timestamp or `fetching`.
- must settle a failed first load into neutral plain copy; request failure text belongs to the toast host.
- must keep last good values when a refresh fails.
- must keep refresh in the page or region toolbar across loading, content, empty and unavailable outcomes.
- must not put retry buttons or failure cards inside an ordinary collection result.
- must render table skeletons within the existing rows and columns, keeping its heading visible.
- must reserve the collection region through loading and empty outcomes without adding an empty-state card.
- may crossfade skeleton and result opacity; must not animate layout height or reorder surrounding content.
- must honor `prefers-reduced-motion` for placeholder animation and result transitions.
- empty collection geometry → [EmptyState](../../components/display/emptyState.md#values).
- must announce loading once per region through `SkeletonStateGroup`; the skeleton shapes stay decorative.
- must show a running refresh on its control through `Button` `isLoading`: the icon turns into a spinner, the label
  stays and the control dims; it keeps focus, and overlapping requests share one pending state.

```vue
<script setup lang="ts">
const vitals = useFleetVitals();
const { refresh, refreshing } = useRefresh(vitals.refetch);
</script>
<template>
  <SkeletonStateGroup :is-loading="vitals.loading || refreshing">
    <span>Memory</span> <SkeletonStateSlot>{{ percent }}%</SkeletonStateSlot>
  </SkeletonStateGroup>
</template>
```

- which surface answers which wait → [feedback](../../components/feedback/feedback.md#loading).

---

## Mutations

- must not use optimistic persisted updates: never change confirmed rows, counts, status flags, caches or navigation outcomes before mutation acknowledgement.
- must keep the form, editor and confirmed content in place while a mutation runs; use loading/disabled action controls for that pending state.
- must distinguish unsaved local drafts, previews and recovery from confirmed server state; those local editing interactions remain immediate.
- must await mutation success before closing its form, removing its row or refreshing affected query keys.
- must refresh each affected grid or editor through its independent read projection after success; that explicit refresh may replace query values with skeletons.
- must consume a command acknowledgement separately from the read result; returned resource data is not an implicit replacement for a different projection.
- may consume an operation's immediate result where that result is the workflow's actual content, such as a generated download or upload acknowledgement.
- must keep a successful write acknowledged if its following read fails; report the refresh failure without inviting duplicate creation.
- must guard overlapping submissions and preserve confirmed content and unsaved input on failure.
- command response shape → [API commands and reads](../../../../../backend/dotnet/core/mla/domains/api/api.md#commands-and-reads).
- must leave confirmed cache values intact on failure and expose the failure to the caller.
- must keep mutation retries off by default; retry only an operation with a declared idempotency contract.
- must distinguish a transport cancellation from proof the server did not commit a mutation.
- must retain the latest value for [autosave](../forms/submission.md), rather than equate deduplication with saving it.

---

## Error adaptation

- must translate a failed public `Result` into a vendor rejection inside a query adapter when the engine requires it.
- must translate that rejection back into the public failure/lifecycle state at the adapter boundary.
- must keep vendor errors and result containers out of the app contract.
- must report page-load and API failures, including HTTP 500, through the app toast host using display-safe localized wording.
- must not place request error messages, HTTP status text or raw backend bodies in ordinary page, grid or card content.
- may render field validation beside its field and error records in a component whose actual purpose is displaying errors; neither exception permits a generic request failure banner.
- must settle query failures through the [loading lifecycle](#loading); a failure must not leave skeletons running.
- must deduplicate notices for the same failure episode across retries and overlapping subscribers; a later distinct failure may notify again.
- must preserve unsaved edits after refresh or mutation failure.
- must keep field validation beside its field; request failure toasts do not replace actionable validation.
- must prevent duplicate notices when both a form and a global query error subscriber handle the same failure.
- must test retry, cancellation and cache behavior against each adapter, not only resolved values.
