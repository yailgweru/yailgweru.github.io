# CLAUDE.md

Instructions for whoever (human or Claude) works on this repository —
Young AI Leaders Gweru Hub, a static site served from GitHub Pages at
`https://yailgweru.github.io/`.

## What this is

A no-build, static site. `index.html` is a single-page app: a Three.js
night-city scene (loaded from a CDN `<script>` tag) with floating "anchor"
nodes for each content section, plus a hidden `#seo-content` block that
holds the same content as real, crawlable HTML/text. **`data.json` is the
single source of truth for site copy, SEO metadata, and the 3D anchor
layout** — `index.html` has no hardcoded copy. Most content edits (mission
text, team bios, adding a section) only touch `data.json`.

There is no bundler, no `node_modules`, no build step — but `index.html`
loads its content with `fetch()` (`data.json`, `blogs/manifest.json`, and
per-post HTML for the read-more sidebar), and browsers block `fetch()`
under the `file://` origin. **Double-clicking `index.html` will not
work** — it fails silently with CORS errors on every fetch. Serve the
repo root with any static file server instead, e.g.:

```
python -m http.server 8000    # then open http://localhost:8000/
```

Any other static server (`npx serve`, VS Code Live Server, etc.) works
the same way — the only requirement is `http://`/`https://`, not `file://`.

## Repo layout

```
index.html              # app shell — 3D scene + overlay UI, reads data.json
data.json                # all copy, SEO fields, 3D anchor positions/colors
robots.txt / sitemap.xml # sitemap.xml must list every page, including each blog post

assets/
  logo.png                # source logo — regenerate favicons from this if it changes
  favicon/                  # generated favicon set + site.webmanifest (committed)
  fonts/                     # self-hosted fonts live here if/when added (committed)
  blogs/<slug>/               # hero + inline images per blog post (committed)

blogs/                     # the single source of truth for all blog content
  index.html                # blog listing page, renders from manifest.json (committed)
  manifest.json               # generated metadata index of published posts (committed)
  <slug>.md                    # markdown source for a published post (committed)
  <slug>.html                  # compiled static HTML for that post (committed)
  images/                     # raw source images referenced by <slug>.md drafts (committed)

scripts/
  publish_blog.py             # GITIGNORED — the markdown -> HTML publish pipeline
  _blog_template.html          # committed — the HTML shell the script fills in
  make_favicons.py             # committed — regenerates assets/favicon/ from logo.png

docs/                       # GITIGNORED — deeper architecture/structure notes, local only
```

Deeper "why" notes live in `docs/architecture.md` and `docs/structure.md`
if that folder exists locally — it's gitignored on purpose (see below), so
don't expect it in a fresh clone. This file (CLAUDE.md) is the one
committed source of truth for how the project is organized.

## Git workflow — commit as you go

**Commit whenever something meaningful changes.** Don't batch unrelated
edits into one commit, and don't leave a working tree dirty at the end of
a task. After any content edit, code change, new blog publish, or asset
update:

```
git add <the specific files that changed>
git commit -m "<concise, why-focused message>"
```

Prefer staging specific paths over `git add -A`/`git add .` when the
change set is broad, so nothing unintended (stray local files, generated
junk) gets swept in — check `git status` before committing broad changes.
Never commit `scripts/publish_blog.py` — it's gitignored for a reason (see
below).

## Blogs — how content actually gets published

**`blogs/` is the single source of truth for blog content — both the
markdown source and its compiled output live there, committed.** Readers
and crawlers are only ever served the compiled `.html` file for a post;
the sibling `.md` is the versioned authoring source, not a page anyone
navigates to (it's not linked from anywhere, and it's not in
`sitemap.xml`).

### Why HTML output instead of client-side markdown rendering

Rendering markdown in the browser would mean post content is invisible to
crawlers until JS runs, and it's one more render-blocking fetch. A
pre-rendered static `.html` file per post is fast, fully indexable on its
own (own canonical URL, OG tags, JSON-LD `BlogPosting`), and needs nothing
from the reader but an HTTP GET.

### Authoring flow

1. Write the draft as `blogs/<slug>.md` with YAML frontmatter:

   ```markdown
   ---
   title: Teaching AI in our own languages
   date: 2026-04-12
   topics: [Education, AI Literacy]
   tags: [shona, ndebele, ai-literacy, education]
   image: images/hero.jpg   # path relative to the draft; becomes the post's hero + OG image
   author: Education Team
   excerpt: Why AI literacy lands differently in Shona and Ndebele.
   ---

   Body in markdown. Reference any inline images with normal markdown
   image syntax and a relative path — they get copied automatically.
   ```

   Required fields: `title`, `date` (YYYY-MM-DD), `topics`, `tags`,
   `image`. A post is not considered complete without at least one image.
   Put source images referenced by drafts in `blogs/images/` (distinct
   from `assets/blogs/<slug>/`, which holds the copies the compiled page
   actually serves).

2. Run the publish script (gitignored, local-only — install deps once
   with `pip install pyyaml markdown`):

   ```
   python scripts/publish_blog.py blogs/<slug>.md
   ```

   This renders `blogs/<slug>.html` from `scripts/_blog_template.html`,
   copies the hero + any inline images into `assets/blogs/<slug>/`,
   updates `blogs/manifest.json` (which `blogs/index.html` reads to render
   the listing grid), and appends a `<url>` entry to `sitemap.xml`.

3. Review the generated `blogs/<slug>.html`, then commit source *and*
   output together:

   ```
   git add blogs/<slug>.md blogs/<slug>.html assets/blogs/<slug> blogs/manifest.json sitemap.xml
   git commit -m "Add blog post: <title>"
   ```

   The script prints this exact command at the end of a successful run.

### Why `scripts/publish_blog.py` is gitignored

The conversion tool is a local working file, not site content — it's only
needed to author a *new* post, never to view or deploy the already-published
site. Its input and output (`blogs/*.md`, `blogs/*.html`, `assets/blogs/*`,
`blogs/manifest.json`, `sitemap.xml`) are all committed, so `blogs/` alone
carries the full history of every post; cloning fresh needs Python only if
you're about to write a new one.

## Read-more sidebar (data-driven)

Any item in a `data.json` section can carry a `more` object — clicking that
item in the 3D scene's holo panel opens the hologram side panel instead of
the inline expander. The renderer in `index.html` is generic; all content
is data, so adding entries never requires HTML/CSS changes:

- `more.body` — array of paragraphs.
- `more.title` / `more.kicker` / `more.meta` — header fields (kicker
  defaults to the section title, title to the item label).
- `more.image` — hero image path (site-root relative).
- `more.link` — `{ "href", "label" }`, rendered as a CTA button.
- `more.fetch` — URL of an HTML page to pull content from at open time:
  its `.content` block is extracted and rendered in the panel (used by
  blog items; `more.fallback` text + a link to the page show if the fetch
  fails).
- `more.people: "leadership" | "members" | "all"` — renders from the
  section's `people` block: `leadership` as full-profile cards (`name`,
  `role`, `image`, `bio` array), `members` as a uniform two-column grid
  (`name`, `role`, `image`, `brief`), `all` as both, with a section label
  above each group only when both are shown together. A missing/empty
  `image` falls back to an initials avatar, so people can be added before
  photos exist. Each person can also carry `linkedin` and/or `site` (full
  URLs) — any that are set render as a small icon-link row on their card
  (icons from `assets/icons/`); leave both blank to show no row.

Links are external-aware: `item.link` / `more.link.href` pointing off-site
open in a new tab (`target="_blank" rel="noopener"`); same-origin links
(e.g. `blogs/<slug>.html`) navigate normally. Use this for anything that
points off the site, like an item whose `more` is omitted and `link` is
just an external URL string (e.g. the Events section's "All events on
Luma" item, which points at the hub's Luma calendar).

The same content is mirrored into the hidden `#seo-content` block so it
stays crawlable.

**Deep links**: every focused section and open panel is addressable —
`#<sectionId>` focuses that anchor (e.g. `#team`), and
`#<sectionId>/<item-slug>` also opens the item's panel (e.g.
`#team/hub-leadership`, `#blogs/<post-slug>`). Item slugs are derived from
the label (lowercased, hyphenated); blog items use the post slug. The URL
hash updates as panels open/close, so any view can be shared as a link.

**Events**: unlike blogs, event items are hand-maintained in `data.json`
(no live sync with Luma) — each carries `more.meta` (date · location),
`more.image` (hotlinked Luma cover image), `more.body`, and
`more.link` to the event's own `https://luma.com/<slug>` page. When
adding/updating events, pull details from
`https://luma.com/user/yailgweru`.

**Blogs in the sidebar**: blog items are built at runtime from
`blogs/manifest.json` and the panel is the reading experience — it fetches
the full article body from the post's own `blogs/<slug>.html` (single
source of truth, no duplication). The static post pages still exist as the
crawlable/canonical copies and as a no-JS fallback; user-facing links (the
blog listing cards, post-page back links) point at the `#blogs/<slug>`
deep links.

## Assets

- **Favicon** (`assets/favicon/`): a full set generated from
  `assets/logo.png` — `favicon.ico` (16/32/48 multi-res), standalone
  16/32/48/96px PNGs, `apple-touch-icon.png` (180px), Android Chrome icons
  (192/512px), and `site.webmanifest`. All referenced from `<head>` in
  both `index.html` and the blog template. If `logo.png` changes, rerun
  `python scripts/make_favicons.py` to regenerate the whole set — don't
  hand-edit the generated files.
- **Fonts** (`assets/fonts/`): empty today by design — the site uses the
  system font stack (`Segoe UI`/`system-ui`), so there are zero external
  font requests and no font-swap flash. If a custom font is ever added,
  self-host the `.woff2` files here rather than pulling from a Google
  Fonts/Adobe Fonts CDN — see `assets/fonts/README.md` for the exact
  `@font-face` pattern (with `font-display: swap` and a system-font
  fallback). Third-party font CDNs add a render-blocking round trip and a
  visible layout shift once the font arrives; self-hosting avoids both.
- **Blog images** (`assets/blogs/<slug>/`): populated automatically by
  `publish_blog.py` — don't add images here by hand, add them to the
  markdown draft instead so the manifest/OG tags stay correct.
- **Icons** (`assets/icons/`): small inline-style SVGs used by the
  hologram sidebar (currently `linkedin.svg`, `website.svg` for the social
  row on team profile/member cards). Hand-authored, not generated — keep
  new ones in the same minimal single-color style (`#6be8ff` stroke/fill,
  24×24 viewBox).

## SEO

- `index.html` builds its `<title>`/meta/OG/Twitter tags and a JSON-LD
  `@graph` (Organization, WebSite) from `data.json`'s `site.seo` block at
  runtime — edit copy there, not in the HTML.
- Every blog post gets its own canonical URL, OG/Twitter tags, and a
  JSON-LD `BlogPosting` block — generated by the publish script, don't
  hand-write these.
- `sitemap.xml` must list every real page: `/`, `/blogs/`, and every
  `/blogs/<slug>.html`. The publish script keeps this in sync
  automatically; if you ever add a page by hand, add its `<url>` entry
  too.
- `robots.txt` points at the sitemap — keep it that way.

## Mobile-friendliness

- Viewport meta is `width=device-width, initial-scale=1.0,
  viewport-fit=cover` — **do not** add `user-scalable=no` or
  `maximum-scale=1.0` back; disabling pinch-zoom fails accessibility and
  mobile-friendliness checks.
- The 3D scene's mobile breakpoint is `max-width: 640px` in
  `index.html`'s `<style>` — mobile gets a smaller holo-panel positioned
  bottom-center, larger tap targets (buttons ≥ 40px), and
  `env(safe-area-inset-*)` padding so UI doesn't sit under notches/home
  indicators on iOS.
- Blog pages (`scripts/_blog_template.html`, `blogs/index.html`) are plain
  responsive HTML/CSS with a single `max-width` wrapper and a 640px
  breakpoint — no JS layout logic, so they can't break on odd viewports.
- When changing any layout CSS, check both the home page (3D scene) and a
  blog post at a narrow width (≈375px) and a short one (≈650px tall) —
  the home page in particular is easy to break on short viewports since
  the canvas is `position: fixed; inset: 0`.

## Conventions to keep in mind

- Don't hardcode copy into `index.html` — it belongs in `data.json`.
- Don't hand-write a `blogs/<slug>.html` file — always go through
  `blogs/<slug>.md` + `publish_blog.py` so metadata, images, the
  manifest, and the sitemap stay consistent.
- Don't add a build step, framework, or package.json unless there's a
  concrete reason — the zero-build-step property is intentional.
