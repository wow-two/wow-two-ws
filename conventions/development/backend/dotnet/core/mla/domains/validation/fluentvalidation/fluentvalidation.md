# FluentValidation

*Last updated: 2026-09-10*

> FluentValidation rule authoring behind the SDK [validation contract](../validation.md).

## Authoring

- must inherit `AbstractValidator<T>` without another SDK base class.
- must follow [validator declaration and naming](../../../constructs/behavior/validator.md).
- must keep provider validators pure; persisted-state and transition checks follow [phase ordering](../validation.md#phases).
- must co-locate the validator with its validated concept.
- must write one `RuleFor` per rule, one chained call per line, with a blank line between rules.
- must use the provider's default message when it states the rule clearly.
- may supply a message when a format or domain constraint would otherwise be unclear.
- must use `nameof` for referenced member names.
- must extract a repeated pure check rather than repeat the same predicate across validators.
- must document nested validator dependencies outer-to-inner through `seealso` or a single branch-table remark.
- must document that extending a nested shape requires updating its validator.

---

## Registration

- must scan owning assemblies once at composition through `AddFluentValidatorsFromAssemblies`.
- must not hand-bind the SDK `IValidator<T>` or provider validator interfaces alongside that scan.
- may have multiple provider validators for one type; the adapter aggregates them.
- must use `AddMediatorValidatingInterceptor()` only when its pre-handler placement satisfies [phase ordering](../validation.md#phases).
- registration → [validation registration](../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Validation/ValidationServiceCollectionExtensions.cs).

---

## Projection

- must let `FluentValidationAdapter<T>` project rule codes and operands.
- must not hand-build `FieldError` when a provider validator already produced the failure.
- must implement `ISensitiveMembers` on validators whose operation must suppress a member's operands.
- must suppress all operands for such members, not only `PropertyValue`; lengths can disclose secret information.
- must never expose `PropertyValue` or duplicate `PropertyPath` through operands.
- must preserve provider placeholder keys; clients translate them when rendering.
- must not treat `PropertyName` as the member path when `.WithName()` supplies a display label.
- must use `.WithSeverity(Severity.Warning)` for advisory rules inside the same validator.
- projection API → [adapter source](../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Validation/FluentValidationAdapter.cs).

---

## Localization

- must map top-level messages through `IErrorMessageMapper` and field messages through `IFieldErrorMessageMapper`.
- must register custom mappers before `AddErrorHttpStatusMapping()` when overriding its `TryAdd` defaults.
- may use request-culture localization inside a rule message when code-based rendering is insufficient.
- must configure request localization before relying on `CurrentUICulture`.
- must not inject scoped localization state into a singleton mapper.
- current mapper lifetime and interfaces → [error mapping registration](../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Web/ErrorMapping/ErrorMappingServiceCollectionExtensions.cs).
