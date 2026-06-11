# Backend — Launch Profiles & `.http`

*Last updated: 2026-06-10*

> ASP.NET Core run configuration. Allocated ports are tracked in [../repo/ports.md](../repo/ports.md).

## `launchSettings.json`

Every API project's `Properties/launchSettings.json` has **both** an `http` and an `https` profile:

- **HTTPS** → **even** port (the "first" port).
- **HTTP** → **odd** port = HTTPS + 1 (adjacent).
- The `https` profile binds **both** URLs (semicolon-separated) so HTTPS-launched runs still answer HTTP; the `http` profile binds only the HTTP URL.
- Pick the next free even port from [../repo/ports.md](../repo/ports.md); never reuse a port across projects.

```json
{
  "profiles": {
    "http":  { "commandName": "Project", "dotnetRunMessages": true,
               "applicationUrl": "http://localhost:5099",
               "environmentVariables": { "ASPNETCORE_ENVIRONMENT": "Development" } },
    "https": { "commandName": "Project", "dotnetRunMessages": true,
               "applicationUrl": "https://localhost:5098;http://localhost:5099",
               "environmentVariables": { "ASPNETCORE_ENVIRONMENT": "Development" } }
  }
}
```

## `.http` files (Rider HTTP Client)

- One `{ProjectName}.http` at the project root next to `Program.cs` (Rider auto-discovers it).
- Declare `@host = https://localhost:{even-port}` at the top — the fallback default so Run works on first click. Reference as `{{host}}`; never bake the scheme into a URL line.
- Reusable headers once: `@contentType = application/json` → `{{contentType}}`.
- No `http-client.env.json` for single-env POCs — add only with ≥2 real environments.
- Reference example: `…/10x-ven-haven/engineering/codebase/backend-services/Haven.Channels.Supply/Requests/listings.http`.
