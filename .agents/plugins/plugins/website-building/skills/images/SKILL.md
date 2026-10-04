---
name: images
description: Make the images for a website in three tiers - hand-built SVG, CSS gradients with grain, and (only with an agreed spend limit) generated images through the OpenAI image API using scripts/generate_image.py - with alt text, contrast overlays and a social preview image. Use when a page needs a hero, illustration, background, diagram or social card.
---

# Images

Pick the cheapest tier that does the job. Order of preference:

1. **Hand-built inline SVG** - diagrams, line drawings, organic shapes. Crisp at any size, uses the brand variables so it follows dark mode, costs nothing, works offline. Usually the better choice.
2. **CSS gradients plus grain** - layered low-alpha radial gradients of the accent colours over the paper colour. The zero-dependency floor.
3. **Generated images** - only when the participant has agreed a provider, a spend limit and who pays (this project's default extra API spend is zero). Ask once, with a number: "up to 3 images, about X, OK?".

## Generating (tier 3)

`OPENAI_API_KEY` must be in `.env`; never print it, never put it in `public/`. Preview what would be sent first - this costs nothing:

```sh
poetry run python .agents/skills/website-building-images/scripts/generate_image.py --dry-run --prompt "warm sunlit desk with a ceramic cup" --brand output/BRAND.md --out public/site/assets/hero.png
```

Drop `--dry-run` to generate, once the spend is agreed. Rules that keep results usable:

- **Text-free backgrounds**: the script adds "no text" and the brand mood. Use these under HTML text, always with a paper-coloured overlay between photo and text so the image never carries the text's contrast.
- **Graphics that must carry words** (social cards): quote every string exactly, list them all, end the prompt with "No other text anywhere", then proofread character by character. Dates and prices are what the model gets wrong most.
- Style words that read as generic AI: glossy 3D, neon, blue circuit boards, robots. Prefer matte, warm, grainy, editorial.
- Save under `public/site/assets/`, compress to a sensible size (hero under about 300 KB as WebP or JPEG), and record prompt, model and date in `output/image-log.md`.

If the key is missing, say so in one line, build with tier 1 or 2, and leave the exact command in an HTML comment where the image would go. Never claim an image was generated when it was not.

## Every image

- Meaningful images get alt text that says what the image shows for this page; decoration gets `alt=""`.
- Set `width` and `height` to stop layout jumps; `loading="lazy"` below the fold, never on the main hero.
- Social preview (`og:image`): 1200x630, text legible at thumbnail size, saved as `public/site/assets/og.png` (see `website-building-seo`).
- Use licensed or participant-owned media only. Fictional people or products are labelled fictional.
