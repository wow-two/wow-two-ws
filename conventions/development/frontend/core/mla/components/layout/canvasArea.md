# CanvasArea

*Last updated: 2026-09-29*

> The pan-and-zoom plane — content laid out at actual size, moved and scaled inside a fixed box.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must let the reader zoom and pan a diagram, map or board wider or taller than its box
- must use it for every product canvas — never hand-roll a transform, a wheel handler or zoom buttons
- should keep the default `bounds: 'content'` for a diagram viewer, so the content never leaves the box
- should set `bounds: 'none'` and `wheel: 'zoom'` for a full-screen editor with an open plane
- should size the box explicitly — a height class or style; the default `h-96` suits a demo, not a page

---

## Values

| Prop | Value | When |
|---|---|---|
| `initialZoom` | `1` | the content's text must stay legible when the box opens |
| `initialZoom` | `'fit'` | the whole shape matters more than its labels at first sight |
| `v-model:viewport` | bound | the page restores, links or shares the view |
| `hasControls` | `false` | the page supplies its own zoom island through the `controls` slot |

---

## Instead of

| Reach for | When |
|---|---|
| [ScrollArea](scrollArea.md) | the content only scrolls and never scales |
| `NodeEditor` | the reader moves and connects the nodes themselves |
| `LightboxModal` | one image opens full screen to zoom |
