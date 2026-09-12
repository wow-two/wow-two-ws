# Models

*Last updated: 2026-09-10*

> The application's own representation of a thing — what a service or handler hands back, inside a `Result`.
> Purpose — a wire shape reaching inward makes a response change ripple into services; the model stops it.
> Use case — every service and handler return value; the edge maps it to a [dto](dto.md).

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
- must declare `{ get; init; }` — a model is built at the point it is returned.
- must carry entities, value objects, primitives or other models — never a [dto](dto.md).

### Type name
- must suffix with `Model`, noun-first — `CodeModel`, `BillingStatusModel`.
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
