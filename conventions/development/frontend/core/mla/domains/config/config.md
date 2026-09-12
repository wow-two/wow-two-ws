# Config

*Last updated: 2026-09-10*

> A typed, fail-fast read of application configuration — one declared schema resolved into one frozen object.
> Purpose — a misconfigured deploy reports every problem at startup, not one boot-crash at a time.
> Use case — declaring an app's settings, layering a runtime override over a build, or parsing env in a test.

## The contract

- must declare every key with a field spec, and infer the output type from the schema.
- must read through an ordered source list, the earlier source winning.
- must treat an empty string as absent, so an unset-but-declared key falls through to the next source.
- must coerce a non-string hit to its string form before parsing it.
- must collect every missing and every invalid key across the whole schema before reporting.
- must throw those problems together as one aggregated error at startup — config fails loud, never silently.
- must keep a secret field's raw value out of the reported issue.
- must name both the schema key and the prefixed lookup key on an issue.
- must apply a lookup prefix at read time only, so the schema key stays the output name.
- must return a frozen, fully typed object, parsed once.
- must yield an empty source rather than throw when a source is unavailable.

---

## Providers

| Provider | Implements | Reach for it when |
|---|---|---|
| `import.meta.env` | the build-time source the bundler inlines | values fixed at build; empty outside a bundler |
| `window` | a runtime global injected per environment | one built image deployed to many environments |
| static | a plain record behind the source type | tests, or values resolved somewhere else |

- must layer the runtime source ahead of the build-time one — that is the default order.

---

```txt
✅ defineConfig({ API_URL: url(), PORT: port() }, { prefix: 'VITE_' })
✅ error.issues                              every problem, reported at once
❌ import.meta.env.VITE_API_URL as string    unparsed, unchecked, typed by assertion
```

---

## Neighbours

- [domains](../domains.md) — the shape every domain follows
- [validation](../validation/validation.md) — the seam a boundary parse shares with a form
- [storage](../storage/storage.md) — the seam that degrades silently where this one fails loud
- [flags](../flags/flags.md) — per-user variation, which configuration deliberately has none of

---

## Trust

- must follow [security](../security/security.md#trust); every browser source is public.
- must use the secret marker only to redact diagnostics, never to promise confidentiality in the browser.
- must reject a malformed supplied value rather than fall through to a lower-priority valid value.
