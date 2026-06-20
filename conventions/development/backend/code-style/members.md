# Members & bodies

*Last updated: 2026-06-14*

> What — the most-abstract class/struct member-body conventions: how a member's body is written, regardless of layer.
> Purpose — keep every body debuggable — intermediates you can save, lines you can breakpoint.
> Use case — reach for it whenever you write a method, accessor, or property body and have to choose block `{ }` vs expression `=>`.

## Bodies

- **must use a block body `{ }`, never an expression body `=>`** — so you can save intermediates to locals + breakpoint any line (a one-liner has to be rewritten to debug)
- **Reserve `=>` for trivial pure getters** — a property/accessor that just returns a field or a constant, with no logic: `public string Name => _name;`.
- **Any logic → block body** — a branch, a call chain, a computation, an `await`, a `match`: write it as `{ … }` even if it currently fits on one line.
- **blank lines separate operations, not closely-related lines** — keep one operation's lines together (no blank within); a blank only *between* operations. e.g. an action body: guard → ⎵ → map-request + send + store-result → ⎵ → return.

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
- [request-models.md](../presentation/request-models.md) — applies it to the `ToCommand` mapping method
