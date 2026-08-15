"""Emit a small posts-index.json (title/link/date/description only, no
post body) alongside rss.xml. rss.xml embeds full <content:encoded> for
feed readers and runs 1.5MB+ across ~290 posts - fine for a feed reader,
much too heavy for the homepage to fetch just to list a few post titles.
"""
import json
from pathlib import Path

_pages = []


def on_nav(nav, config, files):
    # page.meta is only populated once each page is read/rendered, which
    # happens after on_nav - so just keep references here (same mutable
    # Page objects) and read .meta later, in on_post_build.
    global _pages
    _pages = list(nav.pages)
    return nav


def on_post_build(config):
    site_dir = Path(config["site_dir"])
    site_url = config["site_url"].rstrip("/")

    posts = [p for p in _pages if "date" in p.meta]
    data = [
        {
            "title": p.title,
            "link": f"{site_url}/{p.url.lstrip('/')}",
            "date": p.meta["date"].isoformat(),
            "description": p.meta.get("description") or "",
        }
        for p in sorted(posts, key=lambda p: p.meta["date"], reverse=True)
    ]

    (site_dir / "posts-index.json").write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
