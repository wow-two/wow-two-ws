# Integrations

*Last updated: 2026-10-26*

> Reaching a system we do not own — the transport guarantee every outbound call carries, and who owns what.
> Purpose — transport resilience answers to the channel, degradation answers to the app; the two never merge.
> Use case — adding a provider, or deciding where a retry and a fallback each belong.

## Contract

- must wrap every provider in a [client](../../constructs/behavior/client.md) speaking the provider's model.
- must place the app-facing abstraction in a [broker](../../constructs/behavior/broker.md) speaking ours.
- must bind transport resilience — retry, timeout, circuit breaking — to the client.
- must leave degradation to the broker: what the app does once the retries are exhausted is its call.
- must not hard-code a base URL or a credential; both arrive as [settings](../../components/settings.md).

---

## Broker and client

A broker usually sits on top of a client, and neither owns the other. The seam between them is model translation.

| | `Broker` | `Client` |
|---|---|---|
| Speaks | our model | the provider's model |
| Names | a capability — `ChargeAsync` | an endpoint — `PostPaymentIntentAsync` |
| Owns | caching, degradation, translation | URLs, DTOs, headers, transport resilience |
| Swappable | the provider behind it | never — it *is* one provider |

- must leave the client's models, URLs, headers and wire shape to the client.
- must leave the broker's caching, degradation and vocabulary to the broker.
- may call a client method to feed the broker's own policy — reading a TTL off a response is the broker deciding.
- a broker with no client under it is legal; an in-process vendor SDK needs no HTTP wrapper.

---

## Degradation

Retry, timeout and circuit breaking are transport facts, so they bind to the client. What the app does once the
retries are exhausted is a different decision, and it is ours.

- must place the degradation policy on the broker — stale cache, an empty result, or a surfaced failure.
- must not hand-roll a retry inside a broker; that is the client's pipeline leaking upward, multiplying attempts.

---

## Open

Deliberately unwritten; decide against a second real broker rather than inventing now.

- class shape — constructor-injection depth, and whether a broker may hold state.
- lifetime — scoped versus singleton, and what that implies for its cache.
- configuration — whether a broker binds its own settings section or reads the client's.

---

## Providers

| Provider | Reaches the system through | Docs |
|---|---|---|
| HTTP | `IHttpClientFactory`, the SDK resilience pipeline, Refit | [http](http/http.md) |
| child process | the be sdk's `IProcessClient` | [process](process/process.md) |
| vendor SDK | the vendor's own client type and its own knobs | — |

- must give a vendor-SDK client the same transport guarantee through that SDK's knobs.
