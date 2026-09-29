# Http

*Last updated: 2026-09-26*

> Outbound HTTP registration and transport resilience behind the client/broker boundary.

## Registration

- must register clients through `IHttpClientFactory`.
- must prefer `AddRefitApiClient<TApi>` for a new declarative HTTP client.
- must use `AddResilientClient<TClient>` for a typed client, or add `AddSdkResilience` to manual registration.
- must provide base addresses through settings, not source literals.
- must configure JSON at the supported preset seam rather than bypass it with unrelated settings.
- registration API → [Refit registration](../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Http/Refit/RefitClientServiceCollectionExtensions.cs).

---

## Resilience

- must configure retry, circuit breaking and timeout through the SDK resilience seam.
- must keep attempt timeout below the total logical request budget.
- must preserve the provider's valid relationship between attempt timeout and circuit-breaker sampling duration.
- must not stack independent retry loops in a client and broker.
- must not retry or hedge an unsafe side effect without a replay-safe contract or idempotency mechanism.
- must use `UnsafeRequestReplaySelector` to opt an unsafe method into replay; safe methods are GET, HEAD, OPTIONS and TRACE.
- must treat `StreamContent` as non-replayable; streaming calls use the retry client and run once for unsafe methods.
- must pass cancellation through every outbound call.
- must not treat caller cancellation as permission to spend another retry attempt.
- must configure tracing explicitly through the [observability owner](../../observability/observability.md).
- current options and pipeline → [resilience options](../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Http/Resilience/HttpResilienceOptions.cs)
  and [resilience registration](../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Http/Resilience/HttpResilienceBuilderExtensions.cs).
- hedging is a separate client registration; must not stack it with the retry pipeline.

---

## Handlers

- must add cross-cutting HTTP handlers on the same factory-managed client registration.
- must configure authentication, client certificates, hedging and propagated headers only when the integration needs them.
- must not forward arbitrary inbound credentials to another provider.
- must dispose response messages and owned streams after consuming them.

---

## Destination safety

- must use `AddSafeOutboundHttp` on clients accepting external or user-controlled destinations.
- must validate the actual resolved address at connection time, including mapped IPv4 and IPv6 transition ranges.
- must disable automatic redirects and system proxies when destination policy depends on the socket callback.
- must follow a redirect explicitly through the protected client so the next destination is checked.
- must keep HTTPS required unless the integration explicitly permits HTTP.
- must opt private-network destinations in explicitly for controlled internal integrations.
- must not replace the guarded primary handler or enable HTTP/3 on the protected client.
- must configure response-size limits separately; destination protection does not bound downloaded content.

---

## Errors

- must let the HTTP pipeline observe transport exceptions before converting them at the app-facing boundary.
- must preserve a provider's typed failure details when translating them into the application's error vocabulary.
- must follow the [result policy](../../../components/result.md#failure) outside the framework's HTTP callback contract.
- must place fallback, stale-cache use and degradation in the [broker](../integrations.md#degradation).
