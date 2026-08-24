# MLA — one app

*Last updated: 2026-08-23*

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

Every doc under `constructs/` and `components/` takes the same three `##` sections; a doc with nothing to say in
one omits it, never renames it. A `domains/` doc takes its shape from [domains](domains/domains.md) § *The shape*
instead, and a `lla/components/` doc from
[conventions](../../../../conventions.md) § *Authoring a convention*.

| Section | Sub-headings | States |
|---|---|---|
| Location | Group · Folder · File | the group a thing joins, the folder that wraps it, the file's name |
| Declaration | Type doc · Type name | the type's doc fields, and the type's own name |
| Content | Member docs · Members | each member's doc fields, and the members themselves |

- must give each kind or role **one file**, named for it — plural in `components/`, singular in `constructs/`.
- must state only the folder **name**, never the tree above it ([shapes](../../shapes/shapes.md)).
- may override any [`lla/notation/`](../lla/notation/notation.md) rule, stating the override in its own file.
- must give each doc field its own `####` sub-heading, linked to the doc that owns that field.
- must not sub-head a field the thing does not declare.
- must write each rule as what the code **must have** — a banned shape goes in the ❌ example, not a rule.
- must close every doc sub-heading and `Members` with one ✅ / ❌ pair; the ❌ must fail a rule stated above.
- must state a constraint as its own rule only when no positive rule already excludes it.
- must state a member **order** rule in `Members` — a reader cannot predict an order the doc never fixes.

````markdown
# {Thing}

*Last updated: 2026-08-19*

> {One line saying what it is.}
> Purpose — {what having it buys}.
> Use case — {when to reach for it}.

## Location

### Folder
- {rule}

### File
- {rule}

## Declaration

### Type doc

#### [Format](../lla/notation/documentation/documentation.md)
- must {rule}

```typescript
// ✅
{good}
// ❌ {why it fails}
{bad}
```

### Type name
- must {rule}

## Content

### Member docs

#### [Format](../lla/notation/documentation/documentation.md)
- must {rule}

### Members
- must {rule}

```typescript
// ✅
{good}
// ❌ {why it fails}
{bad}
```

## Neighbours

- {link} — {what it owns}
````

---

## Neighbours

- [core](../core.md) — the scope cut this bucket sits in
- [lla](../lla/lla.md) — the scope below: the forms every kind here is built from
- [hla](../hla/hla.md) — the scope above, once a second frontend exists
- [shapes](../../shapes/shapes.md) — the other cut: what changes with the deliverable
