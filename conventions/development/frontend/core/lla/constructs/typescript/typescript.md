# TypeScript

*Last updated: 2026-09-10*

> Every TypeScript construct we may declare, what each one is for, and the constructs banned outright.
> Purpose — settle the *form* once, so no role doc has to re-argue `interface` vs `type`.
> Use case — reach here before declaring a type, and whenever a construct is unfamiliar in this codebase.

## The constructs

| Construct | Declares | Data or behavior | Verdict |
|---|---|---|---|
| `interface` · `interface extends` | a named object shape, open to merging | data | `use` |
| `type` alias — object | a closed object shape, no declaration merging | data | `use with care` |
| `type` alias — union · discriminated union | alternative types, narrowed by a literal member | data | `use` |
| bare string-literal union | a value set with no value behind it | data | `banned` |
| intersection `A & B` · branded alias | one shape combining several, or a nominal primitive | data | `use with care` |
| literal type | one value standing as a type | data | `use` |
| template-literal type | a string type composed from parts | data | `use with care` |
| `const` object + `as const` | a compile-time readonly literal value source | data | `use` |
| `(typeof X)[keyof typeof X]` | the union of a const object's values | data | `use` |
| `enum` · `const enum` | TS's nominal enum, and its inlined form | data | `banned` |
| `class` | a constructible type carrying instance state | behavior | `use with care` |
| `abstract class` · `abstract` member | a base no caller may instantiate | either | `banned` |
| `implements` · `private` · `static` | what a class promises, and who reaches a member | either | `use with care` |
| `accessor` field | a getter/setter pair over a hidden field | data | `banned` |
| `function` · `async function` | a named, hoisted operation | behavior | `use` |
| arrow function | an inline function value | behavior | `use` |
| generator `function*` · overloads | a yielded sequence, or many signatures on one body | behavior | `use with care` |
| type predicate `x is T` | a return that narrows the caller | behavior | `use` |
| assertion signature `asserts x is T` | a call that narrows by throwing | behavior | `use with care` |
| type parameter `<T>` | a type the caller supplies | — | `use` |
| `extends` constraint · default `<T = X>` | the bound, and the argument used when none is given | — | `use` |
| `const` type parameter `<const T>` | infers the argument's literal type | — | `use with care` |
| conditional type · `infer` · mapped type | a type computed from another type | — | `use with care` |
| `keyof` · `typeof` · `T[K]` · `Omit` `Pick` | a type read off another type or a value | — | `use` |
| index signature · readonly tuple | keys not known ahead, or a fixed-length group | data | `use with care` |
| `readonly` member · optional `x?: T` | a member no assignment replaces, or one that may be absent | data | `use` |
| `ReadonlyArray<T>` · `Readonly<T>` · `ReadonlyMap` | a shape or collection carrying no mutators | data | `use` |
| `T[]` · `readonly T[]` | the bracket array forms | data | `banned` |
| `T \| undefined` · `T \| null` | a member present but unset, or absent as a value | data | `use with care` |
| `unknown` · `never` | the type read only once narrowed, and the one no value inhabits | — | `use` |
| `any` | a value the compiler stops checking | — | `banned` |
| `object` · `{}` | any non-primitive, and any non-nullish value | — | `use with care` |
| `as T` · `as unknown as T` · non-null `!` | a type the compiler is told to accept | — | `use with care` |
| `satisfies` | checks a value against a type, keeping its literal type | — | `use` |
| module · named `export` · barrel `index.ts` | the unit of scope, and the names it publishes | — | `use` |
| `export default` · `export *` | an unnamed export, or a whole module re-exported | — | `use with care` |
| `import type` · inline `type` | a type-only import, erased at emit | — | `use` |
| `export =` · `import =` · `<T>x` | the CommonJS and pre-`as` declaration forms | — | `banned` |
| `namespace` | a nested runtime scope inside a module | either | `banned` |
| `declare namespace` · `.d.ts` · `declare global` | a type with no implementation behind it | — | `use with care` |
| decorator `@x` | a declaration wrapped where it is defined | behavior | `banned` |

- must declare an object shape as an `interface`, and reserve `type` for a union or a derivation.
- must expose collection inputs as readonly views; use `Array<T>` for an owned mutable working collection.
- must not treat a readonly type as runtime or deep immutability; aliases may still mutate the underlying value.

### Absence

- must model absence as `field?: T`, never `T | null` — the key is omitted, not sent empty
  ([type mapping](../../../mla/domains/api/type-mapping.md)).
- may declare `field: T | null` where `null` is a **value** the caller must state, so omitting the key becomes a
  compile error — a cleared selection, an absent error. Never where it only means absent.
- must keep a `class` to an `Error` subclass, a chained builder, or a React error boundary
  ([react boundaries](../react/boundaries.md)) — a value set is a `const` object.
- must declare a module-level operation as a `function`, leaving the arrow for an inline callback.
- must reach for `satisfies` where a check must keep the literal type, and `as` only where narrowing cannot reach.

```typescript
// ✅ the const object is the value source; the type derives from it
export const Nav = { Strip: 'strip', Pills: 'pills' } as const;
export type Nav = (typeof Nav)[keyof typeof Nav];

// ❌ no value source, so every use site spells a magic string
export type Nav = 'strip' | 'pills';
```

---

## Banned

A ban here is about the **construct**, whatever role holds it; a ban that depends on the role lives with that role
in [`mla/constructs/`](../../../mla/constructs/constructs.md).

- **`enum` · `const enum`** — reach for a `const` object ([enums](../../components/enums.md)); the member is
  nominal, so the wire string it equals will not assign to it, and a mapper appears at every read boundary.
  ambient `const enum` references also conflict with `isolatedModules`.
- **bare string-literal union** — reach for a `const` object ([enums](../../components/enums.md) § *Use*); a
  union declares no value, so each site spells the literal and a rename misses every one.
- **runtime `namespace`** — use a module and barrel under the house rule; `isolatedModules` rejects namespaces
  in non-module scripts, not every namespace. Type-only `declare namespace` is permitted for external contracts.
- **`any`** — reach for `unknown` and narrow it; checking stops at the annotation, and every error inside that value
  moves to runtime.
- **`T[]` · `readonly T[]`** — use `Array<T>` or `ReadonlyArray<T>` under the spelling rule;
  `readonly T[]` already blocks mutators, just as `ReadonlyArray<T>` does.
- **`abstract class` · `abstract` member** — reach for an `interface` and a function; an inheritance ladder has no
  unit of composition here, where a component composes and a hook closes over its own state.
- **decorator `@x`** — reach for an explicit wrapper call; a decorator moves behavior off the call site and pins the
  file to whichever proposal a build flag selects.
- **`export =` · `import =` · `<T>x`** — reach for ESM `export` / `import` and `as`; the first two contradict
  `verbatimModuleSyntax`, and the angle-bracket assertion is unparseable in a `.tsx` file.
- **`accessor` field** — reach for a plain `readonly` field; it exists to serve the decorator protocol banned above.

```typescript
// ✅ ReadonlyArray blocks the mutators, and the wire pairing holds
readonly rules: ReadonlyArray<CodeRuleDto>;

// ❌ the bracket form — `.push()` compiles, and mutates the caller's array
rules: CodeRuleDto[];
```

---

## Neighbours

- [enums](../../components/enums.md) — the value set every closed vocabulary is declared as
- [constants](../../components/constants.md) · [extensions](../../components/extensions.md)
- [constructs](../../../mla/constructs/constructs.md) — the app roles these constructs are shaped into
- [constructs](../constructs.md) — the verdict legend these rows are read with
- [naming](../../notation/naming/naming.md) — the file, folder and barrel spellings
- [C# constructs](../../../../../backend/dotnet/core/lla/constructs/constructs.md) — the same construct set in C#
