"""Append a content-hash query string (?v=<hash>) to every extra_css
href, so a browser that already cached extra.css from a previous visit
is forced to re-fetch it after we edit the file - it has no hash baked
into its filename the way Material's own bundled assets do (e.g.
main.ec1eaa64.min.css), so without this, edits can silently keep
serving stale CSS to returning visitors until they hard-refresh.
"""
import hashlib
import re
from pathlib import Path

_hash_cache = {}


def _content_hash(docs_dir, rel_path):
    if rel_path not in _hash_cache:
        content = (Path(docs_dir) / rel_path).read_bytes()
        _hash_cache[rel_path] = hashlib.sha256(content).hexdigest()[:8]
    return _hash_cache[rel_path]


def on_post_page(output, page, config):
    for rel_path in config.get("extra_css", []):
        h = _content_hash(config["docs_dir"], rel_path)
        basename = re.escape(Path(rel_path).name)
        # href ends in .../extra.css regardless of how many "../" the
        # url filter prefixed for this page's depth
        pattern = re.compile(rf'(href="[^"]*{basename})"')
        output = pattern.sub(rf'\1?v={h}"', output)
    return output
