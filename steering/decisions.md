# Decisions

Key decisions about the site, each with its reason. Append new entries at the
bottom with the next number. Don't delete entries: mark them **Superseded by
D-xx** or **Under review** instead.

Entries D-01 to D-20 were reconstructed on 2026-11-26 from commit history,
`CLAUDE.md` and `docs/`. Where the reason is inferred rather than written
down, the entry says so.

---

### D-01 · Static site, no build step
**2026-07-16 · Active**
The site is plain HTML/CSS/JS on GitHub Pages, with no bundler, framework or
`package.json`.
**Why:** a small volunteer team can maintain it, hosting is free, and edits
have little that can break.

### D-02 · 3D night-city scene as the home page
**2026-07-16 · Active**
The home page is a Three.js scene, loaded from cdnjs and not vendored, with
one floating anchor per section.
**Why:** it gives the hub a distinctive identity. The CDN is a single point of
failure for the scene only; the crawlable content and blog pages work without
it.

### D-03 · `data.json` is the source of truth for site copy
**2026-07-16 · Active**
All copy, SEO fields and anchor layout live in `data.json`. `index.html`
contains no copy.
**Why:** content edits touch one file and need no HTML changes.

### D-04 · Blog posts compile to static HTML when they're written
**2026-07-16 · Active**
Posts are written in Markdown and compiled to `blogs/<slug>.html` by
`publish_blog.py`. They are not rendered from Markdown in the browser.
**Why:** each post is indexable on its own (canonical URL, OG tags, JSON-LD)
and needs nothing but an HTTP GET.

### D-05 · `blogs/` is the only home for blog content
**2026-07-17 · Active, amended by D-24 (supersedes the original `submissions/` folder)**
The Markdown source and the compiled HTML both live in `blogs/`. The three
"stories" hardcoded in `data.json` were removed; two of them had never been
published.
**Why:** blog content was split across two places, and the home page showed
posts that didn't exist as real pages.

### D-06 · Publish script kept local-only
**2026-07-16 · Superseded by D-25**
`scripts/publish_blog.py` is in `.gitignore` as a local working tool.
**Reality:** it has been tracked since `d1a13ff` and is publicly served.

### D-07 · `docs/` kept local-only
**2026-07-16 · Superseded by D-25**
Architecture notes in `docs/` were meant to stay out of the repo.
**Reality:** they are tracked, publicly served and partly out of date.

### D-08 · Data-driven read-more sidebar
**2026-07-17 · Active**
Any item can carry a `more` object (body, image, meta, link, fetch, people)
that opens the hologram side panel.
**Why:** sections can be added or extended in `data.json` without HTML or CSS
changes.

### D-09 · Blog posts are read in the hologram panel
**2026-07-17 · Active**
The panel fetches the post's `.content` from its static page. User-facing
links point to `#blogs/<slug>`.
**Why:** readers stay in the experience, and the static page remains the one
copy of the text.

### D-10 · Every view is deep-linkable
**2026-07-17 · Active**
`#<section>` and `#<section>/<item-slug>` focus an anchor or open a panel,
and the hash updates as panels open and close.
**Why:** any view can be shared as a link.

### D-11 · Luma is the system of record for events
**2026-07-17 · Active**
Event items are copied into `data.json` by hand from
<https://luma.com/user/yailgweru>, with no live sync. A standing item links to
the full calendar.
**Why (inferred):** this needs no API or build step. The cost is that event
details go out of date unless someone updates them (see Q7).

### D-12 · Real people and real events over placeholders
**2026-07-17 · Active**
The real leadership roster and real Luma events replaced placeholder copy.
**Why:** the site has to show the hub as it actually is.

### D-13 · Crawlable content matches what the scene shows
**2026-07-18 · Active**
`prerender_seo.py` bakes the head, JSON-LD, `#seo-content` and blog cards
into the static HTML, and the runtime rebuilds identical output.
**Why:** crawlers that don't run JavaScript had been seeing a stale head and
almost no content.

### D-14 · Blended Gweru, Zimbabwe and Africa positioning
**2026-07-18 · Superseded by D-23**
The title, h1 and description mix local terms (Gweru, Zimbabwe) with
continental ones (Africa).
**Why:** to reach searches beyond Gweru.

### D-15 · Blog rules: 1 or 2 authors, a disclaimer, and a featured flag
**2026-07-18 · Active**
Every post has one or two authors and ends with a standing disclaimer: views
are the authors' own, and sharing is allowed unless it's discriminatory.
`featured: true` marks a "Top story".
**Why:** members can publish under their own names, and the hub doesn't
endorse every view.

### D-16 · The hub logo is every share image
**2026-07-18 · Active**
`og:image` and `twitter:image` always use the logo. A post's hero image
appears only on the page and its listing card.
**Why:** links look consistent wherever they're shared.

### D-17 · The site also works from `file://`
**2026-07-17 · Active (supersedes the "server required" note in `36d2c95`)**
Generated inline blocks embed `data.json` and the logo in `index.html`.
Serving over HTTP is still the main workflow.
**Why:** the site can be checked by double-clicking `index.html`, with no
server.

### D-18 · One command syncs every generated block
**2026-07-22 · Active**
`python scripts/update_site.py` runs the SEO prerender and both inline
scripts, and regenerates favicons when the logo changes.
**Why:** nobody has to remember which scripts to rerun.

### D-19 · System fonts only
**2026-07-16 · Active**
There are no font CDNs. If a custom font is ever added, it gets self-hosted
in `assets/fonts/`.
**Why:** no render-blocking request and no layout shift while a font loads.

### D-20 · Mobile and accessibility basics
**2026-07-16 · Active**
Pinch-zoom stays enabled, the layout has a 640px breakpoint, tap targets are
at least 40px, and padding respects safe areas.
**Why:** most visitors are likely on phones, and disabling zoom fails
accessibility checks.

### D-21 · A steering folder for direction and history
**2026-11-26 · Active**
`steering/` holds direction, decisions and history, alongside `CLAUDE.md`.
**Why:** decisions were scattered across commit messages and local-only
notes. This folder gives them one home that is easy to change.

---

Decisions D-22 to D-29 were made by the hub lead on 2026-11-26, answering
open questions Q1 to Q9.

### D-22 · The site exists for credibility and visibility, with heavy SEO
**2026-11-26 · Active (answers Q6)**
The site's main job is to make the hub credible and findable. Search
visibility weighs heavily in every content and structure decision.
**How to apply:** when two options are otherwise equal, pick the one that is
better for search and for credibility. Real entities get their own indexable
pages.

### D-23 · SEO targets Zimbabwe and Southern Africa
**2026-11-26 · Active (supersedes D-14, answers Q8)**
The title, h1, description, intro and keywords lead with Zimbabwe, Gweru and
Southern Africa instead of broad pan-African terms. The Organization's
`areaServed` lists Zimbabwe and Southern Africa.
**Why:** these are searches a Gweru hub can realistically rank for.

### D-24 · Blog drafts stay local; only compiled HTML is pushed
**2026-11-26 · Active (amends D-05, answers Q1)**
`blogs/*.md` and `blogs/images/` are gitignored. `publish_blog.py` converts a
draft into `blogs/<slug>.html`, and only that output, its images and the
manifest are committed.
**Why:** GitHub Pages' Jekyll had published a pushed draft as a duplicate,
unlinked copy of its own post.
**Trade-off:** drafts aren't backed up by git, so authors keep their own
copies.

### D-25 · The publish script and `docs/` are tracked on purpose
**2026-11-26 · Active (supersedes D-06 and D-07, answers Q2)**
Both came off `.gitignore`. They had been tracked since `d1a13ff` anyway.
`docs/` was refreshed so it no longer contradicts `CLAUDE.md`.

### D-26 · Projects grow, as community-owned or member-owned
**2026-11-26 · Active (answers Q9)**
Every project is either `community` (run by the hub, optionally with leads)
or `member` (owned by one or more members, linked to their profiles).
Community projects list first, and each group has its own header.
**Why:** to credit members' own work while keeping hub-run work distinct.

### D-27 · Every person and project has its own page and its own sidebar link
**2026-11-26 · Active**
`build_pages.py` generates `team/<slug>.html` and `projects/<slug>.html` with
their own canonical URLs and JSON-LD, all listed in `sitemap.xml`. The same
entries open in the hologram sidebar at `#team/<slug>` and `#projects/<slug>`.
`sitemap.xml` is now generated from every real page (`build_sitemap.py`).
**Why:** credibility and SEO (D-22). People and projects become shareable and
indexable on their own.

### D-28 · One file per person and project, plus photo folders
**2026-11-26 · Active**
People live in `data/team/<slug>.json` and projects in
`data/projects/<slug>.json`; the filename is the slug. Photos for leaders and
members alike go in `assets/team/<slug>.*`, and project images (optional) in
`assets/projects/<slug>.*`. Both are picked up automatically.
**Why:** adding a person or project means adding one file, with no editing of
a large shared JSON.

### D-29 · Join and partnership requests go through Firebase forms
**2026-11-26 · Active (setup pending, Q11)**
"Join the hub" and "Become a partner" are forms defined in `data.json` that
write to Cloud Firestore. `build_form_rules.py` generates create-only
security rules from the same definitions, and the Firestore lite SDK loads
only when someone submits. Until the Firebase config is filled in, the forms
show an email fallback.
**Why:** structured requests instead of loose emails, with no server to run.

