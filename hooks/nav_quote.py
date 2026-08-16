"""Mark the "day-sequence nav" blockquote pattern
(> **[Ngày 20](...) 👈 [XV23](...) 👉 [Ngày 22](...)**) with a class so
CSS can render it as a slim, borderless single-line bar instead of a
regular quote - detected by content (has 👈 and/or 👉), not by changing
how it's authored in Obsidian; it's still a plain blockquote, same as
always. Either arrow alone counts too, for the first/last day in a
series (no previous/next day to link to) - it should look the same
slim way, not fall back to the boxed quote style.
"""
import re

BLOCKQUOTE = re.compile(r"<blockquote>(.*?)</blockquote>", re.S)


def on_page_content(html, page, config, files):
    def mark(match):
        inner = match.group(1)
        if "👈" in inner or "👉" in inner:
            return f'<blockquote class="nav-quote">{inner}</blockquote>'
        return match.group(0)

    return BLOCKQUOTE.sub(mark, html)
