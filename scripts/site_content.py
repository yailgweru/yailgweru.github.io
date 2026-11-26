"""Load, validate and assemble every content source the site is built from.

The JSON files are build inputs only — the browser never reads them. Every
build script imports this module, so all of them see the same validated
content:

  data.json                 site copy, SEO, sections, forms, Firebase config
  data/team/<slug>.json     one person each
  data/projects/<slug>.json one project each
  blogs/manifest.json       published posts (written by publish_blog.py)

`load()` returns a Site with the raw data plus `sections`: data.json's
sections with blog posts, projects and people merged in as items, ready to
render. Problems in any file are collected and reported together, and the
build stops before writing anything.
"""
import copy
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
SITE_ROOT = "https://yailgweru.github.io"
ORG_ID = SITE_ROOT + "/#organization"
ORG_NAME = "Young AI Leaders — Gweru Hub"
LOGO_ABS = SITE_ROOT + "/assets/logo.png"
LOGO_ALT = "Young AI Leaders Community logo — Gweru Hub"

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
GROUPS = {"leadership": "Hub leadership", "member": "Hub member"}
OWNERSHIP = {"community": "Community project", "member": "Member project"}
STATUSES = {"": "", "planned": "Planned", "active": "Active", "completed": "Completed"}


def slugify(text):
    text = re.sub(r"[^a-z0-9\s-]", "", str(text).lower()).strip()
    return re.sub(r"[\s_-]+", "-", text)


def as_list(value):
    if not value:
        return []
    return value if isinstance(value, list) else [value]


def is_external(url):
    return bool(re.match(r"^https?://", url or ""))


class _Errors(list):
    def check_url(self, where, value):
        if value and not is_external(value):
            self.append(f"{where}: '{value}' must be a full URL starting with https://")

    def image(self, where, kind, slug, value):
        """Explicit path wins; otherwise look for assets/<kind>/<slug>.<ext>."""
        if value:
            if not is_external(value) and not (ROOT / value).is_file():
                self.append(f"{where}: image '{value}' does not exist")
            return value
        for ext in IMAGE_EXTS:
            candidate = Path("assets") / kind / f"{slug}{ext}"
            if (ROOT / candidate).is_file():
                return candidate.as_posix()
        return ""


def _read_dir(kind, errors):
    entries = []
    for path in sorted((ROOT / "data" / kind).glob("*.json")):
        where = path.relative_to(ROOT).as_posix()
        if not SLUG_RE.match(path.stem):
            errors.append(f"{where}: filename must be a lowercase-hyphenated slug (e.g. jane-doe.json)")
            continue
        try:
            entry = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{where}: invalid JSON ({e})")
            continue
        entries.append((path.stem, where, entry))
    return entries


def _person(slug, w, p, reserved, errors):
    if not p.get("name"):
        errors.append(f"{w}: 'name' is required")
    if p.get("group") not in GROUPS:
        errors.append(f"{w}: 'group' must be one of {sorted(GROUPS)}")
    if slug in reserved:
        errors.append(f"{w}: slug '{slug}' clashes with a Team section item; rename the file")
    for key in ("linkedin", "site"):
        errors.check_url(f"{w} {key}", p.get(key, ""))
    bio = [str(t) for t in as_list(p.get("bio"))]
    return {
        "slug": slug,
        "name": p.get("name", ""),
        "group": p.get("group", "member"),
        "order": p.get("order", 999),
        "role": p.get("role", ""),
        "image": errors.image(w, "team", slug, p.get("image", "")),
        "brief": p.get("brief", "") or (bio[0] if bio else ""),
        "bio": bio,
        "linkedin": p.get("linkedin", ""),
        "site": p.get("site", ""),
        "page": f"team/{slug}.html",
        "projects": [],
    }


def _project(slug, w, p, people, errors):
    if not p.get("title"):
        errors.append(f"{w}: 'title' is required")
    if not p.get("summary"):
        errors.append(f"{w}: 'summary' is required")
    if p.get("ownership") not in OWNERSHIP:
        errors.append(f"{w}: 'ownership' must be one of {sorted(OWNERSHIP)}")
    status = p.get("status", "") or ""
    if status not in STATUSES:
        errors.append(f"{w}: 'status' must be one of {sorted(s for s in STATUSES if s)} or blank")
    owners = []
    for owner in as_list(p.get("owners")):
        if owner not in people:
            errors.append(f"{w}: owner '{owner}' has no data/team/{owner}.json")
            continue
        owners.append({"slug": owner, "name": people[owner]["name"], "page": people[owner]["page"]})
    if p.get("ownership") == "member" and not owners:
        errors.append(f"{w}: a member-owned project needs at least one entry in 'owners'")
    links = []
    for i, link in enumerate(as_list(p.get("links"))):
        if not isinstance(link, dict) or not link.get("href"):
            errors.append(f"{w}: links[{i}] needs an 'href'")
            continue
        errors.check_url(f"{w} links[{i}]", link["href"])
        links.append({"href": link["href"], "label": link.get("label") or "Learn more"})
    return {
        "slug": slug,
        "title": p.get("title", ""),
        "ownership": p.get("ownership", "community"),
        "owners": owners,
        "status": status,
        "order": p.get("order", 999),
        "summary": p.get("summary", ""),
        "body": [str(t) for t in as_list(p.get("body"))],
        "image": errors.image(w, "projects", slug, p.get("image", "")),
        "links": links,
        "page": f"projects/{slug}.html",
    }


def _assemble_sections(data, team, projects, posts):
    """data.json sections with posts, projects and people merged in as items."""
    sections = copy.deepcopy(data["sections"])
    for s in sections:
        for item in s.get("items", []):
            item.setdefault("slug", slugify(item.get("label", "")))
        s["people"] = {"leadership": [], "members": []}
        s["hidden"] = []

    by_id = {s["id"]: s for s in sections}
    if "blogs" in by_id:
        by_id["blogs"]["items"] = [
            {
                "label": p["title"],
                "detail": p.get("excerpt", ""),
                "slug": p["slug"],
                "more": {
                    "kicker": "Hub Blog",
                    "meta": f"{p['date']} · {p.get('author', '')}",
                    "image": p.get("image", ""),
                    "fetch": f"blogs/{p['slug']}.html",
                    "fallback": p.get("excerpt", ""),
                },
            }
            for p in posts
        ]
    if "projects" in by_id:
        items = []
        for p in projects:
            member = p["ownership"] == "member"
            names = " & ".join(o["name"] for o in p["owners"])
            meta = [((("By " if member else "Led by ") + names) if names else "Run by the hub"), STATUSES[p["status"]]]
            items.append({
                "label": p["title"],
                "detail": p["summary"],
                "slug": p["slug"],
                "group": "Member projects" if member else "Community projects",
                "more": {
                    "kicker": OWNERSHIP[p["ownership"]],
                    "title": p["title"],
                    "meta": " · ".join(m for m in meta if m),
                    "image": p["image"],
                    "lead": p["summary"],
                    "body": p["body"],
                    "project": p,
                },
            })
        by_id["projects"]["items"] = items
    if "team" in by_id:
        t = by_id["team"]
        t["people"] = {
            "leadership": [p for p in team if p["group"] == "leadership"],
            "members": [p for p in team if p["group"] == "member"],
        }
        t["hidden"] = [
            {
                "label": p["name"],
                "detail": p["brief"],
                "slug": p["slug"],
                "more": {"kicker": GROUPS[p["group"]], "title": p["name"], "meta": p["role"], "person": p},
            }
            for p in team
        ]
    return sections


def load():
    errors = _Errors()
    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))

    team_section = next((s for s in data["sections"] if s.get("id") == "team"), {})
    reserved = {slugify(it.get("label", "")) for it in team_section.get("items", [])}
    people = {slug: _person(slug, w, p, reserved, errors) for slug, w, p in _read_dir("team", errors)}
    projects = [_project(slug, w, p, people, errors) for slug, w, p in _read_dir("projects", errors)]

    manifest = ROOT / "blogs" / "manifest.json"
    posts = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else []

    if errors:
        print("Content problems — nothing was written:", file=sys.stderr)
        for e in errors:
            print("  - " + e, file=sys.stderr)
        sys.exit(1)

    projects.sort(key=lambda p: (p["ownership"] != "community", p["order"], p["title"].lower()))
    for pr in projects:
        for o in pr["owners"]:
            people[o["slug"]]["projects"].append({"slug": pr["slug"], "title": pr["title"], "summary": pr["summary"]})
    team = sorted(people.values(), key=lambda p: (p["group"] != "leadership", p["order"], p["name"].lower()))
    posts = sorted(posts, key=lambda p: p["date"], reverse=True)

    return SimpleNamespace(
        data=data,
        site=data["site"],
        team=team,
        projects=projects,
        posts=posts,
        sections=_assemble_sections(data, team, projects, posts),
    )
