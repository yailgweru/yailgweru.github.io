# Architecture

## What this site is

A single-page, no-build, static site hosted on GitHub Pages (`yailgweru.github.io`).
There is no bundler, no framework, no `node_modules`. Everything ships as-is.

## Rendering model

`index.html` is a shell: a fixed-position 3D scene (Three.js, loaded from a CDN
`<script>` tag) plus a handful of overlay UI elements (brand badge, tooltip,
holo-panel, story drawer). On load it fetches `data.json` and:

1. Builds SEO metadata (title, meta tags, JSON-LD `@graph`) via `applySeo()`.
2. Populates a hidden (`.sr-only`) `<main id="seo-content">` with real text
   content — this is what search engines and screen readers actually read;
   the 3D scene is decorative on top of it.
3. Builds the Three.js scene: a night-city environment with floating
   "anchor" nodes, one per section in `data.json`. Clicking an anchor opens
   a holo-panel listing that section's items; items with a `story` object
   open the slide-in story drawer (used for blog posts today).

## Data flow

`data.json` is the single source of truth for site copy, SEO fields, and the
3D anchor layout (`sections[].pos`, `.color`). `index.html` has no hardcoded
copy — everything textual comes from this file. This means most content
edits (mission text, team bios, adding a new section) only touch
`data.json`, not `index.html`.

## Blog system

Blogs are **not** part of `data.json`'s in-scene story drawer long-term —
that mechanism only holds 2-3 inline example stories. Real blog posts are
standalone HTML pages under `/blogs/*.html`, each a full document (own
`<title>`, meta description, OG tags, JSON-LD `BlogPosting`) so they're
independently indexable and shareable, unlike the SPA's in-scene drawer
content which lives behind JS execution.

- `blogs/manifest.json` — generated index of all published posts (title,
  slug, date, tags, topics, hero image, excerpt). `blogs/index.html` reads
  this to render the listing grid.
- `blogs/<slug>.html` — one static file per post, built from
  `scripts/_blog_template.html` by the (gitignored) publish script.
- `assets/blogs/<slug>/` — the post's hero image and any inline images.

See `structure.md` for the exact publish pipeline (markdown draft →
`scripts/publish_blog.py` → committed HTML + manifest + sitemap entry).

## Why HTML output instead of client-side markdown rendering

Rendering markdown in the browser (fetch + client-side parse) would mean
blog content is invisible to crawlers until JS runs and is an extra
render-blocking dependency. Pre-rendering to static HTML at authoring time
keeps every post a plain, fast, fully-indexable document — consistent with
how `#seo-content` is used on the home page.

## SEO surface

- `robots.txt` + `sitemap.xml` at root.
- Per-page canonical URL, OG/Twitter tags, JSON-LD (`Organization`,
  `WebSite`, `BlogPosting` per post).
- `sitemap.xml` must include every `blogs/<slug>.html` URL — the publish
  script appends new posts automatically; verify entries after each publish.

## Known constraints / non-goals

- No build step, on purpose — anyone should be able to open `index.html`
  directly or serve the folder with any static file server.
- Three.js is loaded from cdnjs, not vendored — acceptable tradeoff for
  now (cache-friendly, one less binary to maintain in-repo) but is a
  single point of failure for the 3D scene if the CDN is down; the
  `#seo-content` fallback and blog pages are unaffected either way.
