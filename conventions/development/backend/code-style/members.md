# Members & bodies

*Last updated: 2026-06-14*

> What — the most-abstract class/struct member-body conventions: how a member's body is written, regardless of layer.
> Purpose — keep every body debuggable — intermediates you can save, lines you can breakpoint.
> Use case — reach for it whenever you write a method, accessor, or property body and have to choose block `{ }` vs expression `=>`.

## Bodies

- **Method bodies are block `{ }` — (almost) never expression-bodied (`=>`).** A block body lets you save intermediates to locals + set a breakpoint on any line; a one-liner `=>` has to be rewritten before you can debug it.
- **Reserve `=>` for trivial pure getters** — a property/accessor that just returns a field or a constant, with no logic: `public string Name => _name;`.
- **Any logic → block body** — a branch, a call chain, a computation, an `await`, a `match`: write it as `{ … }` even if it currently fits on one line.
- **One blank line before `return`** — separate the body's work from its result; the return reads at a glance and `result` is a clean breakpoint target.

```csharp
// ✅ trivial pure getter — expression body fine
public string Slug => _slug;

// ✅ method with logic — block body, intermediates breakpointable
public async Task<IActionResult> Get(CancellationToken ct)
{
    var result = await sender.SendAsync(new GetProductsQuery(), ct);

    return result.Match<IActionResult>(...);
}

// ❌ method as expression body — can't breakpoint or inspect the result
public async Task<IActionResult> Get(CancellationToken ct) =>
    (await sender.SendAsync(new GetProductsQuery(), ct)).Match<IActionResult>(...);
```

## See also

- [code-organization.md](code-organization.md) — one file per type, dividers, parameter + raw-string formatting
- [controllers.md](../presentation/controllers.md) — applies this rule to controller actions (block body, save the dispatch result)
- [models.md](models.md) — record style + property rules
