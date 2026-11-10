"""Builds the SCFD console mock pages of this iteration: one frame, one function per page.

Run from this folder: python3 build.py, then render each .html with render-html.sh at 1440.
Two roles share one console: the operator (us) and a client (a subscriber's member).
The gallery follows Wheelhouse's Products page: group tiles, then a collapsible section per group.
"""
from pathlib import Path

OPERATOR_NAV = [
    ("Overview", [("Home", "")]),
    ("Collect", [("Sources", "12"), ("Activity", "")]),
    ("Clients", [("Clients", "1")]),
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


def frame(active: str, crumb: str, body: str, client: bool = False, view: str = "") -> str:
    side = ""
    for group, items in CLIENT_NAV if client else OPERATOR_NAV:
        side += f'<div class="group">{group}</div>'
        for name, count in items:
            on = " on" if name == active else ""
            small = f"<small>{count}</small>" if count else ""
            side += f'<span class="nav{on}">{name}{small}</span>'
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
        note = """<b>Mock, iteration 1, a client's view.</b> A member of a subscribing organization signs in and sees
the same gallery with one difference: Follow, or the state following. Their menu holds Sources and Following only;
nothing about other clients, hosts or access."""
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
        for name, count in [("Overview", ""), ("Posts", "8"), ("Activity", "3"), ("Settings", "")]
    )
    return f"""
<div class="row">{icon("site", "big")}<div><h1>Afisha.uz <span class="tag">healthy</span></h1>
<p class="sub" style="margin:0">last harvest 13:12 · next 19:12</p></div>
<span class="grow"></span><span class="btn">Pause source</span><span class="btn go">Harvest now</span></div>
<div class="pills" style="margin:14px 0 4px">{HARVEST}</div>
<div class="tabs">{tabs}</div>"""


def source_overview() -> str:
    body = source_head("Overview") + f"""
<div class="cols">
<div>
  <div class="card"><div class="pad" style="padding-bottom:6px"><h2>Sections being harvested</h2></div><table>
  <tr><th>Section</th><th>Harvests</th><th>Last</th><th>Next</th><th>Posts</th><th>Followed by</th><th></th></tr>
  <tr><td><b>Fashion</b></td><td>every 6 hours<br><small>checks daily</small></td>
    <td>13:12 <span class="tag warn">partial</span><br><small>5-page limit</small></td><td>19:12</td><td>4</td><td>1 client</td><td><span class="btn sm">Edit</span></td></tr>
  <tr><td><b>Exhibitions</b></td><td>every 6 hours<br><small>checks daily</small></td>
    <td>13:12 <span class="tag">completed</span></td><td>19:12</td><td>4</td><td>1 client</td><td><span class="btn sm">Edit</span></td></tr>
  <tr class="more"><td colspan="7"><span class="chev side-chev">&#9656;</span> 4 more sections nobody follows</td></tr>
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
<div class="note"><b>Mock, iteration 1, the operator's view.</b> Overview lists only the sections being harvested;
the ones nobody follows fold into one closed line. Posts have their own tab, so none repeat here. Chart heights are
samples.</div>"""
    return frame("Sources", "Collect &rsaquo; Sources &rsaquo; Afisha &rsaquo; <b>Afisha.uz</b>", body)


POSTS = [
    ("Показ мод The Fashion Show Line 2026", "event", "21 Nov 2026", "Fashion", "2"),
    ("Fashion article", "article", "", "Fashion", "1"),
    ("Fashion article", "article", "", "Fashion", "1"),
    ("Fashion article", "article", "", "Fashion", "1"),
    ("Exhibition listing", "event", "past", "Exhibitions", "1"),
    ("Exhibition article", "article", "", "Exhibitions", "1"),
    ("Exhibition article", "article", "", "Exhibitions", "1"),
    ("Exhibition article", "article", "", "Exhibitions", "1"),
]
POST_FILTERS = """<div class="row" style="margin-bottom:14px"><span class="search">Search this source's posts</span>
  <span class="filter on">All 8</span><span class="filter">Fashion 4</span><span class="filter">Exhibitions 4</span>
  <span class="filter">Events 2</span></div>"""


def source_posts(view: str) -> str:
    if view == "rows":
        table = "".join(
            f'<tr class="{"sel" if index == 0 else ""}"><td><b>{title}</b>{"<br><small>" + when + "</small>" if when else ""}</td>'
            f'<td>{pill(kind, "on" if kind == "event" else "")}</td><td>{section}</td><td>revision {rev}</td></tr>'
            for index, (title, kind, when, section, rev) in enumerate(POSTS)
        )
        content = f"""<div class="cols" style="grid-template-columns:1fr 400px">
<div class="card"><table><tr><th>Post</th><th>Kind</th><th>Section</th><th>Revision</th></tr>{table}</table></div>
<div class="card pad"><h2>Показ мод The Fashion Show Line 2026</h2>
  <div class="pills" style="margin-bottom:12px">{pill("event", "on")}{pill("Fashion", "on")}{pill("revision 2")}</div>
  <div class="kv"><span>Starts</span><b>21 Nov 2026, 17:00</b>
    <span>Place</span><b>Дворец творчества молодёжи, Ташкент</b>
    <span>Address</span><b>просп. Мустакиллик, 2</b>
    <span>Offers</span><b>1</b>
    <span>Posted</span><b>14 Oct 2026</b>
    <span>Harvested</span><b>today 13:11</b>
    <span>Changed</span><b>the city was added</b></div>
  <p style="margin:14px 0 0"><span class="btn sm">Open the original</span> <span class="btn sm">See the capture</span></p></div>
</div>"""
        note = "The Rows view keeps the pane with a post's facts and evidence beside the list."
    else:
        cards = "".join(
            f"""<div class="card pcard"><div class="thumb">{"no image kept" if kind == "article" else "image link kept"}</div>
  <div class="pills">{pill(kind, "on" if kind == "event" else "")}{pill(section)}</div>
  <b>{title}</b><div class="desc">{when or "no date"} · revision {rev}</div></div>"""
            for title, kind, when, section, rev in POSTS
        )
        content = f'<div class="tiles four">{cards}</div>'
        note = "The Cards view shows each post as a tile; opening one shows its facts and evidence."
    body = source_head("Posts") + POST_FILTERS + content + f"""
<div class="note"><b>Mock, iteration 1, the operator's view.</b> {note} The same Cards and Rows switch in the top
bar governs Sources and Posts, with one remembered choice. Titles other than the fashion show are placeholders.</div>"""
    return frame("Sources", "Collect &rsaquo; Sources &rsaquo; Afisha &rsaquo; Afisha.uz &rsaquo; <b>Posts</b>", body, view=view)


PAGES = {
    "sources": lambda: gallery("cards"),
    "sources-rows": lambda: gallery("rows"),
    "source-afisha": source_overview,
    "source-afisha-posts": lambda: source_posts("rows"),
    "source-afisha-posts-cards": lambda: source_posts("cards"),
    "client-sources": lambda: gallery("cards", client=True),
}

if __name__ == "__main__":
    for name, build in PAGES.items():
        Path(f"{name}.html").write_text(build())
    print("built", ", ".join(PAGES))
