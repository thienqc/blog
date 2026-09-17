"""Turn a curated block of images into a responsive thumbnail grid (see
.photo-grid in extra.css) instead of one full-width image per line.

Wrap the block in the note with `<!-- photo-grid:start -->` /
`<!-- photo-grid:end -->` - every image line inside becomes one grid,
any other line inside is dropped. Works straight from Obsidian, no
front matter needed; posts without the marker are untouched.

Thumbnails are emitted as pre-built `glightbox` anchors (mkdocs-glightbox
plugin) so clicking one pages through the whole gallery full-screen - the
plugin skips images already inside an <a>, so this has to match its own
markup. Paths are resolved by hand via `get_relative_url` because this is
raw HTML: mkdocs's relative-link rewriter only runs on markdown-parsed
`<img>` tags, so a source path like `../assets/img/x.webp` would end up
one directory short here (mkdocs adds a `<slug>/index.html` level).
"""
import posixpath
import re
from urllib.parse import urlsplit

from mkdocs.utils import get_relative_url

IMG_LINE = re.compile(r'^[ \t]*!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)[ \t]*$')
MARKER_BLOCK = re.compile(
    r'[ \t]*<!--\s*photo-grid:start\s*-->[ \t]*\n(.*?)\n[ \t]*<!--\s*photo-grid:end\s*-->',
    re.S,
)


def on_page_markdown(markdown, page, config, files):
    gallery = page.meta.get("filename") or page.file.src_uri

    def replace_marker(match):
        images = [
            (m.group(1), _resolve_src(m.group(2), page))
            for m in (IMG_LINE.match(line) for line in match.group(1).split("\n"))
            if m
        ]
        if not images:
            return ""
        return _render_grid(images, gallery)

    return MARKER_BLOCK.sub(replace_marker, markdown)


def _resolve_src(src, page):
    if urlsplit(src).scheme or src.startswith(("/", "#")):
        return src
    site_relative = posixpath.normpath(
        posixpath.join(posixpath.dirname(page.file.src_uri), src)
    )
    return get_relative_url(site_relative, page.file.url)


def _render_grid(images, gallery):
    items = "\n".join(
        f'  <a class="glightbox" href="{src}" data-gallery="{gallery}">'
        f'<img src="{src}" alt="{alt}" loading="lazy"></a>'
        for alt, src in images
    )
    return f'<div class="photo-grid">\n{items}\n</div>'
