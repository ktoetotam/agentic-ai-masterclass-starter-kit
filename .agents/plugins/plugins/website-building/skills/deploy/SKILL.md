---
name: deploy
description: Prepare a built website for the assigned Cloudflare workshop Worker - what may sit in public/, a _headers file for security and noindex, a 404 page, the local guard, a Wrangler dry run - and stop before publishing unless the participant directly asks. Use when the site is ready to go online, or when asked about Cloudflare, Workers, hosting or "put it live".
---

# Prepare the site for Cloudflare

This skill prepares. **Publishing needs the participant's direct request and the facilitator-issued deployment target.** Never touch the AI Realist production account, its Worker, DNS or routes. For the actual deploy, hand over to `masterclass-deploy` and `guides/facilitator-cloudflare.md`.

## Facts checked against Cloudflare's documentation (Workers static assets)

- `assets.directory` points at the folder that is uploaded. Here it is exactly `./public`, and the local guard rejects any other key in `assets`. So do not add `html_handling` or `not_found_handling` to `wrangler.workshop.json`.
- Default routing serves `about.html` as `/about` and `about/index.html` as `/about/` (the `auto-trailing-slash` default). Link accordingly and test it.
- A plain-text `_headers` file inside the assets folder sets response headers for **assets**: `/path` on one line, then indented `Name: value` lines, `*` wildcards, up to 100 rules. The file itself is not served.
- Default `Cache-Control` for assets is `public, max-age=0, must-revalidate`.
- Source: Cloudflare Workers docs, "Static Assets" (headers, routing and HTML handling pages), read on 4 October 2026. Re-read them if Cloudflare's behaviour looks different.

## Connectors that help (optional)

The Cloudflare Documentation MCP server (`https://docs.mcp.cloudflare.com/mcp`) lets you read current docs instead of relying on memory. Observability and Workers Bindings servers can show the **workshop** account's logs and resources; they can also change things, so keep write tools off and never use them to publish. Do not use the broad Cloudflare API server here. Setup commands and cautions: `website-building-setup`, `references/connectors.md`.

## Preflight, in order

1. **Public means public.** Walk `public/` and read the list. No `.env`, notes, drafts, extracts, `AGENTS.md`, `package*.json`, keys, personal data. No symlinks, no dotfiles (the guard blocks them). Fictional content stays labelled fictional.
2. **Run the page checks**: `website-building-critique` and `website-building-seo` must have passed on the final files.
3. **`public/_headers`** (create if missing; adjust, do not blindly paste):

   ```
   /*
     X-Content-Type-Options: nosniff
     Referrer-Policy: strict-origin-when-cross-origin
     X-Frame-Options: DENY
   ```

   For a private workshop demo also add `X-Robots-Tag: noindex, nofollow` under `/*`. Add a `Content-Security-Policy` only after testing that fonts, images and scripts still load.
4. **`public/404.html`** with a link home. Without `not_found_handling`, an unknown path is not guaranteed to show it; say so in the handover rather than promising it.
5. **Local guard** (changes nothing, deploys nothing): `node scripts/check-deploy.mjs`. It needs `deployment-target.json` from the facilitator; if that is missing or still has placeholders, stop here, finish the local build and tell the participant exactly what is needed.
6. **Dry run** (builds the upload without publishing): `npx wrangler deploy --config wrangler.workshop.json --dry-run`. Read the file list it prints.

## Publish (only on a direct request)

Follow `masterclass-deploy`. After publishing, open the real `workers.dev` address and check: the home page loads, one inner page loads, the 404 behaviour you documented, the response headers (`curl -I`), and the page on a phone-sized viewport. Report what you actually saw.

## Never

Add routes, custom domains or extra bindings; create accounts or resources; change DNS; paste a token into a file or a chat; deploy from a configuration that names a different account than `deployment-target.json`.
