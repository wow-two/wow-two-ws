# National Days — Project Seed

*Last updated: 2026-10-30*

> Every day in the developer's life OS ([10x OS](10x-os-domains-analysis.md)) shows which national days and
> observances fall on it. Saved by the developer on 2026-10-30 from
> [National Take Your Parents To Lunch Day](https://nationaltoday.com/national-take-your-parents-to-lunch-day/);
> the scope is the whole national-day concept, not that one day.
>
> **Status:** idea, saved only.
>
> **Next step:** pick the data source ([OQ-1](#open-questions)), then fold the module into the 10x OS analysis.

## Concept

- Each day carries its observances: name, emoji, category, country.
- Days resolve on the Tashkent date (GMT+5); the source runs on the US date.
- Example, 2026-10-29: 11 observances on National Today, among them National Cat Day, National Internet Day,
  Republic Day of Turkey and World Stroke Day.
- Example rule: Take Your Parents To Lunch Day falls on the 2nd Wednesday of October (2026-10-14, 2027-10-13).

## Fit in the 10x OS

| 10x OS domain | What national days add |
|---|---|
| #1 Calendar | an all-day observance row, beside `Holidays in Uzbekistan` and `Birthdays` ([Almanac](calendar-spec.md)) |
| #8 Brief | the morning brief names today's national days |
| #21 Dashboard shell | a "today is" widget on the day view |
| #3 Planning | optional: a chosen day proposes a block, e.g. `Lunch with parents - Family`; the user approves it in chat |

## Data model

Fields every National Today observance page carries:

| Field | Example |
|---|---|
| Name · emoji | National Take Your Parents To Lunch Day · 🥪 |
| Date rule | fixed (`October 29`), nth weekday (`2nd Wednesday of October`), last weekday (`last Friday of October`), lunar or religious (Karva Chauth) |
| Where | United States, Turkey, worldwide |
| Category | Animal, Federal, Food & Beverage, Fun, Health, Religious, Relationship, Special Interest |
| Tags | Appreciation, Children, Family |

- A date-rule resolver turns each rule into concrete dates per year.
- Lunar and religious rules need their own calendars, beyond Gregorian arithmetic.

## Source: National Today

Checked 2026-10-30 in the built-in browser.

- [`/today/`](https://nationaltoday.com/today/) lists the day's observances with categories; it showed October 29
  while Tashkent was on October 30.
- [`/national-today-calendar/`](https://nationaltoday.com/national-today-calendar/) counts 407–838 holidays per month
  (January–August seen); the counts probably include week- and month-long observances.
- Neither page links a feed, ICS file or API.
- Terms of use for reusing the data: untested.

## Open questions

- OQ-1: Source — National Today (scrape, terms untested), another dataset (untested), or a hand-curated list?
- OQ-2: Filter — show every observance (~11 a day), or only chosen categories and countries (Uzbekistan,
  worldwide, fun)?
- OQ-3: Actions — display only, or let a chosen day propose a calendar block?
