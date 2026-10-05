# Plugins that pair well with the website challenge (Claude Code)

Everything here is optional. The `website-building` skills work alone. These are the plugins we use around them, with the repository each one comes from, so you can read the source before installing. Sources and commands checked on 4 October 2026 against each repository's marketplace file and README.

Install syntax (Claude Code): `claude plugin marketplace add <owner/repo>` once, then `claude plugin install <plugin>@<marketplace>`. Inside a chat the same works as `/plugin`. Codex does not use these plugins; the `website-building` skills cover the same steps there.

## Which one for which step

| Step | Plugin | What it adds | Source repository |
| --- | --- | --- | --- |
| Layout (3, 4) | **frontend-design** | A general front-end design skill; a second opinion on layout, not a replacement for the brand step | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design) (Anthropic) |
| Critique (7) | **design** (design-critique, accessibility-review, design-system, ux-copy, design-handoff) | Structured design feedback and accessibility review; `website-building-critique` calls them when present | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins/tree/main/design) (Anthropic) |
| SEO (6) | **searchfit-seo** | Wider SEO work: site audits, content strategy and briefs, schema, keyword clusters, internal links. Use it for planning and audits; use `website-building-seo` for the pass/fail check of your own HTML | [searchfit/searchfit-seo](https://github.com/searchfit/searchfit-seo) (SearchFit, MIT, third party) |
| Copy | **marketing** (brand-review, content-creation, seo-audit, campaign-plan) | Checks copy against your brand voice; drafts content | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins/tree/main/marketing) (Anthropic) |
| Brand and layout | **figma** | Read a Figma design (frames, tokens) and turn it into code | [figma/mcp-server-guide](https://github.com/figma/mcp-server-guide) (Figma) |
| Images | **canva** | Create, resize and brand-check designs in the participant's own Canva account | [canva-sdks/canva-skills](https://github.com/canva-sdks/canva-skills/tree/main/plugins/canva) (Canva) |
| Critique (7) | **playwright** | A real browser for screenshots at phone and desktop width | [anthropics/claude-plugins-public](https://github.com/anthropics/claude-plugins-public/tree/main/external_plugins/playwright), wrapping [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) |
| Deploy (8) | **cloudflare** | See the warning below | [cloudflare/skills](https://github.com/cloudflare/skills) (Cloudflare, Apache-2.0) |

## Install commands

```sh
# Anthropic official marketplace (already known to Claude Code): frontend-design, figma, canva, playwright
claude plugin install frontend-design@claude-plugins-official

# Anthropic knowledge-work marketplace: design, marketing, searchfit-seo
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install design@knowledge-work-plugins
claude plugin install searchfit-seo@knowledge-work-plugins
```

Direct from the SearchFit repository instead: `claude plugin marketplace add searchfit/searchfit-seo`, then `claude plugin install searchfit-seo@searchfit-seo` (use the marketplace name that `claude plugin marketplace list` prints). Start a new chat after installing so the skills are listed.

## Read this before installing

- **Third-party code.** `searchfit-seo`, `figma`, `canva` and `cloudflare` are written by the companies named, not by AI Realist. Skim the repository first. A plugin is instructions plus optional connectors; it can ask the agent to run commands.
- **Bundled connectors.** Several plugins ship with connector definitions. The `design` and `marketing` plugins list Slack, Linear, Asana, Notion, Atlassian, Figma, Canva and more. They do nothing until you sign in to them. **Do not sign in to any you do not need**, and never to a service that sends messages or edits company records on your behalf. Check with `/mcp` and disable what you do not use.
- **The Cloudflare plugin is not recommended for this workshop.** It bundles `https://mcp.cloudflare.com/mcp`, the account-wide API connector. Its sign-in covers a whole account and cannot be limited to your one workshop Worker. Participants publish only to their own workshop deploy, through `website-building-deploy`, `masterclass-deploy` and the facilitator's deployment target. If you want Cloudflare guidance, read the skills in [cloudflare/skills](https://github.com/cloudflare/skills) (`wrangler`, `workers-best-practices`, `web-perf`) as documentation, or use the read-only Documentation connector from `connectors.md`.
- **No plugin replaces the checks.** Run `seo_check.py` and `check_page.py` anyway; they measure, and the result goes in the handover.
