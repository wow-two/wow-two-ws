# Library

*Last updated: 2026-08-19*

> A package another frontend installs and imports — `@wow-two-beta/ui`, `@wow-two-beta/ui-vue`, a repo-local
> `@{brand}/*`. Take [core](../../core/core.md) whole; infer nothing from the silence here.
> Purpose — a package has no layers, no places and no composition root, so an app's tree rules say nothing here.
> Use case — laying out a package's source, or naming a module a consumer imports.

## Layout

The **package groups by kind**; a product slices by domain ([app](../app/app.md) § *Vectors*). The kinds
themselves, and which suffix routes to which, are [visual kinds](../../core/mla/constructs/visual/visual.md).

- must give every component its own folder — `camelCase` folder, `PascalCase` main file, an `index.ts` barrel,
  a co-located `*.stories.tsx` and a `*.variants.ts` where one is needed.
- must not flatten a component file beside sibling folders.
- must read every kind's group folder (`presentation/actions/` · `presentation/forms/`) as **package layout** —
  the package groups by kind because it ships no domains.
- must place a **capability module** — `auth/` · `query/` · `flags/` · `router/` · `foundation/` — at the
  package root, beside `presentation/`, never inside it. A capability ships seams and providers, not kinds.
- must name that module with a **capability noun** — what the module *is*, so its folder names the thing a
  consumer imports.
- must not name one for the activity it performs — a verb noun says what the code does, and every later
  capability sharing that verb then has the same claim on the folder.
- must keep a `foundation/` primitive importing nothing from `presentation/` or a capability module; the
  boundary is linted, and it runs one way.
- must keep the *presentation* components router-free — a router ships as its own subpath
  ([routing](../app/routing/routing.md) § *Home*).

```txt
✅ clipboard/ · http/ · storage/ · auth/ · query/ · flags/ · router/ · foundation/
❌ validation/ · format/ · sync/      (an activity — the capability being validated or formatted is unnamed)
```

---

## Open

- **delivery** — unwritten. The `exports` subpath map, `sideEffects`, the peer-dependency set, the published
  `dist` and the version bump have no doc yet; today they are read off the shipped packages.
- **architecture** — unwritten beyond the layout above.
- **testing** — unwritten.

---

## Formatting

- must set Prettier `printWidth: 120` in the package, so the width trigger is automatic and the
  3-attribute floor stays a review gate ([JSX attributes](../../core/mla/constructs/constructs.md)).

---

## Neighbours

- [shapes](../shapes.md) — the test that put these rules here rather than in `core/`
- [app](../app/app.md) — the other shape, and the trigger that extracts a surface into a library
- [boundaries](../app/architecture/boundaries.md) — when an app's surface becomes a package's
