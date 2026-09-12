# Security

*Last updated: 2026-09-10*

> Frontend trust boundaries for configuration, sessions and untrusted content.

## Trust

- must treat browser configuration, bundled code, source maps and runtime globals as public.
- must keep service credentials on the server; client-side redaction does not hide a bundled secret.
- must treat client route guards, validation and flags as UX decisions; the backend authorizes every operation.
- must use text rendering for untrusted strings; trusted HTML requires an explicit sanitizer boundary.
- must validate navigation/resource URL schemes and origins for the consuming sink.
- must encode URL components; encoding does not replace protocol/origin validation.
- must avoid embedding raw JSON or error text into executable HTML/script contexts.

---

## Session

- must pair cookie-authenticated writes with the backend's CSRF contract; same-origin hosting alone is insufficient.
- must allowlist return destinations; reject external redirects unless explicitly configured.
- must keep bearer credentials out of persistent browser storage.
- must clear identity-scoped caches, drafts and telemetry identity on logout/account switch.
- must invalidate earlier session resolutions before a newer login/logout transition can be overwritten.
- must distinguish a failed session transport from proof of invalid credentials when choosing visible feedback.

---

## Data

- must persist only declared non-sensitive fields, with tenant/account namespaces where applicable.
- must treat storage contents and configuration overrides as untrusted input.
- must validate file type, size and authorization again on the server; client admission is feedback only.
- must define upload retry idempotency with the server before automatically retrying a write.
- must keep secrets and unnecessary personal data out of events, logs, URLs and errors.
- must redact structured fields before sinks run and sanitize free-text messages separately.
- must expose display-safe failures; retain diagnostic detail only in an explicitly configured trusted sink.

---

## Hosting

- must declare CSP, framing and resource-origin policy in the host's security configuration.
- must document any third-party script origin and its consent/loading lifecycle.
- must follow the [app delivery owner](../../../../shapes/app/delivery/delivery.md) for deployed assets and caching.
