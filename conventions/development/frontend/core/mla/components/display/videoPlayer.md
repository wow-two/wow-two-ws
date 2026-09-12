# VideoPlayer

*Last updated: 2026-09-10*

> Video with the app's own transport, auto-hiding controls and keyboard shortcuts.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must play a clip in the page with chrome that matches the app
- must provide captions for speech and other required media alternatives for its content
- should give it a `poster`, so the frame is not blank before the first play

---

## Instead of

| Reach for | When |
|---|---|
| [AudioPlayer](audioPlayer.md) | the media is sound only |
| [Image](image.md) | a still frame is enough |
| `<iframe>` | the video is hosted and played by a third party |
