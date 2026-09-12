# Delivery

*Last updated: 2026-09-10*

> Release validation and publishing handoff for a .NET SDK family.

## Contract

- must keep the concrete release procedure, project list and version source in the SDK repository.
- must derive the artifact set from the current project metadata and publishing workflow.
- must keep package family versions aligned when the workflow releases them together.
- must declare package identity, license, repository/source metadata and documentation assets in package properties.
- must include `PackageReadmeFile` only when its packed file exists.
- must preserve a functional package README even when it sits below the repository root.
- must apply the [Git publishing policy](../../../../../repo/version-control/git.md); agents prepare, the developer publishes.

---

## Release cut

- must complete the [build checks](../build/build.md) and [test checks](../testing/testing.md).
- must record the exact revision, evaluated candidate version, required checks and artifact list.
- must distinguish a local package version from a version the workflow increments before packing.
- must not call a local pack proof that a later workflow-built artifact was tested.
- must put required release tests in the publishing path or provide matching revision/version evidence before publishing.
- must verify the expected package versions and tags after publishing.
- must identify consumers needing a re-pin without making unused product migrations block an SDK correction.

---

## Backend beta

- must read its current `publish.yml` and `Directory.Build.props` before calculating a release candidate.
- must preserve workflow ownership of the version bump unless the release procedure is explicitly changed.
- must validate every project the workflow packs, including runtime, contracts, CLI and shipped testing libraries.
- must not infer consumer compatibility requirements from a beta label; follow the SDK owner's declared support boundary.

Current procedure: [publishing workflow](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/.github/workflows/publish.yml).
