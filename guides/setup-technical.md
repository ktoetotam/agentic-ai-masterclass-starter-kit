# Let Codex set up the tools

You do not need to copy installation commands from this page. The starter kit includes **`$masterclass-setup`**, a Codex skill that checks your computer and helps install Python, Node, Poetry and Git in your own user account. Start with the [illustrated four-step guide](setup.md) if you have not opened the app yet.

## 1. Open your project

Download the starter kit supplied with this guide, unzip it, and open the **agentic-ai-masterclass** folder as a project in Codex. The [setup guide](setup.md#open-workspace) shows where to click.

## 2. Ask Codex to finish setup

Start a **New chat** in that project. Copy and send this message:

<div class="setup-prompt" markdown="1">
<p id="technical-setup-prompt">Use $masterclass-setup. Check my Mac or Windows computer and this project. Install any missing Python, Node, Poetry and Git tools in my user account. Keep my existing work, use Poetry for Python packages, create my local .env, run the readiness check and open the preview. Explain any step that needs a click from me.</p>
<button class="button" type="button" data-copy="technical-setup-prompt">Copy message</button>
<span class="copy-feedback" role="status" aria-live="polite"></span>
</div>

If the skill does not appear, start a new Codex task and ask it to read **`.agents/skills/masterclass-setup/SKILL.md`** in this project.

## 3. Check the result

Codex should report **“Local runtime checks passed”** and open a page saying **“Your workspace is running.”** If a company laptop blocks an installation, show the exact error to your facilitator; Codex can help you continue with the workshop sample files.

## Python and Poetry {#poetry-and-env}

The skill installs the project's locked Python packages with Poetry. You do not need to create or manage a virtual environment yourself. If the readiness check names Python or Poetry, paste that result into the same Codex chat.

## Git {#install-git}

The same skill checks and installs Git. For tomorrow, make your own free [GitHub account](https://github.com/signup), then [get the public starter repository](teamwork.md). Ask **`$masterclass-setup`** to help you clone it into Codex. Groups come later.
