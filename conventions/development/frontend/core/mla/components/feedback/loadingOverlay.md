# LoadingOverlay

*Last updated: 2026-09-10*

> A scrim over a centred spinner — the region stays readable but stops answering.
> What a state is → [state](../../constructs/visual/state.md).

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

- should set `hasBlur` for a heavy region — it reaches both scrims
- should leave `spinnerSize` at `lg` and `spinnerTone` at `brand`
