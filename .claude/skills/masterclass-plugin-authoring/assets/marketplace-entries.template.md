# Marketplace entries for a new plugin

Add one entry to each file. Keep the order of plugins the same in both.

## `.agents/plugins/marketplace.json` (Codex)

```json
{
  "name": "<plugin-name>",
  "source": {
    "source": "local",
    "path": "./.agents/plugins/plugins/<plugin-name>"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

`installation` is `AVAILABLE`, `INSTALLED_BY_DEFAULT` or `NOT_AVAILABLE`; workshop challenges stay `AVAILABLE` because their setup skill activates them. `authentication` is `ON_INSTALL` or `ON_FIRST_USE`; it matters only for plugins with apps or MCP servers.

## `.claude-plugin/marketplace.json` (Claude Code)

```json
{
  "name": "<plugin-name>",
  "source": "./.agents/plugins/plugins/<plugin-name>",
  "description": "<Short challenge description: what participants build>"
}
```

Paths are written from the repository root, start with `./` and never contain `..`. The entry `name` must equal the `name` in the plugin's manifests.
