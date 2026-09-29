# Vue SDK release — September 26

## Status

- [x] Verified the owner pushed `cbadbd416a662659908956b706a9219e3660ef0f` to GitHub `main`.
- [x] Followed [release run 36187325851](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.ui/actions/runs/36187325851) to its failed test gate.
- [x] Reproduced the Firefox failure locally under Linux with the complete test suite.
- [x] Corrected the iframe fixture; all 2,101 Linux tests across 172 files pass.
- [x] Committed the one-file correction as `8a80db88cdf97ad8392bc6b8b3f490eea416e750`; restored all 39 staged paths.
- [x] Owner pushed `8a80db88cdf97ad8392bc6b8b3f490eea416e750`; matching release run started.
- [x] New CI run passed all gates and npm accepted `0.0.7` for processing.
- [x] Verified the release tag and bot commit against the tested source.
- [x] Verified public npm metadata, tarball integrity and every export target after processing finished.

[Run 36189754639](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.ui/actions/runs/36189754639)
completed successfully at `2026-09-25T21:11:55Z` for source `8a80db88cdf97ad8392bc6b8b3f490eea416e750`.
Typecheck, lint, format, all 2,101 tests across 172 files, library/playground builds, playground browser
smoke and packed-consumer installation passed. The packed gate verified 72 exports, 64 entries without
optional peers and all 68 entries with adapters.

`Lint` is the workflow step label for `pnpm lint`, which runs `eslint .`. It is not a deployment
environment; this workflow declares no `environment:`. The runner is `ubuntu-latest`.

## Release evidence

- npm accepted `@wow-two-beta/ui-vue@0.0.7` at `2026-09-25T21:11:48Z` using the public npm registry and `latest` tag.
- npm explicitly reported: “Your package is being processed and may take a few minutes to become available.”
- CI tarball: 1,609 files; SHA-1 `58f11a0949c189c10de747e6c6962f6f577b28f5`.
- Signed provenance was submitted to [Sigstore](https://search.sigstore.dev/?logIndex=2961853880).
- [GitHub release `ui-vue-v0.0.7`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.ui/releases/tag/ui-vue-v0.0.7)
  was published at `2026-09-25T21:11:50Z`.
- The tag and remote main resolve to `3295e9f1173063f0f50d45de4732bf3a819b918d`.
- Its sole parent is tested source `8a80db88cdf97ad8392bc6b8b3f490eea416e750`; its only change is the Vue manifest version `0.0.6` → `0.0.7`.
- Public npm reports `latest=0.0.7`, published at `2026-09-25T21:19:58.919Z`;
  independently verified at `2026-09-25T21:55:54.998Z`.
- The 2,202,209-byte downloaded tarball matches registry SHA-1/SHA-512 and the CI SHA-1 above.
  Its manifest matches registry metadata; all 140 unique targets from 72 export mappings exist among 1,609 files.
- The provenance payload's subject digest matches that tarball and identifies source `8a80db8`,
  `release-vue.yml` and run `36189754639/attempts/1`. Envelope signatures were not independently
  cryptographically validated by this inspection.
- [Public artifact verification](/private/tmp/ui-vue-0.0.7-verification.json) records exact hashes and provenance fields.

Evidence: [successful CI log](/private/tmp/vue-release-36189754639-success.log).
This task did not pull the shared checkout over another task's staged manifest. Subsequent manifest changes
belong to concurrent work; the remote release and downloaded tarball establish the published state.

## Previous hosted result

Typecheck, lint and format passed. Tests returned 2,100 passing cases and one failure:
`FocusScope.browser.test.ts`, “isolates and restores focus in the owning iframe document”, Firefox only.
The final assertion expected the opener button but received the iframe body. Chromium, forced-colors
Chromium and WebKit passed this case. Publishing did not run in that earlier attempt.

Evidence: [failed CI log](/private/tmp/vue-release-36187325851-failed.log).

## Diagnosis and correction

The test appended a fresh iframe and immediately focused its opener without checking whether that focus
succeeded. The isolated original passed locally, but running the complete Linux suite reproduced the
exact CI failure. An explicit pre-mount assertion then failed before `FocusScope` existed: the iframe's
browsing context had not received focus. This distinguishes fixture setup from component teardown.

The fixture now:

1. Creates an explicit `srcdoc` document and awaits its load event, registered before insertion.
2. Activates the iframe with `contentWindow.focus()` before focusing the opener.
3. Asserts that the opener is active before mounting `FocusScope`.
4. Retains all existing inert, autofocus, parent-frame-isolation and exact return-focus assertions.

Only `engineering/codebase/wow-two-front-vue-beta-sdk/tests/unit/foundation/primitives/FocusScope.browser.test.ts`
changes. Product code and teardown assertions are unchanged. An independent review found no objection;
fixture activation happens exclusively before mounting and cannot assist the restoration assertion.

## Verification

- Frozen-lockfile installation in the isolated committed SDK snapshot.
- Playwright `1.62.1`, matching the lockfile, using `mcr.microsoft.com/playwright:v1.62.1-noble`.
- Original full Linux suite: 1 failed / 2,100 passed, reproducing the hosted Firefox failure.
- Load-only correction: full-suite failure moved to the added pre-mount focus assertion.
- Final correction: 2,101 passed / 172 files, including Chromium, forced-colors, Firefox and WebKit.
- Targeted ESLint, Prettier and whitespace checks pass.
- [Final complete Linux log](/private/tmp/vue-focus-linux-fixed.log).
- [Original and intermediate diagnostic log](/private/tmp/vue-focus-linux-full.log).
- Reproduction scripts and original snapshot: `/private/tmp/vue-focus-ci-36187325851/`.

The Mac-native Firefox attempt timed out without executing tests. Its identified processes were stopped;
Linux Docker tests provide the browser evidence. Containers removed themselves on completion. No browser
security setting or host sandbox configuration was weakened. No source build or artifact change is claimed.

## Commit coordination

The owner explicitly approved temporary isolation of the 39 staged Ocharo React/Vue paths. SDK ordinary-commit
permission was ON for this task. The single reviewed test file was committed, and all 39 exact staged blobs
and modes were restored. Remaining unstaged tracked work matches the pre-operation snapshot.

Commit: `8a80db88cdf97ad8392bc6b8b3f490eea416e750`.
Subject: `test: awaited iframe readiness before focus restoration checks`.
Both author and committer use `Sultonbek Rakhimov <sultonbek.rakhimov@gmail.com>`; GPG verification reports
a good signature. Native escalation preserved configured signing after the sandbox blocked GPG access.

Committed blob `e51956a3d490977ef4a7026bcb6621988032f69f` matches the exact fixture used by the complete
Linux verification. Only that test path changed in the commit. Index snapshot, backup patch and verification:
`/private/tmp/vue-focus-commit-20260926/`.

The owner pushed the correction. The resulting hosted workflow, release commit and tag are verified above.
