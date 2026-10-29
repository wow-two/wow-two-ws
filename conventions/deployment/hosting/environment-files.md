# Environment files

*Last updated: 2026-10-19*

> How per-environment files are named and filled: a .NET service's settings in its repo, and every other file,
> such as host targets and identity inputs.

## Settings

- must keep a .NET service's non-secret defaults in its repo's `appsettings.json`.
- must put environment-specific defaults in `appsettings.Development.json` and `appsettings.Production.json`.
- must run the `dev` environment as ASP.NET Core `Development` and `prod` as `Production`; the deploy descriptor's
  `dotnetEnvironment` turns it on ([deploy descriptor](../descriptor/deploy-descriptor.md) § *Rules*).
- must keep `appsettings.Development.json` fit for deployed dev: no loopback address, local path or local switch.
- must keep machine-local settings in `appsettings.Local.json` beside `appsettings.json`: gitignored, excluded
  from every image build context, read only by a local run
  ([host configuration](../../development/backend/dotnet/shapes/service/platform/startup/host-configuration.md) § *Settings files*).
- must let a deployed target's settings file mount as `appsettings.Target.json`, the pipelines default from v0.7.0;
  never commit one or copy it into an image.
- must keep `appsettings.Target.json` and the retired `appsettings.Machine.json` gitignored and out of every image
  build context too, so a stray copy never leaks.
- must take every deployed override from an environment variable or Wheelhouse's vault; the repo holds defaults only.
- must enter a deployed override in the Wheelhouse console: a non-secret value under Settings, a secret under Secrets.
- must keep secret values out of the repo ([secrets](../../security/secrets/secrets.md) § *Repository content*).
- must declare a service's required settings in its
  [deploy descriptor](../descriptor/deploy-descriptor.md) § *Rules*.

---

## Naming

- must name every other environment-specific file `{name}-{environment}.{ext}`: `console-dev.json`,
  `console-prod.json`, `wheelhouse-dev.json`.
- must not give any environment the unsuffixed name; no file stands for a default environment.
- may keep an unsuffixed name only for a file every environment shares unchanged.

---

## Content

- must make each such environment file complete on its own; one file never overrides another.
- must keep the dev and prod files side by side in the same folder, under the same name stem.
