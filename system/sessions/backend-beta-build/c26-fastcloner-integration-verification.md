# C26 FastCloner integration verification

*Verified: 2026-09-16*

## Result

C26 is complete. `FastCloner` 3.5.6 is a direct SDK dependency and remains directly callable as
`FastCloner.FastCloner.DeepClone`. The SDK adds no wrapper whose name or behavior could hide the package contract.

## Contract

- Use deep cloning for owned, detached in-memory data graphs.
- Preserve runtime types, private/init/get-only state, cycles and shared aliases.
- Preserve collection comparers and rebuild collection hashes around cloned keys.
- Keep copied entity IDs; treat the copy as a detached candidate or snapshot.
- Exclude streams, native handles, callbacks, EF contexts and EF proxies.
- Validate a copied candidate at its accepting boundary; cloning is not validation.
- Make no NativeAOT or generated-code claim for the reflection implementation.

## Verification

- NuGet assets resolved exact package `FastCloner/3.5.6` for the SDK and Foundation tests.
- Foundation.Tests built successfully.
- Foundation.Tests passed 123 of 123 tests on .NET 10.
- Four SDK contract tests cover runtime shape, aliases, cycles, isolation, collection comparers,
  reference keys, record keys with reference members and preserved entity identity.
