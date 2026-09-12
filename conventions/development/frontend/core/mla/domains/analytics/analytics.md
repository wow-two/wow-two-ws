# Analytics

*Last updated: 2026-09-10*

> The product-event sink — three canonical calls in, whatever vendor an app registers out.
> Purpose — consent, super-properties, failure isolation and pre-init buffering are solved once, not per vendor.
> Use case — reporting a product event, gating reporting on consent, or plugging a vendor script in.

## The contract

- must expose exactly three calls — a named event, a user identification, and a page view.
- must fan every call out to registered sinks, and isolate a throwing or rejecting sink from the caller.
- must read the enabled gate at call time; consent and do-not-track settle after the client exists.
- must drop what is buffered when dispatch is turned off — granted consent never replays pre-consent calls.
- must buffer calls made before the first sink registers, dropping the oldest past the cap.
- must drain the buffer into the newly registered sink alone, never as history to a later one.
- must merge super-properties into event properties only, never into identification traits.
- must return an unregister from a registration, and leak nothing when it is called.
- must surface a sink failure on the error handler alone — reporting is never worth an app crash.
- must inherit registration and instance ownership from [domain lifetime](../domains.md#lifetime).
- must declare supported runtimes per entry; keep browser sink loading behind client-only actions.
- must stay separate from the local record seam and from user-visible notices.

---

## Providers

| Provider | Implements | Reach for it when |
|---|---|---|
| console | prints each call, with no network | local development, verifying a wiring |
| memory | retains every call for assertion | tests — a sink with no vendor script |
| any sink | the sink seam over a vendor SDK | production reporting; the adapter is app-side |

---

```txt
✅ analytics.register(consoleAnalyticsProvider())   explicit opt-in, returns the unregister
✅ track('signup_completed', { plan })              super-properties merge under it
❌ identify(userId, { requestId })                  request noise on a permanent profile
```

---

## Neighbours

- [domains](../domains.md) — the shape every domain follows
- [observability](../observability/observability.md) — what the app records locally, a separate seam
- [feedback](../feedback/feedback.md) — user-visible notices, never an analytics sink
- [flags](../flags/flags.md) — the variant an exposure event reports

---

## Identity

- must drop calls made while reporting is disabled; do not buffer them for later consent.
- must clear buffered calls and user-bound properties when consent is revoked or identity changes.
- must keep payloads within [security](../security/security.md#data), including page URL/query data.
