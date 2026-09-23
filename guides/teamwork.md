# Get the starter repository

Tomorrow we will set up **Git** and get the starter project from GitHub. **No groups, invitations, or shared repositories yet.**

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
cd agentic-ai-masterclass-starter-kit
git status
```

If you already started in the ZIP folder, keep it. The clone is a second copy with Git history. Do not run `setup-team-repo.mjs` inside a clone.

**Done:** open the cloned folder in Codex. The facilitator will provide separate group repositories later. Do not push changes to the shared starter repository.
