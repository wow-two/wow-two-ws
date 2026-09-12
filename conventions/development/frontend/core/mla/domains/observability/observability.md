# Observability

*Last updated: 2026-09-10*

> What the app records locally, and where a record lands — level, bound context, redaction, and the sink seam.
> Purpose — a logger is called from error paths, so a failure raised out of one masks the error it was recording.
> Use case — correlating lines under one id, adding a destination, or keeping secrets off a shipped record.

## The contract

- must never throw — nothing here may mask the error that put the caller in the catch block.
- must invoke a sink in isolation and route its failure to the error handler.
- must treat a context as hostile — a throwing getter, a proxy trap, a cycle or pathological depth becomes a marker.
- must mask `password` / `token` / `secret` / `authorization` / `apiKey` at any depth, case-insensitively.
- must redact on the way in, before any sink sees the record — the rule is written once, not once per sink.
- must check the level threshold before any formatting cost, so a debug call may stay in a hot path.
- must serialize an error once, since a bare error stringifies to an empty object.
- must let a child logger bind a context, children nesting and the nearer scope winning a key conflict.
- must build a record carrying level, message, timestamp, context and the serialized error.
- must inherit opt-in registration from [domain lifetime](../domains.md#lifetime).
- must keep this seam local; a product event and a user-visible notice are separate capabilities, not sinks.

---

## Providers

| Provider | Implements | Reach for it when |
|---|---|---|
| console | prints a record through the matching console method | local development, as an opt-in dev sink |
| memory | retains every record for assertion | tests — asserting what was logged and what was masked |
| any sink | the sink seam over a transport | shipping records off the device; the transport is app-side |

---

```txt
✅ createLogger({ sinks: [consoleLogSink()] })     output is opt-in; no sinks is a no-op
✅ log.child({ requestId }).error('save failed')   the id rides every line under it
❌ console.error('save failed', { apiKey })        an unmasked secret, and no threshold
```

---

## Neighbours

- [domains](../domains.md) — the shape every domain follows
- [analytics](../analytics/analytics.md) — product events, consent-gated and vendor-bound
- [feedback](../feedback/feedback.md) — the user-visible half of reporting a failure
- [data](../data/state-and-data.md) — the error type a record most often carries

---

## Payloads

- must follow [security](../security/security.md#data) for free-text redaction and personal data.
- must bound serialized depth, size and retained records so hostile payloads cannot exhaust the logger.
