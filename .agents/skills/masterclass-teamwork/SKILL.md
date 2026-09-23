---
name: masterclass-teamwork
description: Help a participant install Git and clone the masterclass starter; later join a group repository when assigned.
---

# Learn Git with the starter project

Read `guides/teamwork.md` when available. The first session is **Git and the starter repository only**. Help each participant clone `https://github.com/ktoetotam/agentic-ai-masterclass-starter-kit.git` into a new folder, open that folder in Codex, and inspect `git status`. Preserve any existing ZIP-based work. Participants have read access to the starter and must not push to it. Do not initialize inside the clone.

Group repositories, invitations, shared branches, and pull requests come later. Load `references/group-repositories.md` only after the facilitator has assigned the actual group, owner, repository URL, and members. Never guess those values.

## Local setup and joining

- Check `git --version`; the workshop targets Git 2.55.0 or newer. If needed, use `$masterclass-setup` for user-account installation, with no global identity changes. Inspect the working folder, status, repository root, and remotes before changing Git state.
- For the designated owner in an extracted standalone kit, run `node scripts/setup-team-repo.mjs --team <assigned-slug>`. It creates a local repository only. A refusal for an enclosing or unrelated repository means preserve that history and choose the correct folder; never delete `.git` to bypass it.
- For a teammate joining an existing repository, clone the approved URL into a separate local folder, open that folder in Codex, set their own repository-local identity if needed, and use the committed project lockfiles. Do not reinitialize the clone or copy a teammate's `.env` or `.venv`.
- Establish the participant's intended commit name/email before setting `git config --local user.name` or `user.email`. Keep tokens out of remote URLs and conversations.
- Prepare and review local work while remote information is pending. Creating a remote repository, granting access, or publishing must have an approved destination and authorization. Private is the workshop default. Do not change an existing remote or visibility automatically.

## Collaboration

Give each participant a small responsibility and their own branch from current `main`. Use `git pull --ff-only` when updating `main` and stop to inspect divergence. Keep dirty work in its current branch until preserved. For new branches, use `codex/<participant>-<task>` unless the group chose another convention.

Stage specific reviewed paths, inspect the staged diff, and commit a small working change. Never blindly stage the whole folder. Preserve the group's reviewed `.codex/config.toml` and stage that exact file when needed; do not stage the whole `.codex` directory or replace shared project settings with one participant's personal configuration. Include `.env.example` only when it contains safe placeholders; exclude `.env`, `.dev.vars`, private data, generated outputs, virtual environments, and credentials. Every participant keeps their own local secrets; never duplicate `.env` values into shared configuration or other tracked files. Ignore rules do not protect a secret already tracked in Git.

Push to the approved feature branch when authorized, create a pull request into `main`, and ask a teammate to review before merging. Do not force-push or revert others' edits. If a PR is created with an available Codex app attachment tool, attach it to the current task.

One person owns dependency changes and commits `pyproject.toml` with `poetry.lock`. Others install from the lockfile. For merge conflicts, inspect both changes, preserve both intended behaviors, test the combined result, and commit the resolution. Escalate an unclear product decision to the teammates rather than silently discarding one side.

Report the actual repository location, branch, checks, and whether the changes are local, committed, pushed, or awaiting review. Do not describe a local repository as synchronized or remotely published.
