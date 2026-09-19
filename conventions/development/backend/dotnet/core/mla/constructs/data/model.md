# Models

*Last updated: 2026-09-15*

> The application's own data shape, including internal operation inputs, outputs and message wrappers.
> Purpose — a wire shape reaching inward makes a response change ripple into services; the model stops it.
> Use case — internal data shared by services and handlers; the edge maps client projections to a [dto](dto.md).

## Location

### Folder
- must sit in a `Models/` folder under the domain that produces it.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- type summary baseline → [data](data.md) § *Shared rules*.
- must name the thing it stands for.
- must not name the transport, the endpoint, or the client that eventually reads it.

```csharp
// ✅ names the thing
/// <summary>Represents a code as the application sees it.</summary>
// ❌ names the endpoint, so the type follows a route rename
/// <summary>Represents the GET /api/codes response.</summary>
```

### Construct
- declaration baseline → [data](data.md) § *Shared rules*.
- must declare `{ get; init; }` — a model is initialized before use.
- must carry entities, value objects, primitives, application messages or other models — never a [dto](dto.md).

### Type name
- must suffix with `Model`, noun-first — `CodeModel`, `BillingStatusModel`.
- must retain a wrapper's purpose before the role — `EventEnvelopeModel`, `OtpDeliveryEnvelopeModel`.
- must keep the wrapped event's `Event` role; `OrderCreatedEvent` does not become `OrderCreatedEventModel`.
- must serve every operation returning that shape; create and update share one model.
- must qualify only when one noun carries two shapes — `CodeSummaryModel` beside `CodeModel`.
- must not declare one when the operation returns an entity, a value object or a primitive.
- must reach for `Dto` instead when the type is the shape a client reads.

```csharp
// ✅ one model, several operations
public sealed record CodeModel
// ❌ a `Dto` inside a model puts the wire contract in the application layer
public sealed record CodeModel { public required StyleDto Style { get; init; } }
```
