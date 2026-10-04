# Obsidian (optional)

Obsidian is a free notes app; since February 2025 it is free for work use too. It opens the brain folder directly as a "vault" and shows the links, backlinks and a graph of how pages connect. It is optional: `brain.html` shows the same pages in a browser without installing anything. Nothing in this challenge needs Obsidian plugins, its command-line tool or an MCP server.

## Install (the participant does this)

1. Open the official download page: https://obsidian.md/download
2. **Mac:** open the downloaded file and drag Obsidian into **Applications**. If it asks for an admin password they do not have, drag it into **Home → Applications** instead.
   **Windows:** open the downloaded installer and follow the steps.
3. If the work laptop blocks the installation, use `brain.html` instead. Do not look for workarounds.

`brain.py doctor` reports Obsidian once it is installed in a standard location.

## Open the brain

1. Give them the full path of the brain folder, for example `<project folder>/output/second-brain`.
2. In Obsidian choose **Open folder as vault** and select that folder. If Obsidian is already showing another vault, use the vault switcher at the bottom of the left sidebar to open a different folder as a vault.
3. Start at `index.md`. The graph view is in the left sidebar. Citations are links to the original notes in `raw/`; clicking one opens the note.
4. Obsidian updates by itself while the agent adds pages.

## Good habits

- They can write their own preferences in `BRAIN.md`, for example the wiki language or topics to track.
- They should not edit notes in `raw/`. To add a note, they ask the agent to import it, or write new notes in a separate folder and import that folder.
- Obsidian adds a `.obsidian/` settings folder inside the brain. That is fine and stays out of Git with the rest of `output/`.
- Do not install community plugins during the workshop; the brain does not need them.
