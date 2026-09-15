# Vue capability layout and operation carrier audit

*Last updated: 2026-09-10*

## Scope and owners

This follow-up applies [Library / Capability roles](../../../conventions/development/frontend/shapes/library/library.md#capability-roles) and [Results](../../../conventions/development/frontend/core/mla/constructs/data/result.md) to existing nonvisual capabilities. It does not add new capabilities beyond assigning existing shared state helpers to their semantic home. Presentation, forms, physical query/router adapter placement and visual foundation roots have separate implementation owners.

The inventory combines static declarations/import resolution with inspection of file contents. A folder holding one file and a barrel is not itself a violation: root capabilities, visual primitives and declared adapters can legitimately have that form. Factories and protocol seams stay flat; a provider protocol named `*Provider` is not automatically a Vue context-provider role.

## Completed placement

The former utility migration is recorded in [Vue results resolution](vue-results-resolution.md). The subsequent capability pass moves 90 additional physical files, then groups the two new state hooks, and adjusts 219 import/barrel files at the coordinated checkpoint. Counts describe the checkpoint, not later independent lane edits.

| Existing capability | Placement completed |
|---|---|
| channels | Three framework hooks grouped. Factory, transport contract and election engine remain flat. |
| clipboard | Three framework hooks grouped, including the retired shared-hook implementation. Operation/failure models extracted. |
| commands | Two framework hooks and context/provider pair grouped; command operation result/failure have their own model files. Registry and invocation contract remain flat. |
| device | Six framework hooks grouped; DisplayMode and PointerType closed-set files grouped. Platform detection and breakpoint factory remain flat. |
| dom | Four framework hooks grouped. Six enum files remain grouped; singleton data/extension roles stay flat. |
| geolocation | Coordinate and reading shapes grouped; operation/result failure files extracted. Mapping stays at the capability root. Two hooks grouped. |
| gestures | Four hooks and two enum files grouped; pure gesture calculations stay flat. |
| history | Two hooks grouped; independent history factories stay flat. |
| http | Four model files grouped; HTTP factory, envelope policy and failure classification remain flat. |
| i18n | LocaleContext and LocaleProvider grouped. FormattedRelative visual-root placement has a separate owner. |
| net | Three hooks grouped; socket/event-stream/polling factories stay flat. |
| notifications | Two hooks grouped; operation/failure models extracted. |
| observers | Five hooks grouped, including the existing resize observer implementation. Observer factories stay flat. |
| resilience | Two enum files grouped; retry policy and delay calculation stay flat. |
| screen | Three hooks grouped; operation/failure models extracted; two failure-code vocabularies grouped as enums. |
| selection | Four hooks grouped, including typeahead. Existing model group retained. |
| shortcuts | Escape and hotkey hooks grouped. Chord parsing stays flat. |
| speech | Two hooks grouped; operation/failure models extracted; two failure-code vocabularies grouped as enums. |
| state | Controlled value and disclosure are the two framework hooks; public `foundation/state` seam added. |
| storage | Autosave, persistent-state and recent-items hooks grouped. The Zustand structural adapter moved to `adapters/zustand`; public subpath unchanged. |
| auth | AuthContext and AuthProvider grouped; strategy/bridge/storage factories remain flat. |
| flags | FlagsContext and FlagsProvider grouped; resolver protocol and client/provider factories remain flat. |
| query/router | Existing framework hooks grouped; physical vendor-adapter placement subsequently belongs to the domain agent. |
| themes | `Css.ts`, `Generate.ts`, `Registry.ts`, `Validate.ts` use PascalCase filenames; `constants/Pool.ts` and `constants/Authored.ts` hold fixed catalogs. Theme shape is a singleton model; token seam and color engine remain flat. |

No additional homogeneous role group was established beyond existing groups and the Result extractions for these inspected capabilities: analytics, feedback, animation, async, collections, config, crypto, datetime, errors, files, formatters, idb, identifiers, logger, media, oauth, optionals, results, share, uploads, validators, virtualization and workers. Supporting types next to a factory do not turn the factory file into a model role. Result-specific own-file corrections apply independently below. `domain/color` and `domain/emoji` remain separate semantic domain capabilities.

`foundation/hooks` and its 17 one-file subfolders are retired completely. Its functions now live in state, dom, shortcuts, identifiers, device, observers, async, storage, selection and clipboard. Source names are PascalCase. No compatibility hooks bucket remains. Public capability seams were updated by the package owner. There were no tests under `tests/unit/foundation/hooks` at this checkpoint, so no browser test was silently moved into Node routing.

## Operation outcomes

The declaration scan excludes Standard Schema protocol files from house Result rewrites. `SpeechRecognitionResultLike` and `SpeechRecognitionResultListLike` are browser payload protocols, not success/failure carriers. Runtime controls retain their names; state/status projections remain separate from typed failures.

One real missed operation was `CommandRegistry.run`: a legacy string outcome mixed success with missing/unavailable/failed execution. It now returns `CommandRunResult`; handlers may return a total void or an explicit `Result<void, AppError>`. Missing/blocked/explicit handler failures are typed outcomes; programmer exceptions report through `onError` and reject. Four tests verify these boundaries.

The older `useClipboard` swallowed failed copy operations. It now calls the shared `copyText` boundary and returns `ClipboardWriteResult`, preserving `copied`, `error` and `reset`. Generation and disposal guards stop stale completions updating reactive controls. Three tests cover unsupported runtime, reset/disposal and concurrent outcomes.

Twenty-six operation/failure types were extracted from twelve mixed files; unifying the two generic screen carriers leaves 25 dedicated model files. Existing source seams re-export these types without declaring a second carrier. Every new model role group has at least two files. Shared `Result` and command models already had their own files.

| Previous operation alias | Final public operation alias |
|---|---|
| ClipboardWriteResult / ClipboardReadTextResult / ClipboardReadItemsResult | unchanged: already noun + verb |
| PositionResult | PositionReadResult |
| MediaStreamResult | MediaStreamRequestResult |
| NotifyResult | NotificationShowResult |
| ScreenResult / ScreenValueResult | ScreenRequestResult<TValue = void> |
| OrientationLockResult | unchanged |
| ShareResult | ShareSendResult |
| ShareOrCopyResult | ShareSendOrCopyResult |
| SpeakResult | SpeechSpeakResult |
| RecognizerStartResult | unchanged |
| ValidationResult (native validator only) | ValidatorParseResult |
| RunInWorkerResult | WorkerRunResult |
| CommandRunOutcome | CommandRunResult |

Failure type names also change `NotifyFailure` → `NotificationFailure`, `SpeakFailure` → `SpeechFailure`, and `RunInWorkerFailure` → `WorkerRunFailure`. New closed exported vocabularies are ClipboardFailureCode, PositionFailureCode, MediaStreamFailureCode, NotificationFailureCode, ScreenFailureCode, OrientationLockFailureCode, ShareFailureCode, SpeechFailureCode, RecognizerStartFailureCode and WorkerRunFailureCode. The existing `status` discriminant is typed through these vocabularies; runtime status values do not change. Native ValidationFailure continues to use transport-independent AppErrorType with validation issues.

## Reproducible checks

From the Vue package:

```sh
node scripts/check-capabilities.mjs
node scripts/check-capabilities.mjs --all
pnpm exec vue-tsc --noEmit -p tsconfig.typecheck.json
pnpm exec vitest run --project unit --project dom --project ssr tests/unit/foundation tests/unit/auth tests/unit/query tests/unit/router tests/unit/analytics tests/unit/flags tests/unit/providers
```

The checker uses TypeScript AST imports/exports and literal dynamic imports; Vue script blocks are parsed as TypeScript. It includes type dependencies. Default scope excludes presentation/formsEngine; `--all` includes their capability nodes. It reports unresolved relative/source-alias references and strongly connected capability groups, failing when either exists. It does not infer nonliteral dynamic dependencies or prove absence of cycles inside one capability.

The role checkpoint passed 49 test files / 319 tests and strict source/test typechecking. The AST graph at that snapshot passed with 54 scoped capabilities / 156 cross-capability references; including all source passed with 56 capabilities / 1,014 references. Later owners may change these counts while preserving the zero-cycle/zero-unresolved gate. Aggregate packaging, CSS and publishing gates belong to the parent.


## Final owned checkpoint

After own-file extraction and operation/failure-code renaming, the scoped unit/DOM/SSR run passed **50 files / 332 tests** (`/private/tmp/vue-final-model-tests.log`). Strict source/test typechecking passed (`/private/tmp/vue-result-names-typecheck.log`). Scoped source lint and formatting passed. AST capability checks subsequently passed with 54 scoped capabilities / 163 references, and 56 all-source capability nodes / 1,021 references. Later aggregate gates and independent lane checks remain parent-owned.

## Historical theme contrast checkpoint — superseded

This read-only checkpoint is **superseded** by the [Vue theme contrast resolution](vue-theme-contrast-resolution.md), including its required-indicator amendment. The evidence below records the pre-correction artifact, not the current source or release status.

At that checkpoint, the packed build's `getTheme('smart-qr')` returned authored colors with `status: 'validated'` but `meta.contrastAA: false`. Calling its actual `validateTheme` again reproduced all 11 failures. Independent sRGB relative-luminance calculations agreed; this was not missing metadata or a parser-only discrepancy.

| Mode | Foreground / background tokens | Hex colors | Ratio | Minimum |
|---|---|---|---:|---:|
| light | muted-foreground / muted | #6e7188 / #f1f2f8 | 4.2909 | 4.5 |
| light | subtle-foreground / background | #9b9fb5 / #d9dde8 | 1.9274 | 3.0 |
| light | accent-foreground / accent | #ffffff / #0d9488 | 3.7443 | 4.5 |
| light | info-foreground / info | #ffffff / #0891b2 | 3.6820 | 4.5 |
| light | success-foreground / success | #ffffff / #16a34a | 3.2957 | 4.5 |
| light | warning-foreground / warning | #78350f / #f59e0b | 4.2242 | 4.5 |
| dark | primary-foreground / primary | #ffffff / #8b5cf6 | 4.2344 | 4.5 |
| dark | destructive-foreground / destructive | #ffffff / #ef4444 | 3.7631 | 4.5 |
| dark | info-foreground / info | #ffffff / #06b6d4 | 2.4279 | 4.5 |
| dark | success-foreground / success | #ffffff / #22c55e | 2.2786 | 4.5 |
| dark | warning-foreground / warning | #78350f / #f59e0b | 4.2242 | 4.5 |

The former `constants/Validated.ts` documented retaining visual validation status regardless of the automated contrast result. That historical build contained 182 passing themes and one authored failing theme. The read-only review left row 37 open; the subsequent correction resolved that finding and renamed the catalog to `constants/Authored.ts`.


The current result is documented in [Vue theme contrast resolution](vue-theme-contrast-resolution.md): all 183 themes pass 119 declared pairs per mode after the foreground and required-indicator corrections. ForeverPin is a candidate awaiting app review. This establishes the declared token/surface contracts, not universal component WCAG compliance.
