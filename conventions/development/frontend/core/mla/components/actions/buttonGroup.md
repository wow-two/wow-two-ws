# ButtonGroup

*Last updated: 2026-09-10*

> A connected row or column of buttons that stay independent of each other.
> What an action is → [action](../../constructs/visual/action.md).

## Reach for it when

- must reach for it when adjacent commands read as one control — a split button
- must reach for it when every button keeps its own tab stop
- should reach for it around [Button](button.md), [LinkItem](linkItem.md), or [ToggleInput](toggleInput.md) children

---

## Instead of

| Reach for | When |
|---|---|
| [ToggleGroup](toggleGroup.md) | the strip tracks which item is selected |
| [Toolbar](toolbar.md) | the items share one tab stop with arrow-key movement |
| `ControlGroupField` | the row needs a label beside it — a layout concern, not an action |
| [SpeedDialGroup](speedDialGroup.md) | the commands float over the content instead of sitting in it |

---

## Values

- should set `orientation="vertical"` only when the surrounding layout is a column
- should pass `shape="square"` or `"circle"` on icon-only members
