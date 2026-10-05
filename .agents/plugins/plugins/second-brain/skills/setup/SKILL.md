---
name: setup
description: Set up the second brain challenge for a non-technical participant - check the computer, make the challenge skills available, create the brain folder, import the sample or approved notes, build the first wiki, open it in Obsidian or the browser, and prove it works with test questions. Use when someone chooses the second brain build, says "set up my second brain", or the brain folder is missing or broken.
---

# Set up the second brain

You set up a working second brain: a folder of notes that an AI agent keeps organised and answers questions from, always pointing to the exact source passage. The participant is usually non-technical. Explain each step in one plain sentence, ask one question at a time, and do the technical work yourself within the boundaries below.

**Paths.** This skill's folder (the one containing this SKILL.md) holds `scripts/brain.py` and `references/`. The brain lives in `output/second-brain/` in the project unless the participant chooses another folder; `output/` is already ignored by Git. After step 4, always run the copy at `output/second-brain/.brain/brain.py`. Run Python from the project root as `poetry run python ...`. If Poetry is unavailable, `python3` (Mac) or `py` (Windows) also works, because the helper uses only the standard library.

## 1. Say what will happen

Tell them, in three short lines:

- you will check their computer, create the brain folder and fill it from sample notes first;
- when the agent reads notes, the AI service (OpenAI or Anthropic) receives that text, so a local folder does not mean a local AI;
- nothing is sent anywhere else, nothing is installed without asking, and nothing is published.

## 2. Check the computer

1. If `scripts/check-setup.mjs` exists, run `node scripts/check-setup.mjs`. If Project Python or Poetry needs setup, stop and give a paste-ready message such as "Use $masterclass-setup to install Python 3.14.7 and Poetry in my user account and prepare this project." Name skills the way this client invokes them.
2. Run `poetry run python <this skill folder>/scripts/brain.py doctor`. Only Python is required at this point; the brain folder does not exist yet.

## 3. Make the challenge skills available

If `scripts/activate-challenge.mjs` exists, run `node scripts/activate-challenge.mjs second-brain`. It copies the ingest, ask and check skills into `.agents/skills/` for Codex and `.claude/skills/` for Claude Code, without overwriting copies someone edited. Codex's sandbox protects `.agents/`. If the script reports BLOCKED, tell the participant in one line that Codex will ask permission to copy the challenge skills into this project's `.agents` folder and that it only copies files inside this project, then request approval to run the same command outside the sandbox. If they decline, carry on: the skills still work when read by path. In a new chat they appear as `$second-brain-ingest`, `$second-brain-ask` and `$second-brain-check` in Codex, or `/second-brain-ingest` and so on in Claude Code. With the plugin installed they are `/second-brain:ingest` and so on. If none of this is available, read the skills by path from `.agents/plugins/plugins/second-brain/skills/<name>/SKILL.md`.

## 4. Create the brain

Run `poetry run python <this skill folder>/scripts/brain.py init --brain output/second-brain`. It creates `raw/`, `wiki/`, `BRAIN.md` (the rules), `index.md` and `log.md`, and copies the helper to `output/second-brain/.brain/brain.py`.

Run `doctor` again with the copy. **Private notes stay out of Git** must be OK before anything real is imported. If it is not, keep the brain under `output/` or, with their agreement, add the folder to `.gitignore`. Never commit or push brain contents.

Another location, such as an existing Obsidian vault, only on request. Use a new subfolder inside it, for example `<vault>/AI brain`, so the agent never edits their own notes, and check Git status there too.

## 5. Choose the notes

Ask: "Shall we start with the fictional sample notes, or your own notes?" Recommend the sample first.

- **Sample:** `data/knowledge/`, four fictional notes. The answer key `evaluation.json` is skipped automatically.
- **Own notes:** only after they confirm they are allowed to send them to this AI service. Ask for one specific folder, never their whole home or Documents folder, and start with 5–20 notes. `.md` and `.txt` work now. Text PDFs work through pypdf, which the starter installs (`references/upgrades.md`). For Word files, ask them to save a PDF or text copy.

Run `brain.py import <folder>` and explain the result in plain words: how many notes were added, which were skipped and why.

## 6. Build the first wiki

Follow the second-brain ingest skill for the imported notes; read its SKILL.md if it is not loaded. For the sample that is four notes. Finish when `brain.py verify` reports no problems.

## 7. Let them see it

Ask: "Would you like Obsidian, a free notes app with a link map, or a page in your browser with nothing to install?"

- **Browser:** run `brain.py html`, give the full path of `output/second-brain/brain.html` and ask them to double-click it. Regenerate it after each ingest.
- **Obsidian:** follow `references/obsidian.md`. They download and install it themselves from the official site; you never download or run installers for them.

## 8. Prove it works

Follow the second-brain check skill: answer the four sample questions with the ask procedure, grade them with `brain.py eval`, and run the re-import test. With own notes only, ask them for two questions whose answers they know and one they know is not in the notes.

## 9. Report

Give one table with **Ready / Needs attention / Optional** for: Python and search, brain folder, private notes kept out of Git, notes imported, wiki built (verify), view (Obsidian or browser), test questions. Then say where the brain is (full path), how to open it, and give two paste-ready messages:

- "Use $second-brain-ask. What is the current budget for Project Lantern, and did it change?"
- "Use $second-brain-ingest. Add the notes in <folder> to my second brain."

Append "setup complete" to `log.md`. Mention `references/upgrades.md` for the afternoon: PDFs, meeting transcripts, saved web pages, bigger collections.

## Boundaries

- Never edit, move or delete the participant's original notes or anything in `raw/`.
- Never read folders they did not name. The importer skips hidden files, `.env` files and names that look like credentials; if you notice other sensitive files, say so and leave them out.
- Never install apps, browser extensions or packages without their agreement. Obsidian is optional and they install it.
- Keep the brain out of `public/`, deployments, Git and screenshots unless it holds only the fictional sample.
- Do not report a check as passed unless it ran in this session.
