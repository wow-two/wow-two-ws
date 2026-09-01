# Backend lane — register the components

*Last updated: 2026-08-24*

> A hand-off prompt for a separate chat working `conventions/development/backend/`.
> Purpose — the frontend registers every shipped component; the backend registers 8 of its 49 constructs.
> Use case — paste the block below into a new chat scoped to the backend conventions tree.

---

## Why

Both trees state the same three registers — definition · application · surface — in
`core/mla/components/components.md` § *The registers*. They differ only in coverage:

| Tree | Constructs | Component docs |
|---|---|---|
| frontend | 27 | 242 |
| backend | 49 | 8 |

The frontend's 242 are per shipped SDK component. The backend's 8 are per construct that is
"complete on its own" — its own stated test. Nothing is wrong with that test; what is missing is
the same completeness the frontend reached, measured against what the backend SDK actually ships.

---

## The prompt

```
Register the backend's components.

`conventions/development/backend/dotnet/core/mla/` holds 49 construct docs and 8 component docs.
The frontend tree registers every shipped component; the backend should reach the same completeness.

- read `components/components.md` § *The registers* for the split that already exists — definition
  in `constructs/`, application in `components/`, surface beside the code
- add a `components/{name}.md` for each construct a caller chooses between, matching the shape of
  the 8 that are already there
- open each new doc with a link to its construct, as `components.md` already requires
- leave the surface register empty — the backend SDK does not spec its own types yet
- keep the `## Location` / `## Declaration` section vocabulary the construct docs use; `patterns/`
  has its own `Shape · Use · Limits · Components` set and it does not transfer

Stay inside `conventions/development/backend/`. The frontend tree is another lane's and is mid-sweep.

Two docs there cite pre-move frontend paths and need repairing in the same pass:
`shapes/service/platform/responses/serialization.md:7` and
`shapes/service/platform/startup/launch-profiles.md:18`.
```

---

## Neighbours

- [conventions](conventions/conventions.md) § *Three axes, three words* — layer · bucket · register
- [components](conventions/development/frontend/core/mla/components/components.md) — the frontend's register
