# Humanized text formatter verification

*Last updated: 2026-09-13*

## Scope

- `ITextHumanizer` / `TextHumanizer` → `IHumanizedTextFormatter` / `HumanizedTextFormatter`.
- Both declarations moved from `Localization/Humanizing/` to `Localization/Formatters/` with matching namespaces.
- Existing `IRelativeTimeFormatter` / `RelativeTimeFormatter` moved to the same `Formatters/` folder and namespace.
- Concrete type summaries now start with `Formats`; interfaces start with `Defines`.
- Updated exact singleton registrations, namespace imports and localization documentation references.
- Moved the folder guide to `Localization/Formatters/formatters.md` and updated both guide references.
- Preserved `AddHumanizing`, formatting method names/signatures, culture handling, injected clock behavior,
  null checks, Humanizer calls and `TryAddSingleton` customization semantics.
- No new tests, package changes, staging, commits or pushes.

---

## Checks

- `dotnet build WoW.Two.Sdk.Backend.Beta.csproj --no-restore -m:1`, from SDK `src/`:
  exit 0, 37 warnings, 0 errors. Log: `/private/tmp/humanized-text-formatter-build.log`.
- Old type, namespace and folder-guide reference search under SDK `engineering/`, excluding generated output:
  no remaining references.
- `git diff --check` passed for the SDK.
- Existing test-source search found no humanizing or relative-time formatter tests; no unrelated test suite was run.

---

## Limits

This is source-reference and scoped compile verification. No direct formatter runtime test coverage or SDK release gate is claimed.
