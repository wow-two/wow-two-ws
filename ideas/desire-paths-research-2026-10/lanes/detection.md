# Detection signals and instrumentation for desire paths (software products and component libraries)

_Legend. Cost tags in Inferences: **[cheap]** = a 1-2 person team, hours to a few days; **[mid]** = days to build plus upkeep; **[org]** = needs a research or design-ops org. Dates are publication or last-update dates where the page showed one; pre-2019 sources are flagged. "Snippet-only" means the claim comes from a search-result excerpt because the page could not be fetched in full. Researched 2026-10-27._

## 1. End-user product signals: what to measure, which tools surface it, which are self-hostable or privacy-friendly

### Takeaway
Most end-user desire-path signals reduce to a few measurable patterns: site-search queries, frustration clicks (rage and dead), navigation loops and quick backs, funnel abandonment, copy/export events, and free-text complaints. PostHog, Microsoft Clarity and FullStory detect rage and dead clicks out of the box; search-log analysis, copy-out, URL hacking, zoom and repeated manual steps need custom events or log queries. No fetched source documents URL-hacking or browser-zoom detection in a mainstream tool.

### Cited Findings

**Search-log analysis (queries that should have been navigation)**
- Export the top 1,000 query terms over 3-6 months sorted by frequency; review the top ~300 closely and flag terms the site does not offer or you do not understand — [NN/g, Susan Farrell, 2017-07-30 (pre-2019)](https://www.nngroup.com/articles/search-log-analysis/)
- Sort by user identifier then timestamp to reconstruct one person's search sequence; repeated related searches indicate earlier queries failed; a shared IP address may be many people or a server — [NN/g 2017](https://www.nngroup.com/articles/search-log-analysis/)
- Zero-result queries point to misspellings or missing content; blank queries can mean users work around poor search/IA or the widget fires accidentally; frequent numeric queries suggest product-ID or phone lookups are wanted — [NN/g 2017](https://www.nngroup.com/articles/search-log-analysis/)
- High search volume with few downstream conversions (the article's heating-pad example) means "wanted but not findable"; action step: review the first results page for the top 100 queries, then tune synonyms, set best bets, add redirects — [NN/g 2017](https://www.nngroup.com/articles/search-log-analysis/)
- Top-query lists hide most of the information: about 80% sits in the long tail, so group queries by meaning — [online-behavior.com](https://online-behavior.com/?p=5772) (search-result excerpt; practitioner blog)

**Rage clicks, dead clicks and related frustration signals**
- PostHog fires `$rageclick` after three clicks, each within 30 px and 1 s of the previous one; click count, distance and timeout are configurable — [PostHog autocapture docs](https://posthog.com/docs/product-analytics/autocapture.md)
- With the latest SDK `defaults`, PostHog ignores next/previous controls, quantity steppers (`+`/`-`) and text-selection surfaces (inputs, textareas, `contenteditable`) for rage clicks; exclusions via `.ph-no-rageclick`, `css_selector_ignorelist`, `content_ignorelist`, `ignore_text_selection` — [PostHog autocapture docs](https://posthog.com/docs/product-analytics/autocapture.md)
- PostHog defines a dead click (also "slow click") as a click not followed by a change to the page; enable with `capture_dead_clicks: true`; heatmaps collect dead-click coordinates at no extra cost, autocaptured dead-click events bill as standard events; the docs give no default timing threshold — [PostHog autocapture docs](https://posthog.com/docs/product-analytics/autocapture.md)
- Clarity flags rage clicks, dead clicks (no feedback "in a reasonable amount of time", no visual change, no navigation), excessive scrolling, quick backs, and click errors (a JS error after a click); it publishes no numeric thresholds — [Microsoft Learn, Clarity semantic metrics, ms.date 2025-12-01](https://learn.microsoft.com/en-us/clarity/insights/semantic-metrics)
- FullStory groups rage clicks, error clicks, dead clicks and thrashed cursor as its frustration signals — [FullStory help](https://help.fullstory.com/hc/en-us/articles/360020624154) (snippet-only)
- Known false positives: Next/Previous buttons, carousels, image galleries, sliders and incrementing quantity fields invite legitimate repeated clicks — [Request Metrics](https://requestmetrics.com/blog/ux/what-is-a-rage-click/) (search-result excerpt); consistent with PostHog's default ignore-list above

**Back-and-forth loops and abandonment**
- Clarity's "quick back" fires when a user leaves via a click and returns faster than the page's dwell-time threshold; for internal pages "click dwell time" is time spent on a subpage before returning to the source page, a usable proxy for loops — [Microsoft Learn, Clarity semantic metrics](https://learn.microsoft.com/en-us/clarity/insights/semantic-metrics)
- Clarity offers no-code funnels and code-free "smart events" — [Microsoft Learn, Clarity semantic metrics](https://learn.microsoft.com/en-us/clarity/insights/semantic-metrics)

**Copy-paste out of the app**
- PostHog autocapture records copied or cut text when `capture_copied_text` is true, and does not capture clipboard content from password fields — [PostHog autocapture docs](https://posthog.com/docs/product-analytics/autocapture.md)
- PostHog autocapture covers clicks on `a`, `button`, `form`, `input`, `select`, `textarea`, `label`, plus pageviews/pageleaves; form values are not captured automatically — [PostHog autocapture docs](https://posthog.com/docs/product-analytics/autocapture.md)

**Self-hostability**
- PostHog self-hosting is "officially unsupported"; all paid-plan features are Cloud-only; the decision flowchart uses 300k events/month as its threshold; Cloud's free tier covers 1M events/month; no CVEs or tagged releases for self-hosted builds (undated page) — [PostHog self-host docs](https://posthog.com/docs/self-host)

**Concept grounding**
- "Digital desire paths" (Wiesche, Böhm, Schermann, European Journal of Information Systems 33(2), pp. 145-160, March 2024): examined six workarounds in two organizations; reframes workarounds, usually treated as disruptions, as input to design — [RePEc listing](https://ideas.repec.org/a/taf/tjisxx/v33y2024i2p145-160.html) (abstract only; full text is paywalled)

### Inferences
Mapping of desire path to signal to cheapest collection route (cost tags are my judgement; items marked "unverified" come from background knowledge, not a fetched source):

| Desire path | Signal | Cheapest collection | Tier |
|---|---|---|---|
| Search used as navigation | Top queries, zero-result, repeated reformulation in one session | Log queries server-side from the app's own search endpoint; weekly top-300 review per NN/g | [cheap] |
| Element looks clickable but is not | Dead click, rage click on non-interactive element | PostHog autocapture or Clarity; filter to elements with no handler | [cheap] |
| Loop between two screens | A-B-A-B route sequences, quick backs, high dwell-then-return | Router `afterEach` hook emitting a route event; count A-B-A within 30 s (unverified design) | [cheap] |
| Abandoned flow | Funnel drop-off with a late exit to another tab/route | Clarity funnels (no code) or PostHog funnels | [cheap] |
| Copy data out to do the work elsewhere | Copy events on table cells or results, export-button spikes, `capture_copied_text` | PostHog flag, or a `copy` listener on data regions | [cheap] |
| URL hacking | Hand-edited query strings or IDs, 404s with plausible slugs, direct-to-deep-link hits without a referrer | Server access-log query for 404s and unknown params (unverified, no source found) | [cheap] |
| Browser zoom | Zoom change signals low-contrast or too-small UI | `visualViewport`/`devicePixelRatio` change event (unverified, no source found); low priority | [cheap] |
| Repeated manual steps | Same 3-5 event sequence repeated N times in a session | Custom events plus a path/sequence query; bulk-action candidate | [mid] |
| Feature requests framed as workarounds | "I currently do X by...", "how do I get around..." | Tag support tickets and feedback with `workaround`; monthly read (no source found) | [cheap] |
| Cross-cohort and cross-segment validation | New vs power users, per-app | PostHog cohorts or SQL on your own event table | [mid] |
| Moderated observation of 20+ users, replay review at scale | Full qualitative synthesis | Research function | [org] |

- For a solo developer with ~30 apps, a single first-party `track()` in the SDK plus Clarity/PostHog autocapture for rage and dead clicks covers most rows without new infrastructure; replay review is the expensive part, so sample it.
- Clarity is a Microsoft-hosted service; I did not confirm whether any self-host path exists (unverified, treat as not self-hostable).
- Rage/dead clicks are heuristics for "go watch these sessions", not measurements; both vendors' docs frame them that way and Clarity gives no thresholds.

### Gaps
- LogRocket: no primary documentation reviewed.
- Hotjar: no primary documentation fetched; only secondary excerpts that it filters recordings by rage click.
- FullStory: no published numeric thresholds found; its help page was seen only as a search excerpt.
- No source found for detecting URL hacking, browser zoom, or repeated manual steps as named product features.
- No source found on mining support tickets for workaround language.
- Whether Clarity can be self-hosted: not confirmed from a primary source.
- PostHog "hobby" deployment limits: the vendor page gave no events-per-month cap; a third-party guide's ~100K figure is unverified.
- The NN/g search-log article predates 2019 (2017); no 2019+ NN/g replacement found.

## 2. Qualitative methods: what each reveals about desire paths specifically

### Takeaway
Only observation in the user's own context ("what people do") reliably surfaces desire paths, because people stop noticing their own workarounds; contextual inquiry and "show me" sessions are the main discovery tools, JTBD switch interviews find the struggle that precedes a workaround, and first-click/tree tests check whether a proposed paved path is findable rather than discovering new paths. Diary studies are limited to what participants can easily record.

### Cited Findings
- "What people say" and "what people do" are "very often... quite different"; analytics answers how many but not why, and needs instrumentation in advance — [NN/g, Christian Rohrer, 2022-07-17, reviewed 2026-07-15](https://www.nngroup.com/articles/which-ux-research-methods/)
- Field studies and contextual inquiry capture near-natural use in the participant's environment: greater external validity, less control over topics; generative stage; contextual inquiry is the collaborative variant for complex systems — [NN/g Rohrer 2022](https://www.nngroup.com/articles/which-ux-research-methods/)
- Diary studies "can be done only for data that is easily recorded by participants" — [NN/g Rohrer 2022](https://www.nngroup.com/articles/which-ux-research-methods/)
- Card sorting is attitudinal (reveals mental models, not findability); tree testing measures how easily users find items in a hierarchy and is quantitative — [NN/g Rohrer 2022](https://www.nngroup.com/articles/which-ux-research-methods/)
- Contextual inquiry is an ethnographic field study with a small sample, modeled on the craftsman-apprentice relationship, with context (observe where the user normally works) as its first principle — [NN/g, Contextual Inquiry](https://nngroup.com/articles/contextual-inquiry) (opening excerpt only; undated)
- Secondary glossaries say the apprentice framing turns a summarizing interview into a demonstration, targets the gap between reported and actual behaviour, and that people build workarounds they no longer notice; an example has nurses overriding a barcode scanner because it is mounted awkwardly; sessions typically run 2-3 hours — [The Behavioral Scientist glossary](https://www.thebehavioralscientist.com/glossary/contextual-inquiry); [UXtweak](https://blog.uxtweak.com/es/contextual-inquiry/) (combined search excerpt; exact attribution per page unclear)
- JTBD (Bob Moesta): the "struggling moment" is the seed of innovation; the switch interview reconstructs the timeline of the customer's last switch rather than asking for abstract self-analysis; push, pull, anxiety and habit forces explain switching or staying; hypothetical feedback is of little use — [Business of Software talk](https://businessofsoftware.org/talks/understanding-your-customer-jtbd/); [Echai Ventures summary](https://echai.ventures/startingup/jobs-to-be-done/how-do-i-find-the-job-when-my-customers-can-t-articulate-it-themselves)
- Tree testing strips visual design so participants navigate the hierarchy alone; run it first when unsure which problem you have — [CleverX](https://cleverx.com/blog/first-click-testing-vs-tree-testing-which-ia-method-to-use); [Welsh Government digital guidance](https://digitalpublicservices.gov.wales/guidance-and-standards/meet-user-needs/tree-testing)
- First-click testing adds the visual layer (screenshot or prototype, "where would you click first?") and is not suited to multi-step flows, emotional response or discovery behaviour — [CleverX](https://cleverx.com/blog/first-click-testing-vs-tree-testing-which-ia-method-to-use)
- Workarounds can be treated as design input rather than defects; the authors studied six across two organizations — [Wiesche, Böhm, Schermann 2024](https://ideas.repec.org/a/taf/tjisxx/v33y2024i2p145-160.html)

### Inferences
- What each method reveals about desire paths (mapping is mine, built from the cited descriptions):
  - Contextual inquiry / "show me how you do X": finds the actual path including tabs, spreadsheets and notes outside the app. Highest yield, [cheap] at 5-8 sessions of 30-45 min via screen share; [org] when run as formal 2-3 hour ethnography.
  - JTBD switch interview: finds why someone left the paved path (push/pull/anxiety/habit). [cheap] in count (5-8 interviews), skill-intensive.
  - Diary study: only for repeated workarounds users can log (for example "each time I export to a spreadsheet"). [org]; skip for a small team.
  - Tree test: tests whether a label or location users keep searching for is where they expect it. [cheap] with any tree-test tool.
  - First-click test: validates a candidate paved shortcut or renamed control before building. [cheap]; one static screenshot and a form suffice.
  - Analytics first, qualitative second: use quant to find where, qualitative to learn why, per the NN/g how-many/why split.
- A useful interview probe set (background knowledge, unverified as a method): "What do you do right before and right after this screen?", "What do you keep open in another tab/app while using this?", "Show me the last time you did this."

### Gaps
- No source found that applies "show me how you do X" sessions to desire-path discovery by name; the link is inferred from contextual-inquiry descriptions.
- No NN/g diary-study article was fetched; the Rohrer overview is the only NN/g source on diary studies.
- The JTBD sources did not address workarounds or hacks explicitly.
- First-click and tree-test sources are vendor and government guidance, not NN/g.
- No evidence found on sample sizes or hit rates for detecting desire paths specifically with these methods.
- The Wiesche et al. paper's criteria for separating valuable workarounds from noise are not available (full text paywalled).

## 3. Developer-side desire paths in a component library

### Takeaway
The measurable signals are detach rate (Figma), per-component override frequency and overridden lint rules (GitHub, Amplitude and Productboard, second-hand), prop usage, and design-system vs custom component ratios (react-scanner, Omlet, Radius Tracker). Existing tooling is React-oriented; no Vue-capable scanner was confirmed, so a Vue 3 SDK team should expect to write a small AST scanner. Primary publications from Primer, Polaris, Atlassian and Carbon on snowflake detection were not found.

### Cited Findings

**Figma-side (detach)**
- Figma Design System Analytics shows total instances, recent inserts and detachments per component; the 2019 launch example: at Google the button was "used and detached more than any other component", the designer concluded the master was too complex and built a simpler version alongside it; Microsoft used detach data to see "which components are often detached and may need updating" — [Figma blog, 2019-11-20 (editorial note 2025-02)](https://www.figma.com/blog/introducing-design-system-analytics/)
- A high detachment rate is not always a problem (full-screen templates are meant to be detached); otherwise it may mean the component misses designers' needs; the component view lists the teams and files using it for qualitative follow-up; the page gives no numeric thresholds (undated) — [Figma best practices](https://www.figma.com/best-practices/make-the-most-of-design-system-analytics/)
- athenahealth: each detachment points to one of three causes (a bug, a missing enhancement, or an unexpected combination of elements); an auto-layout wrapping bug was caught after detachments rose; they use custom scripts on Library Analytics API data, add component types and "expected detachment rates", review monthly, then diagnostics, user outreach, implementation; ~100,000 insertions/month; recommend looking back over a past period with known outcomes — [Figma, Carly Ayres, "Design systems 104", 2025-02-11](https://www.figma.com/blog/design-systems-104-making-metrics-matter/)
- Example dashboard row: Footer with 25 instances, 9 inserts, 8 detaches in 30 days (uninterpreted in the article) — [Figma "Design systems 104" 2025](https://www.figma.com/blog/design-systems-104-making-metrics-matter/)
- The Library Analytics API is Enterprise-only, recalculated daily at 00:00 UTC, paged at up to 1,000 rows — [Figma developer docs](https://developers.figma.com/docs/rest-api/library-analytics-intro) (search-result excerpt)
- One hands-on report says inserts can be recorded for components consumers never deliberately placed ("passive inserts") — [Medium post](https://iknowdavehouse.medium.com/are-your-figma-design-system-analytics-high-as-a-kite-c5b1440a112b) (anecdotal, single author)

**Code-side (overrides, custom components, forks)**
- GitHub reported per component how often developers override it, to find "where there is user friction"; Amplitude and Productboard engineers reported the number of overridden ESLint rules; Onfido used color overrides to show where DS components could be used; Xero reported adoption per repository using CODEOWNERS; Adverity tracks prop usage (unused prop = removal candidate); Rangle's open-source radius-tracker compares DS components against one-off components as a percentage of code; Sparkbox 2022: "less than 16%" of teams track metrics — [Omlet blog, Patrick Suzuki, 2023-01-10](https://omlet.dev/blog/data-driven-design-systems-in-practice/) (second-hand; no override counts given)
- react-scanner statically extracts component and prop usage into JSON via three processors: `count-components`, `count-components-and-props`, `raw-report` (every instance with prop values and file locations); non-literal prop values appear as AST node types unless `getPropValue` is used — [muthanna.tech](https://muthanna.tech/til/react/finding-the-most-used-react-components-with-react-scanner); [react-scanner fork README](https://github.com/mihkeleidast/react-scanner)
- Fabric's team used react-scanner to compare DS3 vs DS4 component usage with a dashboard, and a custom AST script to flag native HTML elements used instead of components — [GitNation talk, "Measuring Coverage of React Design System"](https://portal.gitnation.org/contents/measuring-coverage-of-react-design-system)
- Brevo (2023-04-28): react-scanner + cron GitHub Actions workflow + Prisma + Metabase, clone all org frontend repos in a matrix job, count projects using the DS, component instances over time, distinct components per project, versions per project, DS-vs-legacy ratio; the post does not mention props, overrides, custom components or CSS, and gives no thresholds; >25 internal projects adopted within a year — [Brevo Engineering](https://engineering.brevo.com/how-to-track-design-system-adoption/)
- Omlet scans repos with a CLI (`init` via npm/yarn/pnpm, run from the library repo) and reports component and prop usage, adoption by project, legacy and non-DS components developers use most, unused props, similar components to consolidate, deprecation impact; the page does not state support beyond React, override tracking, CI use, code-upload behaviour or pricing — [omlet.dev](https://omlet.dev)
- Optimizely used Omlet trendlines as an "adoption scoreboard" and the dependency tree to plan a legacy Grid replacement (2023-05-10); no thresholds or override method given — [Zeplin Gazette](https://blog.zeplin.io/optimizely-harmony-session-2023)
- Omlet 1.0 announcement (2023-10-17): measures component usage and adoption across all projects; the post does not mention overrides or Vue — [Zeplin blog](https://blog.zeplin.io/meet-omlet-component-analytics-for-developers)
- Practitioner guides list override counts, local CSS overrides and `!important` on system components as named metrics, and a "heavily used and heavily overridden" component as a candidate to absorb the override — [Netguru](https://www.netguru.com/blog/design-system-metrics); [OverlayQA](https://overlayqa.com/blog/audit-design-system-adoption/); [Design System Observatory](https://asundiev-devrev.github.io/ds-observatory/) (all snippet-only, practitioner opinion)
- Nathan Curtis (EightShapes) reportedly uses self-reporting by team or product to keep an adoption scorecard — "not exact numbers" but shows what blocks full adoption — [Supernova](https://www.supernova.io/blog/9-design-system-metrics-that-matter) (secondhand, snippet-only)
- Radius Tracker's page says it measures component adoption "in real time" and gives no detection method, framework support or license; a search excerpt says the report is "a collection of files" and the tool is open source — [Rangle](https://rangle.io/radius-tracker); [Radius docs](https://radius.rangle.io/features/tracker)
- A "detachment curve" article argues a healthy detach rate depends on growth stage (expansion tolerates more, consolidation less) — [Design Systems Collective](https://www.designsystemscollective.com/managing-the-design-system-detachment-curve-030b2526f62f) (snippet-only; fetch returned 403)

### Inferences
Everything in this block is my design proposal, grounded in the cited capabilities but not documented by any source as a Vue method (unverified):

- **Vue 3 static scanner [cheap to mid].** Parse SFCs with `@vue/compiler-sfc` (template AST) and count: library component usages (by import source or registered name); props/attrs passed; `class`/`style` bindings on library components (override signal); scoped `:deep()` or `!important` selectors targeting library class names; plain HTML elements where a library component exists (Fabric's native-element idea); `eslint-disable` of library rules (Amplitude/Productboard idea). Emit a react-scanner-style `raw-report` JSON per app, run via cron/CI over the ~30 repos (Brevo's pipeline shape), store in a table or Metabase/sheet. A day or two of work plus a dashboard.
- **Local wrappers and forks [cheap].** A wrapper is an app SFC whose template root is a single library component that forwards props/slots; a fork is an app SFC whose template is near-identical to a library SFC (a similarity heuristic, or the same prop names). Count per library component; two or more apps wrapping the same component is the strongest "pave this" signal.
- **Repeated prop combinations [cheap].** Group `raw-report` records by (component, prop-set, literal values); a combination appearing in 3+ places or apps is a candidate variant or preset. This relies on the raw-report capability above.
- **Escape-hatch props [cheap].** Have the SDK emit a dev/CI-only counter when an escape-hatch prop (`class`, `style`, an unstyled/`as` prop) is used; high use per component mirrors GitHub's per-component override rate.
- **Figma-side detach [org]** only if the SDK has a Figma library and an Enterprise plan; otherwise skip. A small team without Figma Enterprise gets nothing from the Library Analytics API.
- **Hosted tools.** Omlet is React-oriented (page headline and docs say React; no Vue statement found); do not assume Vue support, and ask the vendor before paying. react-scanner is React-only by description.
- **Noise control.** Ratio, not counts: overrides per instance, not raw overrides. Template-like components (designed to be customised) get an "expected" rate, as athenahealth does. Separate "intentional one-off" (a marketing page) from "repeated across apps".

### Gaps
- No primary source found for how Primer, Polaris, Atlassian, IBM Carbon or Spotify Encore detect snowflakes; only the second-hand GitHub/Amplitude/Productboard mentions from Omlet's blog. Brad Frost and Nathan Curtis primary material was not located.
- No Vue-capable scanner (Omlet, react-scanner, Radius Tracker) was confirmed; Omlet's and Radius's framework support is undocumented on the pages fetched.
- Whether Omlet uploads source code or only scan results: not stated.
- The zeroheight "measure the dev side" guide could not be fetched (connection reset), so its coverage/override advice is unreviewed.
- Prevalence and threshold numbers for "healthy" override or detach rates: none published beyond the qualitative statements above.
- The "passive inserts" caveat for Figma counts rests on a single Medium post.

## 4. How to decide what to pave: frequency x friction, cohorts, thresholds, vocal-minority risk

### Takeaway
Published thresholds are scarce: the one concrete number found is GOV.UK's "similar findings from 4 or more different services", paired with severity and a bias toward waiting for a clear body of evidence. Figma-side guidance is qualitative (investigate detach spikes on workhorse components; high detach is not always bad). Any frequency x friction score, cohort rule, or portfolio-scaled threshold below is a proposal, not a documented practice; evidence on the vocal-minority risk is practitioner opinion only.

### Cited Findings
- GOV.UK Design System team will usually investigate when it hears "similar findings from 4 or more different services", depending on the severity of the issue; it wants "a clear body of evidence", does not usually act on feedback immediately, fixes known issues first, and shares findings without a change on GitHub — [GOV.UK Design System, Share findings about your users (undated)](https://design-system.service.gov.uk/community/share-research-findings)
- GOV.UK prioritisation criteria for additions: used by the highest number of services or end users, reduces potential harm, appears in several departments' pattern libraries; evidence came from a community backlog and a two-week survey (302 responses: 131 complete, 171 partial); the post sets no numeric thresholds — [GDS Design in government blog, Ciandelle Scollan, 2022-09-07](https://designnotes.blog.gov.uk/2022/09/07/how-we-prioritise-additions-to-the-gov-uk-design-system/)
- Figma: prioritise high-use "workhorse" components and investigate detachment spikes first; a high detach rate can be intended; no formal frequency/impact model, no numeric thresholds — [Figma "Design systems 104", 2025-02-11](https://www.figma.com/blog/design-systems-104-making-metrics-matter/)
- athenahealth's loop: diagnostics, then user outreach, then implementation tickets, with a monthly review — [Figma "Design systems 104"](https://www.figma.com/blog/design-systems-104-making-metrics-matter/)
- Teams adding "expected" rates per component type avoids misreading designed-to-detach components — [Figma "Design systems 104"](https://www.figma.com/blog/design-systems-104-making-metrics-matter/); [Figma best practices](https://www.figma.com/best-practices/make-the-most-of-design-system-analytics/)
- Industry context: Sparkbox 2022 survey cited as "less than 16%" of teams tracking metrics; average internal-team DS adoption cited as "only 30%" — [Omlet blog 2023-01-10](https://omlet.dev/blog/data-driven-design-systems-in-practice/) (second-hand)
- Practitioner opinion (vendor blogs, low evidence): power users skew feedback (an e-commerce team added advanced filters for power users while new-user conversion fell, then removed features); a "60-70% of requests from 5-10% of users" figure is anecdotal; recommended mitigations are to segment by behavior, weight by who is asking, and treat a segment's silence as information — [Enterpret](https://www.enterpret.com/guides/the-5-ways-to-separate-power-user-feedback-from-everyone-elses); [Glance](https://thisisglance.com/learning-centre/should-i-listen-to-all-user-feature-requests-or-ignore-some)
- NN/g notes session-level search analysis must account for shared IPs (one identifier may be many people), a general caution against counting events as people — [NN/g 2017](https://www.nngroup.com/articles/search-log-analysis/)

### Inferences
Proposals (mine, not sourced as established practice):

- **Score.** `priority = breadth x frequency x friction / cost`, where breadth = distinct apps (or distinct users), frequency = occurrences per active user per week, friction = weight by signal (abandon or error > rage/dead click > override or detach > workaround mention), cost = estimated build effort in SDK days. Count distinct users and apps, never raw events, so one noisy user cannot dominate.
- **Threshold scaling.** GOV.UK's "4 or more" services scales to roughly 3-4 distinct apps out of ~30 for SDK-level paving, or a path used by a meaningful share of one app's active users for product-level paving. These cutoffs are my proposal; GOV.UK gives only the 4-services figure.
- **Rule of three.** The "three occurrences before abstracting" heuristic (from refactoring practice) is a common stand-in for a promotion threshold, but I could not find a design-system source for it; a search surfaced it only as an unverified commenter remark (unverified).
- **Cohort split.** Split signals into (a) first sessions or first week and (b) repeat users with N+ sessions. Friction that new users hit points to a design or discoverability fix; workarounds that only power users build point to shortcuts, bulk actions, or API/export paving. Pave only when the signal has breadth (multiple apps or a non-trivial user share), or both cohorts hit it.
- **Vocal-minority guard.** Require behavioral evidence (distinct users, repeated across sessions) next to every stated request; a request without a behavioral trace goes to a watch list, not the roadmap. GOV.UK's "slow down, build a body of evidence" stance is a precedent.
- **Time axis.** A path that persists across releases outranks a spike; check a spike against a deploy or campaign first (spikes can come from a bug, which Figma's athenahealth example attributes to bugs, not desire).
- **Cost tiers.** Scoring in a spreadsheet and a monthly review [cheap]; cohort queries on your own event table [mid]; formal prioritisation surveys like GOV.UK's [org].

### Gaps
- No published numeric thresholds for override, detach or workaround frequency beyond GOV.UK's 4-services rule.
- No documented frequency x friction scoring model from a design-system team (Figma's piece says it has none).
- Evidence on the vocal-minority risk is vendor blog opinion; no rigorous study found, and the quoted percentages are anecdotal.
- No source supports the "rule of three" as a design-system promotion rule.
- Wiesche et al.'s criteria for judging which workarounds merit incorporation could not be read (paywalled).
- Nathan Curtis / Dan Mall coverage discussions seen only via excerpts.

## 5. Privacy and consent-friendly analytics for small teams

### Takeaway
Cookieless, no-persistent-identifier tools (Plausible, Umami) cover page-level analytics with minimal personal data; PostHog and Clarity cover frustration signals and replay but need masking, consent handling and (for PostHog) a choice between Cloud and an officially unsupported self-host. Consent obligations depend on jurisdiction and exactly what is stored; the vendor claims below are not legal advice.

### Cited Findings
- Plausible uses no cookies, local storage or persistent identifiers; a daily-rotated salt hashed with domain, IP and User-Agent forms the visitor ID (salt deleted every 24 h, so no cross-day tracking); raw IP and UA are not stored; query parameters are dropped except campaign/referral ones; custom events and properties are supported; the vendor states no cookie banner or consent is needed for analytics (a vendor claim) — [Plausible data policy, last updated September 2026](https://plausible.io/data-policy)
- Plausible has an open-source self-hostable Community Edition; cloud plans start at $9/month for 10,000 pageviews; sources disagree on whether funnels need the Business tier — [Databuddy comparison, 2026](https://www.databuddy.cc/blog/plausible-vs-matomo-vs-privacy-first-analytics-2026) (vendor comparison; the author sells a competing product)
- Umami is open source with free self-hosting; sessions are hashed from site ID, IP and user agent with monthly and hourly salts instead of a stored cookie; supports custom events and `identify()`; one table marks its funnels cloud-only — [Databuddy, custom events without cookies](https://www.databuddy.cc/blog/custom-event-tracking-without-cookies) (vendor comparison)
- Matomo is the most feature-heavy (heatmaps, funnels) but runs on PHP + MySQL/MariaDB and uses cookies by default; a cookieless mode tracks less — [Databuddy comparison, 2026](https://www.databuddy.cc/blog/plausible-vs-matomo-vs-privacy-first-analytics-2026) (vendor comparison)
- PostHog privacy controls: elements matching `.ph-no-autocapture` / `[data-ph-no-autocapture]` are ignored; `element_attribute_ignorelist` drops attributes such as `aria-label`; form values and password-field clipboard are not captured; interaction autocapture can be turned off in settings or by `autocapture: false` — [PostHog autocapture docs](https://posthog.com/docs/product-analytics/autocapture.md)
- PostHog self-hosting is officially unsupported and limited to free-plan features; the vendor calls Cloud "far and away the best experience" for most — [PostHog self-host docs](https://posthog.com/docs/self-host)
- Clarity consent: from 2025-10-31 Clarity enforces consent signals for visits from the EEA, UK and Switzerland via Consent Mode; third-party guides describe `window.clarity("consent")` (enables cookie read/write, default) and `window.clarity("stop")` (blocks first-party cookies) — [Microsoft Learn, Clarity consent mode](https://learn.microsoft.com/en-us/clarity/consent-mode) (search-result excerpt); [Secure Privacy](https://secureprivacy.ai/blog/microsoft-clarity-consent-mode)
- Clarity masks sensitive fields by default and allows custom masking rules; the site owner, not Microsoft, is responsible for compliance — [CookieYes](https://www.cookieyes.com/blog/microsoft-clarity-gdpr/); [Secure Privacy](https://secureprivacy.ai/blog/microsoft-clarity-consent-mode) (third-party; they conflict on whether Clarity gathers anonymized cookieless data without consent)

### Inferences
- **Lowest-friction stack for a 1-2 person team with ~30 apps [cheap].** (1) First-party event endpoint through the SDK, no cookies, with a daily-rotating salted hash for session grouping (the Plausible pattern) and a fixed event vocabulary; (2) Plausible CE or Umami (self-hosted, one instance with a site per app) for pageviews and top pages; (3) search-query logging in your own backend; (4) frustration-click and replay review via Clarity or PostHog only on sampled or opt-in sessions, with strict masking.
- **PostHog.** Prefer Cloud over the unsupported self-host unless you accept maintaining it from `master`; for rage/dead clicks alone, events carry element selectors and do not need replay.
- **Free-text hazards.** Search queries and copied text can contain personal data; hash or redact, truncate, and set a short retention window. Do not enable `capture_copied_text` on screens that show customer data.
- **Consent.** If the stack stores nothing on the device and no personal identifier, many teams skip a banner (the Plausible vendor claim); anything with cookies or replay (Clarity default, Matomo default, PostHog persistence) needs a jurisdiction check. This is not legal advice.
- **Replay [mid to org].** Watching sessions is where the time cost lies; sample 10-20 flagged sessions a week rather than reviewing everything.

### Gaps
- Hotjar, FullStory and LogRocket privacy and masking docs were not reviewed.
- Umami, Matomo and Plausible CE are covered only through vendor-written comparisons (one vendor competes with all three) except Plausible's own data policy; official Umami and Matomo docs were not fetched.
- Clarity's cookieless-data behaviour: two third-party sources conflict; Microsoft's consent-mode page was only seen as an excerpt.
- PostHog EU data residency and its cookieless/memory-persistence mode were not verified.
- No legal or regulator sources (EDPB, ICO, CNIL) were consulted on whether cookieless counting needs consent.
- Free-tier quotas for Clarity were not confirmed from a primary source.
