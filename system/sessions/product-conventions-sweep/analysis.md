# Product conventions sweep — analysis

*Last updated: 2026-10-01*

> The point pool of the sweep: what was fixed, which defaults were applied, what waits for the developer, and where
> every product stands against the conventions. State and resume steps → [context](context.md).

## Fixed

Contradictions and stale rules, each resolved in its owning convention.

- [x] F1 — `versioning.md` took the frontend version from `package.json` while forbidding a version there; the
  root and repo indexes repeated the old source.
- [x] F2 — `single-host-serving.md` wrote the SPA straight into `wwwroot` and hand-wired static serving;
  products build into `apps/web/dist`, copy through `deploy`, and the SDK serves it through `SpaHosting`.
- [x] F3 — `repo-structure.md` named backend tests `{Brand}.{Domain}.Tests` and colocated frontend tests, against
  `clean/testing.md` and `workspace.md`.
- [x] F4 — `repo-structure.md` carried a dated audit, a retired `business/` layout, numbered sections, history
  notes and a second copy of the image-publish rules; rewritten to the authoring shape, anchors re-pointed.
- [x] F5 — `styling.md` cited `useTheme`, which `ui-vue` never exported; the SDK ships `ColorModeProvider` and
  `useColorMode`.
- [x] F6 — the loading pattern cited `Skeleton.Slot` / `Skeleton.Group` and a TSX sample; the Vue SDK exports
  `SkeletonStateSlot` / `SkeletonStateGroup` with `isLoading`.
- [x] F7 — 106 component selection entries carried pre-rename names (`Stack`, `Select`, `Tabs`); renamed in
  place to the SDK's public names from the package `MIGRATION.md` table, with 424 links and 59 inline mentions.
- [x] F8 — kind docs cited examples that do not exist (`SelectInput`, `TabsPanel`, `AccordionItem`,
  `NotificationDot`).
- [x] F9 — `dev-cycle.md` said "don't pre-extract" beside the proactive-vector and SDK-change-loop rules.
- [x] F10 — `sdk-extraction.md` named the React package; the development index described a different rule than
  the doc; the root index did not list it.
- [x] F11 — `deploy-descriptor.md` described the release generator as still inside Wheelhouse; it lives in
  `wow-two-platform.pipelines` with the shared `publish.yml`. Its format comparison moved to a rationale doc.
- [x] F12 — `agentic-workflow.md` restated commit rules that disagreed with `git.md` (who publishes, pathless
  `git add`); `git.md` omitted `commit` from the lane check the hook enforces.
- [x] F13 — per-app design spec path pointed at the retired `platform/` top level.
- [x] F14 — 13 mentions of `@wow-two-beta/ui` where the standard is `ui-vue`; the import sample was React.
- [x] F15 — `sdk-structure.md` called itself not yet executed, described Storybook and `tsup`, and cited a flat
  `v0.1.md`; rewritten against the Vue package.
- [x] F16 — the root index authoring rules held an orphaned sentence, a 150-column wrap beside a 120-character
  budget, two table rules, and a `controllers.md` that does not exist.
- [x] F17 — two links pointed at a missing handoff anchor; `launch-profiles.md` linked the proxy rule to the
  wrong owner.

---

## Added

- [x] A1 — [product conformance](../../../conventions/development/repo/structure/product-conformance.md): every
  check a product repo owes, each linked to its owner.
- [x] A2 — [lucide](../../../conventions/development/frontend/core/mla/domains/icons/lucide/lucide.md): the one
  icon set, imports, sizes.
- [x] A3 — loading: the surface-per-wait table in the feedback group lead, and a fuller `LoadingOverlay` entry.
- [x] A4 — [shell](../../../conventions/development/frontend/shapes/app/shell/shell.md): the frame, the bar, the
  account menu, the page heading.
- [x] A5 — [document](../../../conventions/development/frontend/shapes/app/platform/document.md): the
  `index.html` head, app icons, the pre-paint theme script and the splash twin.
- [x] A6 — [UI copy](../../../conventions/design/content/ui-copy.md): how many words a screen carries.
- [x] A7 — known endpoints: `api/runtime-config`; startup defaults: the bundle's `/health` and readiness checks.

---

## Defaults applied

Choices made from the evidence named; each stands until the developer says otherwise.

- [ ] V1 — lucide is the only icon set: the SDK depends on it; `tnis` and `transportbrain` use tabler.
- [ ] V2 — icon sizes `12 · 14 · 16 · 20 · 24+`: the steps the SDK itself uses most.
- [ ] V3 — `engineering/scripts/` stays a sibling of `deployment/`; `operations/` is optional: the template and
  20 repos already have that shape.
- [ ] V4 — the verify workflow is `ci.yml`: three of five repos with CI use that name.
- [ ] V5 — health comes from the SDK boot bundle's `/health` with a readiness check per dependency; no
  hand-mapped route and no `Ready` action. `SpaHosting` likewise replaces hand-wired static serving.
- [ ] V6 — `api/runtime-config` is a known endpoint: the descriptor already required it; ForeverPin implements it.
- [ ] V7 — the line budget is 120 characters; the 150-column wrap is gone.
- [ ] V8 — a capability the SDK lacks may be built inline, with extraction as the next version's scope.
- [ ] V9 — file names `favicon.svg` / `favicon.png`, `apple-touch-icon.png`, `theme.js`, `boot-splash.css`.
- [ ] V10 — the shell anatomy follows Wheelhouse's applied frame.
- [ ] V11 — UI copy rules follow the 2026-09-29 sign-in feedback.
- [ ] V12 — the per-app design spec stays at `engineering/research/design-research/design-research.md`.

---

## Open

Decisions only the developer holds; nothing below was written into a convention.

- [ ] D1 — `.claude/rules/file-references.md` in product repos is a lookup table inside the auto-load folder;
  `10x-ws` moved its own to `.claude/file-references.md`. Move it for the template and 28 repos, or keep it.
- [ ] D2 — product palette home: an SDK-registered theme, or `:root` / `.dark` overrides in the app's
  `index.css` as Wheelhouse does. A theming convention waits on this.
- [ ] D3 — frontend app testing vector: tiers and placement (`apps/web/tests/`, a Playwright `e2e/`); products
  differ and no app-shape doc states it.
- [ ] D4 — `.claude/rules/templates/` auto-loads seven templates into every session; `CLAUDE-app.md` contradicts
  the repo structure. Move them out of the auto-load folder, or delete them in favour of the product template.
- [ ] D5 — the port ledger: the Vite "even port" rule against eight odd allocations, a template row of `8225`
  while the template binds `8224`, a table split by blank lines, two history lines. Another lane has it staged.
- [ ] D6 — `.claude/repo-registry.md` is dated June: it calls the UI SDK React and misses about 25 ventures.
- [ ] D7 — the product template and the `create-repo` skill stamp non-conformant repos; fix them before any
  product handoff, so new repos stop inheriting the gaps.
- [ ] D8 — `docs/conventions-taxonomy.md` proposes a reorganisation the tree has since made differently.
- [ ] D9 — workspace root strays: three `be-*.md` handoffs, empty `core/` and `shapes/` folders.
- [ ] D10 — where a product's gap list lands in phase 2: a root `handoff.md` alone, or backlog rows plus a
  courier handoff.

---

## Product matrix

A file scan on 2026-10-01 of the 32 repos shaped `product/` + `engineering/codebase/`. Heuristic — confirm each
cell against the repo when its handoff is written.

| Repo | Sln | Tests | BE SDK | Boot · health | FE | Ws | ui-vue | Icons | Ver | Fav | Theme | deploy.yml | Publish | ci | Plan | Spec | Root md |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| product-template | sln | bare | 10.0.21 | ✗ hand | Vue | ✓ | 0.0.7 | none | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | v0.1 | ✗ | — |
| wheelhouse | ✓ | ✓ | 10.0.62 | ✓ sdk+ready | Vue | ✓ | 0.0.9 | lucide | ✓ | ✓ | ✓ | ✓ | shared | ✓ | v0.3 | ✓ | — |
| secrets-vault | sln | mixed | 10.0.56 | ✓ sdk | Vue | ✗ | 0.0.6 | none | ✗ | ✗ | ✗ | ✗ | own | ✗ | v0.3 | ✗ | 1 |
| haven | ✓ | ✓ | 10.0.59 | ✓ sdk | Vue | ✓ | 0.0.7 | lucide | ✗ | ✗ | ✗ | ✗ | own | ✓ | v1.2 | ✓ | 1 |
| forever-pin | ✓ | ✓ | 10.0.60 | ✓ sdk | Vue | ✓ | 0.0.7 | none | ✗ | ✓ | ✗ | ✓ | own | ✓ | v0.11 | ✓ | 2 |
| prism | — | — | — | — | Vue+React | ✗ | 0.0.7 | lucide-react | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | v0.17 | ✗ | — |
| transcript-forge | ✓ | ✓ | 10.0.59 | ✓ sdk | Vue+React | ✓ | 0.0.7 | lucide | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | v0.8 | ✗ | 1 |
| sift | sln | bare | 10.0.21 | ✗ hand | React | ✗ | — | none | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | v0.2 +1 | ✗ | — |
| track-2-transportbrain | slnx | bare | 10.0.45 | ✓ sdk | React | ✗ | react ui | tabler | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | none | ✗ | — |
| arcade | sln | bare | 10.0.21 | ✗ hand | Vue | ✓ | 0.0.7 | none | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | v0.1 | ✗ | — |
| config-checker | slnx | bare | local | ✗ hand | Vue | ✓ | file | none | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | v0.1 | ✗ | — |
| customer-promises | slnx | bare | local | ✗ hand | Vue | ✓ | file | none | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | v0.1 | ✗ | — |
| documentation-checker | slnx | bare | local | ✗ hand | Vue | ✓ | file | none | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | v0.1 | ✗ | — |
| epub-review | slnx | bare | local | ✗ hand | Vue | ✓ | file | none | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | v0.1 | ✗ | — |
| file-watch | slnx | bare | local | ✗ hand | Vue | ✓ | file | none | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | v0.1 | ✗ | — |
| hijinx | — | — | — | — | Vue | ✓ | 0.0.7 | none | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | v0.1 | ✗ | — |
| listing-shelf | ✓ | ✓ | 10.0.59 | ✓ sdk | Vue | ✓ | 0.0.7 | none | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | v0.2 | ✗ | 1 |
| museums-gallery | sln | bare | 10.0.21 | ✗ hand | React | ✗ | react ui | lucide-react | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | none +1 | ✓ | 1 |
| pbn-studio | sln | bare | 10.0.21 | ✗ hand | Vue | ✓ | 0.0.7 | none | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | v0.1 | ✗ | — |
| podcast-readiness | slnx | bare | local | ✗ hand | Vue | ✓ | file | none | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | v0.1 | ✗ | — |
| pose-coach | ✓ | bare | 10.0.58 | ✓ sdk | Vue | ✓ | 0.0.7 | none | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | v0.1 | ✗ | — |
| procedure-review | slnx | bare | local | ✗ hand | Vue | ✓ | file | none | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | none | ✗ | — |
| retainer-balance | slnx | bare | local | ✗ hand | Vue | ✓ | file | none | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | none | ✗ | — |
| tnis | ✓ | ✓ | 10.0.63 | ✓ sdk | Vue | ✗ | 0.0.7 | lucide | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ | v0.3 | ✓ | — |
| tnis-mintrans | sln | bare | 10.0.21 | ✗ hand | Vue | ✗ | 0.0.5 | none | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | none | ✗ | — |
| training-seats | slnx | bare | local | ✗ hand | Vue | ✓ | file | none | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | none | ✗ | — |
| vendor-renewals | slnx | bare | local | ✗ hand | Vue | ✓ | file | none | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | none | ✗ | — |
| whiteout | — | — | — | — | React | ✗ | — | none | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | v0.9 +2 | ✗ | — |
| ocharo-assets | ✓ | bare | 10.0.21 | ✗ hand | Vue | ✓ | 0.0.7 | none | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ | v0.1 | ✗ | — |
| ocharo-marketing | ✓ | bare | 10.0.59, 10.0.63 | ✗ hand | Vue | ✗ | 0.0.9 | lucide | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | none +15 | ✗ | — |
| ocharo-platform | ✓ | mixed | 10.0.59, 10.0.63 | ✗ hand | Vue | ✓ | 0.0.7 | lucide | ✓ | ✗ | ✗ | ✓ | own | ✗ | v0.1 | ✗ | — |
| ocharo-studio | ✓ | bare | 10.0.58 | ✗ hand | Vue | ✓ | 0.0.9 | none | ✓ | ✓ | ✗ | ✓ | own | ✗ | v0.1 | ✗ | — |

### Columns

- `Sln` — `✓` is `{Brand}.BackendServices.slnx`; `slnx` has another name; `sln` is the classic format.
- `Tests` — `✓` every test project is tiered; `bare` is `{Product}.Tests`; `mixed` holds both.
- `BE SDK` — the pinned `WoW2.Sdk.Backend.Beta`; `local` is the unpublished `10.0.60-beta.local.20260927.8` build.
- `Boot · health` — `✓` the host calls `AddApiDefaults()`; `sdk` takes `/health` from the bundle, `hand` maps it
  itself, `+ready` adds its own readiness action.
- `Ws` — a pnpm workspace with `apps/web/`. `ui-vue` — the pin; `file` is a local tarball.
- `Ver` — `__APP_VERSION__` is read. `Fav` — a favicon exists. `Theme` — a pre-paint `theme.js` exists.
- `Publish` — `shared` calls the pipelines workflow; `own` copies the steps. `ci` — a `ci.yml` exists.
- `Plan` — the newest version folder; `+N` counts extra files in `engineering/planning/`.
- `Spec` — the design spec sits at its path. `Root md` — stray Markdown files at the repo root.

### Counts

- solution name conforms in 11 of 29 backends; 7 still use `.sln`.
- test projects are tiered in 6 of 29; 21 ship a bare `{Product}.Tests`.
- 10 first-ten repos pin a local SDK build and a `file:` UI tarball.
- 9 of 29 backends boot through `AddApiDefaults()`; 20 map `/health` by hand.
- 4 frontends are React-only, 2 run Vue beside a legacy React app.
- 1 product uses tabler icons; no product uses `LoadingOverlay`.
- 1 repo calls the shared publish workflow; 5 copy it; 26 publish nothing.
- 6 apps ship a favicon, 2 a pre-paint theme script, 8 show the version.
- 5 repos keep the design spec at its path.
