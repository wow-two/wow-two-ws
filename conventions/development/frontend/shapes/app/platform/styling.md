# Styling

*Last updated: 2026-08-19*

> How an app wires Tailwind v4 — the `index.css` entry, the plugin, the token import, and the theme switch.
> Purpose — a wrong `@source` depth silently drops the library's utility classes and raises no build error.
> Use case — standing up a new app's stylesheet, or an app that renders half-styled with a green build.

Which utilities may be written, how classes compose, and what a token is are `core/` questions
([tailwind](../../../core/lla/constructs/tailwind/tailwind.md)). This doc only wires them into an app.

## The entry (`index.css`)

An app's `src/bootstrap/index.css` imports Tailwind, imports the library's design tokens, and `@source`s the library's
compiled output so the utility classes its components emit are generated — Tailwind v4 ignores `node_modules`.

```css
@import 'tailwindcss';

/* Design tokens (@theme) shipped by the library — gives bg-primary, text-foreground,
   bg-card, border-border, etc. */
@import '@wow-two-beta/ui-vue/styles.css';

/* Tailwind v4 ignores node_modules; point it at the beta UI's dist so its utility
   classes are generated. Path is relative to THIS file. */
@source '../../node_modules/@wow-two-beta/ui-vue/dist';
```

- must load the Tailwind Vite plugin `@tailwindcss/vite` — `plugins: [vue(), tailwindcss()]`.
- must not add a `tailwind.config.js` content array; `@source` declarations live in CSS.
- must count `@source`'s depth from `index.css`, which lives in `bootstrap/`
  ([architecture](../architecture/architecture.md) § *Layers*) — `../../node_modules/…`, two up,
  `bootstrap/` → `src/` → repo root. A wrong depth **silently drops** the library's utility classes: the app
  renders half-styled with no build error.
- must keep every authoring block in that stylesheet
  ([authoring](../../../core/lla/constructs/tailwind/authoring.md)).

---

## Brand tokens

- must consume the semantic token classes the library ships via `@theme`, never a raw palette value
  ([color](../../../core/lla/constructs/tailwind/color.md) § *Banned*).
- may extend them in the app's own `@theme` block when the product carries its own brand — the default theme
  works out of the box, so only the keys that must differ are overridden.

---

## `cn()`

- must reach `cn()` from `@{brand}/common/lib` in a multi-app repo, and from the library in a single-app one —
  a second local copy of clsx + tailwind-merge resolves overrides differently.
- the rule that classes compose through `cn()` at all is
  [tailwind](../../../core/lla/constructs/tailwind/tailwind.md) § *The rules every group inherits*.

---

## Dark mode

- must switch themes by toggling the class on `document.documentElement`, which is the app's element to own.
- must drive that toggle through the shared theme hook (`useTheme`), never an ad-hoc `localStorage` read in a
  component.
- the `dark:` variant itself is [variants](../../../core/lla/constructs/tailwind/variants.md).

---

## Neighbours

- [platform](platform.md) — the vector this doc sits in
- [dev-server](dev-server.md) — the other half of the Vite config
- [architecture](../architecture/architecture.md) — the `bootstrap/` layer `index.css` lives in
- [constructs](../../../core/mla/constructs/constructs.md) § *Styling* — the variants file a component co-locates
