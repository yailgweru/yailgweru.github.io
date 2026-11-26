# History

What changed on the site and why it mattered. Newest first.

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
