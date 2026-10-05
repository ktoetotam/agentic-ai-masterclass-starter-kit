---
name: masterclass-check
description: Check, without installing or changing anything, that a masterclass participant has everything the workshop needs - Python, Node, Poetry, Git, GitHub CLI and its sign-in, Wrangler, the shared Python libraries, the project environment, the cloned starter, Google Chrome with the ChatGPT or Claude extension, the local preview and the account steps including Google Drive - and report ready / needs attention / optional in plain language with the exact next step. Use before the workshop, at the 10:25 tool check, after any installation, or when someone asks "am I set up?", "did I install everything?" or "check my computer".
---

# Check my setup

Confirm the participant is ready, in plain language, without changing their computer. This skill only reads and runs checks. Fixes belong to `masterclass-setup` and to the participant's own clicks in `guides/setup.md`.

Tell the participant in one line what you will check and that nothing will be installed or changed. Work from the project root.

## 1. Run the automatic checks

1. `node scripts/check-setup.mjs`: Node, npm, Git, GitHub CLI, whether Git uses the GitHub CLI sign-in, the pinned Wrangler, project Python, Poetry, the project environment, the lockfile, the locked Python packages, `.env` and the starter files.
   Then `poetry run python scripts/check-python.py`: imports the shared libraries for PDFs, Excel, Word, web requests and news feeds.
   If `gh` is available, `gh auth status` shows whether the GitHub sign-in is still valid. Report only logged in / not logged in and the account's existence, never the token or its scopes.
2. `node scripts/check-browser.mjs`: Google Chrome (or Microsoft Edge), the ChatGPT and Claude browser extensions, and whether Codex or Claude can connect to them. It only looks at app locations and extension folder names, never at browsing data.

If `node` is missing, report Node as the first thing to fix and check the rest by hand with version commands only (`python3 --version`, or `py --version` on Windows; `poetry --version`). On a Mac, run `xcode-select -p` before `git --version`. If that fails, report Git as missing instead of running `git`, because it would open Apple's installer.

## 2. Check the project

Read-only:

- `git rev-parse --show-toplevel` and `git remote get-url origin`: is this the cloned starter (`ktoetotam/agentic-ai-masterclass-starter-kit`) or the group's assigned repository? A folder extracted from the ZIP has no `.git`; that is fine before the Git step.
- `git status --short`: report the number of changed files, not their contents.
- Do not open or print `.env`. Its existence is enough.
- If `PLAN.md` names a build, check that build's optional tools from `.agents/skills/masterclass-setup/references/challenge-tools.md` with an import or version command only, for example `poetry run python -c "import pandas"`.

## 3. Run the live checks

- **Preview:** start `node scripts/serve.mjs`, request the printed `http://127.0.0.1:<port>` address once, confirm it answers with status 200 and the starter page, then stop only the process you started.
- **Browser control:** only if this session already has browser tools (the Codex Chrome plugin or Claude in Chrome), open that preview address in the participant's browser and read the page heading. It proves the extension works end to end. If no browser tools are available, leave it as a manual check; do not install anything to make it work.

## 4. Ask about what a script cannot see

Ask once, as a short yes/no list:

- Signed in to the ChatGPT desktop app with Plus (or Pro), with this folder open as a Codex project.
- A free GitHub account exists, its email is verified and two-factor authentication is on.
- In Chrome, `chrome://extensions` (typed into the address bar) shows the ChatGPT or Claude extension with its switch **blue**, and the extension is pinned next to the address bar (puzzle-piece icon, then the pin).
- Using Codex: ChatGPT app → **Settings → Computer Use** shows **Manage** next to Chrome.
- Using Claude Code or Cowork: a paid Claude plan (Pro, Max, Team or Enterprise), signed in to the Claude extension; in Claude Code, `/chrome` shows **Status: Enabled** and **Extension: Installed**.
- **Google Drive** is connected in the ChatGPT app (**Plugins → Google Drive**), with an account their company allows, and a new Codex chat could list three file names. If Codex cannot reach Drive, they know the fallback: download the file into the project's `private/` folder. Do not open Drive files to check this.
- Their company allows these tools with the material they plan to use.

Record what they confirm as "confirmed by participant", never as "checked".

## 5. Report

Use one table, then one next step:

| Status | Item | What it means and what to do |
| --- | --- | --- |
| Ready | ... | ... |
| Needs attention | ... | One plain sentence and a paste-ready fix |
| Optional | ... | ... |

- Map script output: `OK` → Ready, `NEEDS SETUP` → Needs attention, `OPTIONAL` → Optional.
- Runtimes, Poetry, Git, packages and `.env`: the fix is a paste-ready message such as "Use $masterclass-setup to install Node 26.10.0 in my user account without admin rights." Name skills the way the current client invokes them.
- Browser and extensions: point to step 3 of `guides/setup.md` with the official links. The participant installs Chrome and clicks **Add to Chrome** and the permission prompts themselves. Never install extensions, accept browser permissions or sign in on their behalf.
- "Installed" is not "working". A found extension folder does not prove it is switched on or signed in; say so when the live browser check did not run.
- End with **Ready for the workshop** only when every required item is Ready and the participant confirmed the account items. Otherwise give the single most important next step.

Save the same summary, with date and time, to `output/setup-check.md` so it can be shown at the tool check. Include versions and statuses only: no `.env` values, tokens, account names or browser profile contents.

## Boundaries

Do not install, update, uninstall, change settings, edit `.env`, change Git state or sign in to anything. Do not report a check as passed unless it ran in this session. If a check cannot run (blocked by company policy, no permission), say which one and why.
