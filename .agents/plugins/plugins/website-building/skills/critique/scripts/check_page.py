#!/usr/bin/env python3
"""Static design and accessibility check for a page and its brand.css (standard library only).

Usage: python3 check_page.py public/site/index.html [--css public/site/brand.css]

Checks: measured colour contrast of the brand token pairs (light and dark), document basics,
responsive and reduced-motion rules, focus styles, alt text, placeholder copy, loose colours
that bypass the tokens, and local assets that do not exist. A browser is still needed for
overlap, overflow and in-place contrast (see SKILL.md). Exit code 1 if any FAIL.
"""
import argparse
import re
import sys
from pathlib import Path

FAILS, WARNS = [], []


def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a, b):
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def tokens(css, selector_re):
    """Collect --name: #hex declarations inside the first block whose selector matches."""
    out = {}
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        if re.search(selector_re, m.group(1)):
            for name, val in re.findall(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{3,6})\b", m.group(2)):
                out[name] = val
    return out


# (foreground token, background token, minimum ratio, what it is)
PAIRS = [
    ("ink", "paper", 4.5, "body text"),
    ("muted", "paper", 4.5, "secondary text"),
    ("accent-text", "paper", 4.5, "small coloured text and links"),
    ("note", "paper", 4.5, "second colour used as text"),
    ("accent", "paper", 3.0, "accent as large type or UI edge"),
]


def check_tokens(css):
    light = tokens(css, r":root")
    dark = {**light, **tokens(css, r"dark-mode")}
    if not light:
        WARNS.append("no colour tokens found in brand.css (expected :root { --ink: #...; --paper: #...; })")
        return
    for label, scheme in (("light", light), ("dark", dark)):
        for fg, bg, need, what in PAIRS:
            if fg in scheme and bg in scheme:
                r = contrast(scheme[fg], scheme[bg])
                line = "%s %-11s on %-6s %5.2f:1 (%s)" % (label, fg, bg, r, what)
                if r >= need:
                    print("  PASS  " + line)
                elif fg == "accent":
                    WARNS.append(line + " - below 3:1: never use for text or UI edges")
                else:
                    FAILS.append(line + " - needs %.1f:1" % need)
    if "dark-mode" not in css:
        WARNS.append("no body.dark-mode block: fine if the page has no dark mode")


def check_html(path, css_text):
    raw = path.read_text(encoding="utf-8", errors="replace")
    html = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    low = html.lower()
    both = low + "\n" + css_text.lower()

    def need(cond, ok, bad, level=FAILS):
        if cond:
            print("  PASS  " + ok)
        else:
            level.append(bad)

    need(re.search(r"<title>\s*\S", low), "has a title", "missing <title>")
    need("<html" in low and re.search(r"<html[^>]*\blang=", low), "html lang set", "missing lang on <html>")
    need('name="viewport"' in low, "viewport meta present", "missing viewport meta")
    need("@media" in both, "has @media rules", "no @media rules: page will not adapt to phones")
    need("prefers-reduced-motion" in both, "respects reduced motion",
         "no prefers-reduced-motion rule: animations must collapse to visible end states")
    need(":focus-visible" in both, "styles :focus-visible", "no :focus-visible style: keyboard users lose their place", WARNS)
    need(re.search(r"<(main)\b", low), "has <main>", "no <main> landmark", WARNS)
    need(re.search(r'class="[^"]*skip', low) or "skip" in low, "skip link present", "no skip link", WARNS)
    h1s = len(re.findall(r"<h1[\s>]", low))
    need(h1s == 1, "exactly one <h1>", "%d <h1> elements (want one)" % h1s)
    imgs = re.findall(r"<img\b[^>]*>", low)
    bad = [i for i in imgs if " alt=" not in i]
    need(not bad, "every <img> has alt", "%d <img> without alt" % len(bad))
    need("lorem ipsum" not in low, "no lorem ipsum", "lorem ipsum found: write real copy")
    # loose colours bypassing tokens
    page_css = "".join(re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S | re.I)) + " ".join(
        re.findall(r'style="([^"]*)"', html))
    loose = set(re.findall(r"#[0-9a-fA-F]{6}\b", page_css))
    if loose:
        WARNS.append("%d hard-coded colour(s) in the page instead of brand tokens: %s"
                     % (len(loose), ", ".join(sorted(loose)[:6])))
    else:
        print("  PASS  page uses brand tokens, no loose colours")
    # assets exist
    refs = set(re.findall(r'(?:src|href)="([^"#?]+)', html)) | set(re.findall(r"url\(['\"]?([^'\")#?]+)", html + css_text))
    missing = []
    for r in refs:
        if re.match(r"^(https?:|data:|//|mailto:|tel:|javascript:)", r):
            continue
        t = (path.parent / r.lstrip("/")).resolve()
        if not (t.exists() or (t / "index.html").exists()):
            missing.append(r)
    need(not missing, "every local file reference exists", "missing files: %s" % ", ".join(sorted(missing)[:6]))
    third = sorted({m for m in re.findall(r"(?:src|href)=\"(https?://[^\"/]+)", html)
                    if any(k in m for k in ("fonts.googleapis", "fonts.gstatic", "cdn."))})
    if third:
        WARNS.append("third-party requests (self-host instead when you can): " + ", ".join(third))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("--css", help="brand.css (default: brand.css next to the page)")
    a = ap.parse_args()
    page = Path(a.html)
    css_path = Path(a.css) if a.css else page.parent / "brand.css"
    css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
    if not css:
        WARNS.append("brand.css not found at %s: contrast of brand tokens not measured" % css_path)
    print("Brand contrast (WCAG AA):")
    check_tokens(css)
    print("\nPage checks:")
    check_html(page, css)
    for w in WARNS:
        print("  WARN  " + w)
    for f in FAILS:
        print("  FAIL  " + f)
    print("\n%d fail, %d warn" % (len(FAILS), len(WARNS)))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
