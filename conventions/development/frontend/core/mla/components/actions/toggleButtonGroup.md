# ToggleButtonGroup

*Last updated: 2026-09-10*

> The strip that owns one selection across its [ToggleButton](toggleButton.md) children.
> Kind → [control](../../constructs/visual/control.md).

## Reach for it when

- must reach for it when the row's value matters, not the individual presses
- must reach for it with `type="multi"` when any number of items may stay on at once
- should reach for `variant="segmented"` for a short exclusive picker — day / week
- should reach for `variant="pill"` when the items read as detached chips

---

## Instead of

| Reach for | When |
|---|---|
| [ButtonGroup](buttonGroup.md) | the row is commands, with nothing selected |
| `RadioGroup` | the selection is a form field, submitted with the form |
| `Tabs` | the strip switches content panels rather than setting a value |
| [OptionTileGroup](optionTileGroup.md) | the options are icon-only preset tiles |

---

## Values

- should keep `type` at `single`; re-pressing the active item clears it
- should leave attachment alone — `segmented` forces it on, `pill` never attaches
- should set `equalWidth` when every cell shares the row width — an icon strip
