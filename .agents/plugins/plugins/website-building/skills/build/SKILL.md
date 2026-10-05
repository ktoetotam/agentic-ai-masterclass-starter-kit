---
name: build
description: Run the whole website-building process in order - brief, brand, design plan, build, images, SEO, critique, deploy preparation - and hand over a working site in public/site/. Use first whenever someone wants to build, redo or finish a website, landing page or company site, or does not know which website skill comes next.
---

# Build a website, in order

This is the way the AI Realist site is built: decide first, build once, check by measuring. Each step has its own skill; this one keeps the order and the handover. Work in `public/site/` (serve only `public/`) and keep drafts in `output/`.

1. **Brief** (ask at most three questions, then write it down in `output/site-brief.md`): who the visitor is, what the one primary action is, and what is true and approved to say. Fictional company? Say so on the page. Never invent customers, testimonials, addresses or certifications.
2. **Brand** - use `website-building-brand`. Result: `public/site/brand.css` and `output/BRAND.md`.
3. **Design plan** - use `website-building-layout`. Write the plan (layout idea, one signature element, motion story, image plan) and show it to the participant in plain words **before** writing the page. Wait for a yes or a change.
4. **Build** the page from the plan with plain HTML, CSS and JavaScript. One page first.
5. **Images** - use `website-building-images`. Hand-built SVG and CSS first; paid image APIs only with a spend limit the participant has agreed.
6. **SEO** - use `website-building-seo`, then run its script.
7. **Critique** - use `website-building-critique`. Do not call the site finished before this passes.
8. **Deploy preparation** - use `website-building-deploy`. Preparing is not publishing; publishing needs a direct request.

## Handover (always)

Write `output/site-handover.md`: how to start the preview (`node scripts/serve.mjs`), the files that matter, what each check printed (paste the real output), what was **not** checked, and the next most useful improvement. Label anything simulated. Never claim a check passed that was not run.

## Ground rules

- One step at a time, show the result, then continue. Show the page in the browser at phone and desktop width before the critique step.
- Real copy only; no lorem ipsum. Plain verbs, sentence case, specific over clever.
- Keep secrets out of `public/`, screenshots and logs. Keys live in `.env` only.
- Members-only or workshop material keeps `<meta name="robots" content="noindex, nofollow">`.
