# C17 release pipeline verification

*Last updated: 2026-09-16*

## Result

- `publish.yml` creates the workflow-owned version commit and tag before validation.
- restore, full release build and all test projects run before packing or authentication.
- package metadata receives that exact release revision.
- seven NuGets and seven symbol packages are verified before publication.
- the verified packages and `release-manifest.txt` are retained as one workflow artifact.
- the workflow pushes the tested commit/tag only after NuGet publication succeeds.
- the final step verifies the remote tag and all seven versions on NuGet.

## Package verification

`scripts/verify-release-packages.sh` verifies:

- exact package IDs and shared version;
- expected library or tool assets;
- MIT license and repository revision metadata;
- the production package README;
- aligned family dependencies and the CLI's embedded data-abstractions assembly;
- no test-only dependency in production packages;
- no production-mono-library dependency in the base Testing package.

## Local evidence

- source `HEAD`: `4abb2c8c5d2be8d967eae580e0f416802490b3b1`;
- evaluated local version: `10.0.55-beta`;
- release build: zero errors;
- release tests: 402 passed, one Kafka integration test skipped;
- local package verification: seven `.nupkg` and seven `.snupkg` passed.

The working tree contains the sweep, so this local pack proves the package verifier against the
current content but is not a publish candidate. The real candidate revision and incremented version
are created, tested and recorded by the workflow after the developer commits and pushes the sweep.
