# Desire paths in web-app layout, navigation and interaction patterns

Scope: productivity / SaaS web apps. Researched 2026-10-27. Source quality is tagged inline: **[primary]** = the original paper, vendor docs or NN/g article that I fetched and read; **[snippet]** = only a search-result summary, page not read in full; **[secondary]** = blog or aggregator reporting someone else's finding; **[opinion]** = design-practitioner argument with no study behind it. Dates are given wherever the source shows one.

## 1. Command palettes (⌘K): origin, evidence, discoverability problems and fixes

### Takeaway
The palette is a paved desire path of "type what you want instead of navigating to it": it descends from Sublime Text's 2011 palette and was adopted by Superhuman, Linear, Slack, GitHub and VS Code. I found no controlled study of palettes themselves. The evidence is design guidance from builders, plus adjacent HCI research on hotkey learning showing that passive shortcut hints are mostly ignored. GitHub's 2025 near-removal of its palette for "low usage", then the reversal, shows the discoverability problem and the risk of reading low usage as low value.

### Cited Findings
- Sublime Text is generally credited with popularizing the command palette (Sublime Text 2 beta, 2011, fuzzy matching). It grew out of "Goto Anything", and Jon Skinner said the macOS menu-item search was a precedent. Cmd/Ctrl+Shift+P was a side effect of Sublime having no Print for a long time, which freed Ctrl+P. [snippet; not read in full] — [Digital Seams](https://digitalseams.com/blog/why-do-sublime-text-and-vs-code-use-ctrl-shift-p-for-the-command-bar); [command.ai history](https://command.ai/blog/command-palette-past-present-and-future); [techinch history](https://techinch.com/blog/the-history-of-command-palettes). I found no source documenting the origin of the Superhuman, Linear or VS Code palettes.
- Superhuman's post (Tim Boucher, Oct 12, 2021) names ⌘K as the shortcut in Superhuman, Linear and Slack, and ⌘⇧P in Sublime and VS Code. [vendor, primary] — [Superhuman blog](https://blog.superhuman.com/how-to-build-a-remarkable-command-palette/)
- The same post gives these design principles, all vendor assertions with no data attached:
  - A palette lets you add features that would never justify a button, so the UI stays uncluttered.
  - "Users prefer search to menus."
  - It doubles as a teaching tool: perform an action and "learn the shortcut for next time".
  - One shortcut should open it everywhere.
  - Each command gets a default score, so the palette is useful before typing. Ranking adapts to usage, tracking the last-used item in some lists such as labels, and boosts or hides commands by app context.
  - Add aliases and show the matched alias as "<title> (<alias>)".
  - Fuzzy matching must forgive typos.
  - Every action should be reachable from the palette: "treat each new UI element as a command, a shortcut, and a button".
  - Give each command an icon, partly for mobile.
  — [Superhuman blog](https://blog.superhuman.com/how-to-build-a-remarkable-command-palette/)
- VS Code's extension UX guidelines: command names decide whether users can find a command; group commands with a category prefix (example "GitHub Issues"); add keyboard shortcuts where appropriate and never overwrite existing ones; no emoji in names. [primary] — [VS Code UX guidelines](https://code.visualstudio.com/api/ux-guidelines/command-palette)
- GitHub shipped its palette as a public beta at Universe in Oct 2021 and added customizable shortcuts in Feb 2022. It stayed in beta about 3.5 years and off by default, enabled through Feature Preview. In Feb 2024 GitHub disabled it even for users who had enabled it. On Jul 16, 2025 GitHub announced removal on Aug 6 for "low usage", with no figures published. On Jul 21, 2025, after hundreds of posts of pushback (repo switching and keyboard-driven work), GitHub paused the removal. It promised no permanence, only availability while it explores navigation improvements. The article notes many users never discover it. [secondary, news report of GitHub's posts] — [The Register, Jul 22, 2025](https://www.theregister.com/2025/07/22/github_command_palette_backtrack/)
- Hotkey labels beside menu commands are "commonly ignored" because the user already has the command in hand once the menu is open. In a CHI 2007 study (Univ. of Toronto), two techniques raised hotkey use by over 100% and cut task time: audio feedback on menu selection, and disabling menu selection for commands that have a hotkey. Both are lab techniques that disrupt the primary task, not shippable defaults. [primary] — [Grossman, Dragicevic, Balakrishnan, CHI 2007](https://www.dgp.toronto.edu/~ravin/papers/chi2007_learninghotkeys.pdf)
- ExposeHK (CHI 2013) shows hotkeys overlaid on commands while a modifier key is held. Across three studies (toolbars, menus, ribbon), participants used more hotkeys, were faster and preferred it. The abstract also states that shortcuts are known to be infrequently used. [snippet] — [Malacria et al. via HAL](https://hal.archives-ouvertes.fr/hal-01894253)
- In a survey of 853 respondents, most said a social interaction led them to discover shortcuts; few cited computer aids such as tooltips. [snippet] — [HCI ISIR](https://hci.isir.upmc.fr/?p=196)
- A UBC thesis (GEKA) reports that advanced users prefer keyboard command entry but are often unable to use it because shortcuts are missing or unknown. [snippet] — [UBC thesis](https://circle.ubc.ca/handle/2429/17401)
- Linear: a 2019 changelog says the shortcuts page was redesigned and `?` opens it. [snippet] — [Linear changelog 2019-05-09](https://linear.app/changelog/2019-05-09-first-time-user-experience). A third-party 2026 breakdown credits Linear with hover-to-see-shortcut and single-letter shortcuts such as `C` for new issue. [opinion] — [925 Studios](https://www.925studios.co/blog/linear-design-breakdown-saas-ui-2026). Linear's own UI-redesign post (Mar 28, 2024) says nothing about the command menu or sidebar customization; its stated goal was to "reduce visual noise, maintain visual alignment, and increase the hierarchy and density of navigation elements". [primary] — [Linear, part II](https://linear.app/now/how-we-redesigned-the-linear-ui)
- NN/g Heuristic 7 (flexibility and efficiency): shortcuts "hidden from novice users" may speed up experts; provide accelerators such as keyboard commands. Originally 1994, reviewed Jan 30, 2024. [primary] — [NN/g heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)

### Inferences
- A palette is a power-user accelerator, not primary navigation. GitHub's off-by-default beta plus "low usage" is what a feature with no visible entry point looks like, and the pushback shows low usage can hide high value for a vocal expert minority.
- Because passive hint labels are ignored (Grossman 2007), the most reliable teaching moment in a shell is the one Superhuman uses: show the shortcut at the moment the user performs the action through the palette or a button. The `?` overlay and tooltip shortcut hints are cheap complements. Lab-proven disruptive techniques (disabling the menu) are not appropriate.
- A shell with ~30 apps gets most value if apps register commands into one shared palette (title, aliases, category, shortcut, context predicate), following the VS Code and Superhuman models. The shell should also reserve ⌘K and a visible button that opens it, so the entry point is not hidden.

### Gaps
- No peer-reviewed or published usage study of command palettes in web apps, and no adoption percentages from Linear, Slack or Superhuman. A vendor page claiming "up to 60%" faster navigation cites no method and was not used.
- Origin of the ⌘K convention (who used it first) is undocumented in what I found; the Sublime history above was not read from the full pages.
- Linear's own documentation of its command menu and shortcut design was not found.

## 2. Search-first vs. menus; recents, favorites/pins, "continue where you left off"; deep links and URL-encoded state

### Takeaway
Evidence that many users prefer search to browsing is real but old (Nielsen 1997: more than half of web users search-dominant). Superhuman repeats the claim as an assertion. I found no controlled evidence on pins, recents or "continue where you left off", and none beyond developer tutorials for URL-encoded state. The best support is indirect: NN/g's guidance on empty favorites/recents lists and on breadcrumbs.

### Cited Findings
- Nielsen (Jul 14, 1997): "more than half of all users" were search-dominant, about a fifth link-dominant, the remainder mixed. The article gives no sample size or method, and the finding is about 1990s websites. [primary, dated] — [NN/g, Search and You May Find](https://www.nngroup.com/articles/search-and-you-may-find/)
- Superhuman asserts "Users prefer search to menus" and builds ranking around recency (last-used items) and context. [vendor] — [Superhuman blog](https://blog.superhuman.com/how-to-build-a-remarkable-command-palette/)
- NN/g's guidance on empty states in complex applications (Kate Kaplan, Sep 19, 2021) treats empty favorites and empty recent-files lists as common cases and gives an example from DataDog: "Star your favorites to list them here". It also notes Power BI's empty recent-items screen explains how content gets added. [primary] — [NN/g empty states](https://www.nngroup.com/articles/empty-state-interface-design/)
- NN/g on breadcrumbs (Dec 23, 2018, reviewed Sep 1, 2026): they show position in the site hierarchy, not session history. Breadcrumbs help most on deep pages and for users arriving from external links, and they add nothing on flat one- or two-level hierarchies or linear flows. The article offers no quantitative study, only design reasoning. [primary] — [NN/g breadcrumbs](https://www.nngroup.com/articles/breadcrumbs/)
- NN/g (Sep 7, 2015) lists "reduce memory burdens by showing the context users need to resume tasks" among error-prevention practices. [primary] — [NN/g, Preventing User Errors](https://www.nngroup.com/articles/user-mistakes/)
- URL-as-state: guidance from dev tutorials and libraries recommends putting filters, sort, search text, pagination and tabs in query parameters, so views can be bookmarked and shared and so back/forward restores state. Use replace-style updates so each filter change doesn't flood history. For long, complex or sensitive state, store it server-side and put only an ID in the URL. [secondary and opinion; no study] — [nuqs setup recipe](https://playbooks.com/skills/andrelandgraf/fullstackrecipes/nuqs-setup); [Pattern Playground, shareability](https://pattern-playground.onrender.com/patterns/shareability); [DEV Community](https://dev.to/prabhu66/persisting-and-sharing-your-applications-state-local-url-and-beyond-4527)
- NN/g's study of "The Legacy" user type found that such users build workarounds such as bookmarks and manual processes (Jun 27, 2025). That is a desire-path signal for deep links and saved views. [primary] — [NN/g, complex-app user types](https://www.nngroup.com/articles/complex-apps-users/)

### Inferences
- Treating search and a command palette as the fast route, with a visible sidebar as the structural route, matches both the old search-dominant data and current product practice, without needing either to be the only path.
- URL-encoded view state is cheap to standardize in a shell (one composable), and its justification is the bookmark and share workaround NN/g observed in Legacy users. The strongest argument is cost, not measured benefit.
- Recents and pins should follow NN/g's empty-state pattern: an explanation of how items get added, rather than a blank list.

### Gaps
- No empirical study found on pins, favorites, recents, or "resume where you left off" in SaaS.
- No NN/g or Baymard study on URL-encoded state or deep links; the URL-state claims are practitioner guidance.
- Slack's Quick Switcher and Notion's recents were not researched in primary sources.

## 3. Inline editing, bulk actions and multi-select, drag-and-drop, optimistic UI and undo, keyboard shortcut discoverability

### Takeaway
The strongest evidence in this lane is for undo over confirmation (Raskin 2007, NN/g 2015, Gmail Undo Send) and for drag-and-drop needing signifiers plus a non-drag alternative (NN/g 2020). Inline editing and bulk actions rest on design-system guidance, not studies. I found no study on optimistic UI.

### Cited Findings
- Raskin (A List Apart, Jul 21, 2007): users form habits and click OK on reflex, so making warnings louder only gets them dismissed faster. His rule: "Never use a warning when you mean undo". He praises Gmail's undo-after-delete and criticizes Google Calendar and Highrise for warnings without undo. He does not address truly irreversible actions; reader comments raise collaborative editing, undo depth and sensitive-data deletion as unresolved. [primary, opinion essay] — [A List Apart](https://alistapart.com/article/neveruseawarning/)
- NN/g (Laubheimer, Sep 7, 2015): undo is a safety net that makes errors less costly and encourages experimentation. Confirmation is recommended before destructive actions like deletion, but frequent confirmations teach click-through and can raise errors. Do not rely on confirmation as the sole error prevention. It cites Gmail's undo-send, up to 30 seconds. [primary] — [NN/g](https://www.nngroup.com/articles/user-mistakes/)
- Gmail Undo Send launched as a Gmail Labs experiment on Mar 19, 2009 with a 5-second window. It was promoted out of Labs in Jun 2015. Sources disagree on the post-2015 window: one says 10 seconds, another says default 10 with 5 or 30 selectable, and one says the setting is off by default. [primary for 2009, secondary for 2015] — [Gmail Blog, Mar 2009](https://gmail.googleblog.com/2009/03/new-in-labs-undo-send.html); [The Next Web, Jun 23, 2015](https://thenextweb.com/google/2015/06/23/gmails-undo-send-feature-finally-graduates-out-of-labs-after-six-years/); [PCWorld](https://www.pcworld.com/article/428203/google-finally-makes-undo-send-an-official-gmail-feature.html)
- Secondary decision-framework pieces say confirmation still fits genuinely irreversible, infrequent actions, and that actions that send data to systems the user does not control can make undo impossible. [opinion/secondary] — [DEV Community](https://dev.to/137foundry/how-to-choose-between-confirmation-dialogs-undo-windows-and-soft-delete-patterns-1opj)
- NN/g Heuristic 3 requires undo and redo and a clearly marked exit. [primary] — [NN/g heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- Drag-and-drop (NN/g, Laubheimer, Feb 23, 2020):
  - Needs signifiers for grabbability and for what the drag will do.
  - Grab-handle icons are not universal and can resemble menu icons.
  - Use ~100 ms animated reshuffle with easing, triggered when the dragged object's center crosses an edge.
  - Provide keyboard operation (Tab to focus, Space to grab, arrows to move) and screen-reader announcements.
  - Drag is inefficient, imprecise and tiring over long distances.
  - On touch, use it only when users expect it and no cheaper alternative exists; the article's example is Gmail replacing drag with a menu on mobile.
  [primary] — [NN/g](https://www.nngroup.com/articles/drag-drop/)
- Inline edit (PatternFly): use when all editable elements are visible in the row and the data is updated frequently; use field-level edit for small edits to specific fields; use row edit only when rows are independent. Do not use it when editing is the primary function of the view, or when elements are hard to edit inside a table (use a modal). Save is a check icon and cancel a close icon. The page does not cover validation, bulk editing or keyboard behavior. [primary, design-system doc] — [PatternFly](https://www.patternfly.org/components/inline-edit/design-guidelines). Cloudscape and SAP Fiori describe equivalent in-cell patterns with confirm/dismiss icons and display/edit modes. [snippet] — [Cloudscape](https://cloudscape.design/patterns/resource-management/edit/inline-edit/)
- Bulk actions: practitioner pieces recommend always-visible row checkboxes with bulk controls appearing once rows are selected, note that hidden selection mechanisms cost discoverability, and suggest a floating action bar because a crowded top bar is easy to miss. [opinion/snippet] — [UX Collective, The bulk experience](https://uxdesign.cc/the-bulk-experience-7fcca8080f82); [SaaS UI](https://www.saasui.design/blog/saas-bulk-actions-ux-patterns)
- Keyboard shortcut learning: see Section 1 (Grossman 2007; ExposeHK 2013). Lane et al. (2006) reportedly found experienced users rarely used efficient shortcuts and favored icon toolbars; I only saw this in a course slide deck. [secondary/snippet] — [LMU course slides](https://www.medien.informatik.uni-muenchen.de/lehre/ws1415/mmi2/slides/desktop3.pdf)

### Inferences
- Default destructive flows to "do it, then offer undo" (a toast with a timer) wherever the action is reversible in the data layer, and keep confirmation for irreversible or external side-effect actions. This follows Raskin plus NN/g, with the caveat that collaborative and sensitive-data cases need case-by-case judgment.
- A shell-level undo/toast service is a natural standard component, since every one of ~30 apps would otherwise reimplement it.
- Drag-and-drop in the shell should ship with the keyboard alternative and a non-drag path (move-to menu) by default, per NN/g.
- Inline edit should be a table-cell/field-level default for single-field changes and not used for multi-field records (PatternFly's guidance).

### Gaps
- No study on optimistic UI (perceived speed vs failure confusion); not found in the sources checked.
- No controlled evidence on multi-select/bulk-action placement; findings are practitioner opinion.
- No data on how often users actually use inline editing vs edit pages.

## 4. Defaults and empty states: smart defaults, remembering the last choice, prefilled forms, templates

### Takeaway
NN/g's long-standing finding is that users stick with defaults and rarely customize, so the default experience is what matters (2005). Prefilling a returning user's own data is low-risk and widely recommended; pre-selecting a choice on their behalf needs an easy override. NN/g's 2021 empty-state guidance gives three concrete jobs for empty states: status, learning cue, direct pathway.

### Cited Findings
- NN/g, "The Power of Defaults" (Sep 25, 2005): "people tend to stick to the defaults"; users rarely use customization features, so optimize the default experience. Supporting number from a Cornell search-results study: 42% clicked the top hit and 8% the second; with the top two secretly swapped, the originally-first hit still drew 34% and the new first drew 12%. Pre-populate with the most common predictable value; choose defaults that teach the expected input; avoid always defaulting to the most expensive option. [primary, dated] — [NN/g](https://www.nngroup.com/articles/the-power-of-defaults/)
- NN/g empty states (Sep 19, 2021): (1) communicate system status: a blank panel leaves users unsure whether it is loading, failed or empty, and "No records" must not flash while content loads; (2) act as learning cues in context, which is easier to apply than a forced tutorial; (3) give direct pathways to key tasks, for example a Create button on an empty alerts panel, or "add log sources or load demo data". [primary] — [NN/g](https://www.nngroup.com/articles/empty-state-interface-design/)
- NN/g Heuristic 5: avoid slips with helpful constraints and good defaults. [primary] — [NN/g heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- Yale usability guidance: pre-populate forms with information the system already has and offer autocomplete from previous entries. [secondary, institutional guidance] — [Yale UX](https://usability.yale.edu/ux/best-practices/memory-free-interaction)
- Box UK distinguishes "member" defaults (fill from a returning user's existing details) from "smart" defaults (what most users pick), and says users should always be able to override defaults. [secondary, agency white paper] — [Box UK PDF](https://www.boxuk.com/wp-content/uploads/2019/08/Five_Ways_to_Improve_Web_Forms_in_the_Membership_Sector.pdf)
- Caution on pre-selected values: users tend to leave them, so use a static default only when a large share would choose it; "there is no neutral pre-selection". [opinion/secondary] — [Ferguson EDEX wiki](https://fergusonprod.atlassian.net/wiki/spaces/EDEX/pages/146999064/Use+Default+Values+Cautiously); [UX Collective, Default bias](https://uxdesign.cc/default-bias-who-chose-your-settings-d2acde25551b)
- Persistent defaults based on past choices ("use my last address") are cataloged as a pattern. [opinion/snippet] — [Pattern Playground](https://pattern-playground.onrender.com/patterns/good-defaults)
- Learner users benefit from "sandboxes or templates for low-risk exploration" and just-in-time tips (NN/g, Jun 27, 2025). [primary] — [NN/g complex-app user types](https://www.nngroup.com/articles/complex-apps-users/)

### Inferences
- "Remember the last choice" is a defensible default for per-user preferences (sort, view mode, last-used filter, last-selected workspace), because users rarely customize. It should be reflected in the UI so it is not a hidden change, which ties to the self-rearranging-UI risks in Section 6.
- A shared empty-state component with slots for status message, explanation and primary action implements all three NN/g jobs once for ~30 apps.
- Templates and sample data are a first-run pathway (Loggly-style demo data, NN/g Learner guidance).

### Gaps
- No quantitative study found specifically on "remember last choice" or on templates.
- The NN/g Cornell figures concern search-result position bias in 2005, not form defaults; they illustrate default bias generally.
- The sources on form defaults are mostly secondary or opinion.

## 5. Navigation structure evidence: sidebar vs. top nav, number of top-level items, breadcrumbs, tabs, mobile bottom nav; NN/g, Baymard, Jakob's law

### Takeaway
For desktop apps with many or growing sections, NN/g favors visible left-rail vertical navigation, tolerates 7–9+ top-level categories, and says to avoid hiding desktop navigation. NN/g's 179-participant study shows hidden navigation reduces use and discoverability. On mobile, show 4–5 items visibly; beyond that, hidden or "More" navigation is a trade-off. Jakob's Law supports reusing conventions users know from other tools.

### Cited Findings
- NN/g hamburger study (Pernice and Budiu, Jun 26, 2016): 179 participants, 6 live sites, desktop and mobile. Desktop navigation use was 27% when hidden, 48% visible and 50% combo; mobile 57% hidden, 86% combo. Hidden navigation cut content discoverability by more than 20% on both devices, was rated 21% harder than visible (2.6 vs 2.1 on a 1–7 scale), and desktop hidden-navigation tasks took at least 39% longer. Desktop recommendation: avoid hidden navigation. Mobile: with 4 or fewer top-level links show them; with more, hiding some is a reasonable trade-off. [primary] — [NN/g](https://www.nngroup.com/articles/hamburger-menus/)
- NN/g mobile navigation patterns (Budiu, Nov 15, 2015): tab and nav bars suit relatively few options; more than 5 is hard with adequate touch targets; with 4–5 main options showing them all can make sense; a hamburger menu is the least discoverable but holds many options. [primary] — [NN/g](https://www.nngroup.com/articles/mobile-navigation-patterns/)
- NN/g vertical navigation (Laubheimer, May 16, 2021):
  - Fits many top-tier categories without crowding, and is easy to extend.
  - Scans efficiently: visual search in vertical lists needs fewer eye fixations than horizontal.
  - Users look at the left half of the screen 80% of the time (cited eye-tracking).
  - Familiar from Slack and Gmail.
  - Costs horizontal space: the article's example is a content-to-chrome ratio of about 5:1 vs 12:1.
  - Suited to B2B, enterprise and other broad or fast-growing content.
  - More than 7–9 categories is acceptable if planned; use text labels not icons alone, keep it visible, and don't duplicate it horizontally.
  [primary] — [NN/g](https://www.nngroup.com/articles/vertical-nav/)
- Breadcrumbs: NN/g (Dec 2018) recommends them on deep hierarchies as a supplement to, not a replacement for, global navigation, and says on mobile "the cost of using breadcrumbs can quickly overwhelm the benefits". [primary] — [NN/g](https://www.nngroup.com/articles/breadcrumbs/). Baymard's mobile research says breadcrumbs matter more on phones because navigation is hidden, and 36% of mobile sites that have breadcrumbs omit the full hierarchy on product pages. That is e-commerce data. [snippet] — [Baymard](https://baymard.com/blog/implementing-mobile-hierarchy-breadcrumbs)
- Jakob's Law: users spend most of their time on other products and expect yours to work like those they know; keep the old version available temporarily when changing. [secondary summary of Nielsen's law] — [Laws of UX](https://lawsofux.com/jakobs-law/). NN/g's error-prevention article also cites it as "follow design conventions". [primary] — [NN/g](https://www.nngroup.com/articles/user-mistakes/)
- Material/M3 thresholds as relayed by SAP Fiori for Android (which extends M3): navigation bar for 2–5 destinations on compact windows; navigation rail for 3–7 destinations on medium and larger; drawer for 5+; one page says the drawer is being deprecated in favor of an expanded rail with M3 Expressive. [secondary, not official Material docs] — [SAP Fiori Android, navigation bar](https://www.sap.com/design-system/fiori-design-android/v26-4/components/m3-standard-components/navigation-bar/usage)
- Opinion: Smashing Magazine (Jan 2010) argued against vertical navigation, saying dropdown submenus work better in horizontal bars. Dated and opinion; NN/g's 2021 evidence points the other way for broad apps. [opinion] — [Smashing Magazine](https://smashingmagazine.com/2010/01/the-case-against-vertical-navigation)

### Inferences
- A left-rail vertical nav with visible text labels is the best-supported default for a shell hosting many apps, because it extends without redesign and avoids the hidden-navigation penalty. At narrow widths it should collapse to a bottom bar (≤5 items, as in Material and NN/g) with a visible "More".
- The shell should keep the per-app top-level count at or below roughly 7–9 on desktop (NN/g's tolerance) and ≤5 on mobile; anything beyond belongs behind search or the palette.
- Breadcrumbs belong only in apps with three or more levels, and are optional or reduced to the parent link on mobile.
- Jakob's Law argues for the shell borrowing known conventions (Slack/Gmail-style left rail, ⌘K, familiar shortcut keys) rather than inventing layouts.

### Gaps
- The Apple HIG tab-bar page and the official Material 3 navigation pages are JavaScript-rendered and could not be read; the thresholds above come from SAP's M3 extension and NN/g. Apple's guidance is not verified here.
- I found no Baymard research on vertical or bottom navigation specifically. A claim attributed to Baymard (Jan 2026) that hamburger menus reduce navigation discovery by 38% came from a design blog and could not be verified, so I did not use it.
- NN/g's tests were on content sites, not productivity SaaS; no study directly compares sidebar and top nav in a SaaS app.
- NN/g's original Jakob's Law page returned 404, so that law is cited via Laws of UX.

## 6. Adaptive (system changes UI from usage) vs. adaptable (user customizes) interfaces

### Takeaway
The controlled evidence favors user-controlled (adaptable) personalization over system-rearranged (adaptive) UIs: a CHI 2004 lab study found adaptive menus slower than static and less preferred. Adaptive wins only when it substantially shortens the path to an item, when screen space is tight, or when prediction accuracy is high and spatial stability is kept. Two caveats: few users customize at all, and Microsoft publicly abandoned its adaptive menus.

### Cited Findings
- Findlater and McGrenere, CHI 2004 (27 subjects, split menus whose top four items were fixed, user-chosen or system-chosen by frequency and recency). The static menu was significantly faster than the adaptive menu; the adaptable menu was significantly faster than the adaptive menu in some orders and not significantly different from static. Preference for first place: 15 adaptable (55%), 8 adaptive (30%), 4 static (15%). Most frustrating: 15 adaptive, 10 static, 1 adaptable. Six participants commented on the inconsistency of adaptive menus. The authors argue user-driven customization is a more viable approach than automatic adaptation. [primary] — [Findlater and McGrenere 2004](https://www.cs.ubc.ca/labs/edapt/papers/findlater2004.pdf)
- Same paper, caveats: 5 of 27 never customized, and 4 of those 5 were given the adaptable condition first, so some users do not see the value of customizing even with an easy mechanism; showing examples helped. Perceived and measured efficiency diverged: most subjects felt most efficient with adaptable, even though they were slower than static in one order. Related work it cites: in the field, Mackay found customization is minimal because of time, difficulty and lack of interest; a field study by McGrenere et al. on Word 2000 found 65% preferred an adaptable interface, 15% adaptive, 20% asked for static. Greenberg and Witten found an adaptive structure faster than static when it shortened the search path (a phone directory). [primary] — [Findlater and McGrenere 2004](https://www.cs.ubc.ca/labs/edapt/papers/findlater2004.pdf)
- Findlater et al., CHI 2009 (two experiments, 48 users): spatially adaptive interfaces are often not faster than static ones because users must keep re-adapting to the altered layout, wiping out gains. Successes occurred mainly when adaptation greatly reduced steps (a hierarchical menu) or limited screen space forced scrolling. "Ephemeral adaptation" (predicted items appear immediately, others fade in) kept spatial consistency: faster than static at high accuracy (79%) and not significantly slower at low accuracy (50%). [primary] — [Findlater et al. 2009](https://www.cs.ubc.ca/labs/edapt/papers/findlater2009.pdf)
- Gajos et al., CHI 2008 extended abstract: raising both predictability and accuracy of an adaptive interface improved satisfaction, and accuracy mattered more than predictability for performance and utilization. [snippet of abstract; paper body not read] — [Harvard, Gajos 2008](https://www.eecs.harvard.edu/~kgajos/papers/2008/gajos08predictability.shtml)
- Microsoft Office 2000–2003 "adaptive menus" (hidden rarely used items). Jensen Harris is reported to have said that when a menu item was hidden, users had to rescan the whole list, menus varied from person to person, and items vanished after a vacation; Office 2007 had a design tenet "Don't do adaptive behaviors", and the adaptive menus were dropped. These are Harris's statements relayed by journalists; his original post (linked from the second source) was not retrievable. [secondary] — [itwriting.com, Dec 3, 2006](https://www.itwriting.com/blog/68-what-happened-to-smart-tags-in-office-2007-and-is-the-ribbon-next.html); [Computerworld](https://www.computerworld.com/article/1707017/gui-gaffes.html)
- The Computerworld piece quotes Don Norman on why inferring user intent is hard, and says Intellimenus increased confusion. [secondary, opinion-adjacent] — [Computerworld](https://www.computerworld.com/article/1707017/gui-gaffes.html)
- A practitioner post argues personalization can narrow variety and reduce exploration. [opinion] — [LogRocket](https://blog.logrocket.com/ux-design/adaptive-interfaces-risks/)
- NN/g's Legacy users "stick to defaults and avoid customization", and Legends "customize workflows" (Jun 27, 2025). NN/g's Heuristic 7 lists both personalization and customization. [primary] — [NN/g complex-app user types](https://www.nngroup.com/articles/complex-apps-users/); [NN/g heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- NN/g (2005): users rarely use customization features. [primary] — [NN/g, Power of Defaults](https://www.nngroup.com/articles/the-power-of-defaults/)

### Inferences
- For a shared shell, the evidence supports a layered approach. Keep the primary navigation static and predictable. Make personalization user-controlled and additive: pins or favorites the user explicitly sets, and a separate recents list that does not reorder the main nav. Let adaptive ranking live in places where position is not memorized and the list is re-sorted from scratch anyway, such as palette results and search suggestions (as Superhuman describes).
- Because most users never customize (Mackay, NN/g 2005), adaptable features must be backed by good defaults, and guiding users with examples or suggestions lifts uptake (Findlater 2004).
- The lab results are from small menus and short sessions (a 2004 desktop study); the 2009 work says gains appear only under specific conditions. They are consistent with Microsoft's reversal, but no study of rearranging sidebars in modern SaaS was found.

### Gaps
- No recent (post-2015) controlled study of adaptive navigation in web SaaS found.
- The Gajos 2008 body, effect sizes and methods were not read, only the abstract.
- Harris's original post was inaccessible, so the Office adaptive-menu rationale is secondhand.
- Nothing quantifies how many users actually pin, reorder or customize sidebars in current products.

## 7. How desire paths differ by user type: novice vs. expert, mobile vs. desktop, internal tools vs. consumer apps

### Takeaway
NN/g's 2025 research reframes novice vs. expert as three complex-app user types, Legacy, Legend and Learner, each with different workarounds. Mobile users lean more on visible navigation. I found no study that compares internal tools against consumer apps; the only support is NN/g's secondhand "generalized vs. complex apps" framing.

### Cited Findings
- NN/g, "Supporting 'Power Users' Isn't Enough" (Kate Kaplan, Jun 27, 2025):
  - Legacy: long-term users who never became efficient, mistaken for power users. They stick to defaults, avoid customization, use a narrow feature set and build workarounds such as bookmarks and manual processes. Needs: predictable workflows, early notice of changes, legacy views kept during transitions, and easily discoverable time-saving shortcuts.
  - Legend: expert, uses shortcuts, macros and accelerators and customized workflows. Risk: over-prioritizing their feedback adds complexity for everyone, and they may leave for faster tools.
  - Learner: domain expert new to the software; needs onboarding, inline help, just-in-time tips, sandboxes or templates.
  - These groups are not fixed; a Learner can become a Legend or a Legacy depending on design support.
  [primary] — [NN/g](https://www.nngroup.com/articles/complex-apps-users/)
- NN/g Heuristic 7: shortcuts should be hidden from novices but accelerate experts. [primary] — [NN/g heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- Hotkey research: label hints are ignored by users who already have the command in hand (Grossman 2007); the survey of 853 found most shortcut discovery was social, not through UI aids (see Section 1). [primary / snippet]
- Mobile vs desktop: in NN/g's 2016 study participants used navigation more on mobile than desktop (hidden: 57% mobile vs 27% desktop), and hiding navigation hurt discoverability more on desktop, though the device difference was not statistically significant. Mobile tasks overall took about 12% longer. [primary] — [NN/g](https://www.nngroup.com/articles/hamburger-menus/)
- NN/g on drag-and-drop: on touch devices use it only when users expect it and no cheaper alternative exists. [primary] — [NN/g](https://www.nngroup.com/articles/drag-drop/)
- Internal vs consumer: a secondary source quoting NN/g describes generalized apps as serving nonspecialized users with discrete, linear tasks, and complex apps as serving trained users with specialized knowledge managing large data sets. A design agency argues power users prefer dense interfaces and that consumer-style simplicity can fail in complex tools. NN/g also advises accepting an ecosystem of tools and designing connection points such as export to Excel. [secondary/opinion] — [NN/g, What Is a Complex Application?](https://www.nngroup.com/articles/complex-application-design/); [EWM, designing complex interfaces for experts](https://ewm.swiss/en/blog/designing-complex-interfaces-experts)
- NN/g's vertical-nav article recommends the pattern for B2B, enterprise, government, higher-ed and healthcare. [primary] — [NN/g](https://www.nngroup.com/articles/vertical-nav/)

### Inferences
- The shell should serve all three NN/g types: shortcuts and palette for Legends, no forced layout changes and discoverable time-savers for Legacy users, and learnability aids (empty states, templates, inline help) for Learners. Visible shortcut hints in menus and tooltips serve the Legacy group.
- Because most users do not discover shortcuts on their own, a small-app portfolio where each app is used occasionally leans toward Learner and Legacy behavior (low per-app expertise), so default visible navigation and good empty states matter more than expert accelerators. This is an inference, not a measured finding.
- Mobile web variants should favor visible bottom navigation and menu alternatives over drag-and-drop or hover-dependent patterns.

### Gaps
- No direct study comparing desire paths in internal tools versus consumer apps; the NN/g framing was seen only through a secondary summary.
- The NN/g podcast on B2B and enterprise digital misery was seen only as a description.
- No usage data on mobile versus desktop use of shortcuts or palettes in productivity SaaS.
- Little data on how expertise accrues across a portfolio of ~30 small apps sharing one shell, an open question for the team.
