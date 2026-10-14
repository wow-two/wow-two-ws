# Environment files

*Last updated: 2026-10-14*

> How per-environment files on a host or in a repo are named: settings, targets, identity inputs.

## Naming

- must name an environment-specific file `{name}-{environment}.{ext}`: `console-dev.json`, `console-prod.json`,
  `wheelhouse-dev.json`.
- must not give any environment the unsuffixed name; no file stands for a default environment.
- may keep an unsuffixed name only for a file every environment shares unchanged.

---

## Content

- must make each environment's file complete on its own; one file never overrides another.
- must keep dev, test and prod files side by side in the same folder, under the same name stem.
