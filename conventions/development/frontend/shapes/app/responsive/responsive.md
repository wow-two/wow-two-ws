# Responsive

*Last updated: 2026-10-16*

> Which screens an app supports, and how its layouts and interactions adapt between them — phones included.
> Purpose — responsive work is spent only where a product is really used, and done the same way everywhere.
> Use case — scoping a product's frontend, or adding a page, table, dialog or destination to an app on phones.

## Device targets

- must declare the app's device targets in its design spec (`## Screens`): the classes it serves, and its primary.
- must build responsive layouts only across the declared targets; one declared class means one layout.
- must keep an undeclared class out of scope — no layouts, fixes or verification for it.
- must declare every class a user really reaches: a phone target is declared when people open the app on phones.

---

## Screen classes

| Class | Width | Tailwind / SDK `Breakpoint` | Verify at |
|---|---|---|---|
| phone | < 768px | base styles | 390 × 844 |
| tablet | 768–1023px | `md` | 820 × 1180 |
| desktop | ≥ 1024px | `lg` (`2xl` ≥ 1536 widens it) | 1440 × 900 |

- must treat wide screens (`2xl`) as a desktop enhancement — a width cap or extra columns, never a separate design.
- must use the SDK `Breakpoint` steps and Tailwind's screen variants; no custom pixel breakpoints.
- must read breakpoints in script only through the SDK `useBreakpoint` / `useMediaQuery`, never `window.innerWidth`.

---

## Layout rules

- must write mobile-first when phone is declared: base styles serve the phone, `md:` and `lg:` add to them.
- must keep one place per route at every class ([shapes](../../shapes.md)); a class changes the layout, not the route.
- must avoid horizontal page scroll; a wide element scrolls inside its own container.
- must give every hover affordance a touch equivalent on phone and tablet.
- must keep touch targets at least 44 × 44px on phone and tablet.
- must take every phone pattern below from `@wow-two-beta/ui-vue` 0.0.14 or later; each section links its spec.

---

## Navigation

- must keep primary navigation one tap away at every declared class.
- must put primary navigation in a bottom bar on phones — `BottomNavMenu`, one `BottomNavMenuItem` per destination.
- must hold at most 5 destinations in the bottom bar.
- must settle the information architecture — which places are destinations — before building the bar.
- must pad the main region by the bar's height, so the pinned bar never covers content.
- from `md` up → the shell's bar or rail ([shell](../shell/shell.md#bar)).
- implementation → [BottomNavMenu spec](../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/nav/bottomNavMenu/BottomNavMenu.spec.md).

---

## Tables

- must render every table below `md` as one labelled card per row — `Table` / `DataTable` `phoneLayout: 'stack'`,
  the default.
- must leave `stackBreakpoint` at `md`.
- must give every column header text, or its cells a `label`, so each card line names its value.
- may opt one table into sideways scrolling with `phoneLayout: 'scroll'`; the exception is per table, never app-wide.
- implementation → [Table spec](../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/display/table/Table.spec.md)
  · [DataTable spec](../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/display/dataTable/DataTable.spec.md).

---

## Dialogs

- must open a form dialog full screen below `sm` — `ModalContent` `phoneLayout: 'fullscreen'`, the default.
- must put its fields in `ModalBody` and its actions in `ModalFooter`, so the body scrolls and the footer stays pinned.
- must keep a visible way out of a full-screen dialog — `ModalClose`, or a cancel action in the footer.
- must take the phone layout and its safe-area padding from `ModalContent`; never size the panel by hand.
- must open a short confirmation as a bottom sheet below `sm` — `AlertModalContent`, whose `phoneLayout` is `sheet`.
- must set `phoneLayout: 'sheet'` on a `ModalContent` that only confirms — a question, no fields, two actions at most.
- must show every dialog from `sm` up as the centred card, sized by `size`.
- implementation → [ModalContent spec](../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/overlays/modal/ModalContent.spec.md)
  · [AlertModalContent spec](../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/overlays/alertModal/AlertModalContent.spec.md).

---

## List and detail

- must lay out a list-and-detail page with `ListDetailLayout`: side by side from `lg`, one pane at a time below it.
- must leave `breakpoint` at `lg`.
- must derive `isDetailOpen` from the selected item in the route's search params
  ([routing](../routing/routing.md#ownership)), so browser back and the back control both return to the list.
- must answer `back` through the router — the same move as browser back — never by toggling local state.
- must keep the list pane mounted while the detail shows, so its scroll and search survive.
- must mark the chosen item `aria-current` or `aria-selected`, so focus returns to it on back.
- must open the detail pane with a heading — it takes focus when the detail opens.
- implementation → [ListDetailLayout spec](../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/layout/listDetailLayout/ListDetailLayout.spec.md).

---

## Motion

- must animate a state change the reader caused or waits on — a panel opening, a pane arriving, a row added.
- must animate progress — a deployment step turning done, a bar filling — never jump between states.
- motion tokens, reduced motion → [transitions](../../../core/lla/constructs/tailwind/transitions.md#the-utilities).
- region loading and its skeletons → [loading](../../../core/mla/domains/data/state-and-data.md#loading).

---

## Verification

- must check every declared class at its verify size before a version closes.
- must test representative flows per class with the app's browser suite ([delivery](../delivery/delivery.md)).
- must check at the phone size that tables stack, dialogs take their phone layout, list and detail swap with focus
  restored, and the bottom bar covers no content.

---

## Open

- proposals for discussion → [responsive proposals](responsive-proposals.md); owner review in Wheelhouse v0.5.
