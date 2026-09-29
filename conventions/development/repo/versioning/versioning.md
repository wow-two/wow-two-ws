# Versioning

*Last updated: 2026-09-29*

> Where a product's version is declared, how builds stamp it, and how running services and apps report it.
> Purpose — one version answers "what is running" in the API, the UI, the database history and the image tag.
> Use case — starting a version, wiring a new service or app, or reading what a deployment runs.

## Source

- must use the product version `X.Y.Z`: `X.Y` is the active version doc
  ([version track](../../../planning/version-track/version-track.md)); CI assigns `Z` to each release from `main`,
  so nobody bumps a patch by hand.
- must take `X.Y` from the newest `engineering/planning/version-track/v{X.Y}/` folder, `0.0` before `v0.1`;
  opening a version doc is the bump, so nothing else declares the product version.
- must bump `Y` per version doc and `X` only at `Y = 100` or a breaking change (version track rule).
- must let CI inject `X.Y.Z` into every build (build argument `APP_VERSION` → `-p:Version` and the SPA's
  `__APP_VERSION__`); a local build reports `dev`.
- must keep `Directory.Build.props` and `package.json` free of the product version; a `0.0.0` placeholder is fine.
- must let the build append the commit to the informational version (`X.Y.Z+<commit>`); never hand-edit it.

---

## Reporting

- must report the running version from each backend service — the status endpoint returns the informational version.
- must inject the frontend version at build time (`define: { __APP_VERSION__ }` from `package.json`).
- must show every frontend's app version at the top of the app, beside its name in the top bar.
- must show each backend service's version, with its commit, in the account menu or a settings About section.
- must stamp applied migrations with the product version (`MigrationOptions.Version`).

---

## Releases

- must release from `main` only: CI tags `vX.Y.Z` and names the changed images `X.Y.Z`
  ([repo structure](../structure/repo-structure.md) § *Image publishing*).
- must version a `dev`, `test` or other branch build as a pre-release of the next patch (`X.Y.(Z+1)-<branch>.<n>`);
  environments never appear in a version.
- must keep a service's last-changed version in a multi-service product
  ([deploy descriptor](../../../deployment/descriptor/deploy-descriptor.md) § *Builds and versions*).
