@AGENTS.md

## Claude Code

The shared instructions above apply here too: source checks, Poetry dependency rules, `.env` handling, Git workflow and deployment boundaries. Read the relevant guide in `guides/` for the task at hand.

- **Skills.** The workshop skills are in `.claude/skills/` under the same names as in Codex: `/masterclass-guide`, `/masterclass-check`, `/masterclass-setup` and so on. They are generated copies of `.agents/skills/`, which is the maintained version. Edit `.agents/skills/masterclass-*`, then run `node scripts/sync-claude-skills.mjs`; never edit the copies in `.claude/skills/`. For any new or changed skill or plugin, follow `/masterclass-plugin-authoring`.
- **Challenge plugins** such as `second-brain` and `website-building` live in `.agents/plugins/plugins/`. Their setup skill runs `node scripts/activate-challenge.mjs <challenge>`, which copies the challenge skills into `.claude/skills/` (for example `/second-brain-ask`).
- **Codex-specific wording.** In the shared guides and skills, read `$masterclass-x` as `/masterclass-x`. The GPT model names, `.codex/config.toml` and the `codex/` branch prefix apply to Codex only; Claude Code uses the model and effort selected in its own client.
- **Billing.** Claude Code access has its own sign-in and billing. Do not assume ChatGPT Plus pays for it or for API usage.

For the first session, install the needed local tools, make a free GitHub account, then clone and open the public starter repository. Stop there. The facilitator will arrange group repositories later.
