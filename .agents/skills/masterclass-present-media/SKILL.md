---
name: masterclass-present-media
description: Create the masterclass HTML presentation or a small media prototype with a narrative, accessible playback, export checks and explicit generation budgets.
---

# Presentations and media

Choose the requested deliverable before selecting tools. Use `data/company-brief.md` and `data/media/storyboard.md` as fictional inputs. A useful workshop output is an HTML deck or a short captioned media sequence; the skill does not require a paid generation account.

## HTML deck

Define the audience, decision and narrative. Give each slide one clear point and keep source notes for factual claims. Build keyboard navigation, a visible current-slide indicator, readable mobile layouts and reduced-motion behaviour. Prefer assets stored alongside the deck over runtime dependencies on external CDNs.

Provide print CSS that creates one slide per PDF page and hides navigation. Use browser print-to-PDF for the baseline export; optional Playwright Chromium can automate printing and screenshots. Inspect the resulting PDF for clipping, blank pages and text size. A generated `.pptx` is optional; `python-pptx`/PptxGenJS create files but do not by themselves prove that the slides render correctly.

Narration is optional. Start with a script and participant-recorded audio, then add captions and click-to-play controls. Do not rely on autoplay with sound. When voice cloning is requested, use only a voice the participant owns or has explicit permission to clone, and identify generated narration appropriately. Shared deck authentication requires a real server/hosting access boundary; hiding a link or using client-side passwords is not authentication.

## Media studio

Write a short production brief: intended channel, aspect ratio, duration, permitted assets and output format. Plan a storyboard before generating media. Use participant-owned/licensed inputs or clearly labelled fixtures. Keep attribution/licensing notes with the project.

Use the tools actually available. If image/video/audio generation requires a separate provider, confirm the account, exact budget ceiling, number of generations, duration/resolution and retry limit before calls. ChatGPT subscription entitlement is not an API credit balance. Stop generation when the agreed limit is reached; do not retry expensive jobs blindly.

For assembly, use an already available FFmpeg or a user-local installation approved by the participant; never assume a Python wrapper includes the executable. Preserve originals, use a short test export, then verify playback, audio level, caption timing and duration. Browser animation, a storyboard and recorded narration are viable fallbacks when generators or FFmpeg are unavailable.

Minimum deck demo: keyboard navigation and a legible PDF export. Minimum media demo: a 15–30 second local sequence or playable narrated storyboard with captions. Put previewable output in `public/presentation/` or `public/media/`, and keep source recordings, drafts, asset lists and reproduction steps in `output/`. Publish only to the assigned sandbox when requested; do not upload source recordings by default.
