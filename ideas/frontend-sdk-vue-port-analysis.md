# Frontend SDK → Vue — port analysis & pilot plan

*Last updated: 2026-08-10*

> **Status:** analysis, nothing built. Subject = `@wow-two-beta/ui` at `0.0.104`
> (`wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-beta-sdk`).
> Answers three questions: what the SDK actually is, what a Vue port costs, and whether it goes in this repo
> or a new one. Every figure below was **measured off the working tree on 2026-08-10** — file counts, LOC,
> `import` closures, consumer symbol sets. Not recalled.
>
> Driver: the developer knows Vue better than React and finds it more direct. React was chosen originally
> because Vue had thinner library coverage — a premise this analysis re-tests against the SDK's real
> dependency surface.
>
> Companion vector spun out of the same session: [nth26-map-vector-analysis.md](nth26-map-vector-analysis.md).

---

## 1 · Verdict

- **Don't port the whole SDK.** Parity across 237 components ≈ the original 14-week build, for zero current
  Vue consumers.
- **Do extract `packages/core`** — the ~37k agnostic LOC. Pays off for React today; halves any later port.
- **Do run the forever-pin pilot.** Its slice is 30% of the SDK and covers ~84% of what *every* current
  consumer imports.
- If Vue wins the pilot, the marginal cost of covering all 9 existing apps is **3,878 LOC**.
- Repo shape: **same repo, monorepo** (`core` / `react` / `vue`). A separate repo without a shared core
  forks 37k LOC of logic and guarantees drift.

---

## 2 · What the SDK is

| Metric | Value |
|---|---|
| `src/` total | **79,673 LOC · 1,001 files** |
| React-coupled | 42,785 LOC (54%) |
| Framework-agnostic | 36,888 LOC (46%) |
| Subpath exports | 65+ |
| Components | 237 |
| `foundation/` modules | 41 (+ 18 primitives, 18 hooks) |
| `tests/` | 433 files · ~59,000 LOC |
| Build history | 232 commits, `2026-04-28` → `2026-08-05` (~14 weeks) |

Component groups: `forms` 79 · `display` 73 · `feedback` 27 · `layout` 24 · `actions` 14 · `nav` 11 ·
`overlays` 9.

### The layering already favours a port

- `foundation/` — 34,244 LOC, only **23% React-coupled**. The house pattern is *engine in plain TS + a thin
  `useX` binding*; `foundation/geolocation/index.ts` states it outright: "React appears only in the two
  `Use*` modules".
- `presentation/` — 36,748 LOC, **87% React-coupled**. This is the rewrite.
- 17 of 41 `foundation` modules import React **zero** times: `async` `collections` `config` `crypto`
  `datetime` `errors` `files` `format` `http` `idb` `identifiers` `logger` `resilience` `shortcuts`
  `storage` `themes` `validation` — ~11,474 LOC.

### Free-riding layers (copy verbatim, no React anywhere)

| Layer | LOC |
|---|---:|
| 36 × `*.variants.ts` (`tailwind-variants` config) | 2,536 |
| `foundation/themes/` (OKLCH engine, tokens, CSS gen) | 2,403 |
| `domain/` (`color`, `emoji`) | 2,089 |
| `analytics/` | 510 |

Visual parity across frameworks therefore costs nothing — the design system is data, not components.

---

## 3 · React idioms, by difficulty

| Idiom | Files | Vue path |
|---|---:|---|
| `forwardRef` | 233 | **deletes** — attr fallthrough + `defineExpose` |
| `ReactNode` types | 148 | slot types |
| `createContext` / `useContext` | 43 | `provide` / `inject` — mechanical |
| `asChild` / `Slot` | 31 | **rewrite** — no runtime prop-merge; `reka-ui`-style vnode clone |
| `useSyncExternalStore` | 18 | `shallowRef` + subscribe — mechanical |
| `Children.*` traversal | 15 | **re-architect** — Vue slots are functions, not element arrays |
| `cloneElement` | 11 | folded into the `Slot` rewrite |
| `useImperativeHandle` | 10 | `defineExpose` |
| `createPortal` | 1 | `<Teleport>` |

`Children.*` and `asChild` are the only genuine re-architecture. They surface in compound components that
inspect or annotate their children — `ButtonGroup`, `OptionTileGroup`, `ControlGroup`, `RovingFocusGroup`.
Target shape: context registration via `provide`/`inject` instead of child inspection.

---

## 4 · The "Vue has fewer libraries" premise no longer holds here

The SDK carries **8 runtime dependencies**. All 8 are agnostic or have Vue equivalents.

| Dependency | Files | Vue path |
|---|---:|---|
| `@floating-ui/react` | **1** | `@floating-ui/vue` — only `useFloating/offset/flip/shift/size/autoUpdate` used |
| `@radix-ui/react-focus-scope` | 6 | `reka-ui` FocusScope |
| `lucide-react` | 61 | `lucide-vue-next`, 1:1 |
| `marked`, `temporal-polyfill` | 21 | agnostic, no change |
| `clsx`, `tailwind-merge`, `tailwind-variants` | — | agnostic, no change |
| `react-router-dom` (peer) | 20 | `vue-router` — different model, redesign |
| `@tanstack/react-query` (peer) | 18 | `@tanstack/vue-query` |
| `@tanstack/react-form` (peer) | 2 | `@tanstack/vue-form` — adapter redesign |

App-level: `maplibre-gl` agnostic · `@tanstack/react-table` → `vue-table` · `@tabler/icons-react` →
`@tabler/icons-vue`.

The interaction layer (`dismissableLayer`, `focusScope`, `rovingFocusGroup`, `presence`, `portal`,
`anchoredPositioner`) is **hand-built in this SDK**, not imported. That self-reliance is exactly what
removes the library-count argument.

---

## 5 · Consumer depth — the lock-in is much lower than "10 apps" implies

Measured across every frontend importing `@wow-two-beta/ui`:

| App | files | LOC | SDK files | symbols | pinned |
|---|---:|---:|---:|---:|---|
| `forever-pin` | 134 | 6,880 | 42 | **94** | `0.0.97` |
| `transcript-forge` | 45 | 2,787 | 12 | 57 | `^0.0.90` |
| `museums-gallery` | 127 | 8,348 | 41 | 39 | `0.0.104` |
| `drydock` | 17 | 1,475 | 7 | 18 | `0.0.95` |
| `secrets-vault` | 21 | 1,556 | 12 | 17 | `0.0.95` |
| `prism` | 126 | 28,171 | 5 | 11 | `0.0.62` |
| `nth26` | 272 | 23,008 | 5 | 9 | `0.0.104` |
| `tbs` | 235 | 19,561 | 5 | 9 | `0.0.104` |
| `haven` | 52 | 6,737 | 3 | 4 | `^0.0.54` |

- The **biggest** apps are the **shallowest** SDK users. `nth26` 2% of files · `tbs` 2% · `haven` 6% ·
  `prism` 4%.
- Big apps carry their own UI layer: `nth26` → `@nth26/shared` + `@tabler/icons-react`; `haven` →
  `@haven/ui` + `@haven/app-ui` + `cva`.
- Deep usage lives in the small apps: `forever-pin` 94 symbols · `transcript-forge` 57 · `museums-gallery` 39.
- ⚑ **`haven` is already broken on bump** — pinned `^0.0.54`, imports `@wow-two-beta/ui/{actions,forms,hooks}`,
  subpaths absent from the `0.0.104` export map. Fix independently of any Vue decision.
- Losing `forever-pin` to Vue removes the React SDK's only deep real-world validator.

---

## 6 · Port scope, by import closure

Transitive closure over the SDK, seeded from each app's imported symbols, dependencies followed:

| Scope | files | LOC | React to rewrite | copy verbatim |
|---|---:|---:|---:|---:|
| **forever-pin slice** | 346 | 20,145 | 13,681 | 6,464 |
| **all-9-apps slice** | 410 | 24,023 | 16,326 | 7,697 |
| Marginal cost of full coverage | +64 | **+3,878** | +2,645 | +1,233 |

- All-9 needs **85 component folders**: `display` 26 · `forms` 21 · `layout` 15 · `actions` 9 ·
  `feedback` 9 · `overlays` 4 · `nav` 1.
- Versus the full SDK: **30% of LOC, 36% of components.**
- forever-pin's seed was 47 component folders from its 94 symbols (glyph components not seeded) — treat
  20,145 as a floor.

forever-pin slice by area — `presentation/forms` 4,726 · `layout` 2,769 · `actions` 2,439 · `overlays` 2,056 ·
`domain/emoji` 1,970 · `display` 1,759 · `foundation/primitives` 1,407 · `utils` 1,315 · `hooks` 997 ·
`feedback` 366 · `storage` 274 · `icons` 67.

Scoping the pilot by forever-pin lands most of the consumer surface by accident. That is the finding that
makes the pilot worth running.

---

## 7 · Repo shape

- **A · same repo, extract shared core** — `packages/core` (agnostic) → `packages/react` + `packages/vue`.
  One token/variant/logic source, one release train, parity enforced by proximity. Cost: restructure 65
  subpath exports; churn for live React consumers during extraction.
- **B · separate repo `wow-two-sdk-beta.ui-vue`** — zero risk to live consumers, independent cadence. Without
  core extraction first it forks 37k LOC and drifts. Cross-repo bump friction is a known cost
  (`pnpm file:` stale-sync).
- **C · same repo, new package, no extraction** — fastest start, same drift as B with none of the isolation.

**Pick A.** Its first half — the core extraction — is worth doing whether or not Vue ever happens: it makes
pure logic testable without a DOM and opens Svelte / web components / SSR later.

---

## 8 · Risks

- **Double rewrite** — finishing `forever-pin`'s React frontend, then rewriting it in Vue, pays for the frontend
  twice. Bounded at 6,880 LOC, but real. Freeze it at *working*, don't polish.
- **`forms-engine` is the one hard non-component piece** — `AppForm` + `useFieldArray` +
  `defaultMapFieldPath` sit on `@tanstack/react-form`; the Vue adapter is a redesign.
- **`asChild` / `Children.*` land inside the pilot slice** — `ToggleButtonGroup`, `OptionTileGroup`,
  `ControlGroup`.
- **Two SDKs, one maintainer** — if Vue succeeds and React apps stay, every new component is built twice.
  Decide at the pilot's end; don't straddle.
- **Test layer doesn't transfer** — 433 files / ~59k LOC of RTL + Playwright + story-interaction tests are
  React-bound. The a11y suite and Storybook catalog rebuild, not share.
- **Doctrine tension** — `conventions/development/dev-cycle.md` § *Vector completeness* says build the whole
  vector. Across 2 frameworks that doubles the completeness bar. Name the exception explicitly if taken.

---

## 9 · Sequence

1. **Finish `forever-pin`** backend + logic. Freeze the React frontend at working.
2. **Extract `packages/core`** in the UI repo — the ~7.7k agnostic LOC inside the consumer closure:
   `*.variants.ts`, `foundation/themes`, `domain/{color,emoji}`, `foundation/{http,storage,utils}` types.
   Benefits React immediately.
3. **Build `@wow-two-beta/ui-vue` v0.1** against `core` — scope to the ~47 folders forever-pin needs, not 85.
4. **Port the `forever-pin` frontend to Vue.** Same theme, same API names. Measure honestly against React.
5. **Decide.** If Vue wins, the +3,878 LOC covering all 9 apps is the follow-on.

### Open questions

- Preserve the React SDK's exact API names in Vue, or redesign props idiomatically at the seam?
- Does `core` ship as a published package, or stay a workspace-internal package the two adapters bundle?
- Where does the a11y contract live once tests no longer transfer — in `core`, or duplicated per adapter?
