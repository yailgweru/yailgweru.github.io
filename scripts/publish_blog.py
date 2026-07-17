#!/usr/bin/env python3
"""
Publish a markdown draft (blogs/<slug>.md) as a static blog post
(blogs/<slug>.html), wiring up its images, manifest entry and sitemap entry.

This script itself is gitignored and stays local — only needed to author a
new post. Its input (blogs/*.md) and output (blogs/*.html, assets/blogs/*,
blogs/manifest.json, sitemap.xml) are all committed, so blogs/ is the
complete source of truth for every post, source and compiled alike. See
docs/structure.md for the full pipeline contract and CLAUDE.md for the
authoring workflow.

Usage:
    python scripts/publish_blog.py blogs/teaching-ai-in-our-own-languages.md
    python scripts/publish_blog.py blogs/*.md   (shell-expanded, publishes each)

Requires: PyYAML, Markdown  (pip install pyyaml markdown)
"""
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
BLOGS_DIR = ROOT / "blogs"
ASSETS_BLOGS_DIR = ROOT / "assets" / "blogs"
TEMPLATE_PATH = ROOT / "scripts" / "_blog_template.html"
MANIFEST_PATH = BLOGS_DIR / "manifest.json"
SITEMAP_PATH = ROOT / "sitemap.xml"
SITE_ROOT = "https://yailgweru.github.io"

REQUIRED_FIELDS = ["title", "date", "topics", "tags", "image"]


def slugify(text):
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    return re.sub(r"[\s_-]+", "-", text)


def parse_frontmatter(md_path):
    raw = md_path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise ValueError(f"{md_path} is missing YAML frontmatter (must start with '---').")
    parts = raw.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{md_path} has malformed frontmatter (need opening and closing '---').")
    meta = yaml.safe_load(parts[1]) or {}
    body = parts[2].strip()
    if not body:
        raise ValueError(f"{md_path} has no body content after the frontmatter.")

    missing = [f for f in REQUIRED_FIELDS if not meta.get(f)]
    if missing:
        raise ValueError(f"{md_path} frontmatter is missing required field(s): {', '.join(missing)}")

    meta["slug"] = slugify(str(meta.get("slug") or meta["title"]))
    meta.setdefault("author", "Hub Team")
    meta.setdefault("excerpt", "")
    if isinstance(meta["tags"], str):
        meta["tags"] = [t.strip() for t in meta["tags"].split(",") if t.strip()]
    if isinstance(meta["topics"], str):
        meta["topics"] = [t.strip() for t in meta["topics"].split(",") if t.strip()]

    date_obj = meta["date"]
    if not isinstance(date_obj, datetime):
        date_obj = datetime.strptime(str(date_obj), "%Y-%m-%d")
    meta["date_obj"] = date_obj

    return meta, body


IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")


def localize_images(body, meta, draft_dir, out_img_dir):
    """Copy every locally-referenced image into assets/blogs/<slug>/ and
    rewrite the markdown to point at the new location (relative to blogs/)."""
    seen = {}

    def repl(match):
        alt, src = match.group(1), match.group(2)
        if re.match(r"^https?://", src):
            return match.group(0)
        if src not in seen:
            src_path = (draft_dir / src).resolve()
            if not src_path.is_file():
                raise FileNotFoundError(f"Image referenced in markdown not found: {src_path}")
            out_img_dir.mkdir(parents=True, exist_ok=True)
            dest = out_img_dir / src_path.name
            shutil.copyfile(src_path, dest)
            seen[src] = f"../assets/blogs/{meta['slug']}/{src_path.name}"
        return f"![{alt}]({seen[src]})"

    new_body = IMG_RE.sub(repl, body)

    # Hero image (frontmatter `image:`) — copy + resolve the same way.
    hero_src = str(meta["image"])
    if re.match(r"^https?://", hero_src):
        hero_rel = hero_src
        hero_abs = hero_src
    else:
        if hero_src in seen:
            hero_rel = seen[hero_src]
        else:
            src_path = (draft_dir / hero_src).resolve()
            if not src_path.is_file():
                raise FileNotFoundError(f"Frontmatter `image` not found: {src_path}")
            out_img_dir.mkdir(parents=True, exist_ok=True)
            dest = out_img_dir / src_path.name
            shutil.copyfile(src_path, dest)
            hero_rel = f"../assets/blogs/{meta['slug']}/{src_path.name}"
        hero_abs = f"{SITE_ROOT}/{hero_rel.replace('../', '')}"
    meta["image_rel"] = hero_rel
    meta["image_abs"] = hero_abs
    return new_body


def build_json_ld(meta, canonical):
    graph = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": meta["title"],
        "description": meta["excerpt"],
        "image": meta["image_abs"],
        "datePublished": meta["date_obj"].strftime("%Y-%m-%d"),
        "author": {"@type": "Organization", "name": meta["author"]},
        "publisher": {
            "@type": "Organization",
            "name": "Young AI Leaders — Gweru Hub",
            "logo": {"@type": "ImageObject", "url": f"{SITE_ROOT}/assets/logo.png"},
        },
        "keywords": ", ".join(meta["tags"] + meta["topics"]),
        "articleSection": meta["topics"][0] if meta["topics"] else "",
        "mainEntityOfPage": canonical,
    }
    return json.dumps(graph, indent=2)


def render_post(meta, body_html, canonical):
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    tag_pills = "".join(f'<span class="tag">#{xml_escape(t)}</span>' for t in meta["tags"])
    topic_tags = "\n".join(f'<meta property="article:tag" content="{xml_escape(t)}">' for t in meta["tags"] + meta["topics"])
    replacements = {
        "{{TITLE}}": xml_escape(meta["title"]),
        "{{EXCERPT}}": xml_escape(meta["excerpt"]),
        "{{TAGS_CSV}}": xml_escape(", ".join(meta["tags"] + meta["topics"])),
        "{{AUTHOR}}": xml_escape(meta["author"]),
        "{{CANONICAL}}": canonical,
        "{{IMAGE_ABS}}": meta["image_abs"],
        "{{IMAGE_REL}}": meta["image_rel"],
        "{{DATE_ISO}}": meta["date_obj"].strftime("%Y-%m-%d"),
        "{{DATE_DISPLAY}}": meta["date_obj"].strftime("%-d %B %Y") if sys.platform != "win32" else meta["date_obj"].strftime("%#d %B %Y"),
        "{{TAG_PILLS}}": tag_pills,
        "{{TOPIC_TAGS}}": topic_tags,
        "{{JSON_LD}}": build_json_ld(meta, canonical),
        "{{CONTENT_HTML}}": body_html,
    }
    for token, value in replacements.items():
        template = template.replace(token, value)
    return template


def update_manifest(meta):
    posts = json.loads(MANIFEST_PATH.read_text(encoding="utf-8")) if MANIFEST_PATH.exists() else []
    posts = [p for p in posts if p["slug"] != meta["slug"]]
    posts.append({
        "slug": meta["slug"],
        "title": meta["title"],
        "date": meta["date_obj"].strftime("%Y-%m-%d"),
        "author": meta["author"],
        "topics": meta["topics"],
        "tags": meta["tags"],
        "image": meta["image_rel"].replace("../", ""),
        "excerpt": meta["excerpt"],
    })
    posts.sort(key=lambda p: p["date"], reverse=True)
    MANIFEST_PATH.write_text(json.dumps(posts, indent=2) + "\n", encoding="utf-8")


def update_sitemap(canonical):
    text = SITEMAP_PATH.read_text(encoding="utf-8")
    if canonical in text:
        return
    entry = f"  <url>\n    <loc>{canonical}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n"
    text = text.replace("</urlset>", entry + "</urlset>")
    SITEMAP_PATH.write_text(text, encoding="utf-8")


def publish(md_path):
    md_path = Path(md_path).resolve()
    meta, body = parse_frontmatter(md_path)
    slug = meta["slug"]
    out_img_dir = ASSETS_BLOGS_DIR / slug
    body = localize_images(body, meta, md_path.parent, out_img_dir)

    body_html = markdown.markdown(body, extensions=["fenced_code", "tables", "footnotes"])
    canonical = f"{SITE_ROOT}/blogs/{slug}.html"

    BLOGS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = BLOGS_DIR / f"{slug}.html"
    out_path.write_text(render_post(meta, body_html, canonical), encoding="utf-8")

    update_manifest(meta)
    update_sitemap(canonical)

    print(f"Published: {out_path.relative_to(ROOT)}")
    print(f"Hero image: {out_img_dir.relative_to(ROOT)}/{Path(meta['image_rel']).name}")
    print("Updated: blogs/manifest.json, sitemap.xml")
    title = meta["title"]
    print("\nNext: review the output, then commit —")
    print(f'  git add {md_path.relative_to(ROOT)} blogs/{slug}.html assets/blogs/{slug} blogs/manifest.json sitemap.xml')
    print(f'  git commit -m "Add blog post: {title}"')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for arg in sys.argv[1:]:
        publish(arg)
