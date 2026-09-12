# Delivery

*Last updated: 2026-09-10*

> The published library artifact, its dependency boundary and release evidence.

## Exports

- must declare every supported public entry in `package.json` exports with matching runtime and type targets.
- must build every declared entry; fail when an export source or generated target is absent.
- must exclude private source paths from public import contracts.
- must use relative imports in shipping source unless the declaration build rewrites source aliases.
- must leave no private source alias in published declarations.
- must reserve `@src` for tests by default; test aliases do not establish a public package path.
- must declare ESM/CommonJS support explicitly and test each advertised condition.
- must keep framework packages external and list the supported ranges as peers.
- must follow the central [package boundary](../../../../repo/structure/sdk-structure.md#publish) for tarball contents.

---

## Dependencies

- must declare optional vendor peers in package-level `peerDependencies` and `peerDependenciesMeta`.
- must isolate each vendor's runtime imports to its adapter subpath and reachable chunks.
- must let the contract and unrelated adapters build/import without that optional vendor installed.
- must make the selected adapter's missing peer fail with a clear dependency error.
- must not re-export all adapters from the vendor-free root.
- must verify bundle graphs after splitting or moving capabilities; source separation alone is insufficient.
- must state each subpath's [runtime support](../platform/compatibility.md#support-matrix).

---

## Styles

- must export the stylesheet and document whether it supplies tokens, utilities or both.
- must retain required CSS through an accurate `sideEffects` declaration; do not mark required styles removable.
- must avoid importing application styles or changing document theme at module evaluation.
- must document the source-scanning contract when consumers generate utilities from package output.
- must verify an isolated consuming app renders representative components with shipped assets only.
- must keep app token overrides under [app styling](../../app/platform/styling.md).

---

## Artifact

- must build from the intended lockfile with the declared package manager/runtime versions.
- must pack the built package and enumerate every advertised export against the tarball.
- must install that tarball in a clean consumer, without repository aliases or workspace symlinks.
- must typecheck/import each advertised condition and smoke-test representative UI and CSS.
- must test a contract-only consumer with optional vendors absent and selected-adapter consumers with them present.
- must inspect the tarball for private fixtures, credentials, source-only infrastructure and unintended files.
- must record artifact identity, version, commands and results as release evidence.

---

## Publication

- must identify the release owner and the repository's version/tag workflow before publishing.
- must verify the intended package version against the registry; never overwrite an immutable published version.
- must preserve repo-specific beta version policy; breaking changes still need a consumer migration record.
- must publish the exact verified artifact and verify registry version, integrity and installability afterward.
- must record partial publication before retrying; retry only missing artifacts/tags and do not republish an existing version.
- must use a new version for a corrected artifact after publication.
- must follow the workspace Git policy separately from package publication authorization.
