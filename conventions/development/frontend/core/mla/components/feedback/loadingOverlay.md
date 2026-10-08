# LoadingOverlay

*Last updated: 2026-10-01*

> A scrim over a centred spinner — the region stays readable but stops answering.
> What a state is → [state](../../constructs/visual/state.md).

## Reach for it when

- must block a region while a long task runs that a second click would repeat or corrupt — an import, a bulk
  apply, a generated export
- must cover a region that already has content, and keep that content readable behind the scrim
- must not cover a region while its data loads or refreshes — that is the
  [loading pattern](../../domains/data/state-and-data.md#loading)
- must not stand in for one control's pending state — a single command reports on its [Button](../actions/button.md)

---

## Instead of

| Reach for | When |
|---|---|
| [LoadingState](loadingState.md) | the region is empty and the report can take its place |
| [SkeletonState](skeletonState.md) | the unloaded shape is worth drawing rather than dimming |
| [SplashScreen](splashScreen.md) | the app itself is starting and no shell exists yet |
| [Button](../actions/button.md) `isLoading` | one command is in flight and the rest of the region stays usable |
| `BackdropOverlay` | the scrim carries a surface of its own rather than a spinner |

---

## Values

- must set `isInline` to mask one region, on a parent that is `position: relative`
- must cover the viewport, the default form, only when the whole app has to wait
- must drive `isOpen` from the task's own pending state, and clear it on failure as on success
- must name the running task in `label` — `Importing 240 rows…` — where the default `Loading…` hides it
- must leave a cancel or recovery action reachable while the mask is up
  ([state](../../constructs/visual/state.md#content))
- should set `hasBlur` for a heavy region — it reaches both scrims
- should leave `spinnerSize` at `lg` and `spinnerTone` at `brand`
