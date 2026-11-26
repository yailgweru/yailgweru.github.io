# Site direction

> **Status: draft, inferred from the repo on 2026-11-26. Not yet confirmed.**
> Edit this file in place as decisions get made. When an open question is
> answered, record it in [decisions.md](decisions.md) and remove it here.

## What the site is

The public home of the **Young AI Leaders Gweru Hub**, the Gweru (Midlands
Province, Zimbabwe) hub of the Young AI Leaders Community, an ITU AI for Good
initiative. It is live at <https://yailgweru.github.io/>.

Mission, as stated in `data.json`: empower Gweru's youth to build ethical,
responsible, African-rooted AI, localised for our languages, our context and
Africa's challenges.

## What the site is for

This order is inferred from where the work has gone:

1. **Show the hub is real and active.** Partners, sponsors and the global
   network look for leadership, events, partners and posts.
2. **Get found.** The hub should rank for youth and AI searches about Gweru,
   Zimbabwe and Africa. SEO has had more investment than any other area.
3. **Send people to events.** Luma holds events and registration, and the
   site links to it.
4. **Give the hub a voice.** Members write for the blog.
5. **Recruit.** Members, volunteers and partners ("Join the hub", "Get
   involved", "Become a partner").

## Who it's for

- Young people in Gweru and the Midlands, especially students. They are
  potential members and attendees.
- Partners and institutions such as American Corner Gweru, Midlands State
  University, sponsors and speakers.
- The wider Young AI Leaders / AI for Good network.
- Search engines, treated as a first-class reader: everything is also
  available as plain HTML.

## The experience

- The home page is a 3D night-city scene. Each section is a floating anchor
  that opens a "hologram" panel. This is the site's signature look.
- Everything in the scene also exists as crawlable HTML. Every view has a
  shareable link, such as `#team` or `#blogs/<slug>`.
- Blog posts are read inside the hologram panel. The static post pages are
  the canonical copies that search engines index.

## Principles

These follow from past decisions (see [decisions.md](decisions.md)):

- **Simple to run.** Static files on GitHub Pages, with no build step and no
  framework, so a small volunteer team can maintain it.
- **One source of truth per kind of content.** `data.json` holds site copy,
  `blogs/` holds posts and Luma holds events.
- **Real over aspirational.** Show only real projects, events, people and
  posts. In July, placeholder projects and unpublished "phantom" posts were
  removed in favour of the one real project.
- **Crawlable and shareable.** Crawlers and readers without JavaScript see
  what the 3D scene shows.
- **Usable on phones.** Pinch-zoom stays enabled. The layout has a 640px
  breakpoint and safe-area padding.
- **Fast.** The site uses system fonts and no font CDN. Three.js is its only
  CDN dependency.

## Where things stand (2026-11-26)

- The site went live on 2026-07-18 with a Google Search Console
  verification file.
- The last change was on 2026-07-22, so nothing has been updated in four
  months.
- Content: 1 blog post (dated 2026-03-01), 1 project, 4 events (all past,
  Feb to Apr 2026), 4 leaders (no photos or profile links) and 1 member, who
  is a test entry.
- Contact: one email address. The social media copy mentions LinkedIn, X and
  Instagram but links to none of them.

## Open questions

Where I have a recommendation, it's given.

### Fixes

**Q1. GitHub Pages publishes internal files.** The repo has no `.nojekyll`
or `_config.yml`, so GitHub Pages runs Jekyll, which turns Markdown into
pages. These are live now: `/CLAUDE.html`, `/docs/architecture.html`,
`/scripts/publish_blog.py`, and `/blogs/launching-the-gweru-hub.html`. That
last one is a second copy of the real post, built from its `.md` source,
which search engines see as duplicate content. `steering/` will be published
the same way on the next push.
*Recommendation:* add a `_config.yml` that excludes `CLAUDE.md`, `docs/`,
`scripts/`, `steering/` and `blogs/*.md` from the deployed site.

**Q2. Gitignored files are tracked anyway.** `scripts/publish_blog.py` and
`docs/` were committed on 2026-07-16 (`d1a13ff`), and the ignore rule has no
effect on files that are already tracked.
*Recommendation:* commit `publish_blog.py` on purpose, so any team member can
publish, and drop the "local-only" policy in `CLAUDE.md`. Fold `docs/` into
`steering/` or delete it, because `docs/structure.md` still describes the old
`submissions/` folder.

**Q3. Blog post leftovers.** The title reads "Reflecting on the launch the
Gweru Hub" (missing "of"), and the slug has the same wording. The source file
is `launching-the-gweru-hub.md`, but the page is
`reflecting-on-the-launch-the-gweru-hub.html`. Two orphaned image folders
remain in `assets/blogs/`: `launching-the-gweru-hub/` and
`reflecting-on-the-aunch-the-gweru-hub/`.
*Recommendation:* fix the title text but keep the URL, because it's indexed
and GitHub Pages can't redirect. Rename the source `.md` to match the page
and delete the orphaned folders.

**Q4. Test data is live.** "Tanaka Moyo (test)" appears on the site as a
member.
*Recommendation:* remove it now and add real members when you have them.

**Q5. Copy typos.** Two sentences are missing a dash ("Midlands Province
collaborating" and "Zimbabwe a growing"). "Equiping" should be "equipping".
The project is described in the past tense ("sessions that focused on").

### Direction (your call)

**Q6. The site's main job.** Is it mainly there to build credibility with
partners, to drive event sign-ups, or to publish members' writing? The
answer decides what goes on top and what gets maintained.

**Q7. Keeping it current.** The events and the blog haven't been updated
since July. Who updates what, and how often? One option is to name an owner
per section. Another is to stop hand-copying event details and rely on the
Luma link.

**Q8. SEO focus.** The keywords target pan-African terms ("tech Africa",
"Afrotech"), where competition is heavy.
*Recommendation:* lead with Gweru, Midlands and Zimbabwe terms the hub can
win, and keep Africa as secondary.

**Q9. Projects.** There is one project today. Will more come back, such as
the removed ideas (AI for agriculture, Shona/Ndebele learning materials), or
should the section stay small and real?

**Q10. Team presence.** Do you want photos and LinkedIn links for the
leaders, a real member list, and real social media URLs?
