# SplashScreen

*Last updated: 2026-09-29*

> The first-load screen — the product logo centred above a slim progress bar while the app starts.
> What a state is → [state](../../constructs/visual/state.md).

## Reach for it when

- must cover an app's first load, before its shell can render anything useful
- should use the overlay form so the app mounts beneath it and the lift reveals the app with a fade
- should use the page form where nothing else renders until the load finishes

---

## Instead of

| Reach for | When |
|---|---|
| [LoadingState](loadingState.md) | one section, not the whole app, is waiting |
| [LoadingOverlay](loadingOverlay.md) | a running app blocks a region during a long task |
| [Skeleton](skeleton.md) | the shell is up and only its data is loading |

---

## Values

- must fill the `logo` slot with the product's primary horizontal logo, per the [logo system](../../../../../../design/identity/logo-system.md)
- should drive `value` through the real boot stages (shell mounted, session resolved, first route ready); omit it only when no stage is knowable
- should repeat the same logo and bar as static markup inside the app's mount node, so the first paint shows it before scripts load; mounting replaces it
- should close within one fade of the last stage — no minimum display time
- should leave the product's theme to its own tokens and classes; the SDK component carries no product styling
