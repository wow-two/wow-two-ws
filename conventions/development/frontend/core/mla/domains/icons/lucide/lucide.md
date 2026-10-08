# Lucide

*Last updated: 2026-10-01*

> The one icon set a product frontend uses, bound to the [icon contract](../icons.md).
> Purpose — the SDK already ships this set, so a second one doubles the glyph bundle and splits the visual language.
> Use case — adding an icon to a screen, sizing one, or replacing another set's glyph.

## Selection

- must use `lucide-vue-next` as the product's only icon set.
- must declare the version range the SDK declares, so the app and the SDK resolve one copy.
- must not add a second set — another icon package, an icon font, a sprite sheet.
- must not paste a set's SVG into a template; import the glyph component.
- must write a custom adapter component for a brand mark or a glyph the set lacks
  ([icons](../icons.md#providers)).

---

## Import

- must import each glyph by name from the package root — `import { RefreshCw } from 'lucide-vue-next'`.
- must not import the whole set, and must not resolve a glyph from a name string.
- must pass the glyph component to an SDK component's icon prop or slot.
- must render a glyph that carries meaning on its own through the SDK `Icon`, with an `aria-label`.
- must file the import in the third-party group ([imports](../../../../lla/notation/style/imports.md)).

---

## Values

| Size | Where |
|---|---|
| `12` | dense metadata — a table cell, a chip, a caption |
| `14` | inside a control — a button, an input, a menu trigger |
| `16` | beside body text — a nav item, a list row, a menu item |
| `20` | standalone — the `Icon` default |
| `24` and up | a state or hero mark — an empty state, a splash |

- should take a size from that scale; an off-scale size needs a reason in the layout.
- must set the size with the numeric `size` prop; a CSS-unit size goes on the class ([icons](../icons.md)).
- must keep the set's default stroke width.
- must let a glyph inherit `currentColor`; a tone comes from a text token class, never a hex value.
- must take a severity glyph from the SDK's `SeverityIcons`, so each severity keeps one shape everywhere.

---

```vue
<!-- ✅ one set, named imports, the control's own slot -->
<Button><template #leading><RefreshCw :size="14" /></template>Refresh</Button>
<Icon :icon="TriangleAlert" aria-label="Deployment failed" />
<!-- ❌ a second set, and a glyph resolved by name -->
<IconRefresh />            <!-- @tabler/icons-vue -->
<Icon name="refresh" />
```

---

## Neighbours

- [icons](../icons.md) — the contract this provider satisfies
- [document](../../../../../shapes/app/platform/document.md) — the favicon and app icons, which are logo assets
- [logo system](../../../../../../../design/identity/logo-system.md) — the product symbol those assets export
