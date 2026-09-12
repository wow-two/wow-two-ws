# Imports

*Last updated: 2026-09-10*

> How to order and write `import` statements in `.ts`, `.tsx` and Vue script blocks — group order, sort, and
> the `type`-import form.
> Purpose — one deterministic layout, so any file's head reads the same and diffs stay minimal.

**Order:** `side-effect → third-party → SDK → @/ alias → relative`

---

## 1. Groups

- must order groups by **distance from the runtime**, outermost first, in this fixed sequence:

| # | Group | Matches | Example specifier |
|---|---|---|---|
| 1 | Side-effect | bare `import "…"`, no bindings | `"@fontsource-variable/geist"` · `"./index.css"` |
| 2 | Third-party | bare specifiers outside the SDK namespace | `react` · `vue` · `lucide-react` |
| 3 | SDK | `@wow-two-beta/*` roots and subpaths | `@wow-two-beta/ui-vue/presentation/actions` |
| 4 | `@/` alias | app-internal absolute imports | `@/domain/codes/core` |
| 5 | Relative | `../` then `./` | `./gradient` |

- must separate every non-empty group with exactly one blank line, and never blank-line within a group.
- must omit empty groups without leaving additional separators.
- must split group 4 in a multi-package repo — sibling `@{brand}/*` packages sort **before** the `@/` app
  alias, being more distant than app code.

```typescript
// ✅ five groups, one blank line each
import "@fontsource-variable/geist";

import { useEffect, useState } from "react";
import { ArrowRight } from "lucide-react";

import { Button } from "@wow-two-beta/ui/presentation/actions";
import { Stack } from "@wow-two-beta/ui/presentation/layout";

import { UserKind, type Me } from "@/domain/identity";
import { getMe } from "@/integration/identity";

import { AppLayout } from "./AppLayout";
```

---

## 2. Intra-group order

- must sort every group **alphabetically by module specifier** (the string after `from`), case-insensitive.
- side-effect (group 1): must keep global-effect imports (fonts, polyfills) **before** local `./*.css` — load
  order is semantic here, the one group where it overrides the sort.
- third-party (group 2): must place `react`, `react-dom` and `vue` first when present, then sort the rest.
- `@/` alias (group 4): must follow the [app layer order](../../../../shapes/app/architecture/architecture.md),
  then sort alphabetically by full path.
- relative (group 5): must place `../` before `./`, deeper before shallower, alphabetical at equal depth.
- **tie-break**: a `type`-only statement sorts after a value statement from the same module; otherwise the
  raw specifier string decides.

---

## 3. Type imports

- must inline the `type` modifier on the binding — `import { X, type Y } from "…"` — when one statement pulls
  both values and types from a module, so no parallel `import type` twin appears.
- must use a standalone `import type { … }` **only** when the **entire** statement is type-only (no value binding).
- must not add `import type` for a module already imported for a value — fold it in as `type Y`.

```typescript
import { UserKind, type Me } from "@/domain/identity";   // ✅ mixed → inline `type`
import type { CodeDto } from "@/domain/codes/core";       // ✅ all-type → standalone
import { Gradient } from "@/domain/codes/core";
import type { Gradient } from "@/domain/codes/core";      // ❌ split — fold into the value import
```

---

## 4. Rules

- React bindings → [JSX](../../constructs/react/jsx.md) § *React types — import named, never the UMD namespace*.
- must import the SDK through its published subpath (`@wow-two-beta/ui/presentation/forms`), never a deep
  path into the package's `src` or `dist`.
- app aliases and source placement → [app architecture](../../../../shapes/app/architecture/architecture.md).
- library source aliases and declaration safety → [delivery](../../../../shapes/library/delivery/delivery.md).
- must alias a name collision at the import, prefixing the SDK side (`Section as UiSection`), so the local
  symbol keeps the bare name.
- must keep all imports in the file head — a lazy `import()` for code-splitting is the sole exception.
- must import a symbol from the barrel that owns it, never from a second barrel that republishes it — a slice
  barrel is the export site, and a republishing one gives the same symbol two paths
  ([hooks](../../../mla/constructs/behavior/hooks.md) § *One export site*).
