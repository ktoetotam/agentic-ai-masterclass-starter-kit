---
name: setup
description: Set up the website challenge for a non-technical participant - check the computer, make the website-building skills available in this project, create the site folders, and start the local preview. Use when someone chooses the company website build, says "set up my website", or the website skills are not yet listed in the chat.
---

# Set up the website challenge

Explain each step in one plain sentence and ask one question at a time. Do the technical work yourself within these limits: nothing is installed without asking, nothing is published, no paid service is called.

1. **Say what will happen**: you will make the website skills available, create `public/site/` for the page and `output/` for drafts, and open a local preview. Nothing leaves the computer.
2. **Check the computer**: run `node scripts/check-setup.mjs`. If Node, Python or Poetry is missing, stop and offer `masterclass-setup` to fix it.
3. **Make the skills available**: run `node scripts/activate-challenge.mjs website-building`. It copies the skills into `.agents/skills/` (Codex) and `.claude/skills/` (Claude Code) without overwriting copies someone edited, so they appear in a new chat as `website-building-build`, `-brand`, `-layout`, `-images`, `-seo`, `-critique` and `-deploy`. If the script reports BLOCKED, say in one line that the client will ask permission to copy the files, then ask the participant to approve it.
4. **Create the folders**: `public/site/` and `output/` (`output/` is already ignored by Git). Do not put anything private in `public/`.
5. **Start the preview**: `node scripts/serve.mjs`, then open the printed address. Serve only `public/`.
6. **Offer connectors (optional, one at a time)**: read `references/connectors.md` and offer the recommended two (Cloudflare Documentation, Playwright), then the optional ones the participant's plan needs (Figma, Canva, Cloudflare Observability). Say what each reads and changes, add only what they pick, finish sign-in in the browser, and never take a token in the chat. Skip this step if they decline.
7. **Hand over**: tell the participant to start a new chat and say "Use website-building-build to build my website", with the company brief or `data/company-brief.md` if they have one. Mention the optional `OPENAI_API_KEY` for generated images: it is not needed, and no paid call happens without an agreed limit.
