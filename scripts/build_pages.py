#!/usr/bin/env python3
"""Build the per-project deck pages for the portfolio.

Each project lives as a small content module in ``scripts/content/`` exposing a
``PAGE`` dict. This script renders them into ``projects/<slug>/index.html`` plus
a ``projects/index.html`` hub, so the markup for ten pages stays consistent and
is edited in one place.

Usage:
    python3 scripts/build_pages.py            # write pages
    python3 scripts/build_pages.py --check    # render but do not write
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "scripts" / "content"
OUT_DIR = ROOT / "projects"

# Render order; also drives prev/next navigation and the hub grid.
# Render order. Also drives the project numbering, the prev/next navigation,
# the hub grid, and the cards injected into index.html - so reordering or
# removing a project is a one-line change here.
ORDER = [
    "pivot-bio",
    "process-monitoring",
    "htb182-cell-culture",
    "computational-antibody",
    "cr6261-influenza",
    "ricestressdb",
    "moringa-rnaseq",
    "dalbergia-genomics",
]

PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Gopi Chandran</title>
<meta name="description" content="{meta}">
<link rel="stylesheet" href="../../assets/css/deck.css">
</head>
<body>
<div class="topbar"><div class="wrap topinner">
  <a class="wordmark" href="../../index.html">GC<span>.</span> / Portfolio</a>
  <nav class="topnav" aria-label="Project navigation">
    <a href="../index.html">All projects</a>
    <a href="../../index.html#projects">Back to portfolio</a>
    {code_nav}
  </nav>
  <a class="button sm light" href="mailto:gopic2@umbc.edu">gopic2@umbc.edu</a>
</div></div>

<header class="phero"><div class="wrap">
  <div class="kicker">{number} · {category}</div>
  <h1>{headline}</h1>
  <p class="phero-sub">{sub}</p>
  <div class="meta-row">{pills}</div>
  {demo_jump}
  {note}
</div></header>

<main class="wrap deck-shell">
  <div class="deck-bar">
    <div>
      <span class="deck-counter" data-deck-counter>Slide 1 of {n_slides}</span>
      <span class="deck-hint"> · arrow keys, swipe, or the buttons</span>
    </div>
    <div class="deck-controls">
      {demo_jump_sm}
      <button class="button sm light" data-deck-prev aria-label="Previous slide">&larr; Prev</button>
      <button class="button sm primary" data-deck-next aria-label="Next slide">Next &rarr;</button>
    </div>
  </div>
  <div class="deck-track"><i data-deck-bar></i></div>
  <div data-deck>
{slides}
  </div>
</main>

<footer>
  <div class="wrap pfoot"><div class="pfoot-grid">
    {prev_link}
    <a class="button light" href="../index.html">All {n_projects} projects</a>
    {next_link}
  </div></div>
  <div class="wrap fineprint">
    <span>© Gopi Chandran · Project walkthrough</span>
    <span>{footer_note}</span>
    <span><a href="#top">Back to top &uarr;</a></span>
  </div>
</footer>
<script src="../../assets/js/deck.js"></script>
{page_script}
</body></html>
"""

SLIDE_TEMPLATE = """    <section class="slide" aria-label="{title}">
      <div class="slide-eyebrow">{eyebrow}</div>
      <h2>{title}</h2>
{body}
    </section>
"""

HUB_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Project walkthroughs · Gopi Chandran</title>
<meta name="description" content="Nine project walkthroughs - slide decks and runnable demos across bioinformatics, antibody biology, biological databases, cell culture quality and biotech commercialization.">
<link rel="stylesheet" href="../assets/css/deck.css">
</head>
<body>
<div class="topbar"><div class="wrap topinner">
  <a class="wordmark" href="../index.html">GC<span>.</span> / Portfolio</a>
  <nav class="topnav" aria-label="Main navigation">
    <a href="../index.html#frontier">Research frontier</a>
    <a href="../index.html#capabilities">Capabilities</a>
    <a href="../index.html#projects">Projects</a>
  </nav>
  <a class="button sm light" href="https://github.com/gopichandran03" target="_blank" rel="noopener">GitHub &nearr;</a>
</div></div>

<header class="phero"><div class="wrap">
  <div class="kicker">Project walkthroughs</div>
  <h1>{n_word} projects.<br><em>Open any one of them.</em></h1>
  <p class="phero-sub">Each project below opens as a short slide deck you can click through, and most carry a demo you can actually run in the browser - a control chart, a culture planning calculator, a database query console, a microsatellite finder. Every page with a demo has a button at the top that jumps straight to it. The code behind several of them sits in <code>workflows/</code> in this repository.</p>
  <div class="note neutral"><strong>How to read these:</strong> the science, methods, tools and reasoning are from my own project work. Where a demo needs data, it runs on clearly labelled example or synthetic input rather than raw lab or employer data, and each page says so. Published figures from the literature are cited to their source.</div>
</div></header>

<main class="wrap" style="padding-bottom:70px">
  <div class="pgrid">
{cards}
  </div>
</main>

<footer>
  <div class="wrap fineprint" style="padding-top:26px;border-top:1px solid var(--line)">
    <span>© Gopi Chandran · Project walkthroughs</span>
    <span><a href="../index.html">Back to the portfolio &larr;</a></span>
  </div>
</footer>
</body></html>
"""

CARD_TEMPLATE = """    <a class="pcard" href="{slug}/index.html">
      <div class="num">{number} / {category}</div>
      <h3>{card_title}</h3>
      <p>{card_blurb}</p>
      <div class="tags">{tags}</div>
      <div class="go">{cta} &nearr;</div>
    </a>
"""


def load_page(slug: str) -> dict:
    path = CONTENT_DIR / (slug.replace("-", "_") + ".py")
    if not path.exists():
        raise SystemExit(f"missing content module: {path}")
    spec = importlib.util.spec_from_file_location(f"content_{slug}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    page = dict(module.PAGE)
    page["slug"] = slug
    return page


def render_slides(page: dict) -> str:
    out = []
    for slide in page["slides"]:
        out.append(
            SLIDE_TEMPLATE.format(
                eyebrow=slide.get("eyebrow", page["category"]),
                title=slide["title"],
                body=slide["body"].rstrip("\n"),
            )
        )
    return "\n".join(out)


def demo_slide_number(page: dict) -> int | None:
    """1-based index of the slide carrying the interactive demo, if any.

    A content module may set `demo_slide` explicitly; otherwise the first
    slide whose body contains a demo block is used.
    """
    if page.get("demo_slide"):
        return int(page["demo_slide"])
    for i, slide in enumerate(page["slides"], start=1):
        if 'class="demo' in slide["body"]:
            return i
    return None


def render_page(page: dict, prev: dict | None, nxt: dict | None) -> str:
    pills = "".join(
        f'<span class="pill{" " + p[1] if len(p) > 1 else ""}">{p[0]}</span>'
        for p in page["pills"]
    )
    note = (
        f'<div class="note">{page["note"]}</div>' if page.get("note") else ""
    )
    code_nav = (
        f'<a href="../../{page["code"]}">Code &amp; README</a>'
        if page.get("code")
        else ""
    )
    prev_link = (
        f'<a class="button light" href="../{prev["slug"]}/index.html">&larr; {prev["card_title"]}</a>'
        if prev
        else '<a class="button light" href="../../index.html#projects">&larr; Portfolio</a>'
    )
    next_link = (
        f'<a class="button primary" href="../{nxt["slug"]}/index.html">{nxt["card_title"]} &rarr;</a>'
        if nxt
        else '<a class="button primary" href="../../index.html#contact">Get in touch &rarr;</a>'
    )
    n = demo_slide_number(page)
    if n:
        label = page.get("demo_label", "Try the interactive demo")
        demo_jump = (
            f'<button class="demo-jump" data-deck-goto="{n}">'
            f'<span class="play" aria-hidden="true">&#9654;</span> {label}'
            f'<small>skip to slide {n}</small></button>'
        )
        demo_jump_sm = (
            f'<button class="demo-jump" data-deck-goto="{n}">'
            f'<span class="play" aria-hidden="true">&#9654;</span> Demo</button>'
        )
    else:
        demo_jump = demo_jump_sm = ""

    page_script = page.get("page_script", "")
    return PAGE_TEMPLATE.format(
        demo_jump=demo_jump,
        demo_jump_sm=demo_jump_sm,
        title=page["card_title"],
        meta=page["meta"],
        number=page["number"],
        category=page["category"],
        headline=page["headline"],
        sub=page["sub"],
        pills=pills,
        note=note,
        code_nav=code_nav,
        n_slides=len(page["slides"]),
        slides=render_slides(page),
        prev_link=prev_link,
        next_link=next_link,
        footer_note=page.get("footer_note", "Walkthrough built for this portfolio."),
        n_projects=page["_n_projects"],
        page_script=page_script,
    )


def render_hub(pages: list[dict]) -> str:
    cards = []
    for page in pages:
        tags = "".join(f'<span class="tag">{t}</span>' for t in page["tags"])
        cards.append(
            CARD_TEMPLATE.format(
                slug=page["slug"],
                number=page["number"],
                category=page["category"],
                card_title=page["card_title"],
                card_blurb=page["card_blurb"],
                tags=tags,
                cta=page.get("cta", "Open walkthrough"),
            )
        )
    words = {7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}
    return HUB_TEMPLATE.format(cards="\n".join(cards),
                               n_word=words.get(len(pages), str(len(pages))))


CARDS_START = "<!-- PROJECT_CARDS:START -->"
CARDS_END = "<!-- PROJECT_CARDS:END -->"

HOME_CARD = """<article class="project"><div class="num">{number} / {category_upper}</div>\
<h3>{home_title}</h3><p>{card_blurb}</p><div class="tags">{tags}</div>\
<a href="./projects/{slug}/index.html">{cta} &nearr;</a></article>"""


def sync_home_cards(pages: list[dict], write: bool) -> bool:
    """Rewrite the projects grid in index.html so it matches ORDER."""
    home = ROOT / "index.html"
    html = home.read_text(encoding="utf-8")
    if CARDS_START not in html or CARDS_END not in html:
        print("  ! index.html has no PROJECT_CARDS markers - skipping card sync")
        return False
    cards = "\n".join(
        HOME_CARD.format(
            number=p["number"],
            category_upper=p["category"].upper(),
            home_title=p.get("home_title", p["card_title"]),
            card_blurb=p["card_blurb"],
            tags="".join(f'<span class="tag">{t}</span>' for t in p["tags"]),
            slug=p["slug"],
            cta=p.get("cta", "Open walkthrough"),
        )
        for p in pages
    )
    head, _, rest = html.partition(CARDS_START)
    _, _, tail = rest.partition(CARDS_END)
    new = f"{head}{CARDS_START}\n{cards}\n{CARDS_END}{tail}"
    changed = new != html
    if write and changed:
        home.write_text(new, encoding="utf-8")
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="render without writing")
    args = ap.parse_args()

    pages = []
    for i, slug in enumerate(ORDER, start=1):
        page = load_page(slug)
        page["number"] = f"{i:02d}"   # numbering follows ORDER, not the module
        pages.append(page)
    for page in pages:
        page["_n_projects"] = len(pages)
    written = 0
    for i, page in enumerate(pages):
        prev = pages[i - 1] if i > 0 else None
        nxt = pages[i + 1] if i < len(pages) - 1 else None
        html = render_page(page, prev, nxt)
        target = OUT_DIR / page["slug"] / "index.html"
        print(f"{page['slug']:<32} {len(page['slides'])} slides  {len(html):>7,} bytes")
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(html, encoding="utf-8")
            written += 1

    if sync_home_cards(pages, write=not args.check):
        print(f"{'index.html':<32} cards      synced to ORDER")
        written += 0 if args.check else 1

    hub = render_hub(pages)
    print(f"{'projects/index.html':<32} hub        {len(hub):>7,} bytes")
    if not args.check:
        (OUT_DIR / "index.html").write_text(hub, encoding="utf-8")
        written += 1
        print(f"\nwrote {written} files under {OUT_DIR.relative_to(ROOT)}/")
    else:
        print("\n--check: nothing written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
