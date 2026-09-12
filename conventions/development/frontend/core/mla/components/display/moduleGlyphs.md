# ModuleGlyphs

*Last updated: 2026-09-10*

> Four fixed-geometry marks for a module-shape picker — dots, bars, cells.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must preview a module shape in a picker — the QR fill styles, side by side
- must pick the glyph that names the shape; each is its own component, not a variant
- should mount them in an `OptionTileGroup` grid

---

## Instead of

| Reach for | When |
|---|---|
| [FrameGlyph](frameGlyph.md) | the mark previews the eye rather than the modules |
| [RadiusGlyph](radiusGlyph.md) | the mark shows an extent rather than a shape |
| `Icon` | the mark is a named icon rather than a geometry preview |

---

## Values

- should leave `size` at `20` px across the set, so the grid stays even
