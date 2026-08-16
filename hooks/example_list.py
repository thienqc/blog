"""Turn the body of every "Xem thêm" callout (> [!Example]) into a real
<ul><li> list, so every link gets its own bullet - regardless of how it
was authored: multiple links on consecutive `> ` lines with no blank
line between them render as ONE <p> with the links joined by <br/>, not
separate <p> tags, so a plain CSS ::before-per-<p> bullet only hits the
first line. Splitting on <br/> and wrapping each piece (and each
separate <p>, if there happen to be several) in its own <li> handles
every case uniformly and lets normal <ul> bullet styling do the rest.
"""
import re

ADMONITION_EXAMPLE = re.compile(r'<div class="admonition example">(.*?)</div>', re.S)
TITLE = re.compile(r'<p class="admonition-title">.*?</p>', re.S)
PARA = re.compile(r"<p>(.*?)</p>", re.S)
BR = re.compile(r"\s*<br\s*/?>\s*")


def convert(match):
    inner = match.group(1)
    title_match = TITLE.search(inner)
    title_html = title_match.group(0) if title_match else ""
    rest = inner[title_match.end() :] if title_match else inner

    items = []
    for para_match in PARA.finditer(rest):
        for piece in BR.split(para_match.group(1)):
            piece = piece.strip()
            if piece:
                items.append(piece)

    if not items:
        return match.group(0)

    list_html = "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"
    return f'<div class="admonition example">{title_html}{list_html}</div>'


def on_page_content(html, page, config, files):
    return ADMONITION_EXAMPLE.sub(convert, html)
