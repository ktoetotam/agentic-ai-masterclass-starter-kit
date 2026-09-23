# Fictional workshop inputs

Everything in this folder is made up for the masterclass. Company names, people, events, quotes, sales, invoices and contacts are fictional. Domains ending in `.invalid` cannot be used as real websites or email destinations. There are no real bank details. Label public demos “Fictional workshop data.”

Use these files immediately when you cannot bring approved work material. Preserve the originals; write results under `output/`. The fixture dates are deliberate, not a live news feed.

| File or folder | Try it with | What it exercises |
| --- | --- | --- |
| `company-brief.md` | Website, HTML deck, media studio | Audience, approved claims, brand voice and CTA |
| `leads.csv` | Market & lead scout | Explainable scoring, missing data, outreach drafts |
| `knowledge/` | Second brain | Revision, contradiction, answerable and missing facts |
| `media/storyboard.md` | HTML deck, media studio | Narrative, captions and a no-generator fallback |
| `invoices/` | Accountant agent | Duplicate detection, arithmetic, missing currency |
| `news/feed.xml` and `news/source-notes.md` | News radar | Deduplication, dates, evidence and offline ingestion |
| `localisation/` | Localisation agent | Glossary, variables, plural forms and locale formats |
| `sales.csv` | Spreadsheet killer | Reconciliation, filters and scenario calculations |
| `problem-brief.md` | Bring your own problem | A complete input/output workflow |

## Expected checks

**Sales:** 12 source rows, 110 units, EUR 13,250.00 revenue, EUR 6,625.00 cost, EUR 6,625.00 gross profit. Amounts are stored in integer EUR cents. Revenue means the entire row total, not unit price. A scenario that raises all revenue by 10% while leaving costs unchanged yields EUR 14,575.00 revenue and EUR 7,950.00 gross profit. No tax calculation is implied.

**Invoices:** Read the three `.txt` files only. Two represent the same invoice. After deduplication there are two invoice records; the second requires review for missing currency and a stated gross total that disagrees with line arithmetic. `invoices/expected.json` is an answer key, not source evidence.

**Knowledge:** Index the four `.md` documents only. `knowledge/evaluation.json` is an answer key; including it in retrieval would invalidate the exercise. A revised budget supersedes the earlier plan, the current venue is explicitly provisional, and the office door code is absent.

**News:** The feed has five items, one of which duplicates an earlier story by GUID/link; retain four unique items. One story has no publication date. All news items are fictional; source notes are the evidence for offline summaries. `.invalid` links are identifiers, not live sources to fetch.

**Leads:** Four fictional companies. Score known facts, mark absent facts as unknown and do not guess the missing email address. No message should be sent.

**Localisation:** Translate all seven keys while preserving `{company}`, `{count}`, `{date}` and `{amount}` where they appear. Both `seats.one` and `seats.other` exist because plural logic needs an explicit choice. More complex target-language plural rules may require a deliberate schema change, which must be documented.

Text-first fixtures keep setup small. To exercise file formats later, ask Codex to make an `.xlsx` copy from `sales.csv` or a printable PDF from an invoice, then inspect it. Such generated files test conversion, not extraction accuracy on a real scanned invoice.
