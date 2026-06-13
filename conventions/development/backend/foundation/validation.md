# Validation

*Last updated: 2026-06-13*

Input validation runs through the SDK `IValidator<T>` seam, backed by FluentValidation and assembly-scanned at startup.

## Layers

Two distinct mechanisms — do not conflate.

| Concern | Tool | When |
|---|---|---|
| External input (DTOs, requests, commands) | `IValidator<T>` + FluentValidation | At the boundary — before the request reaches domain logic |
| Internal precondition (constructor / method args) | `Guard.Against` (Ardalis) | Inside a type that has already been constructed with trusted-but-checked args |

Validation answers *"is this caller-supplied payload well-formed?"*; guards answer *"did my own code pass a sane argument?"*. See [Guards](#guards-vs-validators).

## Author validators

Validators are FluentValidation `AbstractValidator<T>` — one per validated type, plain FluentValidation, no SDK base class:

```csharp
public sealed class CreateUserValidator : AbstractValidator<CreateUserRequest>
{
    public CreateUserValidator()
    {
        RuleFor(x => x.Email).NotEmpty().EmailAddress();
        RuleFor(x => x.Age).InclusiveBetween(13, 120);
    }
}
```

Multiple validators may target the same `T` — the adapter aggregates all of them.

## Register

Scan assemblies once at composition root via `AddFluentValidatorsFromAssemblies` — **never register `FluentValidation.IValidator<T>` directly** and never hand-bind the SDK `IValidator<T>`:

```csharp
builder.Services.AddFluentValidatorsFromAssemblies();                    // calling assembly
builder.Services.AddFluentValidatorsFromAssemblies(typeof(Program).Assembly);  // explicit
```

What the extension wires (in `ValidationServiceCollectionExtensions`):

- `AddValidatorsFromAssembly(..., includeInternalTypes: true)` — registers each `AbstractValidator<T>` as `FluentValidation.IValidator<T>`.
- `TryAddTransient(typeof(IValidator<>), typeof(FluentValidationAdapter<>))` — binds the **SDK** `IValidator<T>` to `FluentValidationAdapter<T>`, which fans out over the registered `FluentValidation.IValidator<T>[]`.

Consumers depend only on the SDK `WoW.Two.Sdk.Backend.Beta.Validation.IValidator<T>` — the FluentValidation type stays an implementation detail behind the adapter.

## Consume

`IValidator<T>` exposes two entry points; pick by call site.

### Branch on the result (no throw)

`Validate(T)` returns a `ValidationResult` — an abstract record with `Success` and `Failure(IReadOnlyList<ValidationError> Errors)` variants (`IsValid` is sugar for `this is Success`). Pattern-match it:

```csharp
switch (validator.Validate(request))
{
    case ValidationResult.Success:
        // proceed
        break;
    case ValidationResult.Failure failure:
        // failure.Errors : IReadOnlyList<ValidationError>
        break;
}
```

Each `ValidationError` is `(string Property, string Message, string Code)` — `Property` is the member path, `Code` the stable rule code (from FluentValidation `ErrorCode`).

### Throw for the pipeline

`ValidateAndThrow(T)` raises `ValidationException` (carrying `Errors`) when any rule fails — use it where a request-pipeline behavior / filter catches and translates exceptions centrally. The adapter's throw path is `Validate(...) is ValidationResult.Failure failure → throw new ValidationException(failure.Errors)`.

## Map to HTTP

Over HTTP, a validation failure becomes a `DomainError` of category Validation — map each `ValidationError` to `DomainError.Validation(code, message, detail?)` (→ `DomainErrorCategory.Validation`, `StatusCode` 400):

```csharp
ValidationError e = failure.Errors[0];
return Result<UserDto>.Fail(DomainError.Validation(e.Code, e.Message, e.Property));
```

The `Result<T>.Failure(DomainError)` then drives the response status off `DomainError.StatusCode`. See [result-pattern.md](result-pattern.md) and the Errors foundation.

## Guards vs. validators

`Guard.Against` (the Ardalis `IGuardClause` seam, re-exported with `NotSlug` / `NotUlid` wow-two extensions) is **not** a substitute for `IValidator<T>`:

- Guards throw `ArgumentException`-family exceptions for programmer-error preconditions — `Guard.Against.NullOrWhiteSpace(slug, nameof(slug))`.
- Validators produce structured, HTTP-mappable `ValidationError`s for caller-supplied input.

Do not run boundary input through `Guard.Against`, and do not model argument preconditions as `AbstractValidator<T>`.

## See also

- [result-pattern.md](result-pattern.md) — `Result<T>` success/failure containers carrying `DomainError`
- `src/Foundation/Validation/` (SDK) — `IValidator<T>`, `ValidationResult`, `ValidationError`, `ValidationException`, `FluentValidationAdapter<T>`, `AddFluentValidatorsFromAssemblies`
- `src/Foundation/Errors/DomainError.cs` (SDK) — `DomainError.Validation`, `DomainErrorCategory`
- `src/Foundation/Guards/` (SDK) — `Guard.Against`, `IGuardClause`, `NotSlug` / `NotUlid`
- [FluentValidation docs](https://docs.fluentvalidation.net/)
