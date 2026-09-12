# Variants

*Last updated: 2026-09-10*

> Every variant prefix — state, breakpoint, theme, relationship, arbitrary selector — and the ones that hide a rule.
> Purpose — a variant keeps a conditional style in the markup, where the rest of the box's appearance already lives.
> Use case — reach here before styling a state, a breakpoint or a child, and before writing a bracket selector.

## The variants

The largest surface in the group. `focus-visible:` and `hover:` lead it; `[&>*]:` bracket forms carry generated
children.

| Variant | Applies when | Verdict |
|---|---|---|
| `hover:` · `active:` | pointer over, pointer down | `use` |
| `focus-visible:` | focus from the keyboard — the focus-ring variant | `use` |
| `focus:` | focus from any source, including a mouse click | `use with care` |
| `focus-within:` | focus anywhere inside | `use` |
| `disabled:` · `read-only:` · `required:` · `invalid:` | native control states | `use` |
| `checked:` · `indeterminate:` · `placeholder-shown:` | native selection and empty states | `use` |
| `first:` · `last:` · `odd:` · `even:` · `only:` | a child's position among its siblings | `use` |
| `sm:` · `md:` · `lg:` · `xl:` · `2xl:` | at or above a breakpoint — mobile-first | `use` |
| `max-sm:` · `max-lg:` | below a breakpoint | `use with care` |
| `dark:` | under the `.dark` class, via the custom variant | `use` |
| `motion-safe:` · `motion-reduce:` | the user's motion preference | `use` |
| `forced-colors:` · `print:` | forced-colors mode, and print | `use with care` |
| `group-hover:` · `group-focus-within:` · `group-data-[…]:` | an ancestor marked `group` | `use` |
| `peer-checked:` · `peer-focus-visible:` · `peer-disabled:` | a marked previous sibling | `use` |
| `group/name:` · `peer/name:` | a named group or peer, when they nest | `use` |
| `data-[state=open]:` · `data-[disabled]:` | component state on a `data-*` attribute | `use` |
| `aria-[expanded=true]:` · `aria-checked:` | state already on an ARIA attribute | `use` |
| `has-[:checked]:` · `has-[:focus-visible]:` | a parent matched by its descendants | `use with care` |
| `[&>*]:` · `[&>svg]:` · `[&>*:first-child]:` | a direct child a component cannot put a class on | `use with care` |
| `[&::-webkit-slider-thumb]:` · `[&::-moz-range-thumb]:` | a native control's shadow parts | `use` |
| `[&::-webkit-scrollbar]:` | a scrollbar styled per engine | `use with care` |
| `*:` · `**:` | every child, or every descendant | `use with care` |
| `[&_.some-class]:` | a descendant matched by class | `banned` |
| a bracket variant reaching into another component | a rule across a component boundary | `banned` |
| `dark:` on a semantic token | a flip the token already performs | `banned` |
| a variant stack more than three deep | a rule no reader can evaluate at a glance | `use with care` |

- must reach for `focus-visible:` for the focus ring, and `focus:` only where a mouse click should show it too.
- must write breakpoints mobile-first — the unprefixed class is the phone, `sm:` and up are additions.
- must reach for `group` / `peer` before a bracket selector, and a bracket selector only for generated children.
- must let `dark:` handle only what no token covers — an asset swap, a shadow, a blend.
- must move a class map of three or more states out to the recipe
  ([styling](../../../../shapes/app/platform/styling.md)).

---

## Banned

- **`[&_.some-class]:`** — reach for `data-*` on the target; a class-matching descendant selector depends on a class
  another file owns, so a rename there breaks this rule with no error anywhere.
- **a bracket variant reaching into another component** — reach for a prop or a slot
  ([constructs](../../../mla/constructs/constructs.md)); the inner structure is not a contract, so the rule survives
  exactly until that component's next refactor.
- **`dark:` on a semantic token** — reach for the bare token; `dark:bg-card` restates what `bg-card` already does
  under `.dark`, and the two disagree the moment the token is re-pointed ([color](color.md)).

```vue
<!-- ✅ state from data-*, ring on focus-visible, group for the ancestor relationship -->
<div class="group" :data-state="isOpen ? 'open' : 'closed'">
  <button type="button" class="outline-hidden focus-visible:ring-2 focus-visible:ring-ring
                               group-data-[state=open]:rotate-180">…</button>
</div>

<!-- ❌ a class-matching descendant, and a dark: restating what the token already flips -->
<div class="[&_.chevron]:rotate-180 bg-card dark:bg-card">…</div>
```

---

## Neighbours

- [authoring](authoring.md) — `@custom-variant`, where `dark:` is defined
- [border](border.md) — the focus recipe `focus-visible:` completes
- [selectors](../css/selectors.md) — the CSS forms these variants replace
- [styling](../../../../shapes/app/platform/styling.md) — `cn()` and the `tailwind-variants` recipes
- [global attributes](../html/global-attributes.md) — the `data-*` these variants read
