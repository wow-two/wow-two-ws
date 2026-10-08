# Single-host serving

*Last updated: 2026-10-01*

> A single-service product ships as one deployable: the backend serves the built SPA from its `wwwroot`.
> Purpose — one image and one origin: no CORS, no second deploy, and an API that serves the SPA it shipped with.
> Use case — every single-service product repo; a split deploy only when the SPA needs its own CDN or origin.

## Parts

- must build the app into its own `apps/web/dist`
  ([frontend workspace](../../development/frontend/shapes/app/architecture/workspace.md)).
- must copy that artifact into the API project's `wwwroot/` with the workspace's `deploy` script.
- must serve `wwwroot/` from the backend, falling back to `index.html`.
- must run the build and the copy from the `BuildSpa` MSBuild target, so a backend build needs no frontend step.

---

## Frontend artifact

```ts
// {slug}.frontend-services/apps/web/vite.config.ts
build: { outDir: 'dist', emptyOutDir: true }
```

```js
// {slug}.frontend-services/scripts/deploy.mjs — run by the root `deploy` script
const source = new URL('../apps/web/dist/', import.meta.url);
const wwwroot = new URL('../../{slug}.backend-services/{Brand}.Api/wwwroot/', import.meta.url);
```

- must keep Vite's `outDir` at the app's own `dist`, so `emptyOutDir` never reaches a host folder.
- must build the app, empty `wwwroot/`, then copy `dist` into it — in that order, in `scripts/deploy.mjs`.
- must resolve both folders from the script's own location, never from the working directory.
- must stop with a non-zero exit when the build fails or `dist/index.html` is absent.
- must update both paths on a code-directory rename
  ([repo structure](../../development/repo/structure/repo-structure.md#renames)).

---

## Backend serving

- must serve the SPA through the SDK: set `ApiDefaultsOptions.SpaHosting`, and `UseApiDefaults()` wires both halves
  ([startup defaults](../../development/backend/dotnet/shapes/service/platform/startup/startup-defaults.md)).
- may call `UseSpaHosting()` ahead of the pipeline and `MapSpaFallback()` after the app's own endpoints, where
  the host has to order them itself.
- must not hand-wire `UseDefaultFiles`, `UseStaticFiles` or a fallback to `index.html`.
- must reserve `/api/*` for API responses; the SDK fallback answers an unmatched API route with a JSON 404.
- must keep the SPA shell and its static assets public; API authorization remains the backend's responsibility.
- must leave hashed assets under `/assets` to the SDK's immutable caching; every document revalidates.

```csharp
builder.AddApiDefaults(options => options.SpaHosting = _ => { });   // defaults: /api, index.html, /assets
```

---

## Build chain

- must set `SpaRoot` to the frontend workspace root, resolved from the API project's actual location.
- must run the frontend build before MSBuild gathers static and publish content, including on a clean checkout.
- must refresh the content item list after generating files that did not exist at project evaluation.
- must install with the frozen lockfile on each build invocation; an existing `node_modules` is not a freshness check.
- must keep Node and the pinned package-manager version available on the build host.

```xml
<PropertyGroup>
  <!-- Resolve this path against the actual API project location. -->
  <SpaRoot>$(MSBuildProjectDirectory)/../../{slug}.frontend-services/</SpaRoot>
</PropertyGroup>
<Target Name="BuildSpa"
        BeforeTargets="PrepareForBuild;ResolveProjectStaticWebAssets"
        Condition="'$(BuildSpa)' != 'false' and '$(DesignTimeBuild)' != 'true' and '$(NoBuild)' != 'true'">
  <Error Condition="!Exists('$(SpaRoot)package.json')"
         Text="SpaRoot must point to the frontend workspace directory." />
  <Exec Command="pnpm install --frozen-lockfile" WorkingDirectory="$(SpaRoot)" />
  <Exec Command="pnpm run deploy" WorkingDirectory="$(SpaRoot)" />
  <ItemGroup>
    <Content Remove="@(Content)"
             Condition="$([System.String]::Copy('%(Content.Identity)').Replace('\', '/').StartsWith('wwwroot/'))" />
    <Content Include="wwwroot/**/*"
             CopyToOutputDirectory="PreserveNewest"
             CopyToPublishDirectory="PreserveNewest" />
  </ItemGroup>
</Target>
```

- must run this target unconditionally by default; it has no timestamp-only `Inputs`/`Outputs` shortcut.
- may add a build cache only with a content fingerprint over the complete input set and tool versions.
- must include file paths and contents in that fingerprint, so deletions and renames invalidate the cache.
- must include source, public assets, lockfile, manifests, workspace/patch files, configuration and relevant env values.
- must verify all declared outputs still exist before using a cached build.
- must not store secret environment values in a readable cache manifest.
- must publish into a clean staging directory so removed assets cannot remain from a previous publication.
- must use `publish --no-build` only for an already verified matching build; it does not regenerate the SPA.
- must serialize builds that share `wwwroot/`; concurrent builds must use isolated output directories.
- must use `-p:BuildSpa=false` only when another build stage supplies the verified SPA output.
- must build the SPA in a Node-capable container stage and copy `apps/web/dist` into the host's `wwwroot/`.
- must keep generated `wwwroot/` out of Git.

---

## Development

- must run the Vite dev server and proxy `/api` to the backend, so dev is same-origin too
  ([dev server](../../development/frontend/shapes/app/platform/dev-server.md)).
- must call relative `/api/*` URLs; the browser sees one origin in dev and in production.

---

## CORS

- must omit CORS for a same-origin app/API deployment; cookie writes still follow the backend CSRF policy.
- must use explicit allowed origins and credential support for cross-origin cookie auth.
- must not combine credentials with a wildcard origin.
- image packaging and the deploy unit →
  [repo structure](../../development/repo/structure/repo-structure.md#deployment-files).
