#!/usr/bin/env python3
"""One-command sync of every generated block in the site.

Chains the individual sync scripts in the right order so a content edit
(data.json, data/team, data/projects, a new/edited blog post, or a logo
change) always leaves every generated file consistent, instead of relying
on remembering which scripts to rerun by hand:

    python scripts/update_site.py

The JSON files are build inputs only; the browser never reads them. These
steps render them into HTML/XML, always run, in this order:
  1. build_pages.py      - standalone SEO pages team/<slug>.html and
                            projects/<slug>.html from data/team and data/projects
  2. build_form_rules.py - firebase/firestore.rules from the forms in data.json
  3. prerender_seo.py    - index.html's head, JSON-LD, brand bar and the full
                            #hub-content tree (every section, item and sidebar
                            panel), plus the blog cards in blogs/index.html
  4. build_feed.py       - feed.xml, the RSS feed of blog posts
  5. build_llms.py       - llms.txt, the site map for AI answer engines (GEO)
  6. build_sitemap.py    - regenerates sitemap.xml from every real page (last,
                            so its lastmod dates see every file the steps
                            above rewrote)

The files derived from assets/logo.png (the tinified favicon set,
assets/logo-texture.js - the 3D scene's logo texture - and assets/share.jpg,
the share image) are only regenerated
when needed - either pass --favicons to force it, or let this script notice
logo.png is newer than them (or one is missing) and run make_favicons.py
automatically. Pass --no-favicons to skip that check entirely.

Does NOT run publish_blog.py - that's the interactive markdown -> HTML
pipeline for authoring one new post (`python scripts/publish_blog.py
blogs/<slug>.md`), not a resync step, and it's gitignored/local-only.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
LOGO_PNG = ROOT / "assets" / "logo.png"
FAVICON_DIR = ROOT / "assets" / "favicon"
# Single files make_favicons.py derives from logo.png (besides assets/favicon/).
LOGO_FILES = [ROOT / "assets" / "logo-texture.js", ROOT / "assets" / "share.jpg"]

ALWAYS_STEPS = ["build_pages.py", "build_form_rules.py", "prerender_seo.py", "build_feed.py", "build_llms.py"]
LAST_STEP = "build_sitemap.py"


def run_step(name):
    print(f"\n==> {name}")
    result = subprocess.run([sys.executable, str(SCRIPTS / name)], cwd=ROOT)
    if result.returncode != 0:
        print(f"\n{name} failed (exit {result.returncode}) - stopping.", file=sys.stderr)
        sys.exit(result.returncode)


def favicons_are_stale():
    if not LOGO_PNG.exists():
        return False
    if not FAVICON_DIR.exists() or not all(f.exists() for f in LOGO_FILES):
        return True
    favicon_files = list(FAVICON_DIR.glob("*"))
    if not favicon_files:
        return True
    newest_favicon = max(f.stat().st_mtime for f in favicon_files)
    logo_time = LOGO_PNG.stat().st_mtime
    return logo_time > newest_favicon or any(logo_time > f.stat().st_mtime for f in LOGO_FILES)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--favicons", action="store_true", help="force-regenerate assets/favicon/*, assets/logo-texture.js and assets/share.jpg from logo.png")
    parser.add_argument("--no-favicons", action="store_true", help="skip the favicon staleness check entirely")
    args = parser.parse_args()

    if args.favicons and args.no_favicons:
        parser.error("--favicons and --no-favicons are mutually exclusive")

    for step in ALWAYS_STEPS:
        run_step(step)

    if args.favicons:
        run_step("make_favicons.py")
    elif not args.no_favicons and favicons_are_stale():
        print("\nassets/logo.png is newer than its favicons/texture - regenerating them.")
        run_step("make_favicons.py")

    run_step(LAST_STEP)
    print("\nSite is up to date.")


if __name__ == "__main__":
    main()
