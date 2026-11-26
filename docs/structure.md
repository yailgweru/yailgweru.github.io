# Repo structure

The authoritative, up-to-date repo layout lives in `CLAUDE.md` → "Repo
layout", next to the workflows that produce each file. This note only
summarizes how the pieces relate.

## Sources you edit (build inputs — the browser never reads them)

| Source | What it holds |
|---|---|
| `data.json` | Site copy, SEO fields, section anchors, forms, Firebase config |
| `data/team/<slug>.json` | One person (leadership or member) |
| `data/projects/<slug>.json` | One project (community- or member-owned) |
| `blogs/<slug>.md` (local only, gitignored) | A blog post draft |
| `assets/logo.png`, `assets/team/`, `assets/projects/` | Logo and photos |

## Files that are generated (never hand-edit)

| Output | Made by |
|---|---|
| `team/*.html`, `projects/*.html` (SEO landing pages, not linked) | `scripts/build_pages.py` |
| `blogs/<slug>.html`, `blogs/manifest.json`, `assets/blogs/<slug>/` | `scripts/publish_blog.py` |
| `firebase/firestore.rules` | `scripts/build_form_rules.py` |
| Marker blocks in `index.html` (incl. the `#hub-content` tree) and `blogs/index.html` | `prerender_seo.py`, `inline_logo.py` |
| `feed.xml` (RSS) | `scripts/build_feed.py` |
| `sitemap.xml` | `scripts/build_sitemap.py` |
| `assets/favicon/*` | `scripts/make_favicons.py` |

`python scripts/update_site.py` runs every generator except
`publish_blog.py`, in the right order.

## Why blog drafts stay local

GitHub Pages runs Jekyll, which publishes any pushed `.md` file as a page.
A pushed draft became a duplicate, unlinked copy of its own post, so drafts
are gitignored and only the compiled HTML is pushed (steering D-24).
