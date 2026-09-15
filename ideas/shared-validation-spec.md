# Shared validation — one rule set, backend and frontend

*Last updated: 2026-07-27*

> **Status:** both halves **shipped** (2026-07-27) — `wow-two-sdk-beta.ui` + `wow-two-sdk.backend.beta`.
> Piece 3 **killed**; `ErrorCodeResolver` and the resx resolver deferred by owner call — see § *Verdicts*.
> Split out of the forever-pin validation thread because it is a **frontend + backend SDK vector**, not a product
> task; nothing in forever-pin blocks on it. **Not yet adopted by any product.**

## Verdicts (2026-07-27)

The analysis below stands. Three things it did not name decided the shape:

- **the channel was `string[]` end to end.** The code was on the wire and discarded three times — twice
  client-side (`Validator.toStandardResult` has no spec slot for it; `fieldErrors` destructured it away).
  Widening that channel, not writing the catalogue, was the first unit of work.
- **the two vocabularies do not agree.** Server says `NotEmptyValidator`, client says `min`. Normalization is
  now a client-side alias table (`FLUENT_VALIDATION_CODES`), placed there so a form can adopt the catalogue
  before the backend normalizes anything, and keep working unchanged afterwards.
- **without operands a catalogue can only emit parameterless strings.** Every built-in refinement now reports
  its own limits (`{ max: 50, unit: 'characters' }`) beside its code.

| Piece | Verdict |
|---|---|
| 1 · path contract | already the SDK contract — documented, nothing built |
| 2 · message catalogue | **shipped, frontend.** The deliverable is a shared **vocabulary**, not a shared string table — strings render wherever they render; the vocabulary is what makes them agree |
| 3 · rule extraction | **killed.** `string().min().max().pattern()` already covers the entire extractable ceiling in one line per field. Codegen buys a build step, an assembly↔bundle version seam, and a silent-non-extraction failure mode against saving that line |
| 3′ · drift reconciliation | the cheap 80% — a test reflecting `IValidatorDescriptor` against the client validator's codes catches drift with no codegen. Product-level, optional, unbuilt |

**Ordering, resolved.** Not a choice available: `resolveSubmitFailure` groups by path, so cross-field order
dies at mapping. Within-field order is the server's array order; field-to-field order is DOM order. The only
order a user perceives was already right.

**Layer independence, resolved.** A shared *rule definition* (the neutral-format variant) conflicts — it makes
each layer's rules depend on a shared artifact. A shared *message catalogue* does not; messages are
presentation, not authority. Catalogue compatible, neutral format incompatible.

### Shipped — frontend (`wow-two-sdk-beta.ui`)

- `foundation/validation/Messages.ts` — `VALIDATION_CODES` vocabulary · `FLUENT_VALIDATION_CODES` /
  `FLUENT_VALIDATION_PARAMS` alias tables · `defaultValidationMessages` · `createMessageResolver`
- `foundation/http/FieldErrors.ts` — `fieldIssues()` keeps code + operands; `fieldErrors()` is now its
  message-only view
- `foundation/validation` — `ValidationIssue.params`; every built-in refinement reports its operands
- `forms-engine/SchemaValidation.ts` — house validators read natively (the spec erases codes);
  `createOptionsMessageResolver`
- `forms-engine/SubmitErrors.ts` — entries widened to `string | FieldIssue`; resolution runs after the path
  rewrite, so a catalogue entry sees the form path its label is keyed by
- `AppFormOptions.messages` / `.labels`; both adapters wired
- 21 unit + 12 conformance cases (6 × both engines); typecheck + lint clean

### Shipped — backend (`wow-two-sdk.backend.beta`)

- `FieldError.Params` — `IReadOnlyDictionary<string, object>?` from `FormattedMessagePlaceholderValues`
- `FluentValidationAdapter` strips `PropertyValue` (the **rejected value** — FV puts it in every failure's
  placeholder dict, so a verbatim copy would echo a rejected password into the response and the logs) and
  `PropertyPath` (duplicate of `Property`)
- `IFieldErrorMessageResolver` + `DefaultFieldErrorMessageResolver` passthrough — the localization plug;
  `errors[].message` previously bypassed `IErrorMessageResolver` entirely
- `AppErrorProblemDetailsFactory.Create` takes it as an optional trailing arg; all four handlers inject it
- `AddErrorHttpStatusMapping` `TryAdd`s the default
- convention → § *Rule codes and operands* + § *Localize field messages*; folder doc → what a failure carries
- 7 new tests; solution build + 222 tests green

**Deferred, owner call 2026-07-27:** `ValidatorOptions.Global.ErrorCodeResolver`. No product needs the wire
itself normalized, and the client alias table already covers it. Revisit when a non-JS consumer reads codes.

**Deferred:** the resx `IFieldErrorMessageResolver` implementation. The seam ships; the translation waits until
an app needs a non-English validator message. `.WithMessage` is the confirmed localization point.

FluentValidation's global hooks (all reflected off 11.11.0), why no wrapper type, and the settled per-tenant
config shape: `wow-two-ws/ideas/validation-wrapper-analysis.md`.

---

## Original analysis (2026-07-28)

### The ask (owner)

> "I dream about backend to frontend mapped validation — because that would be the ultimate validation:
> making the backend errors have the same validation mapping, order, etc."

### The owner's counter-position, which reframes the problem

The obvious framing is *"two hand-written rule sets always drift, so you need a single source."* The owner
rejects that:

- separate validation per layer is **wanted**, not a compromise — each layer validates its own scope
  (`conventions/development/backend/foundation/validation.md` § *Layer independence*).
- models and validation rules **do not change often**, so the drift window is narrow.

Both hold, and the second one changes what the project actually is. Drift is only a problem if it *costs*
something, so cost it out by direction:

| Drift direction | What the user experiences | Severity |
|---|---|---|
| client **stricter** than server | can't submit something the server would have accepted | annoying, discoverable |
| client **laxer** than server | submits, server rejects, message lands on the field | **none** — the server error path handles it |

So client rules are a **latency optimisation, not an authority**. Lax drift is self-healing the moment
server field errors render correctly on fields — which forever-pin proved out on 2026-07-28 (`P1`).

**That means the valuable target is not shared rules. It is shared *messages* and shared *paths*.**
A user who sees "Name is required" from the client and "Name must not be empty" from the server is hearing
two voices for one rule. That is the drift that shows.

### Therefore — scope this vector as three separable pieces

1. **Path contract (done, promote it).** Server emits a domain member path; the client camelCases and maps;
   unmapped paths render at form level. Already the SDK's `resolveSubmitFailure` / `defaultMapFieldPath`
   contract and now a convention rule. **Nothing to build — document and enforce.**
2. **Message catalogue.** One source of user-facing validation strings, keyed by rule code
   (`NotEmptyValidator`, `MaximumLengthValidator`, …) + member. Server sends the code; the client renders
   from the catalogue, or falls back to the server's message. Kills the two-voices problem without sharing
   a single rule. **Highest value per unit of work.**
3. **Rule extraction (the actual dream, and the hard part).** Generate client-side rules from the
   FluentValidation definitions.
   - precedent exists: `IValidatorDescriptor` reflects a validator's rules, and `FluentValidation.AspNetCore`
     already generated client rules for jQuery unobtrusive validation.
   - the ceiling is low: only simple rules survive extraction — required, length, regex, range, comparison.
   - anything conditional (`When`), cross-field, subtype-dispatched (`SetInheritanceValidator`), or
     whole-set (`CodeRuleSetValidator`) does not survive. forever-pin's validators are mostly these.
   - so extraction covers the *cheap* rules, which are exactly the rules that were never worth sharing.
   - the honest alternative: define rules in a neutral declarative format and generate **both** sides.
     Real single-source, real cost, and it means neither FluentValidation nor zod is the author any more.

### Prior art

- `conventions/development/backend/foundation/validation.md` — § *Layer independence*, § *Phases*, § *Map to HTTP*
- `forever-pin/engineering/planning/validation.md` — § *Presentation validation* (P1 measured, P7 the path rule)
- `forever-pin/engineering/research/error-ordering/error-ordering.md` — the cited status-code / ordering pass
- SDK: `forms-engine/SubmitErrors` (`resolveSubmitFailure`, `defaultMapFieldPath`), `foundation/http/FieldErrors`
