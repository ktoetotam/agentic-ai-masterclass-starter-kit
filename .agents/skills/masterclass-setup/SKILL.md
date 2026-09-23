---
name: masterclass-setup
description: Set up or diagnose an Agentic AI Masterclass participant workspace on macOS or Windows using user-owned installations, Poetry, local environment variables and group Git repositories.
---

# Prepare the participant workspace

Read `AGENTS.md` and `guides/setup.md`. `guides/setup-technical.md` is the short participant page. For installation commands, read only the relevant OS and failed-check sections of `references/platform-installation.md`; use `guides/agent-practices.md` for configuration. For GitHub account and repository steps, read `references/github-setup.md`; use `guides/teamwork.md` for the full group workflow. If these are missing, locate the extracted kit first. Work only in the participant project, outside the facilitator's website repository.

## Check before changing

1. Identify OS, architecture, company restrictions and existing tools. Search the current official vendor documentation and open the matching page before configuring a tool or changing installation commands. Use the platform reference’s official links as starting points, and link the sources used in the handover. Do not rely on search snippets or remembered configuration keys.
2. If Node is available, run `node scripts/check-setup.mjs`. Distinguish required failures from optional tools. Before invoking macOS's `/usr/bin/git` shim, check whether developer tools exist as described in the platform reference. Never dump environment values or credentials.
3. Check app access: the participant must open this folder in Codex and run a local command. A browser chat alone does not verify local execution. App sign-in, subscription, usage and company policy require the participant's confirmation; do not claim the readiness script verifies them.

## Install in the user's account

Targets checked 23 September 2026: Python **3.14.7**, Node **26.10.0 (Current)** with npm, Poetry **2.5.1**, Git **2.55.0+**. Follow the matching commands in the platform reference after verifying current official sources. Install or update only missing/outdated workshop tools, preserving other projects' runtimes and existing environments. On a later date, check official releases and select a supported stable patch; do not switch to a prerelease or silently change the workshop's runtime series.

- Bootstrap Python and an isolated Poetry CLI with uv. Discover the CLI directory with `uv tool dir --bin`; do not guess a Windows path. Poetry creates/manages the project `.venv` using the selected interpreter.
- Install Node's archive for the actual architecture; verify its official checksum. On Windows use `npm.cmd`/`npx.cmd` if PowerShell selects blocked `.ps1` launchers.
- Install Git even if the kit came from a ZIP. Use official PortableGit on Windows; use the platform reference’s isolated micromamba/conda-forge Git environment on Mac when current Git is absent. No Homebrew or Apple developer tools are needed for that route. Keep only its Git executable directory on PATH, without replacing Python or Node with conda packages.
- Restart the app/terminal after user PATH changes. Verify versions in the terminal Codex actually uses.

Do not use sudo, administrator shells, machine-wide PATH changes, Homebrew, WSL installation, execution-policy bypasses or disabled certificate checks. If company policy blocks the user install, identify the exact block and use the IT/pairing fallback in the platform reference.

## Prepare dependencies and variables

Use **Poetry only** for project Python dependencies. Keep `pyproject.toml`, `poetry.lock` and `poetry.toml` together. Run `poetry install` against the committed lock. Add packages with `poetry add` or `poetry add --group dev`; run Python through `poetry run`. Never use `pip install` or `uv pip install` to bypass Poetry. Prefer wheels; the shared Poetry configuration requires them for this compiler-free workshop.

Preserve an existing `.venv` and record its dependencies before migration. If its Python is incompatible, prepare a new extracted kit beside it and migrate the required dependency list. `poetry sync` removes packages absent from the lock: use it only after reconciling existing work, or in a fresh/disposable environment. Do not overwrite a lockfile to silence a mismatch.

Run `node scripts/init-env.mjs`; it preserves an existing `.env`. Keep actual local variables in ignored `.env` and only harmless placeholders in `.env.example`. Never print values, collect reimbursement/bank details, or put secrets in Git or `public/`. Verify explicit loading: the Node preview uses `process.loadEnvFile`, and `poetry run python scripts/check-python.py` checks the locked Python loader. Poetry alone does not load `.env`.

Use project-local npm packages and a committed lockfile for optional JavaScript dependencies. Choose only what the selected challenge needs. Core work requires no Docker, database server or paid API key. Plus and API/media charges are separate; obtain a missing budget decision before paid calls.

## Prepare group work and verify

For the first session, use `$masterclass-teamwork` and the short Git guide to help the participant clone the public starter repository into a new folder. Stop after opening the clone and checking `git status`; getting the repository is the last setup step. Keep any extracted ZIP folder and existing work. Check for enclosing/existing Git repositories first. Do not initialize the clone, configure global identity, push to the starter, or share credentials. Later group repositories require facilitator assignments.

Help each participant create or sign in to their **own free GitHub account** at `https://github.com/signup`, verify their email, and enable two-factor authentication. Let the participant handle password, passkey, email-verification and authentication prompts themselves. Show the public starter at `https://github.com/ktoetotam/agentic-ai-masterclass-starter-kit`, **Code → HTTPS**, and clone it into a separate folder. Use the click-by-click reference; check current GitHub documentation before acting if the interface changes. When groups are assigned later, help them accept the invitation, find their separate private group repository under **All repositories**, and clone that. Never create a remote or send invitations from guessed group assignments.

Read the included `.codex/config.toml` and explain its Sol/Luna defaults. Apply project settings through the normal trust workflow; do not change global permissions or claim prose can switch an active model. Follow `AGENTS.md` for appropriate model/effort and independent parallel work.

Run the readiness check, start `node scripts/serve.mjs`, and verify the loopback page. Stop only the process you started when finished unless it should stay open. Check skill discovery in a new task; use exact skill paths if discovery is unavailable.

Report **ready / needs attention / optional**, including the checks actually completed and the next challenge prompt. Use `guides/troubleshooting.md` for failures. Reimbursement covers one month of ChatGPT Plus: the participant emails their receipt and bank transfer details to hello@airealist.org themselves; do not promise additional expenses.
