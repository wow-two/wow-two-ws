# Frontend workspace

*Last updated: 2026-09-26*

> Product frontend projects, shared packages and their stable build roots.

## Layout

- must create a pnpm workspace at `engineering/codebase/{slug}.frontend-services/` from the first app.
- must place the initial product app at `apps/web/`.
- must add another app beside it at `apps/{app}/`, using a lowercase kebab-case name.
- must keep each app's five-layer source tree inside its own `src/` → [architecture](architecture.md).
- must place repo-shared packages at `packages/{package}/` → [extraction boundaries](boundaries.md#packaging).
- may omit `packages/` until a shared package exists; the workspace glob remains declared.
- must keep app source out of the workspace root.

```text
{slug}.frontend-services/
  package.json
  pnpm-workspace.yaml
  pnpm-lock.yaml
  scripts/                 shared build and deployment orchestration
  apps/
    web/
      package.json
      index.html
      vite.config.ts
      tsconfig*.json
      src/
      tests/               when tests are separate from source
      public/              when public assets exist
      dist/                generated app artifact
  packages/                optional shared packages
    {package}/
      package.json
      src/
      tests/
```

---

## Ownership

- must keep the workspace root private and pin its pnpm version in `packageManager`.
- must declare `apps/*` and `packages/*` in the root `pnpm-workspace.yaml`.
- must keep one `pnpm-lock.yaml` at the workspace root.
- must give each app its own private manifest, dependencies, entry, Vite config and TypeScript config.
- must name app packages `@{brand}/{app}` and shared packages `@{brand}/{package}` with unique names.
- must keep app assets, environment inputs, tests and build output with their owning app.
- may share tooling configuration at the workspace root when apps explicitly extend it.
- must declare repo-local dependencies with `workspace:*` and import their public package exports.
- must keep shared packages independent of app source; one app must not import another app's source.

---

## Commands

- must run installation from the workspace root.
- must expose the initial app through root `dev`, `build` and `typecheck` scripts.
- must preserve those root commands when adding apps; name additional app commands explicitly.
- must select the app by its package name or path when invoking its scripts.
- must keep the IDE and repository verifier entrypoint at the frontend workspace root.
- must derive app artifact paths from `apps/{app}/dist`, including host-copy scripts and Docker stages.
- must include app and workspace manifests, the lockfile and consumed packages in build inputs.
- must follow [app delivery](../delivery/delivery.md) for hosting and artifact verification.

---

## Composition

- must start with one shipped app and the existing single-host serving contract.
- must treat this layout as project organization; runtime federation is a separate architectural choice.
- must define deployment, routes, session ownership and version compatibility before composing independent apps.
- must place owned cross-app runtime agreements in [HLA](../../../core/hla/hla.md).
- must retain existing app paths when adding another app or shared package.
