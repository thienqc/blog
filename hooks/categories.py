"""Custom category listings: Tôi đi / Tôi đọc / Tôi học / Tôi cảm / Khác.

Independent of mkdocs-blogging-plugin's own "categories" feature, which
assigns posts to a category by which directory they physically live in
(config.dirs, matched via file_path.parents - see on_page_content in
mkdocs_blogging_plugin/plugin.py in .venv). That would mean moving every
post into a per-category folder, which breaks the many relative links
between posts and - more importantly - Envelope (the Obsidian plugin
publishing posts from Obsidian) always pushes straight into docs/post/
and can't be told to push elsewhere.

So instead, a post opts into a category via a plain `category: <slug>`
front-matter field - or a list, `category: [<slug>, <slug>]`, to appear
in more than one. Anything missing/unrecognized defaults to "khac".
Category pages (docs/toi-di.md etc.) contain a `{{ category_content
<slug> }}` placeholder that gets swapped for a rendered post list.

Same two-phase pattern mkdocs-blogging-plugin itself uses, for the same
reason: on_page_content runs for every page while mkdocs is still
building content (phase 1 - guaranteed to finish for *all* pages before
any page is templated), collecting posts into buckets; on_post_page then
substitutes into already-rendered HTML (phase 2), so every post has
already been collected by the time any page's placeholder is resolved,
regardless of nav order.
"""
import random
import re

CATEGORY_LABELS = {
    "toi-di": "Tôi đi",
    "toi-doc": "Tôi đọc",
    "toi-hoc": "Tôi học",
    "toi-cam": "Tôi cảm",
    "khac": "Khác",
}
PLACEHOLDER = re.compile(r"\{\{\s*category_content\s+([\w-]+)\s*\}\}")

_posts_by_category = {key: [] for key in CATEGORY_LABELS}
_post_categories = {}  # page -> [keys it belongs to], for "related posts"

# Top-level nav order. Auto-nav (no explicit `nav:` in mkdocs.yml - see
# the comment there for why) sorts alphabetically by filename with
# directories always last, which is neither the order we want nor
# reorderable from YAML without hand-listing every post (losing prev/
# next between posts). Reordering nav.items here instead just changes
# display order - it runs *after* mkdocs already computed prev/next from
# the original order, so that's unaffected.
NAV_ORDER = ["index.md", "toi-di.md", "toi-doc.md", "toi-hoc.md", "toi-cam.md", "khac.md"]


def on_nav(nav, config, files):
    def sort_key(item):
        src_uri = getattr(getattr(item, "file", None), "src_uri", None)
        try:
            return NAV_ORDER.index(src_uri)
        except ValueError:
            return len(NAV_ORDER)  # keep everything else after, in its existing order

    nav.items.sort(key=sort_key)

    # The auto-generated section for post/ is titled "Post" (humanized
    # directory name) and Material doesn't pick that up from
    # post/index.md's own `title:` front matter (only the icon comes
    # from there, via navigation.indexes) - rename it directly here.
    for item in nav.items:
        if getattr(item, "children", None) and item.title == "Post":
            item.title = "Bài viết"
            break

    return nav


def on_files(files, config):
    # Reset at the start of every build (including mkdocs serve rebuilds),
    # otherwise posts pile up duplicated across live-reload rebuilds.
    for key in CATEGORY_LABELS:
        _posts_by_category[key] = []
    _post_categories.clear()
    return files


def on_page_content(html, page, config, files):
    if "date" not in page.meta:
        return html
    raw = page.meta.get("category")
    raw = raw if isinstance(raw, list) else [raw]
    keys = [k for k in raw if k in CATEGORY_LABELS] or ["khac"]
    _post_categories[page.file.src_path] = keys
    for key in keys:
        _posts_by_category[key].append(page)
    return html


# mkdocs-blogging-plugin's own .blog-post styling lives inside a Jinja
# fragment template (templates/blog.html) that only gets embedded on
# pages the plugin itself renders (index.md, via {{ blog_content }}) -
# these category pages don't go through that, so the same handful of
# rules gets repeated here inline instead of depending on it.
STYLE = (
    "<style>"
    ".md-typeset .blog-post:first-of-type h2{margin-top:0}"
    ".md-typeset .blog-post-title{margin-bottom:0;font-size:1.25em}"
    ".md-typeset .blog-post-description{margin-bottom:0;font-style:italic}"
    ".md-typeset .blog-post-extra{color:var(--md-default-fg-color--light)}"
    "</style>"
)


def render_category(key):
    posts = sorted(_posts_by_category[key], key=lambda p: p.meta["date"], reverse=True)
    if not posts:
        return STYLE + "<p><em>Chưa có bài viết nào trong mục này.</em></p>"

    parts = [STYLE]
    for p in posts:
        description = p.meta.get("description") or ""
        parts.append(
            '<div class="blog-post">'
            f'<h2 class="blog-post-title"><a class="link" href="{p.abs_url}">{p.title}</a></h2>'
            f'<p class="blog-post-description">{description}</p>'
            f'<div class="blog-post-extra">{p.meta["date"].strftime("%d-%m-%Y")}</div>'
            "<hr /></div>"
        )
    return "\n".join(parts)


# "Related posts" appended to the bottom of every post: pulled from the
# union of all categories that post belongs to (own post excluded), so
# a post in 2 categories draws from both pools combined rather than
# picking just one. Built at build time (this runs once per build, not
# per page view) - no client-side fetch, no runtime cost per visitor.
RELATED_COUNT = 3
RELATED_STYLE = (
    "<style>"
    ".related-posts{margin-top:2em}"
    ".related-posts ul{list-style:none;padding:0}"
    ".related-posts li{border-bottom:1px solid var(--md-default-fg-color--lightest);padding:0.6em 0}"
    ".related-posts li:first-child{padding-top:0}"
    "</style>"
)
# Insert right before the "Bài ngẫu nhiên" button (overrides/partials/
# comments.html) - falls back to before comments, then end of article,
# for the rare post without comments/that button enabled.
RANDOM_BTN_ANCHOR = re.compile(r'<button id="random-post-btn"')
COMMENTS_ANCHOR = re.compile(r'<h2 id="__comments">')


def render_related(page):
    keys = _post_categories.get(page.file.src_path, [])
    pool = {}
    for key in keys:
        for p in _posts_by_category.get(key, []):
            if p is not page:
                pool[p.abs_url] = p
    candidates = list(pool.values())
    if not candidates:
        return ""

    chosen = random.sample(candidates, min(RELATED_COUNT, len(candidates)))
    items = "".join(f'<li><a href="{p.abs_url}">{p.title}</a></li>' for p in chosen)
    return (
        RELATED_STYLE
        + '<div class="related-posts">'
        + "<h2>Bài cùng chuyên mục</h2>"
        + f"<ul>{items}</ul>"
        + "</div>"
    )


def on_post_page(output, page, config):
    match = PLACEHOLDER.search(output)
    if match:
        key = match.group(1)
        return PLACEHOLDER.sub(lambda _: render_category(key), output, count=1)

    if page.file.src_path in _post_categories:
        related = render_related(page)
        if related:
            anchor_match = RANDOM_BTN_ANCHOR.search(output) or COMMENTS_ANCHOR.search(output)
            insert_at = anchor_match.start() if anchor_match else output.rfind("</article>")
            if insert_at != -1:
                output = output[:insert_at] + related + output[insert_at:]

    return output
