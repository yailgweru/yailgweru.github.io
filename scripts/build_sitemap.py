#!/usr/bin/env python3
"""Regenerate sitemap.xml from every real page on the site.

Lists /, /blogs/, every published post, and every person and project page
(build_pages.py). Those standalone pages aren't linked from the site — the
sitemap is how search engines find them. Person and project pages also list
their photo/image (Google's image sitemap extension), so people can turn up
in image search too.
<lastmod> is the date of the last commit that touched the page's file, or
today if that file has uncommitted changes, so it stays accurate without
hand-editing. Runs last in `python scripts/update_site.py`, after every other
step has rewritten its files.
"""
from xml.sax.saxutils import escape

from images import largest
from site_content import ROOT, SITE_ROOT, is_external, lastmod, load

SITEMAP = ROOT / "sitemap.xml"


def image_url(entry, variants_key):
    """Absolute URL of the entry's largest image variant (or its external image)."""
    if entry.get(variants_key):
        return f"{SITE_ROOT}/{largest(entry[variants_key])['src']}"
    return entry["image"] if is_external(entry.get("image")) else ""


def main():
    # (loc path, file that holds the page, changefreq, priority, image URL)
    site = load()
    urls = [("", "index.html", "weekly", "1.0", ""), ("blogs/", "blogs/index.html", "weekly", "0.8", "")]
    for post in site.posts:
        page = f"blogs/{post['slug']}.html"
        urls.append((page, page, "monthly", "0.7", ""))
    for entry in site.projects:
        urls.append((entry["page"], entry["page"], "monthly", "0.6", image_url(entry, "hero")))
    for entry in site.team:
        urls.append((entry["page"], entry["page"], "monthly", "0.5", image_url(entry, "photo")))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]
    for loc, file, freq, prio, image in urls:
        if not (ROOT / file).exists():
            print(f"WARNING: skipping /{loc} — {file} does not exist")
            continue
        lines += [
            "  <url>",
            f"    <loc>{escape(SITE_ROOT + '/' + loc)}</loc>",
            f"    <lastmod>{lastmod(file)}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{prio}</priority>",
        ]
        if image:
            lines.append(f"    <image:image><image:loc>{escape(image)}</image:loc></image:image>")
        lines.append("  </url>")
    lines.append("</urlset>")
    text = "\n".join(lines) + "\n"

    if SITEMAP.exists() and SITEMAP.read_text(encoding="utf-8") == text:
        print("sitemap.xml already up to date.")
        return
    SITEMAP.write_text(text, encoding="utf-8")
    print(f"sitemap.xml written ({len(urls)} URLs).")


if __name__ == "__main__":
    main()
