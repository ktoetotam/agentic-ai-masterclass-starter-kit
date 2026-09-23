# Work together in a team repository

Each group uses **one private GitHub repository**, and each participant works in their own local clone and branch. Choose one repository owner to prepare the first copy and invite the group. The facilitator supplies the approved GitHub owner, repository name, and group membership; those destinations must be confirmed before creating repositories or granting access.

If your facilitator has already created your group repository from the private starter template, accept the invitation and go straight to **Each teammate clones their own copy** below. Do not initialize another repository or push a separate first commit into it.

You can begin immediately on one shared laptop with a local Git repository. Take turns as the driver while the others review. A remote repository is needed when several laptops exchange changes; a local repository alone does not synchronize them.

## Start with Codex

Open the extracted workshop folder in Codex and use:

> Use $masterclass-teamwork to help our group work together. Our team slug is team-01. First check Git and whether this folder is already a repository. If we are the designated owner, initialize this standalone kit locally and help us review the first commit. If a shared repository already exists, help me clone the approved URL into a separate folder and create my own branch. Preserve existing files and history. Do not create a remote repository or invite people until the facilitator has supplied the owner, repository name, and membership.

Install **Git 2.55.0 or newer** with the [user-account installation instructions](../../../../guides/setup-technical.md#install-git), then reopen the terminal and check:

```text
git --version
```

No GitHub account is required for local work. Each person needs their own GitHub account and access to the assigned repository for the shared remote workflow. Use GitHub's supported sign-in or credential manager; never share a GitHub account or put a token in a remote URL. A free personal GitHub account can host a private repository with collaborators. Organization policies may impose additional requirements. [GitHub collaborator access](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/inviting-collaborators-to-a-personal-repository).

## The owner prepares the first copy once

Extract the complete starter into a normal project folder outside the AI Realist website checkout and outside any other Git repository. Keep the hidden `.agents`, `.codex/config.toml`, and `.gitignore` files. Open a terminal **inside that extracted folder**, then replace `team-01` with the assigned team slug:

```text
node scripts/setup-team-repo.mjs --team team-01
git status --short
```

The helper checks the standalone kit and Git version, creates a local `main` branch, and appends ignore rules for local credentials and generated files. It never stages, commits, creates a remote, publishes, or changes global Git settings. Repeating it for the same initialized team preserves existing branches and work. It refuses to initialize inside the website or overwrite an unrelated repository. [Git initialization](https://git-scm.com/docs/git-init).

If this folder is already a clone or a repository created another way, keep it. Inspect `git status`, `git remote -v`, and `git log -3 --oneline`, then follow the existing-repository workflow with Codex. Do not delete `.git` to make initialization succeed.

Set your own commit identity for this repository only. Replace both example values; use the email or GitHub-provided private `noreply` address you want attached to commits:

```text
git config --local user.name "Your Name"
git config --local user.email "your-commit-email@example.com"
```

This changes no other project's identity. [Project-specific Git settings](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup).

Review the starter files, then stage the known project paths. These commands assume the complete distributed kit; if a named file is missing, inspect the folder rather than changing to `git add .`.

```text
git add -- .gitignore .env.example .node-version .python-version README.md AGENTS.md package.json
git add -- .codex/config.toml
git add -- pyproject.toml poetry.lock poetry.toml
git add -- .agents guides data scripts public wrangler.workshop.json deployment-target.example.json
git diff --cached --stat
git diff --cached
```

Check the actual staged content: only synthetic fixtures, reviewed source code, and safe project configuration should be included. Review and preserve the shared `.codex/config.toml`; stage that file explicitly, never the whole `.codex` directory, which may acquire private local files. Do not include `.env`, `.dev.vars`, `.venv`, credentials, installation receipts, private source data, or generated `output/`. `.env.example` contains variable names and safe placeholders; every teammate creates their own ignored `.env`. Never copy secret values into shared configuration or another tracked file. Ignore rules do not remove already tracked secrets or recognize every possible secret filename. [Selecting files for a commit](https://git-scm.com/docs/git-add).

Once the staged diff is correct:

```text
git commit -m "Start team workshop project"
```

Stop here if the remote owner or team assignments are pending. Local development and reviewed commits can continue.

## Connect the approved private repository

Only the designated owner or facilitator does this once, after the destination and membership are agreed:

1. On GitHub, create the assigned repository under the approved owner and select **Private**. Leave README, `.gitignore`, and license initialization unchecked because the local repository already has its first commit. If the repository already contains work, preserve it and clone/integrate it with Codex instead of pushing over it. [Create a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository).
2. Invite only the assigned group through the repository's access settings. For an organization repository, give the group contribution access such as **Write**, not organization-wide administration. For a personal repository, use its collaborator flow. Invitations must be accepted before a private clone can work.
3. Copy the repository's actual HTTPS clone URL. Replace the all-capital placeholders below; never insert a token into the URL.

```text
git remote -v
git remote add origin https://github.com/APPROVED-OWNER/APPROVED-TEAM-REPO.git
git remote -v
git push --set-upstream origin main
```

If `origin` already exists, inspect it and use it only if it is the approved team repository. Do not overwrite its URL automatically. No force push is needed. GitHub CLI is optional; the browser and Git commands are enough. [Publish existing local code](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github).

## Each teammate clones their own copy

Accept the repository invitation. In a terminal in your normal projects folder, outside the owner's copy and other repositories, replace the URL and local folder name:

```text
git clone https://github.com/APPROVED-OWNER/APPROVED-TEAM-REPO.git team-01
cd team-01
```

Open this new folder in Codex. Set your own local commit identity as above, then follow the [setup guide](../../../../guides/setup.md) for this copy. Install from the committed Poetry lockfile; create your own `.env`. Do not copy another participant's `.venv`, Git credentials, or `.env`. Cloning preserves the shared history; do not rerun the initializer in a clone. [Clone a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

Agree small pieces of work, with one person responsible for each file or area. For example, one person prepares data, another builds the display, and another checks outputs. Choose one dependency owner for `pyproject.toml` and `poetry.lock`; others request dependency changes instead of independently regenerating the lockfile. Commit those two files together. Teammates normally run `poetry install` using the committed lock, rather than `poetry update`. [Poetry and reproducible application dependencies](https://python-poetry.org/docs/basic-usage/#committing-your-poetrylock-file-to-version-control).

## The everyday loop

Begin a small task with a clean working tree. If `git status` shows unfinished changes, preserve them in the existing branch before switching; ask Codex to help if unsure. Replace the example branch name with your name and task:

```text
git status
git switch main
git pull --ff-only
git switch -c codex/anna-chart
```

`--ff-only` stops when your branch has diverged, so Git cannot silently create an unexpected merge while updating `main`. If it stops, inspect the history with Codex; do not reset away local work. [Fast-forward pulls](https://git-scm.com/docs/git-pull).

Build and test your small change. Stage only the paths you reviewed; this example changes the public page:

```text
git diff
git add -- public/index.html
git diff --cached
git commit -m "Add the team chart"
git push --set-upstream origin codex/anna-chart
```

Open a pull request on GitHub from your branch into `main`. Explain the change and how you tested it. Ask another teammate to review and run the relevant check; that reviewer merges it when ready. Configure required reviews if the repository's plan and policies support them; otherwise follow the same rule as a team agreement. Keep `main` demo-ready. [Create and review pull requests](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests).

After the merge, start the next task by switching to `main`, pulling with `--ff-only`, and creating a fresh branch. Do not force-push a teammate's branch, work simultaneously in one shared folder from several laptops, or replace the repository with emailed ZIP files once shared history is established.

## When changes conflict

Tell your teammate which files overlap. With your own work committed and a clean working tree, stay on your feature branch and bring in the current shared work:

```text
git fetch origin
git merge origin/main
git status
```

If Git reports conflicts, ask Codex to explain both sides and combine the intended behavior. Preserve your teammate's changes, remove conflict markers, run the affected checks, and review the final diff. Stage the specific resolved files, commit the merge, and push your feature branch normally. Do not solve a conflict by blindly choosing “ours” or “theirs”, deleting `.git`, or using a force push. For a Poetry lock conflict, the dependency owner reconciles `pyproject.toml`, regenerates the lock once, and tests the result. [GitHub conflict guidance](https://docs.github.com/en/pull-requests/reference/merge-conflicts).

Useful prompt:

> Read our branch and origin/main changes. Explain the conflict and propose a resolution that preserves both teammates' intended behavior. Apply it, run the relevant checks, and show the diff. Keep our history and secrets intact; push only to our approved feature branch when that action is already authorized.

At the end, put run instructions, actual checks, and remaining limitations in the README. Keep the GitHub repository separate from Cloudflare deployment permissions: collaboration access does not grant access to the AI Realist production website. Git and GitHub references checked on **23 September 2026**.
