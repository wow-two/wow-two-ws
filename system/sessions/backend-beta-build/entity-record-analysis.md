# Entity records and classes

*Last updated: 2026-09-12*

> P01 reopened: compare concrete behavior under WoW2's philosophy, including data-oriented models and `with`.

## Conclusion

`sealed class` is not inherently superior to `sealed record` for our entities. Normal EF materialization,
tracking and updates work with records. A record communicates a data-oriented model and supplies a concise,
typed copy operation; both are useful design benefits even when the type also represents a persisted row.

The meaningful extra obligations concern generated equality/hash behavior, shallow copying, validation and
generated formatting. A plain class avoids some of these defaults but loses the built-in `with` operation.
The costs should decide the policy, not Microsoft's preference. The rule-selection owner is
[WoW2 convention philosophy](../../../conventions/philosophy/philosophy.md).

The earlier class conversion has been paused, the record baseline restored, and P01 reopened. This analysis
does not decide the entity-copy workflow or the separate value-object invariant/equality questions.

## What the EF recommendation does and does not mean

EF compares tracked instances by reference even if the entity overrides equality. Its special risk is a
navigation collection that uses value equality. A context also permits only one tracked instance per key;
this applies equally to records and ordinary classes. These are framework behaviors, independently of the
recommendation to avoid record entities. [EF identity resolution](https://learn.microsoft.com/en-us/ef/core/change-tracking/identity-resolution#overriding-object-equality).

The claim “EF relies on reference equality, therefore records cannot work” is refuted. The relevant question
is where application and collection code uses the record's generated equality.

## Benefits retained by records

- **Data intent:** the declaration marks a model primarily carrying data. It remains a reference type and may have behavior.
- **Typed copying:** `var proposed = current with { Name = "B" };` keeps unspecified scalar values and leaves the original scalar state unchanged.
- **Snapshots and proposals:** concise variants work well for fixtures, comparisons and detached update proposals, subject to copy depth.
- **Generated members:** equality and printable member values can save code when those semantics are wanted.

A record does not imply immutability. Our entity convention uses mutable body properties; a class can also
have immutable properties. Both forms allocate objects; this pass provides no benchmark claiming one is faster.

## Concrete costs and their scope

| Behavior | Cost of the record default | What a plain class changes | Possible WoW2 rule |
|---|---|---|---|
| Equality | Generated equality follows instance field values, not solely the database key. Two states of one row may be unequal. | Default equality is object identity, which is not database-key equality either. | Name key comparison explicitly; reserve record equality for the intended state comparison. |
| Mutable hashes | Changing a participating field can change the hash while the object is in a hash set or dictionary. | Default reference hash survives property mutation. | Use keys for lookup, or reference comparers for collections of mutable entities. |
| Navigation collections | Two equal unsaved records can collapse in a default HashSet; later mutation can break removal. | Separate class instances remain distinct by default. | Force reference equality for identity-bearing navigation collections. |
| Copy depth | `with` shares reference members such as mutable lists and navigation objects. | There is no built-in copy; a hand-written shallow copy has the same issue. | State whether a copy is a scalar proposal or a graph snapshot; do not promise deep isolation. |
| Copy validation | A `with` copy does not rerun the ordinary constructor's cross-field checks. | No built-in copy path, but writable properties can still bypass invariants. | Resolved P02: external validation at the accepting boundary; constructor data checks exceptional. |
| Formatting | Generated `ToString` includes public member values, including a secret if exposed there. | Default formatting does not print the object's data. | Avoid whole-entity logging or customize safe formatting; this is not a reason to discard all record benefits. |
| Inheritance | Record inheritance must stay in the record family. | A class can use an ordinary class base. | Evaluate only if an actual required base is incompatible; both sealed forms prohibit derived types. |

These are conditional costs, not seven failures every record will encounter. A class with custom value
equality, a shallow-copy helper or data-printing `ToString` can reintroduce the same behaviors.
Copy, equality and formatting semantics are specified by the
[C# record reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/record).

## `with` and persistence

### Resolved comparison and validation scope — 2026-09-12

The developer normally compares database keys or field values, because separate query results can represent
the same data. This is a useful semantic comparison, not an objection to records. A `HashSet<Guid>` or
`Dictionary<Guid, Entity>` with stable key values avoids mutation of entity fields changing the stored hash.
A comparer reading mutable entity fields still requires those fields to remain stable while the entity is
stored as a hashed element/key. Immutable extracted field tuples also work. Equality and hashing remain
separate from EF's internal reference identity and navigation membership requirements.

Generated record equality does not recursively compare list/array contents. A deep clone can isolate those
collections without making independently allocated collections equal. Structural equality remains P03.

Validation starts outside constructors, in a pure extension method or dedicated validator, currently backed
by FluentValidation. Rules can grow without changing the construction API. Created, copied and deserialized
instances are candidates until accepted by the relevant validation boundary. Constructor data checks are
exceptional documented type contracts; programmer argument guards remain distinct. Neither a class nor a
record gets a general validation advantage under this policy. The normative owner is
[validation placement](../../../conventions/development/backend/dotnet/core/mla/domains/validation/validation.md#placement).

### Persistence behavior

The copy is a new object carrying the same key unless the expression changes it. That can represent a
proposed state of the same row; it does not inherently claim a new row or imply invalid data.

```csharp
var proposed = current with { Name = "B" };
```

There are three different operations:

1. **Copy for calculation or display:** no persistence operation is implied. Shallow-copy/equality rules still apply.
2. **Save through a context with no original instance tracked:** the detached copy can be attached or updated.
   `Attach` alone considers it unchanged; a write needs modification state or supplied original values.
3. **Save while the original is tracked:** attaching the copy conflicts. Applying accepted scalar changes to
   the tracked original works. A manually copied class has the same conflict.

The isolated experiment verified all three relevant EF write outcomes, including
`CurrentValues.SetValues(copy)` on the existing tracked instance. That operation is not an automatic graph
merge: navigation changes, original concurrency values, allowed fields and partial updates still need a contract.

The current SDK makes this distinction relevant:

- [EfRepository.GetByIdAsync](../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/EntityFrameworkCore/Repositories/EfRepository.cs)
  performs a query without an explicit no-tracking operator (line 34); normal context defaults track it.
- `UpdateAsync` calls `Set.Update(entity)` (line 66). Reading and sending a `with` copy through the same tracked
  repository/context therefore reaches the duplicate-instance constraint.
- A record-friendly update contract is possible in our SDK. It must define how proposed state reaches the
  tracked row rather than requiring products to detach or clear the context as a workaround.

The [prototype rule](../../../conventions/development/backend/dotnet/core/mla/constructs/patterns/prototype.md)
now permits entity candidates and snapshots. The earlier blanket ban was a house rule, not a C# or EF
prohibition. Accepting a copied candidate through the repository update API remains the P01 workflow decision.

## Verification

These are isolated experiments, not tests of the whole SDK or its PostgreSQL/provider/interceptor combinations.

### Record semantics

SDK `10.0.300`, target `net10.0`; ten checks passed:

1. Same-value copy compares equal while remaining a distinct reference.
2. Scalar change through `with` preserves the original scalar.
3. A referenced list is shared by original and copy.
4. Same key with changed state compares unequal.
5. Mutating a record's hashed state makes default HashSet lookup fail in the tested case.
6. A reference comparer preserves lookup after mutation.
7. Default class HashSet lookup survives property mutation.
8. Separate lists with the same contents do not produce structural record equality.
9. Generated `ToString` prints a synthetic secret held by a public property.
10. `with` can violate a relation checked only in the original constructor.

Command: `dotnet run --project /private/tmp/wow2-record-semantics/RecordSemantics.csproj`.
The [retained source](experiments/record-semantics/record-semantics.md) reproduces the checks; no SDK source was changed.

### EF comparison

SDK `10.0.300`, runtime `10.0.8`, EF Core/SQLite provider `10.0.3`, SQLite `3.49.1`, arm64;
twenty checks passed:

- Both forms insert, save repeated tracked mutations and preserve the tracked object identity.
- Record `with` copies and manually copied classes hit the same duplicate-key tracking conflict under Attach and Update.
- An unchanged equal record copy also conflicts; value equality does not merge it into the tracked original.
- Detached record copies persist through fresh-context Update and Attach plus explicit modified state.
- Attach alone produces no write; SetValues onto the tracked instance persists the changed values.
- Default HashSet navigation loses one of two equal transient records before persistence; the class retains both.
- A reference comparer preserves both record instances and allows removal after mutable state changes.

Full experiment evidence is retained in [EF experiment results](entity-record-ef-evidence.md).

## Decision boundary

Records remain a viable house choice if data-oriented declarations and copy syntax are worth explicit
identity-collection, copy-depth and persistence-update contracts. Classes are simpler when default reference
semantics and in-place tracked mutation are the intended workflow. Neither answer follows from external authority.

The open design input is whether `entity with { ... }` should be accepted as a proposed update by our
repository contract, or mainly used for detached calculations/snapshots. P01 remains open in the
[audit](conventions-audit.md#points); N114 cannot trigger a class conversion while it is open.
