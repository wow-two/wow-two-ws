# Options

*Last updated: 2026-09-10*

> Code-supplied knobs, applied through the [options construct](../constructs/data/options.md).

## Location

- must use the construct's [location](../constructs/data/options.md#location).

---

## Declaration

- must use the construct's [declaration](../constructs/data/options.md#declaration).

---

## Content

- must name and document each member for the behavior it steers, including its unit and valid range.
- must give an omittable member a usable default.
- must not give a `required` member a default that defeats its must-supply contract.
- must keep values no caller changes in [constants](constants.md).

---

## Registration

- must take optional configuration as `Action<T>? configure = null`.
- must choose the registration by what the value needs:
  - per-call input — pass the value as an argument; do not register it
  - rule-free shared knobs — construct, invoke the delegate, `TryAddSingleton(instance)`
  - validated knobs — `AddValidatedOptions<T>(configure, validate)`
  - cross-registration composition — the options pipeline, preserving `PostConfigure` order
- must supply actual rules in the validated helper's callback; an empty callback validates no domain constraint.
- must validate the final composed value at startup when a composition has constraints.
- must expose a shared value as `T`; the registration projects `IOptions<T>.Value` when it uses that pipeline.
- must not mutate the shared value after registration or resolution.
- must take a must-supply value as an explicit registration parameter and validate the configured result.
- must not rely on `required` inside the options pipeline; it constructs the value without object-initializer checks.
- must not declare `required` on a pipeline-created type; express the obligation in its validation rules.
- must leave configuration-section binding to [settings](settings.md#registration).

```csharp
var naming = new SqlNamingOptions();
configureNaming?.Invoke(naming);
services.TryAddSingleton(naming);
```

- must use the shipped [validated registration helpers](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Options/OptionsRegistrationExtensions.cs)
  for fill/bind, validation, startup checking and projection.
