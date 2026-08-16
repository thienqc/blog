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
from urllib.parse import quote, urljoin, urlsplit

CATEGORY_LABELS = {
    "toi-di": "Tôi đi",
    "toi-doc": "Tôi đọc",
    "toi-hoc": "Tôi học",
    "toi-cam": "Tôi cảm",
    "khac": "Khác",
}
PLACEHOLDER = re.compile(r"\{\{\s*category_content\s+([\w-]+)\s*\}\}")
LINK_TAG = re.compile(r'<a[^>]+href="([^"]+)"', re.I)
ADMONITION_EXAMPLE = re.compile(r'<div class="admonition example">(.*?)</div>', re.S)

_posts_by_category = {key: [] for key in CATEGORY_LABELS}
_post_categories = {}  # src_path -> [category keys it belongs to]
_posts_by_tag = {}  # tag -> [pages with that tag], for "related posts"
_post_tags = {}  # src_path -> [tags it has]
_pages_by_url = {}  # abs_url -> page, to resolve hrefs back to a Page
_pages_by_src_path = {}  # src_path -> page (Page isn't hashable, can't use it as a set element)
_manual_related = {}  # src_path -> [abs_url, ...] extracted from "Xem thêm"
_backlinks = {}  # target abs_url -> set of src_path of pages linking to it
_toi_luu_posts = []  # posts tagged "toi-luu" - hidden corner of "khac", see on_page_content

# Top-level nav order. Auto-nav (no explicit `nav:` in mkdocs.yml - see
# the comment there for why) sorts alphabetically by filename with
# directories always last, which is neither the order we want nor
# reorderable from YAML without hand-listing every post (losing prev/
# next between posts). Reordering nav.items here instead just changes
# display order - it runs *after* mkdocs already computed prev/next from
# the original order, so that's unaffected.
NAV_ORDER = [
    "index.md",
    "toi-di.md",
    "toi-doc.md",
    "toi-hoc.md",
    "toi-cam.md",
    "khac.md",
]


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
    # Prev/next between posts is already computed by this point (mkdocs
    # does that inside get_navigation(), before on_nav ever runs), so
    # trimming section.children afterwards - down to just the index
    # page itself - only affects sidebar *rendering*, not that data:
    # it collapses "Bài viết" from a ~290-item expandable section into
    # a plain link+icon (children|length == 1, so nav-item.html's "only
    # show the toggle arrow if there's more than 1 child" check hides
    # it), matching Khác/Thẻ/etc.
    for item in nav.items:
        if getattr(item, "children", None) and item.title == "Post":
            item.title = "Bài viết"
            index_child = next((c for c in item.children if getattr(c, "is_index", False)), None)
            if index_child is not None:
                item.children = [index_child]
            break

    return nav


def on_files(files, config):
    # Reset at the start of every build (including mkdocs serve rebuilds),
    # otherwise posts pile up duplicated across live-reload rebuilds.
    for key in CATEGORY_LABELS:
        _posts_by_category[key] = []
    _post_categories.clear()
    _posts_by_tag.clear()
    _post_tags.clear()
    _pages_by_url.clear()
    _pages_by_src_path.clear()
    _manual_related.clear()
    _backlinks.clear()
    _toi_luu_posts.clear()
    return files


def _resolve(href, page):
    """Turn a (possibly relative) href from page's own content into an
    absolute site path, so it can be looked up in _pages_by_url."""
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return None
    return urljoin(page.abs_url, href.split("#")[0])


def on_page_content(html, page, config, files):
    _pages_by_url[page.abs_url] = page
    _pages_by_src_path[page.file.src_path] = page

    if "date" not in page.meta:
        return html
    raw = page.meta.get("category")
    raw = raw if isinstance(raw, list) else [raw]
    # "toi-luu" isn't a real category anymore (no nav entry, no own
    # page) - posts tagged with it fall through to "khac" like any
    # other unrecognized value - but they're remembered here so the
    # "khac" page can still pull them out into their own hidden corner.
    if "toi-luu" in raw:
        _toi_luu_posts.append(page)
    keys = [k for k in raw if k in CATEGORY_LABELS] or ["khac"]
    _post_categories[page.file.src_path] = keys
    for key in keys:
        _posts_by_category[key].append(page)

    tags = page.meta.get("tags")
    if isinstance(tags, list):
        _post_tags[page.file.src_path] = tags
        for tag in tags:
            _posts_by_tag.setdefault(tag, []).append(page)

    # "Xem thêm" (> [!Example]) is now folded into "Có thể bạn sẽ thích"
    # instead of showing as its own section - extract the hrefs it
    # points to (resolved to absolute paths; matched against real pages
    # once every page has been collected) and drop the callout from the
    # rendered content entirely.
    example_match = ADMONITION_EXAMPLE.search(html)
    if example_match:
        hrefs = [_resolve(h, page) for h in LINK_TAG.findall(example_match.group(1))]
        _manual_related[page.file.src_path] = [h for h in hrefs if h]
        html = html[: example_match.start()] + html[example_match.end() :]

    # Backlinks: every other post's own outgoing links, resolved and
    # indexed by target - so render_related(page) can later ask "who
    # links to *this* page" in O(1) instead of re-scanning every post.
    for href in LINK_TAG.findall(html):
        target = _resolve(href, page)
        if target and target != page.abs_url:
            _backlinks.setdefault(target, set()).add(page.file.src_path)

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
    ".md-typeset .blog-post-author{color:var(--md-default-fg-color--light);font-size:0.85em;margin:0.2em 0}"
    ".md-typeset .blog-post-description{margin-bottom:0.8em;font-style:italic}"
    ".md-typeset .blog-post-extra{color:var(--md-default-fg-color--light)}"
    "</style>"
)


def _blog_post_list(posts, show_author=False, extra_of=None):
    """extra_of(post) -> str overrides the trailing "extra" line (date
    by default) - used by the Reading Challenge section to show a book
    total instead."""
    parts = []
    for p in posts:
        description = p.meta.get("description") or ""
        author = p.meta.get("Author") if show_author else None
        author_html = f'<div class="blog-post-author">{author}</div>' if author else ""
        extra = extra_of(p) if extra_of else p.meta["date"].strftime("%d-%m-%Y")

        parts.append(
            '<div class="blog-post">'
            f'<h2 class="blog-post-title"><a class="link" href="{p.abs_url}">{p.title}</a></h2>'
            f"{author_html}"
            f'<p class="blog-post-description">{description}</p>'
            f'<div class="blog-post-extra">{extra}</div>'
            "<hr /></div>"
        )
    return "\n".join(parts)


def render_category(key):
    posts = sorted(_posts_by_category[key], key=lambda p: p.meta["date"], reverse=True)
    if not posts:
        return STYLE + "<p><em>Chưa có bài viết nào trong mục này.</em></p>"
    return STYLE + _blog_post_list(posts)


# Photo-grid style for "toi-doc" (book covers, from the `Cover:` front
# matter field - a filename under docs/assets/img/). Posts missing a
# cover (book reviews with no cover scan) fall back to an icon + title
# tile instead of leaving a gap - not a "todo" placeholder, just a
# different valid look for a different kind of post within the category.
GRID_STYLE = (
    "<style>"
    ".cover-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(9rem,1fr));gap:1rem;margin-top:1em}"
    ".cover-grid .cover-card{display:block;color:var(--md-default-fg-color);text-decoration:none}"
    ".cover-grid .cover-thumb{width:100%;aspect-ratio:3/4;border-radius:0.2rem;overflow:hidden;"
    "background:var(--md-default-fg-color--lightest);display:flex;align-items:center;justify-content:center;"
    "transition:opacity 0.15s ease}"
    ".cover-grid .cover-thumb img{width:100%;height:100%;object-fit:cover;display:block}"
    ".cover-grid .cover-thumb svg{width:2rem;height:2rem;fill:var(--md-default-fg-color--light)}"
    # No visible title anymore - the cover alone is the tile. Title
    # still reaches the reader via the <a title=""> tooltip on hover
    # and the <img alt=""> for accessibility/screen readers - just not
    # painted on the page. Hover feedback moves to the thumb itself
    # (fade) since there's no title text to color-shift anymore.
    ".cover-grid .cover-card:hover .cover-thumb{opacity:0.8}"
    "</style>"
)
FALLBACK_ICONS = {
    "toi-doc": '<svg viewBox="0 0 24 24"><path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2m0 18H6v-2h12zm0-4H6V4h12z"/></svg>',
}


def _cards(posts, key, image_of):
    icon = FALLBACK_ICONS[key]
    parts = ['<div class="cover-grid">']
    for p in posts:
        img = image_of(p)
        thumb = f'<img src="{img}" alt="{p.title}" loading="lazy">' if img else icon
        parts.append(
            f'<a class="cover-card" href="{p.abs_url}" title="{p.title}">'
            f'<span class="cover-thumb">{thumb}</span>'
            "</a>"
        )
    parts.append("</div>")
    return "".join(parts)


# Yearly wrap-up posts ("Reading challenge 2018", ...) plus the
# undated hub page ("Reading challenge") - matched by filename, not by
# any dedicated front-matter field, since these already have a fixed,
# consistent naming convention in docs/post/ and adding a new field
# would mean touching every one of them (and the Obsidian vault they're
# synced from) for no real benefit. Anchored to a path segment (right
# after "/" or string start) so it doesn't also match unrelated posts
# that merely mention "reading challenge" in their filename, like
# "toi-khong-tham-gia-reading-challenge.md".
# The undated hub post ("Reading challenge", no year suffix) becomes
# the section's own heading/link; the yearly wrap-ups are everything
# else this regex matches.
READING_CHALLENGE_RE = re.compile(r"(?:^|/)reading-challenge(?:-\d{4})?\.md$")
READING_CHALLENGE_HUB_RE = re.compile(r"(?:^|/)reading-challenge\.md$")
# Yearly posts get published in bulk well after the fact (all nine
# were written within days of each other), so their `date` front
# matter reflects when the retrospective was *written*, not the
# reading year it's about - e.g. 2017-2022 all carry a January 2024
# publish date, and 2023 (published exactly on 2023-12-31) sorts
# *after* all of those by date even though it's a later year. Sort by
# the year in the filename instead - the one thing guaranteed correct.
READING_CHALLENGE_YEAR_RE = re.compile(r"(?:^|/)reading-challenge-(\d{4})\.md$")
# Monthly reading-log posts ("Đọc sách - T09.2024", filename
# doc-sach-YYYY-MM.md) - same filename-matching trick, grouped into
# their own "Nhật ký đọc" section instead of cluttering Review with 16+
# same-shaped, generically-titled entries.
READING_LOG_RE = re.compile(r"(?:^|/)doc-sach-\d{4}-\d{2}\.md$")
# `tongsach` (total books that YEAR - not a cross-year grand total,
# which would double-count rereads across years), as a row of block
# characters (█ full + ▌ half, ~1 full block per DOTS_PER_BOOK books,
# a half block for the remainder - a text-mode progress bar) plus the
# actual number spelled out at the end of the row.
DOTS_PER_BOOK = 5
CHALLENGE_STYLE = (
    "<style>"
    ".reading-challenge-list{list-style:none;margin:0.8em 0 0;padding:0}"
    # flex-start (not space-between) so the bar sits right next to the
    # year instead of pushed to the far edge of the row.
    ".reading-challenge-row{display:flex;justify-content:flex-start;align-items:baseline;"
    "gap:0.8em;padding:0.5em 0;border-bottom:1px solid var(--md-default-fg-color--lightest)}"
    ".reading-challenge-row:last-child{border-bottom:none}"
    ".tongsach-bar{display:flex;align-items:baseline;gap:0.5em;white-space:nowrap;flex-shrink:0}"
    ".tongsach-dots{color:var(--md-accent-fg-color);letter-spacing:0.3em;font-size:0.9em}"
    ".tongsach-total{font-size:0.8em;color:var(--md-default-fg-color--light)}"
    ".tongsach-dots--empty{color:var(--md-default-fg-color--light);letter-spacing:normal}"
    "</style>"
)


def _tongsach_blocks(total, per_block=DOTS_PER_BOOK):
    units = total / per_block
    full = int(units)
    remainder = units - full
    if full == 0:
        return "▌" if remainder > 0 else ""
    half = "▌" if remainder >= 0.5 else ""
    return "█" * full + half
# Monthly reading-log posts, compacted into a chip-grid grouped by
# year (year heading + a row of "T01".."T12" chips, one per post) -
# far more compact than 16 full title/description/date cards for what
# are all same-shaped, generically-titled monthly logs.
READING_LOG_STYLE = (
    "<style>"
    ".reading-log-year{margin-top:1.2em}"
    ".reading-log-year h3{margin:0 0 0.5em;font-size:0.95em;"
    "color:var(--md-default-fg-color--light);font-weight:600}"
    ".reading-log-months{display:flex;flex-wrap:wrap;gap:0.5em}"
    ".reading-log-months a{display:inline-block;padding:0.3em 0.8em;border-radius:0.3rem;"
    "background:var(--md-default-fg-color--lightest);color:var(--md-default-fg-color);"
    "text-decoration:none;font-size:0.85em}"
    ".reading-log-months a:hover{"
    "background:color-mix(in srgb, var(--md-accent-fg-color) 15%, transparent);"
    "color:var(--md-accent-fg-color)}"
    "</style>"
)


def _reading_log_grid(posts):
    by_year = {}
    for p in posts:
        by_year.setdefault(p.meta["date"].year, []).append(p)
    parts = []
    for year in sorted(by_year, reverse=True):
        months = sorted(by_year[year], key=lambda p: p.meta["date"])
        chips = "".join(
            f'<a href="{p.abs_url}" title="{p.title}">T{p.meta["date"].month:02d}</a>' for p in months
        )
        parts.append(
            f'<div class="reading-log-year"><h3>{year}</h3>'
            f'<div class="reading-log-months">{chips}</div></div>'
        )
    return "".join(parts)


def _reading_challenge_list(years):
    items = []
    for p in years:
        # Bare year, not the full post title ("Reading challenge
        # 2025") - shorter, reads better on a phone-width row.
        year = READING_CHALLENGE_YEAR_RE.search(p.file.src_path).group(1)
        total = p.meta.get("tongsach")
        if total:
            dots = (
                '<span class="tongsach-bar">'
                f'<span class="tongsach-dots">{_tongsach_blocks(total)}</span>'
                f'<span class="tongsach-total">{total} quyển</span>'
                "</span>"
            )
        else:
            # No `tongsach` backfilled yet - fall back to the date so
            # the row isn't left blank.
            dots = (
                '<span class="tongsach-dots tongsach-dots--empty">'
                f'{p.meta["date"].strftime("%d-%m-%Y")}</span>'
            )
        items.append(
            '<li class="reading-challenge-row">'
            f'<a href="{p.abs_url}">{year}</a>'
            f"{dots}"
            "</li>"
        )
    return f'<ul class="reading-challenge-list">{"".join(items)}</ul>'


def render_book_grid(config):
    """Tôi đọc, split in four: "Sách" (has a Cover - an actual book,
    grid of covers, A-Z by title), "Reading Challenge" (yearly
    wrap-up posts, newest first), "Nhật ký đọc" (monthly reading-log
    posts, newest first) and "Review" (everything else with no Cover -
    a reflection/review post, not itself a book scan - plain list like
    every other category, newest first)."""
    posts = _posts_by_category["toi-doc"]
    if not posts:
        return GRID_STYLE + "<p><em>Chưa có bài viết nào trong mục này.</em></p>"

    books = sorted((p for p in posts if p.meta.get("Cover")), key=lambda p: p.title)
    no_cover = [p for p in posts if not p.meta.get("Cover")]
    challenges = sorted(
        (p for p in no_cover if READING_CHALLENGE_RE.search(p.file.src_path)),
        key=lambda p: p.meta["date"],
        reverse=True,
    )
    logs = sorted(
        (p for p in no_cover if READING_LOG_RE.search(p.file.src_path)),
        key=lambda p: p.meta["date"],
        reverse=True,
    )
    special_paths = {p.file.src_path for p in challenges} | {p.file.src_path for p in logs}
    reviews = sorted(
        (p for p in no_cover if p.file.src_path not in special_paths),
        key=lambda p: p.meta["date"],
        reverse=True,
    )
    image_of = lambda p: cover_image_url(p, config)

    parts = [GRID_STYLE, STYLE]
    if books:
        parts.append(f"<h2>Sách</h2>{_cards(books, 'toi-doc', image_of)}")
    if challenges:
        # The undated hub post ("Reading challenge") becomes the
        # section's own linked heading instead of a plain "Reading
        # Challenge" text label; the dated yearly wrap-ups are listed
        # below it, newest first, each with a dot count of books read.
        hub = next((p for p in challenges if READING_CHALLENGE_HUB_RE.search(p.file.src_path)), None)
        years = sorted(
            (p for p in challenges if p is not hub),
            key=lambda p: READING_CHALLENGE_YEAR_RE.search(p.file.src_path).group(1),
            reverse=True,
        )
        heading = f'<h2><a class="link" href="{hub.abs_url}">{hub.title}</a></h2>' if hub else "<h2>Reading Challenge</h2>"
        parts.append(CHALLENGE_STYLE + heading + _reading_challenge_list(years))
    if logs:
        parts.append(READING_LOG_STYLE + f"<h2>Nhật ký đọc</h2>{_reading_log_grid(logs)}")
    if reviews:
        parts.append(f"<h2>Bài viết</h2>{_blog_post_list(reviews)}")
    return "".join(parts)


def cover_image_url(page, config):
    cover = page.meta.get("Cover")
    if not cover:
        return None
    site_path = urlsplit(config["site_url"]).path
    return f"{site_path}assets/img/{quote(cover)}"


# "Có thể bạn sẽ thích", appended to the bottom of every post, in
# priority order up to RELATED_COUNT total:
#   1. manual "Xem thêm" links (deliberately curated, always shown)
#   2. backlinks - other posts that link to this one
#   3. filled out with category/tag matches (random) if still short
# Built at build time (this runs once per build, not per page view) -
# no client-side fetch, no runtime cost per visitor.
RELATED_COUNT = 5
# Plain <ul> list, same look as "Xem thêm" (no bordered rows/card - this
# is fixed at build time, not re-randomized per page view, so it isn't
# trying to visually read as "live/dynamic" the way the old bordered-row
# style implied).
RELATED_STYLE = (
    "<style>"
    ".related-posts{margin-top:2em}"
    ".related-posts ul{margin:0.3em 0 0;padding-left:1.1em}"
    "</style>"
)
# Insert right before the "Bài ngẫu nhiên" button (overrides/partials/
# comments.html) - falls back to before comments, then end of article,
# for the rare post without comments/that button enabled.
RANDOM_BTN_ANCHOR = re.compile(r'<button id="random-post-btn"')
COMMENTS_ANCHOR = re.compile(r'<h2 id="__comments">')


def render_related(page):
    src_path = page.file.src_path
    chosen = {}  # abs_url -> page, insertion order = priority

    # 1. Manual "Xem thêm" links - always included, these were a
    # deliberate choice, not something to risk losing to random fill.
    for href in _manual_related.get(src_path, []):
        p = _pages_by_url.get(href)
        if p is not None and p is not page:
            chosen[p.abs_url] = p

    # 2. Backlinks - other posts that link to this one.
    for other_src in _backlinks.get(page.abs_url, ()):
        p = _pages_by_src_path.get(other_src)
        if p is not None and p is not page and p.abs_url not in chosen:
            chosen[p.abs_url] = p

    # 3. Fill the rest (if any slots left) from category/tag matches,
    # randomly, same as before.
    if len(chosen) < RELATED_COUNT:
        keys = _post_categories.get(src_path, [])
        tags = _post_tags.get(src_path, [])
        pool = {}
        for key in keys:
            for p in _posts_by_category.get(key, []):
                if p is not page and p.abs_url not in chosen:
                    pool[p.abs_url] = p
        for tag in tags:
            for p in _posts_by_tag.get(tag, []):
                if p is not page and p.abs_url not in chosen:
                    pool[p.abs_url] = p
        candidates = list(pool.values())
        need = RELATED_COUNT - len(chosen)
        for p in random.sample(candidates, min(need, len(candidates))):
            chosen[p.abs_url] = p

    if not chosen:
        return ""

    items = "".join(
        f'<li><a href="{p.abs_url}">{p.title}</a></li>' for p in list(chosen.values())[:RELATED_COUNT]
    )
    return (
        RELATED_STYLE
        + '<div class="related-posts">'
        + "<h2>Có thể bạn sẽ thích</h2>"
        + f"<ul>{items}</ul>"
        + "</div>"
    )


# "Tôi lưu" isn't a category of its own anymore - it's a hidden corner
# tucked inside "Khác", up top, behind a native <details>/<summary>
# toggle (closed by default: nothing gives away what's inside until
# clicked - that's the "bí ẩn" part, not just a collapsed list). No JS
# needed, it's a plain HTML disclosure widget. Compact <ul> instead of
# the full .blog-post card - just "<title> @<author>", no date.
TOI_LUU_STYLE = (
    "<style>"
    # Rather than keep fighting Material's own admonition box styling
    # on bare <details> (it kept winning out in practice, even after
    # resetting background/border/pseudo-elements individually - some
    # combination of specificity/property-level cascade kept slipping
    # through), the box is now owned outright: the wrapper div *is*
    # the visible box, description stacked inside it under "Tôi lưu"
    # so it's always shown (open or closed), no more flex-row fights
    # over the tall expanded list pushing it around.
    ".toi-luu-header{border:.075rem solid var(--md-accent-fg-color);border-radius:.2rem;"
    "padding:.6rem .8rem;margin-bottom:2em}"
    ".toi-luu-header .toi-luu-desc{margin:.5em 0 0;font-size:0.8em;font-style:italic;"
    "color:var(--md-default-fg-color--light)}"
    ".md-typeset .toi-luu-toggle{background:none;border:none;box-shadow:none;"
    "padding:0;margin:0;font-size:1em}"
    # Material's default "note" icon + chevron + light-blue pill come
    # from bare ".md-typeset summary" rules (no class needed), applied
    # via ::before/::after pseudo-elements with their own background-
    # color/mask-image - overriding just `content` on those pseudo-
    # elements left the icon/pill visible underneath (same specificity,
    # per-property cascade - "content" isn't the only property that
    # paints them). Killing both pseudo-elements outright and using a
    # plain HTML span for the arrow sidesteps all of that.
    ".md-typeset .toi-luu-toggle > summary{background:none;border:none;border-radius:0;"
    "padding:0;margin:0;font-weight:400;min-height:0;display:inline-block;"
    "cursor:pointer;color:var(--md-default-fg-color--light);font-size:0.9em;"
    "list-style:none;width:fit-content}"
    ".md-typeset .toi-luu-toggle > summary::before,"
    ".md-typeset .toi-luu-toggle > summary::after{content:none;display:none}"
    ".toi-luu-toggle summary::-webkit-details-marker{display:none}"
    ".toi-luu-toggle summary:hover{color:var(--md-accent-fg-color)}"
    ".toi-luu-arrow{display:inline-block;margin-right:0.4em;transition:transform 0.15s ease}"
    ".toi-luu-toggle[open] .toi-luu-arrow{transform:rotate(90deg)}"
    ".toi-luu-toggle ul{margin:0.6em 0 0;padding-left:1.2em}"
    ".toi-luu-toggle li{margin:0.3em 0}"
    ".toi-luu-toggle .toi-luu-author{color:var(--md-default-fg-color--light);font-size:0.85em}"
    "</style>"
)


def _toi_luu_list(posts):
    items = []
    for p in posts:
        author = p.meta.get("Author")
        author_html = f' <span class="toi-luu-author">@{author}</span>' if author else ""
        items.append(f'<li><a href="{p.abs_url}">{p.title}</a>{author_html}</li>')
    return f"<ul>{''.join(items)}</ul>"


def render_khac_page():
    toi_luu_paths = {p.file.src_path for p in _toi_luu_posts}
    main = sorted(
        (p for p in _posts_by_category["khac"] if p.file.src_path not in toi_luu_paths),
        key=lambda p: p.meta["date"],
        reverse=True,
    )
    hidden = sorted(_toi_luu_posts, key=lambda p: p.meta["date"], reverse=True)

    if not main and not hidden:
        return STYLE + "<p><em>Chưa có bài viết nào trong mục này.</em></p>"

    parts = [STYLE]
    if hidden:
        parts.append(
            TOI_LUU_STYLE
            + '<div class="toi-luu-header">'
            + '<details class="toi-luu-toggle">'
            + '<summary><span class="toi-luu-arrow">▸</span>Tôi lưu</summary>'
            + _toi_luu_list(hidden)
            + "</details>"
            + '<p class="toi-luu-desc">mấy bài hay hay trên mạng \'có thể\' bị mất</p>'
            + "</div>"
        )
    parts.append(_blog_post_list(main) if main else "<p><em>Chưa có bài viết nào trong mục này.</em></p>")
    return "".join(parts)


def render_category_page(key, config):
    if key == "toi-doc":
        return render_book_grid(config)
    if key == "khac":
        return render_khac_page()
    return render_category(key)


def on_post_page(output, page, config):
    match = PLACEHOLDER.search(output)
    if match:
        key = match.group(1)
        return PLACEHOLDER.sub(lambda _: render_category_page(key, config), output, count=1)

    if page.file.src_path in _post_categories:
        related = render_related(page)
        if related:
            anchor_match = RANDOM_BTN_ANCHOR.search(output) or COMMENTS_ANCHOR.search(output)
            insert_at = anchor_match.start() if anchor_match else output.rfind("</article>")
            if insert_at != -1:
                output = output[:insert_at] + related + output[insert_at:]

    return output
