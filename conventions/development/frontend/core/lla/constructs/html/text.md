# Text

*Last updated: 2026-09-10*

> Every text-level element we may write, what each one means to a screen reader, and the ones banned outright.
> Purpose — a text element states *why* a run reads differently; a utility only states *how* it looks.
> Use case — reach here before emphasising, quoting or marking up a run inside a paragraph.

## The elements

| Element | Means | Verdict |
|---|---|---|
| `<p>` | a paragraph — the default block of prose | `use` |
| `<strong>` | importance, seriousness or urgency | `use` |
| `<em>` | stress emphasis that changes the sentence's meaning | `use` |
| `<code>` · `<pre>` | a code fragment, and a block preserving its whitespace | `use` |
| `<blockquote>` | a quoted block, with an optional `cite` URL | `use` |
| `<mark>` | a run highlighted for the reader's current task | `use` |
| `<kbd>` · `<samp>` · `<var>` | a key to press, program output, a named variable | `use` |
| `<time datetime>` | a machine-readable date, time or duration | `use` |
| `<hr>` | a thematic break between sections of prose | `use` |
| `<abbr title>` · `<dfn>` | an abbreviation with its expansion, and a defining instance | `use with care` |
| `<cite>` | the title of a cited work — a title, never the speaker | `use with care` |
| `<small>` | legal small print or a side comment, not a font size | `use with care` |
| `<del>` · `<ins>` | a removal and an addition in an edited document | `use with care` |
| `<sub>` · `<sup>` | typographic sub- and superscript with real meaning | `use with care` |
| `<s>` | content no longer accurate — a struck price, not decoration | `use with care` |
| `<data value>` | a run paired with a machine-readable value | `use with care` |
| `<bdi>` · `<bdo>` · `<wbr>` | bidi isolation, forced direction, a soft break opportunity | `use with care` |
| `<ruby>` · `<rt>` · `<rp>` | East-Asian pronunciation annotations | `use with care` |
| `<br>` | a line break that is part of the content | `use with care` |
| `<q>` | an inline quote the browser adds quote marks to | `banned` |
| `<b>` · `<i>` | bold and italic with no meaning attached | `banned` |
| `<u>` | an underlined run with no meaning attached | `banned` |
| `<center>` · `<font>` · `<big>` · `<tt>` · `<strike>` | presentation, removed from the standard | `banned` |
| `<marquee>` · `<blink>` | motion nothing can stop | `banned` |

- must pick `<strong>` for importance and `<em>` for stress, then style the weight with a utility
  ([typography](../tailwind/typography.md)).
- must give `<time>` a `datetime` attribute — the visible text is for humans, the attribute is the value.
- must give `<abbr>` a `title`, since the expansion is the whole reason the tag is there.
- must let `<pre>` carry the whitespace and `<code>` the meaning — a code block nests one inside the other.

---

## Banned

- **`<b>` · `<i>`** — reach for `<strong>` / `<em>` when the run means something, and `font-bold` / `italic`
  when it is decoration only. Both tags read out as emphasis on some screen readers and as nothing on others, so
  the announcement depends on the reader rather than on the markup.
- **`<u>`** — reach for `underline` ([typography](../tailwind/typography.md)); an underlined run inside prose is
  read as a link by sighted users, and they click it.
- **`<q>`** — reach for `<blockquote>` or a literal quote character; the browser inserts the marks as
  generated content chosen by `lang`, so the rendered glyph is not the one the design specified.
- **`<center>` · `<font>` · `<big>` · `<tt>` · `<strike>`** — reach for a Tailwind utility; these are
  removed from the standard, so their rendering is a browser quirk rather than a defined behaviour.
- **`<marquee>` · `<blink>`** — reach for a `motion-safe:` animation ([transitions](../tailwind/transitions.md));
  neither honours `prefers-reduced-motion`, which the reduced-motion safety net exists to guarantee.

```html
<!-- ✅ the tag carries the meaning; the utility carries the look -->
<p class="text-sm text-muted-foreground">Renaming is <strong>permanent</strong>.</p>

<!-- ❌ bold with no meaning attached — announced as emphasis on some readers, as nothing on others -->
<p class="text-sm text-muted-foreground">Renaming is <b>permanent</b>.</p>
```

---

## Neighbours

- [headings](headings.md) — the elements that open a section of this prose
- [lists](lists.md) · [flow](flow.md) — the other content-level groups
- [typography](../tailwind/typography.md) — the utilities that style these runs
- [css](../css/css.md) — the `.prose` scope authored content is styled through
- [visual kinds](../../../mla/constructs/visual/visual.md) — the typography components to reach for first
