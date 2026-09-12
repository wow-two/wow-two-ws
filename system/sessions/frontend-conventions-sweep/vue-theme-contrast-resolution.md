# Vue theme contrast resolution

*Last updated: 2026-09-10*

## Outcome

All 183 shipped themes pass the expanded supported-token contrast validator in both modes. Smart QR is now an authored **candidate** pending visual review in its app. There is no claim that the edited palette already has human validation.

Exactly 382 theme foreground values changed: 364 generated subtle-foreground values (182 generated themes × two modes), plus 18 explicit Smart QR foreground values. Fourteen default CSS foreground values changed. At the foreground-only checkpoint every existing background, branded fill, soft fill, border, input and ring token was unchanged. The later required-indicator amendment below separately changes input and border-strong tokens; the current regression hash preserves all other non-foreground tokens except explicitly permitted ring indicators. CSS `@source './'` remains intact.

The complete per-theme/mode/token before-and-after ledger is [vue-theme-token-changes.json](vue-theme-token-changes.json). The generated palette is deterministic; there is no random recoloring.

## Requirements and implementation

[W3C Understanding SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) requires 4.5:1 for ordinary-size text and explicitly includes placeholders. The existing `subtle-foreground` use in InputStyles, CodeEditor and command inputs is small text, so treating it as a 3:1 non-text affordance was incorrect. Threshold comparisons now use the unrounded computed ratio without the previous tolerance.

At the foreground checkpoint the validator had 108 declared pairs per mode: normal/muted/subtle text on background, card, popover and muted; each solid/soft tone pair; soft-toned text on the neutral host surfaces used by outline/ghost variants; ring against page background; and the existing 30% colored glass, 70% neutral glass, 60% soft tint and 30% muted tint over each declared host.

`ForegroundContrast.ts` adjusts foreground lightness while preserving the input surfaces. It first keeps a passing foreground unchanged; otherwise it searches toward the two luminance poles and chooses the nearest passing lightness. Color output is checked after CSS rounding with a small positive contrast margin. Generated subtle text also uses the text threshold from the initial neutral-ramp stage.

The original solid foreground cannot always serve both an opaque saturated fill and the same color at 30% opacity. `Tones.glass` and `Tones.glassOutline` now use each tone's soft foreground, following the existing warning variant: eight class strings changed (primary, destructive, success and info in both variants). Fill tokens, border tokens and alpha values stay intact.

These guarantees apply to the declared opaque SDK surfaces and those specified composited recipes. Foreign custom colors, arbitrary images and other backdrops need contrast verification at the caller's surface; passing token metadata is not a blanket application WCAG certification.

## Explicit authored and default changes

| Palette | Mode | Token | Before | After |
|---|---|---|---|---|
| Smart QR | light | `muted-foreground` | `#6e7188` | `oklch(49.6% 0.0358 279.3)` |
| Smart QR | light | `subtle-foreground` | `#9b9fb5` | `oklch(49.5% 0.0323 277.4)` |
| Smart QR | light | `primary-soft-foreground` | `#5b21b6` | `oklch(42.5% 0.2106 292.8)` |
| Smart QR | light | `accent-foreground` | `#ffffff` | `oklch(22.9% 0.0000 89.9)` |
| Smart QR | light | `accent-soft-foreground` | `#115e59` | `oklch(41.6% 0.0705 188.2)` |
| Smart QR | light | `destructive-soft-foreground` | `#b91c1c` | `oklch(41.4% 0.1694 27.5)` |
| Smart QR | light | `info-foreground` | `#ffffff` | `oklch(23.5% 0.0000 89.9)` |
| Smart QR | light | `info-soft-foreground` | `#0e7490` | `oklch(41.9% 0.0783 223.1)` |
| Smart QR | light | `success-foreground` | `#ffffff` | `oklch(27.3% 0.0000 89.9)` |
| Smart QR | light | `success-soft-foreground` | `#15803d` | `oklch(41.8% 0.1152 150.1)` |
| Smart QR | light | `warning-foreground` | `#78350f` | `oklch(39.7% 0.1054 45.9)` |
| Smart QR | light | `warning-soft-foreground` | `#b45309` | `oklch(46.9% 0.1261 49.0)` |
| Smart QR | dark | `subtle-foreground` | `#6e6e76` | `oklch(61.3% 0.0123 286.0)` |
| Smart QR | dark | `primary-foreground` | `#ffffff` | `oklch(16.9% 0.0000 89.9)` |
| Smart QR | dark | `destructive-foreground` | `#ffffff` | `oklch(22.7% 0.0000 89.9)` |
| Smart QR | dark | `info-foreground` | `#ffffff` | `oklch(35.7% 0.0000 89.9)` |
| Smart QR | dark | `success-foreground` | `#ffffff` | `oklch(37.3% 0.0000 89.9)` |
| Smart QR | dark | `warning-foreground` | `#78350f` | `oklch(39.7% 0.1054 45.9)` |
| Default CSS | light | `subtle-foreground` | `#74747d` | `oklch(54.5% 0.0137 285.9)` |
| Default CSS | light | `primary-soft-foreground` | `#1d4ed8` | `oklch(46.1% 0.2172 264.4)` |
| Default CSS | light | `destructive-soft-foreground` | `#b91c1c` | `oklch(45.8% 0.1873 27.5)` |
| Default CSS | light | `success-foreground` | `#ffffff` | `oklch(27.3% 0 89.9)` |
| Default CSS | light | `success-soft-foreground` | `#15803d` | `oklch(45.5% 0.1254 150.1)` |
| Default CSS | light | `warning-foreground` | `#78350f` | `oklch(39.7% 0.1054 45.9)` |
| Default CSS | light | `warning-soft-foreground` | `#b45309` | `oklch(50.8% 0.1366 49)` |
| Default CSS | light | `info-soft-foreground` | `#0e7490` | `oklch(44.1% 0.0822 223.1)` |
| Default CSS | light | `accent-foreground` | `#ffffff` | `oklch(22.9% 0 89.9)` |
| Default CSS | dark | `primary-foreground` | `#ffffff` | `oklch(23.6% 0 89.9)` |
| Default CSS | dark | `destructive-foreground` | `#ffffff` | `oklch(22.7% 0 89.9)` |
| Default CSS | dark | `success-foreground` | `#ffffff` | `oklch(37.3% 0 89.9)` |
| Default CSS | dark | `warning-foreground` | `#78350f` | `oklch(39.7% 0.1054 45.9)` |
| Default CSS | dark | `info-foreground` | `#ffffff` | `oklch(35.7% 0 89.9)` |


The internal authored palette catalog was renamed `constants/Validated.ts` → `constants/Authored.ts`, and its export became `AuthoredThemes`; registry references were updated. The public registry APIs are unchanged. Smart QR's status, tags and description now identify a contrast-corrected candidate awaiting app review.

## Validation

- `pnpm exec vitest run --project unit tests/unit/foundation/themes` — **2 files / 14 tests passed**.
- Independent sRGB/OKLCH conversion, relative luminance and alpha compositing in the tests verify all 183 themes and actual default CSS variables, without calling the SDK contrast implementation.
- Regressions explicitly require small-placeholder pairs at 4.5:1, check every changed glass recipe, and preserve the previous background/fill/decorative-border palette outside the explicit indicator amendment.
- `pnpm exec vue-tsc --noEmit -p tsconfig.typecheck.json` — passed.
- Scoped ESLint, Prettier and capability-reference checks passed before handoff; parent owns the final build and packed CSS/consumer gates.

This resolution supersedes the read-only Smart QR contrast finding in [vue-capability-layout-audit.md](vue-capability-layout-audit.md).


## Required-indicator amendment

InputStyles uses `input` for the default boundary, `border-strong` on hover and `ring` for keyboard focus, on popover or read-only muted surfaces. These identifiable boundaries and indicators need at least 3:1 against their adjacent surface under [WCAG 2.2 non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html). This requirement does not apply indiscriminately to decorative separators.

The final validator declares **119 pairs per mode**. It now checks input, border-strong and ring against background, card, popover and muted. Pair de-duplication also distinguishes opaque foreground-on-muted from foreground over a 30% muted overlay; both are independently covered. All **183 themes pass**. Every ring already passed the expanded neutral-host requirements, so no ring token changed.

This is a separate amendment to the foreground ledger: **732 theme indicator values changed** (input and border-strong × 183 themes × two modes), plus **four default CSS indicator values**. Only lightness changes; background, fill, decorative border, existing foreground and branded hue values remain intact. The exact 732-value ledger is [vue-theme-indicator-changes.json](vue-theme-indicator-changes.json). Smart QR remains a candidate awaiting app visual review.

| Palette | Mode | Tokens | Before | After |
|---|---|---|---|---|
| Smart QR | light | border-strong | #c7cad9 | oklch(59.1% 0.0210 276.9) |
| Smart QR | light | input | #e4e6f0 | oklch(59.0% 0.0137 277.1) |
| Smart QR | dark | border-strong | #3a3a40 | oklch(51.6% 0.0103 285.9) |
| Smart QR | dark | input | #2a2a2e | oklch(51.6% 0.0072 285.9) |
| Default CSS | light | input, border-strong | #d4d4d8 | oklch(64.3% 0.0055 286.3) |
| Default CSS | dark | input, border-strong | #3f3f46 | oklch(50.6% 0.0119 285.8) |

Invalid input border/focus classes now use destructive-soft-foreground. Selected radio border/dot classes now use primary-soft-foreground. Those existing semantic foregrounds are independently verified at 4.5:1 on the declared neutral hosts, while the branded destructive/primary fills remain unchanged. Default and focus radio indicators retain the corrected input/ring tokens.

Validation: the focused unit/DOM run passes **18 tests across three files**; strict Vue typecheck and scoped ESLint pass. Regressions independently calculate sRGB luminance for every theme and default CSS neutral indicator pair, reject insufficient indicator tokens, verify opaque text pairs independently from overlays, preserve background/fill/decorative-border values against the pre-sweep snapshot, and mount the selected radio to verify its token bindings. These checks establish only the declared token/surface and recipe contracts: they do not claim universal component WCAG compliance or contrast over arbitrary custom, image or foreign backdrops.
