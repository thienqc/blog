#!/usr/bin/env python3
"""Scan docs/assets/ebook/*.epub and (re)generate manifest.json + cover images.

Run this after adding/removing an .epub file in docs/assets/ebook/, then
commit the updated manifest.json (and any new covers/*.jpg) along with the
epub itself. Requires Pillow (./.venv/bin/python -m pip install Pillow).

Title/author/description are only auto-extracted for books not already in
manifest.json — if you hand-edit those fields for an existing book, re-running
this script won't overwrite them (size/cover/slug still refresh).

    ./.venv/bin/python scripts/build-ebook-manifest.py
"""
import html
import io
import json
import os
import re
import sys
import unicodedata
import zipfile

from PIL import Image

COVER_MAX_SIZE = (480, 720)
COVER_JPEG_QUALITY = 85

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EBOOK_DIR = os.path.join(ROOT, "docs", "assets", "ebook")
COVERS_DIR = os.path.join(EBOOK_DIR, "covers")
MANIFEST_PATH = os.path.join(EBOOK_DIR, "manifest.json")

NS = r'(?:[a-zA-Z][\w.-]*:)?'  # optional namespace prefix, e.g. dc:


def slugify(name):
    base = unicodedata.normalize("NFKD", name)
    base = base.encode("ascii", "ignore").decode("ascii")
    base = re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower()
    return base or "book"


def strip_html(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_opf_path(zf):
    container = zf.read("META-INF/container.xml").decode("utf-8", "ignore")
    m = re.search(r'full-path="([^"]+)"', container)
    if not m:
        raise ValueError("container.xml missing rootfile full-path")
    return m.group(1)


def extract_metadata(opf_data):
    def tag(name):
        m = re.search(rf"<{NS}{name}[^>]*>(.*?)</{NS}{name}>", opf_data, re.S)
        return strip_html(m.group(1)) if m else ""

    title = tag("title")
    author = tag("creator")
    description = tag("description")
    return title, author, description


def find_cover_href(opf_data):
    m = re.search(r'<meta[^>]*name="cover"[^>]*content="([^"]+)"', opf_data)
    if m:
        cover_id = m.group(1)
        m2 = re.search(rf'<item[^>]*id="{re.escape(cover_id)}"[^>]*href="([^"]+)"', opf_data)
        if not m2:
            m2 = re.search(rf'<item[^>]*href="([^"]+)"[^>]*id="{re.escape(cover_id)}"', opf_data)
        if m2:
            return m2.group(1)
    m = re.search(r'<item[^>]*properties="[^"]*cover-image[^"]*"[^>]*href="([^"]+)"', opf_data)
    if m:
        return m.group(1)
    m = re.search(r'<item[^>]*href="([^"]+)"[^>]*properties="[^"]*cover-image[^"]*"', opf_data)
    if m:
        return m.group(1)
    return None


def process_epub(filename):
    path = os.path.join(EBOOK_DIR, filename)
    size = os.path.getsize(path)
    with zipfile.ZipFile(path) as zf:
        opf_path = find_opf_path(zf)
        opf_data = zf.read(opf_path).decode("utf-8", "ignore")
        title, author, description = extract_metadata(opf_data)
        cover_href = find_cover_href(opf_data)

        cover_rel = None
        if cover_href:
            opf_dir = os.path.dirname(opf_path)
            cover_zip_path = os.path.normpath(os.path.join(opf_dir, cover_href)).replace("\\", "/")
            try:
                cover_bytes = zf.read(cover_zip_path)
            except KeyError:
                cover_bytes = None
            if cover_bytes:
                cover_name = f"{slugify(os.path.splitext(filename)[0])}.jpg"
                os.makedirs(COVERS_DIR, exist_ok=True)
                img = Image.open(io.BytesIO(cover_bytes)).convert("RGB")
                img.thumbnail(COVER_MAX_SIZE, Image.LANCZOS)
                img.save(os.path.join(COVERS_DIR, cover_name), "JPEG", quality=COVER_JPEG_QUALITY)
                cover_rel = f"covers/{cover_name}"

    if not title:
        title = os.path.splitext(filename)[0]

    return {
        "file": filename,
        "slug": slugify(os.path.splitext(filename)[0]),
        "title": title,
        "author": author,
        "description": description,
        "cover": cover_rel,
        "size": size,
    }


def main():
    if not os.path.isdir(EBOOK_DIR):
        print(f"Không tìm thấy thư mục {EBOOK_DIR}", file=sys.stderr)
        sys.exit(1)

    epubs = sorted(f for f in os.listdir(EBOOK_DIR) if f.lower().endswith(".epub"))
    if not epubs:
        print("Không có file .epub nào.")
        json.dump([], open(MANIFEST_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        return

    existing_by_file = {}
    if os.path.isfile(MANIFEST_PATH):
        with open(MANIFEST_PATH, encoding="utf-8") as f:
            for entry in json.load(f):
                existing_by_file[entry["file"]] = entry

    entries = []
    for filename in epubs:
        prior = existing_by_file.get(filename)
        if prior:
            print(f"Đã có sẵn, giữ nguyên tiêu đề/tác giả/mô tả: {filename}")
            entry = process_epub(filename)
            entry["slug"] = prior.get("slug", entry["slug"])
            entry["title"] = prior.get("title", entry["title"])
            entry["author"] = prior.get("author", entry["author"])
            entry["description"] = prior.get("description", entry["description"])
        else:
            print(f"Sách mới, đang trích metadata: {filename}")
            entry = process_epub(filename)
        entries.append(entry)

    entries.sort(key=lambda e: e["title"].lower())

    seen_slugs = {}
    for entry in entries:
        base = entry["slug"]
        seen_slugs[base] = seen_slugs.get(base, 0) + 1
        if seen_slugs[base] > 1:
            entry["slug"] = f"{base}-{seen_slugs[base]}"

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Đã ghi {MANIFEST_PATH} ({len(entries)} sách).")


if __name__ == "__main__":
    main()
