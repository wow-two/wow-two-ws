# ColorSwatch

*Last updated: 2026-08-20*

> The colour chip — one square or circle over a checkerboard, so partial alpha reads as partial.
> A [display](../../constructs/visual/display.md), not a control, though the SDK ships it in `forms/`.
> Its full surface → `ColorSwatch.spec.md`.

## Reach for it when

- must show one colour beside its name, its token, or its row
- must give a picker its trigger face — [ColorPicker](colorPicker.md) mounts it as one
- should reach for it where the colour is read and never edited

---

## Instead of

| Reach for | When |
|---|---|
| [ColorSwatchPicker](colorSwatchPicker.md) | several chips form a palette the reader chooses from |
| [ColorPicker](colorPicker.md) | clicking it should open a panel rather than run a command |
| [ColorInput](colorInput.md) | the hex is to be read as text as well as colour |
| `Badge` | the chip carries a label rather than a raw colour |

---

## Values

- should leave `size` at `md`, `shape` at `square`, `color` at `#000000`
- must attach a click listener to get a `<button>` — without one it renders a `<div>`
- must pass `color` any CSS colour string, not only a hex
- should set `isSelected` from the palette's selection, never from hover
