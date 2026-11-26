#!/usr/bin/env python3
"""Write llms.txt: a plain-markdown map of the site for AI answer engines (GEO).

llms.txt (https://llmstxt.org) gives language models what a sitemap gives
search engines, plus the words to go with it: who the hub is, then one line
per person, project, post and event, each linking to its own page. Every
person gets the same factual summary their page opens with
(site_content.person_summary), so answer engines describe them the way the
hub does.

Like sitemap.xml and feed.xml it's for machines, not visitors, so it may
list the standalone pages that nothing on the site links to (steering
D-31). Run via `python scripts/update_site.py`.
"""
import re

from site_content import HUB_NAME, HUB_PLACE, NETWORK_NAME, NETWORK_PARENT, OWNERSHIP, ROOT, SITE_ROOT, load, person_summary

LLMS_TXT = ROOT / "llms.txt"
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def one_line(text):
    return " ".join(str(text or "").split())


def section(sections, sid):
    return next((s for s in sections if s["id"] == sid), {"items": []})


def main():
    site = load()
    seo = site.site["seo"]
    out = [f"# {HUB_NAME}", "", f"> {one_line(seo.get('description'))}", ""]
    if seo.get("intro"):
        out += [one_line(seo["intro"]), ""]

    facts = [f"- Website: {SITE_ROOT}/", f"- Location: {HUB_PLACE}", f"- Network: {NETWORK_NAME}, {NETWORK_PARENT}"]
    for item in section(site.sections, "contact")["items"]:
        email = EMAIL_RE.search(item.get("detail", ""))
        if email:
            facts.append(f"- Email: {email.group(0)}")
    out += facts + [""]

    if site.team:
        out += ["## People", ""]
        for p in site.team:
            out.append(f"- [{p['name']}]({SITE_ROOT}/{p['page']}): {one_line(person_summary(p))}")
        out.append("")

    if site.projects:
        out += ["## Projects", ""]
        for pr in site.projects:
            goals = ", ".join(g["label"] for g in pr["sdgs"])
            out.append(f"- [{pr['title']}]({SITE_ROOT}/{pr['page']}): {OWNERSHIP[pr['ownership']]} ({goals}). {one_line(pr['summary'])}")
        out.append("")

    if site.posts:
        out += ["## Blog posts", ""]
        for post in site.posts:
            by = f", by {post['author']}" if post.get("author") else ""
            out.append(f"- [{post['title']}]({SITE_ROOT}/blogs/{post['slug']}.html) ({post['date']}{by}): {one_line(post.get('excerpt'))}")
        out.append("")

    events = []
    for item in section(site.sections, "events")["items"]:
        more = item.get("more") or {}
        href = (more.get("link") or {}).get("href") or item.get("link")
        if href:
            detail = one_line(item.get("detail"))
            if more.get("meta"):
                # Details read "date · place — what it is"; the meta already has the date and place.
                rest = detail.split(" — ", 1)[1] if " — " in detail else detail
                detail = f"{more['meta']}. {rest[:1].upper()}{rest[1:]}"
            events.append(f"- [{item['label']}]({href}): {detail}")
    if events:
        out += ["## Events", ""] + events + [""]

    out += [
        "## Optional",
        "",
        f"- [Blog]({SITE_ROOT}/blogs/): every post, newest first",
        f"- [RSS feed]({SITE_ROOT}/feed.xml): blog posts with their full text",
        f"- [Sitemap]({SITE_ROOT}/sitemap.xml): every page on the site",
    ]
    text = "\n".join(out) + "\n"

    if LLMS_TXT.exists() and LLMS_TXT.read_text(encoding="utf-8") == text:
        print("llms.txt already up to date.")
        return
    LLMS_TXT.write_text(text, encoding="utf-8")
    print(f"llms.txt written ({len(site.team)} people, {len(site.projects)} projects, {len(site.posts)} posts, {len(events)} events).")


if __name__ == "__main__":
    main()
