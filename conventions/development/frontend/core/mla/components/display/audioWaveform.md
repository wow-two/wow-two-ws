# AudioWaveform

*Last updated: 2026-09-10*

> The bar waveform — amplitudes drawn as SVG, optionally seekable.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must show a clip's shape without a full transport — a message row, a preview
- should pass `onSeek` when the bars should be clickable and arrow-key seekable

---

## Instead of

| Reach for | When |
|---|---|
| [AudioPlayer](audioPlayer.md) | the reader needs play, volume and speed too |
| [Sparkline](sparkline.md) | the series is data rather than audio amplitude |

---

## Values

- should leave `tone` at `brand`
