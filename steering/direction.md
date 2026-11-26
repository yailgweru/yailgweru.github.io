# Site direction

> **Status: confirmed by the hub lead on 2026-11-26**, apart from the open
> questions at the bottom. Edit this file in place as decisions get made.
> When an open question is answered, record it in
> [decisions.md](decisions.md) and remove it here.

## What the site is

The public home of the **Young AI Leaders Gweru Hub**, the Gweru (Midlands
Province, Zimbabwe) hub of the Young AI Leaders Community, an ITU AI for Good
initiative. It is live at <https://yailgweru.github.io/>.

Mission, as stated in `data.json`: empower Gweru's youth to build ethical,
responsible, African-rooted AI, localised for our languages, our context and
Africa's challenges.

## What the site is for

**Credibility and visibility, with heavy emphasis on SEO** (D-22). The site
has to show partners, sponsors, members and the global network that the hub
is real and active, and it has to be found in search. When two options are
otherwise equal, pick the one that is better for search and for credibility.

That breaks down into:

1. **Show the hub is real.** Real leadership, members, projects, events and
   partners, each with its own page.
2. **Get found** for youth, AI and tech searches about **Zimbabwe, Gweru and
   Southern Africa** (D-23).
3. **Turn interest into contact.** People join the hub and organisations
   request partnerships through forms (D-29).
4. **Send people to events** on Luma.

## Who it's for

- Young people in Gweru and the Midlands, especially students: potential
  members and attendees.
- Partners and institutions, such as American Corner Gweru, Midlands State
  University, sponsors and speakers.
- The wider Young AI Leaders / AI for Good network.
- Search engines, treated as a first-class reader.

## The experience

- The home page is a 3D night-city scene. Each section is a floating anchor
  that opens a "hologram" panel.
- **The sidebar is where everything is read.** People, projects, posts,
  events and forms all open there, each with its own deep link
  (`#team/<slug>`, `#projects/<slug>`, …).
- **Every person, project and post also has a standalone page** for search
  engines, but nothing on the site links to it (D-27, D-31).
- Projects come in two kinds, **community-owned** (run by the hub) and
  **member-owned** (owned by individual members), and the list is expected to
  grow (D-26).
- All content is rendered into the home page's HTML at build time, so
  crawlers read exactly what visitors see (D-30).
- Blog posts are also published as an RSS feed, `feed.xml` (D-32).

## Principles

- **Simple to run.** Static files on GitHub Pages, no framework and no
  server. Small Python scripts regenerate everything with
  `python scripts/update_site.py`.
- **JSON is for updating, HTML is for reading** (D-30). You edit the JSON
  and rebuild; the browser only ever sees rendered HTML.
- **One source of truth per kind of content.** `data.json` holds site copy
  and forms, `data/team/` and `data/projects/` hold people and projects (one
  file each), the local blog drafts hold posts, and Luma holds events.
- **Link into the sidebar, never to standalone pages** (D-31).
- **Real over aspirational.** Show only real projects, events, people and
  posts. No placeholders or test data on the live site.
- **Every real thing gets a page.** People, projects and posts each get a
  canonical URL, structured data and a sitemap entry.
- **Only compiled output is published.** Markdown drafts stay local; GitHub
  Pages serves the HTML (D-24).
- **Usable on phones and fast.** Pinch-zoom stays enabled, form inputs are
  16px so iOS doesn't zoom, and the Firebase SDK loads only when someone
  submits a form.

## Where things stand (2026-11-26)

- **Content:** 4 leaders (no photos or profile links yet), no members yet,
  1 community project, no blog posts (the launch post was removed), and
  4 events, all in the past (Feb to Apr 2026).
- **Forms:** built, but showing an email fallback until a Firebase project
  is connected (Q11).
- **Unpushed:** all of this work is committed locally and nothing has been
  pushed to the live site.

## Open questions

**Q7. Where blog posts come from.** The answer given was "Blogs come from
Luma page", and it needs one more detail. Does it mean: (a) each Luma event
gets a write-up as a blog post, (b) event details should be pulled
automatically from Luma into the Events section, or (c) something else? Who
writes and publishes the posts?

**Q10. Team presence.** The photo folder (`assets/team/`) is ready. Still
needed: photos, LinkedIn or website links for the leaders, the real member
list, and the hub's social media URLs (the Contact section mentions
LinkedIn, X and Instagram but links to none of them).

**Q11. Firebase project.** Someone needs to create the Firebase project (or
choose an existing one), paste its web config into `data.json`, and deploy
the generated rules. See `CLAUDE.md` → "Forms". Also: who reads
submissions, and should new submissions send an email notification? That
would need a Firebase extension such as Trigger Email.

**Q12. Other Markdown files are still public.** Drafts no longer get
pushed, but GitHub Pages' Jekyll still publishes the committed `CLAUDE.md`,
`docs/*.md` and `steering/*.md` as pages (`/CLAUDE.html`,
`/steering/direction.html`, …).
*Recommendation:* add a `_config.yml` with
`exclude: [CLAUDE.md, docs, steering, scripts, data]` so they stay in the
repo but off the website.

**Events are out of date.** All four listed events are in the past. Add the
next ones from <https://luma.com/user/yailgweru>, or say if the Events
section should only link to Luma (see Q7).
