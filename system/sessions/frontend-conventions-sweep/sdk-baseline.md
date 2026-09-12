# Frontend SDK baseline — 2026-09-09

Scope: read-only baseline of `workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui`, to support the conventions audit. This is not a completed semantic SDK audit. No repository edits, installs, builds, tests, staging, commits or publishing performed. Dirty tree: 690 porcelain status rows at inspection; ownership is unresolved and the rows include staged and unstaged edits.

## Packages and release ownership

| Package | Directory under `engineering/codebase/` | Local package version | Release workflow |
|---|---|---|---|
| `@wow-two-beta/ui` | `wow-two-front-beta-sdk` | `0.0.108` | `.github/workflows/release.yml` |
| `@wow-two-beta/ui-vue` | `wow-two-front-vue-beta-sdk` | `0.0.5` | `.github/workflows/release-vue.yml` |

These are local manifest versions, not independently verified registry versions. There is no package manifest or pnpm workspace at the repository root. Each package has its own manifest, lockfile, workspace and package scripts. Only root `CLAUDE.md` was found; no nested `AGENTS.md`, `CLAUDE.md`, or `.claude/rules/*.md` was found outside ignored dependency/git trees.

Both releases trigger on main pushes filtered to their respective package directory or release workflow; each also supports manual dispatch. Both install, typecheck, lint, build, bump the patch, publish npm, commit/tag the bump, and create a GitHub Release. Vue tags use `ui-vue-v*`; React tags use `v*`. Both `prepublishOnly` scripts rerun typecheck and build. Tests are outside both release workflows; `.github/workflows/test.yml` runs only React, separately. Vue format checking is not in its release workflow. A package choice is necessary before the sweep/release scope is concrete.

## Existing sweep: measured facts and measurement limitations

Source: `engineering/planning/ui-sdk-conventions-sweep.md`, last updated 2026-08-24. Rows combine different scopes: #9 is React, macro rows are Vue, and #11 is four smart-qr app components. The document is a shared backlog, not a single-package audit.

| Sweep row | Current baseline | Interpretation |
|---|---|---|
| #9 React 19 spellings | 324 `forwardRef` calls in 232 source files; 576 token occurrences in 233 files; 164 `ComponentPropsWithoutRef` tokens in 80 files; 46 opening `*Context.Provider` tags in 41 files | Existing 324 sites is reproduced. Its 233 files count is token-based, including an import-only occurrence. Calls and tokens must stay distinct. |
| #12 common Result carrier | Two `Result` declarations in each package, both `StandardSchemaV1.Result<Output>` in embedded Standard Schema contracts; no `foundation/results/` module found | Grepping `type Result` does not prove the requested `Result<TSuccess,TFailure>` carrier exists. Standard Schema declarations are unrelated. Do not rename vendor structural contracts as local bags. |
| #13 Result bags | Many `*Result` names remain across auth, workers, upload, speech, query and browser modules | A token grep includes type imports and reexports; the historic seven return bags cannot be safely re-counted from token matches. Re-enumerate actual definitions and separate controls from failure carriers. |
| #17 expose root handles | 310 `defineExpose` calls; 308 expose only `el`; 1 exposes `el` plus methods (`MessageList`); 1 exposes only `fire` (`Confetti`) | Historic 308 root-only sites reproduced. Literal `defineExpose({ el })` finds only 228; alias forms add 63 and computed/member access forms add 17. Scope semantics matter. |
| #18 demos | Vue has 406 `.vue` source files and zero `.stories.*` files | Historical playground-unreferenced count of 121 was not remeasured; zero stories does not establish zero demos. React has 237 story files. |
| #22 folder casing | React has 23 uppercase-initial source directories; Vue has 26 | These are filesystem counts, not a semantic camelCase validation. The old row's 27 total should not be copied as current. |
| #8/#27 specs | React 203 source `*.spec.md`; Vue 181 | Coverage denominators need a concrete component/root/subpart inventory, so 198/378 is not revalidated. Contradictions require per-spec comparison, not counting. |
| #25 kind suffixes | Vue still has 406 SFC source files | 112 unsuffixed is not independently revalidated; use current kind/compound exemptions rather than a suffix-only regex. |
| #11 Screen→Page | Existing row explicitly says smart-qr | Application-owned; do not silently pull app edits into the SDK sweep. |

Other rows (#7 taxonomy, #14 HTTP Result adoption, #26 capability ownership, #27 specification accuracy, #30 missing ARIA members) remain independent work. The historical #23 live-prop pass-through discussion persists outside the Open table; its status needs reconciliation instead of assuming completion. Smaller breaches in the “15–22” prose also need explicit dispositions or links to completed rows.

## Release-critical gap discovered

The Vue source renames `format` → `formatters`, `sync` → `channels`, `undo` → `history`, and `validation` → `validators` are present. The manifest still advertises the four old subpaths, and Vite's `subpathLayer` still points to old source locations:

- `package.json:106` — `./foundation/format`
- `package.json:186` — `./foundation/sync`
- `package.json:216` — `./foundation/undo`
- `package.json:241` — `./foundation/validation`

`vite.config.ts:128` filters nonexistent entry sources instead of failing the build. Its subsequent warning says those advertised imports will not resolve. Thus a successful build is insufficient evidence that every export exists. No build was run; the evidence is the missing source paths and build configuration. Test include globs also name the old capability paths, so a directory migration must reconcile source entries, export maps, and test discovery together. Confirm actual test movement before deciding whether a glob currently misses tests.

Required sweep addition: validate every advertised runtime and declaration export in the packed artifact, update renamed module entries and test globs, and remove the port-era permissive missing-entry behavior when the port is complete. Do not close “4 activity folders renamed” as release-complete solely because typecheck/format/tests/lint pass.

## Nested instruction conflicts

The repository `CLAUDE.md` is React-era and governs both packages:

1. `CLAUDE.md:50–57` defers `*.spec.md` and later adds `*.standard.md`; the sweep requires specs and says standard files were removed. The local override and sweep target disagree.
2. `CLAUDE.md:28–33` permits `*Helpers.ts`; the sweep records them as banned/renamed.
3. `CLAUDE.md:42–47` requires colocated React stories; the real source/test layout and Vue demo strategy differ.
4. Root-relative `src/`, `.storybook/`, and `apps/` examples predate the two-package `engineering/codebase/` layout.
5. `CLAUDE.md` says tests are not a CI gate; the React test workflow is indeed separate, but local full validation remains necessary to call a sweeping API rename complete.

These require a package-aware SDK instruction refresh before applying the settled central conventions. They are not evidence that the central conventions are internally inconsistent.

## Meaningful release validation

For the selected package, after dirty-tree lane ownership and sweep scope are resolved:

- Run typecheck, lint, relevant formatting checks, and the complete configured test projects. Vue `typecheck` must include its `check-sfc` compiler gate.
- Validate interaction behavior after ref/handle renames: focus, exposed imperative methods, controlled/uncontrolled state and SSR behavior. Pure text counts do not cover these.
- Build and inspect a packed artifact; assert every `exports` runtime/type target exists, CSS/theme assets exist, and renamed entries import successfully.
- Install/import the packed package in an isolated consumer fixture, including optional-peer subpaths. No production consumers is compatible with this packaging smoke test.
- Verify Vue unit/SSR/DOM/browser test discovery and React unit/browser/storybook discovery, as applicable; do not equate `passWithNoTests` with browser coverage.
- Check published registry version only at release preparation time; confirm npm publication, resulting tag and release independently because workflow publication precedes the Git bump/tag step.

No validation above has been executed during this baseline.

## Reproducible read-only commands

Run commands from the SDK repository root. Counts below restrict source scans to `.ts`, `.tsx`, `.vue` and do not include generated dist or dependency trees.

```python
from pathlib import Path
import re
for name in ['wow-two-front-beta-sdk', 'wow-two-front-vue-beta-sdk']:
    root = Path('engineering/codebase') / name
    data = {p: p.read_text() for p in (root / 'src').rglob('*')
            if p.suffix in ('.ts', '.tsx', '.vue')}
    for label, regex in [
        ('forwardRef tokens', r'\bforwardRef\b'),
        ('forwardRef calls', r'\bforwardRef(?:\s*<[^;]*?>)?\s*\('),
        ('ComponentPropsWithoutRef', r'\bComponentPropsWithoutRef\b'),
        ('Context.Provider opening tags', r'<[\w.]*Context\.Provider\b'),
        ('Result declaration', r'\b(?:type|interface|class)\s+Result(?:\s*<|\s*\{|\s*=)'),
        ('defineExpose calls', r'\bdefineExpose\s*(?:<[^>]*>)?\s*\('),
    ]:
        hits = [(p, len(re.findall(regex, t, re.S)))
                for p, t in data.items() if re.search(regex, t, re.S)]
        print(name, label, sum(n for _, n in hits), 'sites', len(hits), 'files')
```

The forwardRef call regex reproduced the historical count but is a lexical inventory, not an AST semantic classifier. Root-only expose count was obtained by enumerating every object body matched by `defineExpose\s*\(\s*\{([\s\S]*?)\}\s*\)` and manually classifying the 18 non-shorthand/alias forms; the unmatched generic `Confetti` call was separately inspected.

```python
from pathlib import Path
import json
root = Path('engineering/codebase/wow-two-front-vue-beta-sdk')
for key, value in json.loads((root/'package.json').read_text())['exports'].items():
    if isinstance(value, dict) and value.get('import', '').endswith('/index.js'):
        src = root / value['import'].replace('./dist/', 'src/').replace('/index.js', '/index.ts')
        if not src.exists():
            print(key, src)
```

This second command reports the four stale capability paths above. It checks source-to-export agreement, not the actual packed output.

