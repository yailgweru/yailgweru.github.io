# History

What changed on the site and why it mattered. Newest first.

## 2026-11-26 · Lite view; no more endless spinner
- The home page gained a lite view (D-36): the same content as a plain
  page, without 3D. Phones on Data Saver, 2G or ≤1 GB of RAM get it
  automatically, and every visitor can switch between the views.
- Fixed: when Three.js couldn't load, the page spun forever. Now it falls
  back to the lite view, as it does when WebGL is missing or the GPU drops
  the 3D scene, and a slow load offers the lite view after 6 seconds.
- Without JavaScript the home page now shows its content instead of a
  spinner.

## 2026-11-26 · Live; images tinified; people optimised for search and AI answers
- **Pushed for the first time** (`7c5b2ce`): everything built since D-22 is
  live on https://yailgweru.github.io/.
- Images are tinified, right-sized and loaded on demand (D-34). The first
  visit to the home page fell from about 390 KB to 190 KB on the wire: the
  HTML from 131 KB to 23 KB, and the brand-bar logo from 106 KB to 4 KB.
  Team, project and blog images now ship as thumbnails with `srcset`, and
  photos lose their EXIF/GPS data.
- Every person page gained a quotable summary sentence, an "At a glance"
  fact list and a fuller JSON-LD graph. The hub's Organization data lists
  every member, and a new `llms.txt` describes the site to AI answer engines
  (D-35).
- Share previews now use `assets/share.jpg`, the logo on a 1200×630 white
  card, so they're no longer cropped or shown on black.

## 2026-11-26 · People and projects tagged; SDG filters
- Projects can be co-owned and have team members. People can tag themselves
  onto projects. Panels and pages show the links both ways, with roles
  (D-33).
- Projects carry UN SDG tags, shown as coloured chips and added to their
  JSON-LD. The Projects panel filters by SDG and by person. AI Literacy for
  All is tagged SDG 4 (Quality Education).
- Person profiles take an ITU profile and up to 7 social links (LinkedIn, X,
  GitHub, Instagram, Facebook, YouTube, website). The build lists each
  profile still missing its ITU link or 2 socials. All four leaders are
  missing both for now.

## 2026-11-26 · Content rendered at build time; RSS feed
- The JSON files became build inputs only (D-30). The build renders every
  section, item and sidebar panel into `index.html`, and the page builds
  the 3D scene and sidebar from that HTML without fetching any JSON. The
  console noise when the page was opened from disk went away as a side
  effect.
- Standalone person, project and post pages stay for search engines, but
  nothing links to them any more (D-31).
- Added an RSS feed, `feed.xml` (D-32).

## 2026-11-26 · Direction set: credibility, SEO, people and projects
The hub lead answered the first round of open questions (decisions D-22 to
D-29):
- **Removed:** the launch reflection post with all its leftovers, and the
  live test member.
- **Copy:** fixed typos, and refocused SEO on Zimbabwe and Southern Africa.
- **Repo:** blog drafts are now local-only, and `publish_blog.py` and
  `docs/` are tracked on purpose.
- **People and projects:** moved into one-file-per-entry folders
  (`data/team/`, `data/projects/`). Each gets its own page and sidebar
  deep link, and projects are split into community-owned and member-owned.
- **Forms:** "Join the hub" and "Become a partner" are Firebase-backed
  forms with generated Firestore rules. They're waiting on a Firebase
  project.
- **Sitemap:** now generated from every real page.

Nothing was pushed yet.

## 2026-11-26 · Steering folder
Added `steering/` (direction, decisions, history). An audit of the repo found
the issues listed as open questions Q1 to Q5 in `direction.md`.

## 2026-07-23 to 2026-11-25 · Quiet period
No commits. Events, blog and team stayed as they were in July.

## 2026-07-22 · One-command sync
`scripts/update_site.py` runs every generated-block script in order.
`CLAUDE.md` now points to it instead of to the individual scripts.

## 2026-07-19 to 07-20 · First real content
- Published the launch reflection post by Brandon T. Bande, dated
  2026-03-01. It took four commits. The slug changed from
  `reflecting-on-the-aunch-…` to `reflecting-on-the-launch-…`, which left
  two orphaned image folders behind.
- Replaced three placeholder projects (AI for agriculture, Education &
  languages, SDG-aligned impact) with the one real project, AI Literacy for
  All. Dropped the "up to 50 young AI leaders" claim.
- Removed 14 of the 15 test members. One is still live.

## 2026-07-18 · SEO work and launch
- Prerendered SEO into the static HTML, so crawlers that don't run
  JavaScript see the full content.
- Retitled the site for blended Gweru, Zimbabwe and Africa reach.
- Blog: posts can have one or two authors, and the listing got search,
  Latest/Top filters and author chips. Posts gained a standing disclaimer,
  and the logo became the share image.
- Removed the smoke-test post from the live index and the sitemap.
- The site went live, and the Google Search Console verification file was
  added.

## 2026-07-17 · Content model
- `blogs/` became the only home for blog content. Inline "stories" in
  `data.json` were removed, and `submissions/` was folded into `blogs/`.
- Added the hologram read-more sidebar. The team section was split into
  leadership cards and a member grid, blog posts are read in the panel, and
  every view got a deep link.
- Real Luma events and the real leadership roster replaced placeholders.
- Added the `file://` fallback through generated inline blocks.

## 2026-07-16 · First build
- Site v1: a Three.js night-city scene driven by `data.json`.
- Added `CLAUDE.md`, the favicon set, a mobile viewport fix and the static
  blog pipeline.
- Merged the `seo-data` branch.
- `publish_blog.py` and `docs/` were committed even though they're on the
  ignore list.

## Before the site (Feb to Apr 2026)
The hub was running before the site existed. The AI Literacy series ran on
Zoom on 2026-02-11 and at American Corner Gweru on 02-28 and 04-25. A Build
with AI buildathon satellite session ran at Midlands State University on
04-30. American Corner Gweru became the hub's venue early in 2026.
