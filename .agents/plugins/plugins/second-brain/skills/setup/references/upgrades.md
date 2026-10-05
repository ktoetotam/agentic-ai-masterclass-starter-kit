# Push further (afternoon)

Ideas for the "ambitious" block once the sample brain works and the participant's own notes are in. Each one keeps the same rule: answers cite the original note in `raw/`, and `brain.py verify` still passes.

| Upgrade | How | Watch out |
| --- | --- | --- |
| PDFs | `pypdf` is in the starter's shared libraries. If `poetry run python -c "import pypdf"` fails, run `poetry install`, then import again. Pages are marked `<!-- page N -->` in the raw note. | Scanned pages have no text; the importer reports them. OCR is not included. Check one PDF's extracted text against the original. |
| Meeting transcripts | Export the transcript as `.txt` or `.md` from Teams, Zoom or Meet and import it. Speaker lines keep their line numbers for citations. | Transcripts contain other people's words; only use meetings they may share with this AI service. |
| Saved web pages | Ask the agent to save an article as Markdown in a separate `clips/` folder, with its URL and date at the top, then import that folder. | Only pages they may store. A saved copy can go stale; keep the date. |
| Word files | Save as PDF or text first. A developer can add `python-docx` with Poetry and extend the importer. | Formatting and tables may not survive conversion; check the result. |
| Synthesis pages | Ask for a timeline, a comparison or "everything about <person>" as a topic page with citations. | Synthesis is where the agent may over-generalise. Verify every line and spot-check against the notes. |
| Health check | Ask: "Find contradictions, stale facts, pages without links and questions the notes leave open." Then run the check skill. | The agent proposes; the participant decides what is true. |
| Bigger collections | Hundreds of notes still work: search uses SQLite full-text search. Semantic search needs extra tools such as qmd (local, Node, downloads large model files) or an embeddings API. | An embeddings API sends the text to another provider and may cost money: approval and budget first. Large downloads may be blocked on work laptops. |
| A question-answering web page | The developer track (`masterclass-knowledge`) builds an app on the same `raw/` folder; `brain.py verify` and `brain.py eval` serve as its tests. | Never deploy private notes. A static website cannot protect them. |
| A shared team brain | Fictional or approved notes only, in a private group repository, in a folder that is not ignored. | Never in `public/` or a public repository. Agree who may add notes. |

Show the result in the demo: one question answered from new material, one honest failure from the "What the agent got wrong" table, and what a team would need to use it for real.
