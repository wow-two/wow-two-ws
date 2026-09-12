# Settings

*Last updated: 2026-09-10*

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

- helper signatures → [validated registration](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Options/OptionsRegistrationExtensions.cs).
- environment overrides → [host configuration](../../../shapes/service/platform/startup/host-configuration.md).
