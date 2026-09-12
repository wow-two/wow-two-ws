# Validators

*Last updated: 2026-09-10*

> The type that decides whether one caller-supplied shape is well-formed.
> Purpose — a named type per validated concept, so a rule has one home and a caller has one thing to run.
> Use case — any external input; an internal precondition is a guard →
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
- must start with **Validates**, and name the shape it checks.
- must not enumerate the rules — they change without the contract changing.

```csharp
// ✅ names what it validates
/// <summary>Validates the Wi-Fi content of a code.</summary>
// ❌ lists rules, so the doc goes stale on the first added rule
/// <summary>Validates that the SSID is present and the password is at least 8 characters.</summary>
```

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.
- must be `public` and derive from `AbstractValidator<T>`, with no SDK base class.
- input phases, lookup boundaries and placement → [validation](../../domains/validation/validation.md).

### Type name
- must suffix with `Validator`, named for the **concept** — `WifiContentValidator`.
- must carry the full type name only when a concept has several models across layers.
- consumption and the `Validate` / `ValidateAndThrow` bridge →
  [validation](../../domains/validation/validation.md) § *Consume*.
- must not inherit a model's role suffix; renaming `ProductEntity` must not force a validator rename.

```csharp
// ✅ one wifi-content model, so the concept names it
public sealed class WifiContentValidator : AbstractValidator<WifiContentValueObject>
// ❌ drags the model's role suffix in for no added information
public sealed class WifiContentValueObjectValidator : AbstractValidator<WifiContentValueObject>
```
