# LoadingOverlay

*Last updated: 2026-08-23*

> A scrim over a centred spinner — the region stays readable but stops answering.
> What a state is → [state](../../constructs/visual/state.md).
> Its full surface → `LoadingOverlay.spec.md`.

## Reach for it when

- must block interaction with a region while a long task runs
- must keep the content behind readable — swapping it out is a [Skeleton](skeleton.md)
- should reach for it where the region already has content

---

## Instead of

| Reach for | When |
|---|---|
| [LoadingState](loadingState.md) | the region is empty and the report can take its place |
| [Skeleton](skeleton.md) | the unloaded shape is worth drawing rather than dimming |
| `Backdrop` | the scrim carries a surface of its own rather than a spinner |

---

## Values

- must set `isInline` to scope the scrim, giving that parent `position: relative`
- must leave `isInline` off to cover the viewport — a `Backdrop` portals behind
- should set `hasBlur` for a heavy region — it reaches both scrims
- should leave `label` at `Loading…`; blanking it still labels the spinner `Loading`
- should leave `spinnerSize` at `lg` and `spinnerTone` at `brand`
