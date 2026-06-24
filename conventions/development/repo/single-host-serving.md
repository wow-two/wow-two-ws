# Single-Host Serving

*Last updated: 2026-06-21*

> **What** — a single-service product app ships as ONE deployable: the backend serves the built SPA from its `wwwroot`; the frontend has no host of its own.
> **Purpose** — one image, one origin → no CORS, no second deploy, and the API always serves the SPA build it shipped with.
> **Use case** — every single-service product repo (drydock, smart-qr, secrets-vault). Reach for a split deploy only when the SPA needs its own CDN / origin.

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

- `emptyOutDir: true` — vite content-hashes asset filenames; clear stale bundles each build so `wwwroot` only holds the current set.
- the relative `outDir` mirrors the SPA→`wwwroot` deploy path in `repo-structure.md` §10 — keep both in sync on any folder rename.

---

## Backend serving

- wire in the host pipeline (full pipeline → `backend/architecture/host-configuration.md`), in this **normative order**:

```csharp
app.UseDefaultFiles();      // / → /index.html
app.UseStaticFiles();       // serve wwwroot assets
// unknown /api/* stays a JSON 404 — MUST precede the SPA fallback
app.MapFallback("/api/{**slug}", () => Results.Problem(statusCode: StatusCodes.Status404NotFound, title: "Not Found"));
app.MapFallbackToFile("index.html");   // every other path → SPA shell (client-side routing)
```

- order matters: static files → `/api/*` 404 fallback → SPA file fallback. Swap the two fallbacks and an unknown `/api/*` returns `index.html` (200) instead of a 404.
- the SPA shell is public — keep `UseStaticFiles` + the fallbacks reachable by anonymous requests (ahead of any default-deny gate).

---

## Build chain — `BuildSpa` target

- add to the API `.csproj` so `dotnet build` / `dotnet publish` always bakes the latest SPA:

```xml
<PropertyGroup>
  <SpaRoot>$(MSBuildProjectDirectory)\..\..\{slug}.frontend-services\</SpaRoot>
</PropertyGroup>
<ItemGroup>
  <SpaInputs Include="$(SpaRoot)src\**\*;$(SpaRoot)index.html;$(SpaRoot)package.json;$(SpaRoot)vite.config.ts" />
</ItemGroup>
<Target Name="BuildSpa" BeforeTargets="Build"
        Inputs="@(SpaInputs)" Outputs="$(MSBuildProjectDirectory)\wwwroot\index.html">
  <Exec Command="pnpm install --frozen-lockfile" WorkingDirectory="$(SpaRoot)" Condition="!Exists('$(SpaRoot)node_modules')" />
  <Exec Command="pnpm build" WorkingDirectory="$(SpaRoot)" />
</Target>
```

- **incremental** — `Inputs`/`Outputs` skip the target unless a SPA source is newer than `wwwroot/index.html`, so it's ~free on backend-only rebuilds; `vite` always rewrites `index.html`, a valid sentinel.
- **`pnpm` must be on PATH** of the build host (local + CI-on-host).
- **Docker** — the .NET SDK build stage has no node: build the SPA in a separate node stage and `COPY` it into `wwwroot`, **or** disable the target in-image (gate the `Target` `Condition` on a `-p:BuildSpa=false` property). Never run `pnpm` inside the .NET SDK image.
- `wwwroot/` is a build artifact → **gitignore it**.

---

## Dev — proxy, not a second origin

- run the Vite dev server (HMR) and proxy the API so dev is same-origin too — no CORS, no `wwwroot` rebuild loop:

```ts
server: { proxy: { "/api": { target: "https://localhost:{evenPort}", changeOrigin: false, secure: false } } }
```

- `secure: false` accepts the .NET self-signed dev cert; the SPA calls relative `/api/*` (no `API_BASE`), so the browser sees one origin in both dev and prod.

---

## CORS posture

- single-host ⇒ same-origin in dev (proxy) **and** prod (`wwwroot`) ⇒ **no CORS** — do not wire `UseCors`.
- split deploy (SPA on its own origin) ⇒ the SDK credentialed policy `AddCredentialedCorsPolicy(origins)` (cookie auth needs `AllowCredentials` + explicit origins; the non-credentialed `AddDefaultCorsPolicy` won't carry the auth cookie).
- image packaging + deploy unit → `repo-structure.md` §8.
