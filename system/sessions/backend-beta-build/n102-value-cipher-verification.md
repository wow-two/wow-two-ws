# N102 value cipher verification

*Verified: 2026-09-16*

## Result

N102 is complete in the SDK. The public seam is `IValueCipher`; its default implementation is `ValueCipher`,
which delegates AES-256-GCM work to `AesGcmCipher`.

## Verification

- SDK source and security documentation contain no `ICryptoCore` or `CryptoCore` references.
- `AddEnvelopeCryptography` registers `IValueCipher` as a singleton.
- Foundation.Tests passed 123 of 123 tests.
- The registration test resolves `IValueCipher` from a bare configured container.

## Consumer adoption

SecretsVault still references `ICryptoCore` in two handlers, tests and documentation. Those edits depend on the
published sweep package and remain in the direct-consumer repin pass.
