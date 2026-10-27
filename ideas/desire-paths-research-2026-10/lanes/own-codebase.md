# Desire paths in our own codebase — products working around the fe sdk (`@wow-two-beta/fe`)

Scope and method (read-only, 2026-10-27). Consumers = every `package.json` under `wow-two-ws/workbench/` that depends on
`"@wow-two-beta/fe"`, minus `node_modules`, `dist`, the SDK's own `apps/atlas` + `apps/playground`, and the parked React
package. That gives **35 apps in 30 repos**: 25 products (Haven has 5 apps, TNIS 2) plus 5 template/domain sample apps
(product-template, domain-template, identity, files, harvest). Counts below say "apps" unless noted; where apps ≠
products the product count is given.

- **Full coverage (mechanical):** an import parser
  over every `src/**/*.vue|ts` (tests excluded) in all 35 apps. It handles multi-line imports and both quote styles, and
  builds the SDK-symbol usage matrix. Pattern greps ran over the same files, plus each app's `vite.config.ts`,
  `index.html` and `bootstrap/index.css`.
- **Not in the matrix:** Haven's shared `packages/shell` sits outside `apps/` and was read separately.
- **Sampled (read by hand):** vendor-renewals and Wheelhouse `AppLayout.vue`; vendor-renewals `AccountMenu.vue`,
  `UseSessionGate.ts`, `FailureMessages.ts`, `ColorMode.ts`, `vite.config.ts` and `index.html`; listing-shelf
  `PageHeading.vue`; TNIS `Section.vue`; Haven `HavenShell.vue`, `AppRoot.vue` and `Router.ts`; the SDK specs for
  AppShell, PageHeader, AccountMenu, BottomNavMenu, DataRegion, Navbar, RoutePageHeader and ScrollRestoration; the SDK
  backlog; the workspace shell convention.
- **Not surveyed:** consumers of the legacy package name `@wow-two-beta/ui-vue` (Secrets Vault `0.0.7`,
  wheelhouse-canary `0.0.6`, home-atlas, med-text-fab, mintrans client apps).

Path shorthand: `{repo}:{app}` = `workbench/…/{repo}/engineering/codebase/{slug}.frontend-services/apps/{app}/src/`.
Repo roots, relative to `wow-two-ws/workbench/`:
- `maxs-projects/ventures/saas/{ventures.vendor-renewals | ventures.listing-shelf | ventures.tnis | 10x-ven-haven | 10x-venture-forever-pin | 10x-ventures-prism | 10x-ventures-transcript-forge | sift | ventures.*}`
- `maxs-projects/ventures/consumer/{ventures.arcade | ventures.hijinx | ventures.matinee | ventures.museums-gallery | ventures.pose-coach}`
- `wow-two-platform/wow-two-platform.wheelhouse`
- SDK source: `wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/codebase/wow-two-sdk-beta-fe/src/` (cited as `SDK/…`)
- SDK planning: `wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/planning/` (cited as `SDK-plan/…`)

## What does the SDK already export for shell, layout, navigation and feedback (the comparison baseline)?

### Takeaway
The SDK (`0.0.33`) already ships almost every shell part a product needs. That covers the frame, page header, top bar,
sidebar, bottom bar, account menu, app switcher, command palette, region-aware scroll restoration, document titles,
data-region states and a toast bus. What it lacks is the **assembly**: no part turns one list of destinations into a
top bar plus a bottom bar, and none covers the session gate, the version badge, the pre-paint theme plumbing or
mutation feedback. Products pin `0.0.26`–`0.0.28`, so several recent SDK parts are unadopted.

### Cited Findings
- **Layout exports:**
  - `AppShell` with `AppShellHeader`, `Sidebar`, `Main`, `Content`, `Aside` and `Footer` — [SDK/presentation/layout/appShell/](SDK/presentation/layout/appShell/AppShell.spec.md).
  - AppShell's props are `sidebarWidth`, `asideWidth`, `sidebarBreakpoint`, `asideBreakpoint`, `sidebarOpen`, `scroll: region|document` and `navigation` (inferred from whether a sidebar is present). By default `AppShellMain` is the one scroll container — [AppShell.spec.md](SDK/presentation/layout/appShell/AppShell.spec.md).
  - `PageHeader` + `PageHeaderActions`: actions teleport into "the most recently mounted `PageHeader`" through a per-app outlet — [PageHeader.spec.md](SDK/presentation/layout/pageHeader/PageHeader.spec.md), [PageHeaderOutlet.ts:1-18](SDK/presentation/layout/pageHeader/PageHeaderOutlet.ts).
  - The rest: `Navbar`, `ListDetailLayout`, `CanvasArea`, `ResizablePanelsLayout`, `TwoColumnLayout`, `StickyLayout`, `Section`, `ScrollArea` and others — [SDK/presentation/layout/index.ts](SDK/presentation/layout/index.ts).
- **Nav exports:** `SidebarMenu` (Group/Item/Section), `BottomNavMenu`(+Item), `Breadcrumb`, `AppSwitcherMenu`, `AccountMenu`, `NavItem`, `NavigationMenu`, `Menubar`, `DropdownMenu`, `ContextMenu`, `Pagination`, `ScrollSpy`, `TableOfContents` — [SDK/presentation/nav/index.ts](SDK/presentation/nav/index.ts).
- **Overlay exports:** `CommandPaletteModal` (Content/Input/List/Group/Item/Empty/Separator), `Modal`, `AlertModal`, `TypedConfirmModal`, `ConfirmPopover`, `Drawer`, `BottomSheet`, `ActionSheet`, `TourPopover` — [SDK/presentation/overlays/](SDK/presentation/overlays/index.ts).
- **Feedback exports:**
  - `DataRegion`, `LoadingState`, `SkeletonState`, `SplashScreen`, `FeedbackToastHost`, `ToastHost`, `UndoBar`, `ErrorBoundary`, `Alert`, `Banner`, `Callout` — [SDK/presentation/feedback/index.ts](SDK/presentation/feedback/index.ts).
  - `EmptyState` lives under display.
  - DataRegion's contract: one region per loading unit, skeleton-first load, a stale-keeping refresh, failure text left to the toast host, and opt-in retry — [DataRegion.spec.md](SDK/presentation/feedback/dataRegion/DataRegion.spec.md).
- **Toolbar** exists as `SDK/presentation/actions/toolbar` — [SDK/presentation/actions/](SDK/presentation/actions/index.ts).
- **`/router`:**
  - `createAppRouter` installs `installDocumentTitle`, `installDocumentMeta`, `installRoutePersistence` and `installPageViewTracker`, and folds in scroll behaviour.
  - It also exports `RoutePageHeader`, `AppErrorBoundary`, `NavigationProgress`, `RouteAnnouncer`, `NotFound`, `AppLink`, `AppNavLink`, `useBreadcrumbs`, `requireAuth`, `useNavigationBlocker` and `lazyPage`.
  - Source: [SDK/router/adapters/vueRouter/index.ts](SDK/router/adapters/vueRouter/index.ts).
- **Scroll restoration covers the AppShell region.** The main region of a `region` AppShell "follows the same policy" as the window (top on a new entry, restored on back/forward) — [ScrollRestoration.ts:36-40](SDK/router/adapters/vueRouter/ScrollRestoration.ts). This landed in `8f50655b` "restored and reset the app shell region scroll on navigation" (2026-10-15) — `git log -S ScrollRegionAttribute` in the fe repo.
- `RoutePageHeader` renders a `PageHeader` whose title and description follow the deepest route `handle.title` / `handle.description` — [RoutePageHeader.spec.md](SDK/router/adapters/vueRouter/routePageHeader/RoutePageHeader.spec.md).
- **`AccountMenu` already holds:** identity, an organization switcher, an items slot, appearance (System/Light/Dark bound to `ColorModeProvider`), language, per-service versions and sign-out — [AccountMenu.spec.md:3-32](SDK/presentation/nav/accountMenu/AccountMenu.spec.md).
  - It shipped in `c852036d` "added an AccountMenu for suite account, appearance and versions" (2026-10-20 18:00 +0500, i.e. 13:00 UTC).
  - That came after the `0.0.27` release (`42ec8657`, 2026-10-20 12:06 UTC), so the first release containing it is `0.0.28` — fe repo `git log`.
- **`/auth`** offers `AuthProvider`, `useAuth` and `createAuthBridge`. It states that "gates, splash screens, and login pages stay app-side" — [SDK/auth/index.ts:1-13](SDK/auth/index.ts).
- **`/feedback`:** `notify({ tone, title })`, `feedbackBus` and `feedbackQueryErrors()` — [SDK/feedback/index.ts:1-30](SDK/feedback/index.ts).
- **Foundation:**
  - `shortcuts` (`useHotkeys`, `useHotkeyMap`) and `commands` (`CommandRegistry`, `useCommandRegistry`, `useCommandShortcuts`) — [SDK/foundation/shortcuts/index.ts](SDK/foundation/shortcuts/index.ts), [SDK/foundation/commands/hooks/](SDK/foundation/commands/index.ts).
  - `colorModeScript()` returns the source of a pre-paint script, to "inline … or write it to a static file". It is a string, not a build plugin — [ColorModeScript.ts:1-30](SDK/foundation/primitives/colorModeProvider/ColorModeScript.ts).
- **Pinned versions:**
  - `0.0.26`: matinee, museums-gallery, forever-pin, prism.
  - `0.0.27`: most ventures, all 5 Haven apps and TNIS.
  - `0.0.28`: sift, file-watch, procedure-review.
  - `0.0.32`: the domain repos. `0.0.33`: Wheelhouse. `0.0.24`: product-template.
  - The SDK itself is at `0.0.33`.
  - Source: each app's `package.json`.
- **Adoption matrix** (apps of 35 importing each symbol from the SDK):

  | Uptake | Symbols (apps of 35) |
  |---|---|
  | Broad | `createAppRouter` 28 · `ColorModeProvider` 25 · `AppShell` 23 · `RouteAnnouncer` 23 · `useColorMode` 22 · `Navbar` 22 · `FeedbackToastHost` 22 · `notify` 22 |
  | Middle | `AppErrorBoundary` 19 · `SplashScreen` 19 · `useAppQuery` 18 · `DataRegion` 15 · `useAppMutation` 15 · `EmptyState` 14 · `NavigationProgress` 12 · `BottomNavMenu` 11 · `NavItem` 11 · `DataTable` 8 · `PageHeader` 7 · `AlertModal` 7 · `ConfirmPopover` 5 |
  | Thin | `ListDetailLayout` 4 · `AccountMenu` 3 · `SidebarMenu` 2 · `AppShellSidebar` 2 · `AppShellFooter` 1 · `CommandPaletteModal` 1 · `Breadcrumb` 1 · `RoutePageHeader` 1 · `PageHeaderActions` 1 · `TypedConfirmModal` 1 |
  | None in `apps/` | `Toolbar`, `AppSwitcherMenu`, `useBreadcrumbs`, `NavigationMenu`, `Menubar` |

  Haven's `packages/shell` adds one product each to `AppShell`, `Navbar`, `BottomNavMenu`, `AccountMenu` and `AppSwitcherMenu`. Source: the import parser run over the consumers (method above).

### Pattern ledger (cross-question summary; evidence in the sections below)

| # | Desire path | Apps (products) | SDK status |
|---|---|---|---|
| D1 | Hand-assembled `AppLayout.vue` frame (brand, version, destinations ×2, account menu, bottom bar) | 23 apps (22 products) + Haven's package | Parts exist; no assembly |
| D2 | Manual `scrollTo({ top: 0 })` watch on route change | 16 | **Paved, not adopted** (`8f50655b`, 2026-10-15) |
| D3 | BottomNavMenu forced into the shell grid with `[grid-area:footer]` | 11 | Unpaved: `AppShellFooter` has no props, used once |
| D4 | One destinations list rendered twice (top bar + bottom bar) with a hand-written active check | 10 (`const Destinations`) + Haven `places` | Unpaved |
| D5 | Version-label regex `/^\d/.test(v) ? 'v'+v : v` | 24 (23 products) | Unpaved for the bar; AccountMenu takes `versions` |
| D6 | Hand-built account / appearance menu (DropdownMenu + MenuRadioGroup + useColorMode) | 14 (+ transcript-forge) | **Paved in `0.0.28`, adopted by 3 apps + Haven** |
| D7 | Session gate: phase machine + splash / failure / sign-in screens | 7 `UseSessionGate.ts`, 5 `SignInGate`, 3 `SessionFailureState` | Explicitly left app-side |
| D8 | Pre-paint theme: local Vite `themeScript()` plugin + `ColorMode.ts` key | 28 vite configs (23 local plugins), 22 key files | Half-paved: script source only |
| D9 | Page header hand-built (`<h1>` + description + actions row) | 33 apps / 105 `*Page.vue` vs PageHeader in 7 apps / 19 files | Paved (`PageHeader`, `RoutePageHeader`); wrap bug in backlog |
| D10 | Manual `document.title` despite `installDocumentTitle` | 7 apps (4 products) | Paved (Haven skips `createAppRouter`) |
| D11 | Mutation feedback: `if (!result.ok) notify(Danger…) else notify(Success…)` + local `FailureMessages.describe` | 22 apps / 64 files; mapper in 10 | Unpaved (backlog: AppError rendering) |
| D12 | Domain confirm / delete modals over AlertModal; delete-account-with-password modal | 7 apps; 3 products for delete-account | Primitives exist; no recipe |
| D13 | Local toolbars; SDK `Toolbar` unused | 3 products | Paved, 0 adopters |
| D14 | Re-implemented glass chrome material | 4 apps | Partly paved (`variant="glass"`); strength not a token |
| D15 | Typing bypass `v-bind="{ 'aria-label': … }"` on SDK parts | 26 sites in 4 apps | Unpaved: props types omit `aria-label` |

## Which local components duplicate or wrap SDK components, and which recur across 3+ products?

### Takeaway
The recurring duplicates are frame-level, not widget-level. Each product hand-writes the `AppLayout`, an
account/appearance menu (14 apps re-create what SDK `AccountMenu` now does), a session gate with sign-in and failure
screens, page headings, and per-domain confirm/delete modals. Tables and empty states are mostly SDK-backed already.
Several duplicates are byte-identical across products, which points to copy-paste between siblings rather than
independent design.

### Cited Findings
- **D1 — `AppLayout.vue` in `bootstrap/` in 23 apps, 56–237 lines each.** All compose SDK
  `AppShell`/`AppShellHeader`/`AppShellMain` (22 also `Navbar`) — import parser over `{repo}:{app}/bootstrap/AppLayout.vue`.
  - Sizes: museums-gallery 237, listing-shelf 204, Wheelhouse 202, forever-pin 133, procedure-review 130, file-watch 124, customer-promises 112, vendor-renewals 112, sift 110, … hijinx 56.
  - The exceptions: Arcade (`ventures.arcade:web/presentation/shell/pages/ArcadeShell.vue`, 62 lines, no SDK shell, a Telegram Mini App); Haven (a shared package, below); TNIS showcase (`AppRoot.vue`); and the 5 template/domain apps, which have no frame.
- **The product template ships no frame.** `wow-two-sdk-beta.product-template:web` holds only `bootstrap/AppRoot.vue` + `presentation/greetings/pages/GreetingPage.vue`. It pins `@wow-two-beta/fe` `0.0.24`, does not call `createAppRouter`, and its page header is a hand row: `<header class="flex flex-wrap items-center gap-3"><h1 class="text-3xl font-semibold">` with app/api version badges — [GreetingPage.vue:16-22](wow-two-sdk-beta/wow-two-sdk-beta.product-template/engineering/codebase/sample.frontend-services/apps/web/src/presentation/greetings/pages/GreetingPage.vue).
- **Haven is the one product that extracted its frame.** [haven.frontend-services/packages/shell/src/HavenShell.vue](maxs-projects/ventures/saas/10x-ven-haven/engineering/codebase/haven.frontend-services/packages/shell/src/HavenShell.vue) (137 lines):
  - It takes a `places` prop and renders it twice — as `NavItem`s in the `Navbar` (:97-101) and as a `BottomNavMenu` (:123-129).
  - It adds `AppSwitcherMenu` across Haven's internal apps (:87), SDK `AccountMenu` (:107), `SplashScreen`, `ColorModeProvider`, `FeedbackToastHost`, and `AppShell scroll="document"` (:82).
  - All 5 Haven apps mount it, e.g. `<HavenShell app="web" product="CRM" :places="places">` — [haven:web/bootstrap/AppRoot.vue](maxs-projects/ventures/saas/10x-ven-haven/engineering/codebase/haven.frontend-services/apps/web/src/bootstrap/AppRoot.vue), and likewise `haven:admin/bootstrap/AppRoot.vue`.
- **D6 — 14 apps hand-build an appearance menu** from `DropdownMenu` + `MenuRadioGroup` + `useColorMode`, all on pins below 0.0.28:
  - The files: `pose-coach:web/presentation/shell/ConsoleMenu.vue` (75 lines), `forever-pin:web/presentation/identity/AccountMenu.vue` (93), `prism:web/presentation/shell/AppearanceMenu.vue` (57), `config-checker:web/presentation/identity/AccountMenu.vue` (84), `customer-promises:…/AccountMenu.vue` (85), `epub-review:…/AccountMenu.vue` (90), `listing-shelf:web/presentation/common/components/AppMenu.vue` (77), `pbn-studio:web/presentation/shell/components/ColorModeMenu.vue` (53), `podcast-readiness:…/AccountMenu.vue` (84), `surface-pattern:web/presentation/system/SettingsMenu.vue` (72), `tnis:studio/presentation/common/components/AboutMenu.vue` (68), `training-seats:…/AccountMenu.vue` (90), `vendor-renewals:…/AccountMenu.vue` (85) and `wheelhouse:web/presentation/shell/components/ProfileMenu.vue` (139).
  - `transcript-forge:web/presentation/common/AppProfileMenu.vue` (122) uses `DropdownMenu` + `useColorMode` too.
  - Source: a grep for files holding both `MenuRadioGroup` and `useColorMode`.
- **The 7 local files named `AccountMenu.vue` rebuild the SDK AccountMenu's own sections without importing it.**
  - vendor-renewals carries an avatar trigger, an email label, an `App {v} · API {v}` line with a 7-char commit shortener, Light/Dark/System radio rows, and a destructive sign-out — [vendor-renewals:web/presentation/identity/AccountMenu.vue:1-85](maxs-projects/ventures/saas/ventures.vendor-renewals/engineering/codebase/vendor-renewals.frontend-services/apps/web/src/presentation/identity/AccountMenu.vue).
  - The SDK AccountMenu spec lists the same sections — [AccountMenu.spec.md:21-32](SDK/presentation/nav/accountMenu/AccountMenu.spec.md).
  - Only the 3 apps on `0.0.28` import the SDK one, e.g. `procedure-review:web/bootstrap/AppLayout.vue:22,53,108` (`AccountMenu`, `AccountMenuVersion[]`, `<AccountMenu :name … :versions … @sign-out>`), plus sift and file-watch.
- **Wheelhouse's phone account surface is a second local build:** `wheelhouse:web/presentation/shell/components/ProfileSheet.vue` (105) combines `BottomSheet` + `SidebarMenu` + `ToggleGroup` + `useColorMode` — import parser. SDK backlog asks for "Ability to size `BottomSheet` to its content | Wheelhouse's profile sheet uses a fixed 540px" — [SDK-plan/backlog.md:149](SDK-plan/backlog.md).
- **D7 — the session gate is hand-built in every signed-in venture.** The SDK says it stays app-side ([SDK/auth/index.ts:12-13](SDK/auth/index.ts)).
  - `application/identity/UseSessionGate.ts` exists in 7 apps, 61–110 lines: forever-pin (110), config-checker (83), customer-promises (92), file-watch (61), podcast-readiness (83), procedure-review (61), vendor-renewals (88).
  - `SignInGate.vue` in 5: forever-pin, config-checker, customer-promises, podcast-readiness, vendor-renewals.
  - `SessionFailureState.vue` in 3: forever-pin 44, customer-promises 17, vendor-renewals 17.
  - `SignInScreen.vue` in 3: documentation-checker, retainer-balance, wheelhouse.
  - The gate maps `useAuth` into a `SessionPhase` of Checking / Failed / Gate / Ready, with retry, submit and sign-out — [vendor-renewals:web/application/identity/UseSessionGate.ts:1-40](maxs-projects/ventures/saas/ventures.vendor-renewals/engineering/codebase/vendor-renewals.frontend-services/apps/web/src/application/identity/UseSessionGate.ts).
  - The layout renders the three phases before the frame — [vendor-renewals:web/bootstrap/AppLayout.vue:50-66](maxs-projects/ventures/saas/ventures.vendor-renewals/engineering/codebase/vendor-renewals.frontend-services/apps/web/src/bootstrap/AppLayout.vue).
- **The copying is literal:**
  - `SignInScreen.css` in documentation-checker and retainer-balance compares byte-identical (`diff -q`) — `{repo}:web/presentation/identity/SignInScreen.css`.
  - `application/common/FailureMessages.ts` in customer-promises and vendor-renewals is byte-identical (`cmp`); config-checker's and podcast-readiness's differ.
  - customer-promises and vendor-renewals `AppLayout.vue` are both 112 lines, and their `SessionFailureState.vue` files are both 17 lines.
- **Page heading component re-implemented:** `listing-shelf:web/presentation/common/components/PageHeading.vue` (33 lines) instead of SDK `PageHeader`. It differs in flex-wrap actions, an `eyebrow` slot, and an `<h1 tabindex="-1" data-page-heading>` focus target — [PageHeading.vue:17-31](maxs-projects/ventures/saas/ventures.listing-shelf/engineering/codebase/listing-shelf.frontend-services/apps/web/src/presentation/common/components/PageHeading.vue). Related local headers: `wheelhouse:web/presentation/product/ProductHeader.vue` (95), `tnis:studio/presentation/network/panels/ScenarioHeader.vue` (123), `haven:landing/presentation/sections/SectionHeading.vue` (12).
- **D12 — confirm/delete modals per domain, built on SDK `AlertModal`/`Modal`:**
  - `forever-pin:…/codes/list/DeleteCodeModal.vue` (58), `transcript-forge:…/common/ConfirmModal.vue` (64), `listing-shelf:…/pipelines/components/PipelineDeleteModal.vue` (67).
  - `epub-review:…/identity/DeleteAccountModal.vue` (78) and `training-seats:…/identity/DeleteAccountModal.vue` (76) — both `AlertModal` + `PasswordInput`.
  - `procedure-review:…/identity/components/AccountDeleteModal.vue` (61, `Modal` + `PasswordInput` + `Alert`).
  - `wheelhouse:…/common/components/DeleteConfirm.vue` (39, `ConfirmPopover`) and `…/deployments/components/ControlConfirmModal.vue` (149).
  - Source: the import parser. A delete-account-with-password modal recurs in 3 products. SDK `TypedConfirmModal` is used by 1 app.
- **D13 — local toolbars, SDK `Toolbar` imported by 0 apps:** `prism:web/presentation/studio/StudioToolbar.vue` (211; `Button`, `SegmentedPicker`, `ToggleInput`), `tnis:studio/presentation/network/controls/ToolBar.vue` (84; no SDK import, local `ToolButton` + `HoverPopover`), `haven:web/presentation/listings/components/ResultsToolbar.vue` (124; `SearchInput`, `SelectPicker`, `ToggleGroup`) — import parser.
- **Tables mostly use the SDK:** `DataTable` in 8 apps, e.g. `haven:web/…/ListingsTable.vue` and `config-checker:web/…/ComparisonTable.vue`; `forever-pin:web/…/ComparisonTable.vue` uses `Table*`. Hand tables without SDK imports appear in only 2 apps: `tnis:studio/…/panels/AffectedRoutesTable.vue` (133) and `museums-gallery:web/…/overview/MuseumMapTable.vue` (52).
- **Marketing/landing frames are local in 2 products:** `forever-pin:web/bootstrap/MarketingLayout.vue` (78), `…/marketing/MarketingSection.vue`, `MarketingFooterSection.vue`, `PricingTierCard.vue`; and Haven landing `SiteHeader.vue` (64), `SiteFooter.vue` (51), `HeroSection.vue`, `PricingSection.vue`, `FeaturesSection.vue`. TNIS showcase has `PitchSection.vue`/`ProductSection.vue`. SDK `PricingCard` and `FeatureCard` are each imported by 1 app.

### Inferences
- **The recurring unit is the frame plus identity chrome, not individual widgets.** The 3+-product duplicates are
  `AppLayout` (22 products), the appearance/account menu (14), the session gate (7), page headers (33 apps), the
  delete-account modal (3) and toolbars (3).
- **The AccountMenu shows the SDK can pave a desire path after the fact.** It was apparently extracted from these
  menus — its commit names "suite account, appearance and versions". Adoption stalls on version pins: 11 of the 14
  apps sit below `0.0.28`.
- **The product template seeds the drift.** It has no frame, an old SDK pin and a hand header row, so each product
  starts by copying a sibling's `AppLayout`/`AccountMenu`/`UseSessionGate`. The byte-identical files support this
  inference; no commit history was checked to prove the copy direction.
- **Haven's `HavenShell` is the closest existing prototype** of a "places-driven shell" the SDK could offer.

### Gaps
- No git-history check of when each local `AccountMenu`/`AppLayout` was written relative to the SDK releases.
- Legacy `@wow-two-beta/ui-vue` consumers (Secrets Vault, wheelhouse-canary, home-atlas, med-text-fab) were not surveyed; Secrets Vault is a platform app and probably carries its own frame.
- Line counts measure size, not semantic duplication; only the vendor-renewals pair was read in full.

## Where do products override or re-theme SDK components, or bypass their APIs?

### Takeaway
Hard overrides (`:deep`, `!important` on SDK parts) are rare and concentrated in TNIS studio and two sign-in screens.
The more telling override is structural: 11 apps reach into AppShell's private grid with `[grid-area:footer]`, and
4 apps re-implement the glass chrome material. The commonest API bypass is typing: products pass `aria-label`
through `v-bind="{…}"` because the SDK props types omit it.

### Cited Findings
- **D3 — `<BottomNavMenu :is-fixed="false" class="[grid-area:footer] md:hidden">` in 11 apps:**
  - matinee `AppLayout.vue:84`, museums-gallery `:165`, forever-pin `:126`, sift `:98`, customer-promises `:100`, file-watch `:115`, listing-shelf `:197`, procedure-review `:121`, vendor-renewals `:100`.
  - transcript-forge `presentation/common/AppTabBar.vue:33` and Wheelhouse `presentation/shell/components/PhoneNav.vue:27`.
  - Source: grep `grid-area:footer`.
  - `AppShellFooter` declares no props and is imported by 1 app (hijinx) — [AppShellFooter.spec.md](SDK/presentation/layout/appShell/AppShellFooter.spec.md).
  - The workspace convention says "must compose it from the SDK `AppShell` and `Navbar`; never hand-roll the grid or the scroll container" — [conventions/development/frontend/shapes/app/shell/shell.md:13](../conventions/development/frontend/shapes/app/shell/shell.md).
- **forever-pin adds a `surface-glass` class onto BottomNavMenu** (`AppLayout.vue:126`). The BottomNavMenu spec warns: "Set the surface through `variant`: a `surface-glass` class beside the solid default loses its fill to the page background" — [BottomNavMenu.spec.md](SDK/presentation/nav/bottomNavMenu/BottomNavMenu.spec.md).
- **D14 — glass material re-implemented in 4 apps:**
  - Wheelhouse: "The console's glass is stronger than the fe SDK `glass` variants … Until glass strength is a theme token, these material roles stay here" — [wheelhouse:web/bootstrap/index.css:37-39](wow-two-platform/wow-two-platform.wheelhouse/engineering/codebase/wheelhouse.frontend-services/apps/web/src/bootstrap/index.css). There are 14 `wh-glass` uses in `.vue` files, e.g. `AppLayout.vue:133` overrides `AppShellHeader variant="glass"` with `border-(--wh-glass-edge) … shadow-(--wh-glass-shadow)`.
  - transcript-forge: 25 `tf-glass` rules in `transcript-forge:web/bootstrap/index.css`.
  - TNIS: "Map overlays — the SDK's glass recipe flattened, in this console's palette" — `tnis:studio/presentation/network/theme.css:296`.
  - The convention mandates glass chrome: "must make the outer chrome glass: `AppShellHeader` / `Navbar` `variant="glass"`, menus and the bottom bar" — [conventions/design/theme/theme-patterns.md:43](../conventions/design/theme/theme-patterns.md).
- **TNIS studio re-skins SDK internals in a 1,610-line `presentation/network/theme.css`:**
  - "SDK tokens, swapped for this console's palette" (:51); "Hides the SDK's own trigger chevron" (:963); `[data-state='open']` / `[data-active='true']` selectors on SDK parts (:160, :972, :1064).
  - Eight `!` utilities on `AccordionGroupTrigger`: `class="!h-full !min-h-0 !pl-2.5 !pr-0 !py-0 !text-[13px] !font-normal !gap-1 …"` — [tnis:studio/presentation/network/primitives/Section.vue:27](maxs-projects/ventures/saas/ventures.tnis/engineering/codebase/tnis.frontend-services/apps/studio/src/presentation/network/primitives/Section.vue). That file also hand-adds a header row with count and actions beside the trigger.
- **The sign-in submit button is forced with `!important` in 2 apps:** `.access-submit { min-height: 48px !important; background: #244c3c !important; color: #fff !important; border-radius: 8px !important }` over SDK `Button class="access-submit"` — `documentation-checker` and `retainer-balance` `presentation/identity/SignInScreen.css:103-107`, `SignInScreen.vue:44`.
- **`!important` totals 8 apps / 32 hits, most not SDK-specific:**
  - Global reduced-motion kill switches in 3 apps: hijinx `bootstrap/index.css:66-67`, matinee `:156-157`, surface-pattern `:78-80`. The SDK `src/index.css` contains a `prefers-reduced-motion` rule (content not inspected).
  - Print CSS: museums `PosterPreview.vue:14-15`, TNIS `theme.css:1547-1604`.
  - One `!text-5xl !leading-[0.95] !font-normal` on a page `<h1>` in matinee `presentation/titles/pages/TitlePage.vue:93`.
- **Rarely used:** `:deep()` 1 hit (hijinx `presentation/rooms/RoomPage.vue:780`); `v-bind="$attrs"` 1 (forever-pin `presentation/common/components/InfoPopover.vue:24`) — grep over all apps.
- **D15 — `aria-label` passed via `v-bind="{ 'aria-label': … }"`: 26 sites in 4 apps.**
  - prism has 22 on `EditableInputInput` and `SelectPickerTrigger`; 17 carry the comment "The input reads aria-label from its attrs; its props type does not list it yet (backlog: SDK adoption)", e.g. `prism:web/presentation/studio/LayersPanel.vue:54-55` and `CompareModal.vue:163-164`.
  - file-watch `AppLayout.vue:115` and procedure-review `AppLayout.vue:121` do it on `BottomNavMenu`, though the BottomNavMenu spec says the bar's name "is the caller's `aria-label`".
  - pbn-studio `DrillColorPicker.vue:37`.
  - Related SDK backlog row: "Fix `@vue-ignore` props breaking `strictTemplates` | ListingShelf, Haven" — [SDK-plan/backlog.md:98](SDK-plan/backlog.md).
- **The SDK backlog already logs many Wheelhouse-local overrides as product-reported gaps** — [SDK-plan/backlog.md:126-160](SDK-plan/backlog.md):
  - `SectionHeading` sized via `[&_h2]` (:129); `DescriptionGroup` labels via `[&_dt]:text-xs` (:130).
  - `NavItem` chip variant via local classes (:150); a `StatCard` trend row fixed by a local class (:151).
  - `DialogFooter` `sm:justify-end` overridden to keep Delete left (:153); `SortableGroupMoveButton` styled locally (:140).
  - `PageHeader` actions not wrapping (:160).
  - Other product rows: `SelectPicker` dropping `class` (ListingShelf, :99) and `SliderInput` lacking `step` and emitting strings (PbnStudio, :100).

### Inferences
- **The highest-value override fixes are structural**: a bottom-bar slot or prop on AppShell (removes 11 grid-area
  hacks) and glass strength as a theme token (Wheelhouse names it as the exit condition).
- **Typing gaps act like overrides.** One fix — declaring `aria-label` (or native attrs) on the SDK props types —
  removes 26 `v-bind` object workarounds.
- **TNIS is the outlier.** Its studio chrome is a full re-skin; whether a "dense/console" density or size on
  Accordion and Button would absorb it is untested.

### Gaps
- Inline `class=` overrides on SDK components that change layout without `!` (e.g. `class="gap-1.5 ps-1 pe-2"` on SDK `Button`) were not counted; the count needs a per-component class-prop audit.
- I did not check whether the SDK `index.css` reduced-motion rule makes the 3 local kill switches redundant.

## What boilerplate does every product write the same way (layout setup, guards, titles, loading/error/empty, forms, toasts)?

### Takeaway
The repeated boilerplate is setup and feedback glue. Most products write the same Vite theme plugin, Tailwind
`@source` line, version-label regex, scroll-to-top watch, page heading row and "toast on mutation result" branch. Two
of these (scroll reset, document title) are already done by `createAppRouter`, so products are now duplicating SDK
behaviour. Loading/error/empty is the success case: 15 apps use `DataRegion`, and only 7 still hand-roll `v-if`
loading triplets.

### Cited Findings
- **D8 — pre-paint colour mode:**
  - 28 apps' `vite.config.ts` import `colorModeScript`; 23 of them define a local `themeScript()` Vite plugin of 15–26 lines that serves `/theme.js` in dev and emits it at build. Haven's 5 apps import it without a local `themeScript` function; their shape was not read.
  - Example: `import { colorModeScript } …` (:4), `function themeScript(): Plugin` (:17), `server.middlewares.use('/theme.js', …)` (:22, :28), `this.emitFile({ … fileName: 'theme.js' })` (:34) — [vendor-renewals:web/../vite.config.ts](maxs-projects/ventures/saas/ventures.vendor-renewals/engineering/codebase/vendor-renewals.frontend-services/apps/web/vite.config.ts).
  - 22 apps hold a `bootstrap/ColorMode.ts` or `Theme.ts` that only exports the storage key, e.g. `export const ColorModeStorageKey = 'vendor-renewals.color-mode';` — `vendor-renewals:web/bootstrap/ColorMode.ts:2`.
  - `index.html` loads `<script vite-ignore src="/theme.js">` — `vendor-renewals:web/../index.html:16`.
  - 11 apps also wire a `boot-splash` static twin (grep `boot-splash` in `index.html`/`vite.config.ts`).
  - The convention mandates `public/theme.js` and the boot-splash twin — [conventions/development/frontend/shapes/app/platform/document.md:39-50](../conventions/development/frontend/shapes/app/platform/document.md).
- **Tailwind setup:** 35/35 apps' `bootstrap/index.css` contain an `@source` line. Sampled: `@source '../../node_modules/@wow-two-beta/fe/dist';` with an explanatory comment — `vendor-renewals:web/bootstrap/index.css:1-6`. The same comment recurs in museums, pose-coach, prism, transcript-forge, customer-promises, file-watch, procedure-review, TNIS and Wheelhouse (SDK-mention comment sweep).
- **D5 — version label:** `/^\d/.test(appVersion) ? \`v${appVersion}\` : appVersion` appears in 24 apps (23 products), e.g. `vendor-renewals:web/bootstrap/AppLayout.vue:35` and `wheelhouse:web/bootstrap/AppLayout.vue:63`. TNIS keeps it in `application/common/AppVersion.ts:5` and `application/showcase/AppVersion.ts:5`. 30 apps reference `__APP_VERSION__`. The convention requires "must show the app version beside the logo" — [shell.md:27-28](../conventions/development/frontend/shapes/app/shell/shell.md).
- **D2 — scroll-to-top watch:**
  - `watch(() => route.path, () => main.value?.el?.scrollTo({ top: 0 }))` appears in 16 apps' `AppLayout.vue`: matinee :45, museums :95, pose-coach :31, forever-pin :55, transcript-forge :65, sift :57, customer-promises :45, epub-review :30, file-watch :59, listing-shelf :75, pbn-studio :21, procedure-review :61, surface-pattern :25, training-seats :30, vendor-renewals :45, Wheelhouse :113.
  - Every one of those apps calls `createAppRouter`, whose scroll restoration resets the AppShell region since `8f50655b` (2026-10-15) — [ScrollRestoration.ts:36-40](SDK/router/adapters/vueRouter/ScrollRestoration.ts).
  - The convention still phrases it as a product duty: "must return the main region to its top when the place changes" — [shell.md:18](../conventions/development/frontend/shapes/app/shell/shell.md).
- **D4 — destinations declared once, rendered twice:**
  - `const Destinations = [{ label, path, icon }]` in 10 apps, e.g. `vendor-renewals:web/bootstrap/AppLayout.vue:5-8`.
  - The list renders as `NavItem` + `RouterLink` in the bar (:80-84) and again as `BottomNavMenuItem` (:100-110).
  - Each active check is hand-written as `route.path === place.path`, found in 9 apps. Haven's equivalent is `PlaceExtensions.isCurrent` — `HavenShell.vue:54`.
- **D9 — page heading:**
  - 33 apps / 105 `*Page.vue` files render their own `<h1>` or `level="1"` heading; SDK `PageHeader` is imported in 19 files across 7 apps (transcript-forge 7, procedure-review 4, file-watch 3, sift 2, config-checker 1, podcast-readiness 1, Wheelhouse 1) and `RoutePageHeader` in 1 file (`pbn-studio:web/presentation/studio/pages/StudioPage.vue`).
  - 15 page files in 12 apps hand-build the full header row (`<header class="flex flex-wrap … justify-between">`); this includes all 5 template/domain sample apps. Example: [vendor-renewals:web/presentation/renewals/pages/AgendaPage.vue:89-101](maxs-projects/ventures/saas/ventures.vendor-renewals/engineering/codebase/vendor-renewals.frontend-services/apps/web/src/presentation/renewals/pages/AgendaPage.vue) — `Heading :level="1"` + muted `Text` + a flex-wrap actions div.
  - The convention wants the label from route metadata so heading, nav entry and document title agree — [shell.md:47-53](../conventions/development/frontend/shapes/app/shell/shell.md).
- **D10 — document titles by hand in 7 apps (4 products):** hijinx `bootstrap/AppLayout.vue:31`, museums `presentation/common/DocumentTitle.ts:8`, listing-shelf `presentation/common/hooks/UseDocumentTitle.ts:11`, and Haven `admin/channels/map/web` `bootstrap/Router.ts` (:21/:24/:14/:59).
  - Haven uses plain `createRouter` + `router.afterEach(… document.title = …)` in all 4 routed apps, not `createAppRouter` — [haven:admin/bootstrap/Router.ts:1-22](maxs-projects/ventures/saas/10x-ven-haven/engineering/codebase/haven.frontend-services/apps/admin/src/bootstrap/Router.ts).
  - SDK backlog: "Ability to set page titles and map routes to typed props | ListingShelf" — [SDK-plan/backlog.md:106](SDK-plan/backlog.md).
- **D11 — mutation feedback:**
  - `notify({ tone: NoticeTone.… })` appears in 64 files across 22 apps. Tone sites: 40 Danger, 33 Success, 7 Warning, 2 Info (grep of the line after each `notify({`).
  - The usual shape is `if (!result.ok) notify({ tone: Danger, title: 'Not saved', description: FailureMessages… })`, e.g. `transcript-forge:web/presentation/settings/TranscriptionDefaultsCard.vue:52` and `…/library/LibraryPage.vue:118-120`.
  - A local `FailureMessages` mapper exists in 10 apps: forever-pin, transcript-forge (`FailureMessageMappers.ts`), sift, config-checker, customer-promises, file-watch, listing-shelf, podcast-readiness, procedure-review, vendor-renewals. It turns `AppError.problem` into a sentence (first field error with its label, else detail/title, else fallback) — [vendor-renewals:web/application/common/FailureMessages.ts:6-28](maxs-projects/ventures/saas/ventures.vendor-renewals/engineering/codebase/vendor-renewals.frontend-services/apps/web/src/application/common/FailureMessages.ts).
  - SDK backlog: "Ability to render backend `AppError` codes and field errors" (open) — [SDK-plan/backlog.md:111](SDK-plan/backlog.md).
  - A grep of `SDK/query/adapters/tanstack/hooks/UseAppMutation.ts` found no notice/notify option (only an internal `onSuccess` at :67).
- **Loading/error/empty:** `<DataRegion` appears in 77 files across 15 apps. Hand `v-if="…isLoading|isPending|isFirstLoad"` appears in 24 files across 7 apps, and `v-else-if="…error|failure"` in 10 files across 5 apps (grep).
  - Wheelhouse-reported DataRegion gaps: "Ability to give infinite queries first-load and refreshing states for `DataRegion`" (:147); "Deprecate `useAppQuery`'s `loading` beside `isFirstLoad`" (:128) — [SDK-plan/backlog.md](SDK-plan/backlog.md).
- **Guards:** `requireAuth` is imported by 2 apps (epub-review and training-seats `bootstrap/router/Routes.ts`). The other signed-in ventures gate in the layout through `useSessionGate` instead (D7).
- **Form wiring:** `application/common/AppForms.ts` — "Pins the product's single form engine: the SDK house adapter" — appears in forever-pin and listing-shelf, and Wheelhouse has `bootstrap/form.ts` (SDK-mention comment sweep).
  - listing-shelf overrides the forms engine's fallback text: "The form keeps the SDK's safe fallback text; the archive's own explanation reads better" — `presentation/listings/components/SaveViewModal.vue:35` and `…/pipelines/components/PipelineSettingsModal.vue:61`.
  - Form wiring was not audited further.

### Inferences
- **About 100 lines of identical glue per product** could move into the SDK or the template: the theme plugin
  (~20 lines × 23), version label, scroll watch, destinations ×2 and FailureMessages. Two items in that set are
  already redundant with `createAppRouter` (scroll reset, document title). The cheapest win is deleting code from
  products and the convention, not adding to the SDK.
- **"Toast after mutation"** is the most frequent feedback boilerplate (64 files). A mutation option that publishes
  the success/failure notice through the bus, plus an SDK `describe(AppError)`, would absorb both the branch and the
  10 mappers. This is inference; the design was not explored.
- **`PageHeader` is under-adopted (7/33 apps).** Known blockers are visible: actions don't wrap (backlog :160) and
  there is no eyebrow slot or focus target (listing-shelf). The template seeds a hand header.

### Gaps
- Not checked at runtime: whether the 16 manual scroll watches double-fire against SDK restoration, or break
  back/forward restoration of the main region. A hand reset on every `route.path` change would probably defeat
  restoring a saved offset on back navigation — **unverified**.
- Tone counts come from line-adjacent grep; multi-line `notify` calls may be missed.

## How does each product structure its shell (sidebar / top / bottom nav, page header, breadcrumbs, palette, search, shortcuts, recents), and is it SDK or hand-built?

### Takeaway
One shape dominates: a top `Navbar` with brand + version + links, the account menu at the end, and `BottomNavMenu`
on phones. 22 apps use it, all hand-assembled from SDK parts. Only Wheelhouse and listing-shelf use a sidebar. Only
Wheelhouse has breadcrumbs (a local `ScopeBar`), only museums-gallery has a command palette, and keyboard shortcuts
are per-page `useHotkeys`. No product has an app-level "recents".

### Cited Findings
- **Top bar + bottom bar (22 apps):**
  - All use AppShell, Navbar and NavItem; all but Wheelhouse use `Navbar` inside `AppShellHeader`.
  - Bottom nav via SDK `BottomNavMenu` appears in 11 apps — matinee, museums, forever-pin, sift, customer-promises, file-watch, listing-shelf, procedure-review, vendor-renewals, transcript-forge (`AppTabBar.vue`) and Wheelhouse (`PhoneNav.vue`) — plus Haven's shell.
  - Source: the import parser over `bootstrap/AppLayout.vue`.
  - Representative: [vendor-renewals:web/bootstrap/AppLayout.vue:66-111](maxs-projects/ventures/saas/ventures.vendor-renewals/engineering/codebase/vendor-renewals.frontend-services/apps/web/src/bootstrap/AppLayout.vue).
- **Sidebar shells (2 apps): Wheelhouse is the reference, and is hand-built over SDK parts** — [wheelhouse:web/bootstrap/AppLayout.vue](wow-two-platform/wow-two-platform.wheelhouse/engineering/codebase/wheelhouse.frontend-services/apps/web/src/bootstrap/AppLayout.vue):
  - A sidebar collapses to an icon rail (`SidebarWidth = { Full: '248px', Rail: '64px' }` :10). The rail state is persisted with `useSidebarCollapsed`, computed per breakpoint (:56-70), and toggled by a local button (:157-168).
  - A brand cell is sized to the sidebar width (:137-141).
  - Tablets get a lazy `NavDrawer` (SDK `Drawer`, :41, :201); phones get `PhoneNav` (SDK `BottomNavMenu` with `wh-glass`, :198).
  - The sidebar body is a local `ConsoleNav` (SDK `SidebarMenu`) inside `AppShellSidebar` (:187-189).
  - Local nav parts without SDK imports: `PinnedNav.vue` (82) and `ProductsNavItem.vue` (129), plus a crumbs computation from route params/query (:72-97).
  - SDK backlog rows from this shell — [SDK-plan/backlog.md:136-141](SDK-plan/backlog.md):
    - "Ability to give `SidebarMenuSection` a header action | Wheelhouse's Pinned 'Edit' button is absolutely positioned" (:138).
    - "Fix `AppShellSidebar` nesting a `<nav>` around `SidebarMenu`'s own landmark" (:139).
    - "Ability to split `SidebarMenuGroup` into a link and a separate toggle" (:141).
  - listing-shelf is the other sidebar app: `AppShellSidebar` + `SidebarMenu`/`SidebarMenuSection`/`SidebarMenuItem` + a local `SavedViewsNav.vue`, plus a `BottomNavMenu` on phones — import parser on `listing-shelf:web/bootstrap/AppLayout.vue`.
- **Breadcrumbs / page actions in the top bar (1 app):** `wheelhouse:web/presentation/shell/components/ScopeBar.vue` (68) uses SDK `Breadcrumb` + `PageHeader`. Backlog — [SDK-plan/backlog.md:136-137](SDK-plan/backlog.md):
  - "Ability to route `Breadcrumb` links and keep one line on phones | Wheelhouse v0.5 `ScopeBar` routes clicks and truncates to the last two crumbs locally".
  - "Ability to place `PageHeaderActions` in the app top bar | Wheelhouse v0.5 mounts a hidden `PageHeader` in the top bar to host page actions (`.wh-page-actions`)".
  - `useBreadcrumbs` from `/router` has 0 importers.
- **Command palette (1 app):** museums-gallery mounts `CommandPaletteModal` with all its parts in the 237-line `AppLayout.vue` (`<CommandPaletteModal v-model:open="isPaletteOpen" trigger-key="k">` :181). SDK backlog: "Adopt the commands registry in both command palettes | each palette keeps its own item registry today" — [SDK-plan/backlog.md:166](SDK-plan/backlog.md).
- **Search and shortcuts:**
  - listing-shelf binds `useHotkeys('/', …)` for search in `bootstrap/AppLayout.vue:66`.
  - transcript-forge ships a local `KeyboardShortcutsModal.vue` (SDK `Modal` + `KeyboardShortcutText`, opened by `useHotkeys('shift+?')` :29) plus a `RowKeyExtensions.ts` over `useHotkeyMap`.
  - prism uses `useHotkeyMap` in `application/studio/UseStudio.ts:726,762`.
  - TNIS studio's `MapSearch.vue` (142) is built on SDK `ComboboxPicker`.
  - Raw `window.addEventListener('keydown')` appears in 5 apps, mostly game/canvas: arcade ×3, museums `GuessGameView.vue:84`, prism `SceneView.vue:369`, TNIS ×6, Wheelhouse `DayProductRows.vue:172`.
- **App switcher:** only Haven (`AppSwitcherMenu` in `HavenShell.vue:87`, across its admin, channels, map and web apps).
- **Recents:** a grep for `recent(s)`/`recently viewed|opened`/`useRecent` found only domain data (e.g. sift feeds, Haven pipeline runs) and no shell-level recents.
- **Document-scrolling and non-SDK shells:**
  - Haven's shell uses `AppShell scroll="document"` (`HavenShell.vue:82`); hijinx comments "The page scrolls as a document" (`bootstrap/AppLayout.vue:12`).
  - Arcade's `ArcadeShell.vue` uses no SDK shell; it frames the launcher and defers back navigation to Telegram ("the back control is Telegram's own inside Telegram").
- **The convention spells out every frame duty as a product "must"** — [shell.md:9-53](../conventions/development/frontend/shapes/app/shell/shell.md):
  - frame in `bootstrap/AppLayout`, logo and version, primary nav in bar or rail, `aria-current`, account menu last;
  - account menu with versions, colour mode and sign-out; page heading from route meta;
  - signed-out screens outside the frame.

### Inferences
- **The shell vocabulary is settled** (top bar + phone bottom bar, optional rail). Every product re-derives it from
  `shell.md` by hand. An SDK "frame preset" that takes destinations, brand, version, account props and a sidebar
  mode would cover 22 apps directly and Wheelhouse/listing-shelf partly. Haven's `HavenShell` and Wheelhouse's
  rail/drawer/phone triad are the two concrete precedents. Note the SDK backlog lists "Shell presets (Vue) | shipped
  v0.1" ([SDK-plan/backlog.md:26](SDK-plan/backlog.md)), yet no `*Preset*` shell was seen in `src/presentation/layout`
  and no product imports one. What that row refers to is unverified.
- **Command palette, breadcrumbs, recents and an app switcher barely appear in products.** They are not desire paths
  yet. They are SDK capability ahead of demand, except for Wheelhouse's breadcrumb/actions-in-bar needs, which are
  already in the backlog.

### Gaps
- "Shell presets (Vue)" in the SDK backlog was not traced to code.
- Mobile behaviour (drawer vs bottom bar thresholds) was read only for Wheelhouse and vendor-renewals.
- `docs/ui-beta-roadmap.md`, `docs/ux-observability-system.md` and `conventions/design/` (beyond the one `theme-patterns.md` line) were not read in this lane.

## What do TODO / workaround / "SDK doesn't" comments in product frontends say?

### Takeaway
Products carry almost no `TODO`/`hack` comments (a whole-app grep hit only Spanish/Portuguese "todos" strings). The
workaround record lives in prose doc-comments that name the SDK, and in the SDK's own "Product-reported gaps"
backlog table, which already lists many of them.

### Cited Findings
- A grep for `TODO|FIXME|workaround|hack|SDK doesn't|until the SDK…` across all 35 apps found one real workaround comment: "SliderInput emits a string and has no `step`; the cast stays until the SDK emits numbers." — `pbn-studio:web/presentation/studio/components/SettingsPanel.vue:81`. The other hits were i18n strings ("todos") and an icon name (`ListTodo`).
- **SDK-naming comments (141 lines across the apps) record these workarounds:**
  - prism ×17: "…its props type does not list it yet (backlog: SDK adoption)" — e.g. `prism:web/presentation/studio/LayersPanel.vue:54`.
  - Wheelhouse: "Until glass strength is a theme token, these material roles stay here" — `wheelhouse:web/bootstrap/index.css:37-39`.
  - Arcade: "the SDK's copy fallback would copy the link alone" — `arcade:web/integration/platform/BrowserPlatform.ts:37`.
  - TNIS: "Hides the SDK's own trigger chevron" — `tnis:studio/presentation/network/theme.css:963`.
  - Wheelhouse: "the SDK move button carries behaviour only" — `wheelhouse:web/presentation/pins/PinEditor.vue:33`, `presentation/products/components/WorkspacesModal.vue:71`.
  - file-watch and procedure-review: "a product palette waits on where palettes live (an open decision)" — `bootstrap/index.css:8`.
  - Wheelhouse: "The SDK trend row is one inline-flex line … so a narrow…" — `presentation/deployments/components/history/RangeStatsTiles.vue:106`.
- **SDK backlog "Product-reported gaps" — [SDK-plan/backlog.md:93-109](SDK-plan/backlog.md):**
  - `useDrag`/`usePinch` capturing on press (ListingShelf).
  - `@vue-ignore` props breaking `strictTemplates` (ListingShelf, Haven).
  - `SelectPicker` dropping `class` (ListingShelf); `SliderInput` lacking `step` (PbnStudio).
  - Split the package build per module (ForeverPin, Haven: "shared chunks (385 kB) outweigh product code").
  - Follow the system colour scheme (ListingShelf, Hijinx); set page titles and map routes to typed props (ListingShelf).
  - Wheelhouse-specific rows follow at :126-160.

### Inferences
- **The SDK team already harvests desire paths, but only from products that reported them** (Wheelhouse dominates
  rows :126-160). The 22-product frame duplication, the theme Vite plugin and the mutation-notice glue have no
  backlog row; they are invisible because each product treats them as "its own composition".
  - Wheelhouse's `CLAUDE.md` frames this boundary: "Shared capability gaps belong in the SDK. Product composition
    stays local." — `wow-two-platform/wow-two-platform.wheelhouse/CLAUDE.md` § Beta SDK usage.

### Gaps
- Comment harvest relied on the words "sdk"/"fe sdk"/"kit"/"@wow-two-beta"; workarounds described without naming the
  SDK would be missed.
- The `kit` hits are mostly domain words (Wheelhouse host kit, PbnStudio paint kit), not SDK references.
