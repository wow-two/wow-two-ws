# Library

*Last updated: 2026-09-10*

> Source layout for a package consumed by another frontend.

## Layout

- must inherit [core](../../core/core.md); this shape owns placement, packaging and verification.
- must group visual components by [kind](../../core/mla/constructs/visual/visual.md) under `presentation/`.
- must give each root component a camelCase folder, PascalCase main file and `index.ts` barrel.
- must keep variants beside source; stories/tests follow [SDK structure](../../../repo/structure/sdk-structure.md#tests).
- must not flatten a component beside sibling component folders.
- must place capability modules beside `presentation/`, named by capability nouns.
- must keep `foundation/` independent of presentation and higher-level capability modules.
- must keep presentation router-free; callers adapt links and route state.
- must lint those dependency boundaries and reject cycles between capability modules.

---

## Capability roles

| Folder | Holds |
|---|---|
| `models/` | the capability's data shapes |
| `enums/` | closed value sets |
| `constants/` | fixed values |
| `extensions/` | extension objects |
| `hooks/` | framework composables |
| `providers/` | context providers and their contexts |

- must keep the seam, factory and barrel flat at the capability root.
- must open a role-group only when it holds two files; a singleton role file stays flat.
- must keep the semantic role clear even when its singleton file is flat.
- must not nest a second capability; compose capabilities through their seams.
- must place implementation-specific adapters in `adapters/{provider}/`, distinct from capability roles.
- must expose the adapter through its declared public subpath; source folders do not dictate export names.
- must keep vendor imports inside the adapter; the contract entry never reaches it transitively.

```text
selection/
  Selection.ts
  SelectionModel.ts          singleton model
  UseSelection.ts            singleton hook
  index.ts

forms/
  FormEngine.ts
  models/                    two or more model files
  hooks/                     two or more hooks
  adapters/
    house/
    tanstack/
```

---

## Package boundary

- must follow [delivery](delivery/delivery.md) for exports, optional peers, CSS and publishing.
- must follow [compatibility](platform/compatibility.md) for runtime and SSR claims.
- must follow [testing](testing/testing.md) for behavior and packed-consumer gates.
- must keep application state/composition roots outside the package; factories accept caller-owned instances.
- must keep formatting configuration consistent with the shared notation owner.
