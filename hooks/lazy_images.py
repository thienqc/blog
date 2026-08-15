"""Add loading="lazy" + decoding="async" to every <img> in the rendered
HTML, except the first one per page (kept eager so it doesn't delay LCP).
Runs at build time so no post has to be edited by hand.
"""
import re

IMG_TAG = re.compile(r"<img(?![^>]*\bloading=)([^>]*)>")


def on_page_content(html, page, config, files):
    count = 0

    def add_attrs(match):
        nonlocal count
        count += 1
        attrs = match.group(1).strip()
        self_closing = attrs.endswith("/")
        if self_closing:
            attrs = attrs[:-1].strip()
        extra = "decoding=\"async\"" if count == 1 else 'loading="lazy" decoding="async"'
        close = " />" if self_closing else ">"
        return f"<img {attrs} {extra}{close}"

    return IMG_TAG.sub(add_attrs, html)
