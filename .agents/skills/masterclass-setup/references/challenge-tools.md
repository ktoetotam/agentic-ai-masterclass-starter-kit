# Optional tools by challenge

Use this only after a participant chooses a challenge. First read its matching `masterclass-*` skill and inspect the available inputs. The starter's local preview, Python standard library, Node and browser cover many first versions. Check current official documentation and the package's supported Python/Node versions before adding anything. Prefer a user-account install and a prebuilt wheel. For Python use `poetry add PACKAGE` (or `poetry add --group dev PACKAGE` for a development-only tool); for JavaScript use project-local `npm install PACKAGE` or `npm install -D PACKAGE`. Review and commit both the manifest and lockfile. Never use global npm or `pip install` for project dependencies.

| Challenge | First working version | Add only when needed |
| --- | --- | --- |
| Company website | Plain HTML, CSS and JavaScript with the included local preview. | A framework chosen by the participant; project-local Playwright for browser checks if an existing browser is insufficient. Browser downloads are optional and may be large or blocked on managed laptops. |
| Market and lead scout | Browser/search tools, public pages and CSV/JSON fixtures. | `httpx` for repeatable Python fetching and `feedparser` for RSS/Atom feeds. Paid search/enrichment APIs require a separate budget. |
| Second brain | Text/Markdown files plus Python `sqlite3` or JSON, with cited source locations. | `pypdf` for text PDFs. Image-only PDFs need OCR or a supplied text export; do not silently treat OCR as included. Hosted embeddings/vector stores are optional. |
| Beyond PowerPoint | HTML slides, keyboard controls and browser Print to PDF. | `python-pptx` or local `pptxgenjs` only if an editable PowerPoint file is required; Playwright only for automated export/screenshots. |
| Media studio | Storyboard, existing/owned images, participant-recorded audio, captions and browser playback. | A user-owned FFmpeg executable for video assembly after checking its current official download options; paid image/audio/video providers only within an agreed budget. |
| Accountant agent | CSV invoices, Python `csv`/`decimal`, deterministic reconciliation and exception reports. | `pypdf` for text PDFs, `openpyxl` for Excel workbooks, or a vetted extraction service only if the actual input requires it. Scanned documents need OCR or manual review. |
| News radar | Public RSS/HTML, Python XML tools, deduplication and a local dashboard. | `feedparser` or `httpx` if standard-library parsing/fetching is insufficient. Scheduling and narration are stretch goals. |
| Localisation agent | Plain text/Markdown, glossary and placeholder checks. | `python-docx` for Word files, `openpyxl` for spreadsheets or another format library only when that format is in the chosen input. |
| Spreadsheet killer | CSV, Python `csv`/`decimal` and a browser dashboard/calculator. | `openpyxl` for `.xlsx`; `pandas` only when the data size/transformations justify it. No database server for the first version. |
| Bring your own problem | One input-to-output slice with local fixtures. | Select a format or connector after identifying the real input, output and approval boundary. |

After adding a package, run the smallest import/command and a realistic sample. Confirm the lockfile changed only as intended and hand over exact startup commands. If installation fails, keep the simple local path and record the missing capability; do not bypass compiler, OS, company-policy or payment restrictions to complete a demo.

Official starting points: [Poetry dependency commands](https://python-poetry.org/docs/cli/#add), [npm dependency flags](https://docs.npmjs.com/specifying-dependencies-and-devdependencies-in-a-package-json-file/), [Playwright browser installation](https://playwright.dev/docs/browsers), [FFmpeg downloads](https://ffmpeg.org/download.html). Recheck them at the time of installation.
