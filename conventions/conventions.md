# Conventions — wow-two

*Last updated: 2026-09-12*

> **The single index to every convention.** When a task touches *how we build* — code, repo structure,
> naming, versioning — search HERE first, then open only the file(s) you need. Lookup table,
> **not auto-loaded**; do not pre-read the targets. Area indexes are named `{area}-conventions.md`; this is the root.

## How to use

1. Find what the task touches below.
2. Open that ONE file (leaf files live in the area sub-folders).
3. A repo-level rule (`workbench/{repo}/CLAUDE.md` or `.claude/rules/`) **overrides** a convention for that repo.

---

## Convention philosophy

- rule authority and tradeoff evaluation → [convention philosophy](philosophy/philosophy.md).

---

## Authoring a convention

Every convention doc follows this shape:

```markdown
# {Title}                         ← noun, matches the file name

*Last updated: YYYY-MM-DD*

> {What — one line}.
> Purpose — {why it exists / the problem it solves}.
> Use case — {when / where you reach for it}.

## {Section}

- compact bullet · backtick every `Symbol` and `path/to/file`
- one fact per bullet, no paragraph > 2 lines

---

## {Next section}

- ...
```

Rules:

- **Super-compact by default** — a convention is a *reference, not a tutorial*. Cut every word that doesn't change what the reader does; if a rule fits in
  a table row or a 1-line bullet, it must not be a paragraph.
- **Shape** — `# Title` → `*Last updated:*` → description blockquote → `##` sections. `---` between **every** section. No `## See also` — link inline only
  where load-bearing.
- **Description** — **one line**: **What** it governs + the scope boundary. Add **Purpose** (*why*) / **Use case** (*when*) only when they aren't obvious from What — and never restate a fact (e.g. a path) in both the description and the body. Not "Conventions for X" filler.
- **Budget — the rule that makes the rest measurable.** A line is **≤120 characters**, **75 preferred**; over 120 is an exception a claim earns by keeping its scope, causality or negation words. No cap on a doc's length — a doc is as long as its rules, and padding is caught by compaction, not by a line count.
- **Compaction — every rule earns its characters.** Cut a line the reader already believes; cut a line that changes nothing they do next; cut the motive clause unless it changes the action. Prefer the verb to its nominalization, and the actor as the subject. A rule that survives all three cuts is the rule; anything else was commentary.
  doc is carrying something that is not a rule — split it or move it (→ *Rationale lives elsewhere*). Check with
  `wc -l` and `expr $(wc -w < f) / $(wc -l < f)`; a words-per-line above ~8 means the bullets have become sentences. `controllers.md` sits at ~4.6.
  Exempt: this file and the `{area}-conventions.md` indexes — an index is a lookup table, and its length tracks the tree, not its own verbosity.
- **One owner per rule.** A rule is stated in exactly **one** doc — the one whose scope owns it — and every other doc links to it (`→ [x](y) § Section`). Two docs stating the same obligation drift into a contradiction, so the restatement is the defect even while the two still agree. Before adding a rule, grep its identifier across the tree; if it is already stated, link instead of restating. A sweep checks for restated rules, not only for conflicting ones.
- **The unit is the rule, not the topic.** Two docs covering naming is fine; two docs stating the same obligation is the defect. `service.md` saying `*Service` and `hosted-service.md` saying `*HostedService` are two rules, each owned where it belongs — both saying "suffix with `Service`" is one rule duplicated, and it extracts. Ask whether the sentences could ever disagree; if they could not, they are one rule.
- **Vectors do not share owners.** The same obligation stated once in the backend conventions and once in the frontend's is not a duplicate — each vector owns its own. Only a repeat *inside* one vector is the defect.
- **Rationale lives elsewhere.** A convention states **what to do**; *why* belongs in a co-located `{name}-rationale.md` or an `ideas/` analysis,
  linked once from the section. Evidence, RFC citations, counter-arguments, and measured findings are analysis — a reader looking up a rule pays
  for them on every read. Keep at most a one-clause because when it changes what the reader does.
- **`## Open` is capped at 5 items** — an unresolved question older than that is a stalled analysis, not a convention note. Move it to the
  rationale / analysis doc and link it.
- **Density** — super-compact bullets, imperatives, one fact per line. No prose paragraph > 2 lines. Code fence for multi-line only; backticks for every
  identifier.
- **A convention states the rule, never its history** — no "this used to be X", no "renamed from Y", no section
  justifying a change against what came before. A change that is right needs no defence, and a reader looking up a rule
  pays for the story on every read. Git carries the history; the doc carries the rule.
- **A convention is rules, not description** — the doc states what a reader must do, and a sentence that only describes
  the world belongs in the description blockquote or in an analysis doc. Reach for a bullet before a paragraph, a table
  before a bullet list, and an RFC keyword before a verb phrase.
- **Directive rules** — write each rule as `- must {action}` / `- must not {action}` / `- may {action}`: one atomic rule per bullet, the exact action, no rationale unless it changes what's done. Turn a description ("the latest folder is active") into a directive ("must treat the latest folder as active").
- **Plain-noun headers** — section headers are flat nouns (`Scope`, `Invariant`, `Naming`, `Lifecycle`), never narrative phrases (`The wall`).
- **Hard wrap** — wrap prose at **150 cols** (the editor's setting).
- **Tables vs bullets** — tables only for narrow 3+-item × 2+-col data that fits inside 150 cols. If any row would exceed the 150-col hard wrap,
  convert that table to bullet points — a wrapped wide table is unreadable.
- **Citation** — concrete symbols (`IKeyedEntity<TId>`, `AddDatabaseBespokeMigrations`) + file paths, **never namespaces** (they go stale — grep the
  symbol). Verify a symbol exists in source before citing; examples come from real code.
- **No duplication** — reference another convention inline; don't restate it. Supersede a stale note in place rather than stacking.
- **Link section to section, never bullet to bullet** — a doc that inherits a rule cites the owning section once, as a heading or one bullet, and states only what it overrides or extends. A reader who opens the child doc alone still sees the chain: base → construct → component.
- **A restatement is allowed only when the rule cannot be lifted** — two docs may carry the same sentence when the things they govern share no parent that could hold it. `Constants` and `Extensions` are different roles that happen to both declare a `public static class`; nothing above them is only-those-two, so each states it. Lift instead the moment a shared parent exists.
- **Location** — `{sub-domain}/{name}.md`; a folder's lead doc is `{folder}.md`, `README.md` only at a repo root.
- **One level per folder** — docs describing different levels never sit at the same folder level. A doc about *what you declare* and a doc about *how you write it* are two levels; separate them by folder or by nesting, never by filename alone.
- **A constraint earns a rule only when no positive rule already excludes it** — a starter rule fixes the starter, so a wrong starter is only a ❌ example; nothing about a correct starter forbids a type from bridging two services, so that needs its own rule.
- **An example demonstrates its own section, never the whole doc** — a code sample under `Member docs` shows the member-doc rules and may omit everything else the type needs. Repeating every convention in every example is what makes examples stale.
- **A line reference is `{file}:{line}`** — `style.md:75`, never "line 75" or "the line about bodies". The form is clickable in an IDE, greppable in a diff, and unambiguous when two files carry the same rule.
- **A link's display text names the thing, never the path** — the label says what the target is, and the path stays inside the parentheses. A path in the text is unreadable inline and goes stale on every move.
- **A layer references one layer down for doc rules, never restates them** — a component doc's `### Type doc` cites the layer below it and stops there; the reader crawls down for the merged set. Restating a lower layer's rule creates a second copy that drifts.
- **One example per doc-comment section, placed last** — it sits after the final field sub-heading so it covers every field the section declared, not only the first.
- **A table degrades to bullets** — if any row would exceed 120 characters, the table becomes bullet points. A wrapped cell is unreadable, and the wrap is the signal that the rows carry sentences rather than fields.
- **No files beside folders** — once a folder holds a sub-folder, every other doc in it gets its own folder too. The folder's own lead doc (`{folder}.md`) is the single exception.
- **A folder earns a lead doc at two docs** — `{folder}.md` says what the folder covers and indexes its contents. A folder holding exactly one doc needs none: that doc is its own lead, and a second file announcing the first is padding.
- **Bullet case** — a bullet is a **lowercase fragment**, not a sentence (capitalize only an identifier / proper noun that opens it). Terse `key - detail` fragments; `controllers.md` is the reference.
- **Order is normative** — list sections and their bullets in the **order they're applied**; readers + adopters follow that order unless a special case is called out (e.g. the attribute order, the doc-block order in `controllers.md`).

---

## Three axes, three words

A rule is filed by three independent questions. Each has its own word, and the words never substitute.

| Axis | Values | Answers |
|---|---|---|
| **layer** | `lla` · `mla` · `hla` | how far does the rule carry — a symbol, one app, between our apps |
| **bucket** | `constructs` · `components` · `domains` · `architecture` · `platform` · `frameworks` | what question does it answer |
| **register** | definition · application · surface | how deep does the statement go |

- must say **layer** only of `lla` / `mla` / `hla` — the word is taken, and a second use collides on the reader.
- **definition** states what a role is, its suffix, its contract shape → the `constructs` bucket.
- **application** states which one to reach for and with what values → the `components` bucket.
- **surface** enumerates one instance's props, slots and states → it lives with the code, never in a convention.
- must keep the surface register out of this tree — a convention that lists an instance's props goes stale the
  release after it is written, and the instance already documents itself beside its own source.

---

## Product principles

Rules every product obeys, whatever the stack. A convention that touches one links here rather than restating it.

- **GWDNBM — Get The Work Done & Never Bother Me.**
- must register, subscribe and wire nothing automatically — every wire is an explicit opt-in the caller states.
- must ship no ad, engagement prompt, nag, or unrequested email; a capability with nothing wired is a no-op.

---

## Domains

| Domain | Covers | Status |
|---|---|---|
| **development** (below) | how we build — repo shape, backend & frontend code style | Active |
| **planning** (below) | how we plan — version docs (grows over time) | Active |
| **agentic-workflow** (below) | how parallel chats / agents share a repo — lanes · no-revert · scope containment | Active |
| **marketing** (below) | how we name, brand & go to market — naming/domains · GTM · channels · SEO · content formats | Active |
| **design** (below) | how we design — variant-driven exploration · per-app specs · light/dark parity | Active |
| **deployment** (below) | how we ship & host — single-host serving · dev-port ledger (Docker · CI/CD · release to come) | Active |
| security | secrets handling, auth patterns, threat model | Planned |

---

## development — index: [development/development-conventions.md](development/development-conventions.md)

Cross-area: **[dev-cycle.md](development/dev-cycle.md)** — 2-cycle app↔SDK maturation (implement in-app → extract to SDK + conventions → adopt across the named active apps).
Cross-area: **[swappable-modules.md](development/swappable-modules.md)** — engine-wrapping SDK modules: house contract + adapter subpaths (optional peers) + one shared conformance suite + app-side one-line engine pin.

### repo/ — repo shape & setup · [repo-conventions.md](development/repo/repo-conventions.md)

| Need | File |
|---|---|
| Repo layout (product / venture) · `product/` + `engineering/` · code under `engineering/codebase/{slug}.{backend,frontend}-services` · naming · folder-docs (no README below root) · archetypes · **image-publish contract** (§13) · **audit** | [development/repo/structure/repo-structure.md](development/repo/structure/repo-structure.md) |
| SDK / library repo shape · `engineering/` + npm package under `engineering/codebase/{slug}/` · `src/` source-only + `tests/{unit,stories}` · config repoint · dist-only publish | [development/repo/structure/sdk-structure.md](development/repo/structure/sdk-structure.md) |
| Commit-message format (`{type}: {past-tense verb} {subject}`, 50–70 chars, subject only · one cohesive change) **+ commit protocol** — agent stages + commits; the human pushes, and history ops need a rapid-building marker (hook-enforced) **+ large files** — LFS vs gitignore, and repairing a binary already in pushed history | [development/repo/version-control/git.md](development/repo/version-control/git.md) |

### backend/ — .NET conventions · [the dotnet index](development/backend/dotnet/dotnet-conventions.md)

Backend rules live under `backend/dotnet/`: `core/` by scope, `shapes/` by deliverable.

| Folder | Owns |
|---|---|
| `core/lla/` | platform forms, symbol naming, documentation and style |
| `core/mla/constructs/` | our role definitions and suffix vocabulary |
| `core/mla/components/` | application rules for self-contained components |
| `core/mla/domains/` | application rules needing a capability or provider |
| `core/hla/` | contracts requiring both owned services to comply |
| `shapes/service/` | service architecture, host composition and delivery |
| `shapes/sdk/` | SDK build, package verification and release obligations |
| `shapes/library/` · `shapes/cli/` | contained-library and CLI shape rules when defined |

**Routing.** Role definition → `core/mla/constructs/` · symbol → `core/lla/` ·
component application → `core/mla/components/` or its owning domain ·
project placement, build and startup → the deliverable under `shapes/`.

### frontend/ — frontend conventions (cut twice) · [the frontend index](development/frontend/frontend-conventions.md)

Two orthogonal cuts: **scope** — how far a rule reaches; **shape** — what is being built.

| Folder | Holds |
|---|---|
| `core/lla/` | one symbol — constructs per platform · a form end to end · naming · docs · style |
| `core/mla/` | one app — the kinds we declare · which to reach for · domains · framework deltas |
| `core/hla/` | between our own frontends — **empty by design** |
| `shapes/app/` | a product frontend — architecture · platform (styling, dev server) · routing |
| `shapes/library/` | a package another frontend imports — kind-grouped layout, capability modules |

**Routing.** A kind you declare → `core/mla/constructs/` · which one, with what values →
`core/mla/components/` · a language form end to end → `core/lla/components/` · how any symbol is written →
`core/lla/notation/` · a capability → `core/mla/domains/{domain}/` · where a folder is created, how it builds
and ships → `shapes/{app,library}/`.

---

## planning — index: [planning/planning-conventions.md](planning/planning-conventions.md)

| Area | File |
|---|---|
| Rough-track docs — `r{X.Y}` unbounded first build: one task per subsystem, no sub-steps + template | [planning/rough-track/rough-track.md](planning/rough-track/rough-track.md) |
| Version-track docs — `v{X.Y}` versions: naming, lifecycle, cadence + iteration template | [planning/version-track/version-track.md](planning/version-track/version-track.md) |
| Polish-track docs — `p{X.Y}` behavior-invariant cleanup, tasks per file, decoupled + template | [planning/polish-track/polish-track.md](planning/polish-track/polish-track.md) |
| Vector-track docs — subject lanes, one chat each: archetype ladders, seams, git + build contention, release cuts + template | [planning/vector-track/vector-track.md](planning/vector-track/vector-track.md) |
| Engineering planning — repo roadmap + backlog | [planning/engineering-planning/engineering-planning-conventions.md](planning/engineering-planning/engineering-planning-conventions.md) |

---

## agentic-workflow — index: [agentic-workflow/agentic-workflow.md](agentic-workflow/agentic-workflow.md)

| Need | File |
|---|---|
| Parallel chats on one tree · assume-intentional / no-revert · lane discipline · scope containment · commit discipline | [agentic-workflow/agentic-workflow.md](agentic-workflow/agentic-workflow.md) |

---

## marketing — index: [marketing/marketing-conventions.md](marketing/marketing-conventions.md)

| Need | File |
|---|---|
| Brand-name + domain selection — taxonomy · scoring rubric · verification runbook (TM · RDAP · handles · cross-language) · domain strategy · checklist | [marketing/brand-naming-and-domains.md](marketing/brand-naming-and-domains.md) |
| Go-to-market meta — laws · launch sequence · activation/retention · pricing & CRO (fee-efficiency) · metrics · workflow · checklist | [marketing/go-to-market.md](marketing/go-to-market.md) |
| Channels catalog — audience-fit + effort/payoff per channel (SEO · short-form · Pinterest · directories · integrations · communities · partnerships) | [marketing/channels/channels.md](marketing/channels/channels.md) |
| SEO — intents · comparison pages · programmatic SEO | [marketing/channels/seo.md](marketing/channels/seo.md) |
| Content formats — short-form video + content library (viral · sell · educate) | [marketing/channels/content-formats.md](marketing/channels/content-formats.md) |
| Meme templates — reusable meme/cultural/trending-audio shells (Nobody's-gonna-know · two-button · expanding-brain · POV …) | [marketing/channels/meme-templates.md](marketing/channels/meme-templates.md) |

---

## design — index: [design/design-conventions.md](design/design-conventions.md)

| Need | File |
|---|---|
| Design exploration — variant-driven (a few in-context options → pick → lock → cascade → spec) · other modes · mode-selection · per-app spec shape | [design/research/design-exploration.md](design/research/design-exploration.md) |

---

## deployment — index: [deployment/deployment-conventions.md](deployment/deployment-conventions.md)

| Need | File |
|---|---|
| Single-host serving (product / venture) — SPA baked into the backend `wwwroot` (vite `outDir` + static-serve + `BuildSpa` target + dev proxy) · CORS posture | [deployment/hosting/single-host-serving.md](deployment/hosting/single-host-serving.md) |
| Port ledger — allocated dev ports | [deployment/hosting/ports.md](deployment/hosting/ports.md) |

---

## Scaffolding

- New conformant repo → skill **`create-repo`**. Template repo: `workbench/wow-two-sdk-beta/wow-two-sdk-beta.product-template/`.

---

## Precedence

A convention applies to **every** repo under `wow-two-ws/`; a repo-level rule overrides for that repo. **Naming + documentation conventions are centralized here** — they apply to the backend-beta SDK too. The SDK keeps only package **layout / registry** as internal architecture under its own `docs/` (`docs/architecture/package-layout.md`, `docs/package-registry.md`).
