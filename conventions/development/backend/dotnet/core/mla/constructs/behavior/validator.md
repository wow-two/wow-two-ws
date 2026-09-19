# Validators

*Last updated: 2026-09-15*

> Checks supplied data against rules and reports validity or failures.
> Purpose — a named type per validated concept, so a rule has one home and a caller has one thing to run.
> Use case — input constraints or domain integrity checks; programmer preconditions use guards →
> [validation](../../domains/validation/validation.md).

## Location

### Folder
- must sit in a `Validators/` folder under the subdomain whose type it checks.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a concrete implementation with **Validates**, naming the shape it checks.
- interface starter → [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.
- must not enumerate the rules — they change without the contract changing.

```csharp
// ✅ names what it validates
/// <summary>Validates the Wi-Fi content of a code.</summary>
// ❌ lists rules, so the doc goes stale on the first added rule
/// <summary>Validates that the SSID is present and the password is at least 8 characters.</summary>
```

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.
- must select the validation contract for the kind of result its callers need.
- input and field validation uses the [FluentValidation integration](../../domains/validation/fluentvalidation/fluentvalidation.md).
- may implement a domain-specific contract for integrity checks with structured domain results.
- must not require `AbstractValidator<T>` solely because a type has the `Validator` suffix.
- input phases, lookup boundaries and placement → [validation](../../domains/validation/validation.md).

### Type name
- must suffix with `Validator`, named for the **concept** — `WifiContentValidator`.
- must carry the full type name only when a concept has several models across layers.
- input-validation consumption and the `Validate` / `ValidateAndThrow` bridge →
  [validation](../../domains/validation/validation.md) § *Consumption*.
- must not inherit a model's role suffix; renaming `ProductEntity` must not force a validator rename.

```csharp
// ✅ one wifi-content model, so the concept names it
public sealed class WifiContentValidator : AbstractValidator<WifiContentValueObject>
// ❌ drags the model's role suffix in for no added information
public sealed class WifiContentValueObjectValidator : AbstractValidator<WifiContentValueObject>
```

---

## Content

- must report whether the supplied data satisfies its rules, with actionable failure details where needed.
- may validate relationships across a supplied collection, including sequence, links and hash consistency.
- must keep validation separate from repairing or persisting the data.
- must document what a successful result establishes and which assumptions remain outside the check.
- must use `Validator` for integrity checks rather than introducing a separate `Verifier` role.
- identity establishment from evidence → [authenticators](authenticator.md).
- domain result carriers → [results](../../components/result.md).
