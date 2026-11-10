"""Builds the SCFD console mock pages of this iteration: one frame, one function per page.

Run from this folder: python3 build.py, then render each .html with render-html.sh at 1440.
Two roles share one console: the operator (us) and a client (a subscriber's member).
The gallery follows Wheelhouse's Products page; a source follows Wheelhouse's product page.
"""
from pathlib import Path

OPERATOR_NAV = [
    ("Overview", [("Home", "")]),
    ("Collect", [("Sources", "12")]),
    ("Deliver", [("Subscribers", "1")]),
    ("System", [("Access", "")]),
]
CLIENT_NAV = [("Ocharo", [("Sources", "12"), ("Following", "2")])]

ICONS = {
    "site": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/>'
            '<path d="M3 12h18"/></svg>',
    "telegram": '<svg viewBox="0 0 24 24"><path d="M21 4 3 11l6 2 2 6 3-4 5 4z"/><path d="m9 13 8-6"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="5"/><circle cx="12" cy="12" r="4"/>'
                 '<circle cx="17" cy="7" r="1"/></svg>',
    "branch": '<svg viewBox="0 0 24 24"><path d="M4 10 12 4l8 6v10H4z"/><path d="M10 20v-6h4v6"/></svg>',
}


def icon(kind: str, extra: str = "") -> str:
    return f'<span class="ico {extra}" title="{kind}">{ICONS[kind]}</span>'


def view_switch(view: str) -> str:
    cards, rows = ("on", "") if view == "cards" else ("", "on")
    return f'<span class="seg"><span class="{cards}">&#9638; Cards</span><span class="{rows}">&#9776; Rows</span></span>'


def frame(active: str, crumb: str, body: str, client: bool = False, view: str = "", tree: bool = False,
          overlay: str = "") -> str:
    side = ""
    for group, items in CLIENT_NAV if client else OPERATOR_NAV:
        side += f'<div class="group">{group}</div>'
        for name, count in items:
            on = " on" if name == active and not tree else ""
            small = f"<small>{count}</small>" if count else ""
            side += f'<span class="nav{on}">{name}{small}</span>'
            if tree and name == "Sources":
                side += ('<span class="nav sub">Afisha</span>'
                         f'<span class="nav sub leaf on">{icon("site", "mini")} Afisha.uz</span>')
    switch = view_switch(view) if view else ""
    who = '<i>OM</i> Ocharo member' if client else '<i>TO</i> Test operator'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>SCFD console mock</title>
<link rel="stylesheet" href="mock.css"></head><body>
<div class="frame">
  <aside class="side"><div class="brand">SCFD <span class="chip">dev</span> <span class="chip">v0.1.14</span></div>{side}</aside>
  <main>
    <div class="bar"><span>&#9707;</span><span class="crumb">{crumb}</span><span class="grow"></span>{switch}
      <span class="avatar">{who} &#9662;</span></div>
    <div class="page">{body}</div>
  </main>
  {overlay}
</div></body></html>"""


def bars(values: list[int], height: int = 36) -> str:
    top = max(values) or 1
    cells = "".join(
        f'<i class="{"zero" if v == 0 else ""}" style="height:{max(3, round(v / top * height))}px"></i>' for v in values
    )
    return f'<span class="bars" style="height:{height}px">{cells}</span>'


def pill(text: str, kind: str = "") -> str:
    return f'<span class="pill {kind}">{text}</span>'


def plural(count: int, word: str) -> str:
    return f"{count} {word}{'' if count == 1 else 's'}"


def toggle(is_on: bool) -> str:
    return f'<span class="toggle{" on" if is_on else ""}"><i></i></span>'


SAMPLE = [0, 2, 0, 1, 3, 0, 0, 4, 1, 0, 2, 0, 5, 8]  # sample heights; Afisha's first real harvests ran on the last day
NONE = [0] * 14
HARVEST = pill("last harvest · <b>4</b> new of <b>23</b> found · partial", "warn")
NO_HARVEST = pill("no harvest yet", "muted")

# group -> (description, [(source name, channel kind, live?, trend)])
GROUPS = {
    "Afisha": ("Event listings across Uzbekistan.", [
        ("Afisha.uz", "site", True, SAMPLE), ("Afisha Telegram", "telegram", False, NONE),
        ("Afisha Instagram", "instagram", False, NONE)]),
    "Anons": ("Event announcements.", [("Anons.uz", "site", False, NONE), ("Anons Telegram", "telegram", False, NONE)]),
    "Uzexpocentre": ("Exhibition venue calendar.", [("uzexpocentre.uz", "site", False, NONE)]),
    "Craft fair": ("Craft fairs and markets.", [
        ("Craft fair site", "site", False, NONE), ("Craft fair Instagram", "instagram", False, NONE)]),
    "Teplo": ("A store with several branches.", [
        ("Teplo · branch 1", "branch", False, NONE), ("Teplo · branch 2", "branch", False, NONE)]),
    "CAEx": ("Exhibition venue calendar.", [("caex.uz", "site", False, NONE)]),
    "OLX": ("Classified listings.", [("olx.uz", "site", False, NONE)]),
}
TOTAL = sum(len(items) for _, items in GROUPS.values())


def toolbar(client: bool) -> str:
    filters = ('<span class="filter on">All 12</span><span class="filter">Following 1</span>' if client else
               '<span class="filter on">All 12</span><span class="filter">Harvesting 1</span>'
               '<span class="filter">Needs attention 0</span><span class="filter">Idle 11</span>')
    groups = "" if client else '<span class="btn">Groups</span>'
    return f'<div class="row"><span class="search">Search {TOTAL} sources</span>{filters}{groups}</div>'


def group_tiles() -> str:
    cards = ""
    for name, (about, items) in GROUPS.items():
        live = any(item[2] for item in items)
        trend = [sum(day) for day in zip(*(item[3] for item in items))]
        kinds = "".join(icon(kind, "mini") for kind in dict.fromkeys(item[1] for item in items))
        state = pill("<b>4</b> new in the last harvest", "warn") if live else NO_HARVEST
        cards += f"""<div class="card gcard"><div class="row"><b>{name}</b><span class="grow"></span>
  <small>{plural(len(items), "source")}</small></div>
  <div class="desc">{about}</div>
  <div class="row">{kinds}</div>
  <div class="row end">{state}<span class="grow"></span>{bars(trend, 26)}</div></div>"""
    return f'<div class="groups">{cards}</div>'


def group_head(name: str, count: int, is_open: bool = True) -> str:
    chevron = "&#9662;" if is_open else "&#9656;"
    return (f'<div class="ghead{"" if is_open else " shut"}"><span class="chev">{chevron}</span><b>{name}</b>'
            f'<small>{plural(count, "source")}</small><span class="rule"></span></div>')


def tile(name: str, kind: str, live: bool, trend: list[int], client: bool) -> str:
    times = "last harvest 13:12 · next 19:12" if live else "never harvested"
    if client:
        state = '<span class="tag">following</span>' if live else '<span class="btn sm">Follow</span>'
    else:
        state = f'<span class="tag{"" if live else " off"}">{"healthy" if live else "idle"}</span>'
    return f"""<div class="card tile{'' if live else ' quiet'}">
  <div class="row">{icon(kind)}<b>{name}</b><span class="grow"></span>{state}</div>
  <div class="desc">{times}</div>
  <div class="row end">{HARVEST if live else NO_HARVEST}<span class="grow"></span>{bars(trend)}</div></div>"""


def source_row(name: str, kind: str, live: bool, trend: list[int]) -> str:
    times = "last harvest 13:12 · next 19:12" if live else "never harvested"
    state = f'<span class="tag{"" if live else " off"}">{"healthy" if live else "idle"}</span>'
    return (f'<div class="lrow">{icon(kind, "mini")}<b>{name}</b><span class="desc">{times}</span><span class="grow"></span>'
            f'{HARVEST if live else NO_HARVEST}{state}{bars(trend, 22)}</div>')


def gallery(view: str, client: bool = False) -> str:
    sub = ("Every source you can follow, by publisher. Open one to choose its sections." if client else
           "The sources we can read, by publisher. Open one for its sections and posts.")
    body = f'<div class="stack"><div><h1>Sources</h1><p class="sub" style="margin:0">{sub}</p></div>' + toolbar(client)
    if not client:
        body += group_tiles()
    for index, (name, (_, items)) in enumerate(GROUPS.items()):
        is_open = view == "rows" or index < 4
        body += "<section>" + group_head(name, len(items), is_open)
        if not is_open:
            body += "</section>"
            continue
        if view == "cards":
            body += '<div class="tiles">' + "".join(tile(*item, client) for item in items) + "</div>"
        else:
            body += '<div class="glist">' + "".join(source_row(*item) for item in items) + "</div>"
        body += "</section>"
    if client:
        note = """<b>Mock, iteration 2, a client's view.</b> A member of a subscribing organization
signs in and sees the same gallery with one difference: Follow, or the state following. Their menu holds Sources and
Following only; nothing about subscribers, settings or access."""
    elif view == "cards":
        note = """<b>Mock, iteration 1, the operator's view.</b> Built as Wheelhouse's Products page: the group tiles
first, then one collapsible section per group with a rule beside its name. A group is a publisher: Afisha with its
website, Telegram and Instagram, or a store with its branches. The icon says how a source is read. A card shows the
last and next harvest under the name, one pill for what the last harvest found, and a 14-day chart at the bottom
right. The Cards and Rows switch sits in the top bar. Only Afisha.uz is real; the rest and the chart heights are
placeholders."""
    else:
        note = """<b>Mock, iteration 1, the operator's view.</b> The Rows view: each group keeps its own bordered
list, as Wheelhouse draws it."""
    body += f'<div class="note" style="margin-top:0">{note}</div></div>'
    crumb = "<b>Sources</b>" if client else "Collect &rsaquo; <b>Sources</b>"
    return frame("Sources", crumb, body, client, view)


def source_head(tab: str) -> str:
    tabs = "".join(
        f'<span class="tab{" on" if name == tab else ""}">{name}{f" <small>{count}</small>" if count else ""}</span>'
        for name, count in [("Overview", ""), ("Posts", "8"), ("Activity", "4"), ("Settings", "")]
    )
    return f"""
<div class="card hcard"><div class="row">{icon("site", "big")}<div><h1>Afisha.uz <span class="tag">healthy</span></h1>
<p class="sub" style="margin:0 0 8px">last harvest 13:12 · next 19:12</p>
<div class="pills"><span class="pill">&#9776; Afisha</span>{HARVEST}</div></div>
<span class="grow"></span><span class="btn">Open the site &#9662;</span><span class="btn go">Harvest now</span></div></div>
<div class="tabs">{tabs}</div>"""


def source_crumb(last: str = "") -> str:
    tail = f"Afisha.uz &rsaquo; <b>{last}</b>" if last else "<b>Afisha.uz</b>"
    return f"Collect &rsaquo; Sources &rsaquo; Afisha &rsaquo; {tail}"


def source_overview() -> str:
    body = source_head("Overview") + f"""
<div class="cols">
<div>
  <div class="card"><div class="pad" style="padding-bottom:6px"><h2>Sections being harvested</h2></div><table>
  <tr><th>Section</th><th>Harvests</th><th>Last</th><th>Next</th><th>Posts</th><th>Followed by</th></tr>
  <tr><td><b>Fashion</b></td><td>every 6 hours<br><small>checks daily</small></td>
    <td>13:12 <span class="tag warn">partial</span><br><small>5-page limit</small></td><td>19:12</td><td>4</td><td>1 subscriber</td></tr>
  <tr><td><b>Exhibitions</b></td><td>every 6 hours<br><small>checks daily</small></td>
    <td>13:12 <span class="tag">completed</span></td><td>19:12</td><td>4</td><td>1 subscriber</td></tr>
  <tr class="more"><td colspan="6"><span class="chev side-chev">&#9656;</span> 4 more sections nobody follows</td></tr>
  </table></div>
</div>
<div>
  <div class="card pad"><h2>Health</h2><div class="kv">
    <span>Reading pace</span><b>a page every 5 s</b>
    <span>Paused</span><b>no</b>
    <span>Failures in a row</span><b>0</b>
    <span>Last refusal</span><b>none</b></div></div>
  <div class="card pad" style="margin-top:20px"><h2>New posts, 14 days</h2>
    <div class="row end" style="margin-top:6px">{bars(SAMPLE, 96)}</div>
    <div class="row" style="margin-top:8px"><small>28 Oct</small><span class="grow"></span><small>today</small></div></div>
</div></div>
<div class="note"><b>Mock, iteration 1, the operator's view.</b> A source opens as a Wheelhouse product does: a
header card, then tabs, with the source under its group in the menu. Overview lists only the sections being
harvested; the rest fold into one closed line. Schedules are changed on Settings. Chart heights are samples.</div>"""
    return frame("Sources", source_crumb(), body, tree=True)


POSTS = [
    ("Показ мод The Fashion Show Line 2026", "event", "21 Nov 2026", "Fashion", "today 13:11"),
    ("Fashion article", "article", "", "Fashion", "today 13:12"),
    ("Fashion article", "article", "", "Fashion", "today 13:12"),
    ("Fashion article", "article", "", "Fashion", "today 13:12"),
    ("Exhibition listing", "event", "past", "Exhibitions", "today 13:12"),
    ("Exhibition article", "article", "", "Exhibitions", "today 13:12"),
    ("Exhibition article", "article", "", "Exhibitions", "today 13:12"),
    ("Exhibition article", "article", "", "Exhibitions", "today 13:12"),
]
POST_FILTERS = """<div class="row" style="margin-bottom:14px"><span class="search">Search this source's posts</span>
  <span class="filter on">All 8</span><span class="filter">Fashion 4</span><span class="filter">Exhibitions 4</span>
  <span class="filter">Events 2</span><span class="filter">Articles 6</span></div>"""

POST_MODAL = f"""<div class="veil"><div class="card modal">
  <div class="row"><h2 style="margin:0">Показ мод The Fashion Show Line 2026</h2><span class="grow"></span><span class="x">&#10005;</span></div>
  <div class="pills" style="margin:10px 0 14px">{pill("event", "on")}{pill("Fashion")}{pill("Afisha.uz")}</div>
  <div class="shots"><div class="thumb shot">post image 1 of 3</div>
    <div class="shot-col"><div class="thumb">2</div><div class="thumb">3</div></div></div>
  <div class="kv wide-kv"><span>Starts</span><b>21 Nov 2026, 17:00</b>
    <span>Place</span><b>Дворец творчества молодёжи, Ташкент</b>
    <span>Address</span><b>просп. Мустакиллик, 2</b>
    <span>Offers</span><b>1</b>
    <span>Posted</span><b>14 Oct 2026</b>
    <span>Harvested</span><b>today 13:11</b></div>
  <h3>Revisions</h3>
  <table class="plain"><tr><td><b>Revision 2</b></td><td>today 13:11</td><td>the city was added</td></tr>
    <tr><td><b>Revision 1</b></td><td>today 05:20</td><td>first harvest</td></tr></table>
  <p style="margin:18px 0 0"><span class="btn sm">Open the original</span> <span class="btn sm">See the capture</span></p>
</div></div>"""


def source_posts(view: str, modal: bool = False) -> str:
    if view == "rows":
        table = "".join(
            f'<tr class="{"sel" if modal and index == 0 else ""}"><td><b>{title}</b>'
            f'{"<br><small>" + when + "</small>" if when else ""}</td>'
            f'<td>{pill(kind, "on" if kind == "event" else "")}</td><td>{section}</td><td>{harvested}</td></tr>'
            for index, (title, kind, when, section, harvested) in enumerate(POSTS)
        )
        content = (f'<div class="card"><table><tr><th>Post</th><th>Kind</th><th>Section</th><th>Harvested</th></tr>'
                   f"{table}</table></div>")
        note = ("A post opens over the page, with no address of its own: its images, its facts, its revisions and the "
                "evidence. Images show inside SCFD only."
                if modal else "The Rows view lists every post with its kind, section and harvest time.")
    else:
        cards = "".join(
            f"""<div class="card pcard"><div class="thumb">post image</div>
  <div class="pills">{pill(kind, "on" if kind == "event" else "")}{pill(section)}</div>
  <b>{title}</b><div class="desc">{when or "no date"}</div></div>"""
            for title, kind, when, section, _ in POSTS
        )
        content = f'<div class="tiles four">{cards}</div>'
        note = "The Cards view shows each post as a tile with its first image."
    body = source_head("Posts") + POST_FILTERS + content + f"""
<div class="note"><b>Mock, iteration 1, the operator's view.</b> {note} The pool keeps posts of every kind; a
subscriber receives only its matches. Revisions show inside a post, not in the list. Titles other than the fashion
show are placeholders.</div>"""
    return frame("Sources", source_crumb("Posts"), body, view=view, tree=True, overlay=POST_MODAL if modal else "")


def source_activity() -> str:
    runs = [
        ("today 13:12", "Fashion", "harvest", '<span class="tag warn">partial</span>',
         "4 new of 23 found · stopped at the 5-page limit"),
        ("today 13:12", "Exhibitions", "harvest", '<span class="tag">completed</span>', "4 new of 26 found"),
        ("today 13:11", "Fashion", "refresh", '<span class="tag">completed</span>', "1 post changed: the city was added"),
        ("today 05:20", "Fashion", "harvest", '<span class="tag">completed</span>', "first harvest · 4 new"),
    ]
    table = "".join(
        f"<tr><td>{when}</td><td><b>{section}</b></td><td>{kind}</td><td>{state}</td><td>{found}</td></tr>"
        for when, section, kind, state, found in runs
    )
    body = source_head("Activity") + f"""
<div class="row" style="margin-bottom:14px"><span class="filter on">All 4</span><span class="filter">Needs attention 1</span>
  <span class="filter">Fashion 3</span><span class="filter">Exhibitions 1</span></div>
<div class="card"><table><tr><th>When</th><th>Section</th><th>Run</th><th>Result</th><th>What it found</th></tr>{table}</table></div>
<div class="note"><b>Mock, iteration 1, the operator's view.</b> A source's runs live on its Activity tab; the Runs
page is gone. A failure reads as a label and a sentence, and a refusal that pauses the source shows here and on
Health. Times before 13:11 are placeholders.</div>"""
    return frame("Sources", source_crumb("Activity"), body, tree=True)


def source_settings() -> str:
    sections = [("Fashion", True), ("Exhibitions", True), ("Concerts", False), ("Theatre", False),
                ("Festivals", False), ("For children", False)]
    rows = "".join(
        f'<tr><td><b>{name}</b></td><td>{toggle(is_on)}</td>'
        f'<td>{"<span class=select>every 6 hours &#9662;</span>" if is_on else ""}</td>'
        f'<td>{"<span class=select>daily &#9662;</span>" if is_on else ""}</td>'
        f'<td>{"<span class=select>5 pages &#9662;</span>" if is_on else ""}</td></tr>'
        for name, is_on in sections
    )
    body = source_head("Settings") + f"""
<div class="cols">
<div class="card"><div class="pad" style="padding-bottom:6px"><h2>Sections</h2>
  <p class="desc" style="margin:0">Turn a section on to harvest it. A section also turns on when a subscriber follows it.</p></div>
  <table><tr><th>Section</th><th>Harvest</th><th>Every</th><th>Check for changes</th><th>Stop after</th></tr>{rows}</table></div>
<div>
  <div class="card pad"><h2>Reading</h2><div class="kv">
    <span>Source</span><b>{toggle(True)} on</b>
    <span>Reading pace</span><b><span class="select">a page every 5 s &#9662;</span></b>
    <span>When refused</span><b>pause this source only</b>
    <span>Read from</span><b>our main server</b></div></div>
  <div class="card pad" style="margin-top:20px"><h2>AI</h2><div class="kv">
    <span>Read posts with AI</span><b>{toggle(False)} off</b>
    <span>Used for</span><b>relevance and a summary, later</b>
    <span>This month</span><b>0 posts</b></div></div>
  <div class="card pad" style="margin-top:20px"><h2>Group</h2><div class="kv">
    <span>Group</span><b><span class="select">Afisha &#9662;</span></b>
    <span>Reader</span><b>Afisha, from an adapter release</b></div></div>
</div></div>
<div class="note"><b>Mock, iteration 1, operators only.</b> This tab replaces the Pipelines page: what is harvested,
how often, how politely, and whether AI reads the posts. A subscriber never sees it. The AI card and the server line
are placeholders for later.</div>"""
    return frame("Sources", source_crumb("Settings"), body, tree=True)


def client_head(tab: str, matched: int) -> str:
    tabs = "".join(
        f'<span class="tab{" on" if name == tab else ""}">{name}{f" <small>{count}</small>" if count else ""}</span>'
        for name, count in [("Overview", ""), ("Posts", str(matched))]
    )
    return f"""
<div class="card hcard"><div class="row">{icon("site", "big")}<div><h1>Afisha.uz <span class="tag">following 2 sections</span></h1>
<p class="sub" style="margin:0 0 8px">last harvest 13:12 · next 19:12</p>
<div class="pills"><span class="pill">&#9776; Afisha</span>{pill("<b>1</b> matched for you in the last harvest", "on")}</div></div>
<span class="grow"></span><span class="btn">Open the site &#9662;</span><span class="btn">Following &#9662;</span></div></div>
<div class="tabs">{tabs}</div>"""


CLIENT_POSTS = [
    ("Показ мод The Fashion Show Line 2026", "event", "21 Nov 2026", "Fashion", "delivered today 13:20", True),
    ("Fashion article", "article", "", "Fashion", "not an event", False),
    ("Fashion article", "article", "", "Fashion", "not an event", False),
    ("Fashion article", "article", "", "Fashion", "not an event", False),
    ("Exhibition listing", "event", "past", "Exhibitions", "already past", False),
    ("Exhibition article", "article", "", "Exhibitions", "not an event", False),
    ("Exhibition article", "article", "", "Exhibitions", "not an event", False),
    ("Exhibition article", "article", "", "Exhibitions", "not an event", False),
]


def client_source_posts(show_all: bool) -> str:
    rows = ""
    for title, kind, when, section, result, matched in CLIENT_POSTS:
        if not matched and not show_all:
            continue
        state = (f'<span class="tag">{result}</span>' if matched else pill(f"not matched · {result}", "muted"))
        rows += (f'<tr class="{"" if matched else "dimmed"}"><td><b>{title}</b>'
                 f'{"<br><small>" + when + "</small>" if when else ""}</td>'
                 f'<td>{pill(kind, "on" if kind == "event" else "")}</td><td>{section}</td><td>{state}</td></tr>')
    matched_on, all_on = ("", " on") if show_all else (" on", "")
    note = ("All is on: every harvested post of the sections you follow, in the same list. The ones that did not match "
            "are dimmed and say why, so you can judge the filter without leaving the page."
            if show_all else
            "Matched is the default: only the posts delivered to you. The switch beside it adds the rest, dimmed.")
    body = client_head("Posts", 1) + f"""
<div class="row" style="margin-bottom:14px"><span class="search">Search this source's posts</span>
  <span class="seg"><span class="{matched_on.strip()}">Matched 1</span><span class="{all_on.strip()}">All 8</span></span>
  <span class="filter on">Both sections</span><span class="filter">Fashion</span><span class="filter">Exhibitions</span></div>
<div class="card"><table><tr><th>Post</th><th>Kind</th><th>Section</th><th>For you</th></tr>{rows}</table></div>
<div class="note"><b>Mock, iteration 2, a client's view.</b> {note} A client has no feed page; posts sit inside
each source it follows. Titles other than the fashion show are placeholders.</div>"""
    return frame("Sources", "Sources &rsaquo; Afisha &rsaquo; Afisha.uz &rsaquo; <b>Posts</b>", body, client=True, view="rows")


PAGES = {
    "sources": lambda: gallery("cards"),
    "sources-rows": lambda: gallery("rows"),
    "source-afisha": source_overview,
    "source-afisha-posts": lambda: source_posts("rows"),
    "source-afisha-posts-cards": lambda: source_posts("cards"),
    "source-afisha-post": lambda: source_posts("rows", modal=True),
    "source-afisha-activity": source_activity,
    "source-afisha-settings": source_settings,
    "client-sources": lambda: gallery("cards", client=True),
    "client-source-posts": lambda: client_source_posts(False),
    "client-source-posts-all": lambda: client_source_posts(True),
}

if __name__ == "__main__":
    for name, build in PAGES.items():
        Path(f"{name}.html").write_text(build())
    print("built", ", ".join(PAGES))
