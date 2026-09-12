# Listbox

*Last updated: 2026-09-10*

> The selection list itself — always open, keyboard-navigable, single or multiple.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must show the options in place, with no trigger and no panel to open
- must fill a surface that is already the picker — a drawer, a split pane, a step
- should reach for it as the shared body under [Select](select.md), [Combobox](combobox.md) and
  [MultiSelect](multiSelect.md)

---

## Instead of

| Reach for | When |
|---|---|
| [Select](select.md) | the list must collapse to a trigger |
| [Combobox](combobox.md) | the reader types to narrow the list |
| [RadioGroup](radioGroup.md) | the options are few and each needs its own visible label |
| `Menu` | the entries run commands rather than set a value |

---

## Values

- should leave `indicator` unset: `check` when single, `checkbox` when multiple
