# Your Agentic AI Masterclass workspace

Start with [the setup guide](guides/setup.md). It covers ChatGPT/Codex access and user-account installation on Windows or Mac.

Open this extracted folder in Codex as a local project. Start a new task and ask:

> Use $masterclass-setup. Check my computer and this workspace. Install or update the workshop tools in my user account without admin rights. Use Poetry for Python dependencies, create my local .env, run the readiness check, and open the preview. Then help me get the public starter repository with Git.

Targets checked **23 September 2026**: **Python 3.14.7**, **Node.js 26.10.0 (Current)** with bundled npm, **Poetry 2.5.1** and **Git 2.55.0+**. Use `$masterclass-setup` in Codex. uv installs Python and the isolated Poetry CLI; Poetry manages this project's `.venv` and dependencies.

Once the tools and project environment are ready, from this folder:

```sh
poetry install
node scripts/init-env.mjs
poetry run python scripts/check-python.py
node scripts/check-setup.mjs
node scripts/serve.mjs
```

Open the printed preview URL; stop with Ctrl+C. No `npm install` is needed for the starter scripts. Add optional dependencies only for your chosen challenge.

Your agent also needs a browser: install [Google Chrome](https://www.google.com/chrome/) and the [ChatGPT extension](https://chromewebstore.google.com/detail/chatgpt/hehggadaopoacecdllhhajmbjkdcmajg) (Codex) or the [Claude extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) (Claude Code, Cowork). Step 3 of [the setup guide](guides/setup.md#add-browser) shows how.

## Check that everything is installed

Start a new task and ask:

> Use $masterclass-check. Check that everything for the masterclass is installed and working, without changing anything, and tell me what still needs attention.

It runs `node scripts/check-setup.mjs` and `node scripts/check-browser.mjs`, tests the preview and asks you about the account steps a script cannot see. It never installs or changes anything.

## Challenge plugins

Some challenges come with their own plugin in `.agents/plugins/plugins/`. The first is **second-brain**: the agent keeps your notes as a linked wiki (open it in [Obsidian](https://obsidian.md/download) or as a page in your browser) and answers with the exact source passage, checked by a script. Start it with:

> Set up the second brain challenge: follow .agents/plugins/plugins/second-brain/skills/setup/SKILL.md

Setup copies the challenge skills into this project with `node scripts/activate-challenge.mjs second-brain`, so they appear in a new chat as `$second-brain-ingest`, `$second-brain-ask` and `$second-brain-check`. Your notes stay in the Git-ignored `output/second-brain/` folder.

The second is **website-building**: brand, layout and motion, images, SEO, design critique and a safe Cloudflare deployment, as seven skills that run in order. Start with:

> Set up the website challenge: follow .agents/plugins/plugins/website-building/skills/setup/SKILL.md

Setup runs `node scripts/activate-challenge.mjs website-building`; afterwards say "Use website-building-build to build my website". Its two checkers, `seo_check.py` and `check_page.py`, read your HTML and cost nothing; image generation is optional and needs an agreed spend limit.

## Not sure what to build or what to do next?

> Use $masterclass-guide. Help me choose a build for today and tell me what to do next.

The guide asks a few questions, suggests builds that fit your work, writes your group's `PLAN.md`, and keeps you moving through the day up to the demo.

## Get the starter with Git

For the first session, each participant makes their own local clone of the [public starter repository](https://github.com/ktoetotam/agentic-ai-masterclass-starter-kit). Use [the short Git guide](guides/teamwork.md) and `$masterclass-teamwork`:

```sh
git clone https://github.com/ktoetotam/agentic-ai-masterclass-starter-kit.git
```

Open the cloned folder in Codex. Preserve any work you made in the extracted ZIP folder; the clone is a separate copy. This is the last setup step. Do not push to the shared starter. The facilitator will set up separate private group repositories when groups are known. GitHub accounts are useful for the workshop; local Git itself works without one.

## Dependencies and local settings

- **Python:** use `poetry add PACKAGE`, `poetry add --group dev PACKAGE` and `poetry run python ...`. Commit `pyproject.toml` and `poetry.lock` together. One teammate owns dependency changes at a time. Use `poetry install` after pulling a lockfile update; do not casually run `poetry update` or bypass the lock with pip.
- **JavaScript:** install packages locally with npm. Commit `package.json` and its lockfile; teammates use `npm ci` once a lockfile exists.
- **Variables:** put your own values in ignored `.env`. `init-env.mjs` copies `.env.example` only if `.env` is absent. Keep only safe placeholders in the example. Never copy another person's secrets.
- **Loading:** the Node preview explicitly loads root `.env` using `process.loadEnvFile`; `check-python.py` demonstrates `python-dotenv` loading with `override=False`. Existing process variables take precedence. New application entrypoints must load their own configuration; Poetry does not automatically load `.env`.

## What is included

- `guides/`: illustrated setup, troubleshooting, team Git workflow, agent practices and Cloudflare runbook.
- `AGENTS.md`: official-documentation checks, Poetry, variables, group workflow and bounded parallel-agent instructions.
- `.codex/config.toml`: project defaults for Sol medium, Luna high subagents, live search and at most two child agents. Review before trusting the project; verify effective settings in your client. See [agent settings](guides/agent-practices.md).
- `.agents/skills/`: twelve reusable workshop skills, including `masterclass-guide` and `masterclass-check`. Keep hidden folders when copying the kit.
- `.claude/skills/`: `/masterclass-guide` and `/masterclass-check` for Claude Code, without installing the plugin.
- `.agents/plugins/` and `.claude-plugin/`: optional Codex and Claude Code plugin marketplaces for the same workshop skills.
- `data/`: fictional practice inputs and expected results where useful.
- `public/`: local-preview and publishable files. Keep only public-safe content here.
- `scripts/`: readiness checks, local environment and Git setup, preview and deployment checks.
- `wrangler.workshop.json` and `deployment-target.example.json`: inactive examples until the facilitator assigns a workshop target.

Use `$masterclass-guide`, `$masterclass-check`, `$masterclass-setup`, `$masterclass-teamwork`, `$masterclass-web`, `$masterclass-research`, `$masterclass-knowledge`, `$masterclass-present-media`, `$masterclass-business-data`, `$masterclass-localise`, `$masterclass-build` or `$masterclass-deploy`. If discovery fails, ask Codex to read the corresponding `.agents/skills/<name>/SKILL.md` directly.

After you choose a challenge, ask `$masterclass-setup` to install only the missing tools for that challenge. Its `references/challenge-tools.md` covers all ten options and local fallbacks.

Keep credentials and private inputs out of `public/` and Git. Use ignored `output/` for private drafts. The kit uses no facilitator credentials and does not grant cloud access or API credits. It runs independently of the AI Realist website repository.

## Optional Codex and Claude Code plugins

The local `.agents/skills/` work in Codex without installing a plugin. For a reusable plugin, each client can add this public repository as a marketplace and install `ai-realist-masterclass@ai-realist-workshops`:

```sh
codex plugin marketplace add ktoetotam/agentic-ai-masterclass-starter-kit
codex plugin add ai-realist-masterclass@ai-realist-workshops
```

```sh
claude plugin marketplace add ktoetotam/agentic-ai-masterclass-starter-kit
claude plugin install ai-realist-masterclass@ai-realist-workshops
```

Claude Code also reads `CLAUDE.md` in this project. Its sign-in and billing are separate from ChatGPT Plus. Plugin installation is optional and is not part of the first-session setup, which ends when you get the starter repository.
