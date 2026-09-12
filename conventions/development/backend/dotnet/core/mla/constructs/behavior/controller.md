# Controllers

*Last updated: 2026-09-10*

> The HTTP delivery surface for one resource — a thin dispatcher, holding no logic of its own.
> Purpose — the edge binds, maps and returns; everything it would otherwise decide belongs behind the mediator.
> Use case — exposing a resource over HTTP; the action's own rules are the [api domain's](../../domains/api/api.md).

## Location

### Folder
- must sit in a `Controllers/` folder under the domain it exposes.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Exposes**, name the resource, and end at `over HTTP` — a controller manages nothing.
- must apply the same starter to a non-resource controller — status, health.
- must spill no detail: not who calls the endpoints, not whether a sibling controller exists.

```csharp
// ✅ names the resource and stops
/// <summary>Exposes portfolio products over HTTP.</summary>
// ❌ spills who consumes it, which changes without the controller changing
/// <summary>Controller that exposes all product endpoints used by the dashboard and the public API.</summary>
```

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.
- must inherit `ControllerBase`.
- must carry `[ApiController]` and a literal kebab-case `[Route("api/{noun}")]` — never the `[controller]` token.
- must inject the mediator for application work, and no service, repository or validator.

```csharp
// ✅
[ApiController]
[Route("api/products")]
public sealed class ProductsController(ISender sender) : ControllerBase
// ❌ unsealed · token route · injects a repository instead of dispatching
[Route("api/[controller]")]
public class ProductsController(IProductRepository repository) : ControllerBase
```

### Type name
- must suffix with `Controller`, prefixed by a plural resource or process noun — `ProductsController`.
