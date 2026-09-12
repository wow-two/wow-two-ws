# RadiusGlyph

*Last updated: 2026-09-10*

> The concentric mark — a filled disc scaled inside a track, showing one extent.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must show a radial fraction compactly — a radius, a spread, a falloff
- must pass `extent` in `0..1`; anything outside renders wrong, not clamped

---

## Instead of

| Reach for | When |
|---|---|
| [FrameGlyph](frameGlyph.md) | the mark previews a frame-and-pupil shape |
| `ProgressBar` | the fraction is task progress rather than geometric extent |
| [Sparkline](sparkline.md) | the value is one point in a series |

---

## Values

- should leave `size` at `16` px, `strokeWidth` at `1.5`, `trackOpacity` at `0.4`
- should leave `color` at `currentColor`, so the mark inherits its row's tone
