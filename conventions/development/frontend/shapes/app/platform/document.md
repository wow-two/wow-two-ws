# Document

*Last updated: 2026-10-02*

> The app's `index.html` — its head, its app icons, and what shows before the first script runs.
> Purpose — the first paint is the one render no component controls.
> Use case — standing up a new app's `index.html`, or fixing a theme flash, a blank tab icon or a wrong title.

## Head

- must set `<html lang>` to the app's default locale ([i18n](../../../core/mla/domains/i18n/i18n.md#locale)).
- must declare the charset and the viewport `width=device-width, initial-scale=1.0`.
- must set `<title>` to the product name; the router replaces it per place
  ([routing](../routing/routing.md#navigation)).
- must mark a private app `noindex, nofollow`.
- must give a public app a description and a social preview image instead.
- must load the app entry as one module script — `/src/bootstrap/main.ts`.
- must not inline a script or a style, so a strict Content-Security-Policy keeps working
  ([security](../../../core/mla/domains/security/security.md#hosting)).

---

## Icons

- must export the favicon from the product's standalone symbol
  ([logo system](../../../../../design/identity/logo-system.md#composition)).
- must keep the icon files in the app's `public/` and link each from the head ([assets](assets.md)).
- must ship one favicon — `favicon.svg` from a vector master, `favicon.png` from a raster one.
- may add `favicon-dark.*`, linked with `media="(prefers-color-scheme: dark)"`, when the symbol's ink fails on a
  dark tab strip.
- must ship `apple-touch-icon.png`, 180 × 180, on an opaque tile.
- must add a web manifest and its icons only when the app is installable.
- must check the tab icon at 16 and 32 CSS pixels in a real browser tab
  ([logo system](../../../../../design/identity/logo-system.md#surfaces)).

---

## First paint

- must apply the stored colour mode from `public/theme.js`, loaded in the head ahead of every stylesheet.
- must set both `html` and `body` backgrounds and `color-scheme` in the early external stylesheet, matching mounted light/dark tokens.
- must resolve an absent, blocked or `system` preference through `prefers-color-scheme`; refresh must not reveal the browser's default white canvas.
- must keep the early mode key and selector synchronized with the mounted colour-mode provider.
- must read the `ColorModeProvider` storage key there, treating `system` and a blocked storage as no choice
  ([styling](styling.md#colour-mode)).
- must render the splash's static twin inside the mount node, styled by `public/boot-splash.css`
  ([SplashScreen](../../../core/mla/components/feedback/splashScreen.md)).
- must keep the twin's logo, bar and colours equal to the mounted splash in both colour modes.
- must let mounting the app replace the twin; nothing else removes it.

```html
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex, nofollow" />
  <title>Wheelhouse</title>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <script src="/theme.js"></script>
  <link rel="stylesheet" href="/boot-splash.css" />
</head>
```

---

## Neighbours

- [platform](platform.md) — the vector this doc sits in
- [styling](styling.md) — the tokens the first paint has to match
- [shell](../shell/shell.md) — the frame that takes over once the app mounts
