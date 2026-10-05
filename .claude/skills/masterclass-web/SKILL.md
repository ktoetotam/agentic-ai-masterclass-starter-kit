---
name: masterclass-web
description: Lighter single-skill route for the company website challenge - build and review a responsive, accessible static site with an honest primary action, SEO basics and a deployable build in public/site/. Use when someone wants one quick page or keeps their own framework. For the full guided website process, use the website-building challenge plugin instead.
---

# Company website

**Default path for most participants:** the `website-building` challenge plugin. It runs brief, brand, layout and motion, images, SEO, critique and deployment preparation as separate steps. Start it by following `.agents/plugins/plugins/website-building/skills/setup/SKILL.md`; it makes `website-building-build` and the step skills available. The rest of this skill is the lighter route: one quick page, or a participant who keeps their own framework.

Start from the participant's brief or `data/company-brief.md`. Deliver a useful website that runs locally, plus a build directory suitable for the assigned deployment sandbox. Preserve the participant's preferred framework; use plain HTML/CSS/JavaScript when no application framework is needed.

1. Identify audience, offer and primary action. Extract approved claims, tone, colours and available assets. Keep fictional branding and testimonials clearly fictional; do not invent customer proof, addresses or certifications.
2. Build the primary journey with a readable hierarchy, responsive layout, keyboard access, visible focus, labelled controls, sufficient contrast and useful empty/error states. Use licensed or participant-owned media and meaningful alternative text.
3. Make the primary action honest: a draft contact form can validate locally and show a demo response. Do not imply a message was delivered when no backend exists. Wire a real recipient only when requested and authorized.
4. Add a descriptive title, meta description, semantic heading structure and social preview metadata. Set canonical URLs only once the destination is known. Add structured data only for verified page content. Keep private workshop builds out of search where appropriate; robots directives are not authentication.
5. Inspect the page at a phone-sized viewport and desktop width. Exercise the navigation and form with the keyboard. Check for missing assets, horizontal overflow and browser errors. Use available browser tools or project-local Playwright; a manual browser checklist is an acceptable fallback.
6. Produce startup/build commands and a compact handover. For publication, use `masterclass-deploy` and the assigned sandbox details. Do not modify the instructor's website or DNS as part of this skill.

Minimum demo: the homepage works at mobile and desktop widths, its primary action gives a truthful result, and every internal link resolves. Suggested output: `public/site/` plus `output/site-handover.md`. Serve only `public/`. If dependencies are blocked, produce one self-contained HTML page and preview it with the existing browser.
