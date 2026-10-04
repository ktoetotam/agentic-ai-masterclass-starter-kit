---
name: critique
description: Critique a finished page before it ships - a script that measures colour contrast and static accessibility, then a browser pass at 360, 768 and 1280 px in both themes, then a structured design critique of hierarchy, usability and consistency with a prioritised fix list. Use before calling any website done, or when asked to review, critique, audit accessibility or "does this look right".
---

# Critique before you ship

Building is half the job. The bugs that matter (overlap, low contrast in place, horizontal scroll) are invisible in the source and obvious in the render. Measure, do not guess.

## 1. Static pass (seconds, no browser)

```sh
python3 .agents/skills/website-building-critique/scripts/check_page.py public/site/index.html
```

It measures the contrast of every brand token pair in light and dark, and checks lang, viewport, `@media`, reduced motion, focus style, one `<h1>`, alt text, placeholder copy, loose colours that bypass `brand.css`, and missing local files. Fix every FAIL; justify each WARN you keep in the handover.

## 2. Browser pass (measure with the browser tools, then look)

At **360, 768 and 1280 px**, in **light and dark**:

- No horizontal scroll: `document.documentElement.scrollWidth <= window.innerWidth`.
- Tab through the page: the focus ring is visible, the order makes sense, nothing is skipped or trapped; touch targets are at least 44 px.
- Read real text on real backgrounds, especially text over images (the overlay must be there).
- Turn reduced motion on: content is fully visible and nothing moves.
- Click every link and the primary action; read the console for errors; check no request goes to an unexpected host.
- Take a screenshot at each width and look at it as a design lead would.

Screenshots can lag behind a resized viewport after a reload; trust measured values (`getBoundingClientRect`, `scrollWidth`, computed styles) over a stale image.

## 3. Design critique (structured, then prioritised)

Review in this order and name one concrete evidence per point:

1. **First impression**: in five seconds, can a stranger say what this is, who it is for and what to do next?
2. **Hierarchy**: one dominant element per screen; headings, size and spacing carry the order.
3. **Usability**: the primary action is obvious and truthful; forms say what they need; errors and empty states exist.
4. **Consistency**: every colour, radius, spacing and type size comes from the tokens; motifs are reused, not reinvented.
5. **Accessibility**: contrast, focus, keyboard, labels, alt text, motion, text size (body at least 16 px on the page).
6. **Copy**: plain verbs, specific claims, nothing the company cannot back up.

Finish with a list: **Fix now** (breaks use or access), **Fix next** (clear improvement), **Optional**. Fix the first group, re-run both passes, and report the result in one line with the real numbers.

If the design plugin skills `design:design-critique` or `design:accessibility-review` are available in your client, use them for the second opinion; the steps above work without them.
