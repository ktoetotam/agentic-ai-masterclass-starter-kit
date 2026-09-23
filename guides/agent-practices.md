# Configure your workshop agent

The starter includes project instructions, ten skills and a small Codex configuration. Together they give your group repeatable working habits. Complete [setup](setup.md), open **your own project folder** in Codex, then use this guide. Official OpenAI documentation was searched and opened on **23 September 2026** before these files were written.

## What the files do

| File | Purpose | Your group's responsibility |
| --- | --- | --- |
| `AGENTS.md` | Shared instructions for how Codex works in this project | Keep commands, boundaries and completion checks accurate |
| `.codex/config.toml` | Supported settings for model, effort, web search and subagent defaults | Review it and confirm the effective settings in your client |
| `.agents/skills/` | Ten reusable workflows for setup, challenge work and deployment | Select the skill that matches the task |
| `pyproject.toml` and `poetry.lock` | Declared and resolved Python dependencies | Change together through Poetry; assign one lockfile owner |
| `poetry.toml` | Project-local Poetry settings | Keep the virtual environment inside this project |
| `.env.example` / `.env` | Variable names with placeholders / private local values | Track the example; keep real values out of Git and public files |

Codex reads applicable `AGENTS.md` guidance at the start of a run. It combines global guidance with project instructions, with more specific instructions later in the chain. `AGENTS.override.md` takes precedence over `AGENTS.md` in the same directory. Start a fresh task after changing instructions and ask which files were loaded. A Markdown instruction describes expected behaviour; it does not itself set a runtime model or create a security boundary. [Official AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Search, then open the official documentation

When changing configuration, use this sequence:

1. Search the **official vendor documentation** for the exact feature and relevant product/version.
2. Open and read the matching page. Check actual setting names, accepted values, file location and whether it is a user, project or organisation setting.
3. Apply the smallest change in the project, preserving unrelated settings.
4. Validate the file and confirm the effective behaviour. Record the supporting URL and any limitation.

For this workshop, that applies to `AGENTS.md`, Codex configuration, dependency/environment setup and deployment settings. Search snippets, old blog posts and a model's memory are not enough. An unavailable page is a reason to identify the unresolved setting and use the supported fallback, not to invent a key.

Try this prompt:

> Before changing configuration, search the relevant official documentation and open the page. Verify the exact fields and version support. Explain the project-level change briefly, preserve unrelated settings, apply it within my request and show how you checked it.

## Choose Luna or Sol deliberately

These are **workshop recommendations**, starting from OpenAI's current guidance. Use the models and effort levels that your account and client actually offer. Availability and UI labels can vary by rollout and workspace settings. [Models](https://learn.chatgpt.com/docs/models).

| Work to do | Starting model | Effort | Workshop example |
| --- | --- | --- | --- |
| A narrow, well-defined task | GPT-6 Luna, `gpt-6-luna` | `high` | Inventory source files; extract a known set of fields; review broken links |
| Building and integrating a prototype | GPT-6 Sol, `gpt-6-sol` | `medium` | Connect invoice parsing, validation and a review screen |
| Difficult reasoning or consequential review | GPT-6 Sol, `gpt-6-sol` | `high` | Trace an intermittent bug; review data boundaries; resolve conflicting requirements |

For a trivial edit, try a lower supported effort when speed matters. Increase effort if the work needs deeper checking. Evaluate the result with the same small input rather than assuming a higher setting fixes every failure. Higher effort and parallel agents use more time/tokens. Luna supports effort up to Max, not Ultra; neither Max nor Ultra is a workshop requirement. [Model effort guidance](https://learn.chatgpt.com/docs/models#pick-a-reasoning-effort).

**Set the parent model in the app's model/Power controls.** Where available, open Advanced to choose the exact model and effort. The CLI offers `/model`. Writing “use Sol” in `AGENTS.md` does not prove that an already-running task changed model. Inspect the active model/effort and start a fresh task when applying project defaults. If a requested option is absent, use an available supported model and record the difference; do not label it as the requested model.

## The included project configuration

The starter's `.codex/config.toml` sets:

```toml
model = "gpt-6-sol"
model_reasoning_effort = "medium"
web_search = "live"

[agents]
max_concurrent_threads_per_session = 2
default_subagent_model = "gpt-6-luna"
default_subagent_reasoning_effort = "high"
```

`model` and `model_reasoning_effort` specify parent defaults. `web_search = "live"` selects live web retrieval; it does not force a search on every turn or bypass network policy. The `AGENTS.md` instruction supplies the requirement to search and open official documentation before configuration changes. [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic).

The `[agents]` settings choose child-agent defaults and cap open child tasks; the cap **excludes the primary agent**. Two is our small-group usage/coordination choice. Demanding delegated work should explicitly request Sol with appropriate effort. Explicit spawn settings override these defaults; a selected custom-agent file can override them again. This starter does not define custom agent files. [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference), [subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents#global-settings).

Project `.codex/` settings load only for a trusted project. Review the starter, then use the client's normal trust workflow if permitted by your organisation. Do not disable security controls or alter global configuration to make these defaults load. Task/CLI overrides and organisation policies can affect the effective result; check the desktop model picker for the current task too. [Configuration scope and precedence](https://learn.chatgpt.com/docs/config-file/config-basic).

This file changes no approval policy, sandbox setting, credentials or paid-service configuration. Defaults do not grant access to unavailable models or extra subscription usage. If a current client rejects a key, check its version and the official reference before adapting the project file.

## Use parallel agents for independent work

The workshop `AGENTS.md` explicitly requests delegation when useful independent pieces exist. Current local Codex clients support delegation requested by the user or applicable project/skill instructions. Start with reading/review tasks; concurrent edits need clear ownership. Subagents inherit the parent's permission context and consume additional usage. [Official subagent guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents).

A useful split for the accountant prototype is:

- **Luna, high:** inspect the invoice fixtures and return their field schema, edge cases and source locations; do not edit files.
- **Sol, high:** review the proposed arithmetic and duplicate rules; return specific failure cases; do not edit files.
- **Parent, Sol, medium:** build the interface while those independent reviews run, then integrate their findings and verify the complete workflow.

For implementation agents, give each a separate file/module. Name the owner of `pyproject.toml`, `poetry.lock`, `package.json`, npm lockfiles and shared configuration. Tell every agent to preserve other contributors' edits. The parent keeps integration responsibility and waits for the promised results before reporting completion. Two people opening separate Codex sessions is group collaboration; each session's subagent cap does not limit the whole group's total usage.

Example prompt:

> Use two parallel subagents. Ask one Luna agent at high effort to inspect the sample input and report edge cases without edits. Ask one Sol agent at high effort to review the proposed validation rules without edits. Specify those settings through the supported spawn controls and report any unavailable option. While they work, implement the interface yourself. Wait for both, incorporate useful findings and verify the complete result. Do not change dependency files in parallel or spawn further agents.

If delegation is unavailable, complete the two reviews sequentially and say so. If there is only one small task, keep it in the main agent. Repeatedly splitting one file among agents usually creates coordination work rather than progress.

## Keep dependencies and variables reproducible

Use **Poetry** for the project's Python dependencies: `poetry add PACKAGE` for a runtime package, `poetry add --group dev PACKAGE` for a development tool, and `poetry run python ...` to execute within the project environment. Keep `pyproject.toml` and `poetry.lock` together in Git. The shared `poetry.toml` requests an in-project `.venv`, which stays untracked. uv bootstraps the Python interpreter and Poetry tool; it is not a second project dependency manager. The `$masterclass-setup` skill carries the platform installation reference and validation steps.

Put local variable values in `.env` and keep the example file to variable names and harmless placeholders. The application must explicitly load its required variables; having a `.env` file on disk does not load it into every process. Keep tokens out of the frontend, `public/`, terminal output and commits. Inspect the **names and presence** of required variables rather than printing their values. Use the starter's documented loader/example when adding integrations.

Each group uses one private repository. Each person works in their own clone on a feature branch, agrees file ownership and shares reviewable commits. One person owns dependency changes at a time. Stage named files, inspect the staged diff and never force-push over a teammate's work. Your private repository is still not a place to store API keys or confidential data without permission.

## Verify the working agreement

Start a new Codex task from the project root and use:

> Read the active AGENTS.md instructions and the included skills. Explain which instruction/configuration files apply, which model and effort are actually active if you can inspect them, how Python dependencies are tracked, and where private variables belong. Run the readiness check. Do not print secrets, change global settings, install optional tools or deploy anything.

The expected result is a clear distinction between requested defaults and verified runtime settings, a successful readiness report or an actionable missing-tool list, and agreement on the first small input-to-output workflow. Confirm the actual model in the app if Codex cannot inspect it reliably.
