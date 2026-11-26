# Steering

This folder records where the site is going and why. `CLAUDE.md` covers how
to work on the repo (scripts, workflows, conventions). This folder covers
what to build and why.

| File | What it holds | How it changes |
|---|---|---|
| [direction.md](direction.md) | Purpose, audiences, principles, current state, open questions | Edited in place. It always describes the current direction. |
| [decisions.md](decisions.md) | Key decisions, each with its reason and status | Append-only. Superseded decisions are marked, never deleted. |
| [history.md](history.md) | Dated timeline of what changed and why it mattered | New entries go on top. |

## How to use it

- **Before significant work** (a new section, a redesign, a content push),
  read `direction.md` and check the work against it.
- **When a decision is made,** add an entry to `decisions.md`. If it answers
  an open question in `direction.md`, remove the question there and update
  any text it affects.
- **After a meaningful change ships,** add a line to `history.md`. Record the
  change and its effect on the site; don't copy the git log.
- Keep entries short. If something needs a long explanation, it probably
  belongs in `CLAUDE.md` (mechanics) or a blog post (story).

## Visibility

These files are committed, so they're visible in the repo. Until open
question Q1 in `direction.md` is resolved, GitHub Pages also publishes them
on the live site as pages (for example `/steering/direction.html`).
