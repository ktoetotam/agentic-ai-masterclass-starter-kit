#!/usr/bin/env python3
"""Static SEO check for the HTML pages in a folder or a single file (standard library only).

Usage: python3 seo_check.py public/site [--members-only]

--members-only: pages are private workshop material, so noindex is REQUIRED (instead of a warning).
Exit code 1 if any FAIL.
"""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.meta = {}
        self.links = []
        self.h = []
        self._h = None
        self.imgs = []
        self.jsonld = []
        self._ld = False
        self.lang = None
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key.lower()] = a.get("content", "")
        elif tag == "link":
            self.links.append(a)
        elif tag in ("h1", "h2", "h3"):
            self._h = [tag, ""]
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._ld = True
            self.jsonld.append("")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3") and self._h:
            self.h.append(tuple(self._h))
            self._h = None
        elif tag == "script":
            self._ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._h:
            self._h[1] += data
        if self._ld and self.jsonld:
            self.jsonld[-1] += data


def check(path, members_only):
    p = Page()
    p.feed(path.read_text(encoding="utf-8", errors="replace"))
    out = []

    def add(level, msg):
        out.append((level, msg))

    t = p.title.strip()
    if not t:
        add("FAIL", "no <title>")
    elif not 15 <= len(t) <= 65:
        add("WARN", "title is %d characters (aim for 15-65): %r" % (len(t), t[:70]))
    d = p.meta.get("description", "").strip()
    if not d:
        add("FAIL", "no meta description")
    elif not 70 <= len(d) <= 165:
        add("WARN", "meta description is %d characters (aim for 70-160)" % len(d))
    if not p.lang:
        add("FAIL", "<html> has no lang attribute")
    if "viewport" not in p.meta:
        add("FAIL", "no viewport meta")
    h1 = [x for x in p.h if x[0] == "h1"]
    if len(h1) != 1:
        add("FAIL" if not h1 else "WARN", "%d <h1> elements (want exactly one)" % len(h1))
    levels = [int(x[0][1]) for x in p.h]
    if any(b - a > 1 for a, b in zip(levels, levels[1:])):
        add("WARN", "heading levels skip (for example h1 straight to h3)")
    noalt = [i for i in p.imgs if "alt" not in i]
    if noalt:
        add("FAIL", "%d <img> without alt (use alt=\"\" for decoration)" % len(noalt))
    robots = p.meta.get("robots", "").lower()
    if members_only:
        if "noindex" not in robots:
            add("FAIL", "members-only page is missing <meta name=\"robots\" content=\"noindex, nofollow\">")
    else:
        if "noindex" in robots:
            add("WARN", "page is noindex - correct only for private material")
        if not any(l.get("rel") == "canonical" for l in p.links):
            add("WARN", "no canonical link (add once the real address is known)")
        for k in ("og:title", "og:description", "og:image"):
            if k not in p.meta:
                add("WARN", "missing %s" % k)
        if "twitter:card" not in p.meta:
            add("WARN", "missing twitter:card")
    for block in p.jsonld:
        try:
            json.loads(block)
        except ValueError:
            add("FAIL", "JSON-LD block is not valid JSON")
    # internal links must resolve
    for href in p.hrefs:
        if re.match(r"^(https?:|mailto:|tel:|#|//|javascript:)", href):
            continue
        target = (path.parent / href.split("#")[0].split("?")[0]).resolve() if not href.startswith("/") else None
        if target is None:
            continue
        if href.split("#")[0] and not (target.exists() or (target / "index.html").exists()):
            add("FAIL", "internal link does not resolve: %s" % href)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--members-only", action="store_true")
    a = ap.parse_args()
    root = Path(a.target)
    pages = sorted(root.rglob("*.html")) if root.is_dir() else [root]
    if not pages:
        sys.exit("no .html files found in %s" % root)
    fails = warns = 0
    for page in pages:
        results = check(page, a.members_only)
        print(page)
        if not results:
            print("  PASS  nothing to fix")
        for level, msg in results:
            print("  %s  %s" % (level, msg))
            fails += level == "FAIL"
            warns += level == "WARN"
    print("\n%d page(s), %d fail, %d warn" % (len(pages), fails, warns))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
