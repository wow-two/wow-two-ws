# ForeverPin palette comparison

*Captured: 2026-09-26*

## Applied direction

- The owner confirmed the after palette on September 26; `6264a34` is the accepted baseline.
- Cool neutral canvas and white navigation/cards replace the lavender wash in light mode.
- Graphite surfaces rise above a charcoal canvas in dark mode.
- Dividers remain quiet; controls use stronger outlines and violet keyboard focus.
- Violet actions, teal status accents, and the accepted typography/layout remain.
- Inactive segmented labels now use the supported SDK soft variant.
- Explicit foreground pairs cover destructive, success, warning, and information states.

## Matched capture conditions

- Before: accepted frame commit `59c708b`, before the palette changes.
- After: palette commit `6264a34`, same record, content, layout, theme, viewport, scroll origin, and browser.
- Desktop viewport/raster: 1440×1000; phone viewport390×844, native raster375×812.
- Disposable local guest record: Spring menu table tent, destination `https://example.com/menu`.
- Files are native browser captures; no screenshot pixels were edited.

## Light desktop

| Before | After |
|---|---|
| ![Before](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/system/sessions/frontend-conventions-sweep/foreverpin-palette-20260926/before-light-desktop.jpg) | ![After](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/system/sessions/frontend-conventions-sweep/foreverpin-palette-20260926/after-light-desktop.jpg) |

## Dark desktop

| Before | After |
|---|---|
| ![Before](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/system/sessions/frontend-conventions-sweep/foreverpin-palette-20260926/before-dark-desktop.jpg) | ![After](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/system/sessions/frontend-conventions-sweep/foreverpin-palette-20260926/after-dark-desktop.jpg) |

## Light mobile

| Before | After |
|---|---|
| ![Before](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/system/sessions/frontend-conventions-sweep/foreverpin-palette-20260926/before-light-mobile.jpg) | ![After](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/system/sessions/frontend-conventions-sweep/foreverpin-palette-20260926/after-light-mobile.jpg) |

## Verification

- TypeScript typecheck and production build passed using Node24.11.0.
- Existing bundle-size warning remains; palette work does not claim bundle optimization.
- All98 declared contrast pairs pass their checked thresholds: text≥4.5:1; control/focus≥3:1.
- Input border against the actual muted Select surface: light3.12:1, dark3.19:1.
- Inactive tab labels: light5.33:1, dark6.82:1; warning hover4.83:1 on white.
- Keyboard focus and an open Select were exercised; selected state remained distinguishable.
- Phone document clientWidth375 equals scrollWidth375.
- These are focused palette checks, not complete accessibility or Vue migration acceptance.
- The palette captures use the existing React app. Vue and backend adoption remain open in v0.10.

## Supporting evidence

- `contrast.json`: declared token pairs, alpha composition method, source hash, thresholds, results.
- `light-computed.json` and `dark-computed.json`: sampled browser styles and dimensions.
- `after-design-light.jpg`: expanded design controls with the final palette.
- `after-dark-focus.jpg` and `after-dark-menu.jpg`: focused/open control appearance during verification.
- During initial captures the QR gradient intermittently painted blank despite visible SVG paths;
  this also occurred in the baseline. Settled primary frames are used for comparison.
  The palette does not change rendered code data or claim to resolve that existing preview/capture issue.
