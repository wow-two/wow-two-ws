# C27 value-object equality verification

*Verified: 2026-09-16*

## Result

C27 is complete by source inventory. The SDK declares no `*ValueObject`, so it has no value-object equality contract
whose collection semantics require custom typed equality or hashing.

## Evidence

- no production C# declaration or reference uses the `ValueObject` suffix
- collection-bearing records are DTOs, options, results or mutable operational state
- GeoJSON geometry, feature and caption records describe transport/model shapes rather than values stored inside an entity row
- entity equality and hashing remain unchanged

## Boundary

The convention remains active for future `*ValueObject` declarations. A future value object with collection identity
must define order and duplicate semantics, implement matching equality and hashing when generated equality is wrong,
and verify equal separate instances plus stable hash behavior.
