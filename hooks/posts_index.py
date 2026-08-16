"""Emit a small posts-index.json (title/link/date/description only, no
post body) alongside rss.xml. rss.xml embeds full <content:encoded> for
feed readers and runs 1.5MB+ across ~290 posts - fine for a feed reader,
much too heavy for the homepage to fetch just to list a few post titles.

Also exposes the same collected list to templates as `blog_posts`, so
overrides/rss.xml doesn't have to rely on nav.pages - nav is now an
explicit, curated list (see mkdocs.yml) that deliberately excludes
individual posts, so nav.pages no longer contains them.
"""
import itertools
import json
import re
from pathlib import Path

_posts = []
ARCHIVE_PLACEHOLDER = re.compile(r"\{\{\s*archive_content\s*\}\}")


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


# "Bài viết" (docs/post/index.md) archive: every post, grouped by year,
# minimal style - just year headings + a plain linked list (no cards,
# no descriptions). Reuses the same `_posts` this hook already collects
# for posts-index.json/rss.xml, so no extra pass over the content.
ARCHIVE_STYLE = (
    "<style>"
    ".post-archive ul{list-style:none;padding:0;margin:0 0 1.5em}"
    ".post-archive li{display:flex;gap:0.8em;padding:0.3em 0}"
    ".post-archive .post-archive-date{color:var(--md-default-fg-color--light);"
    "font-variant-numeric:tabular-nums;flex-shrink:0}"
    "</style>"
)


def render_archive():
    parts = [ARCHIVE_STYLE, '<div class="post-archive">']
    for year, posts in itertools.groupby(sorted_posts(), key=lambda p: p.meta["date"].year):
        parts.append(f"<h2>{year}</h2><ul>")
        for p in posts:
            date_str = p.meta["date"].strftime("%d/%m")
            parts.append(
                f'<li><span class="post-archive-date">{date_str}</span>'
                f'<a href="{p.abs_url}">{p.title}</a></li>'
            )
        parts.append("</ul>")
    parts.append("</div>")
    return "".join(parts)


def on_post_page(output, page, config):
    return ARCHIVE_PLACEHOLDER.sub(lambda _: render_archive(), output, count=1)


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
