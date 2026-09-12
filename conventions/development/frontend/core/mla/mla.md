# MLA — one app

*Last updated: 2026-09-10*

> Mid-level architecture: every rule that needs an app around it to mean anything.
> Purpose — keep app-shaped decisions out of `lla/`, where they would read as language rules.
> Use case — reach here for a kind you declare, which one to reach for, or a capability it consumes.

## The boundary

- **`mla/` when the rule reaches one app** — a kind you declare, a data-fetching contract, a capability's seam.
- **`lla/` when TypeScript, a framework or the browser already supplies the term** — a `type`, a `const` object,
  a doc block, and that form carried end to end in [`lla/components/`](../lla/components/components.md).
- **`hla/` when two of our frontends must agree** — [between our own frontends](../hla/hla.md).
- **[`shapes/`](../../shapes/shapes.md) when the rule loses its subject once a deliverable is absent** — a layer,
  a route, a bundler target, a package manifest.

The terms here are **ours**. `Dto`, `Entity`, `Component`, `Page` are aligned to our architecture, not to anything
TypeScript or a framework defines, which is why they land at this level however familiar they read.

---

## The three buckets

| Bucket | Answers | Lead |
|---|---|---|
| `constructs/` | what is this kind — one file per kind | [constructs](constructs/constructs.md) |
| `components/` | which one to reach for, and with what values | [components](components/components.md) |
| `domains/` | a capability, its contract and its providers | [domains](domains/domains.md) |

- **Three registers, one owner each.** `constructs/` defines the kind, `components/` chooses between kinds and
  fixes values, and one component's own props and slots live in its `{Component}.spec.md` in the SDK repo.
  Registers cut a kind in half; `lla` / `mla` / `hla` are the **layers**, and cut by reach.
- **A third party is a member of the domain that consumes it**, never its own axis.
- **The SDK boundary.** *How to use* and *what to use* from `@wow-two-beta/ui` is a convention and lives here; the
  SDK's own internals live in the SDK's docs. The scope follows the component, not the package.
- **Where a thing is placed is not here.** A doc names the folder — `overlays/`, `pages/` — and the deliverable
  says which tree that folder is created in ([shapes](../../shapes/shapes.md) § *The test*).

---

## Writing a doc in this scope [REQUIRED]

- must name one kind or role per file, using its singular name in both `constructs/` and `components/`.
- must give definition docs role-specific sections for classification, declaration, behavior and lifecycle as needed.
- must give application docs `Reach for it when`, `Instead of`, and `Values`; omit an empty section.
- must keep per-instance props, defaults and slots in the code-adjacent spec, not the application convention.
- must state only the folder name here; source-tree placement belongs to [shapes](../../shapes/shapes.md).
- must link inherited notation rules once per section and state only the role's extension or override.
- must give a doc field a subheading only when the role adds a field-specific rule.
- must place one focused example last in a doc-comment section, not one pair after every inherited field.
- must ensure a rejected example violates the rule illustrated by that section.
- must specify member order only where the role requires one beyond [notation](../lla/notation/notation.md).
- domains use [their own shape](domains/domains.md); all docs inherit
  [convention authoring](../../../../conventions.md#authoring-a-convention).

````markdown
# {Kind}

*Last updated: YYYY-MM-DD*

> {Selection boundary for this kind.}

## Reach for it when

- must use this kind when {responsibility}.

---

## Instead of

- must use {linked sibling kind} when {different responsibility}.

---

## Values

- must choose {value} when {condition}; instance defaults live in the component spec.
````

---

## Neighbours

- [core](../core.md) — the scope cut this bucket sits in
- [lla](../lla/lla.md) — the scope below: the forms every kind here is built from
- [hla](../hla/hla.md) — the scope above, once a second frontend exists
- [shapes](../../shapes/shapes.md) — the other cut: what changes with the deliverable
