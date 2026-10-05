---
name: layout
description: Plan and build a website's layout and animation - a short design plan shown to the participant first, one signature element, hairline-grid sections, an orchestrated hero entrance, scroll reveals, responsive from 360 px, reduced-motion safe. Use when designing or building any page or section, or when a page feels generic or template-like.
---

# Layout and motion

Work like a design lead, in two passes.

## Pass 1: the design plan (show it, wait for a yes)

Write four short items in plain words:

1. **Layout idea** - one sentence of prose, specific to this company.
2. **Signature element** - the one thing the page will be remembered by (a drawn diagram, an oversized number, a map, a timeline). One, not three.
3. **Motion story** - what moves, when and why.
4. **Image plan** - SVG art, generated image, or gradient (see `website-building-images`).

Then critique your own plan: if any part is what you would write for any similar brief (hero = big number plus gradient, scattered fade-ins, 01/02/03 markers on content that is not a sequence), replace it with a choice that only fits this content. Structure must say something true: eyebrows, dividers and numbers appear only where they carry meaning.

## Pass 2: build to the plan

- Plain HTML, CSS and JavaScript in `public/site/`; styling only through the variables in `brand.css`.
- Sections as grids divided by hairlines; side padding 4rem, 2.5rem under 1024 px, 1.5rem under 768 px.
- One `<h1>`; landmarks (`header`, `nav`, `main`, `footer`); a skip link; 44 px minimum touch targets; visible focus.
- Mobile first from 360 px. Put the phone media query **last** in the stylesheet or it loses on source order. No horizontal scroll at any width.
- Honest primary action: a draft form validates locally and shows a demo response. Never imply a message was sent when nothing receives it.

## Motion

One orchestrated moment beats scattered effects: a page-load sequence for the hero, scroll reveals for the rest, a small hover response on controls. Animate only `transform` and `opacity`, 150-600 ms, ease-out for entrances, stagger children by 60-120 ms. Drawing an SVG line in with `stroke-dasharray` is on-brand for diagrams.

```css
.reveal { opacity: 0; transform: translateY(24px);
  transition: opacity .65s ease, transform .65s ease; }
.reveal.visible { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1; transform: none; transition: none; }
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; }
}
```

```js
const io = new IntersectionObserver(entries => entries.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
}), { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
```

Without JavaScript the content must still be visible: add the `.reveal` hiding rule only after a script adds a `js` class to `<html>`.

## Diagrams (SVG)

Reserve a 5% safe inset in each `viewBox`; align repeated nodes to shared coordinates; keep labels horizontal and short; give labels a solid background where a line could cross them; never change `font-size` inside a fixed-box viewBox. Test at 360, 768 and 1280 px in both themes.
