# Connectors for the accountant agent

**None is needed:** the challenge works with the files in `data/accountant-pack/` and the Stripe snapshot. Offer these one at a time, say what each can see and change, and add only what the participant picks. Sign-in happens in the browser; a key, if one is unavoidable, goes into the ignored `.env` by the participant and is read through an environment variable. Never paste a key into the chat. Checked against the vendors' documentation on 7 October 2026; recheck before changing configuration.

## Stripe (sandbox only)

The facilitator seeds one Stripe sandbox and hands out a **read-only agent key** (restricted key marked for agents). `books.py stripe` reads it from `STRIPE_API_KEY` in `.env`. To let the agent ask Stripe questions directly, connect Stripe's MCP server, `https://mcp.stripe.com` ([Stripe MCP](https://docs.stripe.com/mcp)):

- **Codex:** add to this project's `.codex/config.toml`, after asking, a table that reads the key from the environment:

  ```toml
  [mcp_servers.stripe]
  url = "https://mcp.stripe.com"
  bearer_token_env_var = "STRIPE_API_KEY"
  ```

  `codex mcp add stripe --url https://mcp.stripe.com` writes to the personal `~/.codex/config.toml` instead and then signs in with OAuth; say so first.
- **Claude Code:** a project `.mcp.json` entry with the header `"Authorization": "Bearer ${STRIPE_API_KEY}"`, or `claude mcp add --scope local --transport http stripe https://mcp.stripe.com/` and `/mcp` to sign in with OAuth.
- From 31 October 2026 Stripe's MCP server accepts only OAuth or agent keys. With OAuth, choose the **sandbox only**, never a live account.
- Stripe asks a person to confirm refunds and payouts made through MCP, and agent keys fall under approval rules. The agent still never writes to Stripe in this challenge.

## Google Workspace (the workshop account)

Use the account the facilitator gave you (`...@hypefree.ai`), never a work account: a company's Google admin often has to approve the connector, which shows as "requested".

- **Codex:** Plugins → Google Drive, Gmail. **Claude:** Settings → Connectors → Google Drive, Gmail.
- Read only. Save what you need into `output/accountant/downloads/` and run `books.py collect --add output/accountant/downloads`.
- Drafts in Gmail only after the participant says yes to each one; never send.

## With your own data, after the course

| Need | Safer route | Connector |
| --- | --- | --- |
| Bank | Export CSV or CAMT from online banking; the agent never gets a bank login | Most German banks publish no MCP server |
| Payments | Stripe with a read-only agent key | Stripe MCP (official); OAuth limited to what you allow |
| Bookkeeping | A DATEV-format export your tax adviser imports, checked by them | Xero publishes an official MCP server; Lexware Office, sevDesk and DATEV have community servers only: read their code first |
| Customers | A CSV export | Notion, HubSpot (official MCP servers) |
| Documents | One Drive or SharePoint folder, read-only | Google Drive, Microsoft 365 connectors |

## Official skills and plugins from the vendors

Vendors publish agent skills for their own products. They explain the product; they never replace `books.py`, which does every sum. Offer them only when the participant asks, install only what they pick, and say what each one can do before installing it. Checked 7 October 2026.

- **Stripe agent skills** ([docs.stripe.com/skills](https://docs.stripe.com/skills)). The index at `https://docs.stripe.com/.well-known/skills/index.json` lists ten skills. In the workshop install only the two that read and explain:

  ```bash
  npx skills add https://docs.stripe.com --skill stripe-docs --skill stripe-best-practices
  ```

  `stripe-docs` looks things up in Stripe's documentation; `stripe-best-practices` covers sandboxes, subscriptions, refunds and key permissions. Manually installed skills do not update themselves (`npx skills update -y`).
- **Never install `stripe-pay`** in this challenge: it lets an agent send money to another business. `npx skills add https://docs.stripe.com` without `--skill` installs it together with the rest, and so does the Stripe plugin.
- **Stripe plugin** ([Agent plugins for Stripe](https://docs.stripe.com/agents/plugin)): all Stripe skills plus the Stripe MCP server, kept up to date. Claude Code: `claude plugin install stripe@claude-plugins-official`. Codex: `codex plugin add stripe@openai-curated`. It signs in to a Stripe account, so it is for after the course, with a sandbox; during the workshop use the read-only key and the setup above.
- **Anthropic `finance` plugin** for Claude Code ([knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins/tree/main/finance)): month-end close, journal entries and a `reconciliation` skill for bank, subledger and intercompany reconciliations. Install with `claude plugin marketplace add anthropics/knowledge-work-plugins` and `claude plugin install finance@knowledge-work-plugins`. Compare its method with `books.py reconcile`; it is not financial, tax or audit advice. It also lists Snowflake, Databricks, BigQuery and Slack connectors: do not sign in to any you do not need.
- **Gmail and Google Drive**: the ready-made Claude connectors or Codex plugins above. Google's own Workspace CLI (`googleworkspace/cli`) ships agent skills too, but says it is not an officially supported Google product and needs a Google Cloud project: skip it in the workshop.
