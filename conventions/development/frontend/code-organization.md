# Code organization

*Last updated: 2026-06-09*

The TS counterpart of [../backend/code-organization.md](../backend/code-organization.md). File-per-type and one-component-per-folder live in [naming.md](naming.md) / [components.md](components.md); this file covers in-file layout.

## Language baseline

- **No `var`** — `const` by default, `let` only when reassigning. Applies to `.ts`, `.tsx`, inline `<script>`.
- TypeScript **strict** mode on.

## Section dividers

- **`// ── Section ──`** for field groups inside interfaces or large objects.
- **Plain comments** for logical sections inside JSX — no dashes/decorators.
- **Don't over-divide** — 2-3 fields don't need a divider.

```typescript
// ✅ lightweight label for field groups
export interface Listing {
  // ── Meta ──
  id: string;
  isValid: boolean;

  // ── Property ──
  propertyType: PropertyType | null;
}

// ✅ plain comment sections in JSX
{/* Image carousel */}
<div>...</div>

// ❌ dashed decorators
{/* ---- Image carousel ---- */}
// ---- Helpers ----
```

## Import order

Seven groups, ordered by distance from the runtime. **No blank lines between groups** — ordering alone. Within a group: value imports before `type` imports. (`@{brand}` = the repo's package scope, e.g. `@haven`.)

| # | Group | Pattern | Example |
|---|---|---|---|
| 1 | React / framework | `react`, `react-dom` | `import { useState } from "react"` |
| 2 | External libraries | any bare specifier not ours | `import { ChevronDown } from "lucide-react"` |
| 3 | Domain types & enums | `@{brand}/domain/...` | `import { Currency } from "@{brand}/domain/listings/core"` |
| 4 | Shared packages | `@{brand}/common/...`, `@{brand}/ui/...` | `import { cn } from "@{brand}/common/lib"` |
| 5 | App components | `@/.../components/...` | `import { PhoneChip } from "@/common/components/PhoneChip"` |
| 6 | App config / constants / extensions | `@/.../config/...`, `@/.../lib/...` | `import { CONTACT_TYPE_COLORS } from "@/common/lib/constants"` |
| 7 | Relative | `./`, `../` | `import { helper } from "./helper"` |

```typescript
// ✅ ordered by group, no blank lines
import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { type ContactType, ContactTypeLabels } from "@haven/domain/listings/core";
import { cn } from "@haven/common/lib";
import { PhoneChip } from "@/common/components/PhoneChip";
import { CONTACT_TYPE_COLORS } from "@/common/lib/constants";
```

> A **single-Vite-app** repo has no `@{brand}/*` packages — groups 3–4 collapse; `@/` (group 5–6) and relative (7) remain.

## File-internal order

Components: imports → types → constants → helpers → component → sub-components (see [components.md](components.md)). Non-component modules: imports → types → constants → exported members.

## See also

- [naming.md](naming.md) · [components.md](components.md)
- [../backend/code-organization.md](../backend/code-organization.md) — the C# sibling
