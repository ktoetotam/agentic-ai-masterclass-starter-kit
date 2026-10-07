---
name: setup
description: Set up the accountant agent challenge for a non-technical participant - check Python and the libraries, make the challenge skills available, create the books folder, collect the September documents of the fictional Juniper Workshop Lab, and read the Stripe sandbox or its snapshot. Use when someone chooses the accountant or invoice agent build, says set up my accountant agent, or the books folder is missing or broken.
---

# Set up the accountant agent

You set up a working books folder: every document of one month copied in, each as numbered text lines, ready for the agent to extract and for scripts to check. The participant is usually non-technical. Explain each step in one plain sentence, ask one question at a time, and do the technical work yourself within the boundaries below.

**Paths.** This skill's folder holds `scripts/books.py` and `references/`. The books live in `output/accountant/` (already ignored by Git). After step 4, always run the copy at `output/accountant/.books/books.py`, written `books.py` below. Run Python from the project root as `poetry run python ...`; `python3` (Mac) or `py` (Windows) also work, because the helper needs only the standard library plus the starter's pypdf and openpyxl.

## 1. Say what will happen

Three short lines:

- you will create the books folder and fill it with the September documents of Juniper Workshop Lab, a fictional company in Munich: invoices, bills, receipts, emails, bank statements and Stripe payments;
- when the agent reads a document, the AI service (OpenAI or Anthropic) receives its text, so a local folder does not mean a local AI;
- nothing is paid, sent or changed anywhere: Stripe is read with a read-only sandbox key, documents are copied, never moved.

## 2. Check the computer

1. If `scripts/check-setup.mjs` exists, run `node scripts/check-setup.mjs`. If Project Python or Poetry needs setup, stop and give a paste-ready message such as "Use $masterclass-setup to install Python and Poetry in my user account and prepare this project." Name skills the way this client invokes them.
2. Run `poetry run python <this skill folder>/scripts/books.py doctor`.

## 3. Make the challenge skills available

If `scripts/activate-challenge.mjs` exists, run `node scripts/activate-challenge.mjs accountant-agent`. It copies the extract, reconcile, package and check skills into `.agents/skills/` for Codex and `.claude/skills/` for Claude Code, without overwriting copies someone edited. Codex's sandbox protects `.agents/`: if the script reports BLOCKED, say in one line that Codex will ask permission to copy the challenge skills into this project's `.agents` folder and that it only copies files inside this project, then request approval to run the same command outside the sandbox. If they decline, carry on: the skills still work when read by path from `.agents/plugins/plugins/accountant-agent/skills/<name>/SKILL.md`. In a new chat they appear as `$accountant-agent-extract` and so on in Codex, `/accountant-agent-extract` in Claude Code, or `/accountant-agent:extract` with the plugin installed.

## 4. Create the books

Run `poetry run python <this skill folder>/scripts/books.py init --books output/accountant --pack data/accountant-pack`. It creates `inbox/`, `text/`, `records/`, `out/`, `BOOKS.md` (how the books work, with the company's house rules) and `books.json` (month 2026-09, scenario date 8 October 2026), and copies the helper to `output/accountant/.books/books.py`.

**Private books stay out of Git** must be OK in `books.py doctor` before anything real is added.

## 5. Choose where the documents come from

Ask: "Shall we use the files in the starter kit, or the Google Workspace account?" Recommend the files first.

- **Files (default, works offline):** `data/accountant-pack/`: the shared accounting Drive folder in `drive/` and Mira Beispiel's mailbox in `mailbox/eml/`. `answer-key/` is skipped automatically: it is for grading only.
- **Google Workspace:** only with the workshop account the facilitator gave them (`...@hypefree.ai`), never a work account. Connect Google Drive and Gmail read-only (`references/connectors.md`), check that the folder "Juniper accounting (fictional)" and Mira's emails are visible, and save the files into `output/accountant/downloads/`. The content is the same as the starter files, so switch to them if a connector fails.

## 6. Collect

Run `books.py collect` (add `--add output/accountant/downloads` for downloaded files). Explain the result in plain words: how many documents, how many need a record, how many must be read as images, which were found more than once. Email attachments count as documents of their own.

## 7. Stripe

Ask whether the facilitator handed out a read-only Stripe sandbox key.

- **Yes:** the participant opens the project's `.env` file and adds `STRIPE_API_KEY=` followed by the key themselves. Never ask for the key in the chat and never print it. Run `books.py stripe`. Optional: connect the Stripe MCP server read-only as well (`references/connectors.md`).
- **No, or the key fails:** run `books.py stripe --snapshot`. The snapshot is the same sandbox, saved as CSV files.

## 8. Report

One table with **Ready / Needs attention / Optional** for: Python and libraries, books folder, private books out of Git, documents collected, Stripe (key or snapshot). Then give the next message:

- "Use $accountant-agent-extract. Write the records for the documents in my books, one at a time, and run verify."

Append "setup complete" to `output/accountant/log.md`.

## Boundaries

- Never edit, move or delete documents in `data/`, in `inbox/` or in a connected Drive or mailbox.
- Never send, pay, approve, mark as paid or create anything in Stripe, Gmail or Drive. The agent prepares; people act.
- Only sandbox keys: `books.py` refuses live Stripe keys. Keys go into `.env` by the participant, never into chat, files in Git or screenshots.
- Use the participant's own business documents only after they confirm they may send them to this AI service, and only from one folder they name. Keep them under `output/`.
- Do not report a check as passed unless it ran in this session.
