# Product icons

*Last updated: 2026-10-14*

> The icon files every product repo carries — folder, names, variants, format, and the order a consumer falls back in.
> Purpose — one deterministic path per variant lets Wheelhouse compute any icon from its repository.
> Use case — adding icons to a product repo, or resolving a product's or service's icon in a console.

## Ownership

- must fix every icon's path by this doc; must not list icon files in a manifest or store one as a database row.
- must not put a product, repository or brand name in an icon path, so a rename moves no file.
- must keep artwork design — masters, geometry, exports — in the brand guide
  ([logo system](logo-system.md#masters)).

---

## Variants

- must name each variant by three axes: theme, form and color.

| Axis | Values | Meaning |
|---|---|---|
| theme | `light` · `dark` | the surface it is drawn for — `light` has dark ink, `dark` has light ink |
| form | `full` · `short` | `full` is the symbol with its wordmark, `short` is the symbol alone |
| color | `colored` · `monochrome` | `colored` keeps the brand colors, `monochrome` is one flat ink |

- must draw `monochrome` in one flat ink.
- must keep every variant on a transparent background, with no backing tile.
- must ship `short-colored-light` and `short-colored-dark`, the pair a console asks for first.
- may ship the same artwork under both themes when it reads on either surface.
- may omit any other variant; [resolution](#resolution) fills the gap.

---

## Format

- must ship each variant as `svg` or `png`.
- should prefer `svg`; when both exist, `svg` wins.
- must not ship another format.
- must make an `svg` self-contained: a `viewBox`, outlined text, no script, no external reference.
- must export a `png` at the master's native resolution, at least 128 px on its shorter side.
- must keep each file at or under 256 KiB; a larger file is not read.

---

## Paths

- must keep every icon under `product/brand/icons/`.
- must name a file `{form}-{color}-{theme}.{ext}`, lowercase — `short-colored-dark.svg`.
- must place the product's icons directly in that folder.
- must place a service's icons in `product/brand/icons/services/{service}/`, under the same file names.
- must take `{service}` from the service's key in `deploy.yml`
  ([deploy descriptor](../../deployment/descriptor/deploy-descriptor.md#format)).
- may omit a service folder; that service shows the product's icons.
- must not nest deeper.

```
product/brand/icons/
├── short-colored-light.svg         the product, symbol only, for a light surface
├── short-colored-dark.svg
├── full-colored-light.svg          the product, symbol and wordmark
├── full-colored-dark.svg
└── services/                       multi-service repos only
    └── redirect/                   a key under `services:` in deploy.yml
        ├── short-colored-light.svg
        └── short-colored-dark.svg
```

- a single-service repo holds the product's files only; its one service shows them.
- a multi-service repo holds the product's files plus a folder for each service that has its own mark.

---

## Resolution

A request names a scope — the product or one service — and a theme, a form and a color.

- must use the first file that exists, trying these in order:
  1. the service folder, in the requested theme — skipped for a product request
  2. the product folder, in the requested theme
  3. the service folder, in the other theme — skipped for a product request
  4. the product folder, in the other theme
  5. the web app's favicon in `engineering/codebase/*.frontend-services/apps/web/public/` — `favicon-dark` for `dark`,
     then `favicon` ([document](../../development/frontend/shapes/app/platform/document.md#icons))
  6. a monogram: the product name's first letter on a tint derived from the name
- must try these variants within one folder and theme, in order:
  1. the requested form and color
  2. the requested form, the other color
  3. `short`, the requested color, then `short`, the other color — only when the form is `full`
- must try `svg` before `png` for every variant.
- must not substitute `full` for a requested `short`.
- must prefer any variant of the requested theme over any variant of the other theme.

---

## Consumption

- must compute each path from the repository; must not scan a repo for an icon.
- must request the theme of the active color mode, and request again when the mode changes.
- must request `short` beside a visible product name and `full` where the icon stands alone.
- must request `monochrome` only on a surface that tints its icons.
