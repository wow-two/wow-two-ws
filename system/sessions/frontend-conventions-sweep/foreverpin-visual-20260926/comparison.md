# ForeverPin visual comparison

*Last updated: 2026-09-26*

## Choice

Keep the current two-tab builder. The candidate changes contrast, restrained shadows, product heading weight, header wrapping, and shared gutters. Geist and the lavender/violet identity remain.

This is an uncommitted comparison candidate, not an accepted design or a Vue migration. The app still uses React; the selected visual direction can be carried into Vue.

## Desktop — light

| Before | Candidate |
|---|---|
| ![Before light](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/system/sessions/frontend-conventions-sweep/foreverpin-visual-20260926/before-edit-light-desktop-viewport.jpg) | ![Candidate light](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/system/sessions/frontend-conventions-sweep/foreverpin-visual-20260926/after-edit-light-desktop-viewport.jpg) |

## Desktop — dark

| Before | Candidate |
|---|---|
| ![Before dark](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/system/sessions/frontend-conventions-sweep/foreverpin-visual-20260926/before-edit-dark-desktop-viewport.jpg) | ![Candidate dark](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/system/sessions/frontend-conventions-sweep/foreverpin-visual-20260926/after-edit-dark-desktop-viewport.jpg) |

## Mobile — light

| Before | Candidate |
|---|---|
| ![Before mobile](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/system/sessions/frontend-conventions-sweep/foreverpin-visual-20260926/before-edit-light-mobile-viewport.jpg) | ![Candidate mobile](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/system/sessions/frontend-conventions-sweep/foreverpin-visual-20260926/after-edit-light-mobile-viewport.jpg) |

## Evidence

- Both variants use the same disposable saved code and local backend; no mocked API images.
- Desktop: 1440×1000 CSS viewport. Mobile: 390×844 CSS viewport; matching 375×812 native captures.
- Mobile document overflow falls from 604px to 375px at a 375px client width; 360px viewport also fits.
- Theme contrast calculations, source baseline, viewport details, and image hashes: [evidence](evidence.json), [contrast](contrast.json).
- This trial does not fix the known static-edit wording, routing constraints, or other source-audit findings.
- Builder controls and form semantics are unchanged. Keyboard and full migrated-flow acceptance remain future checks.

Full layout/logic analysis: [frontend audit](../foreverpin-ui-audit-20260926.md).
