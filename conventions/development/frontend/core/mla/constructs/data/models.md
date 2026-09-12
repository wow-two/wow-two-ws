# Models

*Last updated: 2026-09-10*

> How to declare a data type, in the order you build one. Scalars and dates →
> [type mapping](../../domains/api/type-mapping.md); enums → [enums](../../../lla/components/enums.md); the API
> envelope and its errors are integration → [state and data](../../domains/data/state-and-data.md).

**Flow:** `owner → kind → file + name → shape + doc → members (doc → type) → mapper`

---

## 1. Owner

The suffix follows whoever owns the shape, never whether a mapping exists.

- must suffix a shape the **wire** owns — `*Dto` on a read, `*ApiRequest` on a write.
- must suffix a shape the **app** owns `*Model`, mapped from a `*Dto` or computed fresh.
- must leave a straight read its `*Dto`; nothing reshapes it, so it needs no `*Model`.
- must not name a `*Model` after the endpoint, the client, or the response that fed it.
- must not suffix `Entity` — the app declares no entity type, and a read shape stands in its place.

---

## 2. Kind

| Kind | Name | Layer |
|---|---|---|
| read shape | `{Noun}Dto` | `integration` |
| app representation of a backend entity | `{Noun}Model` | `domain` |
| service-computed shape, no wire counterpart | `{Noun}Model` | `domain` · `application` |
| write contract | `{Noun}{Verb}ApiRequest` | `integration` |
| nested write sub-shape | `{Noun}Dto` | `integration` |
| list row | `{Noun}RowDto` | `integration` |
| list query | `{Noun}QueryDto` | `integration` |
| content variant | `{Noun}Content` | `domain` |
| descriptor · catalog | `{Noun}Descriptor` · `{noun}Catalog` | `domain` |
| a seam's call knobs | `{Noun}Options` | beside the seam it configures |

- must name the role in the prefix; only a wire **write** payload breaks the pattern, as an `*ApiRequest`.
- must leave an enum name bare — the suffix is what separates a `BuilderStyleDto` from it.
- must distinguish editable input, parsed schema output and submitted request when their shapes differ
  ([forms](../../domains/forms/forms.md)); a direct request binding is valid only when the shapes match.
- **write contract** — noun-first, verb = the CRUD action (`Create` · `Update` · `SetActive`). A shared
  create+update body is `{Noun}CreateUpdateApiRequest`; split it only once the bodies diverge.
- **descriptor + catalog** — a variant-set's lookup table, not a wire shape, so no `*Dto`. `{Noun}Descriptor`
  is one entry (`{ id, label, mode }`); `{noun}Catalog` is the exhaustive list plus a `{noun}(id)` lookup.
- must name it `Descriptor` not `Spec` (`.spec` collides with tests) and `Catalog` not `Registry` — `*Registry`
  names a behavior seam ([headless suffixes](../behavior/headless-suffixes.md)).
- must pair `*Options` with the one call or module it configures, and name it for that — `ApiClientOptions`.
- must send an `*ApiRequest` on a write, never a read shape — a read carries server-owned fields
  (`id` · `slug` · `scanCount`) a write must not.
- must return the DTO on an unchanged read, or its app-owned model when mapped; reserve `*Response` for a real envelope.

---

## 3. File + name

- must give every type its own file, named for the type — no mixed-bag file, no grouped family.
- must name the file `PascalCase.ts`, matching the type it declares.
- must place a data type in a **role-group** folder inside its slice — `models/` holds models, dtos and
  results; `constants/` holds constants (`domain/codes/style/models/` · `integration/codes/models/`).
- must co-locate a type in the slice that **owns** it — a `*Model` in `domain/`, a `*Dto` / `*ApiRequest`
  with its client in `integration/` ([architecture](../../../../shapes/app/architecture/architecture.md)).

---

## 4. Shape + doc

- shape → [typescript](../../../lla/constructs/typescript/typescript.md) § *The constructs*.
- must open a type doc with **`Represents`**, one line; **`Defines`** only for an abstraction, contract or
  enum ([documentation](../../../lla/notation/documentation/documentation.md)).

---

## 5. Members

Per member, in order: **doc → type**.

- must doc each member per [documentation](../../../lla/notation/documentation/documentation.md) § *Verb starters*.
- must leave exactly one blank line between every documented member (a member = its doc + the field).
- must mark required as `field: T`, optional as `field?: T`
  ([typescript](../../../lla/constructs/typescript/typescript.md) § *Absence*).
- must type each member per [type mapping](../../domains/api/type-mapping.md); enums per
  [enums](../../../lla/components/enums.md).
- must group a large model with `// ── Section ──` bands; no `@example`, no mechanism notes.

```typescript
/** Represents an issued invoice and its lifecycle status. */
export interface InvoiceModel {
  /** The invoice's unique id. */
  id: string;

  /** The invoice reference shown to its recipient. */
  reference: string;
}
```

---

## 6. Mapper — only where the app owns the shape

- must reshape `*Dto` → `*Model` in one `mapInvoice(dto)` at the integration boundary
  ([state and data](../../domains/data/state-and-data.md)).
- must not leak a `*Dto` past `integration/` once a `*Model` exists for it.
- must keep a straight read as its DTO when its validated wire representation already fits the caller.
- must decode declared fields at integration when richer values are needed; never infer dates from arbitrary strings.
- must validate untrusted input at runtime; a static DTO annotation does not validate a payload.
- must return a [result](result.md) from a mapper that can fail on a shape it did not expect.

---

## Discriminated dispatch

- must model a variant set (e.g. content types) as a discriminated union on a `type` field.
- must dispatch through a `Record<{Id}, {Noun}Descriptor>` catalog — a missing variant is a compile error.
- may model a meaningful static/dynamic distinction in the descriptor; do not require it for unrelated variant sets.

---

## Neighbours

- [result](result.md) — the carrier a fallible operation returns around these shapes
- [constants](../../../lla/components/constants.md) — the fixed values a member defaults to
- [enums](../../../lla/components/enums.md) — the value set a member is typed as
- [architecture](../../../../shapes/app/architecture/architecture.md) — the slice a model is declared in
