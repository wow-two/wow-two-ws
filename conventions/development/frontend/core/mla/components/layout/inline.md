# Inline

*Last updated: 2026-09-10*

> The leading-edge wrapping row — chips, tags, meta pairs, small inline actions.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must flow small items from the leading edge and wrap them
- must keep a tighter rhythm than a [Stack](stack.md) row gives
- should reach for it for chip rows, tag rows and meta lines

---

## Instead of

| Reach for | When |
|---|---|
| [Cluster](cluster.md) | the wrapped row reads as centred |
| [Stack](stack.md) | the row stays on one line and the gap is wider |
| `ButtonGroup` | adjacent buttons read as one control |
| [Grid](grid.md) | the items have to line up in columns |

---

## Values

- should set `wrap` to `false` only for a single-line row that truncates
