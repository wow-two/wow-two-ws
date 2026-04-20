# Icon Scraper — DX Tool

*Last updated: 2026-04-12 11:00 PM*

## Problem

Every icon library charges ~$100/year now, slowing down software engineering DX. Font Awesome Pro alone is $99/year for access to ~30k icons. Developers need quick access to high-quality icons without per-project licensing friction.

## Research Findings (Font Awesome)

### How FA Works
- **Search page** (`fontawesome.com/search`) shows ALL icons — free + Pro — together
- **Rendering:** SVG+JS method replaces `<i>` tags with inline `<svg>` elements
- **SVG paths** (`<path d="...">`) are fully visible in the DOM — no obfuscation
- **No anti-scraping protection** — no canvas rendering, no image-based delivery, no token-gated SVGs on the search page
- **Pro npm packages** require a paid token, but the website renders everything openly

### Free Tier
- ~2,000 icons under CC BY 4.0 + SIL OFL
- npm: `@fortawesome/free-solid-svg-icons`, `free-regular-svg-icons`, `free-brands-svg-icons`

### Scraping Difficulty: Low
- Headless browser (Playwright/Puppeteer) or API response interception
- Paginate search results, extract SVG paths + metadata (name, style, category)
- Few hours of scripting

### Legal Note
- Pro icons require a valid subscription even for private use
- Enforcement for private/internal use is effectively zero
- Free icons are fully legal to scrape and use

## Concept

Build a local icon index tool that aggregates icons from multiple free sources into a single searchable interface for development use.

### Sources to Aggregate
| Library | Icons | License | Format |
|---------|-------|---------|--------|
| Font Awesome Free | ~2,000 | CC BY 4.0 / SIL OFL | SVG |
| Lucide | ~1,500+ | ISC | SVG |
| Heroicons | ~300+ | MIT | SVG |
| Phosphor | ~7,000+ | MIT | SVG |
| Tabler Icons | ~5,000+ | MIT | SVG |
| Bootstrap Icons | ~2,000+ | MIT | SVG |
| **Total** | **~18,000+** | All free/open | SVG |

### Features (MVP)
- CLI or local web UI to search across all libraries
- Fuzzy search by name, category, tags
- Copy SVG / React component / CSS class to clipboard
- Preview at different sizes
- Show which library each icon comes from

### Future
- VS Code extension with inline icon preview
- Auto-suggest similar icons across libraries
- Icon diff (compare similar icons side by side)
- wow-two SDK integration — `WowTwo.Icons` package

## Technical Direction
- **Scraper:** Node.js + Playwright for libraries without npm packages; npm download for those that have them
- **Index:** JSON/SQLite local database
- **UI:** React local dev server or Electron
- **Updates:** Periodic re-scrape to catch new icons

## Open Questions
- Include FA Pro icons (gray area) or stay strictly legal with free sources only?
- Standalone tool vs wow-two SDK package?
- How to handle icon style normalization across libraries (stroke width, fill vs outline)?

## Status
`idea` — research done, needs implementation plan
