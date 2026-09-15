# Single-Host Serving

*Last updated: 2026-09-10*

> **What** — a single-service product app ships as ONE deployable: the backend serves the built SPA from its `wwwroot`; the frontend has no host of its own.
> **Purpose** — one image, one origin → no CORS, no second deploy, and the API always serves the SPA build it shipped with.
> **Use case** — every single-service product repo (drydock, forever-pin, secrets-vault). Reach for a split deploy only when the SPA needs its own CDN / origin.

## The three parts

- frontend `build.outDir` → the API project's `wwwroot/` — vite writes the SPA where the host serves from
- backend serves `wwwroot` statically, with an SPA fallback to `index.html`
- a `BuildSpa` MSBuild target rebuilds the SPA into `wwwroot` on every backend build — no separate "build the frontend" step

---

## Frontend build → `wwwroot`

- point vite at the API's `wwwroot` so a production build lands exactly where the host serves it:

```ts
// codebase/{slug}.frontend-services/vite.config.ts
build: {
  outDir: "../{slug}.backend-services/{Brand}.Api/wwwroot",
  emptyOutDir: true,
}
```

- must use `emptyOutDir: true` only when that output folder contains generated SPA files exclusively.
- the relative `outDir` mirrors the SPA→`wwwroot` deploy path in `repo-structure.md` §10 — keep both in sync on any folder rename.

---

## Backend serving

- wire in the host pipeline (full pipeline → [host configuration](../../development/backend/dotnet/shapes/service/platform/startup/host-configuration.md)), in this **normative order**:

```csharp
app.UseDefaultFiles();      // / → /index.html
app.UseStaticFiles();       // serve wwwroot assets
// Reserve unknown /api/* for a JSON error, not an SPA document.
app.MapFallback("/api/{**slug}", () => Results.Problem(statusCode: StatusCodes.Status404NotFound, title: "Not Found"));
app.MapFallbackToFile("index.html").AllowAnonymous();   // public SPA shell
```

- must reserve `/api/*` for API responses and verify unknown API routes return JSON errors, not the SPA document.
- must keep the SPA shell and its static assets public; API authorization remains the backend's responsibility.

---

## Build chain — `BuildSpa` target

- must set `SpaRoot` to the frontend package directory, resolved from the API project's actual location.
- must configure Vite to write only generated SPA files into the API's `wwwroot/`.
- must run the frontend build before MSBuild gathers static/publish content, including on a clean checkout.
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
         Text="SpaRoot must point to the frontend package directory." />
  <Exec Command="pnpm install --frozen-lockfile" WorkingDirectory="$(SpaRoot)" />
  <Exec Command="pnpm build" WorkingDirectory="$(SpaRoot)" />
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
- must use `publish --no-build` only for an already verified matching build; it intentionally does not regenerate the SPA.
- must serialize builds that share `wwwroot/`; concurrent builds must use isolated output directories.
- must use `-p:BuildSpa=false` only when another build stage supplies the verified SPA output.
- must build the SPA in a Node-capable container stage and copy its output into the final host artifact.
- must keep generated `wwwroot/` out of Git.


---

## Dev — proxy, not a second origin

- run the Vite dev server (HMR) and proxy the API so dev is same-origin too — no CORS, no `wwwroot` rebuild loop:

```ts
server: { proxy: { "/api": { target: "https://localhost:{evenPort}", changeOrigin: false, secure: false } } }
```

- `secure: false` accepts the .NET self-signed dev cert; the SPA calls relative `/api/*` (no `API_BASE`), so the browser sees one origin in both dev and prod.

---

## CORS posture

- must omit CORS for a same-origin app/API deployment; cookie writes still follow the backend CSRF policy.
- must use explicit allowed origins and credential support for cross-origin cookie auth; never combine credentials with a wildcard origin.
- image packaging + deploy unit → `repo-structure.md` §8.
