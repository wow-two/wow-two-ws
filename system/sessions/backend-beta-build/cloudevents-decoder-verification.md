# CloudEvents decoder correctness verification

*Verified: 2026-09-15*

## Result

Reopened sweep item N91 is resolved for the CloudEvents decoding failure contract. Malformed JSON, invalid base64 and non-string `data_base64` return `Result<object>` failures with `AppErrorType.SerializationFailed`. A valid early payload no longer hides malformed remaining JSON or trailing content.

The decoder still extracts payload data only. Required CloudEvents context attributes are not semantically validated; inbound metadata is discarded. Null `bodyType` remains a programmer error and throws `ArgumentNullException`.

## Changes

SDK root: `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta`.

All `src/` paths below are relative to its `engineering/codebase/wow-two-back-beta-sdk/` directory.

| File | Change |
|---|---|
| `src/Messaging/Serialization/Serializers/CloudEventsMessageSerializer.cs:83` | Parses the complete JSON value into a disposed `JsonDocument`, checks the reader for trailing input, then decodes the first `data` or `data_base64` property in document order. Rejects a non-object document and non-string base64 payload. Catches JSON and format errors at the decoding boundary. |
| `src/Messaging.Tests/MessageSerializerTests.cs:229` | Added 15 regression cases for document completeness, decoding failure, retained payload-only semantics and the programmer guard. |
| `src/Messaging/Serialization/serialization.md:98` | Replaced stale `object?`/null/malformed-throws claims with the current result contract and documented CloudEvents full-document syntax validation without context-attribute validation. |

Serialization output, JSON options, metadata generation, raw-byte base64 handling and first-recognized-payload selection remain unchanged. The implementation materializes a JSON document to validate the entire input before decoding; no performance benchmark was run.

## Regression coverage

- Six malformed-document cases: incomplete JSON, missing outer closing brace after valid data, malformed extensions after `data` or `data_base64`, a second document and trailing non-JSON text.
- Seven undecodable-data cases: invalid base64, numeric/boolean/array/object `data_base64`, base64 containing malformed JSON, and data incompatible with the requested property type.
- One valid payload-only document without required CloudEvents attributes, including a nested extension.
- One null-target-type programmer guard.

Full-document fixtures target `Dictionary<string, string>` so their early payload is genuinely decodable; missing required members in a richer test DTO cannot mask the original early-return defect.

## Validation

Commands ran serially from SDK `engineering/codebase/wow-two-back-beta-sdk/src/`.

```sh
dotnet build Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-restore -m:1 -v:q
dotnet test Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-build --no-restore --filter 'FullyQualifiedName~MessageSerializerTests' -v:minimal
```

- Final build: exit 0; 158 warnings, 0 errors. Log: `/tmp/cloudevents-decoder-build.log`.
- Serializer suite: exit 0; 37 passed, 0 failed, 0 skipped; .NET 10. Includes the 15 new cases and existing three-serializer round trips, emitted CloudEvents attributes and base64 interoperability cases.
- Native `require_escalated` execution supplied the VSTest local socket permission established as necessary in the tracker test run. The command returned its completed passing outcome; no approval remains pending.
- Scoped `git diff --check` passed for the serializer, test file and guide.

## Limits

- This is decoder syntax/failure-contract verification, not full CloudEvents semantic compliance.
- No transport/broker integration, full solution test suite, CI run or release was performed.
- Existing build warnings remain outside this task.
- No staging, commit or push occurred.
