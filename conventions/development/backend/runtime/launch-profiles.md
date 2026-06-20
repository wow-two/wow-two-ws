# Backend — Launch Profiles

*Last updated: 2026-06-19*

> ASP.NET Core run configuration. Allocated ports are tracked in [../repo/ports.md](../repo/ports.md).

## `launchSettings.json`

Every API project's `Properties/launchSettings.json` has a **single `https` profile** binding **two** URLs — the **HTTPS** port first, the **HTTP** port second.

- **Port pairing:** HTTPS on the service's allocated **even** port, HTTP on the adjacent **odd** port (`even`, then `even + 1`). Pick the next free even port from [../repo/ports.md](../repo/ports.md); never reuse a port across projects.
- **HTTPS in dev:** one-time `dotnet dev-certs https --trust`. The Vite dev server proxies `/api` to the backend's **HTTPS** (even) port with `secure: false` (self-signed dev cert) — see [../../frontend/state-and-data.md](../../frontend/state-and-data.md).
- TLS is terminated **upstream** in prod (Cloudflare / reverse proxy); dev mirrors prod over HTTPS so `Secure` cookies + secure-context behaviour stay consistent.

```json
{
  "$schema": "https://json.schemastore.org/launchsettings.json",
  "profiles": {
    "https": {
      "commandName": "Project",
      "dotnetRunMessages": true,
      "launchBrowser": false,
      "applicationUrl": "https://localhost:8220;http://localhost:8221",
      "environmentVariables": { "ASPNETCORE_ENVIRONMENT": "Development" }
    }
  }
}
```
