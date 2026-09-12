# Lossless numeric JSON prototype

*Completed: 2026-09-12; source held for aggregate package verification.*

## Authorized scope

The user selected lossless JSON exploration. This lane implemented new Vue SDK foundation/numbers and foundation/json capabilities, their tests and adjacent API specifications. Parent owns dependencies, public package exports, HTTP opt-in integration and convention amendments. React is untouched. No package publication or source staging was performed by this lane.

## Result

`ExactNumber` is an SDK-owned immutable finite-decimal value exposed as a frozen interface/factory pair, with actual-instance narrowing. Parsed values retain their original JSON numeric token, including exponent spelling, decimal scale and negative zero. Every supported arithmetic operation returns a house Result when an expected failure is actionable.

Exact addition, subtraction, multiplication and truncating remainder use bignumber.js 11.1.5 through a private adapter. Division and rounding require explicit decimal-place precision and a named rounding mode. Comparison returns a Result using normalized exponent order and lexicographic coefficient comparison with virtual trailing zeros; it handles every accepted magnitude without decimal expansion. The public declaration surface carries no vendor instance/type. The arithmetic constructor is isolated from consumer configuration, and per-operation precision does not leak into later calls.

`LosslessJson` uses lossless-json 4.3.1 through a private adapter and custom numeric parser/stringifier. Every JSON numeric token, including a small integer, becomes ExactNumber. Objects restore as null-prototype records. Numeric-looking/date-looking strings remain strings. Native safe integers and bigint can be encoded directly; decimals use an explicit ExactNumber value. Native decimal/unsafe-number values fail instead of guessing their intended decimal representation.

Public source entries:

- `src/foundation/numbers/index.ts`: ExactNumber, NumberLimits, NumberFailureCode, NumberRounding, NumberFailure, NumberRoundingOptions.
- `src/foundation/json/index.ts`: LosslessJson, JsonFailureCode, JsonLimits, JsonFailure, LosslessJsonValue.
- Adjacent contracts: `numbers/ExactNumber.spec.md`, `json/LosslessJson.spec.md`.

## Numeric semantics

- Input accepts the complete finite JSON numeric form within a 16,384-character token budget excluding the optional leading minus. Token parsing does not restrict exponent magnitude to Number, int64, .NET decimal or arithmetic-engine range.
- Arithmetic has an explicit 32,768-place working interval/coefficient budget and output token budget. Division/rounding accept 0–4,096 decimal places. Resource failures do not silently round or clamp inputs.
- Arithmetic emits canonical tokens and normalizes a zero result to `0`. Parsing and sign operations retain zero sign/spelling; numeric equality ignores zero sign and lexical scale.
- `toBigInt` is exact for integral values within the work budget. `toSafeInteger` is exact within ±9007199254740991. `toApproximateNumber` is explicitly approximate and rejects overflow/nonzero underflow. No decimal-text roundtrip is misrepresented as binary64 exactness.
- Implicit default/numeric coercion and native JSON.stringify throw TypeError; use explicit methods and LosslessJson. String interpolation is supported. Native `===` remains identity comparison.
- Exact scope is finite decimal add/subtract/multiply/remainder, explicit rounded divide/round, and comparison; no transcendental or unlimited-resource claim.

## Parser/serializer containment

The upstream parser writes ordinary object properties and only invokes duplicate callbacks for unequal duplicate values. The wrapper therefore performs a bounded lexical key pass before vendor parsing: all object keys become temporary safe keys; every duplicate decoded key fails, including equal values and escaped-key equivalents. A following pass restores original keys into null-prototype records. Prototype and vendor-special names remain ordinary data; no key is silently dropped.

Serialization likewise encodes keys before the vendor serializer and restores them afterward. This prevents `toJSON`, `isLosslessNumber` and prototype-named user fields from being treated as vendor instructions. It accepts only supported data shapes, does not invoke getters/conversion hooks, rejects cycles/accessors/sparse arrays/enumerable symbols/custom instances and preserves programmer errors from Proxy traps.

The in-memory codec has 1,048,576 UTF-16-character, 128-container-depth and 100,000-token/traversal budgets. Array size is checked before index-array allocation. String/key escaped lengths are counted incrementally before serialization allocation. The encoder uses a conservative budget that includes keys/punctuation and temporary encoded-key text. These checks do not claim a hard real-time guarantee or executable-object sandbox.

## Evidence

Final focused command:

```sh
pnpm exec vitest run --project unit tests/unit/foundation/numbers tests/unit/foundation/json tests/unit/foundation/http
```

Result: **109 tests across four files passed** (`/private/tmp/vue-lossless-final-tests.log`), comprising 88 numeric/JSON tests and 21 HTTP tests. Strict Vue typechecking (`/private/tmp/vue-lossless-final-types.log`), scoped ESLint (`/private/tmp/vue-lossless-lint.log`) and scoped Prettier passed.

The numeric suite independently computes expected signed/scaled sums, differences, products, truncating remainders and ordering with native BigInt over 294 combinations of signs/scales/large coefficients. It does not merely compare the wrapper with its vendor implementation. It also verifies cancellation, every rounding tie mode for both signs, repeating division, zero, conversion boundaries, native-operator rejection, vendor configuration isolation, sign-aware maximum token roundtrips and resource failures. Twelve additional cases cover huge signed exponents, lexical equality, zero and equal-order coefficient padding without expanding the value.

The JSON suite consumes actual default System.Text.Json output generated under .NET SDK 10.0.300 by the parent lane. The byte-preserved fixture and generator source live in `tests/unit/foundation/json/fixtures/`; the `.json.txt` suffix protects decimal scale from code formatters. It contains both long/decimal endpoints, the unsafe-native integer 9007199254740993, 28-place fractions, scaled 123.4500 and decimal arithmetic. The fixture byte SHA-256 is `8ebb827f57181d537438d8a7f52226d04a69f091526af6bc03b7fb6a479b8c7e`.

Additional JSON tests cover malformed grammar/escapes, nested arrays, huge exponents, negative zero, prototype keys, duplicate equality/escaping, serialization rejection and allocation guards. Parent/domain integration tests verify HTTP request/response numeric preservation and protocol-failure mapping. Aggregate build, declarations, packed consumers, browser checks and publication remain parent-owned.

## Primary dependency evidence

- [bignumber.js API](https://mikemcl.github.io/bignumber.js/): decimal operations, isolated constructors and explicit rounding configuration supported the arithmetic choice.
- [bignumber.js manifest](https://github.com/MikeMcl/bignumber.js/blob/main/package.json): upstream version and module/type entries; parent installed the pinned 11.1.5 dependency.
- [lossless-json API](https://github.com/josdejong/lossless-json/blob/main/README.md): custom numeric parser/stringifier hooks support an SDK-owned numeric type.
- [lossless-json parser](https://github.com/josdejong/lossless-json/blob/main/src/parse.ts) and [serializer](https://github.com/josdejong/lossless-json/blob/main/src/stringify.ts): source inspection identified the key/duplicate and special-property behaviors contained by the wrapper.

No new product-level choice remains in this lane. Exact domain field ranges and any future replacement of the existing default HTTP JSON codec remain separate contracts; the requested lossless codec is explicit opt-in.

## Integrated verification — 2026-09-12

The parent verified the combined implementation, including HTTP and both form adapters:

| Gate | Result |
|---|---|
| Node/DOM/SSR suite | 93 files / 1,634 tests pass |
| Chromium ordinary/forced colors | Six project files / 30 tests pass |
| Strict source/test types and SFC compilation | Pass; 407 SFCs |
| Capability graph | 58 nodes / 1,032 references; no cycles or unresolved paths |
| Full lint and source/test format | Pass |
| Library/declarations and playground production build | Pass |
| Actual packed consumer | 72 targets; 64 core JS entries without optional peers, 68 with adapters |
| Packed numeric behavior | Exact arithmetic and bare numeric JSON round trip pass from the tarball |
| Independent fresh npm installation | Pass with normal peer resolution and no workspace links |
| Frozen lockfile verification | Pass |
| Registry version | `0.0.5`, verified; this prototype remains unpublished |

Logs: `/private/tmp/lossless-final-{tests,types,lint,format,build,playground,package}.log`,
`/private/tmp/lossless-browser.log`, `/private/tmp/lossless-lockfile.log` and `/private/tmp/lossless-registry.log`.
The final null-safe assertion in the JSON test file was verified again by strict typechecking and its
33-test JSON suite; it did not change runtime source.

The HTTP codec runs before native numeric parsing and also encodes outgoing payloads. Raw problem
diagnostics keep their codec representation while transport status remains a native HTTP status.
Form snapshots retain authentic immutable ExactNumber leaves; dirty comparisons use numeric equality,
including values with different textual scales. Both adapters have mounted submission/reset coverage.

## Capability boundaries

| Capability | Disposition |
|---|---|
| Exact values, basic arithmetic, comparison and rounding | Implemented and tested |
| JSON parser/serializer, HTTP codec and form-value preservation | Implemented and tested |
| Global HTTP-client adoption | Deferred until the prototype's API/behavior is accepted; explicit opt-in is available |
| Exact-number inputs, locale formatting and built-in schema adapters | Follow-up after prototype acceptance; current native-number controls do not change implicitly |
| Powers, roots, transcendental or symbolic/rational arithmetic | Outside this finite-decimal prototype; no correctness claim |
| Backend numeric serialization change | Unnecessary for this experiment: ordinary numeric JSON tokens are preserved |

The tested .NET fixture proves interoperability with default System.Text.Json numeric output, not a
live deployment of the backend SDK. No source was committed and no version was published in this amendment.
