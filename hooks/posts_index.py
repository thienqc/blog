"""Emit a small posts-index.json (title/link/date/description only, no
post body) alongside rss.xml. rss.xml embeds full <content:encoded> for
feed readers and runs 1.5MB+ across ~290 posts - fine for a feed reader,
much too heavy for the homepage to fetch just to list a few post titles.

Also exposes the same collected list to templates as `blog_posts`, so
overrides/rss.xml doesn't have to rely on nav.pages - nav is now an
explicit, curated list (see mkdocs.yml) that deliberately excludes
individual posts, so nav.pages no longer contains them.
"""
import json
from pathlib import Path

_posts = []


def on_files(files, config):
    # Reset at the start of every build (including mkdocs serve
    # rebuilds), otherwise posts pile up duplicated across rebuilds.
    global _posts
    _posts = []
    return files


def on_page_content(html, page, config, files):
    if "date" in page.meta:
        _posts.append(page)
    return html


def sorted_posts():
    return sorted(_posts, key=lambda p: p.meta["date"], reverse=True)


def on_template_context(context, template_name, config):
    # Fires for static_templates (rss.xml, 404.html) - regular doc pages
    # go through on_page_context instead, which static templates don't
    # have (there's no Page object backing them).
    context["blog_posts"] = sorted_posts()
    return context


def on_post_build(config):
    site_dir = Path(config["site_dir"])
    site_url = config["site_url"].rstrip("/")

    data = [
        {
            "title": p.title,
            "link": f"{site_url}/{p.url.lstrip('/')}",
            "date": p.meta["date"].isoformat(),
            "description": p.meta.get("description") or "",
        }
        for p in sorted_posts()
    ]

    (site_dir / "posts-index.json").write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
