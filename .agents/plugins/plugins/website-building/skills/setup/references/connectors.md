# Optional connectors and plugins for the website challenge

A connector (MCP server) lets the agent use another service. **None is needed**: the challenge works with the skills, the local preview and the browser alone. Offer these one at a time, say what each can see and change, and add only what the participant picks. Servers are added per project, never with a token typed into the chat or saved in a tracked file.

Commands and keys below were checked against the vendors' current documentation on 4 October 2026 (Claude Code MCP page, Codex config reference, Cloudflare MCP server list, Figma MCP installation page, Playwright MCP readme). Re-check before changing configuration; versions move.

## Rules for every connector

- Ask before adding. One sentence: what it reads, what it can change, whether it costs money.
- Sign-in happens in the browser (OAuth). Never paste a password, API key or token into the chat. A token, if one is unavoidable, goes into an ignored `.env` and is read through an environment variable.
- Prefer read-only. Use `enabled_tools` (Codex) or the client's tool approval (Claude Code) to keep write actions off.
- Cloudflare: the only Cloudflare connector is the read-only Documentation server. Deploying happens only to the participant's own workshop Worker, named in `deployment-target.json`, never the AI Realist production account, and never through an account-wide connector.
- Project-scoped Claude Code servers are saved in `.mcp.json`; this repository ignores nothing there, so check `git status` and do not commit one that carries a header with a token.

## Tier 1: recommended

| Connector | Why | Cost and risk |
| --- | --- | --- |
| **Cloudflare Documentation** `https://docs.mcp.cloudflare.com/mcp` | The agent reads current Cloudflare docs while preparing the deploy. Read-only reference. | Free; no account access |
| **Playwright** (`npx @playwright/mcp@latest`) | A real browser the agent drives for the critique step: viewport sizes, screenshots, clicks. Needs Node (already required) and a browser download that managed laptops may block. The built-in browser tools of the client do the same job when available. | Free; runs locally |

Claude Code:

```sh
claude mcp add --transport http cloudflare-docs https://docs.mcp.cloudflare.com/mcp
claude mcp add playwright npx @playwright/mcp@latest
```

Codex:

```sh
codex mcp add cloudflare-docs --url https://docs.mcp.cloudflare.com/mcp
codex mcp add playwright npx "@playwright/mcp@latest"
```

## Tier 2: only if the participant wants it

| Connector | Server URL | Use | Sign-in and risk |
| --- | --- | --- | --- |
| **Cloudflare Workers Bindings, Observability, API and every other Cloudflare account connector** | `bindings.`, `observability.`, `mcp.cloudflare.com` | None | **Not offered.** Their OAuth sign-in covers a whole account and cannot be limited to one Worker. Participants touch only their own workshop deploy, and only through `website-building-deploy`, `masterclass-deploy` and the facilitator-issued target. Only the read-only Documentation connector is used for Cloudflare |
| **Figma** | `https://mcp.figma.com/mcp` | Bring an existing design (frames, colours, variables) into the brand and layout steps | OAuth to Figma; reads the files the participant opens |
| **Canva** | `https://mcp.canva.com/mcp` | Pull or export a logo or social image the participant already designed | OAuth to Canva; use only the participant's own designs |

Claude Code (`--scope user` makes it available in every project; the default keeps it to this project):

```sh
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

Then run `/mcp` in Claude Code, pick the server and finish the browser sign-in (`claude mcp login <name>` does the same from the terminal).

Codex: `codex mcp add figma --url https://mcp.figma.com/mcp`, then `codex mcp login figma`. To keep a server read-only, edit `~/.codex/config.toml` and list only the read tools you have inspected:

```toml
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
enabled_tools = ["get_design_context", "get_screenshot", "get_metadata"]
```

Keys used: `url`, `enabled`, `enabled_tools`, `disabled_tools`, `bearer_token_env_var`. Use `bearer_token_env_var` (the name of an environment variable) for any token; never write the token into the file.

## Plugins and skills worth knowing

- **Already in this starter**: the `website-building` skills, `masterclass-web` and `masterclass-deploy`.
- **Claude Code, optional**: `/plugin install frontend-design@claude-plugins-official` adds a general front-end design skill. Use it as a second opinion on layout, not instead of the brand step.
- **Client built-ins**: if the client offers design critique or accessibility review skills, `website-building-critique` can call them for a second opinion; it works without them.
- **GitHub**: use the `gh` command-line tool the workshop already sets up for branches and pull requests. A GitHub connector is not needed.

## What not to add for this challenge

Connectors that send messages, email, calendars or chat on the participant's behalf; payment, analytics and ad accounts; anything that wants a production Cloudflare, DNS or domain account.
