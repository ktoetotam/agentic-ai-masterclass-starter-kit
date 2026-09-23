# Get the starter repository

Tomorrow we will set up **Git**, get the starter project from GitHub, and try a local branch. **No groups, invitations, or shared repositories yet.**

## 1. Install Git

In Codex, open your masterclass project and say:

> Use $masterclass-setup to check Git on my Mac or Windows computer. If it is missing, install it in my user account. Show me `git --version` when it works.

The [installation skill](setup-technical.md#install-git) handles the commands; you do not need administrator access.

## 2. Make your own GitHub account

Already have one? [Sign in](https://github.com/login). Otherwise [sign up for a free account](https://github.com/signup) and verify your email. GitHub asks you to complete account and security steps yourself. GitHub is where you get the starter; Git is the tool on your computer.

## 3. Get the starter

Open the [AI Realist starter repository](https://github.com/ktoetotam/agentic-ai-masterclass-starter-kit). Click **Code → HTTPS → Copy**. In Codex, ask:

> Clone this starter repository into a new folder on my computer: https://github.com/ktoetotam/agentic-ai-masterclass-starter-kit.git. Open the cloned folder as my project. Keep any work I already have in the downloaded ZIP folder.

Or use a terminal in your normal projects folder:

```text
git clone https://github.com/ktoetotam/agentic-ai-masterclass-starter-kit.git
cd agentic-ai-masterclass-starter
git status
```

If you already started in the ZIP folder, keep it. The clone is a second copy with Git history. Do not run `setup-team-repo.mjs` inside a clone.

## 4. Try Git locally

Ask Codex:

> In this cloned starter, show me the latest commit and help me create my own practice branch. Let me make one small change, review it, and commit it locally. Do not push to the shared starter repository.

You can also see the latest commit with `git log -1 --oneline`. Your practice branch and commit stay on your computer. Later, when groups are known, the facilitator will provide a separate group repository for sharing work. Do not push changes to this starter repository.
