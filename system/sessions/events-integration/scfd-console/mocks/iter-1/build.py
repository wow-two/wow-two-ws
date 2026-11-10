"""Builds the SCFD console mock pages of this iteration: one frame, one function per page.

Run from this folder: python3 build.py, then render each .html with render-html.sh at 1440.
"""
from pathlib import Path

NAV = [
    ("Overview", [("Home", "")]),
    ("Collect", [("Sources", "7"), ("Activity", "")]),
    ("Deliver", [("Subscriptions", "2"), ("Subscribers", "1")]),
    ("System", [("Access", "")]),
]


def frame(active: str, crumb: str, body: str) -> str:
    side = ""
    for group, items in NAV:
        side += f'<div class="group">{group}</div>'
        for name, count in items:
            on = " on" if name == active else ""
            small = f"<small>{count}</small>" if count else ""
            side += f'<span class="nav{on}">{name}{small}</span>'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>SCFD console mock</title>
<link rel="stylesheet" href="mock.css"></head><body>
<div class="frame">
  <aside class="side"><div class="brand">SCFD <span class="chip">dev</span> <span class="chip">v0.1.14</span></div>{side}</aside>
  <main>
    <div class="bar"><span>&#9707;</span><span class="crumb">{crumb}</span><span class="grow"></span>
      <span class="select">Ocharo events &#9662;</span>
      <span class="avatar"><i>TO</i> Test operator &#9662;</span></div>
    <div class="page">{body}</div>
  </main>
</div></body></html>"""


def bars(values: list[int], height: int = 40) -> str:
    top = max(values) or 1
    cells = "".join(
        f'<i class="{"zero" if v == 0 else ""}" style="height:{max(3, round(v / top * height))}px"></i>' for v in values
    )
    return f'<span class="bars" style="height:{height}px">{cells}</span>'


def pill(text: str, kind: str = "") -> str:
    return f'<span class="pill {kind}">{text}</span>'


AFISHA_TREND = [0, 2, 0, 1, 3, 0, 0, 4, 1, 0, 2, 0, 5, 8]  # sample heights; the first real captures ran on the last day
NONE = [0] * 14

SOURCES = {
    "Event listings": [
        ("Afisha.uz", "site · Tashkent", True, ["Fashion", "Exhibitions"], 4, AFISHA_TREND),
        ("Anons.uz", "site · Uzbekistan", False, [], 4, NONE),
        ("Craft fair", "site · fairs", False, [], 1, NONE),
    ],
    "Venue calendars": [
        ("Uzexpocentre", "site · Tashkent venue", False, [], 2, NONE),
        ("CAEx", "site · Tashkent venue", False, [], 1, NONE),
    ],
    "Marketplaces": [("OLX", "site · listings", False, [], 3, NONE)],
    "Social": [("Instagram", "accounts", False, [], 0, NONE)],
}


def toolbar(view: str) -> str:
    cards = " on" if view == "cards" else ""
    rows = " on" if view == "rows" else ""
    return f"""
<div class="row" style="margin-bottom:18px">
  <span class="search">Search 7 sources</span>
  <span class="filter on">All 7</span><span class="filter">Following 1</span><span class="filter">Needs attention 0</span>
  <span class="seg"><span class="{cards.strip()}">&#9638; Cards</span><span class="{rows.strip()}">&#9776; Rows</span></span>
</div>"""


def group_cards() -> str:
    cards = ""
    for name, items in SOURCES.items():
        following = sum(1 for item in items if item[2])
        trend = [sum(day) for day in zip(*(item[5] for item in items))]
        posts = sum(trend)
        results = pill(f"<b>{posts}</b> posts", "num") + pill(f"<b>{1 if posts else 0}</b> delivered", "num")
        cards += f"""<div class="card gcard"><div class="row"><b>{name}</b><span class="grow"></span>
  <small>{len(items)} source{"s" if len(items) != 1 else ""} · {following} followed</small></div>
  <div class="row end"><div class="pills">{results}</div><span class="grow"></span>{bars(trend, 30)}</div></div>"""
    return f'<div class="groups">{cards}</div>'


def tile(name: str, kind: str, following: bool, sections: list[str], more: int, trend: list[int]) -> str:
    state = '<span class="tag">healthy</span>' if following else '<span class="tag off">not followed</span>'
    secs = "".join(pill(s, "on") for s in sections)
    if sections:
        secs += pill(f"+{more} sections")
    elif more:
        secs += pill(f"{more} section{'s' if more != 1 else ''} to follow")
    else:
        secs += pill("accounts to follow")
    if following:
        results = (pill("<b>8</b> posts", "num") + pill("<b>1</b> delivered", "num") + pill("<b>1</b> partial", "warn")
                   + pill("<b>0</b> failed", "num"))
        foot = "last capture 13:12 · next 19:12"
    else:
        results = pill("no captures yet", "muted")
        foot = "open to follow a section"
    return f"""<div class="card tile{'' if following else ' quiet'}">
  <div class="row"><span class="ico">{name[0]}</span><div><b>{name}</b><br><small>{kind}</small></div>
    <span class="grow"></span>{state}</div>
  <div class="pills">{secs}</div>
  <div class="row end"><div><div class="pills">{results}</div><small>{foot}</small></div>
    <span class="grow"></span>{bars(trend)}</div></div>"""


def sources_cards() -> str:
    body = ('<h1>Sources</h1><p class="sub">The sources we can read, by group. Open one to follow its sections '
            "and read its posts.</p>" + toolbar("cards") + group_cards())
    for name, items in SOURCES.items():
        body += f'<div class="ghead"><b>{name}</b><small>{len(items)} source{"s" if len(items) != 1 else ""}</small></div><div class="tiles">'
        body += "".join(tile(*item) for item in items) + "</div>"
    body += """<div class="note"><b>Mock, iteration 1.</b> Laid out as Wheelhouse lays out products: the groups first,
each with its figures as pills and a trend, then every group's sources as cards. Each card ends with its result pills
and a 14-day chart of captured posts at the bottom right. Groups and every number except Afisha's pills are
placeholders, and the chart heights are samples: Afisha's first captures ran today.</div>"""
    return frame("Sources", "Collect &rsaquo; <b>Sources</b>", body)


def sources_rows() -> str:
    body = ('<h1>Sources</h1><p class="sub">The sources we can read, by group. Open one to follow its sections '
            "and read its posts.</p>" + toolbar("rows"))
    body += '<div class="card"><table><tr><th>Source</th><th>Following</th><th>Results</th><th>Last capture</th>'
    body += "<th>Next</th><th>Health</th><th>14 days</th></tr>"
    for name, items in SOURCES.items():
        body += f'<tr class="grow-row"><td colspan="7"><b>{name}</b> <small>{len(items)} source{"s" if len(items) != 1 else ""}</small></td></tr>'
        for source, kind, following, sections, more, trend in items:
            if following:
                follows = "".join(pill(s, "on") for s in sections)
                results = pill("<b>8</b> posts", "num") + pill("<b>1</b> delivered", "num") + pill("<b>1</b> partial", "warn")
                last, nxt, health = "13:12", "19:12", '<span class="tag">healthy</span>'
            else:
                follows = pill(f"{more} section{'s' if more != 1 else ''} to follow" if more else "accounts to follow")
                results = pill("no captures yet", "muted")
                last, nxt, health = "never", "", '<span class="tag off">not followed</span>'
            body += (f"<tr><td><b>{source}</b><br><small>{kind}</small></td><td>{follows}</td><td>{results}</td>"
                     f"<td>{last}</td><td>{nxt}</td><td>{health}</td><td>{bars(trend, 24)}</td></tr>")
    body += "</table></div>"
    body += """<div class="note"><b>Mock, iteration 1.</b> The Rows view of the same page: one line per source under
its group, with the same pills and a smaller chart.</div>"""
    return frame("Sources", "Collect &rsaquo; <b>Sources</b>", body)


def source_head(tab: str) -> str:
    tabs = "".join(
        f'<span class="tab{" on" if name == tab else ""}">{name}{f" <small>{count}</small>" if count else ""}</span>'
        for name, count in [("Overview", ""), ("Posts", "8"), ("Activity", "3"), ("Settings", "")]
    )
    return f"""
<div class="row"><span class="ico big">A</span><div><h1>Afisha.uz <span class="tag">healthy</span></h1>
<p class="sub" style="margin:0">Event listings · Tashkent · read from public pages, paced, inside robots.txt</p></div>
<span class="grow"></span><span class="btn">Pause source</span><span class="btn go">Capture now</span></div>
<div class="pills" style="margin:14px 0 4px">{pill("<b>8</b> posts", "num")}{pill("<b>2</b> events", "num")}
{pill("<b>1</b> delivered", "num")}{pill("<b>1</b> partial", "warn")}{pill("<b>0</b> failed", "num")}</div>
<div class="tabs">{tabs}</div>"""


def source_overview() -> str:
    body = source_head("Overview") + f"""
<div class="cols">
<div>
  <div class="card"><div class="pad" style="padding-bottom:6px"><h2>Sections</h2></div><table>
  <tr><th>Section</th><th>State</th><th>Captures</th><th>Last</th><th>Next</th><th>Posts</th><th>Subscribers</th><th></th></tr>
  <tr><td><b>Fashion</b></td><td><span class="tag">following</span></td><td>every 6 hours<br><small>checks daily</small></td>
    <td>13:12 <span class="tag warn">partial</span><br><small>5-page limit</small></td><td>19:12</td><td>4</td><td>Ocharo</td><td><span class="btn sm">Edit</span></td></tr>
  <tr><td><b>Exhibitions</b></td><td><span class="tag">following</span></td><td>every 6 hours<br><small>checks daily</small></td>
    <td>13:12 <span class="tag">completed</span></td><td>19:12</td><td>4</td><td>Ocharo</td><td><span class="btn sm">Edit</span></td></tr>
  <tr><td><b>Concerts</b></td><td><span class="tag off">not followed</span></td><td></td><td></td><td></td><td></td><td></td><td><span class="btn sm">Follow</span></td></tr>
  <tr><td><b>Theatre</b></td><td><span class="tag off">not followed</span></td><td></td><td></td><td></td><td></td><td></td><td><span class="btn sm">Follow</span></td></tr>
  <tr><td><b>Festivals</b></td><td><span class="tag off">not followed</span></td><td></td><td></td><td></td><td></td><td></td><td><span class="btn sm">Follow</span></td></tr>
  </table></div>
  <div class="card" style="margin-top:20px"><div class="pad" style="padding-bottom:6px"><h2>Latest posts</h2></div><table>
  <tr><td><b>Показ мод The Fashion Show Line 2026</b><br><small>event · 21 Nov 2026 · Ташкент · Fashion</small></td>
    <td><span class="tag">delivered to Ocharo</span></td><td>revision 2</td></tr>
  <tr><td><b>Exhibition listing</b><br><small>event · past · Ташкент · Exhibitions</small></td>
    <td><span class="tag off">filtered out</span></td><td>revision 1</td></tr>
  <tr><td colspan="3"><small>6 more on the Posts tab</small></td></tr>
  </table></div>
</div>
<div>
  <div class="card pad"><h2>Health</h2><div class="kv">
    <span>Reading pace</span><b>a page every 5 s</b>
    <span>Paused</span><b>no</b>
    <span>Failures in a row</span><b>0</b>
    <span>Last refusal</span><b>none</b></div></div>
  <div class="card pad" style="margin-top:20px"><h2>Captured posts, 14 days</h2>
    <div class="row end" style="margin-top:6px">{bars(AFISHA_TREND, 96)}</div>
    <div class="row" style="margin-top:8px"><small>28 Oct</small><span class="grow"></span><small>today</small></div>
    <div class="pills" style="margin-top:12px">{pill("<b>8</b> captured", "num")}{pill("<b>49</b> found", "num")}{pill("<b>1</b> changed", "num")}</div></div>
</div></div>
<div class="note"><b>Mock, iteration 1.</b> A source opens like a Wheelhouse product: result pills under the name,
then tabs. Posts left the menu and live here, as the latest two on Overview and all of them on the Posts tab. The
chart sits at the bottom right. Sections other than Fashion and Exhibitions are placeholders.</div>"""
    return frame("Sources", "Collect &rsaquo; Sources &rsaquo; <b>Afisha.uz</b>", body)


def source_posts() -> str:
    rows = [
        ("Показ мод The Fashion Show Line 2026", "event", "21 Nov 2026 · Ташкент", "Fashion", "2",
         '<span class="tag">delivered to Ocharo</span>', " sel"),
        ("Fashion article", "article", "", "Fashion", "1", '<span class="tag off">not an event</span>', ""),
        ("Fashion article", "article", "", "Fashion", "1", '<span class="tag off">not an event</span>', ""),
        ("Fashion article", "article", "", "Fashion", "1", '<span class="tag off">not an event</span>', ""),
        ("Exhibition listing", "event", "past · Ташкент", "Exhibitions", "1", '<span class="tag off">filtered out</span>', ""),
        ("Exhibition article", "article", "", "Exhibitions", "1", '<span class="tag off">not an event</span>', ""),
        ("Exhibition article", "article", "", "Exhibitions", "1", '<span class="tag off">not an event</span>', ""),
        ("Exhibition article", "article", "", "Exhibitions", "1", '<span class="tag off">not an event</span>', ""),
    ]
    table = "".join(
        f'<tr class="{sel.strip()}"><td><b>{title}</b><br><small>{kind}{" · " + when if when else ""}</small></td>'
        f"<td>{section}</td><td>revision {rev}</td><td>{state}</td></tr>"
        for title, kind, when, section, rev, state, sel in rows
    )
    body = source_head("Posts") + f"""
<div class="row" style="margin-bottom:14px"><span class="search">Search this source's posts</span>
  <span class="filter on">All 8</span><span class="filter">Fashion 4</span><span class="filter">Exhibitions 4</span>
  <span class="filter">Events 2</span><span class="filter">Delivered 1</span></div>
<div class="cols" style="grid-template-columns:1fr 400px">
<div class="card"><table><tr><th>Post</th><th>Section</th><th>Revision</th><th>Result</th></tr>{table}</table></div>
<div class="card pad"><h2>Показ мод The Fashion Show Line 2026</h2>
  <div class="pills" style="margin-bottom:12px">{pill("event", "on")}{pill("Fashion", "on")}{pill("revision 2", "num")}</div>
  <div class="kv"><span>Starts</span><b>21 Nov 2026, 17:00</b>
    <span>Place</span><b>Дворец творчества молодёжи, Ташкент</b>
    <span>Address</span><b>просп. Мустакиллик, 2</b>
    <span>Offers</span><b>1</b>
    <span>Posted</span><b>14 Oct 2026</b>
    <span>Captured</span><b>today 13:11</b>
    <span>Changed</span><b>the city was added</b>
    <span>Delivered</span><b>Ocharo, 13:20</b></div>
  <p style="margin:14px 0 0"><span class="btn sm">Open the source page</span> <span class="btn sm">See the capture</span></p></div>
</div>
<div class="note"><b>Mock, iteration 1.</b> A source's posts with what happened to each: delivered, filtered out, or
not an event. The pane shows the facts read from the page and the evidence kept. Titles other than the fashion show
are placeholders.</div>"""
    return frame("Sources", "Collect &rsaquo; Sources &rsaquo; Afisha.uz &rsaquo; <b>Posts</b>", body)


def subscriptions() -> str:
    body = """
<h1>Subscriptions</h1><p class="sub">Who receives which source and section.</p>
<div class="cols">
<div class="card"><table>
<tr><th>Subscriber</th><th>Source</th><th>Section</th><th>Relevance filter</th><th>Delivery</th><th>Last delivered</th></tr>
<tr><td><b>Ocharo</b></td><td>Afisha.uz</td><td>Fashion</td><td>fashion and textile</td><td><span class="tag">delivering</span></td><td>13:20<br><small>1 event</small></td></tr>
<tr><td><b>Ocharo</b></td><td>Afisha.uz</td><td>Exhibitions</td><td>fashion and textile</td><td><span class="tag">delivering</span></td><td>never<br><small>nothing matched yet</small></td></tr>
</table></div>
<div class="card pad"><h2>New subscription</h2>
  <div class="field"><label>Subscriber</label><span class="select">Ocharo &#9662;</span></div>
  <div class="field"><label>Source</label><span class="select">Afisha.uz &#9662;</span></div>
  <div class="field"><label>Sections</label><span class="pick on">Fashion</span><span class="pick on">Exhibitions</span><span class="pick">Concerts</span><span class="pick">Theatre</span></div>
  <div class="field"><label>Relevance filter</label><span class="select">fashion and textile &#9662;</span></div>
  <div class="field dim"><label>Tags</label><span class="pick">from AI classification, later</span></div>
  <span class="btn go">Subscribe</span></div>
</div>
<div class="note"><b>Mock, iteration 1.</b> A subscriber only chooses: subscriber, source, sections. No address and
no typed tag. Choosing a section nobody follows yet starts following it.</div>"""
    return frame("Subscriptions", "Deliver &rsaquo; <b>Subscriptions</b>", body)


PAGES = {
    "sources": sources_cards,
    "sources-rows": sources_rows,
    "source-afisha": source_overview,
    "source-afisha-posts": source_posts,
    "subscriptions": subscriptions,
}

if __name__ == "__main__":
    for name, build in PAGES.items():
        Path(f"{name}.html").write_text(build())
    print("built", ", ".join(PAGES))
