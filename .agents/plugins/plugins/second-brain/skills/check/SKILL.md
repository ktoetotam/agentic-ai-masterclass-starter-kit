---
name: check
description: Check the participant's second brain end to end - Python, search and Git safety (doctor), citations, links and waiting notes (verify), the four sample test questions and the re-import test (eval) - and report in plain language what works and what to fix. Use after setup or ingest, before the demo, or when someone asks whether their second brain works.
---

# Check the second brain

The helper is `poetry run python output/second-brain/.brain/brain.py`, written `brain.py` below; run it from the project root. This skill reads and tests. It writes only the test answers file and, if used, the browser view.

1. `brain.py doctor`: Python, search, the brain folder, private notes kept out of Git, and Obsidian or the browser view.
2. `brain.py verify`: every quote is on the cited line of the raw note, links resolve, every page is in the index and no notes are waiting.
3. If the sample notes are imported (`raw/01-project-plan.md` exists):
   - `brain.py eval` lists the four test questions.
   - Answer each with the ask procedure: search, read the raw lines, cite with links that start with `raw/`. Do not open `data/knowledge/evaluation.json`; the test is whether the brain finds the answers itself.
   - Save `[{"id": "...", "answer": "..."}]` to `.brain/eval-answers.json` in the brain folder.
   - `brain.py eval --answers .brain/eval-answers.json --source data/knowledge` grades the answers and checks that importing the same notes again adds nothing.
4. With own notes only, ask the participant for two questions whose answers they know and one they know is not in the notes. Answer them with the ask procedure and let them judge.

## Report

| Status | Check | What it means |
| --- | --- | --- |
| Works | ... | ... |
| Fix | ... | One plain sentence and the fix |
| Optional | ... | ... |

- Map the output: OK and PASS → Works; PROBLEM, FAIL and NEEDS SETUP → Fix; WARNING and OPTIONAL → Optional.
- Typical fixes: ingest a waiting note again, correct a quote or line, add a page to the index. For Python or Git safety, use the second-brain setup skill.
- Say what the check proves and what it does not. It proves that each quoted passage exists where it is cited and that the sample questions are answered correctly. It does not prove that summaries are complete or that nuance was understood, so suggest spot-checking one topic page against its notes.
- Demo tip: the budget question (a fact that changed), the venue question (still tentative) and the door code (not in the notes) show in under a minute that the brain is honest.
