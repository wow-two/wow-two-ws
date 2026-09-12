# Settings

*Last updated: 2026-09-10*

> The record a configuration section binds into — one typed shape per section.
> Purpose — configuration read as strings fails at the point of use; bound as a record it fails at boot.
> Use case — any value that differs per environment or per deployment.

## Location

### Folder
- must sit in a `Settings/` folder under the layer that reads it, in a service →
  [architecture](../../../../shapes/service/architecture/architecture.md) § *Where a folder is created*.
- must sit beside the `Add*` extension that reads it, in a library, where no layer split exists →
  [options](options.md) § *Location*.
- the two differ because a service exiles its `Add*` methods to `Api/Configurations/`, and a record the
  Application layer reads cannot follow one across that boundary.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Holds**, and name the section it binds.
- must state the section key when the type name does not give it away.

```csharp
// ✅ names the section
/// <summary>Holds the Postgres connection settings.</summary>
// ❌ describes the mechanism instead of the section
/// <summary>Settings bound from appsettings.</summary>
```

### Construct
- declaration baseline → [data](data.md) § *Shared rules*.
- must declare `{ get; init; }` — the binder writes once, at startup.
- defaults → [constructs](../constructs.md) § *`Settings` vs `Options`*.
- must not rely on `required` alone to fail a boot — the binder leaves a `required` member `null` instead of
  throwing, so only validation catches an absent value.

### Type name
- must suffix with `Settings` — `PostgresSettings`, `GoogleAuthSettings`.
- must name the section, never the consumer — no `CodeServiceSettings` for a shared section.

---

## Neighbours

- [settings](../../components/settings.md) — binding, validation, and where the section is registered
