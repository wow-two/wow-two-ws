# Core

*Last updated: 2026-08-23*

> What holds in every frontend deliverable we build — the language forms, the roles we declare, the things
> complete on their own, and the capabilities a codebase reaches for.
> Purpose — a rule that does not change when the deliverable changes belongs here, once.
> Use case — naming a component, writing a doc block, picking a kind, or reaching for a capability.

## The three scopes

| Scope | Answers | Lead |
|---|---|---|
| [lla](lla/lla.md) | one symbol | the TypeScript, HTML, CSS and Tailwind form, and how it is written end to end |
| [mla](mla/mla.md) | one app | the roles we declare, the things complete alone, the capabilities |
| [hla](hla/hla.md) | between our own frontends | empty by design until a second frontend exists |

- must place a rule here when it holds whatever is being built — a product app or a component library.
- must place it under [shapes](../shapes/shapes.md) when it changes with the deliverable.
- must not let a shape's vocabulary leak in — `core/` never names a layer, a route, a bundler or a package
  manifest.

---

## Routing a rule

**Routing.** A kind you declare → `mla/constructs/{kind}.md`. Which one to reach for, and with what values →
`mla/components/`. A language form used end to end → `lla/components/{form}.md`. How any symbol is written →
`lla/notation/`. A concrete technology or capability → `mla/domains/{domain}/`. A framework's own constructs →
`lla/constructs/{framework}/`. A rule spanning frontends we both own → `hla/`.
Where a folder is **created in the source tree**, how an app builds, routes and serves, how a package is
published → [shapes](../shapes/shapes.md), never `core/`.

**The test between `mla/` and `hla/`:** do we own both ends? A third-party widget is adapted in `mla/`, never
contracted in `hla/`.
**The three levels, and where each lands.** A form the platform ships is [lla constructs](lla/constructs/constructs.md).
Everything we declare lands in `mla/`: a **kind** that needs something else present → `mla/constructs/`
(`Page`, `Overlay`, `Model`); a **thing complete alone** → `lla/components/` when the language supplies the form
(`Constants`, `Enums`, `Extensions`), `mla/components/` when we coined it. A ban follows its rule — construct bans
in `lla/`, kind bans with the kind.

**The test between baseline and a domain:** would the rule survive if the feature were deleted? Yes → baseline.
No → the domain that owns it.

---

## What each scope owns

### `lla/` — one symbol
Every rule that holds for **any** symbol, whatever kind it is: its name, its doc blocks, its file layout, its
imports, and the platform constructs banned outright. A rule naming a *kind* we coined is not `lla/`; a rule
naming a capability is not `lla/`. Full boundary and buckets → [lla](lla/lla.md).

### `mla/` — one app
Three buckets. `constructs/` = the kinds we declare, one file per suffix. `components/` = which one to reach
for, and with what values. `domains/` = a capability, its contract and its providers.
Full boundary → [mla](mla/mla.md).

- **A third party is a member of the domain that consumes it**, never its own axis. If the app cannot render
  without it, it is a provider, whoever wrote it.
- **The SDK boundary.** *How to use* and *what to use* from `@wow-two-beta/ui` is a convention and lives here;
  the SDK's own internals live in the SDK's docs. The scope follows the component, not the package.

### `hla/` — between our own frontends
Named ahead of its contents on purpose: without it, the first module-federation or shared-runtime rule lands in
`shapes/app/`, and becomes a single-app default every later app inherits by accident.

---

## Neighbours

- [shapes](../shapes/shapes.md) — what changes with the deliverable: an app, a library
- [frontend conventions](../frontend-conventions.md) — the index over both cuts
