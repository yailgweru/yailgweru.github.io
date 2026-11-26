#!/usr/bin/env python3
"""Generate feed.xml: an RSS 2.0 feed of the published blog posts.

Built from blogs/manifest.json plus each post's compiled page
(blogs/<slug>.html), whose .content block becomes the item's full text
(content:encoded). Item links open the post in the home page's sidebar
(/#blogs/<slug>), the same place every other link on the site points.
Advertised to feed readers by <link rel="alternate"> in the page heads.
Runs as part of `python scripts/update_site.py`.
"""
import mimetypes
import re
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape

from site_content import ROOT, SITE_ROOT, load

FEED = ROOT / "feed.xml"
ZIMBABWE = timezone(timedelta(hours=2))
TITLE = "Young AI Leaders Gweru Hub — Blog"
DESCRIPTION = "Stories from the Young AI Leaders Gweru Hub: projects, workshops and lessons from building AI in Gweru, Zimbabwe and Southern Africa."


def rfc822(date_str):
    return format_datetime(datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=ZIMBABWE))


def post_content(slug):
    """The post page's .content block with site-absolute URLs, or '' if missing."""
    path = ROOT / "blogs" / f"{slug}.html"
    if not path.exists():
        return ""
    match = re.search(r'<div class="content">(.*?)\n  </div>', path.read_text(encoding="utf-8"), re.DOTALL)
    if not match:
        return ""
    body = re.sub(r'(src|href)="\.\./', lambda m: f'{m.group(1)}="{SITE_ROOT}/', match.group(1).strip())
    body = re.sub(r'srcset="([^"]*)"', lambda m: 'srcset="' + m.group(1).replace("../", SITE_ROOT + "/") + '"', body)
    return body.replace("]]>", "]]]]><![CDATA[>")


def enclosure(image):
    path = ROOT / image
    if not image or not path.is_file():
        return ""
    kind = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    return f'      <enclosure url="{escape(SITE_ROOT + "/" + image)}" length="{path.stat().st_size}" type="{kind}"/>\n'


def render_feed(posts, content_for=post_content):
    items = []
    for p in posts:
        link = f"{SITE_ROOT}/#blogs/{p['slug']}"
        body = content_for(p["slug"])
        items.append(
            "    <item>\n"
            f"      <title>{escape(p['title'])}</title>\n"
            f"      <link>{escape(link)}</link>\n"
            f'      <guid isPermaLink="false">yailgweru-blog-{escape(p["slug"])}</guid>\n'
            f"      <pubDate>{rfc822(p['date'])}</pubDate>\n"
            + (f"      <dc:creator>{escape(p['author'])}</dc:creator>\n" if p.get("author") else "")
            + "".join(f"      <category>{escape(t)}</category>\n" for t in p.get("topics") or [])
            + f"      <description>{escape(p.get('excerpt', ''))}</description>\n"
            + (f"      <content:encoded><![CDATA[{body}]]></content:encoded>\n" if body else "")
            + enclosure(p.get("image", ""))
            + "    </item>\n"
        )
    last = f"    <lastBuildDate>{rfc822(posts[0]['date'])}</lastBuildDate>\n" if posts else ""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" '
        'xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        "  <channel>\n"
        f"    <title>{escape(TITLE)}</title>\n"
        f"    <link>{SITE_ROOT}/#blogs</link>\n"
        f'    <atom:link href="{SITE_ROOT}/feed.xml" rel="self" type="application/rss+xml"/>\n'
        f"    <description>{escape(DESCRIPTION)}</description>\n"
        "    <language>en-zw</language>\n"
        # RSS caps the channel image at 144px wide: the tinified 96px favicon.
        f"    <image>\n      <url>{SITE_ROOT}/assets/favicon/favicon-96x96.png</url>\n      <title>{escape(TITLE)}</title>\n"
        f"      <link>{SITE_ROOT}/#blogs</link>\n      <width>96</width>\n      <height>96</height>\n    </image>\n"
        f"{last}"
        + "".join(items)
        + "  </channel>\n</rss>\n"
    )


def main():
    text = render_feed(load().posts)
    if FEED.exists() and FEED.read_text(encoding="utf-8") == text:
        print("feed.xml already up to date.")
        return
    FEED.write_text(text, encoding="utf-8")
    print("feed.xml written.")


if __name__ == "__main__":
    main()
