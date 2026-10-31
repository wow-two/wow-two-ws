# Settings

*Last updated: 2026-10-31*

> Configuration-section values, applied through the [settings construct](../constructs/data/settings.md).

## Location

- must use the construct's [location](../constructs/data/settings.md#location).

---

## Declaration

- must use the construct's [declaration](../constructs/data/settings.md#declaration).

---

## Content

- must name each member for the value it steers; binding keys follow the member names.
- must document what each value changes, its unit, and any valid range or allowed set.
- must keep values no environment changes in [constants](constants.md).

---

## Registration

- must bind domain settings in that domain's registration; host-shared settings use `AddSettings()`.
- must name the section with `nameof` or a `SectionName` constant.
- must use `AddValidatedSettings<T>(configuration, section, validate)` for owned settings with constraints.
- must state actual rules in `validate`; a startup check with no rules cannot reject missing values.
- must let the helper apply data annotations, startup validation and the projection to `T`.
- must register source-generated validation when a complex record uses `[OptionsValidator]`.
- must not read `IConfiguration` inside a consuming service.
- must use [options registration](options.md#registration) for composition and pipeline-construction constraints.

- helper signatures → [validated registration](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src/Foundation/Options/OptionsRegistrationExtensions.cs).
- environment overrides → [host configuration](../../../shapes/service/platform/startup/host-configuration.md).

---

## Stored data

Settings can change under rows written by an earlier release: a stricter password rule over stored passwords, a
removed country over stored phones (developer, 2026-10-31).

- must refuse to start on a value invalid on its own; the log names the setting, never a secret value.
- must refuse a deployed start while a setting conflicts with stored rows; log `Critical` the setting, the count and
  the resolving command.
- must apply at once a change that loosens a rule, or that only adds a step at a person's next action.
- must ship a read-only `config check` verb when settings can conflict with stored rows; exit `0` consistent, `1`
  refused, `2` failed, as `migrate`.
- must let the deploy run `config check` after `migrate` and before the restart, so a refusal leaves the old release
  serving.
- must keep on each row the settings revision it was checked against, when the check cannot re-read the value (a
  hashed password).
