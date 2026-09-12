# Vue browser capabilities and packaging resolution

*Last updated: 2026-09-10*

## Scope

Paths below are relative to the Vue package. This report records parent-owned changes; full integrated
release checks are separate from these targeted results. React remains parked.

## Browser outcomes and lifecycle

Completed clipboard writes/reads, native share/share-or-copy, media capture, notifications, fullscreen,
orientation, wake-lock acquisition, one-shot geolocation/watch readings, speech completion and one-shot
workers use the shared `Result<TSuccess, TFailure>` carrier. Success payloads live in `value`; expected
failure categories and diagnostics live in `failure`. Reactive controls retain their state vocabulary.
Speech recognition callbacks and browser permission-state protocols are not mislabeled as completed operations.

The migration intentionally changes public APIs. Examples:
- `copyText`: `result.ok`, with void success.
- `readText`: successful `value` is the string, including an empty string.
- `requestMediaStream`: successful `value` is the acquired MediaStream.
- `shareOrCopy`: successful `value` is `shared` or `copied`; dismissal remains a failure category and never starts copying.
- `getCurrentPosition`: successful `value` is the position; watch callbacks receive the same carrier.
- `notify`: successful `value` is the Notification handle.
- Fullscreen/orientation failures retain ambiguous TypeError diagnostics rather than claiming every TypeError proves lost activation.

Resource fixes:
- Media capture generations stop superseded or post-stop streams and return cancelled failures to their callers.
- Clipboard reset invalidates a pending completion; older operations cannot reset or overwrite newer state.
- Share controls retain the pending state across overlapping operations and preserve explicit reset.
- Disposed geolocation controls ignore late readings; stopped watch callbacks do not publish.
- Speech cancellation settles SDK promises without waiting for a native end/error event.
- One-shot worker posting failures clear timeout timers, terminate workers and revoke object URLs.

Browser support comments now use method detection rather than the false claim that Firefox cannot read
clipboard text. [MDN readText](https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/readText) and
[read](https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/read) document current support.
Capability detection still does not prove permission or activation.

## Locale

`LocaleProvider` and provider-free consumers default deterministically to `en-US`.
Applications pass the same request locale on server/client and explicitly apply browser preferences after
hydration. Locale/message replacement remains reactive and separate app roots do not share provider state.

## Packaging and release configuration

- Vite derives JavaScript entries from the manifest and rejects missing declared sources.
- Retired format/sync/undo/validation subpaths became formatters/channels/history/validators.
- The utility capability split adds styles/dom/optionals; the old utils entry and root namespace are removed.
- Public type checks use the actual packed package and strict Bundler resolution with skipLibCheck disabled.
- Eight public root-ref types use the explicit ComponentElement contract instead of leaking inferred private Vue types.
- Toolbar and SpeedDial compound statics have explicit public types.
- Tailwind Variants 3.3.1 and Vue Query 5.102.8 fix incompatible generated consumer declarations.
- query/testing declares its optional test-utils peer.
- styles.css declares its Tailwind build peer and registers its own package source directory.
- Release CI validates source, bumps the version, builds and verifies the exact tarball that it publishes.
- The package README reflects Vue-specific entries, optional peers, styles and verification scope.

`scripts/check-package.mjs` packs and extracts the real package, checks all exports/assets, verifies core imports
without optional peers, checks each optional entry with its declared peers, and compiles public declarations.
`--install` adds an actual fresh npm installation. `--output` preserves the verified artifact and prints integrity.
Final review moved that installation to a separate temporary root: the original nested fixture could resolve
missing dependencies through an ancestor's workspace links. Earlier install passes therefore do not establish
complete isolation; the corrected separate-root install must pass before release.
The gate also builds a production consumer from packed JavaScript and the packed stylesheet, asserting SDK-only
utility classes, semantic variables and forced-colors CSS. The old packed stylesheet fails this check with
`Packed consumer CSS omits SDK styling: .h-9`; copying the corrected stylesheet through the normal build copy
step passes. This controlled stylesheet check used the last successful JavaScript build; final source still
requires a fresh combined build. Tailwind's [source detection rules](https://tailwindcss.com/docs/detecting-classes-in-source-files)
exclude node_modules unless explicitly registered.

## Targeted evidence

Before current Result/naming/folder migrations: typecheck/SFC, lint, formatting, build, 60 test files / 1,345
tests, isolated packed consumers and a fresh npm tarball installation passed. Those counts are historical.

Current parent regression run: `vitest --project unit --project dom tests/unit/foundation/browser
tests/unit/foundation/i18n` passes 3 files / 16 tests, including the moved collator test.
This covers browser capability absence, failure categories, share dismissal/fallback, media races,
clipboard/share reset, speech cancellation, worker cleanup, geolocation disposal, provider replacement,
independent roots and deterministic SSR hydration.

Integrated checkpoint: 73 Node/DOM/SSR files / 1,415 tests and compilation of 407 SFCs passed. Packed checks
passed 70 export targets / 62 core JavaScript entries / 66 total JavaScript entries, with strict public types.
Later component/query/date-codec changes require the final combined gates again.

Final combined source, browser, build and packed-consumer checks must run after every lane finishes.
No commit, registry publication or release workflow execution occurred.
