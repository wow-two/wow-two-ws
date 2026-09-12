# ColorSlider

*Last updated: 2026-09-10*

> The single-channel track — hue, saturation, value or alpha, drawn as its own gradient.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must edit exactly one channel, with the gradient showing what the channel does
- must stack several tracks to build a panel by hand — one per channel
- should reach for it for alpha; nothing else in the folder edits opacity alone

---

## Instead of

| Reach for | When |
|---|---|
| [ColorPicker](colorPicker.md) | the whole colour is being picked and the panel is not bespoke |
| [ColorWheel](colorWheel.md) | hue reads better as a ring than a strip |
| [ColorArea](colorArea.md) | saturation and value move together |
| [Slider](slider.md) | the number is not a colour channel and needs no gradient |
