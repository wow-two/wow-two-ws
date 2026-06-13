# Backend — Launch Profiles & `.http`

*Last updated: 2026-06-12*

> ASP.NET Core run configuration. Allocated ports are tracked in [../repo/ports.md](../repo/ports.md).

## `launchSettings.json`

Every API project's `Properties/launchSettings.json` has a **single `http` profile** — no `https`.

- **No TLS in dev.** Skips the dev-cert dance — `dotnet run` / IDE Run / `curl` all work on first click on any machine, and `ASPNETCORE_URLS` overrides cleanly.
- Bind the project's allocated **even** port over HTTP (the canonical service port). One URL, `http` scheme.
- TLS is terminated **upstream** in prod (Cloudflare / reverse proxy), so app-level HTTPS buys nothing — dev mirrors that.
- Pick the next free port from [../repo/ports.md](../repo/ports.md); never reuse a port across projects.

```json
{
  "$schema": "https://json.schemastore.org/launchsettings.json",
  "profiles": {
    "http": {
      "commandName": "Project",
      "dotnetRunMessages": true,
      "launchBrowser": false,
      "applicationUrl": "http://localhost:8220",
      "environmentVariables": { "ASPNETCORE_ENVIRONMENT": "Development" }
    }
  }
}
```

## `.http` files (Rider HTTP Client)

- One `{ProjectName}.http` at the project root next to `Program.cs` (Rider auto-discovers it).
- Declare `@host = http://localhost:{port}` at the top — the fallback default so Run works on first click. Reference as `{{host}}`; never bake the scheme into a URL line.
- Reusable headers once: `@contentType = application/json` → `{{contentType}}`.
- No `http-client.env.json` for single-env POCs — add only with ≥2 real environments.
- Reference example: `…/10x-ven-haven/engineering/codebase/haven.backend-services/Haven.Channels.Supply/Requests/listings.http`.
