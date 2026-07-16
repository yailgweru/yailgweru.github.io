# Repo structure

```
/
├── index.html              # the whole app shell (3D scene + overlay UI)
├── data.json               # all copy, SEO fields, 3D anchor layout
├── robots.txt
├── sitemap.xml             # must list every blogs/<slug>.html
├── CLAUDE.md                # instructions for whoever (human or Claude) works on this repo
├── .gitignore
│
├── assets/
│   ├── logo.png             # source logo, used to derive favicons
│   ├── favicon/              # generated favicon set (see below) — committed
│   │   ├── favicon.ico
│   │   ├── favicon-16x16.png
│   │   ├── favicon-32x32.png
│   │   ├── apple-touch-icon.png
│   │   ├── android-chrome-192x192.png
│   │   ├── android-chrome-512x512.png
│   │   └── site.webmanifest
│   ├── fonts/                # self-hosted font files, if/when added — committed
│   └── blogs/
│       └── <slug>/            # hero + inline images for one post — committed
│
├── blogs/                    # published posts — committed (these are real HTML)
│   ├── index.html              # listing page, reads manifest.json
│   ├── manifest.json            # generated metadata index of all posts
│   └── <slug>.html               # one file per published post
│
├── submissions/              # GITIGNORED — raw .md drafts waiting to be published
│   └── <slug>.md
│
├── scripts/
│   ├── publish_blog.py        # GITIGNORED — converts submissions/*.md -> blogs/*.html
│   └── _blog_template.html    # committed HTML template the script fills in
│
└── docs/                     # GITIGNORED — this folder. Local architecture notes only.
    ├── architecture.md
    └── structure.md
```

## Why submissions/ and the publish script are gitignored

This was an explicit product decision: raw drafts and the conversion
tooling are considered local working files, not site content. Only the
*output* of publishing (the HTML page, its images, the manifest/sitemap
entries) is committed. Practically: if you clone this repo fresh, `blogs/`
already has every published post as plain HTML — you don't need Python or
the script to view or deploy the site. You only need the script if you're
authoring a *new* post.

## Blog frontmatter contract

Every file in `submissions/*.md` must start with YAML frontmatter:

```markdown
---
title: Teaching AI in our own languages
date: 2026-04-12
topics: [Education, AI Literacy]
tags: [shona, ndebele, ai-literacy, education]
image: hero.jpg
author: Education Team
excerpt: Why AI literacy lands differently in Shona and Ndebele.
---

Body content in markdown goes here. The first image referenced with a
relative path (e.g. `![alt](hero.jpg)`) is copied into
`assets/blogs/<slug>/` and used as both the inline image and the OG/social
share image for the post.
```

`slug` is derived from `title` (kebab-case) unless a `slug:` field is set
explicitly in the frontmatter — needed if two posts would otherwise slugify
to the same filename.

## Running a publish

```
python scripts/publish_blog.py submissions/teaching-ai-in-our-own-languages.md
```

This is a local-only tool (gitignored) — see CLAUDE.md for the full
authoring workflow and what the script does step by step.
