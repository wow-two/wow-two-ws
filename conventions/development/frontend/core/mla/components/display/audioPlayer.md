# AudioPlayer

*Last updated: 2026-09-10*

> Audio with the app's own transport — play, scrub, volume, speed.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must play a recording inside the page — a voice note, a track, an episode
- must pass `peaks` to swap the plain scrubber for a waveform
- should read position from `@time-update` rather than reaching for the element

---

## Instead of

| Reach for | When |
|---|---|
| [AudioWaveform](audioWaveform.md) | only the waveform is wanted, with no transport |
| [VideoPlayer](videoPlayer.md) | the media has picture as well as sound |
| `<audio controls>` | the browser's own chrome is acceptable |

---

## Values

- should set `isCompact` where the player sits inside a row rather than owning a block
