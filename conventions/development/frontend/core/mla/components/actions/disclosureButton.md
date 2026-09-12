# DisclosureButton

*Last updated: 2026-09-10*

> The header that expands and collapses a region, chevron included.
> What an action is → [action](../../constructs/visual/action.md).

## Reach for it when

- must reach for it as the header of a collapsible section or accordion item
- must reach for it when the button reports an expanded region — `aria-expanded`
- should let it own its state; go controlled only when a parent coordinates several

---

## Instead of

| Reach for | When |
|---|---|
| [ToggleButton](toggleButton.md) | the state is a mode read back as a value, not an expanded region |
| [Button](button.md) | nothing expands — the click just runs |

---

## Values

- should set `defaultOpen` on a section that must start expanded; it starts closed
