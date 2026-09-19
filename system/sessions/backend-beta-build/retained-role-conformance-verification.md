# Retained-role conformance verification

*Last updated: 2026-09-15*

## Scope

Retained all 11 approved type names and method APIs; moved declarations into the required role folders with matching namespaces.

| Family | Declarations | Placement under SDK `src/` |
|---|---|---|
| Exporter | `CsvTabularExporter` | `Media/Csv/Exporters/` |
| Exporter | `ExcelTabularExporter` | `Media/Excel/Exporters/` |
| Exporter | `ITabularExporter` | `Media/Tabular/Exporters/` |
| Serializer | `IGeoJsonSerializer`, `GeoJsonSerializer` | `Geo/GeoJson/Serializers/` |
| Serializer | `IMessageSerializer`, `SystemTextJsonMessageSerializer`, `MessagePackMessageSerializer`, `CloudEventsMessageSerializer` | `Messaging/Serialization/Serializers/` |
| Bus | `IEventBus`, `TransportEventBus` | `Messaging/Buses/` |

- Concrete summaries now start with `Exports`, `Serializes` or `Dispatches`; interfaces start with `Defines`.
- Updated exact source/DI/test imports and owning feature guides. Registration extensions and options stay in their owning domains.
- Corrected the GeoJSON guide's obsolete static calls and positional construction to the existing instance API/body-property shape.
- Corrected the serializer test summary's obsolete null-result wording to the actual failure result.
- Replaced the bus interface's blanket at-least-once claim with its application-facing publish/send responsibility;
  completion follows the underlying send transport and does not itself establish durability or completed handler execution.
- Preserved serialization formats/options, content-type tokens, result behavior, exporter implementation, delivery metadata,
  DI overrides/lifetimes and method APIs. No per-type stored-JSON wrappers introduced.
- No Parser refactoring or Transport-role restructuring; transport callers changed only as needed for the moved types.
- No new tests, package changes, staging, commits or pushes.

---

## Checks

- `dotnet build Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-restore -m:1`, from SDK `src/`:
  exit 0, 170 warnings, 0 errors. This compiles the core exporters/GeoJSON/serializers/bus and affected messaging helpers/tests.
  Log: `/private/tmp/retained-role-build.log`.
- `dotnet test Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-build --no-restore --filter 'FullyQualifiedName~MessageSerializerTests|FullyQualifiedName~MessagePumpTests'`:
  exit 0, 26 passed, 0 failed, 0 skipped. Native permission granted and actual execution completed in session `34345`.
- SDK `git diff --check` passed; old declaration-path search and new-folder namespace check found no stale targets.
- Existing tests cover the three message serialization formats, content types, supported round trips, selected failures,
  and in-memory publishing/consuming through the default bus. No direct exporter or GeoJSON tests were found.

---

## Explicit follow-ups: behavior preserved in this slice

Paths below are relative to SDK `src/`; findings come from source inspection, not new runtime tests.

1. **CloudEvents malformed-input contract:** `Messaging/Serialization/Serializers/CloudEventsMessageSerializer.cs:82`
   parses JSON/base64 without an exception-to-failure boundary. Parsing exceptions can escape despite
   `IMessageSerializer.Deserialize` promising failure results for undecodable input. The existing tests do not cover these malformed cases.
2. **CloudEvents complete-document acceptance:** the same method returns immediately after decoding `data` or `data_base64`
   (`:105`, `:118`), so it does not validate the remaining envelope or required CloudEvents context attributes.
   Preserve the payload-only decoder boundary or strengthen validation explicitly; do not imply full CloudEvents validation today.
3. **GeoJSON reconstruction and acceptance:** `Geo/GeoJson/Serializers/GeoJsonSerializer.cs:196` converts a numeric feature ID
   to text, which serialization writes as a JSON string. Unsupported members are omitted, and `ParseFeatureCollection` (`:77`)
   returns an empty collection for missing/non-array `features`. Document the lossy supported subset and decide whether that permissive
   input behavior is intended; no full GeoJSON round-trip/validation guarantee is established.
4. **Exporter contract details:** `Media/Csv/Exporters/CsvTabularExporter.cs` delegates schema/header ordering to CsvHelper
   using invariant culture; `Media/Excel/Exporters/ExcelTabularExporter.cs` delegates table/schema production to ClosedXML.
   Exact column ordering, empty-input behavior, encoding where relevant, destination seeking requirements and partial-output behavior
   need a documented contract backed by the wrapped-library behavior. The interface says the destination remains open; Excel stream
   ownership should be verified before claiming that implementation complies.
5. **Excel cancellation and buffering:** `ExcelTabularExporter.cs:20` checks cancellation only before synchronous
   `InsertTable` / `SaveAs` (`:24–25`). The workbook is built in memory and those phases cannot observe subsequent cancellation.
   Document these limits or change implementation separately; this slice preserves them.

These checks do not establish live provider guarantees, full SDK conformance or release readiness.
