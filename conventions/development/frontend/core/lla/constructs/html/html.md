# HTML

*Last updated: 2026-10-01*

> Every HTML element we may write, what each one is for, and the elements banned outright.
> Purpose — the element carries the accessibility semantics; the wrong one costs a `role`, a `tabindex`, a handler.
> Use case — reach here before writing a tag, and whenever a tag is unfamiliar in this codebase.

## The groups

| Group | Covers | Doc |
|---|---|---|
| flow | `div` · `span` — the elements that mean nothing | [flow](flow.md) |
| text | `p` · `strong` · `em` · `code` · `blockquote` · `mark` · `kbd` | [text](text.md) |
| lists | `ul` · `ol` · `li` · `dl` · `dt` · `dd` | [lists](lists.md) |
| forms | `form` · `input` · `label` · `select` · `textarea` · `fieldset` · `legend` | [forms](forms.md) |
| headings | `h1`–`h6` | [headings](headings.md) |
| landmarks | `main` · `nav` · `header` · `footer` · `aside` · `section` · `article` | [landmarks](landmarks.md) |
| interactive | `button` · `a` · `details` · `summary` · `dialog` | [interactive](interactive.md) |
| embedded | `img` · `svg` · `video` · `audio` · `iframe` · `canvas` | [embedded](embedded.md) |
| tables | `table` · `thead` · `tbody` · `tr` · `th` · `td` · `caption` | [tables](tables.md) |
| global attributes | `id` · `class` · `role` · `aria-*` · `data-*` | [global attributes](global-attributes.md) |

---

## The rule every group inherits

- must pick the element whose **meaning** matches, then style it — never `div` with the meaning added back by `role`.
- must let the element supply focusability, keyboard activation and the accessibility role before adding any by hand.
- must keep a native attribute's exact HTML spelling on a prop that forwards it
  ([naming](../../notation/naming/naming.md)).
- must reach for a `@wow-two-beta/ui-vue` component before a raw element — the library already made the choice
  ([constructs](../../../mla/constructs/constructs.md) · [visual kinds](../../../mla/constructs/visual/visual.md)).
- must not gate on lint: no `jsx-a11y` / `vue-a11y` plugin is installed, so these rules are review-enforced.

---

## Banned

- **`<center>` · `<font>` · `<big>` · `<marquee>` · `<blink>`** — reach for a Tailwind utility; these are
  presentational and removed from the standard.
- **`<b>` · `<i>`** — reach for `<strong>` / `<em>` ([text](text.md)), or a `font-bold` / `italic` utility when the
  weight is decoration only.
- **`<br>` for spacing** — reach for a `space-y-*` / `gap-*` utility; a line break is content, not layout.
- **`<table>` for layout** — reach for `grid` or `flex`; a layout table announces rows and columns that do not exist.
- **inline `<style>` / `<script>`** — reach for the stylesheet and the module; both defeat the CSP and the bundler.
- **`<form>` without a `submit` path** — reach for a `<div>`; a form that cannot submit still swallows the Enter key.

---

## Neighbours

- [css](../css/css.md) — what styles these elements
- [tailwind](../tailwind/tailwind.md) — the utility layer that does the styling
- [constructs](../../../mla/constructs/constructs.md) — the roles these elements are wrapped into
