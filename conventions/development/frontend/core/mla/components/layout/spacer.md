# Spacer

*Last updated: 2026-09-10*

> The flexible empty box — one flex child that pushes its siblings apart.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must push siblings to opposite ends of a flex line
- must not reach for it for rhythm → [spacing](../../../lla/constructs/tailwind/spacing.md)

---

## Instead of

| Reach for | When |
|---|---|
| `ml-auto` on the item | one item moves and no placeholder is wanted |
| [Stack](stack.md) | the space is an even gap rather than the leftover |
| [Divider](divider.md) | the separation carries a visible rule |

---

## Values

- should keep `axis` at `horizontal`, its default, on a row
