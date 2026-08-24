# Notation

*Last updated: 2026-08-19*

> How a settled concept gets written down — its name, its documentation, its layout, its imports.
> Purpose — sit between the abstraction and the first keystroke, so no component doc re-argues spelling.
> Use case — reach here while turning a decided component into source.

## The four

| Bucket | Notates |
|---|---|
| [naming/](naming/naming.md) | identity — which characters stand for this thing |
| [documentation/](documentation/documentation.md) | intent — what the reader is told about it |
| [style/](style/style.md) | structure — how the text is arranged |
| [style/imports](style/imports.md) | reach — which names a file pulls in, and in what order |

---

## Defaults

- must apply to **every** symbol, whatever it is — a rule that needs a role is not notation.
- may be **overridden by a component**, which states the override in its own file.
- must be cited rather than restated ([one owner per rule](../../../../../conventions.md)).
- must hold for both frameworks — a rule true only of an SFC or only of JSX belongs with that framework.

---

## Neighbours

- [lla constructs](../constructs/constructs.md) — the constructs being notated
- [constructs](../../mla/constructs/constructs.md) — the app roles that override these defaults
- [components](../components/components.md) — constants, enums and extensions, which override their own
- [Vue SFC](../constructs/vue/vue-sfc.md) — a framework construct, which overrides rather than restates
