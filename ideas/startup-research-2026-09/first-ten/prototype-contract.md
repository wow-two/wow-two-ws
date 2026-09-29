# First-ten prototype collaboration contract

Confirmed scope: analyze implementation/product philosophy/design and create clickable mock UIs for ten selected products. These are static local research artifacts, not production product scaffolds, deployed services or market validation. Production proposals use Vue and .NET subject to verified SDK boundaries. No messages, uploads to external services, account actions or purchases.

## Module contract

Each assigned slug owns `products/{slug}/Product.vue`, `product.css`, `product.md`, and `verification.md` only. Root owns Vue3/Vite/Tailwind4 shell, strict TypeScript setup, shared controls, cross-product analysis, tests and hub. Do not stage, commit, scaffold repositories or edit other lanes. SFC style blocks are forbidden; import scoped CSS from product.css.

Use a Vue SFC with `<script setup lang="ts">` and a typed `api` prop:

```ts
import { ref, computed, watch } from 'vue';
import type { PrototypeApi } from '../../shared/PrototypeApi';
const props = defineProps<{ api: PrototypeApi }>();
const state = ref(props.api.state({ /* typed sample state */ }));
watch(state, value => props.api.save(value), { deep: true });
```

`api.state<T>(initialObject:T):T` returns saved JSON or a clone of initialObject. `api.save(state)` persists locally. `api.toast(message, kind='success')` shows accessible feedback. `api.download(filename, contents, mime='text/plain')` downloads local data. `api.money(number)` formats USD. `api.today` is fixed `2026-09-29` for consistent sample chronology. `api.navigate(slug)` switches products. Optional shared `Icon.vue` is imported from `../../shared/Icon.vue` and accepts `name` string, decorative by default. Icons available: wallet, code, inbox, book, users, file, flag, calendar, layers, mic, arrow-right, check, plus, search, download, chevron, x, sun, moon, play, bell, settings, home, external, reset, alert, clock.

Use native labeled forms and `<dialog>` for task modals with showModal/close; no browser alert/confirm. Native semantic controls are acceptable for one-off research compositions; production maps to verified SDK exports. Root uses public Vue SDK capability where useful. No CDN dependencies or external network requests. No `any`, `defineModel`, Options API, transitions, key modifiers, or v-model modifiers. User content stays in Vue interpolation, not v-html. Set product workspace outer `data-product="slug"`.

## Shared classes

`workspace-heading`, `eyebrow`, `page-title`, `page-description`, `actions`, `btn` (`primary`, `secondary`, `ghost`, `danger`, `small`), `icon-button`, `grid-2`, `grid-3`, `split-layout`, `stack`, `panel`, `panel-header`, `panel-body`, `metrics`, `metric`, `metric-label`, `metric-value`, `metric-note`, `muted`, `small`, `mono`, `badge` (`success`, `warning`, `danger`, `info`, `neutral`), `tabs`, `tab` (`active`), `table-wrap`, `data-table`, `field`, `input`, `select`, `textarea`, `form-grid`, `checklist`, `list-row`, `progress`, `empty-state`, `callout` (`warning`, `info`, `success`), `modal`, `modal-header`, `modal-body`, `modal-footer`, `avatar`, `divider`, `visually-hidden`, `code-block`, `timeline`, `timeline-item`, `stepper`, `step` (`active`, `complete`).

CSS variables: `--canvas`, `--surface`, `--surface-alt`, `--ink`, `--muted`, `--line`, `--accent` (per product), `--accent-soft`, `--danger`, `--warning`, `--success`, `--radius`, `--shadow`. Use semantic tokens and avoid hardcoded text/background colors in inline CSS. Root supplies light/dark and three proposed canvas palettes. Custom layout scoped to `[data-product="slug"]`. Fonts system sans; code system mono. Original UI, no copied logos or remote images.

## Functional quality

Each module requires at least three meaningful state-changing actions, a detail view, form validation, a local export, and a reset handled by shell. Buttons must work. Use realistic synthetic records labeled globally by shell. Never imply real emails, cloud uploads, payments, deployments or monitoring occurred. Export and derived balances must update from state. Local confirmation messages say simulated where appropriate. Core workflow, not just a dashboard; unique task-specific spatial layout. Responsive at390px, tablet820px, desktop1440px, keyboard controls and both themes. Include a short ordered smoke-test scenario in product.md naming exact buttons and expected result.

## Per-product analysis

`product.md` contains: decision/user/job; product philosophy (promise, core object, human decision, automation boundaries, quiet-by-default); viable narrow advantage and named incumbent challenge with actual sources; full core journey including failure/empty/conflict states; MVP and non-goals; domain entities/invariants; proposed API routes/events/background jobs and idempotency/authorization; data ownership/security; proposed Vue/.NET integration boundaries (no invented SDK API availability); acceptance criteria; staged build sequence; free/paid boundary; $20–50 pre-revenue budget design and expansion gate; activation/retention and paid-pilot kill gate; design reference URLs and extracted interaction moves (label visual observations vs conceptual inference), chosen layout rationale; light/dark semantic mapping and proposed reusable controls; mock workflow action coverage and remaining mocked capabilities.

Design selections are recommended proposals, not user-approved locks. Root provides three in-context canvas variants; do not block for design selection. No production implementation is authorized by a mockup alone.
