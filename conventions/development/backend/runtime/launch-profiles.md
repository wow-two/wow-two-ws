# Backend — Launch Profiles

*Last updated: 2026-06-19*

> ASP.NET Core run configuration; ports tracked in [ports.md](../../repo/ports.md). Dev runs HTTPS (TLS is terminated upstream in prod) so `Secure` cookies + secure-context behaviour match prod.

## `launchSettings.json`

- must declare a **single `https` profile** — no separate `http` profile
- must bind two URLs in `applicationUrl`, HTTPS first - `"https://localhost:{even};http://localhost:{even+1}"`
- must use the allocated **even** port for HTTPS, the adjacent **odd** port for HTTP
- must allocate the next free even port from [ports.md](../../repo/ports.md) - never reuse one across projects
- must set `ASPNETCORE_ENVIRONMENT` to `Development`
- must trust the dev cert once per machine - `dotnet dev-certs https --trust`
- the Vite dev server proxies `/api` to the even (HTTPS) port with `secure: false` - see [state-and-data.md](../../frontend/state-and-data.md)

### Example

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
