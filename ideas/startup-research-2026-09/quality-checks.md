# Final quality checks

Checked 2026-09-28 against the final generated artifacts.

## Passed

- Four lane files contain exactly 250 ideas each, with contiguous unique identifiers W0001–W1000 and unique exact titles.
- All records have required fields and eight integer score dimensions between one and five. Weighted ratings were recomputed centrally.
- Each lane contains 40 complete researched dossiers. Every researched dossier references existing registered source IDs.
- The comparison cohort contains 300 ideas; the final set contains 100 researched ideas, ten exploratory selections, one representative per conservative family, and no lane-rejected candidate.
- The three suggested first comparisons W0252, W0012 and W0511 are retained. W0511 remains explicitly reserve. Demoted W0524 is outside the final 100.
- All lifetime/free records have no proposed monthly price. Customer counts use ceiling division by recurring price; one-time buyers do not count toward MRR.
- Hybrid alternatives display “or” rather than adding two prices. Original lane reserve decisions remain visible.
- The report's portfolio examples and operating-contribution arithmetic were checked independently.
- All relative Markdown file links resolve locally.
- A local Chromium render showed 100 default rows, 1,000 under the full-catalogue filter, working ID search, correct lifetime-MRR text and hybrid pricing alternatives.
- The browser produced no JavaScript runtime errors and no horizontal overflow at 390px width. Desktop 1440px and mobile 390px screenshots were visually inspected.

## What these checks cannot establish

Schema checks do not prove that ideas are commercially independent. Family labels are conservative editorial groupings and can miss overlap. Competitor pages and public anecdotes do not prove demand, available customer budget, acceptable acquisition cost, retention, margins or lawful use of every integration. No product implementation, production system or payment account was tested.

## Repository state

All work is under `ideas/startup-research-2026-09/` in the WoW2 meta-repository. Independent product repositories were not edited. Existing staged changes belong to other lanes; those entries were preserved. The research package was not staged, committed or pushed.
