# App delivery

*Last updated: 2026-09-10*

> Reproducible frontend builds and the host that serves them.

## Hosting

- must default to [single-host serving](../../../../../deployment/hosting/single-host-serving.md).
- must call same-origin APIs with relative `/api` URLs; configure the development proxy at the host boundary.
- must preserve API error responses rather than return the SPA document for unknown API routes.
- must retain the same route identity on direct hit and client navigation.
- must follow the shared host's proxy/credential policy and [frontend security](../../../core/mla/domains/security/security.md).
- must declare a separate origin/base-path contract only when the chosen deployment requires it.

---

## Build

- must pin package-manager/runtime versions and install from the lockfile in reproducible builds.
- must refresh dependencies when the lockfile changes; existing `node_modules` is not proof they match.
- must include source, public assets, lockfile, manifest, relevant env/config and build-tool files in incremental inputs.
- must rebuild when a build input changes or is removed; timestamp checks alone cannot detect every deletion.
- must keep generated output separate from authored host files before enabling output-directory cleanup.
- must derive JavaScript/CSS targets from the app's declared browser matrix.
- must include the frontend artifact in the same deployable host image when using single-host serving.

---

## Assets and caching

- must follow [assets](../platform/assets.md) for imports, URLs, images and fonts.
- must give hashed assets immutable caching and revalidate the HTML shell/config that selects them.
- must define recovery from stale chunk references across a deployment; offer reload without a retry loop.
- must not cache authenticated API data through the public static-asset policy.
- must state whether source maps are private diagnostics or intentionally public artifacts.

---

## Verification

- must verify the built artifact with its real host, including direct nested routes and unknown API routes.
- must verify base paths, asset URLs, cache headers and a fresh installation from the lockfile.
- must test representative responsive/keyboard flows under the app's supported browsers.
- must reuse [testing tiers](../../library/testing/testing.md), applying packed-consumer checks to libraries only.
