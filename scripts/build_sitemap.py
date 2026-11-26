#!/usr/bin/env python3
"""Regenerate sitemap.xml from every real page on the site.

Lists /, /blogs/, every published post, and every person and project page
(build_pages.py). Those standalone pages aren't linked from the site — the
sitemap is how search engines find them.
<lastmod> is the date of the last commit that touched the page's file, or
today if that file has uncommitted changes, so it stays accurate without
hand-editing. Runs last in `python scripts/update_site.py`, after every other
step has rewritten its files.
"""
import subprocess
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

from site_content import ROOT, SITE_ROOT, load

SITEMAP = ROOT / "sitemap.xml"
TODAY = date.today().isoformat()


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def lastmod(path):
    if git("status", "--porcelain", "--", path):
        return TODAY
    return git("log", "-1", "--format=%cs", "--", path) or TODAY


def main():
    # (loc path, file that holds the page, changefreq, priority)
    site = load()
    urls = [("", "index.html", "weekly", "1.0"), ("blogs/", "blogs/index.html", "weekly", "0.8")]
    for post in site.posts:
        page = f"blogs/{post['slug']}.html"
        urls.append((page, page, "monthly", "0.7"))
    for entry in site.projects:
        urls.append((entry["page"], entry["page"], "monthly", "0.6"))
    for entry in site.team:
        urls.append((entry["page"], entry["page"], "monthly", "0.5"))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, file, freq, prio in urls:
        if not (ROOT / file).exists():
            print(f"WARNING: skipping /{loc} — {file} does not exist")
            continue
        lines += [
            "  <url>",
            f"    <loc>{escape(SITE_ROOT + '/' + loc)}</loc>",
            f"    <lastmod>{lastmod(file)}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{prio}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    text = "\n".join(lines) + "\n"

    if SITEMAP.exists() and SITEMAP.read_text(encoding="utf-8") == text:
        print("sitemap.xml already up to date.")
        return
    SITEMAP.write_text(text, encoding="utf-8")
    print(f"sitemap.xml written ({len(urls)} URLs).")


if __name__ == "__main__":
    main()
