# Knob

*Last updated: 2026-09-10*

> A rotary dial — drag to sweep a continuous parameter through an arc.
> What a control is → [control](../../constructs/visual/control.md).

## Reach for it when

- must set a fine continuous parameter where a rotation reads as the gesture — gain, mix, blur
- must accept the SDK's `0`–`1` unit range unless the domain says otherwise

---

## Instead of

| Reach for | When |
|---|---|
| [Slider](slider.md) | the range is linear and the track carries meaning |
| [NumberInput](numberInput.md) | the reader needs to type an exact value |
| [Stepper](stepper.md) | the value moves through named stages rather than a range |

---

## Values

- should leave `min` `0`, `max` `1`, `step` `0.01`, `largeStep` `0.1` — the unit-range set
- should leave `arcDegrees` at `270`; a full `360` hides where the range ends
- should leave `size` at `64` px and `isValueShown` on — the number is the only readback
