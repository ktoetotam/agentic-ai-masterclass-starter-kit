---
name: seo
description: Check and improve a website's search and sharing basics - title, meta description, one h1, heading order, alt text, canonical, social preview, JSON-LD schema, sitemap and robots - with a script that reads the HTML and fails on real problems, and keeps private workshop pages out of search. Use before showing or publishing any page, or when asked about SEO, Google, rankings or link previews.
---

# SEO

Honest scope: this checks what is in the HTML. It does not rank anything and it cannot promise traffic. Do not invent keywords, reviews, ratings or addresses.

## 1. Decide the page's job

One sentence per page: who searches for this and what they want. The title and the h1 answer that, in the words the visitor uses.

## 2. Write the basics

- `<title>`: 15-65 characters, the page's subject first, brand last.
- `<meta name="description">`: 70-160 characters, a plain promise that matches the page; not a keyword list.
- One `<h1>`; headings go down one level at a time.
- Social preview: `og:title`, `og:description`, `og:image` (1200x630, see `website-building-images`), `twitter:card`.
- `<link rel="canonical">` only once the real public address is known.
- `lang` on `<html>`; real alt text on meaningful images; descriptive link text (not "click here").

## 3. Structured data (only for facts that are on the page)

Add JSON-LD (`<script type="application/ld+json">`) such as `Organization` or `LocalBusiness` for a real company, `FAQPage` only for visible questions and answers. Never mark up fictional reviews or ratings. Validate that it parses; the script does.

## 4. Files

- `public/site/sitemap.xml` and `robots.txt` only for a site that should be found. List only real, live URLs.
- **Private or workshop builds** (a `workers.dev` demo, members-only material): keep `<meta name="robots" content="noindex, nofollow">` on every page, and do not publish a sitemap. A robots directive is not a lock: it does not keep anyone out.

## 5. Run the check (no network, no cost)

```sh
python3 .agents/skills/website-building-seo/scripts/seo_check.py public/site
python3 .agents/skills/website-building-seo/scripts/seo_check.py public/site --members-only   # private builds
```

Fix every FAIL. Explain every WARN you keep (for example a missing canonical on a demo). The script also fails on internal links that do not resolve. Paste the real output into `output/site-handover.md`.

## Not covered here

Rankings, backlinks, Core Web Vitals in the field and Search Console need live data and the participant's own accounts. Say so rather than guessing numbers.
