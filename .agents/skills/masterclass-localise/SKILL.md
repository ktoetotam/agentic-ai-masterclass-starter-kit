---
name: masterclass-localise
description: Build a terminology-aware document or website localisation workflow that preserves structure, checks placeholders and records linguistic review issues.
---

# Localisation agent

Start with source/target languages, locale, audience, content type and brand voice. Use `data/localisation/en.json`, `glossary.csv` and `brief.md` when no approved source is available. Deliver translated content plus a QA report; keep originals intact.

1. Inventory strings or document sections and identify content that must remain unchanged: product names, identifiers, URLs, variables, markup and numbers whose meaning must be preserved. Track each unit by a stable key.
2. Apply the supplied glossary, register and locale conventions. Preserve placeholder names exactly, allow locale-specific word order, and handle plurals explicitly. Do not convert currencies, units or contractual meaning unless asked. Ask for the intended meaning only when ambiguity materially affects the translation; otherwise record the assumption.
3. Compare source and target keys, placeholder sets, links, numbers and markup. Report missing/extra keys, inconsistent approved terminology and suspicious omissions. Flag contradictory source claims rather than resolving them through invented facts.
4. Render the translated page/document where possible. Check expansion, button wrapping, reading order, language tags and relevant scripts/fonts. For RTL locales, check layout direction separately from string translation and keep mixed-direction identifiers usable.
5. Produce a human review queue for ambiguity, domain terms and high-impact statements. Distinguish an automated consistency check from linguistic sign-off. If the participant asks about a named ISO standard, consult its current official scope and the authorized text they provide; do not claim certification or compliance from these checks alone.

Keep model/API use within the participant's approved budget and data permissions. A JSON/CSV workflow with Codex-assisted translation needs no separate translation API. `.docx` parsing may justify `python-docx`, but retaining a file extension does not prove visual fidelity: inspect a rendered document before claiming preserved layout. Offer text/HTML output if the renderer is unavailable.

Minimum demo: translate the sample to the requested locale, preserve all keys and variables, apply the glossary, and show a QA report with any unresolved questions. Suggested output: `output/localisation/` containing target strings, glossary decisions and the review report.
