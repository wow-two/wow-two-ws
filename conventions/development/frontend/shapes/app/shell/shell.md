# Shell

*Last updated: 2026-10-01*

> The frame every routed place renders inside — the bar, the navigation, the account menu and the page heading.
> Purpose — a product's places share one frame, so chrome is decided once and no page rebuilds it.
> Use case — standing up `AppLayout`, adding a destination, or placing an action that belongs to a whole page.

## Frame

- must build one frame, `AppLayout`, in `bootstrap/`, and mount it through a layout route
  ([routing](../routing/routing.md#places)).
- must compose it from the SDK `AppShell` and `Navbar`; never hand-roll the grid or the scroll container
  ([AppShell](../../../core/mla/components/layout/appShell.md) ·
  [Navbar](../../../core/mla/components/layout/navbar.md)).
- must open the frame with a skip link to the single `<main>`
  ([landmarks](../../../core/lla/constructs/html/landmarks.md)).
- must return the main region to its top when the place changes.
- must render signed-out screens outside the frame — sign-in, an expired session, a first-load splash.

---

## Bar

- must place the product logo at the start of the bar, linking to the home place
  ([logo system](../../../../../design/identity/logo-system.md#composition)).
- must show the app version beside the logo
  ([versioning](../../../../repo/versioning/versioning.md#reporting)).
- must put primary navigation in the bar of a top-bar app, or in the rail of a sidebar app — one of them per app.
- must mark the current destination `aria-current="page"`.
- must keep primary navigation one tap away at every declared screen class
  ([responsive](../responsive/responsive.md#layout-rules)).
- must end the bar with the account menu.

---

## Account menu

- must name who is signed in.
- must show each service's version ([versioning](../../../../repo/versioning/versioning.md#reporting)).
- must offer the colour mode — light, dark, system ([styling](../platform/styling.md#colour-mode)).
- must hold the account-level destinations that stay out of primary navigation.
- must end with sign out.

---

## Page heading

- must render one `<h1>` per place, carrying the label its navigation entry carries.
- may add one line of description under it ([UI copy](../../../../../design/content/ui-copy.md)).
- must place page-level actions beside the heading, at its trailing edge.
- must take the label from route metadata, so the heading, the navigation entry and the document title agree
  ([routing](../routing/routing.md#navigation)).

---

## Neighbours

- [app](../app.md) — the shape this vector belongs to
- [document](../platform/document.md) — what shows before the frame mounts
- [routing](../routing/routing.md) — the places the frame wraps
- [layout](../../../core/mla/constructs/visual/layout.md) — the kind `AppShell` and `Navbar` belong to
