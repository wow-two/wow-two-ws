# Idioms

*Last updated: 2026-06-16*

> What — idiomatic C# sugar: prefer the terse built-in form where it costs no clarity, regardless of layer.
> Purpose — cut ceremony the compiler/IDE can infer, so the code reads at the level of intent, not boilerplate.
> Use case — reach for it whenever the IDE offers a "simplify" / "convert" hint and the shorter form loses nothing.

## Method groups

- **A lambda that only forwards to a method → use the method group.** When the lambda body is just a call passing its params straight through, drop it for
  the method name: `() => NoContent()` → `NoContent`, `x => Process(x)` → `Process`.
- Only when the signature matches **exactly** — no arg reshaping, reordering, or extra args (`x => Foo(x, 1)` stays a lambda).
- Apply wherever the IDE offers "Convert into method group" (Roslyn `IDE0200`).
- Reconciles with [members.md](members.md): a forwarder lambda has **no logic to breakpoint**, so the terse method group is free — unlike a method *body*
  with logic, which stays a block `{ }`.

> Room to grow — other zero-cost idioms land here as adopted: target-typed `new` (`Foo x = new()`), collection expressions (`[]`), etc.

## See also

- [members.md](members.md) — block `{ }` vs expression `=>` bodies; the debuggability rationale this reconciles with
- [controllers.md](../presentation/controllers.md) — the `() => NoContent()` → `NoContent` method group in the `DeleteById` `.Match` example
