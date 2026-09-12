# Enums

*Last updated: 2026-09-10*

> How to declare an enum and layer its display and send-object data — the enum is a `const` object, PascalCase
> key to camelCase wire value, and the only enum constant; displays and payloads attach as `Record<Enum, …>`.
> Use case — adding a value set, or replacing a bare string union with one.

**Flow:** `kind → location → declaration → displays → payloads → use`

---

## 1. Kind

|  | Domain enum | Non-domain enum |
|---|---|---|
| Tied to a product domain? | **yes** — even if it never hits the backend | no |
| Examples | `BarcodeFormat` · `ModuleShape` · `Plan` | `ButtonType` · `Key` (SDK UI tokens) |

- must classify by **domain tie** (`identity` · `codes` · `billing`), not by whether it crosses the API — a
  product-domain concept is a domain enum, a UI, app or integration token is not.

---

## 2. Location

- source placement → [app architecture](../../../shapes/app/architecture/architecture.md) or
  [library](../../../shapes/library/library.md).
- casing and the `Enum`-suffix ban → [naming](../notation/naming/naming.md).

---

## 3. Declaration

- must declare a `const` object `as const`, then derive the type from it on its own line, blank line before.
- must not use the TS `enum` keyword — it is nominally typed and `const enum` carries build pitfalls, while a
  const object tree-shakes and its value **is** the wire string.
- must JSDoc the type with a one-liner opening `Defines …`, and each member with `Refers to …`
  ([documentation](../notation/documentation/documentation.md)).
- must use PascalCase keys and camelCase values for house vocabularies; preserve exact external protocol/DOM values.
- must not add an `Unresolved` / `Unknown` sentinel member — three concerns stay separate:
  - **nothing selected** → `null` or an optional field according to the declared state/wire contract.
  - **any / all** → a real member present on **both** sides, or modelled as absence.
  - **unmappable inbound** → validate at the read boundary; do not silently coerce a value into a valid member.

```typescript
/** Defines the QR data-module body shape. */
export const ModuleShape = {
  /** Refers to a plain square module. */
  Square: "square",
  /** Refers to a module with rounded corners. */
  Rounded: "rounded",
} as const;

export type ModuleShape = (typeof ModuleShape)[keyof typeof ModuleShape];
```

---

## 4. Projections

- must key a display or a payload off the enum, never off a parallel list
  ([enum display](../../mla/constructs/data/enum-display.md) ·
  [enum payload](../../mla/constructs/data/enum-payload.md)) — the suffixes and their layer homes are
  ours, so they live with our constructs.

---

## 5. Use

- must not declare a domain or UI value set as a bare string union (`type X = "a" | "b"`) — a union has no
  value source, so every use site falls back to a magic string literal.
- must compare by member (`X.A`), never by the literal.
- must model a value that is one of an enum's members as the **enum**, never a family of derived booleans
  (`isSolid` + `isGradient`) — each added member then needs a new flag at every branch, and a fall-through
  `if/else` silently mishandles it.
- may derive the enum from a nullable or binary field, once, then compare the result.
- may keep a standalone predicate with no underlying enum (`const isEdit = Boolean(id)`) a boolean.
- must read display from the `Displays` record by value.
- must type a model or DTO field as the enum — the wire string already fits
  ([models](../../mla/constructs/data/models.md)).
- raw form values and parsed enum output → [forms](../../mla/domains/forms/forms.md).

```tsx
if (code.barcodeFormat === BarcodeFormat.QrCode) { }          // ✅ compare by member
if (code.barcodeFormat === "qrCode") { }                      // ❌ magic string

const fill = gradient ? FillType.Gradient : FillType.Solid;   // ✅ derive once, then compare
{fill === FillType.Gradient ? <GradientRow /> : <SolidRow />}
const isGradient = gradient !== null;                         // ❌ boolean stand-in

const { label, icon } = BarcodeFormatDisplays[code.barcodeFormat];
```

---

## Neighbours

- [naming](../notation/naming/naming.md) — the casing an enum, its label Record and a value set take
- [constructs](../../mla/constructs/constructs.md) — the component shape an enum-typed prop sits in
