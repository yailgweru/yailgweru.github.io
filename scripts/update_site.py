#!/usr/bin/env python3
"""One-command sync of every generated block in the site.

Chains the individual sync scripts in the right order so a content edit
(data.json, a new/edited blog post, or a logo change) always leaves every
generated block consistent, instead of relying on remembering which
scripts to rerun by hand:

    python scripts/update_site.py

Steps, always run:
  1. prerender_seo.py  - bakes SEO head/JSON-LD/#seo-content into index.html
                          and the static blog-card list into blogs/index.html
  2. inline_data.py    - resyncs data.json into index.html's file:// fallback
  3. inline_logo.py    - resyncs assets/logo.png into index.html's inline
                          WebGL texture data URI

Favicons (assets/favicon/*) are only regenerated from assets/logo.png when
needed - either pass --favicons to force it, or let this script notice
logo.png is newer than the generated favicon set and do it automatically.
Pass --no-favicons to skip that check entirely.

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

ALWAYS_STEPS = ["prerender_seo.py", "inline_data.py", "inline_logo.py"]


def run_step(name):
    print(f"\n==> {name}")
    result = subprocess.run([sys.executable, str(SCRIPTS / name)], cwd=ROOT)
    if result.returncode != 0:
        print(f"\n{name} failed (exit {result.returncode}) - stopping.", file=sys.stderr)
        sys.exit(result.returncode)


def favicons_are_stale():
    if not LOGO_PNG.exists():
        return False
    if not FAVICON_DIR.exists():
        return True
    favicon_files = list(FAVICON_DIR.glob("*"))
    if not favicon_files:
        return True
    newest_favicon = max(f.stat().st_mtime for f in favicon_files)
    return LOGO_PNG.stat().st_mtime > newest_favicon


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--favicons", action="store_true", help="force-regenerate assets/favicon/* from logo.png")
    parser.add_argument("--no-favicons", action="store_true", help="skip the favicon staleness check entirely")
    args = parser.parse_args()

    if args.favicons and args.no_favicons:
        parser.error("--favicons and --no-favicons are mutually exclusive")

    for step in ALWAYS_STEPS:
        run_step(step)

    if args.favicons:
        run_step("make_favicons.py")
    elif not args.no_favicons and favicons_are_stale():
        print("\nassets/logo.png is newer than assets/favicon/* - regenerating favicons.")
        run_step("make_favicons.py")

    print("\nSite is up to date.")


if __name__ == "__main__":
    main()
