---
name: brand
description: Define a website's brand as tokens and a one-page brand file - colours with measured contrast, two fonts, voice, signature motifs, light and dark mode - and write brand.css so every page uses variables instead of loose colours. Use before designing any page, or when a site looks off-brand, inconsistent or hard to read.
---

# Brand: decide once, use everywhere

The brand is a small set of decisions. Spend your creativity on layout and imagery; do not restyle the brand per page. If the participant has a real brand, extract it (colours, fonts, tone, approved claims). If not, build one from the brief and label it a draft.

## Output

1. `output/BRAND.md` - one page: purpose in a sentence, 3 voice words, colours with their job, fonts, motifs, "never do" list.
2. `public/site/brand.css` - the tokens below. Pages link it and use only the variables.

## The mental model (from the AI Realist site)

**Cream is paper, espresso is ink, coral is the voice, purple marks the "AI" note.** Dark mode swaps paper and ink and keeps the accent. Style everything through variables and dark mode nearly comes free.

```css
:root {
  --paper: #fef6f0;  --paper-2: #fdf0e6;   /* page, alternate surface */
  --ink: #5b4230;    --muted: #7d614f;     /* text, secondary text */
  --accent: #f68a6b; --accent-hover: #e57a5a;   /* decoration, big type, CTAs */
  --accent-text: #b8391e;                  /* accent for SMALL text: 5.4:1 on paper */
  --note: #6a4c93;                         /* second colour for one idea only */
  --line: rgba(91,66,48,.12);              /* hairlines */
  --font-display: 'Playfair Display', Georgia, serif;
  --font-body: 'Inter', system-ui, sans-serif;
}
body.dark-mode {
  --paper: #241912; --paper-2: #2d1f17; --ink: #fff4ea; --muted: #d1b5a3;
  --accent-text: #e85c3c; --note: #c5a9e0; --line: rgba(254,246,240,.14);
}
::selection { background: rgba(106,76,147,.08); }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }
```

These are the AI Realist values: use them as the worked example, replace them with the participant's own. Fonts: self-host them in `public/site/fonts/` (the workspace ships Inter and Playfair Display with licences) so the page makes no third-party request. Persist the theme in `localStorage 'theme'` and follow `prefers-color-scheme` when unset.

## Signature motifs (reuse, don't invent more)

- **Eyebrow with a dash**: small uppercase label, wide letter-spacing, a 2.5rem hairline before it.
- **Hairline grid**: sections are grids whose cells are separated by `1px solid var(--line)`; whitespace and hairlines, not boxes and shadows.
- **Radii**: 6px buttons, 8px menus, 12px dialogs. Nothing rounder.
- **Primary button**: accent fill, uppercase, the gap between label and arrow widens on hover.
- **Headline**: light weight, tight leading, the one key word in italic accent.

## Contrast is measured, not felt

Coral `#f68a6b` on cream is about 2.2:1. It fails for text. Use it for decoration and display type of 24px bold or more; use `--accent-text` for small coloured text, links and labels. Check every text and background pair with `website-building-critique` (`check_page.py` prints the ratios). Aim for 4.5:1 for body text, 3:1 for large text and UI edges.

## Voice

Warm, editorial, opinionated; plain verbs; sentence case; specific over clever. Write a "say / don't say" list of five lines in `BRAND.md`. Any number or claim on the site needs a source note in `BRAND.md` or the page.
