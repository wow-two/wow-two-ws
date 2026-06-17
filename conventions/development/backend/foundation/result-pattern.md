# Result pattern

*Last updated: 2026-06-14*

Every handler and endpoint returns `AppResult<TSuccess, TFailure>` — a discriminated union carrying a typed success **or** a typed, context-bearing failure; raw `Ok(dto)` returns are banned ecosystem-wide.

## The model — `AppResult<TSuccess, TFailure>`

- `abstract record AppResult<TSuccess, TFailure>` with a **private constructor** → the only subtypes are its two nested cases.
- Constrained: `where TSuccess : ISuccessResult`, `where TFailure : IFailureResult` — both are empty marker interfaces. The compiler refuses any payload that isn't a declared success/failure type.
- Two nested sealed cases:
  - `Success(TSuccess Data, IApplicationSuccessContext? Context = null)`
  - `Failure(TFailure Error, IApplicationFailureContext? Context = null)`
- Canonical `AppResult<,>` ships in the **SDK** — `WoW.Two.Sdk.Backend.Beta.Mediator` (`src/Mediator/Result/`). Products still hold a local `ApplicationResult` copy in `Common/Mediator/` until the pending code migration drops it for the SDK reference (see § Rename). Pairs with the mediator — [`../messaging/mediator.md`](../messaging/mediator.md) for `IQuery`/`ICommand`/dispatch.

```csharp
public abstract record AppResult<TSuccess, TFailure>
    where TSuccess : ISuccessResult
    where TFailure : IFailureResult
{
    private AppResult() { }

    public sealed record Success(TSuccess Data, IApplicationSuccessContext? Context = null) : AppResult<TSuccess, TFailure>;
    public sealed record Failure(TFailure Error, IApplicationFailureContext? Context = null) : AppResult<TSuccess, TFailure>;
}
```

---

## Why it carries more than the payload

The union deliberately holds **more than the success DTO** — that surplus is the reason raw returns are banned:

- **Typed failure** — `Failure.Error` is a domain `IFailureResult`, not a bare string/exception. Each operation's failure carries a **message + a `FailureCategory`** (the category pattern below) — a uniform, mappable shape, not per-operation ad-hoc flags. A handler that returned just the DTO would have nowhere to put a typed, mappable failure.
- **Per-side context** — `Success.Context` (`IApplicationSuccessContext`) and `Failure.Context` (`IApplicationFailureContext`) are optional, separately-typed extension slots: cache-hit metadata / pagination on success; retry-after hints / validation detail on failure. Two layers, each independently extensible, neither leaking into the other.
- **Exhaustiveness** — a closed union (private ctor + sealed cases) makes the success/failure split compiler-checked at every call site; a raw `dto` erases the failure branch entirely.

---

## The success / failure payloads

`TSuccess` / `TFailure` are **per-operation domain result containers** (the `{Domain}{Operation}Result` types), not generic. They implement the markers and hold the operation's data / error shape. Every `Failure` follows the **category pattern** — it implements the app's `I{App}Failure` (below), so it carries a `string ErrorMessage` + a `FailureCategory`, never per-operation ad-hoc flags:

```csharp
/// <summary>Outcome of fetching a single code.</summary>
public abstract record CodeGetByIdResult
{
    private CodeGetByIdResult() { }

    public sealed record Success(CodeDto Code) : CodeGetByIdResult, ISuccessResult;

    /// <summary>Category maps the HTTP status (NotFound → 404).</summary>
    public sealed record Failure(string ErrorMessage, FailureCategory Category) : CodeGetByIdResult, IAppFailure;
}
```

- `Failure` carries a **message** (`ErrorMessage`, surfaced as the ProblemDetails detail) + a **`FailureCategory`** (drives the HTTP status) — the uniform two-field shape every operation's failure shares, not a bespoke `bool NotFound` per operation.
- The container itself is the `TSuccess` / `TFailure` argument: `AppResult<CodeGetByIdResult.Success, CodeGetByIdResult.Failure>`.
- Container *file shape* (abstract-record + private ctor, nested `Success`/`Failure` cases, markers) is the §`The success / failure payloads` shape above. The request/handler layout that produces it → [`../messaging/mediator.md`](../messaging/mediator.md) (CQRS request + handler).

---

## The category pattern — uniform failure shape

Every product defines **one** failure interface + **one** category enum; every operation's `Failure` implements the interface. This replaces per-operation ad-hoc flags with a single mappable shape, and keeps the failure→HTTP map in one place.

**1. Product failure interface** — refines the SDK's empty `IFailureResult` marker with the two fields the API layer needs:

```csharp
/// <summary>Product-side failure shape every operation's Failure implements.</summary>
public interface IAppFailure : IFailureResult
{
    /// <summary>Human-readable message surfaced as the ProblemDetails detail.</summary>
    string ErrorMessage { get; }

    /// <summary>Category that drives the HTTP status code.</summary>
    FailureCategory Category { get; }
}
```

**2. `FailureCategory` enum** — the closed set of failure kinds, each mapping to one HTTP status:

```csharp
/// <summary>Categorizes a failure so the API layer can map it to an HTTP status code.</summary>
public enum FailureCategory
{
    Unexpected = 0,   // → 500
    Validation,       // → 400
    NotFound,         // → 404
    Conflict,         // → 409
    Unauthorized,     // → 401
    Forbidden         // → 403
}
```

**3. Product-side `ApiResults.ToStatusCode`** — the single app-side category→status map (lives in the `Api` project):

```csharp
/// <summary>Maps a failure category to an HTTP status code — the single app-side error→status map.</summary>
internal static class ApiResults
{
    public static int ToStatusCode(FailureCategory category) => category switch
    {
        FailureCategory.Validation   => StatusCodes.Status400BadRequest,
        FailureCategory.NotFound     => StatusCodes.Status404NotFound,
        FailureCategory.Conflict     => StatusCodes.Status409Conflict,
        FailureCategory.Unauthorized => StatusCodes.Status401Unauthorized,
        FailureCategory.Forbidden    => StatusCodes.Status403Forbidden,
        _                            => StatusCodes.Status500InternalServerError
    };
}
```

- **Stays product-side.** The SDK `IFailureResult` remains an **empty marker** — the `Category` lives on the product's `I{App}Failure`, never the SDK. Each app implements its own `I{App}Failure` + `FailureCategory`; drydock's `IDrydockFailure` / `FailureCategory` is the reference implementation.
- Naming: `I{App}Failure` per app (`IDrydockFailure`, `ISmartQrFailure`, …); the enum is plain `FailureCategory`.
- **Future option:** the cross-app DRY-lift of `FailureCategory` + the `ToStatusCode` map into the SDK is a possible later move — deferred while it stays product-side and each app owns its own copy.

---

## Construction — Success vs Failure

A handler `new`s the case directly (no factory layer) and wraps the domain container:

```csharp
// success
return new AppResult<CodeGetByIdResult.Success, CodeGetByIdResult.Failure>
    .Success(new CodeGetByIdResult.Success(code.ToDto()));

// failure — typed, with the category the controller maps on
return new AppResult<CodeGetByIdResult.Success, CodeGetByIdResult.Failure>
    .Failure(new CodeGetByIdResult.Failure("Code not found", FailureCategory.NotFound));
```

- A void-ish command still returns `AppResult<…>` with a `Success` payload (which may be empty) — **never** bare `Unit`, `Task`, or a naked DTO.
- `Context` is optional; pass it only when the success/failure side has metadata to surface.

---

## Consumption — `.Match(onSuccess, onFailure)`

Controllers collapse the union with `.Match` — the mandated mapping path; the controller stays a thin dispatcher with no `if`/`switch` over the cases:

```csharp
[HttpGet("{id:guid}")]
public async Task<IActionResult> GetById(Guid id, CancellationToken ct) =>
    (await sender.Send(new CodeGetByIdQuery { Id = id, UserId = userId }, ct)).Match<IActionResult>(
        onSuccess: ok => Ok(ApiResponse<CodeDto>.Ok(ok.Data.Code)),
        onFailure: fail => Problem(detail: fail.Error.ErrorMessage, statusCode: ApiResults.ToStatusCode(fail.Error.Category)));
```

- `Match<TOut>(onSuccess, onFailure)` — one explicit type arg (`TOut`); `TSuccess`/`TFailure` infer from the receiver. Returns one value from both branches — success → `Ok`/`Created`/`NoContent`; failure → always `Problem`, the status mapped by `ApiResults.ToStatusCode(fail.Error.Category)` off the failure's `FailureCategory` (e.g. `NotFound` → 404). The controller never inlines a status literal or a bare `NotFound()`/`Conflict()` — see [`../presentation/controllers.md`](../presentation/controllers.md).
- Each arm receives the **case object**, not a deconstructed payload — success arm gets the `.Success` case (reach `.Data` / `.Context`), failure arm gets the `.Failure` case (reach `.Error` / `.Context`).
- `.Match` ships in the SDK — `AppResultExtensions.Match` (`src/Mediator/Result/`), two overloads: a case-object success arm (`Func<AppResult<…>.Success, TOut>`) and a no-arg success arm (`Func<TOut>`), each paired with a `Func<AppResult<…>.Failure, TOut>` failure arm. Products consume via the SDK once they reference it; the local-copy repos switch over from raw `switch`/`is` as part of the migration below.
- See [`../presentation/controllers.md`](../presentation/controllers.md) for the controller shape and [`../messaging/mediator.md`](../messaging/mediator.md) for the `ISender.Send` dispatch it sits on.

---

## The rule — enforced on every handler & endpoint

| Rule | Statement |
|---|---|
| **Return type** | Every `IQueryHandler` / `ICommandHandler` returns `AppResult<TSuccess, TFailure>`. Every controller action maps one. |
| **No raw success** | `Ok(dto)`, `return dto`, `return Unit.Value` from a handler are **banned** — the typed failure + context must always be expressible. |
| **Typed failure** | Failures travel as the operation's `IFailureResult` — concretely the app's `I{App}Failure` (`ErrorMessage` + `FailureCategory`), never a thrown exception, bare string, or per-op ad-hoc flag crossing the boundary. |
| **Map, don't branch** | Controllers call `.Match` (products still on the local copy: exhaustive `switch`/`is` until they reference the SDK) — no business logic, no `try/catch` (errors → [`../presentation/problem-details.md`](../presentation/problem-details.md)). |

Rationale: a uniform union means the failure path is **always typed and mappable**, context rides alongside the payload without polluting it, and the success/failure split is compiler-enforced at every seam — none of which a raw `Ok(dto)` can guarantee.

---

## Migration — products → SDK `AppResult`

The canonical union ships as **`AppResult<TSuccess, TFailure>`** in the SDK (`WoW.Two.Sdk.Backend.Beta.Mediator`). Products still carry a local `ApplicationResult<TSuccess, TFailure>` in `Common/Mediator/` — the pending code migration deletes that copy and repoints products at the SDK type (and only the carrier moves — markers and context interfaces keep their names). This doc already uses the target name `AppResult`; until a product migrates, its local symbol is `ApplicationResult` with the same shape.

---

## Naming

| Type | Name |
|---|---|
| Union carrier | `AppResult<TSuccess, TFailure>` |
| Nested cases | `AppResult<,>.Success` · `AppResult<,>.Failure` |
| Success / failure markers | `ISuccessResult` · `IFailureResult` (SDK, both empty) |
| Context markers | `IApplicationSuccessContext` · `IApplicationFailureContext` |
| Per-operation container | `{Domain}{Operation}Result` (e.g. `CodeGetByIdResult`, `ChannelGetAllResult`) |
| Product failure interface | `I{App}Failure` (e.g. `IDrydockFailure`) — `ErrorMessage` + `Category` |
| Failure category enum | `FailureCategory` (`Unexpected`/`Validation`/`NotFound`/`Conflict`/`Unauthorized`/`Forbidden`) |
| Category→status map | `ApiResults.ToStatusCode(FailureCategory)` (product `Api` project) |
