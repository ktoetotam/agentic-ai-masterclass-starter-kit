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

For Claude Code, Anthropic's `finance` plugin ([knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins/tree/main/finance)) has a reconciliation skill worth reading. It also lists Snowflake, Databricks, BigQuery and Slack connectors: do not sign in to any you do not need.
