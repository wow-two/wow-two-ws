# Routing

*Last updated: 2026-09-10*

> Framework-neutral places, route ownership and navigation behavior.

## Ownership

- must declare places in an app-owned route model and construct the router at `bootstrap/`.
- must use the SDK router adapter for shared behavior; generic wrappers follow [extraction](../architecture/boundaries.md#sdk-extraction).
- must keep router imports out of SDK presentation components under [library layout](../../library/library.md#layout).
- must keep framework/router syntax in its provider leaf: [Vue](vue/vue.md).
- must assign route-to-page parameter decoding to an app bootstrap adapter; pages receive typed values/callbacks.
- must validate path/search parameters before a page treats them as domain data.
- must keep sharable navigation state in paths/search; reserve fragments for document targets.

---

## Places

- must give a navigable place a URL and a page that works on direct hit, refresh and a new tab.
- must code-split place components and provide a loading/error outcome for failed chunk loads.
- must compose shared chrome through layout routes.
- must give an action a routeless overlay unless it represents a persistent place.
- may intercept a place as an overlay during in-app navigation when direct navigation still produces its page.
- must keep responsive presentation in the component; viewport size does not change the place's identity.
- must declare not-found, forbidden, unresolved-session and route-error behavior.
- must await an unsettled session in guards and follow [auth](../../../core/mla/domains/auth/auth.md).

---

## Navigation

- must set the document title from the deepest matched route metadata with an app fallback.
- must apply deliberate focus and scroll behavior after navigation; restore history scroll without stealing ongoing interaction.
- must focus the new page heading or main region on user navigation when the current focus no longer describes the page.
- must announce route changes through one accessible mechanism, avoiding duplicate title/live-region announcements.
- must preserve modified-click, new-tab and native link semantics.
- must validate redirects through [security](../../../core/mla/domains/security/security.md#session).
- must let a dirty form block navigation through the router's declared blocker seam.

---

## Bootstrap names

- must place `AppRoot`, `AppLayout` and `AppErrorBoundary` in `bootstrap/` when those roles exist.
- must keep route declarations and parameter adapters in `bootstrap/router/` when the group needs multiple files.
- must use the owning visual kind's suffix for pages and overlays; a not-found place is a page.
