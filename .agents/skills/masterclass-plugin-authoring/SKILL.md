---
name: masterclass-plugin-authoring
description: Create, change, rename or remove a skill, plugin or marketplace entry in this starter so it works the same in Codex and Claude Code - folder layout, both plugin manifests (portable root plugin.json and .claude-plugin/plugin.json), both marketplaces, SKILL.md rules, the Claude mirror and the full verification run. Use whenever someone asks to add or update a skill or plugin, make a new challenge plugin, or edits anything under .agents/skills, .claude/skills, .agents/plugins or .claude-plugin.
---

# Plugin and skill authoring

Every skill and plugin in this starter has **one maintained source** and works in **both clients**. Codex reads `.agents/skills/`, `AGENTS.md`, `.agents/plugins/marketplace.json` and root `plugin.json`. Claude Code reads `.claude/skills/`, `CLAUDE.md` (which imports `AGENTS.md`), `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`. Follow this skill for every new skill, plugin or modification, then run the checks in step 6.

Before changing a format, follow `AGENTS.md`: open the current official page and confirm the keys. Starting points: [Claude skills](https://code.claude.com/docs/en/skills), [Claude plugin manifest](https://code.claude.com/docs/en/plugins-reference), [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins), [Agent Skills spec](https://agentskills.io/specification). If a page contradicts this skill, follow the page and update this skill in the same change.

## 1. Decide what you are making

| You need | Put the source here | Users see it as |
| --- | --- | --- |
| A workshop skill used in this project | `.agents/skills/masterclass-<name>/` | `$masterclass-<name>` in Codex, `/masterclass-<name>` in Claude Code |
| A new challenge (a set of skills one group activates) | `.agents/plugins/plugins/<plugin>/` | after activation `$<plugin>-<skill>` / `/<plugin>-<skill>` |
| One more step in an existing challenge | `.agents/plugins/plugins/<plugin>/skills/<skill>/` | same as above |

Never create:

- wrapper skills whose body only says "read another SKILL.md" - they drift and show up twice;
- edits in generated copies: `.claude/skills/masterclass-*` (made by `scripts/sync-claude-skills.mjs`) or activated copies `.agents/skills/<plugin>-*` and `.claude/skills/<plugin>-*` (made by `scripts/activate-challenge.mjs`);
- a `.codex-plugin/` folder (legacy Codex format; the root `plugin.json` replaces it);
- symlinks for skills or instruction files - Git on Windows checks them out as text files.

## 2. Write the SKILL.md

Start from [assets/SKILL.template.md](assets/SKILL.template.md).

- **Frontmatter:** only `name` and `description`, plus `license`, `compatibility` or `metadata` when needed. Client-only fields (`allowed-tools`, `disable-model-invocation`, `context`, `agents/openai.yaml`) make the two clients behave differently; add one only with a written reason in the skill.
- **`name`:** equals the folder name; lowercase letters, digits and single hyphens; at most 64 characters. Workshop skills start with `masterclass-`. Inside a plugin, the folder is the short step name (`ask`); activation renames it to `<plugin>-ask`.
- **`description`:** one line, 250-450 characters (hard limit 1024). First what it does, then `Use when ...` with the words participants actually say. Avoid a colon followed by a space inside the text, because it breaks the YAML. When two skills overlap, each description names the other route ("For the guided process, use ... instead").
- **Body:** under 500 lines; imperative steps; what to do, not why. Move long material into `references/`, templates into `assets/`, helpers into `scripts/`, linked one level deep with relative paths.
- **Client-neutral wording:** "name skills the way the current client invokes them: `$name` in Codex, `/name` in Claude Code". Write "the agent", not "Codex", unless a step really is client-specific; then give both variants.
- **Plugin skills are self-contained:** bundled files are referenced relative to the skill folder. A project file (`scripts/check-setup.mjs`) is used only with "if it exists", plus a fallback. Refer to sibling skills by their activated name, `<plugin>-<skill>`.
- **Participants are mostly non-technical:** plain words, one question at a time, paste-ready next steps, and the boundaries from `AGENTS.md` (no sending, publishing, paying or installing without the concrete authorization).

## 3. New challenge plugin: the layout

```text
.agents/plugins/plugins/<plugin>/
├── plugin.json                  # portable manifest, read by Codex
├── .claude-plugin/plugin.json   # Claude Code manifest
└── skills/
    ├── setup/SKILL.md           # always: checks, activation, first run
    └── <step>/SKILL.md          # one skill per step participants ask for
```

Copy [assets/root-plugin.template.json](assets/root-plugin.template.json) to `plugin.json` and [assets/claude-plugin.template.json](assets/claude-plugin.template.json) to `.claude-plugin/plugin.json`, then replace every `<...>`.

- `name`, `version`, `description`, `author`, `repository` and `keywords` are **identical** in both manifests. The plugin name is kebab-case and does not start with `claude-` or `anthropic-`.
- Root `plugin.json` allows only the schema's keys (`$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, `extensions`). Codex display settings go under `extensions.com.openai.interface`; `defaultPrompt` is a list of strings.
- Neither manifest needs a `skills` key; both clients scan `skills/`.
- **Any change to a plugin's skills bumps `version` in both manifests**, or installed users keep the old copy.
- The `setup` skill runs `node scripts/activate-challenge.mjs <plugin>` if that script exists, explains a BLOCKED result, and still works by reading skills by path when activation is declined. Copy the pattern from `.agents/plugins/plugins/second-brain/skills/setup/SKILL.md`.

## 4. Register the plugin in both marketplaces

Add one entry to each file using [assets/marketplace-entries.template.md](assets/marketplace-entries.template.md):

- `.agents/plugins/marketplace.json` (Codex): `source` object with `"source": "local"`, policy and category.
- `.claude-plugin/marketplace.json` (Claude Code): `source` string.

Both paths are written from the repository root, start with `./` and never contain `..`. The entry `name` equals the manifest `name`. Both marketplaces list exactly the same plugins.

## 5. Update what points to it

- A new or renamed workshop skill: the skill lists in `AGENTS.md` and `README.md`, the counts in `README.md`, `CLAUDE.md` and `guides/agent-practices.md`, and routing in `.agents/skills/masterclass-guide/` if participants should be sent there.
- A new challenge plugin: `AGENTS.md` (challenge plugin list), `.agents/skills/masterclass-guide/references/challenges.md` and `.agents/skills/masterclass-setup/references/challenge-tools.md`.
- A removed skill or plugin: search the repository for its name and remove every reference.

## 6. Verify - run all of it, report what ran

1. `node scripts/sync-claude-skills.mjs` after any change under `.agents/skills/masterclass-*`.
2. `npm run check:plugins` - manifests, marketplaces and every SKILL.md against the rules above.
3. `npm run check:skills` - the Claude copies match their source.
4. `claude plugin validate --strict .` and `claude plugin validate --strict .agents/plugins/plugins/<plugin>` for each changed plugin, when the `claude` CLI is available.
5. For a new plugin or a manifest change, install it in throwaway client homes so nobody's real configuration changes. Use a folder in your scratch space:

   ```sh
   T=<scratch folder>; mkdir -p "$T/codex/.codex" "$T/claude"
   HOME="$T/codex" CODEX_HOME="$T/codex/.codex" codex plugin marketplace add "$PWD"
   HOME="$T/codex" CODEX_HOME="$T/codex/.codex" codex plugin add <plugin>@ai-realist-workshops
   CLAUDE_CONFIG_DIR="$T/claude" claude plugin marketplace add "$PWD"
   CLAUDE_CONFIG_DIR="$T/claude" claude plugin install <plugin>@ai-realist-workshops
   CLAUDE_CONFIG_DIR="$T/claude" claude plugin details <plugin>
   ```

   Both must report the plugin installed with every skill listed.
6. For a challenge plugin, copy the repository without `.git`, `.venv` and `node_modules` to a scratch folder and run `node scripts/activate-challenge.mjs <plugin>` there twice: the first run reports ACTIVATED for every skill in both folders, the second UP TO DATE.
7. Start a new chat or session and confirm the new skill appears in the client's skill list.

Report each check as passed, failed (with the output) or not run (with the reason). Do not commit or push unless asked.
